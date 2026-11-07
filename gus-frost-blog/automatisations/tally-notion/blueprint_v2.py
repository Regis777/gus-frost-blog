# -*- coding: utf-8 -*-
"""Blueprint Make v2 : webhook Tally -> Notion (Clients / Animaux / Dossiers) -> e-mail.

Lecon du test du 07/11/2026 : dans la charge utile Tally, `label` n'est PAS
l'intitule affiche de la question mais le NOM INTERNE du champ. Ce script lit
donc `payload.name` dans le schema du formulaire publie, jamais le titre.
"""
import io, json, re, sys

NB = " "
blocs = json.load(io.open("tally_blocs.json", encoding="utf-8"))

NOMS = set()
OPTIONS = {}      # nom interne -> [textes d'options]
for b in blocs:
    p = b.get("payload") or {}
    if b.get("type") == "HIDDEN_FIELDS":
        for hf in (p.get("hiddenFields") or []):
            NOMS.add(hf.get("name"))
        continue
    n = p.get("name")
    if not n:
        continue
    NOMS.add(n)
    if b.get("type") in ("MULTIPLE_CHOICE_OPTION", "CHECKBOX"):
        OPTIONS.setdefault(n, []).append(p.get("text", ""))

for n in NOMS:
    assert NB not in n, "insecable dans un nom interne : %r" % n

F = "1.data.fields"


def N(nom):
    assert nom in NOMS, "nom interne inconnu : %r" % nom
    assert '"' not in nom
    return nom


def txt(nom):
    return '{{get(map(%s; "value"; "label"; "%s"); 1)}}' % (F, N(nom))


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


CLIENTS = "3ddfde7b-711d-4824-8cd7-c7f893911dc0"
ANIMAUX = "de7e8e55-5bb7-4521-8aa1-eab0d6431faf"
DOSSIERS = "6cfb904e-03b1-44b6-8f18-0be7f2656ddf"
CNX_NOTION = 8104817
CNX_GMAIL = 10587186     # connexion « google » : ActionSendEmail refuse « google-email »
HOOK = 4058042

courriel = txt("email")
prenom = '{{ifempty(%s; %s)}}' % (txt("first_name")[2:-2], txt("Prénom du client")[2:-2])

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

analyse = "\n\n".join([
    "Motif détaillé : " + txt("Motif détaillé"),
    "Dernier épisode : " + txt("Dernier épisode"),
    "Déjà essayé : " + txt("Déjà essayé"),
    "Objectif : " + txt("Objectif"),
])

DIGEST = [
    ("Ancienneté", choix("Ancienneté")),
    ("Fréquence", choix("Fréquence")),
    ("Évolution", choix("Évolution")),
    ("Réaction du maître", txt("Réaction du maître")),
    ("Habitat", choix("Habitat")),
    ("Environnement", choix("Environnement")),
    ("Adultes au foyer", txt("Adultes au foyer")),
    ("Autres animaux", txt("Autres animaux")),
    ("Cohérence du foyer", txt("Cohérence du foyer")),
    ("Temps seul", choix("Temps seul")),
    ("Sorties", txt("Sorties")),
    ("Alimentation", txt("Alimentation")),
    ("Sommeil", txt("Sommeil")),
    ("Santé connue", txt("Santé connue")),
    ("Traitements", txt("Traitements")),
    ("Compléments", txt("Compléments")),
    ("Autre professionnel", txt("Autre professionnel")),
    ("Quatre premiers mois", txt("Quatre premiers mois")),
]
brut = "\n".join("%s : %s" % (k, v) for k, v in DIGEST)

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
                               "name": "Ce client existe-t-il déjà ?"}}},
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
                  {"key": "N° de commande", "type": "rich_text", "value": txt("order_id")},
                  {"key": "Statut", "type": "select", "value": "Questionnaire reçu"},
                  {"key": "Date de réception", "type": "date",
                   "date": {"start": "{{now}}", "includeTime": True}},
                  {"key": "Liens vidéo", "type": "url", "value": txt("Lien vidéo")},
                  {"key": "Vétérinaire consulté", "type": "select",
                   "value": veto},
                  {"key": "Niveau de risque", "type": "select", "value": risque},
                  {"key": "Analyse", "type": "rich_text", "value": analyse},
                  {"key": "Réponses brutes", "type": "rich_text", "value": brut},
                  {"key": "Animal", "type": "relation", "value": ["{{6.id}}"]},
              ]},
              "metadata": {"designer": {"x": 1500, "y": 150,
                                        "name": "Créer le Dossier"}}},
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
                             {"key": "Consentement cas pédagogique", "type": "checkbox",
                              "value": coche("Consentement cas pédagogique")},
                             {"key": "Date consentement cas", "type": "date",
                              "date": {"start": coche_date("Consentement cas pédagogique"),
                                       "includeTime": True}},
                         ]},
              "metadata": {"designer": {"x": 1800, "y": 150,
                                        "name": "Rafraîchir la fiche Client"}}},
             {"id": 9, "module": "google-email:ActionSendEmail", "version": 1,
              "parameters": {"account": CNX_GMAIL},
              "mapper": {
                  "to": ["contact@gusetfrost.fr"],
                  "subject": "Nouveau questionnaire : " + txt("Nom du chien") +
                             " (" + prenom + ")",
                  "html": ("<p>Un questionnaire du Programme vient d'arriver.</p>"
                           "<p><strong>Motif :</strong> " + txt("Motif") + "</p>"
                           "<p><strong>Vétérinaire :</strong> " + veto +
                           "<br><strong>Niveau de risque :</strong> " + risque + "</p>"
                           "<p><strong>Vidéo :</strong> " + txt("Lien vidéo") +
                           "</p><p><strong>N° de commande :</strong> " +
                           txt("order_id") + "</p>"
                           "<p>Dossier Notion : https://www.notion.so/"
                           "{{replace(7.id; \"-\"; \"\")}}</p>"
                           "<p style=\"color:#888;font-size:13px\">Délai contractuel"
                           " : 7 jours ouvrés. Objectif : 72 h.</p>"),
                  "attachments": [],
              },
              "metadata": {"designer": {"x": 2100, "y": 150,
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
assert NB not in s, "une insecable s'est glissee dans le blueprint"
io.open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(s)
print("blueprint v2 ecrit : %d octets, 0 insecable" % len(s))
