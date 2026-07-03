#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Déploie le cluster C4 (langage corporel du chien) dans le blog « Chiens »
de Gus & Frost, via l'Admin GraphQL API.

- Crée les 13 articles EN BROUILLON par défaut (isPublished=false).
- Idempotent : si un article avec le même handle existe déjà dans le blog,
  il est mis à jour au lieu d'être dupliqué.
- Renseigne auteur (« Gus & Frost »), tags, et SEO (métachamps global.title_tag /
  global.description_tag).

Prérequis (variables d'environnement) :
  SHOPIFY_SHOP        ex: monshop.myshopify.com   (domaine .myshopify.com, pas gusetfrost.fr)
  SHOPIFY_ADMIN_TOKEN token Admin API (shpat_...) d'une app perso avec write_content
Optionnel :
  SHOPIFY_API_VERSION  (défaut 2025-04)
  SHOPIFY_BLOG_ID      (défaut = blog « Chiens » : gid://shopify/Blog/103894909149)
  PUBLISH=true         pour publier directement au lieu de créer en brouillon

Lancement (à la racine du repo) :
  export SHOPIFY_SHOP=monshop.myshopify.com
  export SHOPIFY_ADMIN_TOKEN=shpat_xxx
  python3 deploy/deploy_c4_to_shopify.py
"""
import os, csv, json, sys, urllib.request

SHOP    = os.environ.get("SHOPIFY_SHOP")
TOKEN   = os.environ.get("SHOPIFY_ADMIN_TOKEN")
API     = os.environ.get("SHOPIFY_API_VERSION", "2025-10")
BLOG_ID = os.environ.get("SHOPIFY_BLOG_ID", "gid://shopify/Blog/103894909149")
PUBLISH = os.environ.get("PUBLISH", "false").lower() == "true"
ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du repo

if not SHOP or not TOKEN:
    sys.exit("ERREUR : définis SHOPIFY_SHOP (xxx.myshopify.com) et SHOPIFY_ADMIN_TOKEN.")

def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/{API}/graphql.json",
        data=payload,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        out = json.loads(r.read().decode("utf-8"))
    if out.get("errors"):
        raise RuntimeError(json.dumps(out["errors"], ensure_ascii=False))
    return out["data"]

# NB : Blog.articles n'accepte pas d'argument `query`. On interroge donc la racine
# articles(query:"blog_id:<num> handle:<slug>") puis on filtre le handle exact.
FIND = "query($q: String!){ articles(first:5, query:$q){ nodes{ id handle } } }"
CREATE = ("mutation($a: ArticleCreateInput!){ articleCreate(article:$a){ "
          "article{ id handle isPublished } userErrors{ field message } } }")
UPDATE = ("mutation($id: ID!, $a: ArticleUpdateInput!){ articleUpdate(id:$id, article:$a){ "
          "article{ id handle isPublished } userErrors{ field message } } }")

def seo_metafields(row):
    return [
        {"namespace":"global","key":"title_tag","type":"single_line_text_field","value":row["meta_title"]},
        {"namespace":"global","key":"description_tag","type":"single_line_text_field","value":row["meta_description"]},
    ]

def main():
    rows = [r for r in csv.DictReader(open(os.path.join(ROOT,"manifest.csv"), encoding="utf-8"))
            if r["cluster_num"] == "4"]
    print(f"{len(rows)} articles C4 -> blog {BLOG_ID}  (publish={PUBLISH})\n")
    ok = 0
    for r in rows:
        slug = r["slug"]
        body = open(os.path.join(ROOT, r["file"]), encoding="utf-8").read().strip()
        tags = [t.strip() for t in r["tags"].split(",") if t.strip()]
        common = {"title":r["title"], "handle":slug, "body":body, "tags":tags,
                  "author":{"name":"Gus & Frost"}, "isPublished":PUBLISH,
                  "metafields":seo_metafields(r)}
        num = BLOG_ID.rsplit("/", 1)[-1]
        nodes = gql(FIND, {"q":f"blog_id:{num} handle:{slug}"})["articles"]["nodes"]
        found = [n for n in nodes if n["handle"] == slug]
        if found:
            res = gql(UPDATE, {"id":found[0]["id"], "a":common})["articleUpdate"]; act="MAJ  "
        else:
            res = gql(CREATE, {"a":{**common, "blogId":BLOG_ID}})["articleCreate"]; act="CRÉÉ "
        errs = res["userErrors"]
        if errs:
            print(f"  ✗ {slug} : {errs}")
        else:
            ok += 1
            print(f"  ✓ {act}{slug}  (isPublished={res['article']['isPublished']})")
    print(f"\nTerminé : {ok}/{len(rows)} OK. "
          f"{'Publiés.' if PUBLISH else 'En brouillon — à relire dans l’admin puis publier.'}")

if __name__ == "__main__":
    main()
