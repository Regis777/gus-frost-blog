#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calcule les commissions des ambassadeurs pour un mois donné.

ATTRIBUTION : une commande est attribuée à un ambassadeur si elle porte SON
code promo (champ discount_codes de la commande). Une commande utilisant
plusieurs codes est attribuée au premier code ambassadeur reconnu.

BASE DE COMMISSION (option --base) :
  - net (défaut) : sous-total produits APRÈS remise ambassadeur, hors livraison/taxes.
                   -> tu paies la commission sur ce que le client a réellement payé.
  - brut         : total des produits AVANT remise.

Sont exclues : les commandes annulées (cancelled_at) et les commandes de test.
Note : les remboursements partiels sont pris en compte via current_subtotal_price
(base 'net'). Les commandes intégralement remboursées mais non annulées restent
comptées — à vérifier à la main si tu as beaucoup de retours.

Sortie : affiliation/rapports/commissions_<AAAA-MM>.csv + récap console.
Option --details : écrit aussi affiliation/rapports/detail_<AAAA-MM>.csv (commande par commande).

Usage :
  python affiliation/calcul_commissions.py                    # mois précédent (défaut)
  python affiliation/calcul_commissions.py --mois 2026-07
  python affiliation/calcul_commissions.py --mois 2026-07 --base brut --details
"""
import argparse
import calendar
import csv
import datetime
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "affiliation"))
import moteur  # noqa: E402

CENT = Decimal("0.01")


def money(v):
    try:
        return Decimal(str(v if v not in (None, "") else "0"))
    except Exception:
        return Decimal("0")


def month_bounds(mois):
    """Bornes ISO [1er 00:00:00 ; dernier jour 23:59:59] du mois donné."""
    start = datetime.datetime(mois.year, mois.month, 1, 0, 0, 0)
    last = calendar.monthrange(mois.year, mois.month)[1]
    end = datetime.datetime(mois.year, mois.month, last, 23, 59, 59)
    return start.isoformat(), end.isoformat()


def prev_month(today):
    first = today.replace(day=1)
    return (first - datetime.timedelta(days=1)).replace(day=1)


def main():
    ap = argparse.ArgumentParser(description="Commissions ambassadeurs (mensuel).")
    ap.add_argument("--mois", help="AAAA-MM (défaut : mois précédent)")
    ap.add_argument("--base", choices=["net", "brut"], default="net",
                    help="assiette de la commission (défaut : net).")
    ap.add_argument("--details", action="store_true",
                    help="écrit aussi le détail commande par commande.")
    args = ap.parse_args()

    if args.mois:
        try:
            mois = datetime.datetime.strptime(args.mois, "%Y-%m")
        except ValueError:
            sys.exit("Format --mois attendu : AAAA-MM (ex. 2026-07)")
    else:
        pm = prev_month(datetime.date.today())
        mois = datetime.datetime(pm.year, pm.month, 1)

    label = mois.strftime("%Y-%m")
    cmin, cmax = month_bounds(mois)

    registry = moteur.load_registry()
    code_map = {r["code"]: r for r in registry}

    print("Commissions — mois %s | base %s" % (label, args.base))
    print("Codes ambassadeurs au registre : %d" % len(registry))
    print("Récupération des commandes (%s -> %s) ..." % (cmin, cmax))
    sh = moteur.client()
    orders = moteur.fetch_orders(sh, cmin, cmax)
    print("Commandes récupérées : %d" % len(orders))
    print("=" * 80)

    agg = {r["code"]: {"row": r, "n": 0, "base": Decimal("0")} for r in registry}
    details, skipped_cancel, skipped_test, no_code = [], 0, 0, 0

    for o in orders:
        if o.get("cancelled_at"):
            skipped_cancel += 1
            continue
        if o.get("test"):
            skipped_test += 1
            continue
        codes = [(dc.get("code") or "").upper() for dc in (o.get("discount_codes") or [])]
        matched = next((c for c in codes if c in code_map), None)
        if not matched:
            no_code += 1
            continue
        if args.base == "brut":
            base = money(o.get("total_line_items_price"))
        else:
            base = money(o.get("current_subtotal_price") or o.get("subtotal_price"))
        agg[matched]["n"] += 1
        agg[matched]["base"] += base
        if args.details:
            details.append((matched, o.get("name"), (o.get("created_at") or "")[:10],
                            str(base), o.get("currency", "")))

    # --- construction des lignes du rapport ---
    ca_col = "ca_%s_eur" % args.base
    lignes, total_base, total_comm = [], Decimal("0"), Decimal("0")
    for code, d in agg.items():
        if d["n"] == 0:
            continue
        r = d["row"]
        comm = (d["base"] * Decimal(str(r["taux"]))).quantize(CENT, ROUND_HALF_UP)
        total_base += d["base"]
        total_comm += comm
        lignes.append({
            "code": code,
            "prenom": r.get("prenom", ""),
            "nom": r.get("nom", ""),
            "email": r.get("email", ""),
            "nb_commandes": d["n"],
            ca_col: str(d["base"].quantize(CENT)),
            "taux": str(r["taux"]),
            "commission_eur": str(comm),
        })
    lignes.sort(key=lambda x: Decimal(x["commission_eur"]), reverse=True)

    os.makedirs(moteur.REPORTS_DIR, exist_ok=True)
    out = os.path.join(moteur.REPORTS_DIR, "commissions_%s.csv" % label)
    if lignes:
        with open(out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
            w.writeheader()
            w.writerows(lignes)

    if args.details and details:
        dout = os.path.join(moteur.REPORTS_DIR, "detail_%s.csv" % label)
        with open(dout, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["code", "commande", "date", "base_%s" % args.base, "devise"])
            w.writerows(details)

    # --- récap console ---
    print("%-16s %-22s %5s %12s %6s %12s"
          % ("CODE", "AMBASSADEUR", "CMD", "CA", "TAUX", "COMMISSION"))
    print("-" * 80)
    for l in lignes:
        who = (l["prenom"] + " " + l["nom"]).strip()
        print("%-16s %-22s %5d %12s %5d%% %12s"
              % (l["code"], who[:22], l["nb_commandes"], l[ca_col],
                 int(round(float(l["taux"]) * 100)), l["commission_eur"]))
    print("-" * 80)
    print("TOTAL : %d ambassadeur(s) rémunéré(s) | CA %s | commissions %s"
          % (len(lignes), str(total_base.quantize(CENT)), str(total_comm.quantize(CENT))))
    print("Commandes sans code ambassadeur : %d | annulées : %d | test : %d"
          % (no_code, skipped_cancel, skipped_test))
    if lignes:
        print("Rapport écrit : %s" % os.path.relpath(out, ROOT))
        if args.details:
            print("Détail écrit  : %s" % os.path.relpath(
                os.path.join(moteur.REPORTS_DIR, "detail_%s.csv" % label), ROOT))
    else:
        print("Aucune vente attribuée ce mois-ci — aucun rapport écrit.")


if __name__ == "__main__":
    main()
