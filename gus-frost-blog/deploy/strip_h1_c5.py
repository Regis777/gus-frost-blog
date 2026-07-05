#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retire le <h1> de tête (le titre, dupliqué avec celui rendu par le thème Dawn)
des 13 corps C5. Retrait idempotent : uniquement le <h1>…</h1> qui suit
immédiatement <article …>. MAJ body_html des 13 (statut de publication inchangé).

Usage :
  python deploy/strip_h1_c5.py                 # DRY-RUN : montre l'avant/après du 1er article
  python deploy/strip_h1_c5.py --only <slug>   # cible un seul article (aperçu)
  python deploy/strip_h1_c5.py --apply         # écrit repo + Shopify (13 par défaut)
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
# retire le <h1>…</h1> qui suit l'ouverture <article …>
H1_HEAD = re.compile(r'(<article\b[^>]*>\s*)<h1\b[^>]*>.*?</h1>\s*', re.S)


def strip_head_h1(html):
    new, n = H1_HEAD.subn(r"\1", html, count=1)
    return new, n


def top_snippet(html, n=6):
    return "\n".join(html.splitlines()[:n])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()

    env = load_env()
    sh = Shopify(env)
    blog = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    rows = [r for r in read_manifest() if r["cluster_num"] == "5"]
    rows.sort(key=lambda r: (0 if r["type"] == "pilier" else 1, r["slug"]))
    if args.only:
        rows = [r for r in rows if r["slug"] == args.only]

    print("=" * 70)
    print("Strip <h1> de tête C5 | %s" % ("APPLY" if args.apply else "DRY-RUN (aperçu)"))
    print("=" * 70)
    shown = False
    for r in rows:
        p = os.path.join(ARTDIR, r["slug"] + ".html")
        html = open(p, encoding="utf-8").read()
        new, n = strip_head_h1(html)
        state = "h1 retiré" if n else "aucun h1 de tête (déjà propre)"
        print("  %-30s : %s" % (r["slug"], state))
        if not shown and n:
            print("\n  --- AVANT (haut de %s) ---" % r["slug"])
            print("  " + top_snippet(html).replace("\n", "\n  "))
            print("\n  --- APRÈS ---")
            print("  " + top_snippet(new).replace("\n", "\n  "))
            print("  (rendu final : 1 seul <h1>, celui du thème = article.title)\n")
            shown = True
        if args.apply and n:
            open(p, "w", encoding="utf-8", newline="").write(new)
            art = sh.find_article(blog, r["slug"])
            pub = bool(art.get("published_at"))
            sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, art["id"]),
                    {"article": {"id": art["id"], "body_html": new}})
            print("        -> MAJ OK (published inchangé=%s)" % pub)

    print("\n" + ("Terminé." if args.apply else "DRY-RUN : rien écrit."))


if __name__ == "__main__":
    main()
