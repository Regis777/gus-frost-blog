#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genere des apercus locaux de relecture pour un cluster, a partir du body_html REEL
stocke dans Shopify (donc avec les vraies images CDN) + le CSS gf-article. Ecrit un
fichier par article et une page d'index dans build/. Aucun secret expose.

Usage : python scripts/preview_cluster.py --cluster 1
"""
import argparse
import os
import html as htmlmod

from publish import ROOT, read_manifest, order_rows, load_env, Shopify, BUILD_DIR

PAGE = ("<!doctype html><html lang=fr><head><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        "<title>%s</title><style>%s\n%s</style></head><body>"
        "<div class=gf-preview-note>%s</div>%s</body></html>")
EXTRA = ("body{background:#fff;margin:0;padding:2.2rem 1rem}"
         ".gf-preview-note{max-width:760px;margin:0 auto 1.5rem;padding:.7rem 1rem;"
         "background:#314431;color:#fff;border-radius:8px;font:14px/1.5 -apple-system,"
         "'Segoe UI',Arial,sans-serif}.gf-preview-note a{color:#EFE7DA}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cluster", type=int, required=True, choices=[1, 2, 3])
    args = ap.parse_args()

    env = load_env()
    css = open(os.path.join(ROOT, "theme", "gf-article.css"), encoding="utf-8").read()
    rows = order_rows([r for r in read_manifest() if r["cluster_num"] == str(args.cluster)])

    sh = Shopify(env)
    blog_id = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    os.makedirs(BUILD_DIR, exist_ok=True)

    index_items = []
    for r in rows:
        art = sh.find_article(blog_id, r["slug"])
        if not art:
            print("  (absent: %s)" % r["slug"]); continue
        body = art.get("body_html") or ""
        note = ("RELECTURE — <b>%s</b> [%s] · brouillon. Images CDN reelles. "
                "Dawn ajoutera seulement l'en-tete/pied autour."
                % (htmlmod.escape(r["title"]), r["type"]))
        out = os.path.join(BUILD_DIR, "preview-%s.html" % r["slug"])
        with open(out, "w", encoding="utf-8") as f:
            f.write(PAGE % (r["slug"], EXTRA, css, note, body))
        index_items.append((r["type"], r["title"], "preview-%s.html" % r["slug"]))
        print("  %s" % os.path.relpath(out, ROOT))

    # page d'index
    lis = "".join(
        "<li><span class='t'>%s</span> <a href='%s'>%s</a></li>"
        % (t.upper(), href, htmlmod.escape(title)) for t, title, href in index_items)
    idx_css = ("body{font:16px/1.6 -apple-system,'Segoe UI',Arial,sans-serif;"
               "max-width:760px;margin:2rem auto;padding:0 1rem;color:#2a2a2a}"
               "h1{color:#314431}li{margin:.5rem 0}a{color:#314431}"
               ".t{display:inline-block;width:74px;font-size:.7rem;color:#fff;background:#314431;"
               "border-radius:4px;padding:1px 6px;text-align:center;margin-right:.5rem}")
    idx = ("<!doctype html><html lang=fr><head><meta charset=utf-8><title>Relecture cluster %s</title>"
           "<style>%s</style></head><body><h1>Relecture — cluster %s</h1>"
           "<p>%d articles (brouillon). Clique pour ouvrir chaque apercu.</p><ul>%s</ul></body></html>"
           % (args.cluster, idx_css, args.cluster, len(index_items), lis))
    idx_path = os.path.join(BUILD_DIR, "preview-INDEX-cluster%s.html" % args.cluster)
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(idx)
    print("\nINDEX : %s" % idx_path)


if __name__ == "__main__":
    main()
