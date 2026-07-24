#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crée / synchronise les codes promo des ambassadeurs sur Shopify, à partir de
affiliation/ambassadeurs.csv.

- Idempotent : un code déjà présent n'est PAS recréé (contrôle via lookup Shopify).
- Seules les lignes statut=actif sont traitées (les 'exemple', 'en_attente',
  'inactif' sont ignorées).
- Le script ne modifie jamais un code existant : il signale seulement si la
  remise dans Shopify diffère de celle du CSV.

Usage :
  python affiliation/creer_codes.py --dry-run   # montre ce qui serait créé (aucun appel réseau)
  python affiliation/creer_codes.py             # crée réellement les codes manquants
"""
import argparse
import datetime
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "affiliation"))
import moteur  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Création des codes promo ambassadeurs.")
    ap.add_argument("--dry-run", action="store_true",
                    help="aucun appel d'écriture : liste ce qui serait créé.")
    args = ap.parse_args()

    rows = [r for r in moteur.load_registry() if r["statut"] == "actif"]
    if not rows:
        print("Aucun ambassadeur 'actif' dans le registre. Rien à faire.")
        print("(Passe la colonne statut à 'actif' dans affiliation/ambassadeurs.csv.)")
        return

    print("Ambassadeurs actifs : %d" % len(rows))
    print("Mode : %s" % ("DRY-RUN (aucune écriture)" if args.dry_run else "CRÉATION RÉELLE"))
    print("=" * 68)

    sh = None if args.dry_run else moteur.client()
    starts_at = datetime.datetime.now().replace(microsecond=0).isoformat()
    created = existing = mismatch = 0

    for r in rows:
        code, remise = r["code"], r["remise_client"]
        who = moteur.full_name(r) or r.get("email") or code

        if args.dry_run:
            print("- %-16s  -%d %%   (%s)   -> serait créé si absent"
                  % (code, round(remise), who))
            continue

        dc = moteur.lookup_code(sh, code)
        if dc:
            existing += 1
            pr = moteur.get_price_rule(sh, dc.get("price_rule_id")) or {}
            val = abs(float(pr.get("value", "0") or 0))
            note = ""
            if round(val) != round(remise):
                mismatch += 1
                note = "   ATTENTION : remise Shopify %d %% != CSV %d %%" % (round(val), round(remise))
            print("- %-16s  existe déjà (price_rule=%s)%s"
                  % (code, dc.get("price_rule_id"), note))
        else:
            pr, dc = moteur.create_code(sh, code, remise, starts_at)
            created += 1
            print("- %-16s  CRÉÉ  -%d %%  (price_rule=%s)   (%s)"
                  % (code, round(remise), pr["id"], who))

    print("=" * 68)
    if args.dry_run:
        print("Dry-run terminé. Relance SANS --dry-run pour créer réellement les codes.")
    else:
        print("Créés : %d | déjà présents : %d | écarts de remise : %d"
              % (created, existing, mismatch))
        if mismatch:
            print("Un écart = la remise dans Shopify diffère du CSV. Le script ne touche "
                  "pas l'existant : corrige côté Shopify si nécessaire.")


if __name__ == "__main__":
    main()
