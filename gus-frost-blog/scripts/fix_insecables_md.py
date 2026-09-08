#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pose les espaces insecables U+00A0 dans un fichier Markdown, hors blocs de code,
   hors code en ligne et hors URL. Puis controle qu'il n'en manque plus."""
import io, re, sys

NB = " "


def corrige_ligne(l):
    morceaux = re.split(r"(`[^`]*`|<https?://[^>]*>|\bhttps?://\S+)", l)
    for i in range(0, len(morceaux), 2):
        t = morceaux[i]
        t = re.sub(r" ([:;!?»])", NB + r"\1", t)
        t = re.sub(r"(«) ", r"\1" + NB, t)
        t = re.sub(r"(\d) (€|%)", r"\1" + NB + r"\2", t)
        morceaux[i] = t
    return "".join(morceaux)


def parcours(s, action):
    dans_code, out, defauts = False, [], []
    for n, l in enumerate(s.split("\n"), 1):
        if l.lstrip().startswith("```"):
            dans_code = not dans_code
            out.append(l)
            continue
        if dans_code:
            out.append(l)
            continue
        if action == "corrige":
            out.append(corrige_ligne(l))
        else:
            hors = "".join(re.split(r"(`[^`]*`|<https?://[^>]*>|\bhttps?://\S+)", l)[::2])
            if re.search(r"[^\s ] [:;!?»]|« [^\s]", hors):
                defauts.append((n, l.strip()[:80]))
            out.append(l)
    return "\n".join(out), defauts


for p in sys.argv[1:]:
    s = io.open(p, encoding="utf-8", newline="\n").read()
    s2, _ = parcours(s, "corrige")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
    _, defauts = parcours(s2, "controle")
    print("%s : %d insecables, %d defaut(s) restant(s)"
          % (p, s2.count(NB), len(defauts)))
    for n, l in defauts:
        print("   ligne %d" % n)
