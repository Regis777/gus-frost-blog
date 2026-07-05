#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajoute la colonne `excerpt` à manifest.csv (juste après `meta_description`) et la
remplit depuis manifest_excerpts_C1-C5.csv (colonnes cluster_num,slug,excerpt).
Idempotent. Ne touche à aucun autre fichier.

Usage :
  python deploy/add_excerpt_column.py            # DRY-RUN : diagnostic, rien écrit
  python deploy/add_excerpt_column.py --apply
"""
import argparse
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
MANIFEST = os.path.join(ROOT, "manifest.csv")
EXC = os.path.join(ROOT, "articles", "cluster-6-chiot", "manifest_excerpts_C1-C5.csv")
NEW_ORDER = ["cluster_num", "cluster_tag", "type", "slug", "parent_pilier_slug",
             "title", "meta_title", "meta_description", "excerpt", "tags",
             "file", "prompts_file", "links_to_resolve", "images_to_resolve"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    with open(MANIFEST, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    header = list(rows[0].keys()) if rows else []
    excerpts = {}
    with open(EXC, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            excerpts[r["slug"].strip()] = r["excerpt"].strip()

    has_col = "excerpt" in header
    missing = [r["slug"] for r in rows if not (r.get("excerpt") or excerpts.get(r["slug"]))]
    filled = sum(1 for r in rows if (r.get("excerpt") or excerpts.get(r["slug"])))
    print("Lignes manifest : %d | colonne excerpt déjà présente : %s" % (len(rows), has_col))
    print("Excerpts dispo (fichier) : %d | lignes couvertes : %d/%d"
          % (len(excerpts), filled, len(rows)))
    if missing:
        print("  ⚠ slugs SANS excerpt : %s" % ", ".join(missing))

    # construire les lignes finales
    out = []
    for r in rows:
        r = dict(r)
        if not r.get("excerpt"):
            r["excerpt"] = excerpts.get(r["slug"], "")
        out.append([r.get(c, "") for c in NEW_ORDER])

    if not args.apply:
        print("\nNouvel en-tête (14 col) :\n  " + ",".join(NEW_ORDER))
        print("excerpt en position %d (après meta_description). DRY-RUN : rien écrit."
              % (NEW_ORDER.index("excerpt") + 1))
        return

    with open(MANIFEST, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(NEW_ORDER)
        w.writerows(out)
    # verif
    with open(MANIFEST, encoding="utf-8-sig", newline="") as f:
        chk = list(csv.reader(f))
    ncols = {len(r) for r in chk}
    empty = sum(1 for r in chk[1:] if not r[NEW_ORDER.index("excerpt")].strip())
    print("\nÉcrit. Colonnes/ligne : %s | en-tête[8]=%s | lignes sans excerpt : %d"
          % (ncols, chk[0][8], empty))


if __name__ == "__main__":
    main()
