# -*- coding: utf-8 -*-
"""Genere la fiche produit du Programme du Foyer Apaise.

Toutes les espaces insecables sont ecrites   en echappement ASCII :
jamais de litteral invisible (voir memoire nbsp-heredoc-perdu).
"""
import json, io, re, sys

NB = " "

TITRE = "Le Programme du Foyer Apaisé" + NB + ": 90" + NB + "jours d'accompagnement"

SEO_TITRE = "Le Programme du Foyer Apaisé" + NB + ": 90" + NB + "jours pour un chien serein"

SEO_DESC = (
    "Un bilan écrit à son nom, l'analyse d'une vidéo de votre chien, "
    "vos questions par e-mail pendant 90" + NB + "jours, un rendez-vous mensuel en visio "
    "et le coffret d'accessoires. L'accompagnement d'un comportementaliste, "
    "pas un guide de plus."
)

H = []
a = H.append

a("<p>Vous avez déjà essayé. Un tapis, un diffuseur, plus de balades, "
  "peut-être même une consultation. Pendant trois jours, ça allait mieux. "
  "Puis la semaine a repris, un soir vous avez sauté l'étape, le lendemain aussi, "
  "et au bout de dix jours l'objet était au fond du placard.</p>")

a("<p><strong>Ce n'est pas un manque de volonté.</strong> C'est ce qui arrive à "
  "presque tout le monde quand personne ne vient voir où vous en êtes.</p>")

a("<h3>Une séance donne des consignes. Elle ne vous accompagne pas.</h3>")

a("<p>Un rendez-vous, c'est un bilan et des consignes justes. Le vrai travail commence "
  "en sortant" + NB + ": le jour 4, quand votre chien régresse et que vous ne savez pas si "
  "c'est normal. Le jour 9, quand vous n'avez plus le temps. Le jour 21, quand ça marche "
  "et que vous ne savez pas quoi faire ensuite. Personne n'est là à ces moments "
  "précis, et ce sont les seuls qui comptent.</p>")

a("<p>Le Programme du Foyer Apaisé est construit autour de cela" + NB + ": non pas vous "
  "expliquer quoi faire, mais faire en sorte que vous le fassiez pendant 90" + NB + "jours.</p>")

a("<h3>Ce que comprend le Programme</h3>")
a("<ul>")
a("<li><strong>Votre bilan écrit, à son nom.</strong> Après votre commande, vous "
  "recevez un questionnaire détaillé sur votre chien, votre foyer et les situations "
  "qui déclenchent le stress. Votre bilan écrit vous est adressé habituellement "
  "sous 72" + NB + "h, et au plus tard sous 7" + NB + "jours ouvrés à compter de la "
  "réception de votre questionnaire.</li>")
a("<li><strong>L'analyse d'une vidéo de votre chien.</strong> Vous filmez deux minutes de "
  "la situation qui coince" + NB + ": le départ, l'orage, le retour du soir. Je la regarde "
  "et je vous réponds par écrit.</li>")
a("<li><strong>Vos questions par e-mail, illimitées, pendant toute la durée.</strong> "
  "Réponse sous 48" + NB + "h ouvrées. C'est la partie qui empêche l'abandon.</li>")
a("<li><strong>Un rendez-vous en visioconférence chaque mois.</strong> 45" + NB + "minutes, "
  "toutes vos questions, trois mois durant.</li>")
a("<li><strong>La méthode écrite.</strong> Le manuel du Foyer Apaisé, 30 recettes "
  "classées par besoin et par moment, la feuille de route jour par jour, et le carnet de "
  "bord qui vous fait tenir.</li>")
a("<li><strong>Le coffret d'accessoires</strong>, expédié chez vous" + NB + ": tapis de "
  "léchage, tapis de fouille, jouet de mastication. Le léchage est l'outil du calme, "
  "la fouille celui de la dépense mentale.</li>")
a("</ul>")

a("<p>L'accompagnement court sur 90" + NB + "jours à compter de l'envoi de votre bilan. "
  "Vous disposez de six mois après votre commande pour renvoyer votre questionnaire" + NB +
  ": rien ne se périme si vous démarrez plus tard.</p>")

a("<h3>Le coffret</h3>")
a("<p>Le coffret est fourni pour l'exécution du Programme. Il n'est ni vendu "
  "séparément, ni facturé à part. Son expédition suit notre Politique "
  "d'expédition, et le délai de votre bilan ne dépend pas de l'arrivée du "
  "colis" + NB + ": vous commencez à la lecture de votre bilan, pas à la "
  "réception du paquet.</p>")

a("<h3>Ce que le même parcours coûte en cabinet</h3>")
a("<ul>")
a("<li>Un bilan comportemental d'une heure" + NB + ": environ 110" + NB + "€</li>")
a("<li>Deux séances de suivi" + NB + ": environ 145" + NB + "€</li>")
a("</ul>")
a("<p>Soit environ 255" + NB + "€, sans les outils, sans les recettes, et sans personne "
  "entre les rendez-vous. Le Programme est à 179" + NB + "€.</p>")

a("<h3>La garantie</h3>")
a("<p>Si, après avoir suivi le Programme et rempli votre carnet de bord pendant "
  "trente (30) jours consécutifs, vous ne constatez aucune évolution, le prix vous est "
  "intégralement remboursé sur simple demande adressée à "
  "contact@gusetfrost.fr, accompagnée du carnet renseigné. Vous conservez alors le "
  "coffret et l'ensemble des supports remis. Cette garantie ne restreint ni votre droit de "
  "rétractation, ni les garanties légales.</p>")

a("<h3>Qui vous accompagne</h3>")
a("<p>En France, le métier de comportementaliste n'est pas réglementé" + NB + ": "
  "n'importe qui peut s'en réclamer. C'est pour cela que nous vous disons exactement qui "
  "accompagne votre chien. Vingt ans de pratique, majoritairement en cabinet, au Canada, à "
  "recevoir des chiens et des chats. Ces dernières années, une concentration sur un "
  "seul sujet" + NB + ": la gestion du stress chez le chien. ACACED.</p>")
a("<p>Gus était un chien. Frost était un chat. C'est leur nom qui est sur cette "
  "boutique.</p>")

a("<h3>Le cadre</h3>")
a("<p>Le Programme est un accompagnement éducatif et comportemental. Il ne constitue ni un "
  "diagnostic, ni une prescription, ni un traitement, et il ne se substitue pas à une "
  "consultation vétérinaire" + NB + ": certains troubles du comportement ont une "
  "origine médicale. Pour une anxiété sévère, voyez votre "
  "vétérinaire avant toute chose.</p>")
a("<p>L'évolution d'un chien dépend de la mise en œuvre effective des "
  "recommandations. Aucun résultat comportemental ne peut être garanti.</p>")

a("<h3>Après votre commande</h3>")
a("<p>Vous recevez par e-mail le lien vers votre questionnaire comportemental. Vous le "
  "remplissez à votre rythme, vous y joignez votre vidéo, et votre bilan suit. "
  "Le coffret part de son côté.</p>")
a("<p>Avant de payer, vous confirmez que l'accompagnement peut démarrer sans attendre le "
  "délai de rétractation de 14" + NB + "jours" + NB + ": c'est ce qui permet de vous "
  "envoyer votre questionnaire tout de suite. Vous gardez la possibilité de vous "
  "rétracter, seule la part déjà fournie restant due, et la garantie de "
  "30" + NB + "jours ci-dessus va plus loin.</p>")

HTML = "\n".join(H)

# ---- garde-fous -------------------------------------------------------------
def controle(nom, texte):
    pb = []
    for mauvais in ("—", "–"):
        if mauvais in texte:
            pb.append("tiret cadratin/demi-cadratin")
    for mot in ("protocole", "plan écrit", "diplômé", "certifié",
                "agréé", "expert", "362", "n'hésitez pas",
                "incontournable", "véritable", "boule de poils",
                "quatre pattes"):
        if mot.lower() in texte.lower():
            pb.append("mot banni : " + mot)
    # connecteurs bannis : seulement en tete de phrase
    for conn in ("En effet", "De plus", "Par ailleurs", "En outre", "En conclusion",
                 "En résumé", "Et "):
        if re.search(r"(?:^|[.!?>]\s*)" + re.escape(conn), texte):
            pb.append("connecteur banni en tete de phrase : " + conn)
    # insecables : avant : ; ! ? et devant l'euro / les unites
    for m in re.finditer(r" (?=[:;!?»])", texte):
        pb.append("espace ordinaire avant un signe double, pos " + str(m.start()))
    for m in re.finditer(r"(?<=\d) (?=[€%])", texte):
        pb.append("espace ordinaire devant une unite, pos " + str(m.start()))
    for m in re.finditer(r"(?<=\d) (?=h\b|jours|minutes)", texte):
        pb.append("espace ordinaire entre nombre et unite, pos " + str(m.start()))
    print(("OK   " if not pb else "ECHEC") + " " + nom)
    for p in sorted(set(pb)):
        print("      - " + p)
    return not pb

ok = all([controle("titre", TITRE), controle("seo titre", SEO_TITRE),
          controle("seo desc", SEO_DESC), controle("description", HTML)])

# obligations contractuelles
oblig = {
    "delai 72 h + 7 jours dans la meme phrase":
        "72" + NB + "h, et au plus tard sous 7" + NB + "jours ouvrés" in HTML,
    "trente (30) jours consecutifs": "trente (30) jours consécutifs" in HTML,
    "integralement rembourse": "intégralement remboursé" in HTML,
    "demande a contact@gusetfrost.fr": "contact@gusetfrost.fr" in HTML,
    "carnet renseigne": "carnet renseigné" in HTML,
    "conserve le coffret et les supports": "conservez alors le coffret" in HTML,
    "non-substitution veterinaire": "ne se substitue pas" in HTML,
    "Politique d'expedition citee": "Politique d'expédition" in HTML,
    "delai independant du colis": "ne dépend pas de l'arrivée du colis" in HTML,
    "duree 90 jours": "90" + NB + "jours" in HTML,
    "bilan ecrit": "bilan écrit" in HTML,
    "analyse video": "analyse d'une vidéo" in HTML,
    "echanges e-mail": "questions par e-mail" in HTML,
    "visio mensuelle": "visioconférence chaque mois" in HTML,
    "supports numeriques": "manuel du Foyer Apaisé" in HTML,
    "coffret": "coffret d'accessoires" in HTML,
    "ancrage 255 sans prix barre": "255" + NB + "€" in HTML,
}
print()
for k, v in oblig.items():
    print(("OK   " if v else "MANQUE ") + k)
ok = ok and all(oblig.values())

with io.open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    json.dump({"titre": TITRE, "seoTitre": SEO_TITRE, "seoDesc": SEO_DESC,
               "html": HTML}, f, ensure_ascii=False, indent=1)

print()
print("description : " + str(len(HTML)) + " caracteres, " +
      str(HTML.count(NB)) + " insecables")
print("VERDICT : " + ("pret" if ok else "A CORRIGER"))
