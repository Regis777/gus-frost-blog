#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gus & Frost — moteur d'affiliation (briques communes).

Deux outils s'appuient dessus :
  - creer_codes.py        : crée / synchronise les codes promo des ambassadeurs
  - calcul_commissions.py : attribue les ventes par code et calcule les commissions

Principe : LE CODE PROMO EST LA CLÉ D'ATTRIBUTION. Shopify compte nativement
les commandes portant un code promo — zéro cookie, zéro tracking fragile,
zéro app tierce. Chaque ambassadeur = un code unique = une remise pour sa
communauté + une commission pour lui.

stdlib uniquement (urllib), comme le reste de la pipeline. Réutilise le client
Shopify de scripts/publish.py (auth Client Credentials Grant + .env à la racine).
"""
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import load_env, Shopify  # noqa: E402

REGISTRY = os.path.join(ROOT, "affiliation", "ambassadeurs.csv")
REPORTS_DIR = os.path.join(ROOT, "affiliation", "rapports")


# ------------------------------- registre ---------------------------------- #
def load_registry(path=REGISTRY):
    """Lit ambassadeurs.csv -> liste de dicts normalisés. Contrôle l'unicité des codes."""
    if not os.path.exists(path):
        sys.exit("Registre introuvable : %s" % path)
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):  # start=2 : ligne CSV (en-tête = 1)
            code = (row.get("code") or "").strip().upper()
            if not code:
                continue
            row["code"] = code
            row["statut"] = (row.get("statut") or "").strip().lower()
            row["taux"] = _to_float(row.get("taux"), 0.10)          # commission, ex. 0.10 = 10 %
            row["remise_client"] = _to_float(row.get("remise_client"), 15)  # remise en %, ex. 15
            row["_ligne"] = i
            rows.append(row)
    _check_unique(rows)
    return rows


def _to_float(v, default):
    try:
        return float(str(v).replace(",", ".").strip())
    except (TypeError, ValueError):
        return default


def _check_unique(rows):
    seen = {}
    for r in rows:
        if r["code"] in seen:
            sys.exit("Code en double dans le registre : %s (lignes %s et %s)"
                     % (r["code"], seen[r["code"]], r["_ligne"]))
        seen[r["code"]] = r["_ligne"]


def full_name(row):
    return " ".join(x for x in [(row.get("prenom") or "").strip(),
                                (row.get("nom") or "").strip()] if x).strip()


# ---------------------- Shopify : requêtes avec en-têtes -------------------- #
def client():
    """Client Shopify prêt à l'emploi (token géré par publish.Shopify)."""
    return Shopify(load_env())


def _request(sh, method, url_or_path, payload=None, ok_404=False):
    """GET/POST bas niveau réutilisant le token de publish.Shopify, mais qui
    EXPOSE LES EN-TÊTES (indispensable pour la pagination via le header Link,
    que publish._req n'expose pas). ok_404=True : renvoie None au lieu de lever."""
    url = url_or_path if url_or_path.startswith("http") else sh.base + url_or_path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("X-Shopify-Access-Token", sh.token)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return (json.loads(body) if body else {}), dict(resp.headers)
    except urllib.error.HTTPError as e:
        if e.code == 404 and ok_404:
            return None, {}
        detail = e.read().decode("utf-8", "replace")
        raise SystemExit("HTTP %s sur %s %s\n%s" % (e.code, method, url, detail))


def _next_link(headers):
    """Extrait l'URL de la page suivante depuis le header Link (pagination REST)."""
    link = headers.get("Link") or headers.get("link") or ""
    for part in link.split(","):
        seg = part.split(";")
        if len(seg) >= 2 and 'rel="next"' in seg[1]:
            return seg[0].strip().strip("<>")
    return None


# ------------------------------- commandes --------------------------------- #
ORDER_FIELDS = ("id,name,created_at,cancelled_at,financial_status,test,"
                "currency,subtotal_price,current_subtotal_price,"
                "total_line_items_price,total_price,discount_codes")


def fetch_orders(sh, created_min, created_max, verbose=True):
    """Récupère toutes les commandes de la fenêtre [min, max], pagination incluse."""
    params = urllib.parse.urlencode({
        "status": "any",
        "created_at_min": created_min,
        "created_at_max": created_max,
        "limit": 250,
        "fields": ORDER_FIELDS,
    })
    url = "/orders.json?" + params
    orders, page = [], 0
    while url:
        data, headers = _request(sh, "GET", url)
        batch = data.get("orders", [])
        orders += batch
        page += 1
        if verbose:
            print("  page %d : %d commandes (cumul %d)" % (page, len(batch), len(orders)))
        url = _next_link(headers)
        if url:
            time.sleep(0.3)  # respect du rate limit REST
    return orders


# ------------------------------ codes promo -------------------------------- #
def lookup_code(sh, code):
    """Renvoie le discount_code Shopify s'il existe (via /discount_codes/lookup), sinon None."""
    data, _ = _request(sh, "GET",
                       "/discount_codes/lookup.json?code=%s" % urllib.parse.quote(code),
                       ok_404=True)
    if not data:
        return None
    return data.get("discount_code")


def get_price_rule(sh, price_rule_id):
    data, _ = _request(sh, "GET", "/price_rules/%s.json" % price_rule_id)
    return (data or {}).get("price_rule")


def create_code(sh, code, remise_client, starts_at):
    """Crée une price rule (remise -remise_client %) + son code promo.
    Retourne (price_rule, discount_code)."""
    pr_payload = {"price_rule": {
        "title": "AMBASSADEUR-%s" % code,
        "target_type": "line_item",
        "target_selection": "all",
        "allocation_method": "across",
        "value_type": "percentage",
        "value": "-%.1f" % float(remise_client),   # ex. "-15.0"
        "customer_selection": "all",
        "once_per_customer": False,                 # réutilisable par la communauté
        "starts_at": starts_at,
    }}
    pr, _ = _request(sh, "POST", "/price_rules.json", pr_payload)
    price_rule = pr["price_rule"]
    dc, _ = _request(sh, "POST", "/price_rules/%s/discount_codes.json" % price_rule["id"],
                     {"discount_code": {"code": code}})
    return price_rule, dc["discount_code"]
