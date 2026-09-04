#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gus & Frost — notification instantanée des moteurs (IndexNow + Bing).

Prévient les moteurs qu'une URL vient d'être publiée ou modifiée, au lieu
d'attendre leur prochain passage sur le sitemap. Utile ici parce qu'on publie
par clusters entiers : 70 articles d'un coup, c'est 70 URL signalées en une
requête au lieu de plusieurs semaines de crawl naturel.

Deux transports, indépendants l'un de l'autre. Le script utilise ceux qui sont
configurés et ignore les autres sans râler.

  1. IndexNow (api.indexnow.org) -> Bing, Yandex, Seznam, Naver, Yep.
     Exige une clé HÉBERGÉE sur le domaine. Sur Shopify il n'y a pas de racine
     accessible en écriture : voir --install-key, qui pose le nécessaire.

  2. Bing URL Submission API -> Bing seul, mais AUCUN fichier à héberger.
     Une clé d'API générée dans Bing Webmaster Tools (Paramètres > Accès API)
     suffit. C'est le transport le plus simple à mettre en route.

Bing alimente Yahoo, DuckDuckGo, Ecosia, Qwant, ChatGPT Search et Perplexity :
c'est le transport qui compte le plus. Google n'a pas d'équivalent public
(son Indexing API est réservée aux offres d'emploi et aux directs) : pour lui,
seul le sitemap fait foi, donc rien à faire ici.

Variables .env (toutes optionnelles) :
  SITE_URL=https://gusetfrost.fr
  INDEXNOW_KEY=<32 à 128 caractères hexadécimaux>
  INDEXNOW_KEY_LOCATION=<URL complète du fichier de clé, si non standard>
  BING_WEBMASTER_API_KEY=<clé Bing Webmaster Tools>

Usage :
  python scripts/ping_indexnow.py --cluster 15                     # les URL du cluster 15 (blog chiens)
  python scripts/ping_indexnow.py --cluster 19 --blog chats --tag chaton
  python scripts/ping_indexnow.py --urls https://gusetfrost.fr/blogs/chiens/mon-article
  python scripts/ping_indexnow.py --sitemap                        # tout le site (rattrapage)
  python scripts/ping_indexnow.py --cluster 15 --dry-run           # montre ce qui partirait
  python scripts/ping_indexnow.py --verify-key                     # la clé est-elle joignable ?
  python scripts/ping_indexnow.py --install-key                    # pose la clé sur la boutique
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from publish import load_env, read_manifest, blog_conf  # noqa: E402

INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
BING_ENDPOINT = "https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch"
DEFAULT_SITE = "https://gusetfrost.fr"

# Le fichier de clé est servi par un gabarit de page, seule surface en texte brut
# qu'une boutique Shopify expose sur son propre domaine (les Fichiers partent sur
# cdn.shopify.com, autre hôte : IndexNow refuse).
KEY_PAGE_HANDLE = "indexnow"
KEY_TEMPLATE_SUFFIX = "indexnow"
KEY_TEMPLATE_FILE = "templates/page.indexnow.liquid"

INDEXNOW_MAX = 10000   # plafond du protocole
BING_MAX = 100         # lots volontairement courts : l'API renvoie 400 au-delà de 500

UA = "GusEtFrost-IndexNow/1.0 (+https://gusetfrost.fr)"


# ------------------------------ utilitaires -------------------------------- #
def env_get(env, key, default=None):
    """Les vraies variables d'environnement priment sur le .env."""
    return os.environ.get(key) or env.get(key) or default


def site_url(env):
    return env_get(env, "SITE_URL", DEFAULT_SITE).rstrip("/")


def host_of(url):
    m = re.match(r"https?://([^/]+)", url)
    return m.group(1) if m else url


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def http(method, url, body=None, headers=None):
    """Renvoie (code, texte). Ne lève pas sur 4xx/5xx : les codes sont l'information."""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("User-Agent", UA)
    if data is not None:
        req.add_header("Content-Type", "application/json; charset=utf-8")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:                                    # DNS, TLS, timeout…
        return 0, str(e)


# --------------------------- collecte des URL ------------------------------ #
def urls_for_cluster(env, n, tag=None, blog=None):
    conf = blog_conf(blog or env_get(env, "BLOG_HANDLE"))
    rows = [r for r in read_manifest(conf["manifest_path"]) if r["cluster_num"] == str(n)]
    if tag:
        pref = "articles/cluster-%d-%s/" % (n, tag)
        rows = [r for r in rows if r["file"].replace(os.sep, "/").startswith(pref)]
    base = site_url(env)
    return ["%s/blogs/%s/%s" % (base, conf["handle"], r["slug"]) for r in rows]


def urls_from_sitemap(env):
    """Déplie le sitemap index de Shopify et renvoie toutes les URL du site."""
    base = site_url(env)
    code, body = http("GET", base + "/sitemap.xml")
    if code != 200:
        sys.exit("Sitemap injoignable (HTTP %s) : %s/sitemap.xml" % (code, base))
    locs = re.findall(r"<loc>([^<]+)</loc>", body)
    children = [u for u in locs if "sitemap" in u.rsplit("/", 1)[-1]]
    if not children:
        return sorted(set(locs))
    out = []
    for child in children:
        c, b = http("GET", child.replace("&amp;", "&"))
        if c == 200:
            out += re.findall(r"<loc>([^<]+)</loc>", b)
        else:
            print("  ⚠ sous-sitemap illisible (HTTP %s) : %s" % (c, child))
    # La page qui sert la clé est technique : Shopify la met dans son sitemap,
    # inutile de la pousser aux moteurs en plus.
    skip = "/pages/%s" % KEY_PAGE_HANDLE
    return sorted({u.replace("&amp;", "&") for u in out
                   if not u.rstrip("/").endswith(skip)})


# ------------------------------- transports -------------------------------- #
INDEXNOW_CODES = {
    200: "OK, URL acceptées",
    202: "accepté, validation de la clé en cours",
    400: "requête invalide",
    403: "clé refusée (fichier de clé introuvable ou contenu incorrect)",
    422: "URL hors du domaine, ou clé ne correspondant pas à l'hôte",
    429: "trop de requêtes (throttling)",
}


def send_indexnow(env, urls, dry_run=False):
    key = env_get(env, "INDEXNOW_KEY")
    if not key:
        return None, "INDEXNOW_KEY absente du .env — transport ignoré"
    base = site_url(env)
    loc = env_get(env, "INDEXNOW_KEY_LOCATION") or "%s/%s.txt" % (base, key)
    ok = True
    detail = []
    for lot in chunks(urls, INDEXNOW_MAX):
        payload = {"host": host_of(base), "key": key,
                   "keyLocation": loc, "urlList": lot}
        if dry_run:
            detail.append("DRY-RUN %d URL" % len(lot))
            continue
        code, body = http("POST", INDEXNOW_ENDPOINT, payload)
        label = INDEXNOW_CODES.get(code, "réponse inattendue")
        detail.append("HTTP %s (%s) sur %d URL" % (code, label, len(lot)))
        if code not in (200, 202):
            ok = False
            if body.strip():
                detail.append("  réponse : %s" % body.strip()[:300])
    return ok, " | ".join(detail)


def send_bing(env, urls, dry_run=False):
    key = env_get(env, "BING_WEBMASTER_API_KEY")
    if not key:
        return None, "BING_WEBMASTER_API_KEY absente du .env — transport ignoré"
    base = site_url(env)
    ok = True
    detail = []
    for lot in chunks(urls, BING_MAX):
        if dry_run:
            detail.append("DRY-RUN %d URL" % len(lot))
            continue
        code, body = http("POST", "%s?apikey=%s" % (BING_ENDPOINT, key),
                          {"siteUrl": base, "urlList": lot})
        detail.append("HTTP %s sur %d URL" % (code, len(lot)))
        if code != 200:
            ok = False
            if body.strip():
                detail.append("  réponse : %s" % body.strip()[:300])
    return ok, " | ".join(detail)


def ping_urls(urls, env=None, dry_run=False, quiet=False):
    """Point d'entrée réutilisable par les scripts de déploiement.

    Renvoie True si au moins un transport a abouti, False si tous ceux qui sont
    configurés ont échoué, None si aucun n'est configuré. Ne lève jamais : un
    ping raté ne doit pas faire échouer une publication réussie.
    """
    env = env if env is not None else load_env()
    urls = sorted({u.strip() for u in urls if u and u.strip()})
    if not urls:
        if not quiet:
            print("Aucune URL à signaler.")
        return None
    results = {}
    for name, fn in (("IndexNow", send_indexnow), ("Bing", send_bing)):
        try:
            results[name] = fn(env, urls, dry_run)
        except Exception as e:                                # jamais bloquant
            results[name] = (False, "exception : %s" % e)
    if not quiet:
        print("Ping de %d URL%s%s :"
              % (len(urls), "s" if len(urls) > 1 else "",
                 "  [DRY-RUN]" if dry_run else ""))
        if dry_run:
            for u in urls[:5]:
                print("    %s" % u)
            if len(urls) > 5:
                print("    … et %d autres" % (len(urls) - 5))
        for name, (ok, msg) in results.items():
            mark = "…" if ok is None else ("✓" if ok else "✗")
            print("  %s %-9s %s" % (mark, name, msg))
    states = [ok for ok, _ in results.values() if ok is not None]
    if not states:
        return None
    return any(states)


# --------------------- installation de la clé IndexNow --------------------- #
def new_key():
    return os.urandom(16).hex()          # 32 caractères hexadécimaux


def key_candidates(env, key):
    base = site_url(env)
    return ["%s/%s.txt" % (base, key),
            "%s/pages/%s" % (base, KEY_PAGE_HANDLE)]


def verify_key(env):
    """Cherche où la clé est réellement servie et dit quoi mettre dans le .env."""
    key = env_get(env, "INDEXNOW_KEY")
    if not key:
        print("INDEXNOW_KEY absente du .env. Lance --install-key pour en poser une.")
        return False
    declared = env_get(env, "INDEXNOW_KEY_LOCATION")
    tried = ([declared] if declared else []) + key_candidates(env, key)
    good = None
    for url in tried:
        code, body = http("GET", url)
        served = body.strip()
        match = served == key
        print("  %s %-58s HTTP %s%s"
              % ("✓" if match else "✗", url, code,
                 "" if match else "  (contenu != clé)"))
        if match and good is None:
            good = url
    if not good:
        print("\nAucun emplacement ne renvoie la clé. IndexNow répondra 403.")
        print("Relance --install-key, ou pose le gabarit à la main (voir docstring).")
        return False
    print("\nClé servie sur : %s" % good)
    if declared != good:
        print("À mettre dans le .env :\n  INDEXNOW_KEY_LOCATION=%s" % good)
    return True


def install_key(env, theme_id=None, dry_run=False):
    """Pose de quoi servir la clé sur le domaine de la boutique :
         1. gabarit templates/page.indexnow.liquid ({% layout none %} + la clé)
         2. page /pages/indexnow qui utilise ce gabarit
         3. redirection /<clé>.txt -> /pages/indexnow (best effort)
    Exige une app Shopify avec write_themes + write_content.
    """
    from publish import Shopify                                   # noqa: E402
    from wire_theme import gql, list_themes, upsert_file          # noqa: E402

    key = env_get(env, "INDEXNOW_KEY") or new_key()
    base = site_url(env)
    sh = Shopify(env)

    themes = list_themes(sh)
    if theme_id:
        target = next((t for t in themes if str(t["id"]) == str(theme_id)), None)
    else:
        target = next((t for t in themes if t.get("role") == "main"), None)
    if not target:
        sys.exit("Thème cible introuvable. `python scripts/wire_theme.py --list` pour voir les id.")

    print("Thème : %s (%s, id=%s)" % (target["name"], target["role"], target["id"]))
    print("Clé   : %s" % key)
    if dry_run:
        print("DRY-RUN : rien écrit.")
        return

    gid = "gid://shopify/OnlineStoreTheme/%s" % target["id"]
    upsert_file(sh, gid, KEY_TEMPLATE_FILE, "{%%- layout none -%%}%s" % key)
    print("  ✓ %s posé" % KEY_TEMPLATE_FILE)

    existing = sh._req("GET", "/pages.json?handle=%s" % KEY_PAGE_HANDLE).get("pages", [])
    page = {"title": "IndexNow", "handle": KEY_PAGE_HANDLE, "body_html": "",
            "template_suffix": KEY_TEMPLATE_SUFFIX, "published": True}
    if existing:
        page["id"] = existing[0]["id"]
        sh._req("PUT", "/pages/%s.json" % page["id"], {"page": page})
        print("  ✓ page /pages/%s mise à jour" % KEY_PAGE_HANDLE)
    else:
        sh._req("POST", "/pages.json", {"page": page})
        print("  ✓ page /pages/%s créée" % KEY_PAGE_HANDLE)

    # Confort : rend l'emplacement standard /<clé>.txt valide lui aussi. Le scope
    # des redirections n'est pas toujours accordé — on n'en fait pas un échec.
    try:
        sh._req("POST", "/redirects.json",
                {"redirect": {"path": "/%s.txt" % key, "target": "/pages/%s" % KEY_PAGE_HANDLE}})
        print("  ✓ redirection /%s.txt -> /pages/%s" % (key, KEY_PAGE_HANDLE))
    except SystemExit as e:
        print("  ⚠ redirection non créée (%s) — sans conséquence, "
              "INDEXNOW_KEY_LOCATION suffit." % e)

    print("\nÀ ajouter au .env :")
    print("  INDEXNOW_KEY=%s" % key)
    print("  INDEXNOW_KEY_LOCATION=%s/pages/%s" % (base, KEY_PAGE_HANDLE))
    print("\nPuis : python scripts/ping_indexnow.py --verify-key")


# ---------------------------------- CLI ------------------------------------ #
def main():
    ap = argparse.ArgumentParser(description="Signale des URL à IndexNow et à Bing.")
    ap.add_argument("--cluster", type=int, help="numéro de cluster du manifest")
    ap.add_argument("--tag", help="suffixe du sous-cluster, ex. chiot-accueil")
    ap.add_argument("--blog", default=None, help="chiens (défaut) ou chats")
    ap.add_argument("--urls", nargs="+", help="URL complètes à signaler")
    ap.add_argument("--sitemap", action="store_true", help="toutes les URL du sitemap")
    ap.add_argument("--home", action="store_true", help="accueil + les deux pages hub")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify-key", action="store_true", help="la clé IndexNow est-elle servie ?")
    ap.add_argument("--install-key", action="store_true", help="pose la clé sur la boutique")
    ap.add_argument("--theme-id", help="thème cible de --install-key (défaut : le thème en ligne)")
    args = ap.parse_args()

    env = load_env()

    if args.verify_key:
        sys.exit(0 if verify_key(env) else 1)
    if args.install_key:
        install_key(env, args.theme_id, args.dry_run)
        return

    base = site_url(env)
    urls = []
    if args.cluster is not None:
        found = urls_for_cluster(env, args.cluster, args.tag, args.blog)
        if not found:
            print("⚠ Aucune ligne de manifest pour le cluster %d%s (blog %s)."
                  % (args.cluster, "/" + args.tag if args.tag else "",
                     args.blog or env_get(env, "BLOG_HANDLE", "chiens")))
        urls += found
    if args.urls:
        urls += args.urls
    if args.sitemap:
        urls += urls_from_sitemap(env)
    if args.home:
        urls += [base + "/",
                 base + "/pages/conseils-chiens",
                 base + "/pages/conseils-chats"]
    if not urls:
        ap.error("rien à signaler : donne --cluster, --urls, --sitemap ou --home.")

    res = ping_urls(urls, env, args.dry_run)
    sys.exit(0 if res is not False else 1)


if __name__ == "__main__":
    main()
