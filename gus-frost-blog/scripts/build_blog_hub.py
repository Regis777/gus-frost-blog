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
import argparse, csv, html, os, re
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


NBSP = " "


def insecables(s):
    """Typo FR : insecable avant ; : ! ? » et apres «. Les titres du manifest
    sont saisis en espaces ASCII ; on normalise a l'affichage."""
    s = re.sub(r"[  ]+([;:!?»])", NBSP + r"\1", s)
    s = re.sub(r"«[  ]+", "«" + NBSP, s)
    return s


def esc(s):
    return html.escape(insecables(s.strip()), quote=False)


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
    # Regroupe par (cluster_num, cluster_tag) : un meme cluster_num porte plusieurs
    # sous-clusters (schema « par pilier »), qui doivent rester des themes distincts.
    # Les satellites sont rattaches par parent_pilier_slug, pas par position.
    clusters = OrderedDict()
    for r in rows:
        clusters.setdefault((int(r["cluster_num"]), r["cluster_tag"]), []).append(r)

    def live(r):
        return r["slug"] not in drafts

    # Un pilier sans satellite propre est un hub de super-silo : il chapeaute les
    # piliers des autres sous-clusters partageant son cluster_num (ex. « Élever un
    # chiot » -> Accueillir un chiot, puis Propreté, Socialisation… a mesure).
    piliers_par_num = {}
    for (cn, _tag), arts in clusters.items():
        for a in arts:
            if a["type"].upper() == "PILIER":
                piliers_par_num.setdefault(cn, []).append(a)

    def satellites_de(pilier, arts):
        return [a for a in arts
                if a["type"].upper() != "PILIER"
                and a["parent_pilier_slug"].strip() == pilier["slug"]
                and live(a)]

    def rendu(pilier, enfants):
        lis = "\n".join(
            '        <li><a href="/blogs/%s/%s">%s</a></li>' % (BLOG, a["slug"], esc(a["title"]))
            for a in enfants
        )
        return ('    <section class="gf-hub-cluster">\n'
                '      <h2 class="gf-hub-pilier"><a href="/blogs/%s/%s">%s</a></h2>\n'
                '      <ul class="gf-hub-list">\n%s\n      </ul>\n'
                '    </section>' % (BLOG, pilier["slug"], esc(pilier["title"]), lis))

    sections, vus = [], set()
    for cn in sorted({k[0] for k in clusters}):
        blocs_hub, blocs_pilier = [], []
        for (kcn, _tag), arts in clusters.items():
            if kcn != cn:
                continue
            for pilier in (a for a in arts if a["type"].upper() == "PILIER"):
                if not live(pilier):
                    continue  # pilier non publie -> on saute son theme
                sats = satellites_de(pilier, arts)
                if sats:
                    blocs_pilier.append(rendu(pilier, sats))
                    vus.update([pilier["slug"]] + [a["slug"] for a in sats])
                else:
                    autres = [p for p in piliers_par_num.get(cn, [])
                              if p["slug"] != pilier["slug"] and live(p)]
                    if not autres:
                        continue  # hub encore vide -> rien a lister
                    blocs_hub.append(rendu(pilier, autres))
                    vus.add(pilier["slug"])
        sections.extend(blocs_hub + blocs_pilier)  # le hub ouvre son cluster
    n_clu, n_art = len(sections), len(vus)

    # NB Dawn : html{font-size:62.5%} -> 1rem = 10px. Les tailles ci-dessous sont
    # donc x10 (2rem = 20px). C'est ce piege qui rendait le titre de pilier
    # (1.25rem = 12.5px) PLUS PETIT que ses satellites (body = 1.5rem = 15px) et le
    # champ de recherche illisible (1rem = 10px). Couleurs : creme #EFE7DA
    # (scheme-2 du theme) sur page blanche, encre vert profond #314431 (scheme-1),
    # contraste 8,4:1.
    style = (
        '<style>\n'
        '  .gf-hub-intro{max-width:60ch;margin:0 auto 2rem;text-align:center;}\n'
        '  .gf-hub-grid{display:grid;grid-template-columns:1fr;gap:1.5rem;}\n'
        '  @media (min-width:750px){.gf-hub-grid{grid-template-columns:1fr 1fr;gap:2rem;}}\n'
        '  .gf-hub-cluster{border:1px solid rgba(49,68,49,.14);border-radius:14px;'
        'padding:1.8rem 2rem;background:#efe7da;}\n'
        '  .gf-hub-pilier{font-size:2rem;font-weight:600;margin:0 0 1rem;line-height:1.25;}\n'
        '  .gf-hub-pilier a{text-decoration:none;}\n'
        '  .gf-hub-list{list-style:none;margin:0;padding:0;font-size:1.55rem;}\n'
        '  .gf-hub-list li{padding:.7rem 0;border-top:1px solid rgba(49,68,49,.16);line-height:1.4;}\n'
        '  .gf-hub-list li:first-child{border-top:0;padding-top:0;}\n'
        '  .gf-hub-list a{text-decoration:none;}\n'
        '  .gf-hub-list a:hover,.gf-hub-pilier a:hover{text-decoration:underline;}\n'
        '  .gf-hub-search{display:flex;gap:.8rem;max-width:44rem;margin:0 auto 3rem;}\n'
        '  .gf-hub-search input[type=search]{flex:1;padding:1.2rem 1.8rem;font-size:1.6rem;'
        'border:1px solid rgba(49,68,49,.3);border-radius:999px;'
        'background:rgb(var(--color-background));color:inherit;}\n'
        '  .gf-hub-search input[type=search]::placeholder{opacity:.65;}\n'
        '  .gf-hub-search button{padding:1.2rem 2.2rem;font-size:1.6rem;font-weight:500;'
        'border:0;border-radius:999px;cursor:pointer;white-space:nowrap;'
        'background:rgb(var(--color-foreground,26 26 26));'
        'color:rgb(var(--color-background,255 255 255));}\n'
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
