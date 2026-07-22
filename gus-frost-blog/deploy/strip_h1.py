#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retire le H1 de tete du corps des articles EN LIGNE (H1 duplique).

Le theme Dawn rend deja le titre de l'article en H1 ; les clusters anciens
(C1 a C4, deployes avant deploy_cluster.py) ont un second H1 dans le body_html,
donc le titre s'affiche deux fois. deploy_cluster.prepare() retire ce H1 depuis,
d'ou des clusters recents sains.

Securite : on ne retire le H1 que s'il est en TETE du corps ET que son texte
correspond au titre de l'article (comparaison insensible a la casse, aux
espaces et a la ponctuation d'espacement). Sinon on signale et on ne touche a rien.
Comme pour normalize_typo, on opere sur le corps Shopify, jamais sur le fragment
repo (les fragments de C1/C2/C3 ne sont pas « bakes »).

Usage :
  python deploy/strip_h1.py --dry-run
  python deploy/strip_h1.py --backup <chemin.json>
"""
import argparse, json, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify, read_manifest        # noqa: E402

H1_HEAD = re.compile(r'(<article\b[^>]*>\s*)<h1\b[^>]*>(.*?)</h1>\s*', re.S)


def cle(s):
    """Titre comparable : sans balises, sans accents d'espacement, minuscule."""
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace(" ", " ").replace("’", "'")
    s = re.sub(r"[«»\"“”]", "", s)          # « shake-off » == shake-off
    return re.sub(r"\s+", " ", s).strip().lower()


def retry(fn, essais=6):
    for k in range(essais):
        try:
            r = fn()
            time.sleep(0.55)
            return r
        except SystemExit as e:
            if "429" not in str(e) or k == essais - 1:
                raise
            time.sleep(2 * (k + 1))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--backup", help="fichier JSON ou sauvegarder les corps avant modification")
    ap.add_argument("--cluster", type=int)
    ap.add_argument("--force-head", action="store_true",
                    help="retire aussi un H1 de tete dont le texte differe du titre")
    args = ap.parse_args()

    env = load_env()
    sh = Shopify(env)
    blog = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    rows = read_manifest()
    if args.cluster:
        rows = [r for r in rows if r["cluster_num"] == str(args.cluster)]

    cibles, refus = [], []
    for r in rows:
        art = retry(lambda: sh.find_article(blog, r["slug"]))
        if not art:
            continue
        b = art["body_html"]
        if "<h1" not in b:
            continue
        m = H1_HEAD.search(b)
        if not m:
            refus.append((r["slug"], "H1 present mais pas en tete du corps"))
            continue
        if cle(m.group(2)) != cle(art["title"]):
            if not args.force_head:
                refus.append((r["slug"], "H1 « %s » != titre « %s »"
                              % (cle(m.group(2))[:40], cle(art["title"])[:40])))
                continue
            print("   ! %-38s H1 de tete au texte different, retire quand meme" % r["slug"])
        cibles.append((r, art, m))

    print("=" * 74)
    print("H1 de tete a retirer : %d article(s)" % len(cibles))
    for r, art, _m in cibles[:4]:
        print("   ex. %-40s %s" % (r["slug"], art["title"][:45]))
    if refus:
        print("\nNON TRAITES (%d) — a regarder a la main :" % len(refus))
        for s, why in refus:
            print("   ⚠ %-40s %s" % (s, why))
    if args.dry_run:
        print("\nDRY-RUN : rien pousse.")
        return

    if args.backup:
        json.dump({r["slug"]: {"id": a["id"], "body_html": a["body_html"]}
                   for r, a, _m in cibles},
                  open(args.backup, "w", encoding="utf-8"), ensure_ascii=False)
        print("\nSauvegarde : %s (%d articles)" % (args.backup, len(cibles)))

    pousses = 0
    for r, art, m in cibles:
        body = H1_HEAD.sub(r"\1", art["body_html"], count=1)
        if "<h1" in body:
            print("  ⚠ %-40s H1 encore present, ignore" % r["slug"]); continue
        retry(lambda: sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, art["id"]),
                              {"article": {"id": art["id"], "body_html": body}}))
        pousses += 1
        if pousses % 15 == 0:
            print("  … %d poussés" % pousses)
    print("\n%d corps mis à jour." % pousses)


if __name__ == "__main__":
    main()
