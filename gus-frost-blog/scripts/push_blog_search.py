#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajoute la section « Recherche blog » (scopée type=article) au thème LIVE Dawn :
  - upload sections/gf-blog-search.liquid
  - patch templates/blog.json    (section en TÊTE de l'ordre)
  - patch templates/article.json (section en PIED de l'ordre)
Idempotent : ne duplique pas la section si déjà présente.

Usage : python scripts/push_blog_search.py [--theme-id 158654333149] [--dry-run]
"""
import argparse, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import load_env, Shopify  # noqa: E402
import wire_theme as wt                 # noqa: E402

SECTION_KEY = "gf_blog_search"
SECTION_TYPE = "gf-blog-search"
LOCAL_SECTION = os.path.join(ROOT, "theme", "gf-blog-search.liquid")


def split_header(raw):
    """Sépare l'en-tête commentaire /* ... */ du corps JSON."""
    m = re.match(r"\s*/\*.*?\*/\s*", raw, re.S)
    if m:
        return raw[m.start():m.end()], raw[m.end():]
    return "", raw


def patch_template(sh, gid, filename, position, dry):
    raw = wt.read_file(sh, gid, filename)
    header, jtxt = split_header(raw)
    data = json.loads(jtxt)
    already = SECTION_KEY in data.get("sections", {})
    data.setdefault("sections", {})[SECTION_KEY] = {"type": SECTION_TYPE, "settings": {}}
    order = [x for x in data.get("order", []) if x != SECTION_KEY]
    data["order"] = ([SECTION_KEY] + order) if position == "top" else (order + [SECTION_KEY])
    new = header + json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    print("  %s : %s (ordre -> %s)" % (filename, "DÉJÀ présent, ré-aligné" if already else "AJOUT", data["order"]))
    if not dry:
        wt.upsert_file(sh, gid, filename, new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme-id", default="158654333149")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sh = Shopify(load_env())
    # résout le gid du thème
    themes = wt.list_themes(sh)
    t = next((x for x in themes if str(x["id"]) == str(args.theme_id)), None)
    if not t:
        sys.exit("Thème id %s introuvable." % args.theme_id)
    gid = "gid://shopify/OnlineStoreTheme/%s" % args.theme_id
    print("Thème cible : %s (%s, role=%s) | %s" % (t["name"], args.theme_id, t["role"],
                                                   "DRY-RUN" if args.dry_run else "LIVE"))
    section_body = open(LOCAL_SECTION, encoding="utf-8").read()
    print("  sections/%s.liquid : upload (%d octets)" % (SECTION_TYPE, len(section_body)))
    if not args.dry_run:
        wt.upsert_file(sh, gid, "sections/%s.liquid" % SECTION_TYPE, section_body)
    patch_template(sh, gid, "templates/blog.json", "top", args.dry_run)
    patch_template(sh, gid, "templates/article.json", "bottom", args.dry_run)
    print("OK." if not args.dry_run else "DRY-RUN : rien écrit.")


if __name__ == "__main__":
    main()
