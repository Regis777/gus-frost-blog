#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cable le thème Gus & Frost : charge gf-article.css (page article), ajoute le snippet
related-articles, et l'inclut apres {{ article.content }}.

PRE-REQUIS :
  - app avec scopes read_themes + write_themes (sinon HTTP 403).
  - le thème CIBLE doit exister et etre NON PUBLIE (duplique en 1 clic dans l'admin :
    Boutique en ligne > Themes > ... a cote du theme en ligne > Dupliquer).

Securite : n'ecrase jamais aveuglement. Les 2 patchs (theme.liquid, section article)
sont idempotents ; si l'ancre attendue est introuvable, le patch est SAUTE et signale
(a faire a la main via theme/INTEGRATION.md), au lieu de risquer de casser le theme.

Usage :
  python scripts/wire_theme.py --list                 # liste les themes (id, role, nom)
  python scripts/wire_theme.py --theme-id 123456789   # cable ce theme precis
  python scripts/wire_theme.py                         # auto : dernier theme NON PUBLIE
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

from publish import load_env, Shopify, ROOT

CSS_LOCAL = os.path.join(ROOT, "theme", "gf-article.css")
SNIPPET_LOCAL = os.path.join(ROOT, "theme", "related-articles.liquid")

CSS_ASSET = "assets/gf-article.css"
SNIPPET_ASSET = "snippets/related-articles.liquid"

CSS_INCLUDE = (
    "{%- if template.name == 'article' -%}\n"
    "  {{ 'gf-article.css' | asset_url | stylesheet_tag }}\n"
    "{%- endif -%}\n"
)
RENDER_TAG = "{%- render 'related-articles' -%}"

CSS_MARKER = "gf-article.css"
SNIPPET_MARKER = "related-articles"


def gql(sh, query, variables):
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(sh.base + "/graphql.json", data=payload, method="POST")
    req.add_header("X-Shopify-Access-Token", sh.token)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit("HTTP %s GraphQL\n%s" % (e.code, e.read().decode("utf-8", "replace")))
    if data.get("errors"):
        raise SystemExit("Erreur GraphQL : %s" % json.dumps(data["errors"], ensure_ascii=False))
    return data["data"]


def list_themes(sh):
    data = sh._req("GET", "/themes.json")
    return data.get("themes", [])


def read_file(sh, gid, filename):
    q = """
    query($id: ID!, $fn: [String!]) {
      theme(id: $id) {
        files(filenames: $fn, first: 1) {
          nodes { filename body { ... on OnlineStoreThemeFileBodyText { content } } }
        }
      }
    }"""
    d = gql(sh, q, {"id": gid, "fn": [filename]})
    nodes = (d.get("theme") or {}).get("files", {}).get("nodes", [])
    if not nodes:
        return None
    return nodes[0]["body"].get("content", "")


def upsert_file(sh, gid, filename, content):
    m = """
    mutation($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
      themeFilesUpsert(themeId: $themeId, files: $files) {
        upsertedThemeFiles { filename }
        userErrors { filename code message }
      }
    }"""
    files = [{"filename": filename, "body": {"type": "TEXT", "value": content}}]
    d = gql(sh, m, {"themeId": gid, "files": files})
    res = d["themeFilesUpsert"]
    if res["userErrors"]:
        raise SystemExit("themeFilesUpsert erreurs : %s" % json.dumps(res["userErrors"], ensure_ascii=False))
    return res["upsertedThemeFiles"]


def patch_head(sh, gid):
    fn = "layout/theme.liquid"
    body = read_file(sh, gid, fn)
    if body is None:
        return "SAUTE (layout/theme.liquid introuvable)"
    if CSS_MARKER in body:
        return "deja present"
    if "</head>" not in body:
        return "SAUTE (</head> introuvable)"
    new = body.replace("</head>", CSS_INCLUDE + "</head>", 1)
    upsert_file(sh, gid, fn, new)
    return "patché (CSS charge avant </head>)"


def patch_article_section(sh, gid):
    candidates = ["sections/main-article.liquid", "templates/article.liquid"]
    for fn in candidates:
        body = read_file(sh, gid, fn)
        if body is None:
            continue
        if SNIPPET_MARKER in body:
            return "%s : deja present" % fn
        if "article.content" not in body:
            return "%s : SAUTE (ancre 'article.content' introuvable)" % fn
        idx = body.rfind("article.content")
        end = body.find("}}", idx)
        if end == -1:
            return "%s : SAUTE (sortie '}}' de article.content introuvable)" % fn
        insert_at = end + 2
        new = body[:insert_at] + "\n" + RENDER_TAG + body[insert_at:]
        upsert_file(sh, gid, fn, new)
        return "%s : patché (render apres article.content)" % fn
    return "SAUTE (ni sections/main-article.liquid ni templates/article.liquid)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--theme-id", help="id numerique du theme cible")
    ap.add_argument("--allow-live", action="store_true",
                    help="autorise le cablage du theme PUBLIE (live). A n'utiliser qu'en go-live assume.")
    args = ap.parse_args()

    env = load_env()
    sh = Shopify(env)
    themes = list_themes(sh)

    if args.list:
        for t in themes:
            print("%-12s %-12s %s" % (t["id"], t["role"], t["name"]))
        return

    if args.theme_id:
        target = next((t for t in themes if str(t["id"]) == str(args.theme_id)), None)
        if not target:
            sys.exit("Theme id %s introuvable." % args.theme_id)
    else:
        unpub = [t for t in themes if t["role"] == "unpublished"]
        if not unpub:
            sys.exit("Aucun theme NON PUBLIE trouve. Duplique d'abord ton theme en ligne "
                     "(admin > Themes > ... > Dupliquer), ou passe --theme-id.")
        if len(unpub) > 1:
            print("Plusieurs themes non publies :")
            for t in unpub:
                print("  %s  %s" % (t["id"], t["name"]))
            sys.exit("Precise lequel avec --theme-id.")
        target = unpub[0]

    if target["role"] == "main" and not args.allow_live:
        sys.exit("REFUS : le theme cible est PUBLIE (live). Utilise une copie non publiee, "
                 "ou --allow-live si c'est volontaire (go-live).")

    gid = "gid://shopify/OnlineStoreTheme/%s" % target["id"]
    print("Theme cible : %s (id=%s, role=%s)" % (target["name"], target["id"], target["role"]))
    print("=" * 60)

    with open(CSS_LOCAL, "r", encoding="utf-8") as f:
        css = f.read()
    with open(SNIPPET_LOCAL, "r", encoding="utf-8") as f:
        snippet = f.read()

    upsert_file(sh, gid, CSS_ASSET, css)
    print("1. %s : uploade" % CSS_ASSET)
    upsert_file(sh, gid, SNIPPET_ASSET, snippet)
    print("2. %s : uploade" % SNIPPET_ASSET)
    print("3. %s -> %s" % ("layout/theme.liquid", patch_head(sh, gid)))
    print("4. section article -> %s" % patch_article_section(sh, gid))

    print("=" * 60)
    print("Apercu : admin > Themes > '%s' > Apercu, puis ouvre un article du blog 'chiens'."
          % target["name"])


if __name__ == "__main__":
    main()
