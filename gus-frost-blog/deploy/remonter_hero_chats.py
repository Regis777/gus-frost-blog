#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remonte la figure de l'image a la une en TETE du corps des articles.

Contexte : le 06/09/2026, la banniere du theme a ete retiree du gabarit
d'article (la meme photo s'affichait deux fois, cf. memoire hero-image-dupliquee).
Consequence pour le blog chats : sa photo est posee 400 a 860 mots plus bas dans
le corps, donc l'article ouvre sur un long pave de texte. On la remonte.

C'est un DEPLACEMENT, jamais une insertion : on retire le bloc existant et on
replace exactement la meme chaine en tete. La legende suit sa photo.

Piege qui a coute une fausse manoeuvre le 06/09/2026 : Shopify suffixe un UUID
au nom de fichier quand un fichier du meme nom existe deja, si bien qu'une meme
photo apparait en `hero-x.png` (corps, /files/) et
`hero-x_c0596f86-....png` (image a la une, /articles/). Comparer les noms bruts
fait croire a deux images differentes. D'ou `cle()` ci-dessous.

Usage :
  python deploy/remonter_hero_chats.py --blog chats                        # dry-run
  python deploy/remonter_hero_chats.py --blog chats --slug <slug> --apply  # palier
  python deploy/remonter_hero_chats.py --blog chats --backup sauv.json --apply
"""
import argparse, json, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify  # noqa: E402

OUVRE = re.compile(r"<article\b[^>]*>", re.I)
IMGSRC = re.compile(r'<img\b[^>]*?\bsrc=["\']([^"\']+)["\']', re.I)
FIGURE = re.compile(r"<figure\b[^>]*>.*?</figure>", re.S | re.I)
IMGTAG = re.compile(r"<img\b", re.I)
CAP = re.compile(r"<figcaption\b", re.I)
UUID = re.compile(r"_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?=\.)", re.I)
BLANCS = re.compile(r"\s+")

# Au-dela de ce nombre de caracteres depuis le debut du corps, la photo est
# consideree comme « pas en tete » et merite d'etre remontee.
SEUIL_TETE = 120


def cle(url):
    """Nom de fichier comparable : sans parametres, sans suffixe de taille, sans UUID."""
    if not url:
        return ""
    nom = url.split("?")[0].rsplit("/", 1)[-1]
    return UUID.sub("", re.sub(r"_\d+x\d*(?=\.)", "", nom)).lower()


def sans_blancs(s):
    return BLANCS.sub(" ", s).strip()


def retry(fn, essais=6):
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


def tous_les_articles(sh, blog_id):
    url = "%s/blogs/%s/articles.json?limit=250" % (sh.base, blog_id)
    arts = []
    while url:
        req = urllib.request.Request(url)
        req.add_header("X-Shopify-Access-Token", sh.token)
        with urllib.request.urlopen(req) as resp:
            arts += json.loads(resp.read().decode("utf-8"))["articles"]
            lien = resp.headers.get("Link", "") or ""
        m = re.search(r'<([^>]+)>;\s*rel="next"', lien)
        url = m.group(1) if m else None
    attendu = sh._req("GET", "/blogs/%s/articles/count.json" % blog_id)["count"]
    if len(arts) != attendu:
        sys.exit("REFUS : %d articles pour %d annonces — pagination incomplete."
                 % (len(arts), attendu))
    return arts


def examiner(art):
    """-> (nouveau_corps, None) si deplacable, sinon (None, raison ou None)."""
    corps = art.get("body_html") or ""
    une = cle((art.get("image") or {}).get("src", ""))
    if not une:
        return None, "pas d'image a la une"

    mimg = next((m for m in IMGSRC.finditer(corps) if cle(m.group(1)) == une), None)
    if not mimg:
        return None, "photo a la une absente du corps"

    ouv = OUVRE.match(corps.lstrip())
    if not ouv:
        return None, "le corps ne commence pas par <article>"
    debut = len(corps) - len(corps.lstrip())
    apres_ouverture = debut + ouv.end()

    # Le bloc a deplacer : la <figure> englobante si elle existe, sinon l'<img>.
    fig = next((f for f in FIGURE.finditer(corps)
                if f.start() < mimg.start() < f.end()), None)
    if fig:
        i, j = fig.start(), fig.end()
    else:
        i, j = mimg.start(), corps.index(">", mimg.start()) + 1
    bloc = corps[i:j]

    if i - apres_ouverture <= SEUIL_TETE:
        return None, None                        # deja en tete : rien a faire

    # On absorbe les blancs autour pour ne pas laisser de trou.
    g = i
    while g > apres_ouverture and corps[g - 1] in " \t\r\n":
        g -= 1
    d = j
    while d < len(corps) and corps[d] in " \t\r\n":
        d += 1

    reste = corps[:g] + "\n\n" + corps[d:]
    neuf = (reste[:apres_ouverture] + "\n" + bloc + "\n" + reste[apres_ouverture:])

    # Garde-fous : rien d'autre que ce bloc n'a bouge.
    if IMGTAG.findall(neuf) != IMGTAG.findall(corps):
        return None, "le nombre d'images changerait"
    if len(CAP.findall(neuf)) != len(CAP.findall(corps)):
        return None, "le nombre de legendes changerait"
    if neuf.count(bloc) != 1:
        return None, "le bloc apparaitrait %d fois" % neuf.count(bloc)
    if sans_blancs(neuf.replace(bloc, "", 1)) != sans_blancs(corps.replace(bloc, "", 1)):
        return None, "le corps differerait ailleurs que sur ce bloc"
    if not neuf.lstrip().lower().startswith("<article"):
        return None, "le corps ne commencerait plus par <article>"
    return neuf, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blog", required=True, choices=("chiens", "chats"))
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup", help="fichier JSON ou sauvegarder les corps avant")
    ap.add_argument("--slug", help="ne traiter que cet article (palier de test)")
    ap.add_argument("--brouillons", action="store_true")
    args = ap.parse_args()

    sh = Shopify(load_env())
    blog = sh.find_blog_id(args.blog)
    arts = tous_les_articles(sh, blog)
    if args.slug:
        arts = [a for a in arts if a["handle"] == args.slug] or sys.exit(
            "slug introuvable : %s" % args.slug)

    cibles, refus, brouillons = [], [], 0
    for a in arts:
        neuf, raison = examiner(a)
        if raison:
            refus.append((a["handle"], raison))
            continue
        if neuf is None:
            continue
        if a.get("published_at") is None and not args.brouillons:
            brouillons += 1
            continue
        cibles.append((a, neuf))

    print("=" * 74)
    print("blog %-7s : %d articles | photo a remonter en tete : %d"
          % (args.blog, len(arts), len(cibles)))
    if brouillons:
        print("   (%d brouillon(s) concerne(s), ignore(s) — --brouillons pour les inclure)"
              % brouillons)
    for a, _n in cibles[:4]:
        print("   ex. /blogs/%s/%s" % (args.blog, a["handle"]))
    if refus:
        print("\nNON TRAITES (%d) :" % len(refus))
        for s, why in refus[:20]:
            print("   ! %-45s %s" % (s, why))

    if not args.apply:
        print("\nDRY-RUN : rien pousse. Relancer avec --apply.")
        return
    if not cibles:
        print("\nRien a faire.")
        return

    if args.backup:
        json.dump({a["handle"]: {"id": a["id"], "body_html": a["body_html"]}
                   for a, _n in cibles},
                  open(args.backup, "w", encoding="utf-8"), ensure_ascii=False)
        print("\nSauvegarde : %s (%d articles)" % (args.backup, len(cibles)))

    pousses = 0
    for a, neuf in cibles:
        retry(lambda: sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog, a["id"]),
                              {"article": {"id": a["id"], "body_html": neuf}}))
        pousses += 1
        if pousses % 25 == 0:
            print("  ... %d pousses" % pousses)
    print("\n%d corps mis a jour sur le blog %s." % (pousses, args.blog))


if __name__ == "__main__":
    main()
