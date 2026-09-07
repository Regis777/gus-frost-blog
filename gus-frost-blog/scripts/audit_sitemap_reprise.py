#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reteste les URL non concluantes de build/audit_sitemap.csv (429, erreurs reseau)
   avec un rythme plus lent et quelques nouvelles tentatives, puis reecrit le CSV."""
import argparse, csv, os, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "build", "audit_sitemap.csv")
UA = "Mozilla/5.0 (compatible; GusEtFrost-audit-seo/1.0)"


class SansRedirection(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(SansRedirection)


def head(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        r = OPENER.open(req, timeout=30)
        return r.status, ""
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location") or ""
    except Exception as e:
        return 0, str(e)


def genre(code):
    if code == 200:
        return "ok"
    if 300 <= code < 400:
        return "redirection"
    if code == 404:
        return "404"
    if code == 0:
        return "erreur reseau"
    return "http %s" % code


ap = argparse.ArgumentParser()
ap.add_argument("--delai", type=float, default=1.5)
ap.add_argument("--attente-initiale", dest="attente", type=float, default=0,
                help="pause avant de commencer, le temps que le pare-feu Shopify relache l'IP")
a = ap.parse_args()
if a.attente:
    print("pause de %d s avant de commencer" % a.attente); sys.stdout.flush()
    time.sleep(a.attente)

rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
a_refaire = [r for r in rows if r["type"] not in ("ok", "404", "redirection")]
print("%d URL a reprendre sur %d" % (len(a_refaire), len(rows)))

for i, r in enumerate(a_refaire, 1):
    for essai in range(1, 4):
        code, dest = head(r["url"])
        if code != 429:
            break
        attente = 20 * essai
        print("   429, pause %ds (%s)" % (attente, r["url"]))
        time.sleep(attente)
    r["code"], r["destination"], r["type"] = code, dest, genre(code)
    if r["type"] != "ok":
        print("  %-12s %s -> %s" % (r["type"], r["url"], dest))
    if i % 25 == 0:
        print("... %d/%d" % (i, len(a_refaire)))
        sys.stdout.flush()
    time.sleep(a.delai)

with open(CSV, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["url", "code", "destination", "type"])
    for r in rows:
        w.writerow([r["url"], r["code"], r["destination"], r["type"]])

compte = {}
for r in rows:
    compte[r["type"]] = compte.get(r["type"], 0) + 1
print("\n--- bilan final ---")
for k in sorted(compte):
    print("%-14s %d" % (k, compte[k]))
