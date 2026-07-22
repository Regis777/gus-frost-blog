#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apercu LOCAL d'un article : corps resolu + gf-article.css inline, dans un seul .html
ouvrable au navigateur (file://). Aucun appel reseau, aucun secret, zero risque.
Les <img src="REMPLACER_..."> sont remplacees par des blocs placeholder (pour juger
la mise en page avant generation des visuels).

Usage : python scripts/local_preview.py <slug>
"""
import os
import re
import sys

from publish import ROOT, read_manifest, load_env, build_resolver, resolve_body

CSS = os.path.join(ROOT, "theme", "gf-article.css")
IMG_TAG_RE = re.compile(r'<img\b[^>]*>', re.IGNORECASE)


def attr(tag, name):
    m = re.search(r'%s\s*=\s*"([^"]*)"' % name, tag, re.IGNORECASE)
    return m.group(1) if m else ""


def img_to_placeholder(tag):
    if "REMPLACER_" not in tag:
        return tag
    alt = attr(tag, "alt") or "image"
    w = attr(tag, "width") or "1080"
    h = attr(tag, "height") or "1080"
    return ('<div class="gf-imgph" style="aspect-ratio:%s/%s">'
            '<span>🖼️ %s</span></div>') % (w, h, alt)


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage : python scripts/local_preview.py <slug>")
    slug = sys.argv[1]
    row = next((r for r in read_manifest() if r["slug"] == slug), None)
    if not row:
        sys.exit("slug '%s' absent du manifest." % slug)

    env = load_env()
    resolver = build_resolver(env)
    with open(os.path.join(ROOT, row["file"].replace("/", os.sep)), "r", encoding="utf-8") as f:
        raw = f.read()
    body, _unres, _n = resolve_body(raw, resolver)
    body = IMG_TAG_RE.sub(lambda m: img_to_placeholder(m.group(0)), body)

    with open(CSS, "r", encoding="utf-8") as f:
        css = f.read()

    extra = (
        "body{background:#fff;margin:0;padding:2.5rem 1rem;}"
        ".gf-preview-note{max-width:760px;margin:0 auto 1.5rem;padding:.7rem 1rem;"
        "background:#314431;color:#fff;border-radius:8px;font:14px/1.4 -apple-system,"
        "'Segoe UI',Helvetica,Arial,sans-serif;}"
        ".gf-imgph{background:#EFE7DA;border:2px dashed #b9ac90;border-radius:10px;"
        "color:#5b5b5b;display:flex;align-items:center;justify-content:center;"
        "text-align:center;padding:1rem;font-style:italic;max-width:100%;margin:0 auto;}"
    )

    html = (
        "<!doctype html><html lang=fr><head><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        "<title>Apercu — %s</title><style>%s\n%s</style></head><body>"
        "<div class=gf-preview-note>Apercu LOCAL (CSS Gus &amp; Frost). "
        "Les blocs beige = emplacements des futures images. Le rendu Dawn ajoutera "
        "seulement l'en-tete/pied de page autour.</div>%s</body></html>"
    ) % (slug, extra, css, body)

    out = os.path.join(ROOT, "build", "preview-%s.html" % slug)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(out)


if __name__ == "__main__":
    main()
