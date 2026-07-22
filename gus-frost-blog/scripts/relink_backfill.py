#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recâble les renvois qu'`unlink_placeholders.py` avait convertis en prose, une fois
le cluster cible déployé.

Le mémo `_BACKFILL_liens.md` écrit lors de la neutralisation garde, pour chaque
cible manquante, le fichier et le TEXTE EXACT qui portait le lien. Ce script relit
ce mémo et ré-entoure ce texte d'un <a> vers la nouvelle cible.

La cible n'a pas toujours le même slug que celui d'origine : le rédacteur d'un
cluster cite parfois un slug supposé, et le cluster réel sort sous un autre nom
(ex. « chat-peureux-se-cache » -> « chat-qui-se-cache »). D'où le mapping explicite.

Usage :
  python scripts/relink_backfill.py --dir articles/cluster-1-langage-chat --blog chats \\
      --map chat-peureux-se-cache=chat-qui-se-cache,chaton-socialisation=socialisation-chaton
  # ... puis --apply
"""
import argparse
import csv
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import blog_conf                                        # noqa: E402

ENTRY = re.compile(r"^- `([^`]+)`\s+— texte\s*:\s*«\s*(.+?)\s*»\s*$")
HEAD = re.compile(r"^##\s+`([^`]+)`\s*$")


def manifest_slugs(path):
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8-sig", newline="") as f:
        return {r["slug"] for r in csv.DictReader(f)}


def read_memo(path):
    """-> [(cible_origine, fichier, texte)] dans l'ordre du mémo."""
    out, cur = [], None
    for line in open(path, encoding="utf-8"):
        h = HEAD.match(line.rstrip())
        if h:
            cur = h.group(1)
            continue
        e = ENTRY.match(line.rstrip())
        if e and cur:
            out.append((cur, e.group(1), e.group(2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--blog", default=None)
    ap.add_argument("--map", help="ancienne-cible=nouveau-slug, séparés par des virgules")
    ap.add_argument("--map-file", help="JSON {clé: slug} ; la clé est soit le TEXTE exact "
                                       "du lien, soit l'ancienne cible. Le texte l'emporte.")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if not args.map and not args.map_file:
        sys.exit("Fournir --map ou --map-file.")

    conf = blog_conf(args.blog)
    known = manifest_slugs(conf["manifest_path"])
    # Le slug cité dans le PLACEHOLDER est souvent une supposition du rédacteur ;
    # le TEXTE du lien, lui, dit sans ambiguïté ce qui est promis au lecteur.
    # On autorise donc une clé de mapping par texte, prioritaire sur la cible.
    mapping = {}
    if args.map_file:
        import json
        mapping.update(json.load(open(args.map_file, encoding="utf-8")))
    for pair in (args.map or "").split(","):
        if not pair.strip():
            continue
        old, _, new = pair.partition("=")
        mapping[old.strip()] = new.strip()

    inconnues = sorted(v for v in mapping.values() if v not in known)
    if inconnues:
        sys.exit("Cibles absentes du manifest %s : %s" % (conf["manifest"], inconnues))

    d = args.dir if os.path.isabs(args.dir) else os.path.join(ROOT, args.dir)
    memo = os.path.join(d, "_BACKFILL_liens.md")
    if not os.path.exists(memo):
        sys.exit("Mémo introuvable : %s" % memo)

    print("=" * 74)
    print("Back-fill des renvois | blog «%s» | %s"
          % (conf["handle"], "APPLY" if args.apply else "PLAN (aucune écriture)"))
    print("=" * 74)

    done, skipped = 0, []
    for cible, slug, texte in read_memo(memo):
        cle = texte if texte in mapping else cible
        if cle not in mapping:
            skipped.append((slug, cible, "pas dans le mapping"))
            continue
        p = os.path.join(d, slug + ".html")
        html = open(p, encoding="utf-8").read()
        # le texte du mémo a ses espaces normalisées : on reconstruit une regex
        # tolérante aux retours à la ligne du fichier.
        pat = re.compile(r"(?<!>)" + r"\s+".join(re.escape(w) for w in texte.split()))
        m = pat.search(html)
        if not m:
            skipped.append((slug, cible, "texte introuvable (déjà recâblé ?)"))
            continue
        lien = '<a href="/blogs/%s/%s">%s</a>' % (conf["handle"], mapping[cle], m.group(0))
        print("  • %-38s « %s » -> /%s" % (slug, texte[:46], mapping[cle]))
        done += 1
        if args.apply:
            open(p, "w", encoding="utf-8").write(html[:m.start()] + lien + html[m.end():])

    print("\n" + "=" * 74)
    print("%d renvoi(s) recâblé(s)%s." % (done, "" if args.apply else " (simulation)"))
    for s in skipped:
        print("  · ignoré : %-34s %-30s %s" % s)
    if done and args.apply:
        print("\nRedéployer le cluster pour propager : deploy_cluster.py --cluster … --bake")


if __name__ == "__main__":
    main()
