#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bascule le drapeau `published` d'articles deja deployes, SANS toucher au corps.

A utiliser apres relecture des brouillons poses par deploy_cluster.py : le corps
en ligne est deja resolu et « bake », il ne faut surtout pas le regenerer.

Selection identique a deploy_cluster.py : --cluster, et --tag pour viser un
sous-cluster (plusieurs sous-clusters partagent un meme cluster_num).

Usage :
  python deploy/set_published.py --cluster 6 --tag chiot-accueil --dry-run
  python deploy/set_published.py --cluster 6 --tag chiot-accueil --publish
  python deploy/set_published.py --cluster 6 --tag chiot-accueil --unpublish
"""
import argparse, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify, read_manifest          # noqa: E402


def cluster_rows(n, tag=None):
    rows = [r for r in read_manifest() if r["cluster_num"] == str(n)]
    if tag:
        pref = "articles/cluster-%d-%s/" % (n, tag)
        rows = [r for r in rows if r["file"].replace(os.sep, "/").startswith(pref)]
    rows.sort(key=lambda r: (0 if r["type"].upper() == "PILIER" else 1, r["slug"]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cluster", type=int, required=True)
    ap.add_argument("--tag", help="suffixe du sous-cluster, ex. chiot-accueil")
    ap.add_argument("--only")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--publish", action="store_true")
    g.add_argument("--unpublish", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    want = bool(args.publish)
    env = load_env()
    sh = Shopify(env)
    blog = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    rows = cluster_rows(args.cluster, args.tag)
    if args.only:
        rows = [r for r in rows if r["slug"] == args.only]
    if not rows:
        sys.exit("Aucune ligne selectionnee.")

    print("=" * 74)
    print("C%d%s -> blog «%s» | published=%s | %s"
          % (args.cluster, "/" + args.tag if args.tag else "", env["BLOG_HANDLE"],
             want, "DRY-RUN (aucune ecriture)" if args.dry_run else "LIVE"))
    print("=" * 74)

    done = skipped = absent = 0
    for r in rows:
        slug = r["slug"]
        art = sh.find_article(blog, slug)
        if not art:
            print("  ⚠ %-40s ABSENT en ligne" % slug); absent += 1; continue
        now = art.get("published_at") is not None
        if now == want:
            print("  = %-40s deja published=%s" % (slug, now)); skipped += 1; continue
        if args.dry_run:
            print("  → %-40s %s -> %s" % (slug, now, want)); done += 1; continue
        sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, art["id"]),
                {"article": {"id": art["id"], "published": want}})
        print("  ✓ %-40s %s -> %s" % (slug, now, want)); done += 1
        time.sleep(0.4)

    print("\n%d modifie(s) | %d inchange(s) | %d absent(s)" % (done, skipped, absent))
    if args.dry_run:
        print("DRY-RUN : rien ecrit.")


if __name__ == "__main__":
    main()
