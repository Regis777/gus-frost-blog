#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crée (ou met à jour, idempotent) la page Shopify « Programme Ambassadeurs »
dont le corps est affiliation/page_ambassadeurs.html.

Même logique que scripts/create_blog_hub_page.py : réutilise le client Shopify
de publish.py, upsert par handle, + métachamps SEO (title_tag / description_tag).
Publiée par défaut (la boutique est sous mot de passe : invisible du public).

Usage :
  python affiliation/deploy_page.py --dry-run   # n'appelle rien, affiche le diagnostic
  python affiliation/deploy_page.py             # crée / met à jour la page (publiée)
  python affiliation/deploy_page.py --draft     # créer/mettre à jour en brouillon
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import load_env, Shopify  # noqa: E402

SEO_TITLE = "Programme Ambassadeurs — Gus & Frost"
SEO_DESC = ("Devenez ambassadeur Gus & Frost : partagez les produits que vous "
            "aimez, offrez une remise à votre communauté et touchez une commission "
            "sur chaque commande. Gratuit, sans engagement.")


def main():
    ap = argparse.ArgumentParser(description="Déploie la page Programme Ambassadeurs.")
    ap.add_argument("--handle", default="programme-ambassadeurs")
    ap.add_argument("--title", default="Programme Ambassadeurs")
    ap.add_argument("--body", default="affiliation/page_ambassadeurs.html")
    ap.add_argument("--draft", action="store_true", help="published=false (brouillon).")
    ap.add_argument("--dry-run", action="store_true", help="aucun appel API.")
    args = ap.parse_args()

    body_path = os.path.join(ROOT, args.body)
    body_html = open(body_path, encoding="utf-8").read()

    print("Page   : %s (handle=%s)" % (args.title, args.handle))
    print("Corps  : %s (%d octets)" % (args.body, len(body_html.encode("utf-8"))))
    print("État   : %s" % ("BROUILLON" if args.draft else "PUBLIÉE"))
    if args.dry_run:
        print("Dry-run : aucun appel API. Relance sans --dry-run pour déployer.")
        return

    sh = Shopify(load_env())
    existing = sh._req("GET", "/pages.json?handle=%s&limit=1" % args.handle).get("pages", [])
    payload = {"page": {
        "title": args.title,
        "handle": args.handle,
        "body_html": body_html,
        "published": not args.draft,
        "metafields": [
            {"namespace": "global", "key": "title_tag",
             "value": SEO_TITLE, "type": "single_line_text_field"},
            {"namespace": "global", "key": "description_tag",
             "value": SEO_DESC, "type": "single_line_text_field"},
        ],
    }}
    if existing:
        pid = existing[0]["id"]
        res = sh._req("PUT", "/pages/%s.json" % pid, payload)
        action = "MISE À JOUR"
    else:
        res = sh._req("POST", "/pages.json", payload)
        action = "CRÉATION"

    p = res.get("page", {})
    print("=" * 60)
    print("%s : id=%s | published=%s"
          % (action, p.get("id"), p.get("published_at") is not None))
    print("URL storefront : /pages/%s" % p.get("handle"))


if __name__ == "__main__":
    main()
