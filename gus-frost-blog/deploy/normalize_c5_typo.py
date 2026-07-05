#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Normalise le cluster C5 pour en faire une référence propre :
  1. ajoute id="faq" au <h2> FAQ des satellites (le pilier l'a déjà) ;
  2. remplace l'espace normale par une insécable (U+00A0) avant ; : ! ? »
     et après « — UNIQUEMENT dans le texte, jamais dans les balises/attributs.

Puis MET À JOUR le body_html des 13 articles (idempotent, statut de publication
inchangé : pilier en ligne, 12 satellites brouillon) et réécrit les {slug}.html.

Usage :
  python deploy/normalize_c5_typo.py            # DRY-RUN : montre les changements, rien écrit
  python deploy/normalize_c5_typo.py --apply    # écrit repo + Shopify
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify, read_manifest   # noqa: E402

ARTDIR = os.path.join(ROOT, "articles", "cluster-5-repas-gamelle")
NBSP = " "


def normalize(html):
    """Retourne (html_normalisé, n_id, n_insec)."""
    n_id = 0
    # 1) id="faq" sur le <h2> FAQ s'il ne l'a pas déjà
    if re.search(r"<h2>\s*Questions fréquentes", html):
        html, n_id = re.subn(r"<h2>(\s*Questions fréquentes)", r'<h2 id="faq">\1', html)

    # 2) insécables — sur les segments de TEXTE seulement (hors <balises>)
    n_insec = 0
    parts = re.split(r"(<[^>]+>)", html)
    for i in range(0, len(parts), 2):          # indices pairs = texte
        seg = parts[i]
        seg, a = re.subn(r" ([;:!?»])", NBSP + r"\1", seg)   # espace avant ponctuation double
        seg, b = re.subn(r"(«) ", r"\1" + NBSP, seg)          # espace après guillemet ouvrant
        n_insec += a + b
        parts[i] = seg
    return "".join(parts), n_id, n_insec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    env = load_env()
    sh = Shopify(env)
    blog = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    rows = [r for r in read_manifest() if r["cluster_num"] == "5"]
    rows.sort(key=lambda r: (0 if r["type"] == "pilier" else 1, r["slug"]))

    print("=" * 68)
    print("Normalisation C5 | %s" % ("APPLY (écritures)" if args.apply else "DRY-RUN"))
    print("=" * 68)
    tot_id = tot_insec = 0
    for r in rows:
        slug = r["slug"]
        p = os.path.join(ARTDIR, slug + ".html")
        html = open(p, encoding="utf-8").read()
        new, n_id, n_insec = normalize(html)
        tot_id += n_id; tot_insec += n_insec
        changed = new != html
        print("  %-30s id=%d insécables=%-3d %s"
              % (slug, n_id, n_insec, "→ à modifier" if changed else "(déjà propre)"))
        if args.apply and changed:
            open(p, "w", encoding="utf-8", newline="").write(new)
            art = sh.find_article(blog, slug)
            pub = bool(art.get("published_at"))
            sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, art["id"]),
                    {"article": {"id": art["id"], "body_html": new}})
            print("        -> MAJ OK (published inchangé=%s)" % pub)

    print("\n" + "=" * 68)
    print("Total : +%d id=faq, %d insécables%s"
          % (tot_id, tot_insec, "" if args.apply else " (aucune écriture — DRY-RUN)"))


if __name__ == "__main__":
    main()
