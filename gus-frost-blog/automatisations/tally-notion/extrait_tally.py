# -*- coding: utf-8 -*-
"""Extrait le schema du formulaire Tally depuis la page publique."""
import io, json, re, sys

s = io.open("tally_page.html", encoding="utf-8").read()
m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', s, re.S)
d = json.loads(m.group(1))


def trouve_blocs(o, chemin=""):
    if isinstance(o, dict):
        if "blocks" in o and isinstance(o["blocks"], list) and o["blocks"]:
            yield chemin + ".blocks", o["blocks"]
        for k, v in o.items():
            for r in trouve_blocs(v, chemin + "." + k):
                yield r
    elif isinstance(o, list):
        for i, v in enumerate(o):
            for r in trouve_blocs(v, chemin + "[%d]" % i):
                yield r


for chemin, blocs in trouve_blocs(d):
    print(chemin, len(blocs))
    types = {}
    for b in blocs:
        types[b.get("type")] = types.get(b.get("type"), 0) + 1
    print("   ", types)
    with io.open("schema_formulaire_pbgAZZ.json", "w", encoding="utf-8") as f:
        json.dump(blocs, f, ensure_ascii=False, indent=1)
    break
