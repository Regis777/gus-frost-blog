#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cuit le bloc « articles liés » dans le corps des articles.

POURQUOI. Le snippet related-articles.liquid bouclait sur `blog.articles`, que
Liquid plafonne a 50 articles hors pagination : 73 % du blog chien et 100 % du
blog chat affichaient un cadre vide. Le maillage est desormais calcule ici, a
partir du manifest, et ecrit dans le corps — plus aucune limite Liquid.

IDEMPOTENT. Le bloc est encadre par des marqueurs HTML ; une seconde execution
le remplace au lieu de l'empiler. Relancer apres chaque cluster.

Le balisage reproduit celui du snippet a l'identique (memes classes), pour que
gf-article.css continue de s'appliquer sans changement.

Usage :
  python scripts/bake_maillage.py --blog chats               # dry-run
  python scripts/bake_maillage.py --blog chats --apply
  python scripts/bake_maillage.py --blog chiens --apply --sources-seules
"""
import argparse
import csv
import html
import io
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify  # noqa: E402

DEBUT = "<!-- gf-maillage:debut -->"
FIN = "<!-- gf-maillage:fin -->"
RX_BLOC = re.compile(re.escape(DEBUT) + r".*?" + re.escape(FIN), re.S)

MANIFESTS = {"chiens": "manifest.csv", "chats": "manifest_chat.csv"}
NBSP = u" "


def esc(s):
    return html.escape((s or "").strip(), quote=False)


def tous_les_articles(sh, blog_id):
    url = "%s/blogs/%s/articles.json?limit=250" % (sh.base, blog_id)
    arts = []
    while url:
        req = urllib.request.Request(url)
        req.add_header("X-Shopify-Access-Token", sh.token)
        with urllib.request.urlopen(req) as resp:
            arts += json.loads(resp.read().decode("utf-8"))["articles"]
            lien = resp.headers.get("Link", "") or ""
        suivant = re.search(r'<([^>]+)>;\s*rel="next"', lien)
        url = suivant.group(1) if suivant else None
    return arts


def carte(blog, art, img):
    """Une vignette + un titre, comme le rendait le snippet."""
    if img and img.get("src"):
        src = img["src"]
        src += ("&" if "?" in src else "?") + "width=240"
        vignette = ('<img class="gf-related-thumb" src="%s" alt="%s" '
                    'width="240" height="180" loading="lazy">'
                    % (esc(src), esc(img.get("alt"))))
    else:
        vignette = ('<span class="gf-related-thumb gf-related-thumb--empty" '
                    'aria-hidden="true"></span>')
    return ('<a class="gf-related-card" href="/blogs/%s/%s">%s'
            '<span class="gf-related-title">%s</span></a>'
            % (blog, art["handle"], vignette, esc(art["title"])))


def bloc(blog, courant, pilier, freres, images):
    if not freres:
        return None                       # rien a montrer : pas de cadre vide
    est_pilier = pilier is not None and pilier["handle"] == courant["handle"]
    parts = [DEBUT, '<aside class="gf-related">']
    if est_pilier:
        parts.append("<h2>Le dossier complet</h2>")
    else:
        if pilier is not None:
            parts.append('<p class="gf-related-parent">Cet article fait partie du '
                         'dossier%s: <a href="/blogs/%s/%s">%s</a>.</p>'
                         % (NBSP, blog, pilier["handle"], esc(pilier["title"])))
        parts.append("<h2>À lire aussi dans ce dossier</h2>")
    classe = "gf-related-grid gf-related-grid--2col" if len(freres) > 3 else "gf-related-grid"
    parts.append('<div class="%s">' % classe)
    for f in freres:
        parts.append(carte(blog, f, images.get(f["handle"])))
    parts.append("</div></aside>")
    parts.append(FIN)
    return "\n".join(parts)


def pose(corps, bl):
    """Remplace le bloc existant, ou l'ajoute a la fin. Idempotent."""
    corps = corps.rstrip()
    if RX_BLOC.search(corps):
        return RX_BLOC.sub(lambda _m: bl or "", corps).rstrip() if bl \
            else RX_BLOC.sub("", corps).rstrip()
    return (corps + "\n\n" + bl) if bl else corps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blog", choices=sorted(MANIFESTS), required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--sources-seules", action="store_true",
                    help="n'ecrit que les fichiers locaux, pas les articles en ligne")
    ap.add_argument("--only", help="un slug, pour essayer")
    args = ap.parse_args()

    sh = Shopify(load_env())
    blog_id = next(b["id"] for b in sh._req("GET", "/blogs.json?limit=250")["blogs"]
                   if b["handle"] == args.blog)
    arts = tous_les_articles(sh, blog_id)
    par_slug = {a["handle"]: a for a in arts}
    images = {a["handle"]: a.get("image") for a in arts}

    rows = list(csv.DictReader(io.open(os.path.join(ROOT, MANIFESTS[args.blog]),
                                       encoding="utf-8-sig")))
    # Le regroupement suit le manifest, pas les tags en ligne : c'est la source.
    par_cluster = {}
    for r in rows:
        par_cluster.setdefault((r["cluster_num"], r["cluster_tag"]), []).append(r)

    stats = {"ecrits": 0, "inchanges": 0, "sans_freres": 0, "absents": 0, "liens": 0}
    for cle, groupe in sorted(par_cluster.items()):
        piliers = [r for r in groupe if r["type"].upper().startswith("PILIER")]
        pilier_row = piliers[0] if piliers else None
        for r in groupe:
            if args.only and r["slug"] != args.only:
                continue
            art = par_slug.get(r["slug"])
            if art is None:
                stats["absents"] += 1
                continue
            # freres = les satellites du meme sous-cluster, sauf soi
            freres = [par_slug[x["slug"]] for x in groupe
                      if not x["type"].upper().startswith("PILIER")
                      and x["slug"] != r["slug"] and x["slug"] in par_slug]
            pilier = par_slug.get(pilier_row["slug"]) if pilier_row else None
            bl = bloc(args.blog, art, pilier, freres, images)
            if bl is None:
                stats["sans_freres"] += 1
                continue
            stats["liens"] += len(freres)

            # 1) le fichier source, pour que le prochain deploiement le garde
            f = os.path.join(ROOT, r["file"].replace("/", os.sep))
            if os.path.exists(f):
                src = io.open(f, encoding="utf-8").read()
                neuf = pose(src, bl)
                if neuf != src and args.apply:
                    io.open(f, "w", encoding="utf-8", newline="\n").write(neuf + "\n")

            # 2) l'article en ligne
            corps = art.get("body_html") or ""
            neuf = pose(corps, bl)
            if neuf == corps:
                stats["inchanges"] += 1
                continue
            stats["ecrits"] += 1
            if args.apply and not args.sources_seules:
                sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog_id, art["id"]),
                        {"article": {"id": art["id"], "body_html": neuf}})
                time.sleep(0.25)

    print("blog %s : %d a ecrire | %d deja a jour | %d sans frere | %d absents en ligne"
          % (args.blog, stats["ecrits"], stats["inchanges"],
             stats["sans_freres"], stats["absents"]))
    print("         %d liens internes poses au total" % stats["liens"])
    if not args.apply:
        print("DRY-RUN : rien ecrit.")


if __name__ == "__main__":
    main()
