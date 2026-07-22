#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genere la checklist des images a produire pour un cluster : pour chaque article,
liste les fichiers attendus (nom = ce qui suit REMPLACER_), dimensions et ALT,
+ le chemin du fichier de prompts. Ecrit un .md dans images/<dossier-cluster>/.

Usage : python scripts/image_checklist.py --cluster 1 [--type satellite|pilier]
"""
import argparse
import os
import re

from publish import ROOT, read_manifest, order_rows

IMG_RE = re.compile(r'<img\b[^>]*>', re.IGNORECASE)


def attr(tag, name):
    m = re.search(r'%s\s*=\s*"([^"]*)"' % name, tag, re.IGNORECASE)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cluster", type=int, required=True, choices=[1, 2, 3])
    ap.add_argument("--type", choices=["pilier", "satellite"])
    args = ap.parse_args()

    rows = [r for r in read_manifest() if r["cluster_num"] == str(args.cluster)]
    if args.type:
        rows = [r for r in rows if r["type"] == args.type]
    rows = order_rows(rows)

    cluster_dir = os.path.basename(os.path.dirname(
        os.path.join(ROOT, rows[0]["file"].replace("/", os.sep))))
    out_dir = os.path.join(ROOT, "images", cluster_dir)
    os.makedirs(out_dir, exist_ok=True)

    lines = ["# Images a produire — cluster %s%s" % (
        args.cluster, " (%s)" % args.type if args.type else "")]
    lines.append("")
    lines.append("Depose chaque image dans **ce dossier** avec EXACTEMENT le nom indique "
                 "(le script `upload_images.py` fait la correspondance automatiquement). "
                 "Extensions .jpg/.png/.webp acceptees, garde le meme nom de base.")
    lines.append("")
    total = 0
    for r in rows:
        path = os.path.join(ROOT, r["file"].replace("/", os.sep))
        html = open(path, "r", encoding="utf-8").read()
        imgs = []
        for tag in IMG_RE.findall(html):
            src = attr(tag, "src")
            if not src.startswith("REMPLACER_"):
                continue
            imgs.append((src[len("REMPLACER_"):], attr(tag, "width"),
                         attr(tag, "height"), attr(tag, "alt")))
        if not imgs:
            continue
        lines.append("## %s  (%s)" % (r["slug"], r["type"]))
        lines.append("Prompts : `%s`" % r["prompts_file"])
        lines.append("")
        lines.append("| Fichier a deposer | Dimensions | Description (ALT) |")
        lines.append("|---|---|---|")
        for name, w, h, alt in imgs:
            dims = ("%s x %s" % (w, h)) if w and h else "—"
            lines.append("| `%s` | %s | %s |" % (name, dims, alt))
            total += 1
        lines.append("")
    lines.append("**Total : %d images.**" % total)

    out = os.path.join(out_dir, "_A_DEPOSER_%s.md" % (args.type or "TOUS").upper())
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Ecrit : %s  (%d images)" % (os.path.relpath(out, ROOT), total))


if __name__ == "__main__":
    main()
