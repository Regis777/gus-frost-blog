#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sort les deux personnalisations d'article des fichiers de Dawn.

Une mise a jour du theme reecrit les fichiers de Dawn : tout ce qu'on y greffe
saute. Deux greffes existaient :

  1. layout/theme.liquid       -> chargement conditionnel de gf-article.css
  2. sections/main-article.liquid -> render de gf-carnet-promo et related-articles

La premiere est remplacee par une section a nous, gf-article-css, posee en tete
de templates/article.json. Les deux renders, eux, ne sont pas remplaces : depuis
le 02/09/2026 l'encart Carnet et les articles lies sont cuits dans le corps des
articles par bake_maillage.py. Les remettre afficherait chaque bloc deux fois —
c'est pourquoi --revert ne les restaure pas.

Apres ca, plus aucun fichier de Dawn n'est modifie sur les pages article.

Usage :
  python scripts/degreffe_article.py --theme-id 163845112029 --dry-run
  python scripts/degreffe_article.py --theme-id 163845112029 --apply
  python scripts/degreffe_article.py --theme-id ... --apply --revert
"""
import argparse
import json
import os
import sys
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify  # noqa: E402

# Les greffes, telles qu'elles existent dans le theme.
GREFFE_CSS = (
    "  {%- if template.name == 'article' -%}\n"
    "  {{ 'gf-article.css' | asset_url | stylesheet_tag }}\n"
    "{%- endif -%}\n"
    "</head>"
)
SANS_GREFFE_CSS = "  </head>"

# Traites separement : « Copie de Dawn » ne porte que le second, le snippet
# gf-carnet-promo n'y ayant jamais ete depose.
GREFFE_RENDERS = [
    "\n{%- render 'gf-carnet-promo' -%}",
    "\n{%- render 'related-articles' -%}",
]

SECTIONS = [
    ("gf-article-css.liquid", "sections/gf-article-css.liquid", "gf_article_css",
     "gf-article-css"),
]

# Section d'un etat anterieur : l'encart Carnet et les articles lies sont
# desormais cuits dans le corps (bake_maillage.py), elle n'a plus rien a rendre.
SECTIONS_OBSOLETES = ["gf_article_extras"]
FICHIERS_OBSOLETES = ["sections/gf-article-extras.liquid"]


def get(sh, tid, key):
    """Rend None si le fichier n'existe pas encore (publish.Shopify leve sur 404)."""
    try:
        d = sh._req("GET", "/themes/%s/assets.json?asset[key]=%s"
                    % (tid, urllib.parse.quote(key)))
    except SystemExit as e:
        if "HTTP 404" in str(e):
            return None
        raise
    return d.get("asset", {}).get("value")


def put(sh, tid, key, val):
    sh._req("PUT", "/themes/%s/assets.json" % tid, {"asset": {"key": key, "value": val}})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme-id", required=True)
    ap.add_argument("--revert", action="store_true", help="remet les greffes, retire les sections")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    sh = Shopify(load_env())
    tid = args.theme_id
    theme = next((t for t in sh._req("GET", "/themes.json")["themes"] if str(t["id"]) == str(tid)), None)
    if theme is None:
        sys.exit("Theme %s introuvable." % tid)
    print("Theme : %s (%s, role=%s)\n" % (theme["name"], tid, theme["role"]))

    ecrire = {}

    # ---- layout/theme.liquid ------------------------------------------------
    layout = get(sh, tid, "layout/theme.liquid")
    if args.revert:
        if GREFFE_CSS in layout:
            print("  = layout/theme.liquid          greffe deja presente")
        elif SANS_GREFFE_CSS in layout:
            ecrire["layout/theme.liquid"] = layout.replace(SANS_GREFFE_CSS, GREFFE_CSS, 1)
            print("  ~ layout/theme.liquid          greffe CSS remise")
        else:
            sys.exit("REFUS : </head> introuvable dans layout/theme.liquid.")
    else:
        if GREFFE_CSS in layout:
            ecrire["layout/theme.liquid"] = layout.replace(GREFFE_CSS, SANS_GREFFE_CSS, 1)
            print("  ~ layout/theme.liquid          greffe CSS retiree")
        else:
            print("  = layout/theme.liquid          aucune greffe (deja propre)")

    # ---- sections/main-article.liquid ---------------------------------------
    # Les renders ne sont JAMAIS remis, meme en --revert : l'encart Carnet et les
    # articles lies vivent maintenant dans le corps des articles. Les remettre
    # afficherait chaque bloc deux fois.
    art = get(sh, tid, "sections/main-article.liquid")
    presents = [g for g in GREFFE_RENDERS if g in art]
    if presents:
        neuf = art
        for g in presents:
            neuf = neuf.replace(g, "", 1)
        ecrire["sections/main-article.liquid"] = neuf
        print("  ~ sections/main-article.liquid %d render(s) retire(s)" % len(presents))
    else:
        print("  = sections/main-article.liquid aucune greffe (deja propre)")

    # ---- les deux sections --------------------------------------------------
    if not args.revert:
        for local, cle, _id, _type in SECTIONS:
            src = open(os.path.join(ROOT, "theme", local), encoding="utf-8").read()
            if get(sh, tid, cle) == src:
                print("  = %-28s a jour" % cle)
            else:
                ecrire[cle] = src
                print("  + %-28s deposee" % cle)

    # ---- templates/article.json --------------------------------------------
    tpl = json.loads(get(sh, tid, "templates/article.json"))
    ordre = list(tpl.get("order", []))
    sections = dict(tpl.get("sections", {}))
    avant = list(ordre)

    # La section obsolete part dans les deux sens.
    for sid in SECTIONS_OBSOLETES:
        sections.pop(sid, None)
        if sid in ordre:
            ordre.remove(sid)

    if args.revert:
        for _l, _k, sid, _t in SECTIONS:
            sections.pop(sid, None)
            if sid in ordre:
                ordre.remove(sid)
    else:
        css_id = SECTIONS[0][2]
        sections.setdefault(css_id, {"type": SECTIONS[0][3], "settings": {}})
        if css_id not in ordre:
            ordre.insert(0, css_id)            # en tete : la feuille avant le texte

    if ordre != avant or sections != tpl.get("sections", {}):
        tpl["sections"], tpl["order"] = sections, ordre
        ecrire["templates/article.json"] = json.dumps(tpl, ensure_ascii=False, indent=2)
        print("  ~ templates/article.json       ordre : %s" % " > ".join(ordre))
    else:
        print("  = templates/article.json       inchange")

    if not ecrire:
        print("\nRien a faire.")
        return
    if args.dry_run:
        print("\n%d fichier(s) a ecrire. DRY-RUN : rien ecrit." % len(ecrire))
        return

    print()
    for cle, val in ecrire.items():
        put(sh, tid, cle, val)
        # La relecture immediate rend parfois la version d'avant : l'API sert un
        # instant l'ancien contenu apres un PUT. On redemande plutot que de
        # crier a l'ecart pour un simple decalage de propagation.
        for essai in range(4):
            relu = get(sh, tid, cle)
            ok = (json.loads(relu) == json.loads(val)) if cle.endswith(".json") else (relu == val)
            if ok:
                break
            time.sleep(1.5)
        print("  ecrit %-32s relecture %s%s"
              % (cle, "OK" if ok else ">>> ECART <<<",
                 " (apres %d relecture(s))" % (essai + 1) if ok and essai else ""))

    # le fichier de section devenu inutile, s'il traine encore
    for cle in FICHIERS_OBSOLETES:
        if get(sh, tid, cle) is not None:
            sh._req("DELETE", "/themes/%s/assets.json?asset[key]=%s"
                    % (tid, urllib.parse.quote(cle)))
            print("  - %-32s supprimee (sans objet)" % cle)

    # controle final : plus aucune greffe dans les fichiers de Dawn
    if not args.revert:
        l2 = get(sh, tid, "layout/theme.liquid")
        a2 = get(sh, tid, "sections/main-article.liquid")
        print("\nFichiers de Dawn encore greffes : %s"
              % ("AUCUN" if "gf-article.css" not in l2 and "gf-carnet-promo" not in a2
                 else ">>> il en reste <<<"))


if __name__ == "__main__":
    main()
