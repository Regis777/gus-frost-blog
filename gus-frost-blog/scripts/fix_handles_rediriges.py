#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reecrit les liens internes qui pointent vers un handle redirige.

Douze articles chiot ont ete renommes ; les anciens handles survivent comme
brouillons et comme redirections 301. Les corps d'articles, eux, pointent encore
vers les anciens : chaque lien coute a Google un aller-retour inutile, et c'est
ce qui alimente le motif « Page avec redirection » de la Search Console.

Corrige la SOURCE (articles/), pas la copie en ligne : une edition faite
uniquement en ligne serait perdue au prochain rebake.

  python scripts/fix_handles_rediriges.py            # dry-run
  python scripts/fix_handles_rediriges.py --apply
"""
import argparse, collections, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ancien handle -> nouveau, tels que definis par les redirections Shopify
MAP = {
    "chiot-guide-premiers-mois": "elever-un-chiot",
    "preparer-arrivee-chiot-maison": "preparer-arrivee-chiot",
    "premiers-jours-chiot-adaptation": "premiers-jours-chiot",
    "premieres-nuits-chiot-sommeil": "premieres-nuits-chiot",
    "chiot-accidents-proprete-solutions": "chiot-accidents-pipi-maison",
    "temps-proprete-chiot-delais": "combien-temps-chiot-propre",
    "socialiser-chiot-fenetre-rencontres": "socialiser-son-chiot",
    "mordillements-chiot-canaliser": "mordillements-dentition-chiot",
    "dentition-chiot-etapes-solutions": "dentition-chiot-etapes",
    "besoin-mastication-chiot": "chiot-besoin-macher",
    "manipulation-soins-chiot-habituation": "habituer-chiot-manipulation",
    "gerer-energie-chiot-jeu-repos": "autocontrole-gerer-excitation-chiot",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    racine = os.path.join(ROOT, "articles")
    total = collections.Counter()
    touches = 0

    for dossier, _, fichiers in os.walk(racine):
        for nom in sorted(fichiers):
            if not nom.endswith(".html"):
                continue
            chemin = os.path.join(dossier, nom)
            s = io.open(chemin, encoding="utf-8", newline="").read()
            avant = s
            for vieux, neuf in MAP.items():
                # uniquement dans une URL d'article, jamais dans du texte
                motif = re.compile(r'(/blogs/chiens/)%s(?=["\'/#?])' % re.escape(vieux))
                s, n = motif.subn(r"\g<1>" + neuf, s)
                if n:
                    total[vieux] += n
            if s != avant:
                touches += 1
                rel = os.path.relpath(chemin, ROOT)
                nb = sum(1 for _ in re.finditer(r"/blogs/chiens/", avant)) 
                print("  %-62s %d lien(s) reecrit(s)"
                      % (rel, sum(v for v in [1]) if False else
                         sum(len(re.findall(r'/blogs/chiens/%s(?=["\'/#?])' % re.escape(v), avant))
                             for v in MAP)))
                if a.apply:
                    io.open(chemin, "w", encoding="utf-8", newline="").write(s)

    print("\n--- par handle ---")
    for vieux, neuf in sorted(MAP.items()):
        print("  %-38s -> %-36s %d" % (vieux, neuf, total[vieux]))
    print("\n%d fichier(s) concerne(s), %d lien(s) au total%s"
          % (touches, sum(total.values()), "" if a.apply else "  (DRY-RUN, rien ecrit)"))
    if a.apply:
        print("Sources corrigees. Il reste a redeployer ces articles pour que le")
        print("changement existe aussi en ligne.")


if __name__ == "__main__":
    main()
