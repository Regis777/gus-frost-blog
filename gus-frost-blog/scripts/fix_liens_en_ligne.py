#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reecrit EN LIGNE les liens internes qui pointent vers un handle redirige.

Chirurgical, sur le modele de push_refs.py : on part du corps en ligne, on y
remplace les seules URL concernees, et on renvoie UNIQUEMENT `body_html`.
Rien d'autre n'est touche -- ni les images, ni le maillage bake, ni la FAQ, ni
le statut de publication. On n'utilise surtout pas deploy_cluster.py, qui
rebatit le corps entier.

Le pendant local est scripts/fix_handles_rediriges.py, deja applique a
articles/. Les deux partagent la meme table.

  python scripts/fix_liens_en_ligne.py            # dry-run
  python scripts/fix_liens_en_ligne.py --apply
"""
import argparse, collections, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import load_env, Shopify          # noqa: E402
from wire_theme import gql                     # noqa: E402
from fix_handles_rediriges import MAP          # noqa: E402

REQUETE = """
query($apres: String) {
  articles(first: 100, after: $apres) {
    nodes { id handle title body blog { id handle } }
    pageInfo { hasNextPage endCursor }
  }
}
"""

MOTIFS = [(re.compile(r'(/blogs/chiens/)%s(?=["\'/#?])' % re.escape(v)), n)
          for v, n in MAP.items()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--pause", type=float, default=0.6)
    a = ap.parse_args()

    sh = Shopify(load_env())
    arts, cur = [], None
    while True:
        d = gql(sh, REQUETE, {"apres": cur})["articles"]
        arts.extend(d["nodes"])
        if not d["pageInfo"]["hasNextPage"]:
            break
        cur = d["pageInfo"]["endCursor"]
    print("%d articles en ligne examines\n" % len(arts))

    total, ecrits = collections.Counter(), 0
    for art in arts:
        corps = art["body"] or ""
        neuf = corps
        compte = 0
        for motif, cible in MOTIFS:
            neuf, n = motif.subn(r"\g<1>" + cible, neuf)
            compte += n
        if not compte:
            continue
        total[art["blog"]["handle"]] += compte
        print("  /blogs/%s/%-46s %2d lien(s)"
              % (art["blog"]["handle"], art["handle"], compte))
        if a.apply:
            aid = art["id"].rsplit("/", 1)[-1]
            bid = art["blog"]["id"].rsplit("/", 1)[-1]
            sh._req("PUT", "/blogs/%s/articles/%s.json" % (bid, aid),
                    {"article": {"id": int(aid), "body_html": neuf}})
            ecrits += 1
            time.sleep(a.pause)

    print("\n%d lien(s) au total : %s"
          % (sum(total.values()), dict(total) or "aucun"))
    print("%s" % ("%d article(s) reecrit(s) en ligne." % ecrits if a.apply
                  else "DRY-RUN : rien ecrit."))


if __name__ == "__main__":
    main()
