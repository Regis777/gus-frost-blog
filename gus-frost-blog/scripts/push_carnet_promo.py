#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajoute l'encart « Le Carnet » en pied de TOUS les articles du blog :
  - upload snippets/gf-carnet-promo.liquid
  - upload assets/gf-article.css       (contient les styles .gf-carnet-promo)
  - patch  sections/main-article.liquid : insere le render AVANT 'related-articles'

Idempotent : si le render est deja present, le patch est saute.
Prudent : si l'ancre attendue est introuvable, on ne touche PAS au fichier et on
le signale, plutot que d'inserer au hasard dans le gabarit live.

Usage :
  python scripts/push_carnet_promo.py --theme-id 158654333149 --allow-live --dry-run
  python scripts/push_carnet_promo.py --theme-id 158654333149 --allow-live
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from publish import load_env, Shopify      # noqa: E402
import wire_theme as wt                     # noqa: E402

SNIPPET_LOCAL = os.path.join(ROOT, "theme", "gf-carnet-promo.liquid")
SNIPPET_DIST = "snippets/gf-carnet-promo.liquid"
CSS_LOCAL = os.path.join(ROOT, "theme", "gf-article.css")
CSS_DIST = "assets/gf-article.css"

SECTION = "sections/main-article.liquid"
RENDER = "{%- render 'gf-carnet-promo' -%}"
ANCRE_LIES = "{%- render 'related-articles' -%}"
MARQUEUR = "gf-carnet-promo"


def upload(sh, gid, local, distant, dry):
    with open(local, "r", encoding="utf-8") as f:
        contenu = f.read()
    avant = wt.read_file(sh, gid, distant)
    if avant == contenu:
        print("  %-38s identique, rien a faire" % distant)
        return
    print("  %-38s %s (%d octets)"
          % (distant, "remplace" if avant is not None else "cree", len(contenu.encode("utf-8"))))
    if not dry:
        wt.upsert_file(sh, gid, distant, contenu)


def patch_section(sh, gid, dry):
    body = wt.read_file(sh, gid, SECTION)
    if body is None:
        return "SAUTE (%s introuvable)" % SECTION
    if MARQUEUR in body:
        return "deja present, rien a faire"
    if ANCRE_LIES not in body:
        return ("SAUTE (ancre \"%s\" introuvable) -> a inserer a la main" % ANCRE_LIES)
    new = body.replace(ANCRE_LIES, RENDER + "\n" + ANCRE_LIES, 1)
    if not dry:
        wt.upsert_file(sh, gid, SECTION, new)
    return "patche (encart insere avant 'related-articles')"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme-id", required=True)
    ap.add_argument("--allow-live", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sh = Shopify(load_env())
    cible = next((t for t in wt.list_themes(sh) if str(t["id"]) == str(args.theme_id)), None)
    if not cible:
        sys.exit("Theme id %s introuvable." % args.theme_id)
    if cible["role"] == "main" and not args.allow_live:
        sys.exit("REFUS : '%s' est le theme PUBLIE. Relance avec --allow-live si c'est voulu."
                 % cible["name"])

    gid = "gid://shopify/OnlineStoreTheme/%s" % cible["id"]
    print("Theme cible : %s (id=%s, role=%s) | %s"
          % (cible["name"], cible["id"], cible["role"], "DRY-RUN" if args.dry_run else "ECRITURE"))
    print("=" * 62)
    upload(sh, gid, SNIPPET_LOCAL, SNIPPET_DIST, args.dry_run)
    upload(sh, gid, CSS_LOCAL, CSS_DIST, args.dry_run)
    print("  %-38s %s" % (SECTION, patch_section(sh, gid, args.dry_run)))
    print("=" * 62)
    print("DRY-RUN : rien ecrit." if args.dry_run else "OK — l'encart est en pied de chaque article.")


if __name__ == "__main__":
    main()
