#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crée (ou met à jour, idempotent) la page Shopify « Conseils chiens » dont le corps
est build/blog_hub.html (généré par build_blog_hub.py). Publiée par défaut.
Réutilise le client Shopify (CCG) de publish.py.

Usage : python scripts/create_blog_hub_page.py [--handle conseils-chiens] [--title "Conseils chiens"] [--draft]
"""
import argparse, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import load_env, Shopify  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", default="conseils-chiens")
    ap.add_argument("--title", default="Conseils chiens")
    ap.add_argument("--body", default="build/blog_hub.html")
    ap.add_argument("--draft", action="store_true", help="créer en brouillon (published=false)")
    args = ap.parse_args()

    body_html = open(os.path.join(ROOT, args.body), encoding="utf-8").read()
    sh = Shopify(load_env())

    existing = sh._req("GET", "/pages.json?handle=%s&limit=1" % args.handle).get("pages", [])
    payload = {"page": {"title": args.title, "handle": args.handle,
                        "body_html": body_html, "published": not args.draft}}
    if existing:
        pid = existing[0]["id"]
        res = sh._req("PUT", "/pages/%s.json" % pid, payload)
        action = "MISE À JOUR"
    else:
        res = sh._req("POST", "/pages.json", payload)
        action = "CRÉATION"
    p = res.get("page", {})
    print("%s page : id=%s | handle=%s | published=%s" % (action, p.get("id"), p.get("handle"), p.get("published_at") is not None))
    print("URL storefront : /pages/%s" % p.get("handle"))
    print("body_html : %d octets" % len(body_html))


if __name__ == "__main__":
    main()
