#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphe des liens internes entre articles, mesure des liens ENTRANTS.

Un article que rien ne pointe est un orphelin : Google le decouvre par le
sitemap, mais rien ne lui dit qu'il compte, et il reste en « Detectee,
actuellement non indexee ».

  python scripts/diag_liens_entrants.py [--csv build/liens_entrants.csv]

Lecture seule.
"""
import argparse, collections, csv, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import load_env, Shopify          # noqa: E402
from wire_theme import gql                     # noqa: E402

REQUETE = """
query($apres: String) {
  articles(first: 100, after: $apres) {
    nodes { id handle title body blog { handle } }
    pageInfo { hasNextPage endCursor }
  }
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="build/liens_entrants.csv")
    a = ap.parse_args()

    sh = Shopify(load_env())
    arts, curseur = [], None
    while True:
        d = gql(sh, REQUETE, {"apres": curseur})["articles"]
        arts.extend(d["nodes"])
        if not d["pageInfo"]["hasNextPage"]:
            break
        curseur = d["pageInfo"]["endCursor"]
    print("%d articles recuperes" % len(arts))

    # index : (blog, handle) -> article
    cle = lambda a: (a["blog"]["handle"], a["handle"])
    connus = {cle(x): x for x in arts}
    entrants = collections.defaultdict(set)
    sortants = collections.Counter()

    motif = re.compile(r'href="(?:https://gusetfrost\.fr)?/blogs/([a-z0-9\-]+)/([a-z0-9\-]+)"')
    for art in arts:
        src = cle(art)
        for blog, handle in set(motif.findall(art["body"] or "")):
            cible = (blog, handle)
            if cible in connus and cible != src:
                entrants[cible].add(src)
                sortants[src] += 1

    par_blog = collections.Counter(k[0] for k in connus)
    print("par blog :", dict(par_blog))

    lignes = []
    for k, art in connus.items():
        e = entrants.get(k, set())
        lignes.append({
            "blog": k[0], "handle": k[1], "titre": art["title"],
            "liens_entrants": len(e),
            "entrants_meme_blog": sum(1 for s in e if s[0] == k[0]),
            "entrants_autre_blog": sum(1 for s in e if s[0] != k[0]),
            "liens_sortants": sortants.get(k, 0),
        })
    lignes.sort(key=lambda r: (r["liens_entrants"], r["blog"], r["handle"]))

    chemin = os.path.join(ROOT, a.csv)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with io.open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
        w.writeheader()
        w.writerows(lignes)

    print("\n--- liens entrants, par blog ---")
    for blog in sorted(par_blog):
        sous = [r for r in lignes if r["blog"] == blog]
        orph = [r for r in sous if r["liens_entrants"] == 0]
        faibles = [r for r in sous if 0 < r["liens_entrants"] <= 2]
        croises = sum(1 for r in sous if r["entrants_autre_blog"] > 0)
        moy = sum(r["liens_entrants"] for r in sous) / float(len(sous))
        print("%-8s %3d articles | orphelins %3d | 1-2 entrants %3d | moyenne %.1f | recoivent de l'autre blog %d"
              % (blog, len(sous), len(orph), len(faibles), moy, croises))
        for r in orph[:12]:
            print("      orphelin : /blogs/%s/%s" % (r["blog"], r["handle"]))
        if len(orph) > 12:
            print("      … et %d autres" % (len(orph) - 12))
    print("\nDetail : %s" % a.csv)


if __name__ == "__main__":
    main()
