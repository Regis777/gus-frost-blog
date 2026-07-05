#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Déploie le cluster C5 (repas / gamelle) dans le blog « Chiens » de Gus & Frost,
EN BROUILLON, en reproduisant exactement la configuration des articles C4.

S'appuie sur l'outillage éprouvé du repo (scripts/publish.py, scripts/upload_images.py) :
  - authentification .env (Client Credentials Grant, token en cache) ;
  - blog cible = BLOG_HANDLE (chiens) ;
  - upsert idempotent par handle (create/update, jamais de doublon) ;
  - auteur « Gus & Frost », tags du manifest, SEO en métachamps global.title_tag /
    global.description_tag ;
  - images téléversées sur Shopify Files (réutilisées si déjà présentes) ;
  - image mise en avant = l'image hero- de l'article, alt repris du <img>.

Les corps articles/cluster-5-repas-gamelle/{slug}.html sont déjà :
  - nettoyés (pas de bloc <style> ni de commentaire d'en-tête, comme C4) ;
  - maillés (liens internes en /blogs/chiens/{slug}) ;
  - porteurs des noms d'images descriptifs (hero-...png) posés dans les src.

Usage (racine du repo) :
  python deploy/deploy_c5_to_shopify.py --dry-run   # aucune écriture : diagnostic complet
  python deploy/deploy_c5_to_shopify.py             # téléverse images + crée les 13 brouillons
  python deploy/deploy_c5_to_shopify.py --only repas-du-chien
Le passage EN LIGNE n'est jamais fait ici : published=false toujours.
"""
import argparse
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from publish import load_env, Shopify, read_manifest, make_payload  # noqa: E402
from upload_images import (staged_upload, existing_file_url,          # noqa: E402
                           file_create, wait_ready)

IMG_DIR = os.path.join(ROOT, "images", "cluster-5")
IMG_SRC_RE = re.compile(r'<img\b[^>]*\ssrc="([^"]+)"[^>]*>', re.IGNORECASE)
ALT_RE = re.compile(r'\salt="([^"]*)"', re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r'PLACEHOLDER_')


def c5_rows():
    rows = [r for r in read_manifest() if r["cluster_num"] == "5"]
    rows.sort(key=lambda r: (0 if r["type"] == "pilier" else 1, r["slug"]))
    return rows


def article_images(body):
    """Retourne [(src_name, alt), ...] dans l'ordre du document. Le 1er = hero."""
    out = []
    for tag in re.findall(r'<img\b[^>]*>', body, re.IGNORECASE):
        m = re.search(r'\ssrc="([^"]+)"', tag)
        if not m:
            continue
        alt = ALT_RE.search(tag)
        out.append((m.group(1), alt.group(1) if alt else ""))
    return out


def resolve_images(sh, names, do_upload):
    """names: set de noms de fichiers (ex. hero-repas-du-chien.png).
    Retourne (name->cdn_url, statut) ; statut: name->'reuse'|'upload'|'MISSING_LOCAL'."""
    url_map, status = {}, {}
    for name in sorted(names):
        local = os.path.join(IMG_DIR, name)
        reused = existing_file_url(sh, name)
        if reused:
            url_map[name] = reused
            status[name] = "reuse"
            continue
        if not os.path.exists(local):
            status[name] = "MISSING_LOCAL"
            continue
        if not do_upload:
            status[name] = "upload"   # serait téléversé
            continue
        resource_url, _ = staged_upload(sh, local)
        # alt renseigné à la création du fichier : repris du 1er article qui l'utilise
        fid = file_create(sh, resource_url, "")
        url_map[name] = wait_ready(sh, fid)
        status[name] = "upload"
        time.sleep(0.4)
    return url_map, status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="aucune écriture Shopify : diagnostic + récap.")
    ap.add_argument("--only", help="limiter à un slug.")
    ap.add_argument("--bake", action="store_true",
                    help="réécrire les {slug}.html du repo avec les URL CDN (mode live).")
    args = ap.parse_args()

    env = load_env()
    sh = Shopify(env)
    blog_handle = env.get("BLOG_HANDLE", "").strip()
    blog_id = sh.find_blog_id(blog_handle)

    rows = c5_rows()
    if args.only:
        rows = [r for r in rows if r["slug"] == args.only]
        if not rows:
            sys.exit("slug '%s' absent des lignes C5." % args.only)

    # collecte des corps + images
    bodies, all_imgs = {}, set()
    for r in rows:
        path = os.path.join(ROOT, r["file"].replace("/", os.sep))
        body = open(path, encoding="utf-8").read()
        bodies[r["slug"]] = body
        for name, _alt in article_images(body):
            all_imgs.add(name)

    mode = "DRY-RUN (aucune écriture)" if args.dry_run else "LIVE (écritures réelles)"
    print("=" * 72)
    print("C5 -> blog «%s» (id=%s) | brouillon (published=false) | %s"
          % (blog_handle, blog_id, mode))
    print("Articles : %d | images distinctes : %d" % (len(rows), len(all_imgs)))
    print("=" * 72)

    # images
    url_map, status = resolve_images(sh, all_imgs, do_upload=not args.dry_run)
    n_reuse = sum(1 for v in status.values() if v == "reuse")
    n_up = sum(1 for v in status.values() if v == "upload")
    n_miss = [k for k, v in status.items() if v == "MISSING_LOCAL"]
    print("\nIMAGES : %d déjà sur Files (réutilisées) | %d à téléverser%s"
          % (n_reuse, n_up, " (faits)" if not args.dry_run else ""))
    if n_miss:
        print("  ⚠ ABSENTES localement : %s" % ", ".join(n_miss))

    print("\nARTICLES :")
    anomalies = []
    for r in rows:
        slug = r["slug"]
        body = bodies[slug]
        imgs = article_images(body)
        hero = next((n for n, _a in imgs if n.startswith("hero-")), imgs[0][0] if imgs else None)
        hero_alt = next((a for n, a in imgs if n == hero), "")
        n_tags = len([t for t in r["tags"].split(",") if t.strip()])
        n_links = body.count("/blogs/%s/" % blog_handle)
        has_style = "<style" in body.lower()
        has_ph = bool(PLACEHOLDER_RE.search(body))
        existing = sh.find_article(blog_id, slug)
        action = "MAJ" if existing else "CRÉATION"
        if has_style:
            anomalies.append("%s : bloc <style> résiduel" % slug)
        if has_ph:
            anomalies.append("%s : PLACEHOLDER_ résiduel" % slug)
        if hero not in url_map and not args.dry_run:
            anomalies.append("%s : URL CDN hero manquante" % slug)
        print("  • [%-8s] %s" % (action, slug))
        print("      titre  : %s" % r["title"])
        print("      hero   : %s  (alt: %s)" % (hero, (hero_alt[:60] + "…") if len(hero_alt) > 60 else hero_alt))
        print("      tags   : %d | liens internes : %d | 2e image : %s"
              % (n_tags, n_links, next((n for n, _a in imgs if n != hero), "—")))

        if not args.dry_run:
            for name, cdn in url_map.items():
                body = body.replace('src="%s"' % name, 'src="%s"' % cdn)
            if args.bake:
                open(os.path.join(ROOT, r["file"].replace("/", os.sep)), "w",
                     encoding="utf-8").write(body)
            payload = make_payload(r, body, publish=False)
            if hero in url_map:
                payload["image"] = {"src": url_map[hero], "alt": hero_alt}
            result, act = sh.upsert_article(blog_id, payload)
            art = result.get("article", {})
            print("      -> %s OK (id=%s, published=%s)"
                  % (act, art.get("id"), art.get("published_at") is not None))
            time.sleep(0.6)

    print("\n" + "=" * 72)
    if anomalies:
        print("ANOMALIES :")
        for a in anomalies:
            print("  ⚠ " + a)
    else:
        print("Aucune anomalie détectée.")
    if args.dry_run:
        print("\nDRY-RUN terminé : rien n'a été écrit sur Shopify.")
    else:
        print("\nTerminé : 13 brouillons dans le blog « %s ». À relire puis publier à la main."
              % blog_handle)


if __name__ == "__main__":
    main()
