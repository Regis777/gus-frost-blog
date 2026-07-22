#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifie un article publie : champs cles + meta SEO. Usage : python scripts/verify.py <slug>"""
import sys
import re
from publish import load_env, Shopify

IMG_RE = re.compile(r'REMPLACER_[A-Za-z0-9.\-]+')


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage : python scripts/verify.py <slug>")
    slug = sys.argv[1]
    env = load_env()
    sh = Shopify(env)
    blog_id = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    art = sh.find_article(blog_id, slug)
    if not art:
        sys.exit("Article '%s' introuvable sur le blog '%s'." % (slug, env["BLOG_HANDLE"]))
    aid = art["id"]
    mf = sh._req("GET", "/blogs/%s/articles/%s/metafields.json" % (blog_id, aid))
    seo = {m["key"]: m["value"] for m in mf.get("metafields", [])
           if m.get("namespace") == "global" and m["key"] in ("title_tag", "description_tag")}
    body = art.get("body_html") or ""
    print("Article      : %s" % art.get("title"))
    print("id / handle  : %s / %s" % (aid, art.get("handle")))
    print("published    : %s (published_at=%s)" % (art.get("published_at") is not None, art.get("published_at")))
    print("tags         : %s" % art.get("tags"))
    print("SEO title    : %s" % seo.get("title_tag", "(absent)"))
    print("SEO desc     : %s" % seo.get("description_tag", "(absent)"))
    print("images restantes (REMPLACER_) : %d" % len(set(IMG_RE.findall(body))))
    print("apercu admin : https://admin.shopify.com/store/%s/content/articles/%s"
          % (env["SHOPIFY_STORE_DOMAIN"].split(".")[0], aid))


if __name__ == "__main__":
    main()
