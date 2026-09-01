#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenere et republie une page hub (« Conseils chiens » / « Conseils chats ») en
une commande, en allant chercher la liste des brouillons directement dans
Shopify au lieu de la coller a la main.

Le garde-fou : un satellite publie dont le PILIER est encore en brouillon
disparait de la page regeneree (build_blog_hub.py saute le theme entier). Sans
controle, une regeneration faite trop tot retire des articles publies du
sommaire et les prive de leur lien entrant. Le script refuse donc d'ecrire tant
qu'un article aujourd'hui liste sortirait de la page.

Usage :
  python scripts/refresh_hub.py --blog chats              # dry-run + diagnostic
  python scripts/refresh_hub.py --blog chats --apply
  python scripts/refresh_hub.py --blog chats --apply --force   # assume les pertes
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from publish import load_env, Shopify  # noqa: E402

BLOGS = {
    "chiens": {
        "manifest": "manifest.csv",
        "page": "conseils-chiens",
        "titre": "Conseils chiens",
        "intro": ("Tous nos guides et conseils pour comprendre et accompagner votre chien, "
                  "organisés par thème. Chaque thème s'ouvre sur un guide principal, "
                  "complété par des articles détaillés."),
    },
    "chats": {
        "manifest": "manifest_chat.csv",
        "page": "conseils-chats",
        "titre": "Conseils chats",
        "intro": ("Tous nos guides et conseils pour comprendre et accompagner votre chat, "
                  "organisés par thème. Chaque thème s'ouvre sur un guide principal, "
                  "complété par des articles détaillés."),
    },
}


def tous_les_articles(sh, blog_id):
    """Pagine par curseur (en-tete Link, rel=next).

    NE PAS revenir a `since_id` : sur ce blog il rendait 250 articles sur 264,
    et les 14 manquants etaient alors pris pour des non-publies — le garde-fou
    ci-dessous devenait faux. Le total est reverifie contre articles/count.json.
    """
    url = "%s/blogs/%s/articles.json?limit=250" % (sh.base, blog_id)
    arts = []
    while url:
        req = urllib.request.Request(url)
        req.add_header("X-Shopify-Access-Token", sh.token)
        with urllib.request.urlopen(req) as resp:
            arts += json.loads(resp.read().decode("utf-8"))["articles"]
            lien = resp.headers.get("Link", "") or ""
        suivant = re.search(r'<([^>]+)>;\s*rel="next"', lien)
        url = suivant.group(1) if suivant else None

    attendu = sh._req("GET", "/blogs/%s/articles/count.json" % blog_id)["count"]
    if len(arts) != attendu:
        sys.exit("REFUS : %d articles recuperes pour %d annonces — pagination incomplete."
                 % (len(arts), attendu))
    return arts


def liens(html, blog):
    return set(re.findall(r'/blogs/%s/([a-z0-9\-]+)' % blog, html))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blog", choices=sorted(BLOGS), required=True)
    ap.add_argument("--apply", action="store_true", help="ecrit la page (sinon dry-run)")
    ap.add_argument("--force", action="store_true",
                    help="ecrit meme si des articles publies sortent du sommaire")
    args = ap.parse_args()
    conf = BLOGS[args.blog]

    sh = Shopify(load_env())
    blog = next((b for b in sh._req("GET", "/blogs.json?limit=250")["blogs"]
                 if b["handle"] == args.blog), None)
    if blog is None:
        sys.exit("Blog '%s' introuvable." % args.blog)

    arts = tous_les_articles(sh, blog["id"])
    publies = {a["handle"] for a in arts if a.get("published_at")}
    brouillons = {a["handle"] for a in arts if not a.get("published_at")}
    print("Blog %s : %d articles (%d publies, %d brouillons)"
          % (args.blog, len(publies) + len(brouillons), len(publies), len(brouillons)))

    out = "build/hub_%s.html" % args.blog
    cmd = [sys.executable, os.path.join(ROOT, "scripts", "build_blog_hub.py"),
           "--blog", args.blog, "--manifest", conf["manifest"], "--out", out,
           "--intro", conf["intro"], "--draft", ",".join(sorted(brouillons))]
    # PYTHONIOENCODING : sans ca, le fils ecrit en cp1252 et la lecture utf-8 casse.
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                         encoding="utf-8", errors="replace", env=env)
    if res.returncode:
        sys.exit("build_blog_hub.py a echoue :\n%s" % (res.stderr or res.stdout))
    print((res.stdout or "").strip())

    nouveau = open(os.path.join(ROOT, out), encoding="utf-8").read()
    page = sh._req("GET", "/pages.json?handle=%s&limit=1" % conf["page"])["pages"]
    if not page:
        sys.exit("Page '%s' introuvable : la creer d'abord avec create_blog_hub_page.py" % conf["page"])
    page = page[0]

    avant, apres = liens(page["body_html"], args.blog), liens(nouveau, args.blog)
    perdus = sorted((avant - apres) & publies)   # publies, listes aujourd'hui, absents demain
    gagnes = sorted(apres - avant)
    morts = sorted(apres & brouillons)

    print("\nliens : %d -> %d   (+%d, -%d)" % (len(avant), len(apres), len(gagnes), len(avant - apres)))
    if morts:
        sys.exit("REFUS : %d lien(s) vers des brouillons : %s" % (len(morts), morts[:5]))
    if perdus:
        print("\n!! %d article(s) PUBLIE(S) sortiraient du sommaire :" % len(perdus))
        for s in perdus:
            print("   - %s" % s)
        print("   Cause habituelle : leur pilier est encore en brouillon.")
        if not args.force:
            print("\nRien ecrit. Publier les piliers manquants, ou relancer avec --force.")
            return

    if not args.apply:
        print("\n(dry-run — relancer avec --apply)")
        return

    sh._req("PUT", "/pages/%s.json" % page["id"],
            {"page": {"id": page["id"], "title": conf["titre"], "body_html": nouveau}})
    ctl = sh._req("GET", "/pages.json?handle=%s&limit=1" % conf["page"])["pages"][0]
    print("\nAPPLIQUE. Relecture : titre=%r | %d liens | %d octets"
          % (ctl["title"], len(liens(ctl["body_html"], args.blog)), len(ctl["body_html"])))


if __name__ == "__main__":
    main()
