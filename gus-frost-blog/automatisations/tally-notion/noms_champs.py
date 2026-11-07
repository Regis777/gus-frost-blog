# -*- coding: utf-8 -*-
"""Associe chaque question a son NOM INTERNE : c'est lui que Tally envoie en `label`."""
import io, json, re

NB = " "
blocs = json.load(io.open("tally_blocs.json", encoding="utf-8"))
TAG = re.compile(r"<[^>]+>")


def texte(b):
    p = b.get("payload") or {}
    h = p.get("html")
    if h is None:
        h = p.get("safeHTMLSchema") or ""
    if isinstance(h, list):
        out = []

        def ap(x):
            if isinstance(x, str):
                out.append(x)
            elif isinstance(x, list):
                for y in x:
                    ap(y)
        ap(h)
        h = "".join(out)
    if not isinstance(h, str):
        h = str(h)
    return (TAG.sub("", h).replace("&nbsp;", NB).replace("&#39;", "'")
            .replace("&amp;", "&").strip())


SAISIE = ("INPUT_TEXT", "INPUT_NUMBER", "INPUT_DATE", "INPUT_LINK", "TEXTAREA",
          "MULTIPLE_CHOICE_OPTION", "CHECKBOX")

titre = ""
vus = set()
lignes = []
for b in blocs:
    t = b.get("type")
    p = b.get("payload") or {}
    if t == "TITLE":
        titre = texte(b)
        continue
    if t == "HIDDEN_FIELDS":
        for hf in (p.get("hiddenFields") or []):
            lignes.append(("[cache]", hf.get("name"), ""))
        continue
    if t in SAISIE:
        g = b.get("groupUuid")
        if t in ("MULTIPLE_CHOICE_OPTION", "CHECKBOX"):
            if g in vus:
                continue
            vus.add(g)
        nom = p.get("name") or ""
        lignes.append((titre, nom, t))

larg = max(len(x[1] or "") for x in lignes)
for titre, nom, t in lignes:
    print("%-*s  <- %s  [%s]" % (larg, nom or "(SANS NOM)", titre[:60], t))
print()
print(len(lignes), "champs")
sans = [l for l in lignes if not l[1]]
print(len(sans), "sans nom interne")
