#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Déploiement GÉNÉRIQUE d'un cluster dans le blog « Chiens » de Gus & Frost, EN BROUILLON.
Remplace les deploy_cN_to_shopify.py : une seule logique, paramétrée par --cluster N.
Auto-découverte :
  ARTDIR  = articles/cluster-N-*      IMG_DIR = images/cluster-N-*
  MAP     = <ARTDIR>/*images_map.csv  (colonnes : num, nouveau_fichier, article_slug, role, alt)
Transforme chaque fragment : retire <style> d'aperçu et <h1> de tête, résout
PLACEHOLDER_{slug} -> /blogs/chiens/{slug}, remplace <div class="gf-imgph">Image N…</div>
par <img src alt>. summary_html = excerpt. Image à la une = image role=hero. published=false.

Usage :
  python deploy/deploy_cluster.py --cluster 7 --dry-run   # aucune écriture : diagnostic + récap
  python deploy/deploy_cluster.py --cluster 7 --bake      # upload images + crée les brouillons
"""
import argparse, csv, glob, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify, read_manifest, make_payload          # noqa: E402
from upload_images import (staged_upload, existing_file_url, file_create,    # noqa: E402
                           wait_ready)
from img_optim import build_img, png_dims                                    # noqa: E402

PH_LINK = re.compile(r'PLACEHOLDER_([A-Za-z0-9\-]+)')
IMGPH = re.compile(r'<div class="gf-imgph">\s*Image\s*(\d+)\b[^<]*</div>', re.IGNORECASE)
H1_HEAD = re.compile(r'(<article\b[^>]*>\s*)<h1\b[^>]*>.*?</h1>\s*', re.S)


def short_alt(a, lim=255):
    # Shopify refuse (422 « image is invalid ») un alt d'image à la une > 255 caractères.
    # L'alt complet reste dans le <img> du corps ; seule la vignette est raccourcie.
    a = a.strip()
    if len(a) <= lim:
        return a
    cut = a[:lim - 1]
    sp = cut.rfind(" ")
    if sp > lim * 0.6:
        cut = cut[:sp]
    return cut.rstrip(" ,;:").rstrip(".") + "."


def discover(n, tag=None):
    # tag = suffixe du dossier (ex. « chiot-accueil » -> articles/cluster-6-chiot-accueil).
    # Indispensable dès qu'un numéro de cluster porte plusieurs sous-clusters.
    pat = ("cluster-%d-%s" % (n, tag)) if tag else ("cluster-%d-*" % n)
    art = sorted(glob.glob(os.path.join(ROOT, "articles", pat)))
    img = sorted(glob.glob(os.path.join(ROOT, "images", pat)))
    if not art:
        sys.exit("Dossier articles/cluster-%d-* introuvable." % n)
    if not img:
        sys.exit("Dossier images/cluster-%d-* introuvable." % n)
    maps = sorted(glob.glob(os.path.join(art[0], "*images_map.csv")))
    if not maps:
        sys.exit("Fichier *images_map.csv introuvable dans %s" % art[0])
    return art[0], img[0], maps[0]


def load_map(mp):
    rows = list(csv.DictReader(open(mp, encoding="utf-8-sig")))
    by_num = {int(r["num"]): r for r in rows}
    by_slug = {}
    for r in rows:
        by_slug.setdefault(r["article_slug"], []).append(r)
    return by_num, by_slug


def cluster_rows(n, tag=None):
    rows = [r for r in read_manifest() if r["cluster_num"] == str(n)]
    if tag:
        pref = "articles/cluster-%d-%s/" % (n, tag)
        rows = [r for r in rows if r["file"].replace(os.sep, "/").startswith(pref)]
    rows.sort(key=lambda r: (0 if r["type"].upper() == "PILIER" else 1, r["slug"]))
    return rows


def prepare(raw, slug, slug_set, by_num, cdn_map, dim_map):
    body = raw[raw.find("<article"):].rstrip()
    body = H1_HEAD.sub(r"\1", body, count=1)
    unknown = sorted({s for s in PH_LINK.findall(body) if s not in slug_set})
    body = PH_LINK.sub(lambda m: "/blogs/chiens/" + m.group(1), body)
    nums, mismatch, missing = [], [], []

    def repl(m):
        n = int(m.group(1))
        nums.append(n)
        row = by_num.get(n)
        if not row:
            missing.append(n); return m.group(0)
        if row["article_slug"] != slug:
            mismatch.append((n, row["article_slug"]))
        src = cdn_map.get(row["nouveau_fichier"], row["nouveau_fichier"])
        alt = row["alt"].replace('"', "&quot;")
        dims = dim_map.get(row["nouveau_fichier"])
        return build_img(src, alt, dims, row.get("role") == "hero")

    body = IMGPH.sub(repl, body)
    return body, unknown, nums, mismatch, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cluster", type=int, required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--bake", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--tag", help="suffixe du sous-cluster, ex. chiot-accueil")
    args = ap.parse_args()
    N = args.cluster

    artdir, imgdir, mp = discover(N, args.tag)
    env = load_env()
    sh = Shopify(env)
    blog = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    by_num, by_slug = load_map(mp)
    slug_set = {r["slug"] for r in read_manifest()}
    rows = cluster_rows(N, args.tag)
    if args.only:
        rows = [r for r in rows if r["slug"] == args.only]

    all_files = sorted({r["nouveau_fichier"] for r in by_num.values()})
    local_missing = [f for f in all_files if not os.path.exists(os.path.join(imgdir, f))]
    dim_map = {f: png_dims(os.path.join(imgdir, f)) for f in all_files}
    cdn_map = {}
    for f in all_files:
        u = existing_file_url(sh, f)
        if u:
            cdn_map[f] = u
        elif not args.dry_run and f not in local_missing:
            resource, _ = staged_upload(sh, os.path.join(imgdir, f))
            fid = file_create(sh, resource, "")
            cdn_map[f] = wait_ready(sh, fid); time.sleep(0.3)

    mode = "DRY-RUN (aucune écriture)" if args.dry_run else "LIVE"
    print("=" * 74)
    print("Cluster C%d -> blog «%s» | brouillon | %s" % (N, env["BLOG_HANDLE"], mode))
    print("Dossier : %s | Images : %d (sur Files : %d | absentes : %d)"
          % (os.path.basename(artdir), len(all_files), len(cdn_map), len(local_missing)))
    if local_missing:
        print("  ⚠ images absentes localement : %d, ex. %s"
              % (len(local_missing), ", ".join(local_missing[:3])))
    print("=" * 74)

    anomalies = []
    for r in rows:
        slug = r["slug"]
        path = os.path.join(ROOT, r["file"].replace("/", os.sep))
        raw = open(path, encoding="utf-8").read()
        body, unknown, nums, mismatch, missing = prepare(raw, slug, slug_set, by_num, cdn_map, dim_map)
        hero = next((x for x in by_slug.get(slug, []) if x["role"] == "hero"), None)
        want = int(r["images_to_resolve"])
        n_links = body.count("/blogs/%s/" % env["BLOG_HANDLE"])
        exists = sh.find_article(blog, slug)
        act = "MAJ" if exists else "CRÉATION"

        probs = []
        if body.count("<article") != 1: probs.append("article!=1")
        if "<style" in body.lower(): probs.append("style résiduel")
        if "<h1" in body.lower(): probs.append("h1 résiduel")
        if "PLACEHOLDER_" in body: probs.append("PLACEHOLDER résiduel")
        if body.count('class="gf-faq"') != 1: probs.append("faq!=1")
        if body.count('class="gf-cta"') != 1: probs.append("cta!=1")
        if body.count("/collections/stress") != 1: probs.append("collstress!=1")
        if "gf-imgph" in body: probs.append("gf-imgph résiduel")
        if len(nums) != want: probs.append("images %d!=%d(manifest)" % (len(nums), want))
        if unknown: probs.append("liens inconnus:%s" % unknown)
        if mismatch: probs.append("img slug-mismatch:%s" % mismatch)
        if missing: probs.append("Image N hors mapping:%s" % missing)
        if not r["excerpt"].strip(): probs.append("excerpt vide")
        if not hero: probs.append("pas d'image hero")
        if probs:
            anomalies.append("%s : %s" % (slug, "; ".join(probs)))

        print("  • [%-8s] %-40s" % (act, slug))
        print("      titre  : %s" % r["title"])
        print("      hero   : %s" % (hero["nouveau_fichier"] if hero else "—"))
        print("      images : %d | liens int. : %d | tags : %d | excerpt : %dc%s"
              % (len(nums), n_links, len([t for t in r["tags"].split(",") if t.strip()]),
                 len(r["excerpt"]), "  ⚠ " + "; ".join(probs) if probs else ""))

        if not args.dry_run and not probs:
            payload = make_payload(r, body, publish=False)
            payload["summary_html"] = r["excerpt"]
            if hero and hero["nouveau_fichier"] in cdn_map:
                payload["image"] = {"src": cdn_map[hero["nouveau_fichier"]],
                                    "alt": short_alt(hero["alt"])}
            res, a = sh.upsert_article(blog, payload)
            print("      -> %s OK id=%s" % (a, res.get("article", {}).get("id")))
            if args.bake:
                open(os.path.join(artdir, slug + ".html"), "w", encoding="utf-8").write(body + "\n")
            time.sleep(0.6)

    print("\n" + "=" * 74)
    print("Attendu manifest : %d liens, %d images."
          % (sum(int(r["links_to_resolve"]) for r in rows),
             sum(int(r["images_to_resolve"]) for r in rows)))
    if anomalies:
        print("ANOMALIES (%d) :" % len(anomalies))
        for a in anomalies: print("  ⚠ " + a)
    else:
        print("Aucune anomalie.")
    print("\nDRY-RUN : rien écrit." if args.dry_run else "Terminé.")


if __name__ == "__main__":
    main()
