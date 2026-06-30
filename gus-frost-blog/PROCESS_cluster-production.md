# Brief de lancement de cluster — Gus & Frost

**Comment l'utiliser :** ouvre une nouvelle conversation **dans le même Projet**, colle ce texte en entier, puis écris « on attaque le cluster ». Ce document est la **source de vérité de la recette** — il prime sur ce que la mémoire aura retenu ou non. L'autre source de vérité, ce sont les livrables : le dépôt GitHub `Regis777/gus-frost-blog` (projet rangé dans le sous-dossier `gus-frost-blog/`), les fichiers de prompts, et le calendrier Notion.

---

# PARTIE A — Recette permanente (vaut pour tout cluster)

## Marque & identité

- Gus & Frost : boutique Shopify premium chien/chat, contenu **en français**.  
- Identité visuelle : **vert profond \#314431** \+ **beige clair \#EFE7DA** \+ beige/taupe/crème/bois clair.  
- Images : **photo lifestyle réaliste**, jamais cartoon, **aucun texte ni logo dans l'image**.  
- Règle produit absolue : les produits **aident à apaiser / à occuper**, ils ne « soignent » ni ne « guérissent » **jamais**.

## Voix « anti-IA » (stricte)

- Entrée par une **scène concrète**, pas une généralité.  
- **Faits \> promesses** : chiffres prudents, cas pratiques, mini-protocoles, tableaux.  
- **Zéro emoji.** Pas de clichés. **Bannir** : « En effet », « De plus », « véritable », « incontournable », « N'hésitez pas ».  
- Ton **expert mais rassurant**, jamais culpabilisant ni prescriptif médical.  
- Encadrés **CONSEIL** et **CAS PRATIQUE** **sans icône**.  
- Conclusion \= **« Par où commencer »** avec **UNE seule action**.  
- Méthode : si un 1er jet est court, **étoffer** (jamais raccourcir) avec de la vraie valeur ; recompter les mots via script.

## Architecture SEO (silo)

- **1 pilier \+ N satellites**, tous **interreliés**. (Clusters 1-3 : 10 satellites chacun. Le nombre est à confirmer au démarrage.)  
- Le pilier est le hub ; chaque satellite vise une **requête longue traîne**.

## Format HTML (gabarit « v2 »)

- **1 fichier HTML autonome par article**, avec `<style>` scopé `.gf-article` et les classes `.gf-conseil`, `.gf-cta`, `.gf-satellites`, `.gf-pilier`, `.gf-faq`.  
- Métadonnées en commentaire d'en-tête : SLUG URL, META TITLE, META DESC, MOTS-CLÉS, TAGS, TYPE.  
- Polices Crimson Pro \+ DM Sans ; palette vert/or ; FAQ \+ CTA de conversion.  
- Images : balises `<img id="..." src="REMPLACER_xxx.jpg" width=... height=... alt="...">`.  
- **Prompts d'images dans un fichier `.md` séparé par article** (`..._PROMPTS-IMAGES.md`), chaque prompt relié à l'`id` de son image. Pour chaque image : description de création IA, objectif pédagogique, alt SEO, justification de placement.  
- Tailles images : **hero 1600×900**, **corps 1080×1080**, **infographie 1080×1350**.  
- Images **stratégiques** (une toutes les 2-3 sections), scènes de vie réelles. Texte des infographies ajouté **sous Canva**, pas dans l'image IA.

## Maillage interne

- Liens internes via placeholders `PLACEHOLDER_...` (Claude Code les résoudra) : satellites, pilier, `PLACEHOLDER_collection-...`, `PLACEHOLDER_produit-...`.  
- Liens **inline** contextuels \= à conserver. Le **bloc de navigation du bas** sera retiré au nettoyage (remplacé par la section dynamique du thème).

## Conventions de nommage

- Fichiers de prod : `AAAA-MM-JJ_TYPE_slug_v1.html` (+ `..._PROMPTS-IMAGES.md`).  
- Fichiers nettoyés (dépôt) : `{slug}.html` dans `articles/cluster-N-theme/`.  
- Image de blog : le fichier porte le **nom du placeholder sans le préfixe `REMPLACER_`**.  
- Épingles Pinterest : `PIN_C{N}-{PIL|SNN}_{NN}_{slug-court}.png`.

## Pipeline du cluster (dans l'ordre)

1. **Production des articles** (pilier \+ satellites), voix \+ format ci-dessus, livrés en local dans `/mnt/user-data/outputs/` \+ `present_files` (**pas** Google Drive).  
2. **Fichiers de prompts d'images** (un par article).  
3. **Nettoyage HTML** → version dépôt (style retiré → `gf-article.css` ; bloc liens bas retiré).  
4. **Check-list d'images du cluster** générée automatiquement (`images-prompts/cluster-N/CHECKLIST_images.md`)  
   + ligne ajoutée à `CHECKLIST_images_INDEX.md`, **sans toucher aux autres clusters**.  
5. **Mise à jour du `manifest.csv`** (1 ligne/article : cluster, type, slug, parent pilier, titres, meta, tags, chemins).  
6. **Upload GitHub** (par toi ou Claude Code).  
7. **Épingles Pinterest** insérées dans Notion (voir ci-dessous).

## Notion (calendrier éditorial)

- Base existante, `data_source_id = dd95def5-119b-409f-a85e-95592f46a792`. **Demander le feu vert avant toute modif de schéma/données.**  
- Propriétés déjà ajoutées : `Lien destination` (URL), `Texte alternatif`, `Tableau Pinterest`. La colonne `ID Make` est **conservée**.  
- Épingles : **piliers 6-8**, **satellites 4-5**, format 1000×1500. Statut **Brouillon**, `Cible = Pinterest`, board par cluster. Lien destination \= **slug provisoire** (préfixer du domaine une fois le blog en ligne).  
- **Ne pas publier d'épingles avant la mise en ligne du blog** (sinon liens 404).

## Gestion de session

- Un cluster entier \= grosse session. Tout produire **dans une seule conversation** ; utiliser des **formats condensés** si on approche des limites, pour terminer le cluster.

---

# PARTIE B — Cluster du moment : **Chats — « griffades contrôlées »**

C'est le **premier cluster chat** (les clusters 1-3 étaient chien). **Toutes les images doivent montrer des CHATS**, jamais de chien. Même voix, même identité visuelle.

## Sujet

Apprendre au chat à faire ses griffes au bon endroit : comprendre le besoin de griffer, choisir et placer un griffoir, rediriger depuis le canapé/les meubles, prévenir chez le chaton.

## Repères de numérotation (proposés)

- Dossier : `articles/cluster-4-griffades-chat/`  
- `cluster_tag` : `cluster-griffades-chat` · placeholders satellites : `c4-sat-0N`  
- Pinterest : préfixe `PIN_C4-...` · board Notion : **« Griffades du chat »**  
- Produits (à venir, contenu-first) : `PLACEHOLDER_produit-griffoir`, `PLACEHOLDER_collection-griffades-chat` (les produits chat ne sont pas encore lancés → CTA présents mais à résoudre plus tard ; ne rien surpromettre).

## Plan proposé (à confirmer / ajuster au démarrage)

**Pilier :** Comprendre et canaliser les griffades du chat — le guide complet.

**Satellites (proposition, \~10) :**

1. Pourquoi mon chat fait ses griffes (sur le canapé, partout) — le besoin derrière le geste  
2. Comment choisir un bon griffoir (vertical/horizontal, sisal, hauteur, stabilité)  
3. Où placer le griffoir pour qu'il l'utilise vraiment  
4. Empêcher le chat de griffer le canapé et les meubles (rediriger en douceur)  
5. Apprendre au chaton à faire ses griffes au bon endroit (prévention)  
6. Mon chat ignore son griffoir : pourquoi et que faire  
7. Arbre à chat ou griffoir : que choisir  
8. Protéger meubles, murs et tapis pendant l'apprentissage  
9. Les erreurs à éviter (crier, punir… et pourquoi le dégriffage est à proscrire)  
10. Griffades excessives et stress : quand c'est un signe de mal-être

## Décisions à acter au démarrage

1. **Nombre de satellites** (garder 10 comme les clusters chien, ou ajuster ?).  
2. **Validation du plan** ci-dessus (sujets, ordre, angles).  
3. **Slugs définitifs** de chaque article (je les proposerai pour validation).  
4. **Volume d'épingles Pinterest** (mêmes fourchettes : pilier 6-8, satellites 4-5).

## Première action attendue de moi (dans le nouveau fil)

Confirmer le plan \+ les décisions ci-dessus **avant** de produire en masse, puis lancer la production en suivant le pipeline (Partie A), avec **check-list d'images du cluster incluse**.  
