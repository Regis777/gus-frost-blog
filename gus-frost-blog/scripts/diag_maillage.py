#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic du bloc « articles liés » (snippets/related-articles.liquid).

Le bloc rend un cadre vide sur la majorite des articles. Deux causes,
independantes, mesurees separement ici :

1. LE PLAFOND DE 50. Le snippet fait `{% for a in blog.articles %}`. Hors
   pagination, Liquid n'expose que les 50 articles les plus recents du blog. Un
   article ne voit donc ses freres que s'ils sont dans cette fenetre — ce qui
   exclut tous les clusters anciens. Cause dominante, les deux blogs.

2. LE TAG DE ROLE. Le snippet exige `a.tags contains 'satellite'`. Les premiers
   clusters portaient ce tag ; la convention a change en cours de route (colonne
   `type` passee de `satellite` a `SAT01`..`SAT18`) et le tag a cesse d'etre
   pose. Cote chien le deploiement le reconstruit, cote chat non : les 219
   articles en sont depourvus.

Usage : python scripts/diag_maillage.py
"""
import collections
import csv
import io
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify  # noqa: E402

FENETRE = 50  # ce que Liquid expose dans blog.articles sans paginate
BLOGS = [("chiens", "manifest.csv"), ("chats", "manifest_chat.csv")]


def tous_les_articles(sh, blog_id):
    """Pagination par curseur : since_id sous-compte (250 sur 264 constate)."""
    url = "%s/blogs/%s/articles.json?limit=250" % (sh.base, blog_id)
    arts = []
    while url:
        req = urllib.request.Request(url)
        req.add_header("X-Shopify-Access-Token", sh.token)
        with urllib.request.urlopen(req) as resp:
            arts += json.loads(resp.read().decode("utf-8"))["articles"]
            lien = resp.headers.get("Link", "") or ""
        suivant = re.search(r'<([^>]+)>;\s*rel="next"', lien)
        url = suivant.group(1) if suivant else None
    return [a for a in arts if a.get("published_at")]


def tags(a):
    return {t.strip() for t in (a.get("tags") or "").split(",") if t.strip()}


def main():
    sh = Shopify(load_env())
    blogs = {b["handle"]: b["id"] for b in sh._req("GET", "/blogs.json?limit=250")["blogs"]}

    for nom, manifeste in BLOGS:
        arts = tous_les_articles(sh, blogs[nom])
        arts.sort(key=lambda a: a["published_at"], reverse=True)
        fenetre = {a["id"] for a in arts[:FENETRE]}

        rows = {r["slug"]: r for r in csv.DictReader(io.open(
            os.path.join(ROOT, manifeste), encoding="utf-8-sig"))}
        role = {s: ("pilier" if r["type"].upper().startswith("PILIER") else "satellite")
                for s, r in rows.items()}

        par_cluster = collections.defaultdict(list)
        for a in arts:
            for t in tags(a):
                if t.startswith("cluster-"):
                    par_cluster[t].append(a)

        def cartes(a, role_corrige):
            clu = next((t for t in tags(a) if t.startswith("cluster-")), None)
            if clu is None:
                return 0
            def sat(b):
                return (role.get(b["handle"]) == "satellite") if role_corrige \
                    else ("satellite" in tags(b))
            freres = [b for b in par_cluster[clu] if sat(b) and b["id"] != a["id"]]
            return len([b for b in freres if b["id"] in fenetre])

        vides = sum(1 for a in arts if cartes(a, False) == 0)
        vides_si_tags = sum(1 for a in arts if cartes(a, True) == 0)
        a_retaguer = [a["handle"] for a in arts
                      if role.get(a["handle"]) and role[a["handle"]] not in tags(a)]

        print("=" * 68)
        print("BLOG %s — %d articles publies" % (nom.upper(), len(arts)))
        print("  a 0 carte aujourd'hui                   : %3d (%.0f %%)"
              % (vides, 100.0 * vides / len(arts)))
        print("  a 0 carte si on pose les tags de role   : %3d (%.0f %%)"
              % (vides_si_tags, 100.0 * vides_si_tags / len(arts)))
        print("  a 0 carte sans le plafond de 50         :   0")
        print("  articles depourvus du tag de role       : %3d" % len(a_retaguer))


if __name__ == "__main__":
    main()
