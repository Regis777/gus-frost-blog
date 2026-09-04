#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repare une « Updated copy » produite par la mise a jour du theme.

CE QUE FAIT SHOPIFY. Le bouton « Mettre a jour » de l'admin fabrique une copie
en Dawn 16 et tente d'y fusionner nos personnalisations. Mesure du 01/09/2026 :
les fichiers qui nous appartiennent survivent, mais les MODELES JSON sont
abimes — product.monoproduit remis a zero (26 blocs perdus), et une section Dawn
par defaut (main-page / main-product + related-products) reinjectee en tete des
modeles custom.

CE QUE FAIT CE SCRIPT. Il recopie, depuis le theme PUBLIE vers la copie, les
fichiers dont Dawn n'a rien a dire : nos modeles de page et de produit, nos
sections et assets maison, les groupes de sections. Tout le reste de la copie
reste du Dawn 16 pur.

Il ne publie rien. Il affiche un bilan a controler en apercu.

Le theme publie sert de source, et nos modeles sont DECOUVERTS a l'execution :
rien a tenir a jour ici quand une fiche produit nait. Ce que le script ne
reconnait pas est affiche, pour qu'un oubli se voie.

Usage :
  python scripts/migrer_dawn16.py --copie <id> --dry-run
  python scripts/migrer_dawn16.py --copie <id> --apply
"""
import argparse
import json
import os
import sys
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from publish import load_env, Shopify  # noqa: E402

# Le theme publie est trouve a l'execution : le coder en dur le rendait faux
# des la premiere migration reussie.

# Nos modeles sont DECOUVERTS, pas listes a la main : un modele cree plus tard
# serait sinon oublie ici, et la fusion l'abimerait sans que personne le voie.
# Regle : un modele est a nous des qu'il pose une de nos sections. S'y ajoutent
# ceux qui n'utilisent que des sections Dawn mais portent nos choix de mise en
# page. Ce qui n'est couvert par aucune des deux regles est AFFICHE en fin de
# passage, pour qu'un oubli soit visible au lieu d'etre silencieux.
MODELES_TOUJOURS = [
    "templates/article.json",
    "templates/blog.json",
    "templates/index.json",
]

# Nos fichiers maison. La fusion les laisse intacts, mais on les recopie : c'est
# idempotent, et ca couvre le cas ou une version future les toucherait.
MAISON = [
    "assets/gf-article.css",
    "assets/gf-carnet-landing.css", "assets/gf-carnet.css", "assets/gf-carnet.js",
    "assets/gf-quiz-anxiete.css", "assets/gf-quiz-anxiete.js",
    "sections/gf-article-css.liquid",
    "sections/gf-blog-search.liquid",
    "sections/gf-carnet-landing.liquid", "sections/gf-carnet.liquid",
    "sections/gf-cookie-consent.liquid", "sections/gf-parrainage.liquid",
    "sections/gf-quiz-anxiete.liquid",
    "sections/avis-produit.liquid", "sections/monoproduit.liquid",
    "sections/rituel-du-calme.liquid", "sections/tapis-lechage.liquid",
    "sections/conversion-marquee.liquid", "sections/conversion-reviews.liquid",
    "sections/conversion-sticky-atc.liquid", "sections/conversion-trust.liquid",
    "snippets/gf-carnet-promo.liquid", "snippets/related-articles.liquid",
]

# Le bandeau cookies vit dans le groupe pied de page.
GROUPES = ["sections/footer-group.json"]

# Reglage supprime par Dawn 16 avec les comptes clients classiques : on ne le
# reinjecte pas en recopiant notre groupe d'en-tete.
HEADER_GROUPE = "sections/header-group.json"
REGLAGE_DISPARU = "enable_customer_avatar"


def get(sh, tid, cle):
    """L'API plafonne a 2 appels/seconde : on temporise et on reprend sur 429."""
    for essai in range(6):
        try:
            d = sh._req("GET", "/themes/%s/assets.json?asset[key]=%s"
                        % (tid, urllib.parse.quote(cle)))
            time.sleep(0.55)
            return d.get("asset", {}).get("value")
        except SystemExit as e:
            if "HTTP 404" in str(e):
                return None
            if "HTTP 429" in str(e):
                time.sleep(2 + essai)
                continue
            raise
    sys.exit("Abandon : 429 repete sur %s" % cle)


def put(sh, tid, cle, val):
    sh._req("PUT", "/themes/%s/assets.json" % tid, {"asset": {"key": cle, "value": val}})


def nos_types_de_sections():
    """Les types de section que nous fournissons, deduits de MAISON."""
    return {os.path.basename(c)[:-len(".liquid")]
            for c in MAISON if c.startswith("sections/")}


def decouvrir_modeles(sh, tid):
    """Rend (a_recopier, non_couverts). Un modele est a nous s'il pose une de
    nos sections ; article/blog/index le sont par nature."""
    nos_types = nos_types_de_sections()
    tous = sorted(a["key"] for a in sh._req("GET", "/themes/%s/assets.json" % tid)["assets"]
                  if a["key"].startswith("templates/") and a["key"].endswith(".json"))
    time.sleep(0.55)
    a_recopier, non_couverts = [], []
    for cle in tous:
        if cle in MODELES_TOUJOURS:
            a_recopier.append(cle)
            continue
        v = get(sh, tid, cle)
        try:
            d = json.loads(v) if v else {}
        except ValueError:
            non_couverts.append((cle, "illisible"))
            continue
        types = {s.get("type") for s in d.get("sections", {}).values()}
        a_nous = sorted(types & nos_types)
        if a_nous:
            a_recopier.append(cle)
        else:
            non_couverts.append((cle, ", ".join(sorted(t for t in types if t))[:58]))
    return a_recopier, non_couverts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--copie", required=True, help="id de la « Updated copy »")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    sh = Shopify(load_env())
    themes = {str(t["id"]): t for t in sh._req("GET", "/themes.json")["themes"]}
    publies = [t for t in themes.values() if t["role"] == "main"]
    if len(publies) != 1:
        sys.exit("REFUS : %d theme(s) publie(s), impossible de choisir la source." % len(publies))
    PUBLIE = publies[0]["id"]
    if str(PUBLIE) == args.copie:
        sys.exit("REFUS : la copie ne peut pas etre le theme publie.")
    if args.copie not in themes:
        sys.exit("Theme %s introuvable." % args.copie)
    cible = themes[args.copie]
    if cible["role"] != "unpublished":
        sys.exit("REFUS : %s n'est pas un brouillon (role=%s)." % (cible["name"], cible["role"]))
    print("Source  : %s (%s, publie)" % (themes[str(PUBLIE)]["name"], PUBLIE))
    print("Cible   : %s (%s, brouillon)\n" % (cible["name"], args.copie))

    MODELES, non_couverts = decouvrir_modeles(sh, PUBLIE)
    print("%d modele(s) reconnu(s) comme les notres :" % len(MODELES))
    for m in MODELES:
        print("   . %s" % m.replace("templates/", ""))
    if non_couverts:
        # Affiche des le dry-run : c'est ici qu'un modele oublie doit sauter aux yeux.
        print("\n%d modele(s) laisse(s) a Dawn 16, aucune de nos sections dedans." % len(non_couverts))
        print("A relire : si l'un d'eux est en realite a nous, il faut le proteger.")
        for cle, types in non_couverts:
            print("   . %-30s sections : %s" % (cle.replace("templates/", ""), types or "(aucune)"))
    print()

    ecrire, absents = {}, []
    for cle in MODELES + MAISON + GROUPES:
        src = get(sh, PUBLIE, cle)
        if src is None:
            absents.append(cle)
            continue
        if get(sh, args.copie, cle) != src:
            ecrire[cle] = src

    # en-tete : on recopie le notre, moins le reglage que Dawn 16 ne connait plus
    def sans_reglage_disparu(txt):
        d = json.loads(txt)
        for s in d.get("sections", {}).values():
            s.get("settings", {}).pop(REGLAGE_DISPARU, None)
        return d

    src = get(sh, PUBLIE, HEADER_GROUPE)
    cible_txt = get(sh, args.copie, HEADER_GROUPE)
    if src is not None and cible_txt is not None:
        # On compare les deux cotes DEBARRASSES du reglage : sinon le script se
        # croit du travail a faire a chaque passage sur une copie deja saine.
        a, b = sans_reglage_disparu(src), sans_reglage_disparu(cible_txt)
        if a != b:
            ecrire[HEADER_GROUPE] = json.dumps(a, ensure_ascii=False, indent=2)

    print("%d fichier(s) a recopier, %d introuvable(s) a la source" % (len(ecrire), len(absents)))
    for cle in sorted(ecrire):
        print("   ~ %s" % cle)
    for cle in absents:
        print("   ! absent du theme publie : %s" % cle)

    if args.dry_run:
        print("\nDRY-RUN : rien ecrit.")
        return

    print()
    for cle, val in ecrire.items():
        put(sh, args.copie, cle, val)
        for essai in range(4):
            relu = get(sh, args.copie, cle)
            ok = (json.loads(relu) == json.loads(val)) if cle.endswith(".json") else (relu == val)
            if ok:
                break
            time.sleep(1.5)
        print("   ecrit %-46s %s" % (cle, "OK" if ok else ">>> ECART <<<"))
        time.sleep(0.2)

    # ---- bilan a controler -------------------------------------------------
    # Controle exact plutot qu'heuristique : un modele est bon s'il est
    # identique a celui du theme publie. Deviner ce qui est « parasite » ne
    # marche pas — product.conversion porte legitimement un main-product.
    print("\n--- controles ---")
    for cle in MODELES:
        a, b = get(sh, PUBLIE, cle), get(sh, args.copie, cle)
        if b is None:
            print("   ! %-40s absent de la copie" % cle.replace("templates/", "")); continue
        ident = json.loads(a) == json.loads(b)
        d = json.loads(b)
        print("   %-40s %-4s ordre : %s"
              % (cle.replace("templates/", ""), "ok" if ident else "!!",
                 " > ".join(d.get("order", []))[:70]))
    print("\nApercu a controler : un article, les pages custom, chaque fiche produit,")
    print("puis publication seulement si tout est vert.")


if __name__ == "__main__":
    main()
