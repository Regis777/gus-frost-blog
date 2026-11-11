# -*- coding: utf-8 -*-
"""Fabrique une soumission Tally de recette et l'envoie au webhook Make.

Pourquoi ce script : rejouer une vraie soumission etait jusqu'ici impossible
sans remplir les sept pages du formulaire a la main. Il lit le schema du
formulaire publie, donc les identifiants d'options sont les vrais, et la charge
utile a exactement la forme de celle que Tally envoie.

    python -I charge_utile_test.py <url du webhook> [--nom ZZTest] [--email x@y]

L'URL du webhook n'est pas ecrite ici : c'est un secret partage, elle se passe
en argument.
"""
import io, json, sys, uuid, datetime, urllib.request

SCHEMA = "schema_formulaire_pbgAZZ.json"

# Reponses de recette, par NOM INTERNE de champ. Pour un choix, le texte de
# l'option (ou un fragment sans ambiguite) ; pour des cases, une liste.
# Les questions a cases en cochent PLUSIEURS, dont des options a virgule :
# c'est ce cas-la que la recopie dans Notion doit tenir.
REPONSES = {
    "order_id": "TEST-RECETTE",
    "email": "zz-recette@gusetfrost.fr",
    "first_name": "Essai",
    "Prénom du client": "Essai",
    "Nom du chien": "ZZTest",
    "Sexe": "Mâle",
    "Stérilisé": "Non",
    "Âge à la stérilisation": None,
    "Race": "Croise berger",
    "Âge": "3 ans",
    "Poids": 22,
    "Provenance": "Refuge",
    "Âge à l'arrivée (semaines)": 10,
    "Date d'arrivée": "2026-11-03",
    "Quatre premiers mois": "Donnees de test, a supprimer.",
    "Motif": "RECETTE TECHNIQUE - a supprimer",
    "Motif détaillé": "Soumission de recette, chaine Tally vers Notion.",
    "Ancienneté": "Plus d'un an",
    "Contexte d'apparition": ["Déménagement", "Décès, humain ou animal"],
    "Fréquence": "De temps en temps",
    "Évolution": "C'est stable",
    "Déclencheurs": ["Bruits", "La solitude", "Vétérinaire"],
    "Dernier épisode": "Test automatise.",
    "Niveau de risque": "Marque ou rougeur sans plaie",
    "Réaction du maître": "Test automatise.",
    "Déjà essayé": "Test automatise.",
    "Objectif": "Test automatise.",
    "Habitat": "Maison avec jardin clôturé",
    "Environnement": "Périurbain",
    "Adultes au foyer": 2,
    "Enfants au foyer": ["De 4 à 10 ans"],
    "Autres animaux": "Aucun. Test automatise.",
    "Cohérence du foyer": "Test automatise.",
    "Temps seul": "De 1 à 3 heures",
    "Solitude": ["Vocalises", "Destructions"],
    "Sorties": "2 sorties, 1 h au total",
    "Type de sorties": ["Hygiénique", "Longe"],
    "Matériel": ["Harnais", "Longe"],
    "Occupation": ["Mastication", "Jeux de flair"],
    "Alimentation": "Croquettes, 2 repas",
    "Sommeil": "Panier au salon, 14 h",
    "Vétérinaire consulté": "sans examen approfondi",
    "Dernier examen": "2026-11-03",
    "Santé connue": "Aucun. Test automatise.",
    "Traitements": "Aucun. Test automatise.",
    "Signes de douleur": ["Raideur au lever", "Sensibilité au toucher"],
    "Compléments": "Aucun",
    "Autre professionnel": "Non. Test automatise.",
    "Lien vidéo": "https://example.com/test-recette",
}
# Les quatre consentements : coches, la seule option de chaque groupe.
CONSENTEMENTS = ("Consentement cadre", "Consentement exactitude",
                 "Consentement rétractation", "Consentement e-mail",
                 "Consentement cas pédagogique")

SIMPLE = {"INPUT_TEXT": "INPUT_TEXT", "TEXTAREA": "TEXTAREA",
          "INPUT_NUMBER": "INPUT_NUMBER", "INPUT_DATE": "INPUT_DATE",
          "INPUT_LINK": "INPUT_LINK"}


def charge_utile(blocs, reponses):
    champs = []
    groupes = {}
    for b in blocs:
        t = b.get("type")
        p = b.get("payload") or {}
        if t == "HIDDEN_FIELDS":
            for hf in (p.get("hiddenFields") or []):
                champs.append({"key": "question_" + hf["uuid"][:8],
                               "label": hf["name"], "type": "HIDDEN_FIELDS",
                               "value": reponses.get(hf["name"])})
        elif t in SIMPLE:
            champs.append({"key": "question_" + b["uuid"][:8],
                           "label": p["name"], "type": t,
                           "value": reponses.get(p["name"])})
        elif t in ("MULTIPLE_CHOICE_OPTION", "CHECKBOX"):
            g = groupes.setdefault(b["groupUuid"], {
                "nom": p["name"], "type": b.get("groupType"),
                "cle": "question_" + b["groupUuid"][:8], "options": []})
            g["options"].append({"id": b["uuid"], "text": p.get("text", "")})
            g["position"] = g.get("position", len(champs))
            if p.get("isLast"):
                champs.append(g)
    sortie = []
    for c in champs:
        if "options" not in c:
            sortie.append(c)
            continue
        nom, opts = c["nom"], c["options"]
        voulu = reponses.get(nom)
        if nom in CONSENTEMENTS:
            voulu = [opts[0]["text"]]
        if voulu is None:
            choisis = []
        elif isinstance(voulu, list):
            choisis = [cherche(opts, v, nom) for v in voulu]
        else:
            choisis = [cherche(opts, voulu, nom)]
        sortie.append({"key": c["cle"], "label": nom,
                       "type": "MULTIPLE_CHOICE" if c["type"] == "MULTIPLE_CHOICE"
                       else "CHECKBOXES",
                       "value": [o["id"] for o in choisis], "options": opts})
        if c["type"] != "MULTIPLE_CHOICE":
            ids = set(o["id"] for o in choisis)
            for o in opts:
                sortie.append({"key": c["cle"] + "_" + o["id"],
                               "label": "%s (%s)" % (nom, o["text"]),
                               "type": "CHECKBOXES", "value": o["id"] in ids})
    return sortie


def plat(t):
    """Les textes d'options affiches contiennent des insecables, pas les noms."""
    return t.replace(u" ", " ")


def cherche(opts, voulu, nom):
    voulu = plat(voulu)
    exact = [o for o in opts if plat(o["text"]) == voulu]
    if len(exact) == 1:
        return exact[0]
    flous = [o for o in opts if voulu.lower() in plat(o["text"]).lower()]
    assert len(flous) == 1, "option ambigue ou absente : %r / %r" % (nom, voulu)
    return flous[0]


def main():
    url = sys.argv[1]
    args = sys.argv[2:]
    reponses = dict(REPONSES)
    for i in range(0, len(args) - 1, 2):
        cle, val = args[i], args[i + 1]
        if cle == "--nom":
            reponses["Nom du chien"] = val
        elif cle == "--email":
            reponses["email"] = val
        elif cle == "--commande":
            reponses["order_id"] = val
        else:
            raise SystemExit("argument inconnu : " + cle)

    blocs = json.load(io.open(SCHEMA, encoding="utf-8"))
    champs = charge_utile(blocs, reponses)
    maintenant = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    rid = uuid.uuid4().hex[:7]
    corps = {
        "eventId": str(uuid.uuid4()),
        "eventType": "FORM_RESPONSE",
        "createdAt": maintenant,
        "data": {"responseId": rid, "submissionId": rid, "respondentId": rid,
                 "locale": None, "formId": "pbgAZZ",
                 "formName": "Votre bilan comportemental",
                 "createdAt": maintenant, "fields": champs},
    }
    brut = json.dumps(corps, ensure_ascii=False).encode("utf-8")
    sans_valeur = [c["label"] for c in champs
                   if c.get("value") in (None, [], "") and "(" not in c["label"]]
    print("%d champs, %d octets" % (len(champs), len(brut)))
    print("chien : %s | e-mail : %s | commande : %s"
          % (reponses["Nom du chien"], reponses["email"], reponses["order_id"]))
    if sans_valeur:
        print("sans valeur : " + ", ".join(sans_valeur))
    req = urllib.request.Request(url, data=brut,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print("reponse Make : %s %s" % (r.status, r.read().decode("utf-8")[:80]))


if __name__ == "__main__":
    main()
