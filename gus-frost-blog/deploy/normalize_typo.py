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
  --bodies  corps EN LIGNE (relu sur Shopify, jamais le fragment repo qui, pour
            C1/C2/C3, porte encore des src="REMPLACER_...") -> pousse body_html.

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


def retry(fn, essais=6):
    """Shopify plafonne a 2 req/s : temporise, et repart en arriere sur un 429."""
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
    """IMPORTANT : on normalise le corps **en ligne**, pas le fragment du repo.

    Les clusters anciens (C1, C2, C3) n'ont jamais ete « bakes » : leur fragment
    repo porte encore des src="REMPLACER_..." et n'a pas les URLs CDN. Pousser le
    repo remplacerait les images par des placeholders. Le corps Shopify est donc la
    seule source de verite ici ; on le relit, on le normalise, on le repousse.
    Le fragment repo est normalise separement, pour rester lisible, sans etre pousse.
    """
    rows = read_manifest()
    if args.cluster:
        rows = [r for r in rows if r["cluster_num"] == str(args.cluster)]
    env = load_env()
    sh = Shopify(env)
    blog = sh.find_blog_id(env["BLOG_HANDLE"].strip())

    cibles = []
    for r in rows:
        art = retry(lambda: sh.find_article(blog, r["slug"]))
        if not art:
            print("  ⚠ %-40s ABSENT en ligne" % r["slug"]); continue
        n = compte(art["body_html"])
        if n:
            cibles.append((r, art, n))
    print("Corps a normaliser EN LIGNE : %d article(s), %d occurrence(s)"
          % (len(cibles), sum(n for _r, _a, n in cibles)))
    for r, art, n in cibles[:5]:
        m = re.search(r".{0,45}[ ][;:!?»].{0,15}", art["body_html"])
        print("   ex. %-40s %3d  %s" % (r["slug"], n,
                                        m.group(0).replace("\n", " ") if m else ""))
    if args.dry_run:
        print("\nDRY-RUN : rien ecrit, rien pousse.")
        return

    pousses = 0
    for r, art, _n in cibles:
        body = norm(art["body_html"])
        retry(lambda: sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, art["id"]),
                              {"article": {"id": art["id"], "body_html": body}}))
        pousses += 1
        if pousses % 20 == 0:
            print("  … %d poussés" % pousses)

    # fragments repo : normalises pour rester coherents, jamais pousses
    locaux = 0
    for r in rows:
        p = os.path.join(ROOT, r["file"].replace("/", os.sep))
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        i = s.find("<article")
        if i < 0 or not compte(s[i:]):
            continue
        open(p, "w", encoding="utf-8").write(s[:i] + norm(s[i:]))
        locaux += 1
    print("\n%d corps en ligne mis à jour | %d fragment(s) repo normalisé(s)."
          % (pousses, locaux))


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
