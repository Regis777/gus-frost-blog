# -*- coding: utf-8 -*-
"""
Rattrapage : réécrit les <img> des articles de blog en balises optimisées
(srcset multi-largeurs + sizes + width/height + lazy/eager) pour que le CDN Shopify
serve du WebP redimensionné. Aucun ré-upload d'image.

Travaille sur le CORPS LIVE Shopify (source de vérité), car les fichiers Drive des
vieux clusters sont désynchronisés (C1–C4 = placeholders REMPLACER, C7 = pré-bake).
Gère les deux formats de balise ; ne touche que les <img> dont le src est une URL CDN
et qui n'ont pas déjà un srcset (idempotent). Met aussi à jour le fichier repo/Drive
quand il contient le même type de balise (sinon il est laissé tel quel).

Usage :
  python scripts/optimize_article_images.py --only <slug> --apply
  python scripts/optimize_article_images.py --cluster 14 --apply
  python scripts/optimize_article_images.py --all --apply
  (sans --apply : plan, lit le live mais n'écrit rien)  options : --no-files  --sleep 0.4
"""
import argparse, csv, os, re, sys, time
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from img_optim import build_img, png_dims               # noqa: E402
from publish import load_env, Shopify                   # noqa: E402
import glob

REPO_ROOT = r"C:\Users\regis\gfbrepo\gus-frost-blog"
IMG = re.compile(r'<img\b[^>]*>', re.I)
SRC = re.compile(r'\ssrc="([^"]+)"', re.I)
ALT = re.compile(r'\salt="([^"]*)"', re.I)
FNAME = re.compile(r'/files/([^/?"]+\.(?:png|jpe?g|webp))', re.I)


def dims_index():
    return {os.path.basename(f): png_dims(f) for f in glob.glob(os.path.join(ROOT, "images", "cluster-*", "*.png"))}


def transform(html, dims_idx, counter):
    def repl(m):
        tag = m.group(0)
        if "srcset=" in tag:
            return tag  # déjà optimisé
        ms = SRC.search(tag)
        if not ms or not ms.group(1).startswith("http"):
            return tag  # pas une URL CDN (REMPLACER, relatif) -> on laisse
        base = ms.group(1)
        alt = (ALT.search(tag).group(1) if ALT.search(tag) else "")
        fn = FNAME.search(base)
        fname = fn.group(1) if fn else ""
        dims = dims_idx.get(fname)
        hero = fname.startswith("hero-") or 'id="img-hero"' in tag
        counter[0] += 1
        if not dims:
            counter[1].append(fname)
        return build_img(base, alt, dims, hero)
    return IMG.sub(repl, html)


def slugs_from(args):
    rows = list(csv.DictReader(open(os.path.join(ROOT, "manifest.csv"), encoding="utf-8-sig")))
    if args.only:
        return [(r["slug"], r["file"]) for r in rows if r["slug"] == args.only]
    if args.cluster:
        return [(r["slug"], r["file"]) for r in rows if r["cluster_num"] == str(args.cluster)]
    return [(r["slug"], r["file"]) for r in rows]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only"); ap.add_argument("--cluster"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true"); ap.add_argument("--no-files", action="store_true")
    ap.add_argument("--sleep", type=float, default=0.4)
    args = ap.parse_args()
    if not (args.only or args.cluster or args.all):
        sys.exit("Préciser --only, --cluster ou --all.")
    dims_idx = dims_index()
    sh = Shopify(load_env()); blog = sh.find_blog_id("chiens")
    targets = slugs_from(args)

    tot_arts = tot_imgs = done = skipped = failed = 0
    all_miss = []
    for slug, relfile in targets:
        tot_arts += 1
        try:
            art = sh.find_article(blog, slug)
            if not art:
                print("  [MANQUE] %s (pas trouvé sur Shopify)" % slug); failed += 1; continue
            body = sh._req("GET", "/blogs/%s/articles/%s.json" % (blog, art["id"]))["article"]["body_html"]
            cnt = [0, []]
            new = transform(body, dims_idx, cnt)
            if new == body:
                skipped += 1; continue
            tot_imgs += cnt[0]; all_miss += cnt[1]
            print("  [%s] %-42s %d img" % ("OK" if args.apply else "PLAN", slug, cnt[0]) +
                  ("  ! sans dims: %s" % cnt[1] if cnt[1] else ""))
            if args.apply:
                sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, art["id"]),
                        {"article": {"id": art["id"], "body_html": new}})
                if not args.no_files:
                    for rootdir in (ROOT, REPO_ROOT):
                        p = os.path.join(rootdir, relfile.replace("/", os.sep))
                        if os.path.exists(p):
                            fc = open(p, encoding="utf-8").read()
                            fn = transform(fc, dims_idx, [0, []])
                            if fn != fc:
                                open(p, "w", encoding="utf-8").write(fn)
                done += 1
                time.sleep(args.sleep)
        except BaseException as e:
            print("  [ERR] %s : %s" % (slug, str(e)[:120])); failed += 1
    print("\n%s : %d articles vus, %d optimisés, %d déjà ok, %d échecs | %d images%s" % (
        "APPLIQUÉ" if args.apply else "PLAN", tot_arts, done if args.apply else (tot_arts-skipped-failed),
        skipped, failed, tot_imgs, "  ! dims manquantes: %d" % len(set(all_miss)) if all_miss else ""))


if __name__ == "__main__":
    main()
