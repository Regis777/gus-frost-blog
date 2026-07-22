#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gus & Frost — publication des articles de blog Shopify, pilotee par manifest.csv.

Conception :
  - stdlib uniquement (urllib) : aucun pip requis.
  - resout les liens internes PLACEHOLDER_ via reference/placeholder-map.json + .env
    (les <img src="REMPLACER_..."> sont laissees telles quelles : images traitees plus tard).
  - cree les articles en BROUILLON (published=false) par defaut.
  - ordre impose : PILIER avant ses satellites, cluster par cluster.
  - idempotent : si un article existe deja (meme handle), il est mis a jour (PUT) au lieu d'etre recree.

Usage :
  python scripts/publish.py --dry-run --only anxiete-separation-chien      # ecrit build/<slug>.html, aucun appel API
  python scripts/publish.py --only anxiete-separation-chien                # publie CE pilier en brouillon
  python scripts/publish.py --cluster 1                                    # tout le cluster 1 (pilier d'abord)
  python scripts/publish.py --all                                          # les 33, dans l'ordre
  python scripts/publish.py --all --publish                               # passe published=true (NE PAS lancer sans validation)

Le .env est lu depuis la racine du depot. Voir .env.example.
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "manifest.csv")

# ---------------------------- blogs geres ---------------------------------- #
# Le pipeline sert deux blogs. Chacun a SON manifest (les cluster_num se
# recoupent d'un blog a l'autre : C10 chien != CH10 chat) et SA collection CTA.
# Defaut « chiens » partout : sans --blog, le comportement historique est intact.
BLOGS = {
    "chiens": {"manifest": "manifest.csv", "collection": "stress"},
    "chats": {"manifest": "manifest_chat.csv", "collection": "chat"},
}
DEFAULT_BLOG = "chiens"
MANIFEST_HEADER = ("cluster_num,cluster_tag,type,slug,parent_pilier_slug,title,"
                   "meta_title,meta_description,excerpt,tags,file,prompts_file,"
                   "links_to_resolve,images_to_resolve\n")
MAP_FILE = os.path.join(ROOT, "reference", "placeholder-map.json")
BUILD_DIR = os.path.join(ROOT, "build")
TOKEN_CACHE = os.path.join(ROOT, ".shopify_token_cache.json")

PLACEHOLDER_RE = re.compile(r'PLACEHOLDER_[A-Za-z0-9-]+')
IMG_REMPLACER_RE = re.compile(r'REMPLACER_[A-Za-z0-9.\-]+')


def blog_conf(handle=None):
    """Config du blog cible : handle, manifest dedie, collection du CTA."""
    h = (handle or DEFAULT_BLOG).strip()
    if h not in BLOGS:
        sys.exit("Blog '%s' inconnu. Blogs geres : %s" % (h, ", ".join(sorted(BLOGS))))
    conf = dict(BLOGS[h])
    conf["handle"] = h
    conf["manifest_path"] = os.path.join(ROOT, conf["manifest"])
    return conf


def ensure_manifest(path):
    """Cree le manifest (en-tete seul) s'il n'existe pas encore : cas du 1er
    cluster d'un nouveau blog."""
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(MANIFEST_HEADER)
    return path


# ----------------------------- .env ---------------------------------------- #
def load_env():
    env = {}
    path = os.path.join(ROOT, ".env")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    # les variables d'environnement reelles ont la priorite
    for k in ("SHOPIFY_STORE_DOMAIN", "SHOPIFY_CLIENT_ID", "SHOPIFY_CLIENT_SECRET",
              "SHOPIFY_ADMIN_TOKEN", "SHOPIFY_API_VERSION",
              "BLOG_HANDLE", "COLLECTION_HANDLE", "PRODUCT_GILET_HANDLE",
              "PRODUCT_TAPIS_FOUILLE_HANDLE", "PRODUCT_TAPIS_LECHAGE_HANDLE"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    env.setdefault("SHOPIFY_API_VERSION", "2024-10")
    return env


# ------------------------- resolution des liens ---------------------------- #
def build_resolver(env):
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        m = json.load(f)
    blog = env.get("BLOG_HANDLE", "").strip()
    resolved = {}

    def article_url(slug):
        return "/blogs/%s/%s" % (blog, slug)

    for token, slug in m.get("piliers", {}).items():
        resolved[token] = article_url(slug)
    for token, slug in m.get("satellites", {}).items():
        resolved[token] = article_url(slug)

    def expand(val):
        # remplace ${VAR} par la valeur d'env
        def repl(mo):
            return env.get(mo.group(1), "").strip()
        return re.sub(r'\$\{([A-Z_]+)\}', repl, val)

    for token, val in m.get("collections", {}).items():
        h = expand(val)
        if h:
            resolved[token] = "/collections/%s" % h
    for token, val in m.get("produits", {}).items():
        if token.startswith("_"):
            continue
        h = expand(val)
        if h:
            resolved[token] = "/products/%s" % h
    return resolved


CTA_DIV_RE = re.compile(r'(<div class="gf-cta">)(.*?)(</div>)', re.S)


def wrap_cta_call(html):
    """Met en forme le bloc .gf-cta :
       - deux-points (espace insecable avant, typo FR) juste avant le bouton ;
       - pas de point apres le bouton ;
       - isole la derniere phrase d'appel dans <span class="gf-cta-call"> (sur sa ligne).
    Idempotent. Bloc d'une seule phrase (pas de '. ') : juste ponctuation, sans span."""
    def repl(m):
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        inner = inner.replace("dans notre <a", "dans notre&nbsp;: <a")
        inner = inner.replace("</a>.", "</a>")
        if "gf-cta-call" not in inner:
            idx = inner.rstrip().rfind(". ")
            if idx != -1:
                head, tail = inner[:idx + 2], inner[idx + 2:].strip()
                if tail:
                    inner = '%s<span class="gf-cta-call">%s</span>' % (head, tail)
        return "%s%s%s" % (open_tag, inner, close_tag)
    return CTA_DIV_RE.sub(repl, html)


def resolve_body(html, resolver):
    """Remplace les PLACEHOLDER_ par leur URL. Retourne (html, unresolved_set, image_count)."""
    unresolved = set()

    def repl(mo):
        token = mo.group(0)
        if token in resolver:
            return resolver[token]
        unresolved.add(token)
        return token

    out = PLACEHOLDER_RE.sub(repl, html)
    images = IMG_REMPLACER_RE.findall(out)
    return out, unresolved, len(images)


# ------------------------------- manifest ---------------------------------- #
def read_manifest(path=None):
    rows = []
    with open(path or MANIFEST, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def order_rows(rows):
    """Tri : par cluster, pilier avant satellites."""
    return sorted(rows, key=lambda r: (int(r["cluster_num"]),
                                       0 if r["type"] == "pilier" else 1,
                                       r["slug"]))


def select_rows(rows, args):
    if args.only:
        sel = [r for r in rows if r["slug"] == args.only]
        if not sel:
            sys.exit("Aucun article avec slug '%s' dans le manifest." % args.only)
        return sel
    if args.cluster:
        sel = [r for r in rows if r["cluster_num"] == str(args.cluster)]
        if args.type:
            sel = [r for r in sel if r["type"] == args.type]
        return order_rows(sel)
    if args.all:
        sel = rows
        if args.type:
            sel = [r for r in sel if r["type"] == args.type]
        return order_rows(sel)
    sys.exit("Precise --only <slug>, --cluster <n> ou --all.")


# ------------------------------ Shopify API -------------------------------- #
class Shopify:
    def __init__(self, env):
        self.domain = env.get("SHOPIFY_STORE_DOMAIN", "").strip()
        self.version = env.get("SHOPIFY_API_VERSION", "2024-10").strip()
        self.client_id = env.get("SHOPIFY_CLIENT_ID", "").strip()
        self.client_secret = env.get("SHOPIFY_CLIENT_SECRET", "").strip()
        # token "tout fait" facultatif (compat retro) ; sinon Client Credentials Grant
        self.static_token = env.get("SHOPIFY_ADMIN_TOKEN", "").strip()
        if not self.domain:
            sys.exit("SHOPIFY_STORE_DOMAIN doit etre defini dans .env")
        if not self.static_token and not (self.client_id and self.client_secret):
            sys.exit("Fournis SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET (recommande) "
                     "ou SHOPIFY_ADMIN_TOKEN dans .env")
        self.base = "https://%s/admin/api/%s" % (self.domain, self.version)
        self.token = self._get_token()

    # --- Client Credentials Grant (token valide ~24 h, mis en cache local) --- #
    def _get_token(self):
        if self.static_token:
            return self.static_token
        cached = self._read_cache()
        if cached:
            return cached
        token, expires_in = self._fetch_token()
        self._write_cache(token, expires_in)
        return token

    def _read_cache(self):
        try:
            with open(TOKEN_CACHE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            return None
        if data.get("domain") != self.domain or data.get("client_id") != self.client_id:
            return None
        # marge de securite de 120 s avant expiration
        if data.get("expires_at", 0) - 120 > time.time():
            return data.get("access_token")
        return None

    def _write_cache(self, token, expires_in):
        data = {
            "domain": self.domain,
            "client_id": self.client_id,
            "access_token": token,
            "expires_at": time.time() + int(expires_in),
        }
        try:
            with open(TOKEN_CACHE, "w", encoding="utf-8") as f:
                json.dump(data, f)
            os.chmod(TOKEN_CACHE, 0o600)
        except OSError:
            pass  # cache best-effort

    def _fetch_token(self):
        url = "https://%s/admin/oauth/access_token" % self.domain
        form = urllib.parse.urlencode({
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }).encode("utf-8")
        req = urllib.request.Request(url, data=form, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("Accept", "application/json")
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            raise SystemExit(
                "Echec Client Credentials Grant (HTTP %s). Verifie le Client ID/Secret "
                "et que l'app est bien installee sur le store.\n%s" % (e.code, detail))
        token = data.get("access_token")
        if not token:
            raise SystemExit("Reponse OAuth sans access_token : %s" % data)
        return token, data.get("expires_in", 86399)

    def _req(self, method, path, payload=None):
        url = self.base + path
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("X-Shopify-Access-Token", self.token)
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            raise SystemExit("HTTP %s sur %s %s\n%s" % (e.code, method, path, detail))

    def find_blog_id(self, handle):
        data = self._req("GET", "/blogs.json?limit=250")
        for b in data.get("blogs", []):
            if b.get("handle") == handle:
                return b["id"]
        avail = ", ".join(b.get("handle", "?") for b in data.get("blogs", []))
        sys.exit("Blog handle '%s' introuvable. Blogs disponibles : %s" % (handle, avail))

    def find_article(self, blog_id, handle):
        data = self._req("GET", "/blogs/%s/articles.json?handle=%s&limit=1" % (blog_id, handle))
        arts = data.get("articles", [])
        return arts[0] if arts else None

    def upsert_article(self, blog_id, payload):
        existing = self.find_article(blog_id, payload["handle"])
        body = {"article": payload}
        if existing:
            return self._req("PUT", "/blogs/%s/articles/%s.json" % (blog_id, existing["id"]), body), "maj"
        return self._req("POST", "/blogs/%s/articles.json" % blog_id, body), "creation"


# ------------------------------- payload ----------------------------------- #
def make_payload(row, body_html, publish):
    tags = ", ".join(t.strip() for t in row["tags"].split(",") if t.strip())
    return {
        "title": row["title"],
        "handle": row["slug"],
        "body_html": body_html,
        "tags": tags,
        "author": "Gus & Frost",
        "published": bool(publish),
        "metafields": [
            {"namespace": "global", "key": "title_tag",
             "value": row["meta_title"], "type": "single_line_text_field"},
            {"namespace": "global", "key": "description_tag",
             "value": row["meta_description"], "type": "single_line_text_field"},
        ],
    }


# --------------------------------- main ------------------------------------ #
def main():
    ap = argparse.ArgumentParser(description="Publication blog Gus & Frost (manifest-driven).")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--only", help="slug d'un seul article")
    g.add_argument("--cluster", type=int, choices=[1, 2, 3])
    g.add_argument("--all", action="store_true")
    ap.add_argument("--type", choices=["pilier", "satellite"],
                    help="filtre (avec --cluster/--all) : ne publier que les piliers ou les satellites.")
    ap.add_argument("--publish", action="store_true",
                    help="published=true (defaut : brouillon). NE PAS utiliser sans validation.")
    ap.add_argument("--dry-run", action="store_true",
                    help="aucun appel API : ecrit le HTML resolu dans build/ et affiche le diagnostic.")
    args = ap.parse_args()

    env = load_env()
    resolver = build_resolver(env)
    rows = select_rows(read_manifest(), args)

    if not args.dry_run:
        sh = Shopify(env)
        blog_id = sh.find_blog_id(env.get("BLOG_HANDLE", "").strip())
    else:
        os.makedirs(BUILD_DIR, exist_ok=True)

    print("=" * 70)
    print("Cible blog handle : %s | brouillon : %s | dry-run : %s"
          % (env.get("BLOG_HANDLE", "?"), not args.publish, args.dry_run))
    print("Articles a traiter : %d (pilier d'abord)" % len(rows))
    print("=" * 70)

    total_unresolved = 0
    for row in rows:
        path = os.path.join(ROOT, row["file"].replace("/", os.sep))
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        body, unresolved, n_imgs = resolve_body(raw, resolver)
        body = wrap_cta_call(body)
        flag = "  [%s]" % row["type"].upper()
        print("\n- %s%s" % (row["slug"], flag))
        print("    liens non resolus : %s | images REMPLACER restantes : %d"
              % (sorted(unresolved) if unresolved else "0", n_imgs))
        total_unresolved += len(unresolved)

        if args.dry_run:
            out = os.path.join(BUILD_DIR, row["slug"] + ".html")
            with open(out, "w", encoding="utf-8") as f:
                f.write(body)
            print("    -> ecrit : %s" % os.path.relpath(out, ROOT))
            continue

        payload = make_payload(row, body, args.publish)
        result, action = sh.upsert_article(blog_id, payload)
        art = result.get("article", {})
        print("    -> %s OK (id=%s, published=%s)"
              % (action, art.get("id"), art.get("published_at") is not None))
        time.sleep(0.6)  # respect du rate limit REST (2 req/s)

    print("\n" + "=" * 70)
    if total_unresolved:
        print("ATTENTION : %d lien(s) placeholder non resolu(s) au total "
              "(handle collection manquant ?)." % total_unresolved)
    print("Termine.")


if __name__ == "__main__":
    main()
