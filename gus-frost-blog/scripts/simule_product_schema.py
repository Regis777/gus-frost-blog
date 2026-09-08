#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rejoue HORS LIGNE la logique de snippets/gf-product-schema.liquid sur les donnees
reelles d'un produit, pour controler que le JSON produit est valide avant tout
depot sur la boutique. Ce n'est PAS un rendu Shopify : c'est une simulation
fidele des filtres Liquid utilises par le fragment.

  python scripts/simule_product_schema.py <handle> [--sortie build/x.json]
"""
import argparse, datetime, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import load_env, Shopify  # noqa: E402
from wire_theme import gql  # noqa: E402

SHOP_URL = "https://gusetfrost.fr"
DEVISE = "EUR"
PORT_MONTANT = "8.80"
PORT_PAYS = "FR"
PREPA = (1, 2)
TRANSIT = (2, 6)
RETOUR_JOURS = 14

REQUETE = """
query($handle: String!) {
  productByHandle(handle: $handle) {
    id title handle vendor productType descriptionHtml
    media(first: 10) { nodes { ... on MediaImage { image { url } } } }
    variants(first: 25) {
      nodes { id title price sku barcode availableForSale
              inventoryItem { requiresShipping } }
    }
  }
}
"""


def filtre_description(html):
    """Reproduit : replace '<' -> ' <' | strip_html | strip_newlines | decodage | collapse."""
    t = html.replace("<", " <")
    t = re.sub(r"<[^>]*>", "", t)          # strip_html
    t = t.replace("\n", "").replace("\r", "")  # strip_newlines
    for a, b in (("&nbsp;", " "), ("&#39;", "'"), ("&quot;", '"'),
                 ("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&")):
        t = t.replace(a, b)
    for motif in ("   ", "  ", "  "):
        t = t.replace(motif, " ")
    for a, b in ((" .", "."), (" ,", ","), (" )", ")")):
        t = t.replace(a, b)
    t = t.strip()
    return t[:5000] + "..." if len(t) > 5000 else t


def url_image(u, largeur=1946):
    """Reproduit : image_url: width: N | prepend: 'https:'."""
    base = u.split("?")[0]
    version = ""
    if "?" in u:
        for p in u.split("?", 1)[1].split("&"):
            if p.startswith("v="):
                version = "?" + p
    sep = "&" if version else "?"
    return "https:" + base.replace("https:", "") + version + sep + "width=%d" % largeur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("handle")
    ap.add_argument("--sortie")
    a = ap.parse_args()

    sh = Shopify(load_env())
    p = gql(sh, REQUETE, {"handle": a.handle})["productByHandle"]
    if not p:
        raise SystemExit("Produit introuvable : %s" % a.handle)

    base = SHOP_URL + "/products/" + p["handle"]
    images = [url_image(m["image"]["url"]) for m in p["media"]["nodes"] if m.get("image")][:8]
    desc = filtre_description(p["descriptionHtml"] or "")
    annee = datetime.date.today().year + 1
    v0 = p["variants"]["nodes"][0]

    d = {"@context": "https://schema.org/", "@type": "Product",
         "@id": base + "#product", "name": p["title"], "url": base}
    if images:
        d["image"] = images
    if desc:
        d["description"] = desc
    if p["vendor"]:
        d["brand"] = {"@type": "Brand", "name": p["vendor"]}
    if p["productType"]:
        d["category"] = p["productType"]
    if v0.get("sku"):
        d["sku"] = v0["sku"]
        d["mpn"] = v0["sku"]
    if v0.get("barcode") and len(v0["barcode"]) == 13:
        d["gtin13"] = v0["barcode"]

    offres = []
    for v in p["variants"]["nodes"]:
        vid = v["id"].rsplit("/", 1)[-1]
        o = {"@type": "Offer",
             "@id": "%s?variant=%s#offer" % (base, vid),
             "url": "%s?variant=%s" % (base, vid),
             "priceCurrency": DEVISE,
             "price": float(v["price"]),
             "priceValidUntil": "%d-12-31" % annee,
             "itemCondition": "https://schema.org/NewCondition",
             "availability": "https://schema.org/InStock" if v["availableForSale"]
                             else "https://schema.org/OutOfStock",
             "seller": {"@type": "Organization", "name": "Gus et Frost"}}
        if v.get("sku"):
            o["sku"] = v["sku"]
        if v.get("barcode") and len(v["barcode"]) == 13:
            o["gtin13"] = v["barcode"]
        if v["inventoryItem"]["requiresShipping"]:
            o["shippingDetails"] = {
                "@type": "OfferShippingDetails",
                "shippingRate": {"@type": "MonetaryAmount",
                                 "value": PORT_MONTANT, "currency": DEVISE},
                "shippingDestination": {"@type": "DefinedRegion",
                                        "addressCountry": PORT_PAYS},
                "deliveryTime": {
                    "@type": "ShippingDeliveryTime",
                    "handlingTime": {"@type": "QuantitativeValue",
                                     "minValue": PREPA[0], "maxValue": PREPA[1],
                                     "unitCode": "DAY"},
                    "transitTime": {"@type": "QuantitativeValue",
                                    "minValue": TRANSIT[0], "maxValue": TRANSIT[1],
                                    "unitCode": "DAY"}}}
            o["hasMerchantReturnPolicy"] = {
                "@type": "MerchantReturnPolicy",
                "applicableCountry": PORT_PAYS,
                "returnPolicyCountry": PORT_PAYS,
                "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                "merchantReturnDays": RETOUR_JOURS,
                "returnMethod": "https://schema.org/ReturnByMail",
                "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
                "refundType": "https://schema.org/FullRefund",
                "merchantReturnLink": SHOP_URL + "/policies/refund-policy"}
        else:
            o["hasMerchantReturnPolicy"] = {
                "@type": "MerchantReturnPolicy",
                "applicableCountry": PORT_PAYS,
                "returnPolicyCategory": "https://schema.org/MerchantReturnNotPermitted",
                "merchantReturnLink": SHOP_URL + "/policies/refund-policy"}
        offres.append(o)
    d["offers"] = offres

    texte = json.dumps(d, ensure_ascii=False, indent=2)
    json.loads(texte)  # controle de validite
    sortie = a.sortie or os.path.join("build", "jsonld_%s.json" % p["handle"])
    chemin = os.path.join(ROOT, sortie)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    io.open(chemin, "w", encoding="utf-8", newline="\n").write(texte + "\n")
    print("JSON valide — %d offres, %d images, description de %d caracteres"
          % (len(offres), len(images), len(desc)))
    print("Ecrit : %s" % sortie)


if __name__ == "__main__":
    main()
