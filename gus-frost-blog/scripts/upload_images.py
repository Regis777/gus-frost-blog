#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integre les images d'un article : uploade les fichiers locaux sur les Fichiers Shopify
(Content > Files), remplace les src="REMPLACER_..." par les URLs CDN, et republie
l'article (brouillon par defaut).

PRE-REQUIS :
  - app avec scopes write_files + read_files (sinon HTTP 403 sur stagedUploadsCreate).
  - deposer les images dans images/<dossier-cluster>/ avec le nom = ce qui suit
    "REMPLACER_" dans le HTML (voir images/.../_A_DEPOSER_ICI.md).

Flux Shopify Files :
  stagedUploadsCreate -> POST multipart vers le staging -> fileCreate(originalSource)
  -> polling node(id) jusqu'a fileStatus READY -> recuperation de image.url.

Usage :
  python scripts/upload_images.py --only anxiete-separation-chien            # republie en brouillon
  python scripts/upload_images.py --only anxiete-separation-chien --dry-run  # uploade + ecrit build/, sans toucher l'article
  python scripts/upload_images.py --only anxiete-separation-chien --publish  # published=true (NE PAS sans validation)
"""
import argparse
import json
import mimetypes
import os
import sys
import time
import uuid
import urllib.request
import urllib.error

from publish import (load_env, Shopify, ROOT, read_manifest, build_resolver,
                     resolve_body, wrap_cta_call, make_payload, BUILD_DIR)
from wire_theme import gql

IMG_TOKEN_PREFIX = "REMPLACER_"
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")


def find_local_image(images_dir, base_name):
    """base_name = nom attendu (ce qui suit REMPLACER_), ex. 'hero-anxiete-separation.jpg'.
    Tolerant a l'extension : si 'hero.jpg' absent mais 'hero.png' present, le prend."""
    direct = os.path.join(images_dir, base_name)
    if os.path.exists(direct):
        return direct
    stem = os.path.splitext(base_name)[0]
    for ext in IMG_EXTS:
        p = os.path.join(images_dir, stem + ext)
        if os.path.exists(p):
            return p
    return None


def multipart_post(url, fields, file_field, filename, file_bytes, mime):
    """POST multipart/form-data en stdlib. fields = liste [{name,value}] (ordre important)."""
    boundary = "----gfboundary" + uuid.uuid4().hex
    crlf = b"\r\n"
    body = []
    for f in fields:
        body.append(("--" + boundary).encode())
        body.append(('Content-Disposition: form-data; name="%s"' % f["name"]).encode())
        body.append(b"")
        body.append(str(f["value"]).encode())
    body.append(("--" + boundary).encode())
    body.append(('Content-Disposition: form-data; name="%s"; filename="%s"'
                 % (file_field, filename)).encode())
    body.append(("Content-Type: %s" % mime).encode())
    body.append(b"")
    body.append(file_bytes)
    body.append(("--" + boundary + "--").encode())
    body.append(b"")
    data = crlf.join(body)
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)
    with urllib.request.urlopen(req) as r:
        return r.status, r.read().decode("utf-8", "replace")


def staged_upload(sh, path):
    filename = os.path.basename(path)
    mime = mimetypes.guess_type(filename)[0] or "image/jpeg"
    size = os.path.getsize(path)
    m = """
    mutation($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets { url resourceUrl parameters { name value } }
        userErrors { field message }
      }
    }"""
    variables = {"input": [{
        "filename": filename, "mimeType": mime, "resource": "FILE",
        "httpMethod": "POST", "fileSize": str(size),
    }]}
    d = gql(sh, m, variables)
    res = d["stagedUploadsCreate"]
    if res["userErrors"]:
        raise SystemExit("stagedUploadsCreate: %s" % res["userErrors"])
    target = res["stagedTargets"][0]
    with open(path, "rb") as f:
        content = f.read()
    fields = [{"name": p["name"], "value": p["value"]} for p in target["parameters"]]
    status, resp = multipart_post(target["url"], fields, "file", filename, content, mime)
    if status not in (200, 201, 204):
        raise SystemExit("Upload staging echoue (HTTP %s) : %s" % (status, resp))
    return target["resourceUrl"], mime


def existing_file_url(sh, filename):
    """URL CDN d'un fichier deja present dans la bibliotheque Shopify (recherche par nom),
    sinon None. Evite les doublons / re-uploads."""
    stem = os.path.splitext(filename)[0]
    q = """
    query($q: String!) {
      files(first: 25, query: $q) {
        nodes { ... on MediaImage { fileStatus image { url } } }
      }
    }"""
    try:
        d = gql(sh, q, {"q": "filename:%s" % stem})
    except (SystemExit, Exception):
        return None  # recherche indisponible -> on uploadera
    for n in (d.get("files", {}) or {}).get("nodes", []):
        url = (n.get("image") or {}).get("url", "") or ""
        if n.get("fileStatus") == "READY" and ("/%s." % stem) in url:
            return url
    return None


def file_create(sh, resource_url, alt):
    m = """
    mutation($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files { id fileStatus alt }
        userErrors { field message }
      }
    }"""
    variables = {"files": [{
        "originalSource": resource_url, "contentType": "IMAGE", "alt": alt or "",
    }]}
    d = gql(sh, m, variables)
    res = d["fileCreate"]
    if res["userErrors"]:
        raise SystemExit("fileCreate: %s" % res["userErrors"])
    return res["files"][0]["id"]


def wait_ready(sh, file_id, timeout=120):
    q = """
    query($id: ID!) {
      node(id: $id) {
        ... on MediaImage { fileStatus image { url width height } }
      }
    }"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        d = gql(sh, q, {"id": file_id})
        node = d.get("node") or {}
        status = node.get("fileStatus")
        if status == "READY":
            img = node.get("image") or {}
            if img.get("url"):
                return img["url"]
        if status == "FAILED":
            raise SystemExit("Traitement image FAILED (%s)" % file_id)
        time.sleep(2)
    raise SystemExit("Timeout: image pas READY apres %ss (%s)" % (timeout, file_id))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", required=True, help="slug de l'article")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--dry-run", action="store_true",
                    help="uploade les images mais n'ecrit pas l'article (ecrit build/<slug>.html)")
    args = ap.parse_args()

    env = load_env()
    row = next((r for r in read_manifest() if r["slug"] == args.only), None)
    if not row:
        sys.exit("slug '%s' absent du manifest." % args.only)

    art_path = os.path.join(ROOT, row["file"].replace("/", os.sep))
    with open(art_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # dossier images : images/<meme-dossier-que-l-article>/
    cluster_dir = os.path.basename(os.path.dirname(art_path))
    images_dir = os.path.join(ROOT, "images", cluster_dir)

    # collecte des tokens REMPLACER_ + alt
    import re
    tokens = {}  # base_name -> alt
    for mtag in re.finditer(r'<img\b[^>]*>', raw, re.IGNORECASE):
        tag = mtag.group(0)
        srcm = re.search(r'src="(REMPLACER_[^"]+)"', tag)
        if not srcm:
            continue
        token = srcm.group(1)
        base = token[len(IMG_TOKEN_PREFIX):]
        altm = re.search(r'alt="([^"]*)"', tag)
        tokens[token] = (base, altm.group(1) if altm else "")

    if not tokens:
        sys.exit("Aucune image REMPLACER_ dans cet article.")

    # verif presence des fichiers AVANT tout appel API
    missing, plan = [], {}
    for token, (base, alt) in tokens.items():
        p = find_local_image(images_dir, base)
        if not p:
            missing.append(base)
        else:
            plan[token] = (p, alt)
    print("Dossier images : %s" % os.path.relpath(images_dir, ROOT))
    if missing:
        sys.exit("Images manquantes (%d) : %s\nDepose-les puis relance."
                 % (len(missing), ", ".join(missing)))

    sh = Shopify(env)
    url_map = {}
    for token, (path, alt) in plan.items():
        fname = os.path.basename(path)
        reused = existing_file_url(sh, fname)
        if reused:
            url_map[token] = reused
            print("- %s\n    -> (deja present, reutilise) %s" % (token, reused))
            continue
        print("- %s" % token)
        resource_url, _mime = staged_upload(sh, path)
        fid = file_create(sh, resource_url, alt)
        cdn = wait_ready(sh, fid)
        url_map[token] = cdn
        print("    -> %s" % cdn)
        time.sleep(0.4)

    # corps final : liens resolus + images remplacees
    resolver = build_resolver(env)
    body, _unres, _n = resolve_body(raw, resolver)
    body = wrap_cta_call(body)
    for token, cdn in url_map.items():
        body = body.replace('src="%s"' % token, 'src="%s"' % cdn)

    if args.dry_run:
        os.makedirs(BUILD_DIR, exist_ok=True)
        out = os.path.join(BUILD_DIR, args.only + ".html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(body)
        print("\nDry-run : %d image(s) traitee(s), article NON modifie. Ecrit : %s"
              % (len(url_map), os.path.relpath(out, ROOT)))
        return

    blog_id = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    payload = make_payload(row, body, args.publish)
    result, action = sh.upsert_article(blog_id, payload)
    art = result.get("article", {})
    print("\nArticle %s OK (id=%s, published=%s)"
          % (action, art.get("id"), art.get("published_at") is not None))


if __name__ == "__main__":
    main()
