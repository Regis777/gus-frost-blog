#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neutralise les renvois internes qui ne peuvent PAS encore être résolus.

Un cluster est souvent rédigé avant les clusters qu'il cite (CH1 renvoie à CH3,
CH8, CH9… non produits). Ces `PLACEHOLDER_<slug>` ne correspondent à aucune ligne
du manifest : au déploiement ils deviendraient des liens /blogs/<blog>/<slug> en
404, et `deploy_cluster.py` refuse d'écrire l'article tant qu'ils sont là.

Ce script transforme le lien en texte simple, en gardant la phrase intacte :
    <a href="PLACEHOLDER_chat-peureux-se-cache">un chat qui se cache</a>
 -> un chat qui se cache

La prose est conservée telle quelle : au moment où le cluster cible sortira, le
back-fill consiste à re-poser un <a> autour de ce même texte (voir le
<slug>_backfill.md écrit à côté du cluster, qui liste quoi recâbler et où).

Usage :
  python scripts/unlink_placeholders.py --dir articles/cluster-1-langage-chat --blog chats
  python scripts/unlink_placeholders.py --dir articles/cluster-1-langage-chat --blog chats --apply
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

LINK = re.compile(r'<a\s+href="PLACEHOLDER_([A-Za-z0-9-]+)"\s*>(.*?)</a>', re.S)


def manifest_slugs(path):
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8-sig", newline="") as f:
        return {r["slug"] for r in csv.DictReader(f)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="dossier des {slug}.html du cluster")
    ap.add_argument("--blog", default=None, help="chiens (défaut) ou chats")
    ap.add_argument("--apply", action="store_true", help="écrit (sinon : plan seul)")
    args = ap.parse_args()

    conf = blog_conf(args.blog)
    known = manifest_slugs(conf["manifest_path"])
    d = args.dir if os.path.isabs(args.dir) else os.path.join(ROOT, args.dir)
    files = sorted(f for f in os.listdir(d) if f.endswith(".html"))

    print("=" * 74)
    print("Neutralisation des renvois non résolubles | blog «%s» | %s"
          % (conf["handle"], "APPLY" if args.apply else "PLAN (aucune écriture)"))
    print("  manifest de référence : %s (%d slugs connus)" % (conf["manifest"], len(known)))
    print("=" * 74)

    total, per_target = 0, {}
    for fn in files:
        p = os.path.join(d, fn)
        html = open(p, encoding="utf-8").read()
        hits = [(s, t) for s, t in LINK.findall(html) if s not in known]
        if not hits:
            continue
        for s, t in hits:
            per_target.setdefault(s, []).append((fn, re.sub(r"\s+", " ", t).strip()))
        total += len(hits)
        print("  • %-38s %d renvoi(s) : %s"
              % (fn.replace(".html", ""), len(hits), ", ".join(sorted({s for s, _ in hits}))))
        if args.apply:
            new = LINK.sub(lambda m: m.group(2) if m.group(1) not in known else m.group(0), html)
            open(p, "w", encoding="utf-8").write(new)

    print("\n" + "=" * 74)
    if not total:
        print("Aucun renvoi non résoluble : rien à faire.")
        return
    print("%d renvoi(s) sur %d cible(s) manquante(s)." % (total, len(per_target)))

    # Mémo de back-fill : à rejouer quand les clusters cibles seront publiés.
    memo = os.path.join(d, "_BACKFILL_liens.md")
    lines = ["# Back-fill des renvois neutralisés",
             "",
             "Ces renvois ont été convertis en texte simple faute de cible existante au",
             "moment du déploiement. Quand le cluster propriétaire sortira, re-poser un",
             "`<a href=\"/blogs/%s/<slug>\">` autour du texte indiqué." % conf["handle"],
             ""]
    for s in sorted(per_target):
        lines.append("## `%s`" % s)
        for fn, txt in per_target[s]:
            lines.append("- `%s` — texte : « %s »" % (fn.replace(".html", ""), txt))
        lines.append("")
    if args.apply:
        open(memo, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print("Mémo de back-fill écrit : %s" % os.path.relpath(memo, ROOT))
    else:
        print("PLAN uniquement. Relancer avec --apply pour écrire.")


if __name__ == "__main__":
    main()
