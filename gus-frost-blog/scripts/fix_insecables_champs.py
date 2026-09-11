#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose les espaces insecables (U+00A0) dans les CHAMPS des articles en ligne :
titre, extrait (summary), titre SEO et description SEO.

POURQUOI
L'audit du 01/09/2026 avait mis le CORPS des 483 articles a zero faute, mais pas
ces quatre champs : le 11/09/2026, 78 titres et 83 extraits en ligne gardaient
une espace ordinaire avant « : ? ; ! » — d'ou un deux-points seul en debut de
ligne dans le titre de l'article, les listes du blog et le carrousel de
l'accueil. La faute venait des manifests (colonnes title, meta_title,
meta_description, excerpt), corriges le meme jour.

ORDRE A RESPECTER
Corriger les manifests AVANT de lancer ce script : sinon le prochain
publish / rebake reecrit les champs fautifs depuis la source.

REGLE (celle de fix_insecables_md.py)
Insecable avant : ; ! ? » , apres « , et entre un chiffre et € ou %.
Dans l'extrait (HTML), seul le texte hors balises est touche.

  python scripts/fix_insecables_champs.py            # a blanc : bilan seul
  python scripts/fix_insecables_champs.py --apply    # ecrit en ligne
  python scripts/fix_insecables_champs.py --corps [--apply]     # + corps des articles
  python scripts/fix_insecables_champs.py --sources [--apply]   # fichiers source locaux

CORPS : CORRECTION CHIRURGICALE, PAS DE RECUIT
Les titres fautifs avaient ete recopies dans les blocs cuits (« articles
lies », 922 occurrences). Relancer bake_maillage.py les aurait corriges... en
reconstruisant tout le bloc, encart « Le Carnet » compris, depuis une source
qui dit « chien » — alors que les articles chats ont en ligne une version
« chat ». Ici on ne change QUE des espaces, dans le texte hors balises, hors
<script> (donnees structurees) et hors <style>. Chaque modification est
verifiee : meme texte une fois les espaces retirees.
"""
import argparse
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import load_env, Shopify   # noqa: E402
import wire_theme as wt                  # noqa: E402

NB = u"\u00a0"
PONCT = re.compile(r"(?<=\S) ([:;!?\u00bb])")
GUILL = re.compile(u"\u00ab ")
CHIFFRE = re.compile(r"(\d) ([\u20ac%])")


def corrige_texte(t):
    t = PONCT.sub(NB + r"\1", t)
    t = GUILL.sub(u"\u00ab" + NB, t)
    return CHIFFRE.sub(r"\1" + NB + r"\2", t)


def corrige_html(h):
    morceaux = re.split(r"(<[^>]+>)", h)
    return "".join(m if m.startswith("<") else corrige_texte(m) for m in morceaux)


def corrige_corps(h):
    """Texte hors balises, en laissant intacts <script> et <style>."""
    blocs = re.split(r"(<script.*?</script>|<style.*?</style>)", h, flags=re.S | re.I)
    return "".join(b if re.match(r"<(script|style)", b, re.I) else corrige_html(b)
                   for b in blocs)


def seulement_des_espaces(avant, apres):
    """Garde-fou : chaque caractere modifie doit etre une espace ordinaire
    devenue insecable — rien d'autre. (Comparer les chaines apres avoir retire
    les insecables ne marche pas : celles deja presentes faussent le test.)"""
    if len(avant) != len(apres):
        return False
    return all(x == y or (x == " " and y == NB) for x, y in zip(avant, apres))


LIRE = """
query($c: String) {
  articles(first: 100, after: $c) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id title summary handle blog { handle }
      titre_seo: metafield(namespace: "global", key: "title_tag") { type value }
      desc_seo: metafield(namespace: "global", key: "description_tag") { type value }
    }
  }
}"""

ECRIRE = """
mutation($id: ID!, $article: ArticleUpdateInput!) {
  articleUpdate(id: $id, article: $article) {
    article { id }
    userErrors { field message }
  }
}"""


def tous_les_articles(sh):
    out, cur = [], None
    while True:
        d = wt.gql(sh, LIRE, {"c": cur})["articles"]
        out += d["nodes"]
        if not d["pageInfo"]["hasNextPage"]:
            return out
        cur = d["pageInfo"]["endCursor"]


def corrections(a):
    """Renvoie (entree ArticleUpdateInput, liste des champs touches)."""
    entree, champs = {}, []
    t = corrige_texte(a["title"] or "")
    if t != a["title"]:
        entree["title"] = t
        champs.append("titre")
    s = a.get("summary") or ""
    s2 = corrige_html(s)
    if s2 != s:
        entree["summary"] = s2
        champs.append("extrait")
    mfs = []
    for cle_gql, cle_mf, nom in (("titre_seo", "title_tag", "titre SEO"),
                                 ("desc_seo", "description_tag", "description SEO")):
        mf = a.get(cle_gql)
        if mf and mf.get("value"):
            v2 = corrige_texte(mf["value"])
            if v2 != mf["value"]:
                mfs.append({"namespace": "global", "key": cle_mf,
                            "type": mf["type"], "value": v2})
                champs.append(nom)
    if mfs:
        entree["metafields"] = mfs
    return entree, champs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="ecrire en ligne (sinon : a blanc)")
    ap.add_argument("--corps", action="store_true", help="corriger aussi le corps des articles en ligne")
    ap.add_argument("--sources", action="store_true", help="corriger les fichiers source locaux (colonne file)")
    a = ap.parse_args()
    if a.sources:
        return sources(a.apply)
    sh = Shopify(load_env())
    if a.corps:
        return corps(sh, a.apply)
    arts = tous_les_articles(sh)
    a_faire = [(x, *corrections(x)) for x in arts]
    a_faire = [(x, e, c) for (x, e, c) in a_faire if e]
    compte = {}
    for _, _, champs in a_faire:
        for c in champs:
            compte[c] = compte.get(c, 0) + 1
    print("articles lus : %d | a corriger : %d | champs : %s" % (len(arts), len(a_faire), compte))
    for x, _, champs in a_faire[:5]:
        print("  ex. %-8s %-50s %s" % (x["blog"]["handle"], x["title"][:50], champs))
    if not a.apply:
        print("A BLANC : rien n'a ete ecrit. Relancer avec --apply.")
        return
    erreurs = 0
    for i, (x, entree, _) in enumerate(a_faire, 1):
        d = wt.gql(sh, ECRIRE, {"id": x["id"], "article": entree})["articleUpdate"]
        if d["userErrors"]:
            erreurs += 1
            print("  ERREUR %s : %s" % (x["handle"], d["userErrors"]))
        if i % 20 == 0:
            print("  %d / %d" % (i, len(a_faire)))
        time.sleep(0.35)
    print("ecrits : %d, erreurs : %d" % (len(a_faire) - erreurs, erreurs))
    reste = [x for x in tous_les_articles(sh) if corrections(x)[0]]
    print("CONTROLE apres ecriture : %d article(s) encore fautif(s)" % len(reste))
    sys.exit(1 if reste or erreurs else 0)


LIRE_CORPS = """
query($c: String) {
  articles(first: 50, after: $c) {
    pageInfo { hasNextPage endCursor }
    nodes { id handle body }
  }
}"""


def corps(sh, apply):
    arts, cur = [], None
    while True:
        d = wt.gql(sh, LIRE_CORPS, {"c": cur})["articles"]
        arts += d["nodes"]
        if not d["pageInfo"]["hasNextPage"]:
            break
        cur = d["pageInfo"]["endCursor"]
    a_faire = []
    for x in arts:
        b = x["body"] or ""
        n = corrige_corps(b)
        if n != b:
            if not seulement_des_espaces(b, n):
                sys.exit("REFUS %s : modification autre qu'un espace" % x["handle"])
            a_faire.append((x, n))
    print("corps lus : %d | a corriger : %d" % (len(arts), len(a_faire)))
    if not apply:
        print("A BLANC : rien n'a ete ecrit.")
        return
    err = 0
    for i, (x, n) in enumerate(a_faire, 1):
        d = wt.gql(sh, ECRIRE, {"id": x["id"], "article": {"body": n}})["articleUpdate"]
        if d["userErrors"]:
            err += 1
            print("  ERREUR %s : %s" % (x["handle"], d["userErrors"]))
        if i % 25 == 0:
            print("  %d / %d" % (i, len(a_faire)))
        time.sleep(0.35)
    print("ecrits : %d, erreurs : %d" % (len(a_faire) - err, err))


def sources(apply):
    import csv
    import io
    total = fichiers = 0
    for m in ("manifest.csv", "manifest_chat.csv"):
        for r in csv.DictReader(io.open(os.path.join(ROOT, m), encoding="utf-8-sig")):
            f = os.path.join(ROOT, (r.get("file") or "").replace("/", os.sep))
            if not r.get("file") or not os.path.exists(f):
                continue
            brut = io.open(f, "rb").read()
            txt = brut.decode("utf-8")
            n = corrige_corps(txt)
            if n == txt:
                continue
            if not seulement_des_espaces(txt, n):
                sys.exit("REFUS %s : modification autre qu'un espace" % f)
            fichiers += 1
            total += sum(1 for x, y in zip(txt, n) if x != y)
            if apply:
                io.open(f, "wb").write(n.encode("utf-8"))   # fins de ligne preservees
    print("fichiers source a corriger : %d (%d espaces)%s"
          % (fichiers, total, "" if apply else " — A BLANC"))


if __name__ == "__main__":
    main()
