#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le corps HTML de la page « Conseils chiens » (sommaire du blog) à partir de
manifest.csv : les articles groupés par cluster, pilier en tête + satellites listés.
Exclut les slugs non publiés (passés via --draft, sinon aucun).

Usage :
  python scripts/build_blog_hub.py --out build/blog_hub.html [--draft slug1,slug2,...]
La sortie est le body_html à poser dans la page Shopify (page.blog-hub non requis :
rendu dans le template `page` par défaut). Régénérable après chaque nouveau cluster.
"""
import argparse, csv, html, os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def esc(s):
    return html.escape(s.strip(), quote=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="build/blog_hub.html")
    ap.add_argument("--blog", default="chiens", help="handle du blog pour les liens /blogs/<blog>/<slug>")
    ap.add_argument("--manifest", default="manifest.csv", help="manifest source (défaut : chiens)")
    ap.add_argument("--intro", default="", help="phrase d'intro personnalisée (optionnel)")
    ap.add_argument("--draft", default="", help="slugs non publiés à exclure, séparés par des virgules")
    args = ap.parse_args()
    BLOG = args.blog
    drafts = {s.strip() for s in args.draft.split(",") if s.strip()}

    rows = list(csv.DictReader(open(os.path.join(ROOT, args.manifest), encoding="utf-8-sig")))
    # regroupe par cluster_num (ordre croissant), pilier d'abord puis satellites (ordre manifest)
    clusters = OrderedDict()
    for r in rows:
        clusters.setdefault(int(r["cluster_num"]), []).append(r)

    sections, n_art, n_clu = [], 0, 0
    for cn in sorted(clusters):
        arts = clusters[cn]
        pilier = next((a for a in arts if a["type"].upper() == "PILIER"), None)
        if not pilier or pilier["slug"] in drafts:
            continue  # pas de pilier publié -> on saute le thème entier
        sats = [a for a in arts if a["type"].upper() != "PILIER" and a["slug"] not in drafts]
        n_clu += 1
        n_art += 1 + len(sats)
        lis = "\n".join(
            '        <li><a href="/blogs/%s/%s">%s</a></li>' % (BLOG, a["slug"], esc(a["title"]))
            for a in sats
        )
        sections.append(
            '    <section class="gf-hub-cluster">\n'
            '      <h2 class="gf-hub-pilier"><a href="/blogs/%s/%s">%s</a></h2>\n'
            '      <ul class="gf-hub-list">\n%s\n      </ul>\n'
            '    </section>' % (BLOG, pilier["slug"], esc(pilier["title"]), lis)
        )

    style = (
        '<style>\n'
        '  .gf-hub-intro{max-width:60ch;margin:0 auto 2rem;text-align:center;}\n'
        '  .gf-hub-grid{display:grid;grid-template-columns:1fr;gap:1.5rem;}\n'
        '  @media (min-width:750px){.gf-hub-grid{grid-template-columns:1fr 1fr;gap:2rem;}}\n'
        '  .gf-hub-cluster{border:1px solid rgba(0,0,0,.08);border-radius:12px;padding:1.2rem 1.4rem;background:rgb(var(--color-background));}\n'
        '  .gf-hub-pilier{font-size:1.25rem;margin:0 0 .6rem;line-height:1.3;}\n'
        '  .gf-hub-pilier a{text-decoration:none;}\n'
        '  .gf-hub-list{list-style:none;margin:0;padding:0;}\n'
        '  .gf-hub-list li{padding:.25rem 0;border-top:1px solid rgba(0,0,0,.06);}\n'
        '  .gf-hub-list li:first-child{border-top:0;}\n'
        '  .gf-hub-list a{text-decoration:none;}\n'
        '  .gf-hub-list a:hover,.gf-hub-pilier a:hover{text-decoration:underline;}\n'
        '  .gf-hub-search{display:flex;gap:.5rem;max-width:34rem;margin:0 auto 2rem;}\n'
        '  .gf-hub-search input[type=search]{flex:1;padding:.7rem 1rem;font-size:1rem;border:1px solid rgba(0,0,0,.2);border-radius:999px;background:rgb(var(--color-background));color:inherit;}\n'
        '  .gf-hub-search button{padding:.7rem 1.3rem;font-size:1rem;border:0;border-radius:999px;cursor:pointer;background:rgb(var(--color-foreground,26 26 26));color:rgb(var(--color-background,255 255 255));}\n'
        '  .gf-hub-search button:hover{opacity:.9;}\n'
        '</style>'
    )
    search = (
        '<form action="/search" method="get" role="search" class="gf-hub-search">\n'
        '  <input type="hidden" name="type" value="article">\n'
        '  <input type="hidden" name="options[prefix]" value="last">\n'
        '  <input type="search" name="q" placeholder="Rechercher un conseil…" '
        'aria-label="Rechercher dans les articles du blog" required>\n'
        '  <button type="submit">Rechercher</button>\n'
        '</form>'
    )
    intro_txt = args.intro.strip() or (
        "Tous nos guides et conseils pour comprendre et accompagner votre chien, "
        "organisés par thème. Chaque thème s'ouvre sur un guide principal, complété par des articles détaillés."
    )
    intro = '<p class="gf-hub-intro">%s</p>' % esc(intro_txt)
    body = "%s\n%s\n%s\n<div class=\"gf-hub-grid\">\n%s\n</div>\n" % (
        style, intro, search, "\n".join(sections))

    outp = os.path.join(ROOT, args.out)
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    open(outp, "w", encoding="utf-8").write(body)
    print("Page générée : %s" % args.out)
    print("Thèmes (piliers publiés) : %d | articles listés : %d" % (n_clu, n_art))


if __name__ == "__main__":
    main()
