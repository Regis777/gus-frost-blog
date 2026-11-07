# -*- coding: utf-8 -*-
"""Pousse la fiche produit du Programme (titre + SEO + description) sur Shopify.

Le contenu vient du JSON genere par fiche_programme.py : aucune retranscription,
donc aucune insecable perdue.
"""
import io, json, os, sys, urllib.request, urllib.error

SCRIPTS = r"C:\Users\regis\Google Drive\Gus et Frost\BLOGS_Gus et Frost\scripts"
sys.path.insert(0, SCRIPTS)
import publish  # noqa: E402

PID = "gid://shopify/Product/9672845230301"

with io.open(sys.argv[1], encoding="utf-8") as f:
    d = json.load(f)

env = publish.load_env()
sh = publish.Shopify(env)

MUT = """
mutation ($input: ProductInput!) {
  productUpdate(input: $input) {
    product { id title handle templateSuffix status
              seo { title description } }
    userErrors { field message }
  }
}
"""

payload = {
    "query": MUT,
    "variables": {
        "input": {
            "id": PID,
            "title": d["titre"],
            "descriptionHtml": d["html"],
            "seo": {"title": d["seoTitre"], "description": d["seoDesc"]},
        }
    },
}

res = sh._req("POST", "/graphql.json", payload)
print(json.dumps(res, ensure_ascii=False, indent=1)[:2000])

# relecture : on compare au bit pres
Q = """
query ($id: ID!) { product(id: $id) {
  title descriptionHtml seo { title description } } }
"""
back = sh._req("POST", "/graphql.json", {"query": Q, "variables": {"id": PID}})
p = back["data"]["product"]
print()
for cle, attendu, obtenu in (
    ("titre", d["titre"], p["title"]),
    ("seo titre", d["seoTitre"], p["seo"]["title"]),
    ("seo desc", d["seoDesc"], p["seo"]["description"]),
    ("description", d["html"], p["descriptionHtml"]),
):
    etat = "IDENTIQUE" if attendu == obtenu else "DIFFERENT"
    print("%-12s %s (%d car., %d insecables en ligne)" %
          (cle, etat, len(obtenu or ""), (obtenu or "").count("\u00a0")))
