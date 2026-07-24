#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pousse le récap de commissions du mois vers Klaviyo, un ÉVÉNEMENT par ambassadeur.

Chaîne : calcul_commissions.py -> rapports/commissions_AAAA-MM.csv -> CE script
-> événement Klaviyo « Récap commission ambassadeur » (avec les chiffres en
propriétés) -> un FLOW Klaviyo déclenché par cette métrique envoie l'e-mail
personnalisé (voir affiliation/email_recap_klaviyo.html + README).

Côté SERVEUR (clé privée pk_...), contrairement au Carnet qui utilise l'API
client (clé publique, navigateur). La clé se met dans .env : KLAVIYO_PRIVATE_KEY.

stdlib uniquement (urllib).

Usage :
  python affiliation/push_commissions_klaviyo.py --dry-run              # mois précédent, aperçu sans envoi
  python affiliation/push_commissions_klaviyo.py --mois 2026-07 --dry-run
  python affiliation/push_commissions_klaviyo.py --mois 2026-07         # envoi réel des événements
"""
import argparse
import csv
import datetime
import json
import os
import sys
import time
import urllib.request
import urllib.error
from decimal import Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "affiliation"))
from publish import load_env  # noqa: E402
import moteur  # noqa: E402  (REPORTS_DIR)

KLAVIYO_URL = "https://a.klaviyo.com/api/events/"
REVISION = "2024-10-15"
METRIC = "Récap commission ambassadeur"
NBSP = " "
MOIS_FR = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet",
           "août", "septembre", "octobre", "novembre", "décembre"]


def mois_affichage(label):
    """'2026-07' -> 'juillet 2026'."""
    try:
        y, m = label.split("-")
        return "%s %s" % (MOIS_FR[int(m)], y)
    except Exception:
        return label


def fr_montant(v):
    """'48.60' -> '48,60 €' (virgule décimale + espace insécable avant €)."""
    d = Decimal(str(v or "0")).quantize(Decimal("0.01"))
    return ("%.2f" % d).replace(".", ",") + NBSP + "€"


def prev_month_label(today):
    first = today.replace(day=1)
    prev = (first - datetime.timedelta(days=1))
    return "%04d-%02d" % (prev.year, prev.month)


def read_report(label):
    path = os.path.join(moteur.REPORTS_DIR, "commissions_%s.csv" % label)
    if not os.path.exists(path):
        sys.exit("Rapport introuvable : %s\nLance d'abord : "
                 "python affiliation/calcul_commissions.py --mois %s" % (path, label))
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        ca_col = next((c for c in reader.fieldnames if c.startswith("ca_")), None)
    return rows, ca_col, path


def build_payload(row, ca_col, label, metric):
    taux_pct = int(round(float(row.get("taux", "0") or 0) * 100))
    props = {
        "code": row.get("code", ""),
        "mois": label,
        "mois_affichage": mois_affichage(label),
        "nb_commandes": int(row.get("nb_commandes", "0") or 0),
        "ca": float(Decimal(str(row.get(ca_col, "0") or "0"))),
        "ca_affichage": fr_montant(row.get(ca_col, "0")),
        "taux_affichage": "%d%s%%" % (taux_pct, NBSP),
        "commission": float(Decimal(str(row.get("commission_eur", "0") or "0"))),
        "commission_affichage": fr_montant(row.get("commission_eur", "0")),
    }
    return {"data": {"type": "event", "attributes": {
        "properties": props,
        "value": props["commission"],
        "metric": {"data": {"type": "metric", "attributes": {"name": metric}}},
        "profile": {"data": {"type": "profile", "attributes": {
            "email": (row.get("email") or "").strip(),
            "first_name": row.get("prenom", ""),
            "last_name": row.get("nom", ""),
        }}},
    }}}


def post_event(key, payload):
    req = urllib.request.Request(KLAVIYO_URL, data=json.dumps(payload).encode("utf-8"),
                                 method="POST")
    req.add_header("Authorization", "Klaviyo-API-Key %s" % key)
    req.add_header("revision", REVISION)
    req.add_header("content-type", "application/json")
    req.add_header("accept", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise SystemExit("Klaviyo HTTP %s sur /api/events/\n%s" % (e.code, detail))


def main():
    ap = argparse.ArgumentParser(description="Envoi des récaps de commissions vers Klaviyo.")
    ap.add_argument("--mois", help="AAAA-MM (défaut : mois précédent)")
    ap.add_argument("--metric", default=METRIC, help="nom de la métrique Klaviyo.")
    ap.add_argument("--dry-run", action="store_true", help="aperçu sans envoi (clé non requise).")
    args = ap.parse_args()

    label = args.mois or prev_month_label(datetime.date.today())
    rows, ca_col, path = read_report(label)
    if not rows:
        print("Rapport %s vide : aucun ambassadeur rémunéré ce mois-ci. Rien à envoyer." % label)
        return

    print("Récap Klaviyo — mois %s (%s)" % (label, mois_affichage(label)))
    print("Source : %s" % os.path.relpath(path, ROOT))
    print("Métrique : %s | base CA : %s" % (args.metric, ca_col))
    print("Mode : %s" % ("DRY-RUN (aucun envoi)" if args.dry_run else "ENVOI RÉEL"))
    print("=" * 74)

    key = None
    if not args.dry_run:
        env = load_env()
        key = (env.get("KLAVIYO_PRIVATE_KEY") or os.environ.get("KLAVIYO_PRIVATE_KEY") or "").strip()
        if not key:
            sys.exit("KLAVIYO_PRIVATE_KEY manquante dans .env (clé privée pk_...). "
                     "Ajoute-la ou relance avec --dry-run.")
        if not key.startswith("pk_"):
            print("Avertissement : une clé privée Klaviyo commence normalement par 'pk_'.")

    sent = skipped = 0
    for row in rows:
        email = (row.get("email") or "").strip()
        who = moteur.full_name(row) or row.get("code", "")
        if not email:
            skipped += 1
            print("- %-16s  PAS D'E-MAIL -> ignoré (%s)" % (row.get("code", ""), who))
            continue
        payload = build_payload(row, ca_col, label, args.metric)
        p = payload["data"]["attributes"]["properties"]
        line = ("- %-16s %-22s %s cmd | CA %s | commission %s -> %s"
                % (row.get("code", ""), who[:22], p["nb_commandes"],
                   p["ca_affichage"], p["commission_affichage"], email))
        if args.dry_run:
            print(line + "   [aperçu]")
            sent += 1
            continue
        status = post_event(key, payload)
        print(line + ("   [OK %s]" % status))
        sent += 1
        time.sleep(0.2)  # courtoisie API

    print("=" * 74)
    verbe = "à envoyer" if args.dry_run else "envoyés"
    print("Événements %s : %d | ignorés (sans e-mail) : %d" % (verbe, sent, skipped))
    if args.dry_run:
        print("Dry-run terminé. Relance SANS --dry-run pour envoyer (clé Klaviyo requise).")
    else:
        print("Le FLOW Klaviyo déclenché par « %s » enverra l'e-mail à chaque ambassadeur."
              % args.metric)


if __name__ == "__main__":
    main()
