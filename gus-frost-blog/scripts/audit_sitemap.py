#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit d'indexation : lit le sitemap Shopify (et ses sous-sitemaps), fait une
requete HEAD sur chaque URL et classe les reponses.

  python scripts/audit_sitemap.py [--delai 0.3] [--sortie build/audit_sitemap.csv]

Ne modifie rien en ligne : lecture seule.
"""
import argparse
import csv
import os
import re
import sys
import time
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (compatible; GusEtFrost-audit-seo/1.0)"
RACINE = "https://gusetfrost.fr/sitemap.xml"


def http(url, methode="GET"):
    req = urllib.request.Request(url, method=methode, headers={"User-Agent": UA})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        return r.status, r.headers.get("Location"), r.geturl(), r.read() if methode == "GET" else b""
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location"), url, b""
    except Exception as e:
        return 0, str(e), url, b""


class SansRedirection(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(SansRedirection)


def head_sans_suivi(url):
    """Renvoie (code, destination). Ne suit pas la redirection."""
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        r = OPENER.open(req, timeout=30)
        return r.status, ""
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location") or ""
    except Exception as e:
        return 0, str(e)


def urls_du_sitemap(url, vus):
    """Descend recursivement dans les sitemaps et rend la liste des <loc> de pages."""
    if url in vus:
        return []
    vus.add(url)
    code, _, _, corps = http(url)
    if code != 200:
        print("  sitemap illisible (%s) : %s" % (code, url), file=sys.stderr)
        return []
    xml = corps.decode("utf-8", "replace")
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    if "<sitemapindex" in xml:
        out = []
        for sous in locs:
            print("  sous-sitemap : %s" % sous)
            out.extend(urls_du_sitemap(sous, vus))
        return out
    return locs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--delai", type=float, default=0.3)
    ap.add_argument("--sortie", default="build/audit_sitemap.csv")
    a = ap.parse_args()

    print("Lecture du sitemap : %s" % RACINE)
    urls = urls_du_sitemap(RACINE, set())
    # dedoublonnage en conservant l'ordre
    vus, propres = set(), []
    for u in urls:
        if u not in vus:
            vus.add(u)
            propres.append(u)
    print("%d URL a verifier\n" % len(propres))

    sortie = os.path.join(ROOT, a.sortie)
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    compte = {}
    with open(sortie, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["url", "code", "destination", "type"])
        for i, u in enumerate(propres, 1):
            code, dest = head_sans_suivi(u)
            if code == 200:
                genre = "ok"
            elif 300 <= code < 400:
                genre = "redirection"
            elif code == 404:
                genre = "404"
            elif code == 0:
                genre = "erreur reseau"
            else:
                genre = "http %s" % code
            compte[genre] = compte.get(genre, 0) + 1
            w.writerow([u, code, dest, genre])
            if genre != "ok":
                print("  %-12s %s -> %s" % (genre, u, dest))
            if i % 50 == 0:
                print("... %d/%d" % (i, len(propres)))
            time.sleep(a.delai)

    print("\n--- bilan ---")
    for k in sorted(compte):
        print("%-14s %d" % (k, compte[k]))
    print("\nDetail : %s" % sortie)


if __name__ == "__main__":
    main()
