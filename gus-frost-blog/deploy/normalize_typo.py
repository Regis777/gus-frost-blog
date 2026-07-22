#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Typo FR sur l'existant en ligne : pose les espaces insecables manquantes.

Regle (absolue, cf. Regis) : U+00A0 avant ; : ! ? » et apres «.
Les articles recents sortent deja normalises de mkfinal (normalize_fr) ; ce script
rattrape l'existant qui a ete saisi en espaces ASCII.

Deux perimetres INDEPENDANTS :
  --fields  title / meta_title / meta_description / excerpt du manifest
            -> pousse title, summary_html et les metafields SEO. Le corps n'est pas touche.
  --bodies  corps des fragments du repo -> pousse body_html.

Usage :
  python deploy/normalize_typo.py --fields --dry-run
  python deploy/normalize_typo.py --fields
  python deploy/normalize_typo.py --bodies --dry-run [--cluster 1]
"""
import argparse, csv, glob, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify, read_manifest        # noqa: E402

NBSP = " "
MANIFEST = os.path.join(ROOT, "manifest.csv")
FIELDS = ["title", "meta_title", "meta_description", "excerpt"]


def norm(s):
    s = re.sub(r"[  ]+([;:!?»])", NBSP + r"\1", s)
    s = re.sub(r"«[  ]+", "«" + NBSP, s)
    return s


def compte(s):
    return len(re.findall(r"[ ]+[;:!?»]", s)) + len(re.findall(r"«[ ]+", s))


def do_fields(args):
    rows = list(csv.DictReader(open(MANIFEST, encoding="utf-8-sig")))
    hdr = list(rows[0].keys())
    touches, exemples, modifies = 0, [], set()
    for r in rows:
        for c in FIELDS:
            if compte(r[c]):
                if len(exemples) < 5:
                    exemples.append((r["slug"], c, r[c][:70]))
                r[c] = norm(r[c])
                touches += 1
                modifies.add(r["slug"])
    print("Champs manifest a normaliser : %d (sur %d article(s))" % (touches, len(modifies)))
    for s, c, v in exemples:
        print("   ex. %-34s %-16s %s" % (s, c, v))
    if args.dry_run:
        print("\nDRY-RUN : manifest non ecrit, rien pousse.")
        return

    w = csv.DictWriter(open(MANIFEST, "w", encoding="utf-8", newline=""), fieldnames=hdr)
    w.writeheader()
    [w.writerow(r) for r in rows]
    print("manifest.csv normalise.")

    env = load_env()
    sh = Shopify(env)
    blog = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    pousses = absents = 0
    for r in rows:
        if r["slug"] not in modifies:
            continue  # inchange : on ne touche pas l'article en ligne
        art = sh.find_article(blog, r["slug"])
        if not art:
            print("  ⚠ %-40s ABSENT en ligne" % r["slug"]); absents += 1; continue
        payload = {"id": art["id"], "title": r["title"], "summary_html": r["excerpt"],
                   "metafields": [
                       {"namespace": "global", "key": "title_tag",
                        "value": r["meta_title"], "type": "single_line_text_field"},
                       {"namespace": "global", "key": "description_tag",
                        "value": r["meta_description"], "type": "single_line_text_field"}]}
        sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, art["id"]), {"article": payload})
        pousses += 1
        if pousses % 25 == 0:
            print("  … %d poussés" % pousses)
        time.sleep(0.35)
    print("\n%d article(s) mis à jour | %d absent(s)" % (pousses, absents))


def do_bodies(args):
    rows = read_manifest()
    if args.cluster:
        rows = [r for r in rows if r["cluster_num"] == str(args.cluster)]
    cibles = []
    for r in rows:
        p = os.path.join(ROOT, r["file"].replace("/", os.sep))
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        i = s.find("<article")
        if i < 0 or not compte(s[i:]):
            continue
        cibles.append((r, p, s, i))
    print("Corps a normaliser : %d article(s), %d occurrence(s)"
          % (len(cibles), sum(compte(s[i:]) for _r, _p, s, i in cibles)))
    for r, _p, s, i in cibles[:5]:
        m = re.search(r".{0,45}[ ][;:!?»].{0,15}", s[i:])
        print("   ex. %-40s %s" % (r["slug"], m.group(0).replace("\n", " ") if m else ""))
    if args.dry_run:
        print("\nDRY-RUN : rien ecrit, rien pousse.")
        return

    env = load_env()
    sh = Shopify(env)
    blog = sh.find_blog_id(env["BLOG_HANDLE"].strip())
    pousses = 0
    for r, p, s, i in cibles:
        body = norm(s[i:])
        open(p, "w", encoding="utf-8").write(s[:i] + body)
        art = sh.find_article(blog, r["slug"])
        if not art:
            print("  ⚠ %-40s ABSENT en ligne" % r["slug"]); continue
        sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, art["id"]),
                {"article": {"id": art["id"], "body_html": body}})
        pousses += 1
        time.sleep(0.35)
    print("\n%d corps mis à jour." % pousses)


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--fields", action="store_true")
    g.add_argument("--bodies", action="store_true")
    ap.add_argument("--cluster", type=int, help="restreint --bodies a un cluster_num")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    (do_fields if args.fields else do_bodies)(args)


if __name__ == "__main__":
    main()
