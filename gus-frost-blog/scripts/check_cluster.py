#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôle qualité d'un cluster d'articles (gabarit « standard C5 »), réutilisable
pour C6 et suivants. Stdlib uniquement, aucune écriture, aucun appel réseau.

Vérifie, par article :
  STRUCTURE  1 seul <article class="gf-article"> … </article>.
  FAQ        1 <h2 id="faq">…</h2> + 1 <div class="gf-faq"> avec N questions (h3), N attendu.
  CTA        1 <div class="gf-cta"> + 1 <span class="gf-cta-call"> + 1 lien vers la
             collection du blog (chiens -> /collections/stress, chats -> /collections/chat),
             et AUCUN lien /products/ dans le CTA.
  ORDRE      FAQ avant CTA ; le CTA est le dernier bloc avant </article>.
  IMAGES     chaque <img> a un alt non vide ; au moins une image hero-.
  MAILLAGE   liens internes en /blogs/<blog>/<slug> pointant vers un slug du manifest ;
             signale les PLACEHOLDER_ restants (toléré avant la passe de maillage).
  TYPO FR    espace insécable (U+00A0/U+202F) avant ; : ! ? » et après « (signale les
             espaces normales fautives).
  DIVERS     signale un <style> résiduel et tout JSON-LD/FAQPage (hors gabarit C5).

Usage :
  python scripts/check_cluster.py --dir articles/cluster-6-xxx
  python scripts/check_cluster.py --dir articles/cluster-5-repas-gamelle --faq 5 --blog chiens
  python scripts/check_cluster.py --dir articles/cluster-10-cohabitation-chat --faq 5 --blog chats
  python scripts/check_cluster.py --dir <dossier> --pre-maillage   # tolère PLACEHOLDER_ + noms d'images nus
Codes de sortie : 0 = aucun ERROR, 1 = au moins un ERROR.
"""
import argparse
import csv
import os
import re
import sys

try:                                    # sortie UTF-8 même sur console Windows cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import blog_conf                                        # noqa: E402

DOUBLE_PUNCT = ";:!?»"


def manifest_slugs(p):
    if not os.path.exists(p):
        return set()
    with open(p, encoding="utf-8-sig", newline="") as f:
        return {r["slug"] for r in csv.DictReader(f)}


def strip_tags(html):
    return re.sub(r"<[^>]+>", "", html)


def check_file(path, slugs, blog, faq_expected, pre_maillage, collection="stress"):
    html = open(path, encoding="utf-8").read()
    E, W = [], []            # errors, warnings

    # STRUCTURE
    if html.count("<article") != 1 or html.count("</article>") != 1:
        E.append("structure: attendu 1 <article> et 1 </article> (trouvé %d/%d)"
                 % (html.count("<article"), html.count("</article>")))

    # FAQ
    n_faq_div = html.count('class="gf-faq"')
    n_faq_head = len(re.findall(r"<h2[^>]*>\s*Questions fréquentes", html))
    n_faq_id = len(re.findall(r'<h2[^>]*id="faq"', html))
    faq_block = re.search(r'<div class="gf-faq">(.*?)</div>', html, re.S)
    n_q = faq_block.group(1).count("<h3") if faq_block else 0
    if n_faq_div != 1 or n_faq_head != 1:
        E.append("FAQ: attendu 1 <h2>Questions fréquentes</h2> + 1 div.gf-faq (trouvé %d titre / %d div)"
                 % (n_faq_head, n_faq_div))
    elif n_faq_id != 1:
        W.append('FAQ: <h2> sans id="faq" (ancre) — présent sur le pilier C5, absent des satellites')
    if faq_expected and n_q != faq_expected:
        E.append("FAQ: %d questions (h3), attendu %d" % (n_q, faq_expected))

    # CTA
    n_cta = html.count('class="gf-cta"')
    n_call = html.count('class="gf-cta-call"')
    cta_block = re.search(r'<div class="gf-cta">(.*?)</div>', html, re.S)
    inner = cta_block.group(1) if cta_block else ""
    n_coll = inner.count("/collections/%s" % collection)
    if n_cta != 1 or n_call != 1:
        E.append("CTA: attendu 1 div.gf-cta + 1 span.gf-cta-call (trouvé %d/%d)" % (n_cta, n_call))
    if n_coll != 1:
        E.append("CTA: lien /collections/%s attendu 1 fois dans le bloc (trouvé %d)"
                 % (collection, n_coll))
    if "/products/" in inner:
        E.append("CTA: contient un lien /products/ (le standard pointe vers /collections/%s)"
                 % collection)

    # ORDRE : FAQ avant CTA ; CTA dernier bloc avant </article>
    if faq_block and cta_block:
        if html.find('class="gf-faq"') > html.find('class="gf-cta"'):
            E.append("ordre: la FAQ doit précéder le CTA")
        after_cta = html[html.rfind('class="gf-cta"'):]
        if re.search(r'<div class="gf-(conseil|cas|recette|etapes)', after_cta):
            W.append("ordre: un encadré apparaît après le CTA (le CTA devrait clore l'article)")

    # IMAGES
    imgs = re.findall(r"<img\b[^>]*>", html)
    for tag in imgs:
        alt = re.search(r'\balt="([^"]*)"', tag)
        if not alt or not alt.group(1).strip():
            E.append("image sans alt: %s" % tag[:70])
    if not any('src="hero-' in t or "/hero-" in t for t in imgs):
        W.append("aucune image hero- détectée")

    # MAILLAGE
    ph = len(re.findall(r"PLACEHOLDER_", html))
    if ph and not pre_maillage:
        E.append("maillage: %d PLACEHOLDER_ non résolu(s)" % ph)
    elif ph:
        W.append("maillage: %d PLACEHOLDER_ (toléré en pré-maillage)" % ph)
    for tgt in re.findall(r'href="/blogs/%s/([a-z0-9-]+)"' % re.escape(blog), html):
        if slugs and tgt not in slugs:
            E.append("maillage: cible inconnue au manifest -> %s" % tgt)

    # TYPO FR (sur le texte hors balises)
    text = strip_tags(html)
    bad_before = len(re.findall(r" [%s]" % re.escape(DOUBLE_PUNCT), text))
    bad_after = len(re.findall(r"« ", text))
    if bad_before or bad_after:
        W.append("typo FR: %d espace(s) normale(s) avant ; : ! ? » et %d après « "
                 "(attendu insécable U+00A0/U+202F)" % (bad_before, bad_after))

    # DIVERS
    if "<style" in html.lower():
        W.append("bloc <style> résiduel (le corps s'appuie sur theme/gf-article.css)")
    if "application/ld+json" in html or "FAQPage" in html:
        W.append("JSON-LD/FAQPage présent (hors gabarit C5 : balisage géré au thème)")

    return E, W, {"faq_q": n_q, "imgs": len(imgs), "placeholders": ph}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="dossier des {slug}.html à contrôler")
    ap.add_argument("--blog", default="chiens")
    ap.add_argument("--faq", type=int, default=5, help="nb de questions FAQ attendu (0 = ne pas vérifier)")
    ap.add_argument("--pre-maillage", action="store_true",
                    help="tolère les PLACEHOLDER_ restants (avant résolution du maillage)")
    args = ap.parse_args()

    d = args.dir if os.path.isabs(args.dir) else os.path.join(ROOT, args.dir)
    files = sorted(f for f in os.listdir(d) if f.endswith(".html"))
    if not files:
        sys.exit("Aucun .html dans %s" % d)
    conf = blog_conf(args.blog)
    slugs = manifest_slugs(conf["manifest_path"])

    print("=" * 74)
    print("Contrôle cluster : %s  (%d fichiers) | blog=%s | CTA=/collections/%s | FAQ attendue=%s"
          % (args.dir, len(files), conf["handle"], conf["collection"], args.faq or "off"))
    print("=" * 74)
    n_err = n_warn = n_ok = 0
    for f in files:
        E, W, info = check_file(os.path.join(d, f), slugs, conf["handle"], args.faq,
                                args.pre_maillage, conf["collection"])
        tag = "FAIL" if E else ("WARN" if W else " OK ")
        if E: n_err += 1
        elif W: n_warn += 1
        else: n_ok += 1
        print("\n[%s] %-34s faq=%d imgs=%d ph=%d"
              % (tag, f.replace(".html", ""), info["faq_q"], info["imgs"], info["placeholders"]))
        for e in E:
            print("      ✗ " + e)
        for w in W:
            print("      · " + w)

    print("\n" + "=" * 74)
    print("Bilan : %d OK | %d WARN | %d FAIL  (sur %d)" % (n_ok, n_warn, n_err, len(files)))
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
