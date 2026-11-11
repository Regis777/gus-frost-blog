# -*- coding: utf-8 -*-
"""Blueprint Make v4 : webhook Tally -> Notion (Clients / Animaux / Dossiers) -> e-mail.

Quatre lecons payees comptant.

1. 07/11/2026 — dans la charge utile Tally, `label` n'est PAS l'intitule affiche
   de la question mais le NOM INTERNE du champ. Ce script lit donc
   `payload.name` dans le schema du formulaire publie, jamais le titre.

2. 08/11/2026 — le module Notion de Make remplace tout saut de ligne par la
   chaine litterale « <br /> » dans une propriete texte. Les deux textes longs
   passent donc par le CORPS de la page Dossier, en vrais blocs Notion, et
   `controle_sauts_de_ligne` interdit tout saut de ligne dans le blueprint.

3. 11/11/2026 — **un module ne peut pas lire la sortie d'un module situe dans
   une AUTRE route du routeur.** `ifempty(get(map(3.array; "id"); 1); 5.id)` ne
   valait donc rien des que la route 1 venait de creer le client : la chaine
   echouait a la fiche Animal, et seule la presence prealable du client la
   faisait passer. Remede : apres le routeur, la route 2 **recherche a nouveau**
   la fiche, qui existe desormais dans les deux cas. Meme remede pour l'animal.
   Regle a garder : aucune formule ne reference un module d'une autre route.

4. 11/11/2026 — dedoublonnage des Animaux : un animal est identifie par son nom
   ET son client (`relation:contains`), jamais par son nom seul, sinon deux
   clients ayant un chien du meme nom partageraient la fiche.
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
    return '{{toString(ifempty(%s; "non renseigné"))}}' % inner


# ---------------------------------------------------------------- blocs Notion

def h3(titre):
    return {"type": "heading_3",
            "heading_3": {"text": [{"type": "text", "text": {"content": titre}}]}}


def ligne(etiquette, nom):
    # L'espace de separation est un fragment STATIQUE : un contenu reduit a
    # « espace + formule » est ramene par Make a la valeur brute.
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

# Les deux identifiants dont tout depend. Ils viennent d'une recherche faite
# DANS la meme route : jamais d'un module d'une autre route (lecon 3).
CLIENT = "{{11.id}}"
ANIMAL = "{{15.id}}"

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


def cnx():
    return {"__IMTCONN__": CNX_NOTION}


def place(x, y, nom):
    return {"designer": {"x": x, "y": y, "name": nom}}


def cherche_client(idm, x, y, nom):
    return {"id": idm, "module": "notion:searchObjects1", "version": 1,
            "parameters": cnx(),
            "mapper": {"limit": 1, "select": "data_source_item",
                       "data_source": CLIENTS,
                       "filter": [[{"a": "E-mail |&*^%$#@| email",
                                    "o": "email:equals", "b": courriel}]]},
            "metadata": place(x, y, nom)}


def cherche_animal(idm, x, y, nom):
    """Un animal = un nom ET un client. Le nom seul confondrait deux foyers."""
    return {"id": idm, "module": "notion:searchObjects1", "version": 1,
            "parameters": cnx(),
            "mapper": {"limit": 1, "select": "data_source_item",
                       "data_source": ANIMAUX,
                       "filter": [[{"a": "Nom de l'animal |&*^%$#@| title",
                                    "o": "text:equals",
                                    "b": txt("Nom du chien")},
                                   {"a": "Client |&*^%$#@| relation",
                                    "o": "relation:contains", "b": CLIENT}]]},
            "metadata": place(x, y, nom)}


def agrege(idm, source, x, y, nom):
    return {"id": idm, "module": "builtin:BasicAggregator", "version": 1,
            "parameters": {"feeder": source},
            "mapper": {"id": "{{%d.id}}" % source},
            "metadata": place(x, y, nom)}


def rien_trouve(idm):
    return [[{"a": '{{get(map(%d.array; "id"); 1)}}' % idm, "o": "notexist"}]]


# Le webhook est une URL publique : on ne traite que ce qui a la forme d'une
# soumission du bon formulaire. Cela n'arrete pas un faussaire qui connaitrait
# l'URL (il faudrait pour cela un secret partage avec Tally), mais cela ecarte
# tout ce qui arrive par erreur ou au hasard.
authentique = {"name": "Une soumission de CE formulaire",
               "conditions": [[{"a": "{{1.eventType}}", "o": "text:equal",
                                "b": "FORM_RESPONSE"},
                               {"a": "{{1.data.formId}}", "o": "text:equal",
                                "b": "pbgAZZ"}]]}

porte = cherche_client(2, 300, 0, "Ce client existe-t-il déjà" + NB + "?")
porte["filter"] = authentique

flow = [
    {"id": 1, "module": "gateway:CustomWebHook", "version": 1,
     "parameters": {"hook": HOOK, "maxResults": 1}, "mapper": {},
     "metadata": place(0, 0, "Questionnaire Tally reçu")},
    porte,
    agrege(3, 2, 600, 0, "Toujours un bundle, même si personne"),
    {"id": 4, "module": "builtin:BasicRouter", "version": 1, "mapper": None,
     "metadata": {"designer": {"x": 900, "y": 0}},
     "routes": [
         {"flow": [
             {"id": 5, "module": "notion:createDataSourceItem", "version": 1,
              "parameters": cnx(),
              "filter": {"name": "Client inconnu", "conditions": rien_trouve(3)},
              "mapper": {"select": "map", "data_source": CLIENTS, "fields": [
                  {"key": "Prénom", "type": "title", "value": prenom},
                  {"key": "E-mail", "type": "email", "value": courriel},
                  {"key": "Statut", "type": "select", "value": "Bilan en cours"},
                  {"key": "Dernier contact", "type": "date",
                   "date": {"start": "{{now}}", "includeTime": True}},
              ]},
              "metadata": place(1200, -150, "Créer la fiche Client")},
         ]},
         {"flow": [
             cherche_client(11, 1200, 150, "Le client, créé ou retrouvé"),
             cherche_animal(12, 1500, 150, "Cet animal existe-t-il déjà" + NB + "?"),
             agrege(13, 12, 1800, 150, "Toujours un bundle, même si personne"),
             {"id": 14, "module": "builtin:BasicRouter", "version": 1,
              "mapper": None, "metadata": {"designer": {"x": 2100, "y": 150}},
              "routes": [
                  {"flow": [
                      {"id": 6, "module": "notion:createDataSourceItem",
                       "version": 1, "parameters": cnx(),
                       "filter": {"name": "Animal inconnu",
                                  "conditions": rien_trouve(13)},
                       "mapper": {"select": "map", "data_source": ANIMAUX,
                                  "fields": [
                           {"key": "Nom de l'animal", "type": "title",
                            "value": txt("Nom du chien")},
                           {"key": "Espèce", "type": "select", "value": "Chien"},
                           {"key": "Sexe", "type": "select", "value": sexe},
                           {"key": "Stérilisé", "type": "checkbox",
                            "value": sterilise},
                           {"key": "Âge à la stérilisation",
                            "type": "rich_text",
                            "value": txt("Âge à la stérilisation")},
                           {"key": "Race ou croisement", "type": "rich_text",
                            "value": txt("Race")},
                           {"key": "Âge", "type": "rich_text",
                            "value": txt("Âge")},
                           {"key": "Poids (kg)", "type": "number",
                            "value": txt("Poids")},
                           {"key": "Provenance", "type": "select",
                            "value": provenance},
                           {"key": "Âge à l'arrivée (semaines)",
                            "type": "number",
                            "value": txt("Âge à l'arrivée (semaines)")},
                           {"key": "Date d'arrivée au foyer", "type": "date",
                            "date": {"start": txt("Date d'arrivée"),
                                     "includeTime": False}},
                           {"key": "Client", "type": "relation",
                            "value": [CLIENT]},
                       ]},
                       "metadata": place(2400, 0, "Créer la fiche Animal")},
                  ]},
                  {"flow": [
                      cherche_animal(15, 2400, 300,
                                     "L'animal, créé ou retrouvé"),
                      {"id": 7, "module": "notion:createDataSourceItem",
                       "version": 1, "parameters": cnx(),
                       "mapper": {"select": "map", "data_source": DOSSIERS,
                                  "fields": [
                           {"key": "Motif", "type": "title",
                            "value": txt("Motif")},
                           {"key": "N° de commande", "type": "rich_text",
                            "value": txt("order_id")},
                           {"key": "Statut", "type": "select",
                            "value": "Questionnaire reçu"},
                           {"key": "Date de réception", "type": "date",
                            "date": {"start": "{{now}}", "includeTime": True}},
                           {"key": "Liens vidéo", "type": "url",
                            "value": txt("Lien vidéo")},
                           {"key": "Vétérinaire consulté",
                            "type": "select", "value": veto},
                           {"key": "Niveau de risque", "type": "select",
                            "value": risque},
                           {"key": "Animal", "type": "relation",
                            "value": [ANIMAL]},
                       ]},
                       "metadata": place(2700, 300, "Créer le Dossier")},
                      {"id": 10, "module": "notion:appendADatabaseItemContent",
                       "version": 1, "parameters": cnx(),
                       "mapper": {"select": "map", "page": "{{7.id}}",
                                  "objects": CORPS},
                       "metadata": place(
                           3000, 300,
                           "Écrire le questionnaire dans le Dossier")},
                      {"id": 8, "module": "notion:updateADatabaseItem",
                       "version": 1, "parameters": cnx(),
                       "mapper": {"page": CLIENT, "select": "map",
                                  "updateBy": "data_source",
                                  "data_source": CLIENTS, "fields": [
                           {"key": "Statut", "type": "select",
                            "value": "Bilan en cours"},
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
                       "metadata": place(3300, 300,
                                         "Rafraîchir la fiche Client")},
                      {"id": 9, "module": "google-email:ActionSendEmail",
                       "version": 1, "parameters": {"account": CNX_GMAIL},
                       "mapper": {
                           "to": ["contact@gusetfrost.fr"],
                           "subject": "Nouveau questionnaire" + NB + ": " +
                                      txt("Nom du chien") + " (" + prenom + ")",
                           "html": (
                               "<p>Un questionnaire du Programme vient"
                               " d'arriver.</p>"
                               "<p><strong>Motif" + NB + ":</strong> " +
                               txt("Motif") + "</p>"
                               "<p><strong>Vétérinaire" + NB +
                               ":</strong> " + veto +
                               "<br><strong>Niveau de risque" + NB +
                               ":</strong> " + risque + "</p>"
                               "<p><strong>Vidéo" + NB + ":</strong> " +
                               txt("Lien vidéo") +
                               "</p><p><strong>N° de commande" + NB +
                               ":</strong> " + txt("order_id") + "</p>"
                               "<p>Dossier Notion" + NB +
                               ": https://www.notion.so/"
                               "{{replace(7.id; \"-\"; \"\")}}</p>"
                               "<p style=\"color:#888;font-size:13px\">"
                               "Délai contractuel" + NB + ": 7" + NB +
                               "jours ouvrés. Objectif" + NB + ": 72" +
                               NB + "h.</p>"),
                           "attachments": [],
                       },
                       "metadata": place(3600, 300,
                                         "Prévenir Régis")},
                  ]},
              ]},
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


def controle_routes(noeud, visibles=None, chemin="racine"):
    """Aucune formule ne doit referencer un module d'une autre route (lecon 3).

    Make ne resout pas ces references : elles valent du vide, en silence.
    """
    visibles = set(visibles or ())
    for m in noeud:
        propre = json.dumps({k: v for k, v in m.items() if k != "routes"},
                            ensure_ascii=False)
        refs = set()
        for expr in re.findall(r"\{\{(.*?)\}\}", propre):
            refs.update(int(x) for x in re.findall(r"(?<![\w.])(\d+)\.", expr))
        for ref in sorted(refs):
            assert ref in visibles or ref == m["id"], \
                "module %d (%s) reference le module %d, hors de sa route" % (
                    m["id"], chemin, ref)
        visibles.add(m["id"])
        for i, r in enumerate(m.get("routes") or []):
            controle_routes(r["flow"], visibles, "%s/route %d" % (chemin, i + 1))


controle_sauts_de_ligne(s)
controle_insecables(s)
controle_etiquettes(s)
controle_routes(flow)

io.open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(s)
print("blueprint v4 ecrit : %d octets" % len(s))
print("corps du Dossier : %d blocs" % len(CORPS))
print("insecables : %d" % s.count(NB))
