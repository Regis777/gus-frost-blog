#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archive locale, hors Shopify, du contenu integral d'un theme.

POURQUOI. Un theme supprime ne revient pas, et l'admin ne sait exporter qu'en
envoyant un ZIP par courriel. Avant tout menage de themes, ce script pose sur le
disque une copie fidele de ce qui va disparaitre. Il sert aussi a prendre un
instantane date du theme PUBLIE avant une migration.

CE QU'IL FAIT. Il liste les fichiers du theme, telecharge chacun (texte ou
binaire) et les ecrit en respectant l'arborescence d'origine
(assets/, sections/, snippets/, templates/, locales/, config/, layout/). Il
depose a cote un _MANIFESTE.json : id et role du theme, date, puis un couple
taille + md5 par fichier. Ces md5 rendent un diff ulterieur immediat, sans avoir
a retelecharger quoi que ce soit.

Lectures seules : rien n'est modifie cote Shopify.

PIEGE. L'API REST est limitee a 2 requetes/seconde et il y a une requete par
fichier : comptez ~4 min pour un theme Dawn (environ 375 fichiers). La pause de
0,55 s entre appels est la pour ca, ne pas la retirer.

Usage :
  python scripts/archiver_theme.py --dest "<dossier>" --theme <id> [--theme <id>...]
  python scripts/archiver_theme.py --dest "<dossier>" --tout

Le dossier retenu le 05/09/2026 :
  "C:/Users/regis/Google Drive/Gus et Frost/04_SHOPIFY-TECH/archives-themes"
"""
import argparse
import base64
import hashlib
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

PAUSE = 0.55  # limite REST : 2 requetes/seconde
INTERDITS = '<>:"/\\|?*'  # caracteres refuses par un nom de dossier Windows


def nom_de_dossier(theme):
    """Nom lisible et date : on retrouve d'un coup d'oeil ce qui a ete pris,
    dans quel role, et quand."""
    brut = "%s (%s, %s)" % (theme.get("name", "sans-nom"),
                            theme.get("role", "?"),
                            time.strftime("%Y-%m-%d"))
    return "".join(" " if c in INTERDITS else c for c in brut).strip()


def lister_fichiers(sh, theme_id):
    data = sh._req("GET", "/themes/%s/assets.json" % theme_id)
    return [a["key"] for a in data.get("assets", [])]


def contenu(sh, theme_id, cle):
    """Rend les octets du fichier. Shopify sert le texte dans `value` et le
    binaire (images, polices) en base64 dans `attachment` : les deux cas
    comptent, sans quoi l'archive perd silencieusement les images du theme."""
    q = urllib.parse.urlencode({"asset[key]": cle})
    actif = sh._req("GET", "/themes/%s/assets.json?%s" % (theme_id, q)).get("asset", {})
    if actif.get("value") is not None:
        return actif["value"].encode("utf-8")
    if actif.get("attachment"):
        return base64.b64decode(actif["attachment"])
    return None


def archiver(sh, theme, dest, nom=None):
    theme_id = theme["id"]
    racine = os.path.join(dest, nom or nom_de_dossier(theme))
    os.makedirs(racine, exist_ok=True)

    cles = lister_fichiers(sh, theme_id)
    print("%s (%s) : %d fichiers" % (theme.get("name"), theme_id, len(cles)))

    fichiers, vides = [], []
    for i, cle in enumerate(cles, 1):
        octets = contenu(sh, theme_id, cle)
        if octets is None:
            vides.append(cle)
            continue
        chemin = os.path.join(racine, *cle.split("/"))
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with open(chemin, "wb") as f:
            f.write(octets)
        fichiers.append({"fichier": cle, "octets": len(octets),
                         "md5": hashlib.md5(octets).hexdigest()})
        if i % 50 == 0:
            print("   %d/%d" % (i, len(cles)))
        time.sleep(PAUSE)

    manifeste = {
        "theme_id": theme_id,
        "nom": theme.get("name"),
        "role": theme.get("role"),
        "archive_le": time.strftime("%Y-%m-%d %H:%M"),
        "fichiers": fichiers,
    }
    with open(os.path.join(racine, "_MANIFESTE.json"), "w", encoding="utf-8") as f:
        json.dump(manifeste, f, ensure_ascii=False, indent=2)

    # Un fichier vide n'est pas une erreur fatale, mais il doit se voir : c'est
    # le seul cas ou l'archive est incomplete sans que le compte final le dise.
    for cle in vides:
        print("   ! sans contenu, non ecrit : %s" % cle)
    total = sum(f["octets"] for f in fichiers)
    print("   OK %d fichiers, %.1f Ko -> %s\n" % (len(fichiers), total / 1024.0, racine))
    return len(fichiers)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", required=True, help="dossier ou deposer les archives")
    ap.add_argument("--theme", action="append", default=[],
                    help="id du theme (repetable)")
    ap.add_argument("--tout", action="store_true", help="tous les themes du store")
    ap.add_argument("--nom", help="nom de dossier impose (un seul theme)")
    args = ap.parse_args()

    if not args.theme and not args.tout:
        sys.exit("Rien a faire : donne --theme <id> ou --tout.")
    if args.nom and len(args.theme) != 1:
        sys.exit("--nom ne vaut que pour un seul --theme.")

    sh = Shopify(load_env())
    themes = {str(t["id"]): t for t in sh._req("GET", "/themes.json").get("themes", [])}

    if args.tout:
        cibles = list(themes.values())
    else:
        cibles = []
        for tid in args.theme:
            if str(tid) not in themes:
                sys.exit("Theme %s introuvable. Presents : %s"
                         % (tid, ", ".join("%s (%s)" % (k, v.get("name"))
                                           for k, v in themes.items())))
            cibles.append(themes[str(tid)])

    os.makedirs(args.dest, exist_ok=True)
    total = sum(archiver(sh, t, args.dest, args.nom) for t in cibles)
    print("--- %d theme(s), %d fichiers archives ---" % (len(cibles), total))


if __name__ == "__main__":
    main()
