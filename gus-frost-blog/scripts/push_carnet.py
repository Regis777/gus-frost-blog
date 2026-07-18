#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Depose la web app « Le Carnet » dans un theme Shopify :
  - assets/gf-carnet.css
  - assets/gf-carnet.js
  - sections/gf-carnet.liquid
  - templates/page.carnet.json

Idempotent : re-uploader ecrase simplement les 4 fichiers, rien d'autre n'est touche
(aucun patch de layout/theme.liquid : la section charge ses propres assets).

Usage :
  python scripts/push_carnet.py --list
  python scripts/push_carnet.py --theme-id 162807808221            # copie non publiee
  python scripts/push_carnet.py --theme-id 158654333149 --allow-live
  python scripts/push_carnet.py --theme-id ... --dry-run
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from publish import load_env, Shopify      # noqa: E402
import wire_theme as wt                     # noqa: E402

# (fichier local dans theme/, destination dans le theme)
FICHIERS = [
    ("gf-carnet.css",    "assets/gf-carnet.css"),
    ("gf-carnet.js",     "assets/gf-carnet.js"),
    ("gf-carnet.liquid", "sections/gf-carnet.liquid"),
    ("page.carnet.json", "templates/page.carnet.json"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--theme-id")
    ap.add_argument("--allow-live", action="store_true",
                    help="autorise l'ecriture sur le theme PUBLIE (go-live assume).")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sh = Shopify(load_env())
    themes = wt.list_themes(sh)

    if args.list:
        for t in themes:
            print("%-14s %-12s %s" % (t["id"], t["role"], t["name"]))
        return

    if not args.theme_id:
        sys.exit("Precise --theme-id (voir --list).")
    cible = next((t for t in themes if str(t["id"]) == str(args.theme_id)), None)
    if not cible:
        sys.exit("Theme id %s introuvable." % args.theme_id)

    if cible["role"] == "main" and not args.allow_live:
        sys.exit("REFUS : '%s' est le theme PUBLIE. Relance avec --allow-live si c'est voulu."
                 % cible["name"])

    gid = "gid://shopify/OnlineStoreTheme/%s" % cible["id"]
    print("Theme cible : %s (id=%s, role=%s) | %s"
          % (cible["name"], cible["id"], cible["role"],
             "DRY-RUN" if args.dry_run else "ECRITURE"))
    print("=" * 62)

    for local, distant in FICHIERS:
        chemin = os.path.join(ROOT, "theme", local)
        if not os.path.exists(chemin):
            sys.exit("Fichier local manquant : %s" % chemin)
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
        avant = wt.read_file(sh, gid, distant)
        etat = "remplace" if avant is not None else "cree"
        if avant == contenu:
            etat = "identique, rien a faire"
        print("  %-30s %7d octets  -> %s" % (distant, len(contenu.encode("utf-8")), etat))
        if not args.dry_run and avant != contenu:
            wt.upsert_file(sh, gid, distant, contenu)

    print("=" * 62)
    if args.dry_run:
        print("DRY-RUN : rien ecrit.")
    else:
        print("OK. Cree ensuite une page avec le modele 'carnet' (scripts/create_carnet_page.py).")


if __name__ == "__main__":
    main()
