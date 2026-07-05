#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Passe 2 du cluster C5 : les 13 articles existent déjà (créés par deploy_c5_to_shopify.py).
Cette passe MET À JOUR chaque article avec :
  - le NOUVEAU corps (versions v1 enrichies : bloc FAQ gf-faq + bloc CTA gf-cta vers
    /collections/stress) ;
  - l'EXTRAIT (summary_html) repris de C5_extraits.csv (distinct de la méta-description).

Sûreté : mise à jour MINIMALE (body_html + summary_html uniquement). On NE touche PAS
au statut de publication (le pilier reste EN LIGNE, les 12 satellites restent brouillon),
ni aux tags, SEO métachamps, auteur ou image à la une (déjà posés en passe 1).

Corps préparé comme en passe 1 / comme C4 : commentaire d'en-tête + bloc <style> retirés
(slice depuis <article>), liens PLACEHOLDER_{slug} -> /blogs/chiens/{slug}, src images
-> URL CDN (réutilise les fichiers déjà sur Shopify Files). FAQ, CTA et le lien réel
/collections/stress sont conservés tels quels.

Usage :
  python deploy/update_c5_faq_cta.py --dry-run      # aucun écrit : diagnostic + récap
  python deploy/update_c5_faq_cta.py --bake         # met à jour + réécrit les {slug}.html
"""
import argparse
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import load_env, Shopify, read_manifest          # noqa: E402
from upload_images import existing_file_url                    # noqa: E402

ARTDIR = os.path.join(ROOT, "articles", "cluster-5-repas-gamelle")
EXTRAITS = os.path.join(ROOT, "C5_extraits.csv")
PH_RE = re.compile(r'PLACEHOLDER_([A-Za-z0-9\-]+)')
IMG_RE = re.compile(r'<img\b[^>]*\ssrc="([^"]+)"', re.IGNORECASE)


def c5_rows():
    rows = [r for r in read_manifest() if r["cluster_num"] == "5"]
    rows.sort(key=lambda r: (0 if r["type"] == "pilier" else 1, r["slug"]))
    return rows


def v1_path(slug):
    for f in os.listdir(ARTDIR):
        if re.match(r'2026-07-03_[A-Z0-9]+_%s_v1\.html$' % re.escape(slug), f):
            return os.path.join(ARTDIR, f)
    return None


def load_extraits():
    d = {}
    with open(EXTRAITS, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            d[r["slug"].strip()] = r["extrait"].strip()
    return d


def prepare_body(raw, slug_set, cdn_map):
    """slice <article>..end ; resolve PLACEHOLDER ; bake CDN images. Retourne (body, unknown_links, missing_imgs)."""
    i = raw.find("<article")
    body = raw[i:].rstrip()
    unknown = sorted({s for s in PH_RE.findall(body) if s not in slug_set})
    body = PH_RE.sub(lambda m: "/blogs/chiens/" + m.group(1), body)
    missing = []
    for name in IMG_RE.findall(body):
        if name.startswith("http"):
            continue
        cdn = cdn_map.get(name)
        if cdn:
            body = body.replace('src="%s"' % name, 'src="%s"' % cdn)
        else:
            missing.append(name)
    return body, unknown, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--bake", action="store_true", help="réécrit les {slug}.html + supprime les v1 (mode live).")
    ap.add_argument("--only")
    args = ap.parse_args()

    env = load_env()
    sh = Shopify(env)
    blog = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    extraits = load_extraits()
    rows = c5_rows()
    if args.only:
        rows = [r for r in rows if r["slug"] == args.only]
    slug_set = {r["slug"] for r in read_manifest()}

    # map images -> CDN (déjà téléversées en passe 1)
    imgnames = set()
    vmap = {}
    for r in rows:
        p = v1_path(r["slug"])
        vmap[r["slug"]] = p
        if p:
            for n in IMG_RE.findall(open(p, encoding="utf-8").read()):
                if not n.startswith("http"):
                    imgnames.add(n)
    cdn_map = {}
    for n in sorted(imgnames):
        u = existing_file_url(sh, n)
        if u:
            cdn_map[n] = u

    mode = "DRY-RUN (aucune écriture)" if args.dry_run else "LIVE"
    print("=" * 72)
    print("C5 passe 2 (FAQ+CTA+extrait) -> blog «%s» | %s" % (env["BLOG_HANDLE"], mode))
    print("Images résolues CDN : %d/%d" % (len(cdn_map), len(imgnames)))
    print("=" * 72)

    anomalies = []
    for r in rows:
        slug = r["slug"]
        p = vmap[slug]
        if not p:
            anomalies.append("%s : fichier v1 introuvable" % slug); print("  ✗ %s : v1 introuvable" % slug); continue
        raw = open(p, encoding="utf-8").read()
        body, unknown, missing = prepare_body(raw, slug_set, cdn_map)
        extrait = extraits.get(slug, "")
        art = sh.find_article(blog, slug)
        exists = art is not None
        published = bool(art.get("published_at")) if exists else False
        img = (art.get("image") or {}).get("src", "—") if exists else "—"
        # contrôles
        chk = {
            "faq": body.count('class="gf-faq"'),
            "cta": body.count('class="gf-cta"'),
            "coll": body.count('/collections/stress'),
            "article": body.count('<article'),
            "style": 1 if "<style" in body.lower() else 0,
            "ph": 1 if "PLACEHOLDER_" in body else 0,
        }
        problems = []
        if chk["faq"] != 1: problems.append("faq=%d" % chk["faq"])
        if chk["cta"] != 1: problems.append("cta=%d" % chk["cta"])
        if chk["coll"] != 1: problems.append("collstress=%d" % chk["coll"])
        if chk["article"] != 1: problems.append("article=%d" % chk["article"])
        if chk["style"]: problems.append("style résiduel")
        if chk["ph"]: problems.append("PLACEHOLDER résiduel")
        if unknown: problems.append("liens inconnus:%s" % unknown)
        if missing: problems.append("img non résolues:%s" % missing)
        if not extrait: problems.append("extrait manquant")
        if not exists: problems.append("article inexistant (serait créé)")
        if problems:
            anomalies.append("%s : %s" % (slug, "; ".join(problems)))

        action = "MAJ" if exists else "CRÉATION"
        print("  • [%-3s] %-30s published=%s | faq=%d cta=%d coll=%d | extrait=%dc"
              % (action, slug, published, chk["faq"], chk["cta"], chk["coll"], len(extrait)))
        if problems:
            print("        ⚠ " + "; ".join(problems))

        if not args.dry_run and exists and not problems:
            payload = {"id": art["id"], "body_html": body, "summary_html": extrait}
            sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, art["id"]), {"article": payload})
            print("        -> MAJ OK (body+extrait ; published inchangé=%s)" % published)
            if args.bake:
                out = os.path.join(ARTDIR, slug + ".html")
                open(out, "w", encoding="utf-8", newline="").write(body + "\n")

    if args.bake and not args.dry_run:
        for r in rows:
            p = vmap.get(r["slug"])
            if p and os.path.exists(p):
                os.remove(p)
        print("\nFichiers v1 supprimés, {slug}.html réécrits.")

    print("\n" + "=" * 72)
    if anomalies:
        print("ANOMALIES (%d) :" % len(anomalies))
        for a in anomalies:
            print("  ⚠ " + a)
    else:
        print("Aucune anomalie.")
    print("DRY-RUN terminé, rien écrit." if args.dry_run else "Terminé.")


if __name__ == "__main__":
    main()
