# -*- coding: utf-8 -*-
"""Le garde-fou doit refuser une reference a un module d'une autre route."""
import io, json, re

P = ("C:/Users/regis/Google Drive/Gus et Frost/BLOGS_Gus et Frost/"
     "automatisations/tally-notion/blueprint_v2.py")
src = io.open(P, encoding="utf-8").read()
ns = {"json": json, "re": re}
exec(src[src.index("def controle_routes"):src.index("controle_sauts_de_ligne(s)")], ns)

CAS = [
    ("la faute du 07/11 (5.id depuis l'autre route)",
     [{"id": 1, "module": "w"}, {"id": 3, "module": "z"},
      {"id": 4, "module": "builtin:BasicRouter", "routes": [
          {"flow": [{"id": 5, "module": "x"}]},
          {"flow": [{"id": 6, "module": "y", "mapper": {
              "b": '{{ifempty(get(map(3.array; "id"); 1); 5.id)}}'}}]}]}],
     False),
    ("un ancetre commun, legitime",
     [{"id": 1, "module": "w"}, {"id": 3, "module": "z"},
      {"id": 4, "module": "builtin:BasicRouter", "routes": [
          {"flow": [{"id": 6, "module": "y", "mapper": {
              "b": '{{get(map(3.array; "id"); 1)}}'}}]}]}],
     True),
    ("une reference dans la meme route, legitime",
     [{"id": 1, "module": "w"},
      {"id": 4, "module": "builtin:BasicRouter", "routes": [
          {"flow": [{"id": 7, "module": "y"},
                    {"id": 8, "module": "y", "mapper": {"b": "{{7.id}}"}}]}]}],
     True),
]

for nom, flow, doit_passer in CAS:
    try:
        ns["controle_routes"](flow)
        ok = True
        detail = ""
    except AssertionError as e:
        ok = False
        detail = str(e)
    verdict = "OK" if ok == doit_passer else "RATE"
    print("%-4s %-45s %s" % (verdict, nom, detail))
