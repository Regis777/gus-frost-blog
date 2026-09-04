#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gus & Frost — balises de validation de propriete du site (Yandex, Pinterest…).

Les consoles webmaster demandent de prouver qu'on possede le domaine. Trois
methodes existent partout : enregistrement DNS, fichier a la racine, ou balise
<meta> dans le <head>. Sur Shopify la balise meta est la plus simple et la plus
sure : une ligne, idempotente, retirable, et elle ne depend pas d'un acces DNS.

Ce script pose / retire / verifie ces balises dans layout/theme.liquid du theme
EN LIGNE. Il ne touche jamais au reste du fichier : si l'ancre </head> est
introuvable, il s'arrete au lieu de bricoler.

Cas Yandex, a connaitre : la validation dans Yandex Webmaster n'est pas qu'un
confort. Yandex n'accepte les notifications IndexNow que pour les sites dont les
droits sont verifies chez lui — sans elle, la moitie « Yandex » du ping de
scripts/ping_indexnow.py est ignoree. Voir [[indexnow-ping]].

Usage :
  python scripts/site_verification.py --list                       # ce qui est pose aujourd'hui
  python scripts/site_verification.py --add yandex --code XXXX --dry-run
  python scripts/site_verification.py --add yandex --code XXXX
  python scripts/site_verification.py --check yandex               # la balise est-elle servie ?
  python scripts/site_verification.py --remove yandex
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from publish import load_env, Shopify                              # noqa: E402
from wire_theme import list_themes, read_file, upsert_file         # noqa: E402
from ping_indexnow import http, site_url                           # noqa: E402

THEME_FILE = "layout/theme.liquid"

# cle CLI -> (attribut name= de la balise, console concernee)
PROVIDERS = {
    "yandex":    ("yandex-verification", "Yandex Webmaster"),
    "google":    ("google-site-verification", "Google Search Console"),
    "bing":      ("msvalidate.01", "Bing Webmaster Tools"),
    "pinterest": ("p:domain_verify", "Pinterest"),
    "facebook":  ("facebook-domain-verification", "Meta Business"),
}


def meta_re(name):
    """Reperage tolerant : ordre des attributs et type de guillemets libres."""
    return re.compile(r'[ \t]*<meta[^>]*\bname=["\']%s["\'][^>]*>\s*\n?'
                      % re.escape(name), re.IGNORECASE)


def pick_theme(sh, theme_id=None):
    themes = list_themes(sh)
    if theme_id:
        t = next((x for x in themes if str(x["id"]) == str(theme_id)), None)
    else:
        t = next((x for x in themes if x.get("role") == "main"), None)
    if not t:
        sys.exit("Theme cible introuvable. `python scripts/wire_theme.py --list` pour les id.")
    return t


def cmd_list(sh, theme):
    body = read_file(sh, theme["gid"], THEME_FILE)
    if body is None:
        sys.exit("%s introuvable sur le theme %s." % (THEME_FILE, theme["name"]))
    found = re.findall(r'<meta[^>]*\bname=["\']([^"\']+)["\'][^>]*\bcontent=["\']([^"\']*)["\']',
                       body, re.IGNORECASE)
    known = {v[0]: k for k, v in PROVIDERS.items()}
    rows = [(n, c) for n, c in found if n in known]
    if not rows:
        print("Aucune balise de validation posee dans %s." % THEME_FILE)
        return
    for name, content in rows:
        print("  %-28s %-34s (%s)"
              % (name, content, PROVIDERS[known[name]][1]))


def cmd_add(sh, theme, key, code, dry_run):
    name, console = PROVIDERS[key]
    body = read_file(sh, theme["gid"], THEME_FILE)
    if body is None:
        sys.exit("%s introuvable sur le theme %s." % (THEME_FILE, theme["name"]))

    tag = '  <meta name="%s" content="%s">\n' % (name, code)
    rx = meta_re(name)
    existing = rx.search(body)
    if existing:
        if code in existing.group(0):
            print("  = %s deja pose avec ce code, rien a faire." % name)
            return
        new = rx.sub(tag, body, count=1)
        action = "remplace (l'ancien code est ecrase)"
    else:
        if "</head>" not in body:
            sys.exit("Ancre </head> introuvable dans %s : rien touche." % THEME_FILE)
        new = body.replace("</head>", tag + "</head>", 1)
        action = "ajoute avant </head>"

    print("  %s -> %s  [%s]" % (name, code, action))
    if dry_run:
        print("DRY-RUN : rien ecrit.")
        return
    upsert_file(sh, theme["gid"], THEME_FILE, new)
    print("  ✓ %s ecrit sur le theme « %s »" % (THEME_FILE, theme["name"]))
    print("\nValide maintenant depuis la console %s." % console)


def cmd_remove(sh, theme, key, dry_run):
    name, _ = PROVIDERS[key]
    body = read_file(sh, theme["gid"], THEME_FILE)
    if body is None:
        sys.exit("%s introuvable sur le theme %s." % (THEME_FILE, theme["name"]))
    rx = meta_re(name)
    if not rx.search(body):
        print("  = %s absent, rien a faire." % name)
        return
    new = rx.sub("", body, count=1)
    print("  - %s retire" % name)
    if dry_run:
        print("DRY-RUN : rien ecrit.")
        return
    upsert_file(sh, theme["gid"], THEME_FILE, new)
    print("  ✓ %s ecrit" % THEME_FILE)


def cmd_check(env, key):
    """Verifie ce que le site sert VRAIMENT, pas ce que le fichier contient."""
    name, console = PROVIDERS[key]
    base = site_url(env)
    code, body = http("GET", base + "/")
    if code != 200:
        print("  ✗ accueil injoignable (HTTP %s)" % code)
        return False
    m = re.search(r'<meta[^>]*\bname=["\']%s["\'][^>]*>' % re.escape(name),
                  body, re.IGNORECASE)
    if not m:
        print("  ✗ aucune balise %s servie sur %s/" % (name, base))
        return False
    print("  ✓ servie sur %s/ : %s" % (base, m.group(0).strip()))
    print("    (%s peut valider)" % console)
    return True


def main():
    ap = argparse.ArgumentParser(description="Balises de validation de propriete du site.")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--add", choices=sorted(PROVIDERS))
    ap.add_argument("--remove", choices=sorted(PROVIDERS))
    ap.add_argument("--check", choices=sorted(PROVIDERS))
    ap.add_argument("--code", help="valeur content= fournie par la console")
    ap.add_argument("--theme-id", help="theme cible (defaut : le theme en ligne)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    env = load_env()

    if args.check:
        sys.exit(0 if cmd_check(env, args.check) else 1)

    if not (args.list or args.add or args.remove):
        ap.error("donne --list, --add, --remove ou --check.")
    if args.add and not args.code:
        ap.error("--add exige --code (la valeur content= donnee par la console).")

    sh = Shopify(env)
    theme = pick_theme(sh, args.theme_id)
    theme["gid"] = "gid://shopify/OnlineStoreTheme/%s" % theme["id"]
    print("Theme : %s (%s, id=%s)" % (theme["name"], theme["role"], theme["id"]))

    if args.list:
        cmd_list(sh, theme)
    if args.add:
        cmd_add(sh, theme, args.add, args.code, args.dry_run)
    if args.remove:
        cmd_remove(sh, theme, args.remove, args.dry_run)


if __name__ == "__main__":
    main()
