#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifie la regle des espaces insecables (U+00A0) dans les textes destines aux
visiteurs : avant : ; ! ? » et apres « .

Ne controle QUE les chaines reellement affichees, pour eviter le bruit :
  - .json    : toutes les valeurs de chaines
  - .liquid  : les "default" du schema (le reste est du code)
  - .js      : les litteraux contenant des accents (donc du francais)
Les entites HTML &nbsp; comptent comme des insecables (usage courant en .liquid/.js).

Usage :
  python scripts/check_insecables.py                    # fichiers du Carnet
  python scripts/check_insecables.py theme/mon.liquid   # fichiers precis
Sortie : code 1 s'il reste des violations (utilisable en garde-fou).
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NBSP = u" "

DEFAUT = [
    "theme/page.carnet-landing.json",
    "theme/page.carnet.json",
    "theme/gf-carnet-landing.liquid",
    "theme/gf-carnet.liquid",
    "theme/gf-carnet-promo.liquid",
    "theme/gf-carnet.js",
]

RX_JSON = re.compile(r'"[^"]*"\s*:\s*"([^"]*)"')
RX_DEFAUT = re.compile(r'"default"\s*:\s*"([^"]*)"')
# Litteral sur UNE ligne : sans cette contrainte, les apostrophes des commentaires
# francais (« l'app ») font matcher des pans entiers de code.
RX_JS = re.compile(r"'([^'\\\n]*(?:\\.[^'\\\n]*)*)'")
RX_COMMENTAIRE = re.compile(r"/\*.*?\*/|//[^\n]*", re.S)
RX_ACCENT = re.compile(u"[à-ÿ]")

# une espace ordinaire collee a un signe double, ou juste apres un guillemet ouvrant
RX_FAUTE = re.compile(u"\\S «|\\S [:;!?»]|« ")


def chaines(chemin):
    texte = io.open(chemin, encoding="utf-8").read()
    if chemin.endswith(".json"):
        return RX_JSON.findall(texte)
    if chemin.endswith(".liquid"):
        return RX_DEFAUT.findall(texte)
    if chemin.endswith(".js"):
        # Les commentaires ne sont pas affiches : on les retire avant analyse.
        code = RX_COMMENTAIRE.sub(" ", texte)
        return [s for s in RX_JS.findall(code) if RX_ACCENT.search(s)]
    return texte.split("\n")


def main():
    fichiers = sys.argv[1:] or DEFAUT
    total = 0
    for rel in fichiers:
        chemin = os.path.join(ROOT, rel)
        if not os.path.exists(chemin):
            print("  (absent) %s" % rel)
            continue
        for s in chaines(chemin):
            # &nbsp; est un insecable valide : on le neutralise avant analyse
            propre = s.replace("&nbsp;", NBSP)
            for m in RX_FAUTE.finditer(propre):
                total += 1
                extrait = propre[max(0, m.start() - 45):m.start() + 15]
                print("%-34s %s" % (rel, extrait.replace(NBSP, "_")))
    print("-" * 62)
    if total:
        print("%d violation(s) — insecable manquante (« _ » = insecable presente)." % total)
        return 1
    print("Aucune violation. Insecables conformes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
