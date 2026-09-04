#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bascule le drapeau `published` d'articles deja deployes, SANS toucher au corps.

A utiliser apres relecture des brouillons poses par deploy_cluster.py : le corps
en ligne est deja resolu et « bake », il ne faut surtout pas le regenerer.

Selection identique a deploy_cluster.py : --cluster, et --tag pour viser un
sous-cluster (plusieurs sous-clusters partagent un meme cluster_num).

Chaque article dont le drapeau bascule est ensuite signale aux moteurs (IndexNow
+ Bing) via scripts/ping_indexnow.py : mise en ligne comme retrait, les deux les
interessent. Le ping n'est jamais bloquant ; --no-ping le desactive.

Usage :
  python deploy/set_published.py --cluster 6 --tag chiot-accueil --dry-run
  python deploy/set_published.py --cluster 6 --tag chiot-accueil --publish
  python deploy/set_published.py --cluster 6 --tag chiot-accueil --unpublish
  python deploy/set_published.py --cluster 6 --publish --no-ping
"""
import argparse, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify, read_manifest, blog_conf   # noqa: E402
from ping_indexnow import ping_urls, site_url                     # noqa: E402


def cluster_rows(n, tag=None, manifest=None):
    rows = [r for r in read_manifest(manifest) if r["cluster_num"] == str(n)]
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
    ap.add_argument("--blog", default=None, help="chiens (defaut) ou chats")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--publish", action="store_true")
    g.add_argument("--unpublish", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-ping", action="store_true",
                    help="ne pas signaler les URL a IndexNow / Bing")
    args = ap.parse_args()

    want = bool(args.publish)
    env = load_env()
    sh = Shopify(env)
    conf = blog_conf(args.blog or env.get("BLOG_HANDLE"))
    blog = sh.find_blog_id(conf["handle"])
    rows = cluster_rows(args.cluster, args.tag, conf["manifest_path"])
    if args.only:
        rows = [r for r in rows if r["slug"] == args.only]
    if not rows:
        sys.exit("Aucune ligne selectionnee.")

    print("=" * 74)
    print("C%d%s -> blog «%s» | published=%s | %s"
          % (args.cluster, "/" + args.tag if args.tag else "", conf["handle"],
             want, "DRY-RUN (aucune ecriture)" if args.dry_run else "LIVE"))
    print("=" * 74)

    done = skipped = absent = 0
    touched = []
    for r in rows:
        slug = r["slug"]
        art = sh.find_article(blog, slug)
        if not art:
            print("  ⚠ %-40s ABSENT en ligne" % slug); absent += 1; continue
        now = art.get("published_at") is not None
        if now == want:
            print("  = %-40s deja published=%s" % (slug, now)); skipped += 1; continue
        touched.append(slug)
        if args.dry_run:
            print("  → %-40s %s -> %s" % (slug, now, want)); done += 1; continue
        sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, art["id"]),
                {"article": {"id": art["id"], "published": want}})
        print("  ✓ %-40s %s -> %s" % (slug, now, want)); done += 1
        time.sleep(0.4)

    print("\n%d modifie(s) | %d inchange(s) | %d absent(s)" % (done, skipped, absent))
    if args.dry_run:
        print("DRY-RUN : rien ecrit.")

    # Signalement aux moteurs. Volontairement apres coup et non bloquant : un
    # ping rate ne doit pas laisser croire que la publication a echoue.
    if touched and not args.no_ping:
        base = site_url(env)
        print()
        ping_urls(["%s/blogs/%s/%s" % (base, conf["handle"], s) for s in touched],
                  env, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
