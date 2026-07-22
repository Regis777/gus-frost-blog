# Prompt de démarrage — Cluster C6 (Chiot, les premiers mois)

> À coller tel quel dans une nouvelle conversation de ce projet.

---

Nouveau cluster à produire : **C6 — Chiot, les premiers mois**.
On reprend exactement le même pipeline et les mêmes standards que le cluster C5 (repas/gamelle), qui vient d'être finalisé dans ce projet.

## CONTEXTE
- Projet Gus & Frost, boutique premium FR sur Shopify, blog « Le Journal », modèle SEO en silos.
- Clusters existants : C1 anxiété de séparation, C2 peurs/bruits, C3 chien calme et serein au quotidien, C4 langage corporel, C5 repas/gamelle.
- Modèle : Opus 4.8 pour la rédaction.

## PÉRIMÈTRE ET FRONTIÈRE DE C6 (important)
- Cible : le chiot, de 0 à 6 mois. Fort levier d'acquisition.
- EXCLURE la solitude et l'anxiété de séparation du chiot : déjà traité en C1. On y renvoie par un lien, on ne réécrit pas l'angle.
- Territoire ouvert à privilégier : arrivée à la maison et préparation, premières nuits, dentition (pont naturel vers le tapis de léchage congelé de C5), fenêtre de socialisation, mordillements, propreté (totalement libre, gros volume), gestion de l'énergie du chiot, besoins de mastication, premiers soins/manipulation.
- Vérifier chaque satellite contre C2 (éducation/marche générales restent hors chiot) et C3 (calme) pour éviter tout doublon.

## STANDARDS À RESPECTER (identiques à C5)
- Structure silo : 1 pilier (~3 500-4 000 mots) + 12 satellites (~2 500 mots), en fragments HTML autonomes compatibles pipeline Shopify.
- Chaque fichier : bloc `<style>` de prévisualisation avec le brand refonte (Montserrat Bold + Lora ; #314431 forêt, #a8ff6a lime, #efe7da crème, #c16b47 terracotta, #9dae8b sauge), retirable au profit de theme/gf-article.css.
- Typographie FR : espaces insécables avant : ; ! ? et dans « » ; pas de tiret cadratin ; pas de « et » en début de phrase ; encadrés CONSEIL et CAS PRATIQUE sans icônes.
- Ton : expert mais rassurant, problème vers solution, jamais culpabilisant ni médicalement prescriptif ; produits introduits comme conséquence d'un besoin, jamais en accroche ; tout ce qui est médical renvoyé au vétérinaire.
- Liens internes en `PLACEHOLDER_slug` (intra et inter-silos), à résoudre en passe de maillage.
- Nommage fichiers : `AAAA-MM-JJ_TYPE_slug_v1.html` (TYPE = PILIER ou SATxx).
- Manifest : le schéma inclut désormais une colonne `excerpt` (résumé de blog Shopify affiché sur la page du blog et l'accueil), placée juste après `meta_description`. Rédiger un `excerpt` pour chaque article de C6 (une à deux phrases d'accroche, distinctes de la méta-description, ton problème vers solution).
- Cluster_tag proposé : `cluster-chiot` (à confirmer). Numérotation dog-only : C6.
- Références vérifiées contre sources primaires avant inclusion ; signaler toute nouvelle référence pour validation.
- Fichier de prompts d'images consolidé au fil de l'eau, numéroté séquentiellement sur tout le cluster (1.png, 2.png…) pour le renommage automatisé ; situations réelles, aucun texte incrusté (textes d'infographie ajoutés dans Canva) ; objectif pédagogique + alt SEO FR + rationale par image.
- Autonome d'abord : toujours sauvegarder le fichier HTML complet avant tout post-traitement.

## SLUGS INTER-SILOS DISPONIBLES (pour câbler le maillage)

**C1 — `cluster-anxiete-separation`** (dossier `cluster-1-anxiete-separation`)
Pilier : anxiete-separation-chien
Satellites : anxiete-separation-chien-comprendre · camera-radio-pheromones-chien · chien-anxieux-absence-que-faire · combien-temps-chien-seul · erreurs-anxiete-separation-chien · espace-rassurant-chien-seul · habituer-chien-rester-seul · jouets-occupation-chien-seul · prevenir-anxiete-separation-chiot · signes-anxiete-separation-chien
→ Cibles clés pour C6 (solitude du chiot) : **prevenir-anxiete-separation-chiot**, **combien-temps-chien-seul**.

**C2 — `cluster-peur-bruit`** (dossier `cluster-2-peur-bruit`)
Pilier : chien-peur-bruit-phobie
Satellites : chien-petards-14-juillet · chien-peur-feux-artifice · chien-peur-inconnus-autres-chiens · chien-peur-orage · chien-peureux-en-ville · crise-panique-sonore-chien · desensibiliser-chien-bruits · erreurs-chien-qui-a-peur · gilet-anti-stress-couverture-ponderee-chien · pourquoi-chien-peur-bruits

**C3 — `cluster-calme-serenite`** (dossier `cluster-3-calme-serenite`)
Pilier : chien-calme-serenite-quotidien
Satellites : apprendre-le-calme-chien · chien-excitation-retrouvailles-invites · chien-hyperactif-trop-excite · environnement-apaisant-chien-maison · erreurs-chien-agite · mastication-lechage-chien · promenade-depense-chien-equilibre · routine-rythme-quotidien-chien · sommeil-du-chien · stimulation-mentale-chien

**C4 — `cluster-langage-corporel`** (dossier `cluster-4-langage-corporel`)
Pilier : langage-corporel-chien
Satellites : signaux-apaisement-chien · queue-chien-signification · baillement-chien-stress · chien-leche-truffe-babines · oreilles-chien-emotions · oeil-de-baleine-chien · postures-stress-chien · chien-s-ebroue-signal · echelle-stress-chien-morsure · haletement-tremblements-chien-stress · observer-chien-carnet-signaux · idees-recues-langage-canin

**C5 — `cluster-repas-gamelle`** (dossier `cluster-5-repas-gamelle`, slugs figés, merge manifest en attente)
Pilier : repas-du-chien
Satellites : chien-mange-trop-vite · gamelle-anti-glouton-chien · ralentir-repas-chien · nourrir-chien-sans-gamelle · recettes-tapis-lechage-chien · chien-gourmand-toujours-faim · chien-quemande-table · repas-plusieurs-chiens · combien-repas-chien-par-jour · chien-ne-mange-pas-gamelle · transition-alimentaire-chien · choisir-gamelle-chien
→ Cible clé pour C6 (dentition) : **recettes-tapis-lechage-chien**.

## DÉMARRAGE
Commence par me proposer l'ARBORESCENCE COMPLÈTE de C6 (pilier + 12 satellites : slugs, titres, meta_title, meta_description, excerpt, tags), au format mergeable dans manifest.csv, plus le plan de maillage intra-silo et les ponts inter-silos (dont le renvoi vers C1 pour la solitude, et vers C5 pour la dentition). On valide l'arborescence avant toute rédaction.
