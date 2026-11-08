# -*- coding: utf-8 -*-
"""Blueprint Make v3 : webhook Tally -> Notion (Clients / Animaux / Dossiers) -> e-mail.

Deux lecons payees comptant :

1. 07/11/2026 — dans la charge utile Tally, `label` n'est PAS l'intitule affiche
   de la question mais le NOM INTERNE du champ. Ce script lit donc
   `payload.name` dans le schema du formulaire publie, jamais le titre.

2. 08/11/2026 — le module Notion de Make remplace tout saut de ligne par la
   chaine litterale « <br /> » dans une propriete texte (verifie : un saut, deux
   sauts, et un saut produit par une formule donnent tous « <br /> »). Les deux
   textes longs ne passent donc plus par des proprietes : ils sont ecrits dans
   le CORPS de la page Dossier, en vrais blocs Notion. Le garde-fou
   `controle_sauts_de_ligne` interdit desormais tout saut de ligne dans le
   blueprint, pour que le defaut ne puisse pas revenir.
"""
import io, json, re, sys

NB = u" "
SCHEMA = "schema_formulaire_pbgAZZ.json"
blocs = json.load(io.open(SCHEMA, encoding="utf-8"))

NOMS = set()
TYPES = {}        # nom interne -> type de bloc Tally
OPTIONS = {}      # nom interne -> [textes d'options]
for b in blocs:
    p = b.get("payload") or {}
    if b.get("type") == "HIDDEN_FIELDS":
        for hf in (p.get("hiddenFields") or []):
            NOMS.add(hf.get("name"))
            TYPES[hf.get("name")] = "HIDDEN_FIELDS"
        continue
    n = p.get("name")
    if not n:
        continue
    NOMS.add(n)
    TYPES[n] = b.get("type")
    if b.get("type") in ("MULTIPLE_CHOICE_OPTION", "CHECKBOX"):
        OPTIONS.setdefault(n, []).append(p.get("text", ""))

for n in NOMS:
    assert NB not in n, "insecable dans un nom interne : %r" % n

F = "1.data.fields"
LIBRE = ("INPUT_TEXT", "TEXTAREA", "INPUT_LINK")
COUPE = 1900      # une propriete comme un bloc Notion plafonne a 2 000 caracteres


def N(nom):
    assert nom in NOMS, "nom interne inconnu : %r" % nom
    assert '"' not in nom
    return nom


def brut(nom):
    return 'get(map(%s; "value"; "label"; "%s"); 1)' % (F, N(nom))


def txt(nom):
    return "{{%s}}" % brut(nom)


def choix(nom):
    lab = N(nom)
    sel = 'get(get(map(%s; "value"; "label"; "%s"); 1); 1)' % (F, lab)
    opts = 'get(map(%s; "options"; "label"; "%s"); 1)' % (F, lab)
    return '{{get(map(%s; "text"; "id"; %s); 1)}}' % (opts, sel)


def coche(nom):
    return '{{if(length(get(map(%s; "value"; "label"; "%s"); 1)) > 0; true; false)}}' \
        % (F, N(nom))


def coche_date(nom):
    return '{{if(length(get(map(%s; "value"; "label"; "%s"); 1)) > 0; now; emptystring)}}' \
        % (F, N(nom))


def option(nom, fragment):
    cands = [o for o in OPTIONS.get(N(nom), []) if fragment.lower() in o.lower()]
    assert len(cands) == 1, "option ambigue %r / %r -> %s" % (nom, fragment, cands)
    return cands[0]


def switch(nom, paires):
    args = "; ".join('"%s"; "%s"' % (option(nom, a), b) for a, b in paires)
    return '{{switch(%s; %s; "")}}' % (choix(nom)[2:-2], args)


def valeur(nom):
    """La valeur d'un champ, telle qu'elle s'affiche dans le corps du Dossier."""
    if nom in OPTIONS:
        inner = choix(nom)[2:-2]
    else:
        inner = brut(nom)
        if TYPES.get(N(nom)) in LIBRE:
            inner = "substring(%s; 0; %d)" % (inner, COUPE)
    # toString : un champ numerique renvoie un nombre, Notion exige une chaine.
    # Et un contenu reduit a « espace + formule » est reduit par Make a la valeur
    # brute : l'espace de separation doit donc etre un fragment statique a part.
    return '{{toString(ifempty(%s; "non renseigné"))}}' % inner


# ---------------------------------------------------------------- blocs Notion

def h3(titre):
    return {"type": "heading_3",
            "heading_3": {"text": [{"type": "text", "text": {"content": titre}}]}}


def ligne(etiquette, nom):
    return {"type": "paragraph", "paragraph": {"text": [
        {"type": "text", "text": {"content": etiquette + NB + ":"},
         "annotations": {"bold": True}},
        {"type": "text", "text": {"content": " "}},
        {"type": "text", "text": {"content": valeur(nom)}},
    ]}}


MOTIF = ["Motif détaillé", "Dernier épisode", "Déjà essayé",
         "Objectif"]

QUESTIONNAIRE = [
    "Ancienneté",
    "Fréquence",
    "Évolution",
    "Réaction du maître",
    "Habitat",
    "Environnement",
    "Adultes au foyer",
    "Autres animaux",
    "Cohérence du foyer",
    "Temps seul",
    "Sorties",
    "Alimentation",
    "Sommeil",
    "Santé connue",
    "Traitements",
    "Compléments",
    "Autre professionnel",
    "Quatre premiers mois",
]

CORPS = ([h3("Le motif, par le client")] +
         [ligne(e, e) for e in MOTIF] +
         [h3("Le questionnaire tel que reçu")] +
         [ligne(e, e) for e in QUESTIONNAIRE])

# ------------------------------------------------------------------- scenario

CLIENTS = "3ddfde7b-711d-4824-8cd7-c7f893911dc0"
ANIMAUX = "de7e8e55-5bb7-4521-8aa1-eab0d6431faf"
DOSSIERS = "6cfb904e-03b1-44b6-8f18-0be7f2656ddf"
CNX_NOTION = 8104817
CNX_GMAIL = 10587186     # connexion « google » : ActionSendEmail refuse « google-email »
HOOK = 4058042

courriel = txt("email")
prenom = '{{ifempty(%s; %s)}}' % (brut("first_name"), brut("Prénom du client"))

veto = switch("Vétérinaire consulté", [
    ("cause médicale", "Cause médicale écartée"),
    ("traitement est en cours", "Traitement en cours"),
    ("sans examen approfondi", "Sans examen approfondi"),
    ("Non, jamais", "Jamais"),
])
risque = switch("Niveau de risque", [
    ("Non, jamais", "Aucun contact"),
    ("Contact sans marque", "Contact sans marque"),
    ("Marque ou rougeur", "Marque ou rougeur"),
    ("Plaie superficielle", "Plaie superficielle"),
    ("Plaie profonde", "Plaie profonde ou morsures multiples"),
])
sexe = switch("Sexe", [("Mâle", "Mâle"), ("Femelle", "Femelle")])
provenance = switch("Provenance", [
    ("Élevage", "Élevage"), ("Refuge", "Refuge"),
    ("Association", "Association"), ("Particulier", "Particulier"),
    ("Animalerie", "Animalerie"), ("Trouvé", "Trouvé"),
    ("Né chez vous", "Né chez vous"),
])
sterilise = '{{if(%s = "%s"; true; false)}}' % (
    choix("Stérilisé")[2:-2], option("Stérilisé", "Oui"))

CLIENT_ID = '{{ifempty(get(map(3.array; "id"); 1); 5.id)}}'

flow = [
    {"id": 1, "module": "gateway:CustomWebHook", "version": 1,
     "parameters": {"hook": HOOK, "maxResults": 1}, "mapper": {},
     "metadata": {"designer": {"x": 0, "y": 0,
                               "name": "Questionnaire Tally reçu"}}},
    {"id": 2, "module": "notion:searchObjects1", "version": 1,
     "parameters": {"__IMTCONN__": CNX_NOTION},
     "mapper": {"limit": 1, "select": "data_source_item", "data_source": CLIENTS,
                "filter": [[{"a": "E-mail |&*^%$#@| email", "o": "email:equals",
                             "b": courriel}]]},
     "metadata": {"designer": {"x": 300, "y": 0,
                               "name": "Ce client existe-t-il déjà ?"}}},
    {"id": 3, "module": "builtin:BasicAggregator", "version": 1,
     "parameters": {"feeder": 2}, "mapper": {"id": "{{2.id}}"},
     "metadata": {"designer": {"x": 600, "y": 0,
                               "name": "Toujours un bundle, même si personne"}}},
    {"id": 4, "module": "builtin:BasicRouter", "version": 1, "mapper": None,
     "metadata": {"designer": {"x": 900, "y": 0}},
     "routes": [
         {"flow": [
             {"id": 5, "module": "notion:createDataSourceItem", "version": 1,
              "parameters": {"__IMTCONN__": CNX_NOTION},
              "filter": {"name": "Client inconnu",
                         "conditions": [[{"a": '{{get(map(3.array; "id"); 1)}}',
                                          "o": "notexist"}]]},
              "mapper": {"select": "map", "data_source": CLIENTS, "fields": [
                  {"key": "Prénom", "type": "title", "value": prenom},
                  {"key": "E-mail", "type": "email", "value": courriel},
                  {"key": "Statut", "type": "select", "value": "Bilan en cours"},
                  {"key": "Dernier contact", "type": "date",
                   "date": {"start": "{{now}}", "includeTime": True}},
              ]},
              "metadata": {"designer": {"x": 1200, "y": -150,
                                        "name": "Créer la fiche Client"}}},
         ]},
         {"flow": [
             {"id": 6, "module": "notion:createDataSourceItem", "version": 1,
              "parameters": {"__IMTCONN__": CNX_NOTION},
              "mapper": {"select": "map", "data_source": ANIMAUX, "fields": [
                  {"key": "Nom de l'animal", "type": "title",
                   "value": txt("Nom du chien")},
                  {"key": "Espèce", "type": "select", "value": "Chien"},
                  {"key": "Sexe", "type": "select", "value": sexe},
                  {"key": "Stérilisé", "type": "checkbox", "value": sterilise},
                  {"key": "Âge à la stérilisation", "type": "rich_text",
                   "value": txt("Âge à la stérilisation")},
                  {"key": "Race ou croisement", "type": "rich_text", "value": txt("Race")},
                  {"key": "Âge", "type": "rich_text", "value": txt("Âge")},
                  {"key": "Poids (kg)", "type": "number", "value": txt("Poids")},
                  {"key": "Provenance", "type": "select", "value": provenance},
                  {"key": "Âge à l'arrivée (semaines)", "type": "number",
                   "value": txt("Âge à l'arrivée (semaines)")},
                  {"key": "Date d'arrivée au foyer", "type": "date",
                   "date": {"start": txt("Date d'arrivée"), "includeTime": False}},
                  {"key": "Client", "type": "relation", "value": [CLIENT_ID]},
              ]},
              "metadata": {"designer": {"x": 1200, "y": 150,
                                        "name": "Créer la fiche Animal"}}},
             {"id": 7, "module": "notion:createDataSourceItem", "version": 1,
              "parameters": {"__IMTCONN__": CNX_NOTION},
              "mapper": {"select": "map", "data_source": DOSSIERS, "fields": [
                  {"key": "Motif", "type": "title", "value": txt("Motif")},
                  {"key": "N° de commande", "type": "rich_text",
                   "value": txt("order_id")},
                  {"key": "Statut", "type": "select", "value": "Questionnaire reçu"},
                  {"key": "Date de réception", "type": "date",
                   "date": {"start": "{{now}}", "includeTime": True}},
                  {"key": "Liens vidéo", "type": "url",
                   "value": txt("Lien vidéo")},
                  {"key": "Vétérinaire consulté", "type": "select",
                   "value": veto},
                  {"key": "Niveau de risque", "type": "select", "value": risque},
                  {"key": "Animal", "type": "relation", "value": ["{{6.id}}"]},
              ]},
              "metadata": {"designer": {"x": 1500, "y": 150,
                                        "name": "Créer le Dossier"}}},
             {"id": 10, "module": "notion:appendADatabaseItemContent", "version": 1,
              "parameters": {"__IMTCONN__": CNX_NOTION},
              "mapper": {"select": "map", "page": "{{7.id}}", "objects": CORPS},
              "metadata": {"designer": {
                  "x": 1800, "y": 150,
                  "name": "Écrire le questionnaire dans le Dossier"}}},
             {"id": 8, "module": "notion:updateADatabaseItem", "version": 1,
              "parameters": {"__IMTCONN__": CNX_NOTION},
              "mapper": {"page": CLIENT_ID, "select": "map", "updateBy": "data_source",
                         "data_source": CLIENTS, "fields": [
                             {"key": "Statut", "type": "select", "value": "Bilan en cours"},
                             {"key": "Dernier contact", "type": "date",
                              "date": {"start": "{{now}}", "includeTime": True}},
                             {"key": "Consentement e-mail", "type": "checkbox",
                              "value": coche("Consentement e-mail")},
                             {"key": "Date consentement e-mail", "type": "date",
                              "date": {"start": coche_date("Consentement e-mail"),
                                       "includeTime": True}},
                             {"key": "Consentement cas pédagogique",
                              "type": "checkbox",
                              "value": coche("Consentement cas pédagogique")},
                             {"key": "Date consentement cas", "type": "date",
                              "date": {"start": coche_date(
                                  "Consentement cas pédagogique"),
                                  "includeTime": True}},
                         ]},
              "metadata": {"designer": {"x": 2100, "y": 150,
                                        "name": "Rafraîchir la fiche Client"}}},
             {"id": 9, "module": "google-email:ActionSendEmail", "version": 1,
              "parameters": {"account": CNX_GMAIL},
              "mapper": {
                  "to": ["contact@gusetfrost.fr"],
                  "subject": "Nouveau questionnaire" + NB + ": " + txt("Nom du chien") +
                             " (" + prenom + ")",
                  "html": ("<p>Un questionnaire du Programme vient d'arriver.</p>"
                           "<p><strong>Motif" + NB + ":</strong> " + txt("Motif") + "</p>"
                           "<p><strong>Vétérinaire" + NB + ":</strong> " + veto +
                           "<br><strong>Niveau de risque" + NB + ":</strong> " +
                           risque + "</p>"
                           "<p><strong>Vidéo" + NB + ":</strong> " +
                           txt("Lien vidéo") +
                           "</p><p><strong>N° de commande" + NB + ":</strong> " +
                           txt("order_id") + "</p>"
                           "<p>Dossier Notion" + NB + ": https://www.notion.so/"
                           "{{replace(7.id; \"-\"; \"\")}}</p>"
                           "<p style=\"color:#888;font-size:13px\">Délai contractuel"
                           + NB + ": 7" + NB + "jours ouvrés. Objectif" + NB +
                           ": 72" + NB + "h.</p>"),
                  "attachments": [],
              },
              "metadata": {"designer": {"x": 2400, "y": 150,
                                        "name": "Prévenir Régis"}}},
         ]},
     ]},
]

bp = {"name": "Questionnaire Tally → Notion (Le Programme)", "flow": flow,
      "metadata": {"instant": True, "version": 1,
                   "scenario": {"roundtrips": 1, "maxErrors": 3, "autoCommit": True,
                                "autoCommitTriggerLast": True, "sequential": False,
                                "slots": None, "confidential": False, "dataloss": False,
                                "dlq": False, "freshVariables": False},
                   "designer": {"orphans": []}}}

s = json.dumps(bp, ensure_ascii=False, separators=(",", ":"))

# ------------------------------------------------------------------ garde-fous

def controle_sauts_de_ligne(texte):
    """Un saut de ligne ressort en « <br /> » litteral chez Notion : interdit."""
    assert "\\n" not in texte and "\\r" not in texte and "\n" not in texte, \
        "saut de ligne dans le blueprint : Notion afficherait un <br /> litteral"
    assert "<br />" not in texte, "balise <br /> en dur dans le blueprint"


def controle_insecables(texte):
    """Chaque insecable sert la typographie, et aucun signe double n'en manque."""
    for m in re.finditer(NB, texte):
        suivant = texte[m.end():m.end() + 1]
        assert suivant in (":", ";", "!", "?", "»") \
            or texte[m.start() - 1].isdigit(), \
            "insecable mal placee : %r" % texte[max(0, m.start() - 30):m.end() + 10]
    for m in re.finditer(r" (?=[:;!?»])", texte):
        raise AssertionError("espace ordinaire avant un signe double : %r"
                             % texte[max(0, m.start() - 40):m.end() + 10])
    for e in MOTIF + QUESTIONNAIRE:
        assert (e + NB + ":") in texte, "etiquette sans insecable : %r" % e


def controle_etiquettes(texte):
    """Les libelles cherches dans la charge utile Tally doivent exister."""
    trouves = re.findall(r'\\"label\\"; \\"(.*?)\\"', texte)
    assert trouves, "aucun libelle Tally trouve : la regle de controle est a revoir"
    for lab in trouves:
        assert lab in NOMS, "libelle Tally inconnu : %r" % lab


controle_sauts_de_ligne(s)
controle_insecables(s)
controle_etiquettes(s)

io.open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(s)
print("blueprint v3 ecrit : %d octets" % len(s))
print("corps du Dossier : %d blocs" % len(CORPS))
print("insecables : %d" % s.count(NB))
