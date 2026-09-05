#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Petit utilitaire : lire / ecrire UN fichier de theme Shopify.

  python scripts/theme_file.py pull sections/gf-cookie-consent.liquid theme/gf-cookie-consent.liquid
  python scripts/theme_file.py push sections/gf-cookie-consent.liquid theme/gf-cookie-consent.liquid --allow-live
  python scripts/theme_file.py themes
"""
import argparse
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from publish import load_env, Shopify      # noqa: E402
import wire_theme as wt                     # noqa: E402


def theme_gid(sh, theme_id=None):
    themes = wt.list_themes(sh)
    if theme_id:
        t = next((x for x in themes if str(x["id"]) == str(theme_id)), None)
    else:
        t = next((x for x in themes if x["role"] == "main"), None)
    if not t:
        raise SystemExit("Theme introuvable.")
    return t, "gid://shopify/OnlineStoreTheme/%s" % t["id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["pull", "push", "themes"])
    ap.add_argument("remote", nargs="?")
    ap.add_argument("local", nargs="?")
    ap.add_argument("--theme-id")
    ap.add_argument("--allow-live", action="store_true")
    a = ap.parse_args()

    sh = Shopify(load_env())

    if a.action == "themes":
        for t in wt.list_themes(sh):
            print("%-14s %-12s %s" % (t["id"], t["role"], t["name"]))
        return

    t, gid = theme_gid(sh, a.theme_id)
    print("Theme : %s (%s, %s)" % (t["name"], t["id"], t["role"]))

    if a.action == "pull":
        content = wt.read_file(sh, gid, a.remote)
        if content is None:
            raise SystemExit("Fichier absent du theme : %s" % a.remote)
        with io.open(os.path.join(ROOT, a.local), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print("OK pull -> %s (%d octets)" % (a.local, len(content.encode("utf-8"))))
        return

    if t["role"] == "main" and not a.allow_live:
        raise SystemExit("Theme PUBLIE : ajoutez --allow-live pour ecrire dessus.")
    with io.open(os.path.join(ROOT, a.local), "r", encoding="utf-8") as f:
        content = f.read()
    wt.upsert_file(sh, gid, a.remote, content)
    print("OK push %s -> %s (%d octets)" % (a.local, a.remote, len(content.encode("utf-8"))))


if __name__ == "__main__":
    main()
