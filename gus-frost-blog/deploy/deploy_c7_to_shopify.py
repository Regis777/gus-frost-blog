#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Déploie le cluster C7 (soins, manipulations et toilettage) dans le blog « Chiens » de Gus & Frost, EN BROUILLON,
sur le modèle C5 — avec les mêmes spécificités que C6 :
  - retrait du <h1> de tête (STRIP_H1=oui : le thème rend déjà le titre) ;
  - les images sont des encadrés <div class="gf-imgph">Image N - …</div> à remplacer
    par de vrais <img src alt> via C6_images_map.csv (clé = num « Image N »).

Corps déployé = fragment depuis <article>, sans <style> ni <h1> de tête,
liens PLACEHOLDER_{slug} -> /blogs/chiens/{slug} (CTA /collections/stress conservé),
<img> insérés (src = URL CDN après upload, alt = mapping). summary_html = excerpt.
Image à la une = image role=hero de l'article (+ son alt). published=false.

Usage :
  python deploy/deploy_c7_to_shopify.py --dry-run   # aucune écriture : diagnostic + récap
  python deploy/deploy_c7_to_shopify.py --bake      # upload images + crée les 13 brouillons
"""
import argparse
import csv
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify, read_manifest, make_payload          # noqa: E402
from upload_images import (staged_upload, existing_file_url, file_create,    # noqa: E402
                           wait_ready)

ARTDIR = os.path.join(ROOT, "articles", "cluster-7-soins-toilettage")
IMG_DIR = os.path.join(ROOT, "images", "cluster-7-soins-toilettage")   # 27 .png renommés (hero-<slug> + <slug>-n)
MAP = os.path.join(ARTDIR, "C7_images_map.csv")
PH_LINK = re.compile(r'PLACEHOLDER_([A-Za-z0-9\-]+)')
IMGPH = re.compile(r'<div class="gf-imgph">\s*Image\s*(\d+)\b[^<]*</div>', re.IGNORECASE)
H1_HEAD = re.compile(r'(<article\b[^>]*>\s*)<h1\b[^>]*>.*?</h1>\s*', re.S)


def load_map():
    rows = list(csv.DictReader(open(MAP, encoding="utf-8-sig")))
    by_num = {int(r["num"]): r for r in rows}
    by_slug = {}
    for r in rows:
        by_slug.setdefault(r["article_slug"], []).append(r)
    return rows, by_num, by_slug


def c7_rows():
    rows = [r for r in read_manifest() if r["cluster_num"] == "7"]
    rows.sort(key=lambda r: (0 if r["type"].upper() == "PILIER" else 1, r["slug"]))
    return rows


def prepare(raw, slug, slug_set, by_num, cdn_map):
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
        fn = row["nouveau_fichier"]
        src = cdn_map.get(fn, fn)
        alt = row["alt"].replace('"', "&quot;")
        return '<img src="%s" alt="%s">' % (src, alt)

    body = IMGPH.sub(repl, body)
    return body, unknown, nums, mismatch, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--bake", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()

    env = load_env()
    sh = Shopify(env)
    blog = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    _, by_num, by_slug = load_map()
    slug_set = {r["slug"] for r in read_manifest()}
    rows = c7_rows()
    if args.only:
        rows = [r for r in rows if r["slug"] == args.only]

    # images : présence locale + déjà sur Files
    all_files = sorted({r["nouveau_fichier"] for r in by_num.values()})
    local_missing = [f for f in all_files if not os.path.exists(os.path.join(IMG_DIR, f))]
    cdn_map = {}
    for f in all_files:
        u = existing_file_url(sh, f)
        if u:
            cdn_map[f] = u
        elif not args.dry_run and f not in local_missing:
            resource, _ = staged_upload(sh, os.path.join(IMG_DIR, f))
            fid = file_create(sh, resource, "")
            cdn_map[f] = wait_ready(sh, fid); time.sleep(0.3)

    mode = "DRY-RUN (aucune écriture)" if args.dry_run else "LIVE"
    print("=" * 74)
    print("C7 (soins-toilettage) -> blog «%s» | brouillon | %s" % (env["BLOG_HANDLE"], mode))
    print("Images : %d au total | déjà sur Files : %d | absentes localement : %d"
          % (len(all_files), len(cdn_map), len(local_missing)))
    if local_missing:
        print("  ⚠ à décompresser (images_C7_renamed.zip) avant exécution : %d fichiers, ex. %s"
              % (len(local_missing), ", ".join(local_missing[:3])))
    print("=" * 74)

    anomalies = []
    for r in rows:
        slug = r["slug"]
        path = os.path.join(ROOT, r["file"].replace("/", os.sep)) if "/" in r["file"] \
            else os.path.join(ARTDIR, r["file"])
        raw = open(path, encoding="utf-8").read()
        body, unknown, nums, mismatch, missing = prepare(raw, slug, slug_set, by_num, cdn_map)
        hero = next((x for x in by_slug.get(slug, []) if x["role"] == "hero"), None)
        want_imgs = int(r["images_to_resolve"])
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
        if len(nums) != want_imgs: probs.append("images %d!=%d(manifest)" % (len(nums), want_imgs))
        if unknown: probs.append("liens inconnus:%s" % unknown)
        if mismatch: probs.append("img slug-mismatch:%s" % mismatch)
        if missing: probs.append("Image N hors mapping:%s" % missing)
        if not r["excerpt"].strip(): probs.append("excerpt vide")
        if not hero: probs.append("pas d'image hero")
        if probs:
            anomalies.append("%s : %s" % (slug, "; ".join(probs)))

        print("  • [%-8s] %-38s" % (act, slug))
        print("      titre  : %s" % r["title"])
        print("      hero   : %s" % (hero["nouveau_fichier"] if hero else "—"))
        print("      images : %d | liens int. : %d | tags : %d | excerpt : %dc%s"
              % (len(nums), n_links, len([t for t in r["tags"].split(",") if t.strip()]),
                 len(r["excerpt"]), "  ⚠ " + "; ".join(probs) if probs else ""))

        if not args.dry_run and not probs:
            payload = make_payload(r, body, publish=False)
            payload["summary_html"] = r["excerpt"]
            if hero and hero["nouveau_fichier"] in cdn_map:
                payload["image"] = {"src": cdn_map[hero["nouveau_fichier"]], "alt": hero["alt"]}
            res, a = sh.upsert_article(blog, payload)
            print("      -> %s OK id=%s" % (a, res.get("article", {}).get("id")))
            if args.bake:
                open(os.path.join(ARTDIR, slug + ".html"), "w", encoding="utf-8").write(body + "\n")
            time.sleep(0.6)

    print("\n" + "=" * 74)
    tot_links = sum(int(r["links_to_resolve"]) for r in rows)
    tot_imgs = sum(int(r["images_to_resolve"]) for r in rows)
    print("Attendu manifest : %d liens, %d images." % (tot_links, tot_imgs))
    if anomalies:
        print("ANOMALIES (%d) :" % len(anomalies))
        for a in anomalies: print("  ⚠ " + a)
    else:
        print("Aucune anomalie.")
    print("\nDRY-RUN : rien écrit." if args.dry_run else "Terminé.")


if __name__ == "__main__":
    main()
