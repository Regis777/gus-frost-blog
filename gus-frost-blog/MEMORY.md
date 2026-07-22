# MEMORY.md — Index mémoire du projet blog SEO Gus & Frost

> Index central du projet de blogs SEO en silos de Gus & Frost (boutique premium francophone Shopify, accessoires chiens et chats). Point d'entrée pour reprendre le travail dans une nouvelle session. Deux blogs coexistent dans ce dépôt : **CHAT** (handle `chats`) et **CHIEN** (handle par défaut). Cet index se concentre sur le **blog CHAT** ; les clusters chien vivent dans le même dépôt (dossiers `C7-…` à `C15-…`, `NP1/2/3`, fichiers `*_PASSAGE-RELAI_claude-code.md`).

## 1. Comment reprendre le travail (à lire en premier)

1. Lire ce fichier, puis les **standards permanents** (section 3) et la **mémoire du dernier cluster produit** (section 4).
2. Dépôt : `C:\Users\regis\Google Drive\Gus et Frost\BLOGS_Gus et Frost\`. La production vit dans `Blogs cowork\`. **Note : ce dossier s'appelait auparavant `gus-frost-blog` ; il a été renommé `BLOGS_Gus et Frost`.** Google Drive peut encore afficher un dossier fantôme `gus-frost-blog` vide/inaccessible : l'ignorer et toujours pointer sur `BLOGS_Gus et Frost`.
3. Gabarit de référence le plus abouti : le dernier cluster chat produit (voir section 4). Réutiliser ses `gf_shared.py`, `ck.py`, `mkfinal.py`.
4. **Piège environnement (impératif)** : travailler dans le workspace cloud (`/tmp/…`), jamais en édition in-place sur le mount Drive (désync connue qui sert des fichiers tronqués). Ne rapatrier sur le Drive qu'à la fin, via `SendUserFile` → `device_commit_files`.
5. Chaque nouveau cluster suit le cycle : arborescence → bibliographie vérifiée → pilier → satellites (sous-agents) → build + `ck.py` 0 erreur → prompts d'images → maillage → **`manifest_CH<N>_rows.csv` (méta SEO, voir §2)** → commit Drive → mise à jour de cette mémoire.

> ⚠️ **Le `manifest_CH<N>_rows.csv` est un livrable de rédaction, pas de déploiement.** Il a été oublié sur CH1, CH2, CH6, CH10 et sur les 7 clusters non déployés — soit 11 clusters sur 12. Un cluster sans ce fichier **ne peut pas être ingéré** : c'est lui qui porte le `title`, le `meta_title`, la `meta_description`, l'`excerpt` et les `tags`, c'est-à-dire **tout le SEO on-page**. Aucun cluster n'est « terminé » sans lui.

## 2. Conventions techniques (chat)

- **Numérotation** : chat = `cluster_num` = numéro du label CH au plan CHAT (indépendant de l'ordre de production). Voir `Blogs cowork\Gus-Frost_STANDARD_numerotation-clusters.md`.
- `cluster_tag` suffixé `-chat` ; dossier `articles/cluster-{num}-{tag-court}-chat` ; blog handle `chats` (`/blogs/chats/{slug}`) ; slugs suffixés `-chat`. **Manifest chat séparé** du chien.
- CTA unique `gf-cta` → `/collections/chat` (via `gf_shared.cta()`). Aucun `/products/` dans le corps.
- Gabarit CSS : `gf-article`, `gf-conseil`, `gf-cas`, `gf-faq`, `gf-imgph`, `gf-encadre-titre`.
- Règles `ck.py` (0 erreur exigé) : corps `bodies/<slug>.html` de `<article class="gf-article">` à la fin du `</div>` de la FAQ (pas de `</article>`, pas de `gf-cta` : `mkfinal.py` les ajoute) ; 1 `id="faq"` ; FAQ à 5 `<h3>` ; 1 `gf-cta` ; 1 seul `href="/collections/chat"` ; 0 `/products/` ; nb de `<figure>` = nb de marqueurs `Image N`.
- Interdits : tiret cadratin `—`, phrase commençant par « Et », insécables manuelles (le build normalise), et formules bannies : « En effet », « De plus », « véritable », « incontournable », « N'hésitez pas ».
- Longueurs : pilier ~3 500 mots (voire plus), satellites ~2 500 mots. Images : pilier 3, chaque satellite 2, marqueurs `Image N` uniques et séquentiels sur tout le cluster.
- **Méta SEO — `manifest_CH<N>_rows.csv`, à la racine du dossier Cowork du cluster.** 14 colonnes : `cluster_num, cluster_tag, type, slug, parent_pilier_slug, title, meta_title, meta_description, excerpt, tags, file, prompts_file, links_to_resolve, images_to_resolve`. Modèle de référence : `Blogs cowork\CH7-griffades\manifest_CH7_rows.csv`.
  - `meta_title` **48-62 caractères**, suffixe « | Gus & Frost » compris.
  - `meta_description` **160-195 c.**, factuelle, annonce le contenu réel de l'article (pas une paraphrase du titre).
  - `excerpt` **100-145 c.**, 2ᵉ personne, souvent « <constat>. Voici <ce que l'article apporte>. »
  - `tags` = `<cluster_tag>` + 2 mots-clés en kebab-case.
  - Insécables : écrire en espaces normales, la normalisation est faite au montage (ne jamais taper U+00A0 à la main).
  - Les champs mécaniques (`type`, `file`, `parent_pilier_slug`, `links_to_resolve`, `images_to_resolve`) se recalculent depuis les fragments : ne pas les saisir à la main.

## 3. Standards permanents (dans `Blogs cowork\`)

- `Gus-Frost_STANDARD_references-verifiees.md` — toute donnée passe par une source primaire vérifiée, graduée A→X ; formulation calibrée sur la preuve ; livrable `C{num}_bibliographie.md` par cluster avant rédaction.
- `Gus-Frost_STANDARD_numerotation-clusters.md` — règle de numérotation chat/chien.
- `Gus-Frost_plan_clusters_CHAT.md.docx` — plan des 12 clusters chat (CH1-CH12), périmètres et frontières.

## 4. Registre des clusters CHAT

Ordre de production à ce jour : **CH1 → CH7 → CH2 → CH6 → CH10**, puis CH3, CH4, CH5, CH8, CH9, CH11, CH12.

**Le blog chat est COMPLET et intégralement déployé en brouillon depuis le 22/07/2026.** Les 12 clusters, soit **156 articles**, 324 images sur le CDN, **1 063 liens internes**, 156 cibles, **aucun lien orphelin, aucun article non cité, aucun lien mort**. Vérifié via l'API Shopify : 156 articles, **0 publié**, tous avec image à la une et excerpt. Rien n'est publié — Régis relit avant publication.

| Label | Cluster | Statut | Mémoire / cadrage |
|---|---|---|---|
| **CH1** | Le langage du chat | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH1_arborescence.md` |
| **CH2** | Le chat serein au quotidien | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH2_arborescence.md`, `CH2_bibliographie.md`, `CH2-serenite\` |
| **CH6** | Litière, propreté et marquage | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH6_arborescence.md`, `CH6_bibliographie.md`, `CH6-litiere\gus-frost-ch6-litiere.md` |
| **CH7** | Griffades et griffoir | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH7_arborescence.md`, `CH7_bibliographie.md`, `CH7-griffades\` |
| **CH3** | Le chat craintif | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH3_arborescence.md`, `CH3-…\` |
| **CH4** | Le chat d'intérieur : ennui, solitude, absence | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH4_arborescence.md`, `CH4-…\` |
| **CH5** | Le repas du chat | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH5_arborescence.md`, `CH5-…\` |
| **CH8** | Territoire, enrichissement et jeu | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH8_arborescence.md`, `CH8-…\` |
| **CH9** | Le chaton, les premiers mois | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH9_arborescence.md`, `CH9-…\` |
| **CH10** | Cohabitation, agression et vie sociale | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH10_arborescence.md`, `CH10_bibliographie.md`, `CH10-cohabitation\gus-frost-ch10-cohabitation.md` |
| **CH11** | Les grandes transitions de vie | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH11_arborescence.md`, `CH11-…\` |
| **CH12** | Le chat senior | **Déployé (brouillons)** 22/07/2026 | `Gus-Frost_CH12_arborescence.md`, `CH12-…\` |

### Slugs des clusters produits (cibles de maillage résolubles)

**CH1 — langage** (pilier `langage-du-chat`) — liste COMPLÈTE des 12 satellites, relevée sur les fichiers déployés : `queue-chat-signification`, `oreilles-chat-emotions`, `clignement-lent-chat`, `ronronnement-chat-signification`, `miaulements-chat-comprendre`, `vibrisses-moustaches-chat`, `pupilles-yeux-chat`, `postures-corps-chat`, `signes-agacement-inconfort-chat`, `marquage-facial-frottements-chat`, `observer-chat-carnet-signaux`, `idees-recues-langage-chat`.
> ⚠ Correction du 22/07/2026 : `agression-par-caresses-chat` et `gamelle-vibrisses-chat` figuraient ici par erreur — **ils n'ont jamais été produits**. CH10 s'y est fié et a posé 2 renvois morts (neutralisés au déploiement). Le sujet « agression par caresses » est couvert par `signes-agacement-inconfort-chat`. Ne jamais citer un slug qui n'est pas dans un fichier livré.

**CH2 — sérénité** (pilier `chat-serein-quotidien`) : `routine-chat-previsibilite`, `sommeil-chat`, `importance-jeu-chat`, `stress-chat-signes-causes`, `reduire-stress-ambiant-chat`, `ressources-chat-regle-nplus1`, `securite-refuges-chat`, `environnement-apaisant-chat`, `pheromones-chat-efficacite`, `plusieurs-chats-harmonie-quotidien`, `signes-chat-bien-etre`, `idees-recues-bien-etre-chat`.

**CH6 — litière** (pilier `litiere-proprete-chat`) : `choisir-litiere-chat`, `choisir-bac-litiere-chat`, `ou-placer-litiere-chat`, `combien-bacs-litiere-chat`, `entretenir-litiere-chat`, `chat-fait-hors-litiere`, `marquage-urinaire-chat`, `elimination-inappropriee-chat`, `nettoyer-odeurs-urine-chat`, `litiere-chaton-apprentissage`, `litiere-chat-age-senior`, `idees-recues-litiere-chat`.

**CH7 — griffades** (pilier `pourquoi-chat-griffe`) : `choisir-griffoir-chat`, `griffoir-vertical-ou-horizontal-chat`, `ou-placer-griffoir-chat`, `entretenir-changer-griffoir-chat`, `proteger-meubles-griffades-chat`, `griffades-marquage-chat`, `degriffage-chat` (liste principale ; autorité : `Gus-Frost_CH7_arborescence.md`).

**CH10 — cohabitation** (pilier `cohabitation-chats-vie-sociale`) : `presenter-deux-chats`, `reprendre-presentation-chats-ratee`, `conflits-entre-chats-foyer`, `agression-redirigee-chat`, `seuil-tolerance-agression-chat`, `cohabitation-chat-chien`, `chat-et-arrivee-bebe`, `amenager-ressources-tensions-chats`, `jeu-brutal-jeune-chat`, `peur-agression-defensive-chat`, `consulter-comportementaliste-chat`, `idees-recues-agression-cohabitation-chat` (autorité : `Gus-Frost_CH10_arborescence.md`).

## 5. CH10 — dernier cluster produit (résumé)

13 articles (pilier 3 747 mots ck ; satellites 3 168-4 019 ck), 13/13 `ck.py` 0 erreur. Cluster le plus sensible du blog : **option prudente** (comprendre, sécuriser, séparer, renvoyer au vétérinaire comportementaliste ; aucune rééducation autonome d'une agression installée). Deux mécanismes tenus partout où l'agression est approchée : **« médical d'abord »** et **le point de bascule**. Socle : sociabilité facultative du chat (Crowell-Davis 2004), besoins environnementaux / cinq piliers (AAFP-ISFM Ellis 2013), lien douleur/comportement (Mills 2020), agression dirigée (Amat & Manteca 2019), ressources > nombre (Finka 2022), chat-chien (Feuerstein & Terkel 2008 ; Kinsman 2022), toxoplasmose (CDC). 93 liens internes, 28 cibles. Prénoms CAS à exclure : Vadim, Filou, Zélie, Gribouille, Tibère, Réglisse, Ficelle, Sésame, Lupin, Kiro, Naïa, Marcel, Anouk. Détail complet : `CH10-cohabitation\gus-frost-ch10-cohabitation.md`.

**CH10 — déployé le 22/07/2026** en même temps que CH1, CH2, CH6 et CH7 : 13 brouillons sur le blog `chats`, 27 images sur le CDN, 93 liens internes résolus. Il restait 2 renvois vers `agression-par-caresses-chat` (slug inexistant, cf. §4) : convertis en prose, tracés dans `articles/cluster-10-cohabitation-chat/_BACKFILL_liens.md`.

### Pipeline à deux blogs (levé le 22/07/2026)

Le pré-requis en suspens depuis CH1 est traité : `publish.py` porte une table `BLOGS` qui associe à chaque blog son manifest et sa collection de CTA (`chiens` → `manifest.csv` + `/collections/stress` ; `chats` → `manifest_chat.csv` + `/collections/chat`). `ingest_cluster.py`, `deploy_cluster.py`, `check_cluster.py` et `unlink_placeholders.py` prennent tous `--blog chats` ; sans ce drapeau le comportement chien est strictement inchangé.

- **`--tag` est obligatoire** dès qu'un `cluster_num` porte plusieurs dossiers : `deploy_cluster.py` refuse désormais de tourner sans (C10 chien « transitions » vs CH10 chat « cohabitation-chat »).
- `ingest_cluster.py --blog chats` accepte la nomenclature Cowork `CH<N>_…` en plus de `C<N>_…`.
- `scripts/unlink_placeholders.py` convertit en prose les renvois dont la cible n'existe pas encore, et écrit un `_BACKFILL_liens.md` dans le dossier du cluster : c'est la liste de ce qu'il faudra recâbler à la sortie des clusters cibles.
- **Piège** : `--bake` réécrit le fragment avec le corps résolu. Un `--dry-run` relancé APRÈS un `--bake` signale « images 0!=N » sur tout le cluster ; c'est un artefact, pas un défaut. Le contrôle qui fait foi est celui d'avant le bake, ou l'API Shopify.
- **Méta SEO** : les dossiers Cowork chat ne livraient pas de `manifest_CH<N>_rows.csv` (sauf CH7). Les 4 fichiers manquants ont été rédigés le 22/07/2026 (format : `meta_title` 48-62 c. suffixé « | Gus & Frost », `meta_description` 160-195 c., `excerpt` 100-145 c. à la 2ᵉ personne, insécables normalisées par script). **À produire par la session Cowork pour les prochains clusters.**

## 5 bis. Maillage : back-fill SOLDÉ le 22/07/2026

Les 12 clusters étant tous ingérés, tous les renvois se résolvent. Les 11 liens de CH1 et les 2 de CH10 neutralisés en cours de route ont été recâblés, **d'après le TEXTE du lien et non le slug supposé** : les slugs cités par les rédacteurs (`agression-par-caresses-chat`, `chat-peureux-se-cache`, `chaton-socialisation`, `gamelle-vibrisses-chat`, `territoire-chat-amenagement`) n'ont jamais existé, mais chaque texte désignait sans ambiguïté un pilier réel. Un même slug supposé pouvait couvrir deux sujets différents (`territoire-chat-amenagement` servait aussi pour la litière) : **toujours trancher sur le texte promis au lecteur.**

Outils : `scripts/unlink_placeholders.py` (neutralise + écrit `_BACKFILL_liens.md`) et `scripts/relink_backfill.py` (recâble, mapping par texte ou par cible). Piège : un cluster déjà déployé a ses fragments « bakés » ; pour le redéployer, **le ré-ingérer d'abord** depuis le dossier Cowork, sinon le contrôle d'images échoue.

## 5 ter. SEO — audit de cannibalisation (22/07/2026)

`Blogs cowork\AUDIT_cannibalisation_blog-chat.md`. Sur les 12 870 paires possibles : **6 signalements, 1 réel, 1 modéré, 2 faibles, 2 faux positifs** — l'architecture en silos a tenu. Les deux premiers sont **corrigés et redéployés** : le duo « chat et bébé » (CH10 recentré sur sécurité/toxoplasmose, CH11 sur le calendrier de préparation, liens croisés posés) et le trio « routine et prévisibilité » (CH2 redescend désormais vers ses variantes CH3 et CH4).

**Pas de données de volume** : l'abonnement Ahrefs n'inclut pas l'API (« Insufficient plan ») et l'offre est disproportionnée pour le projet (119 €/mois mini). Décision du 22/07/2026 : **on s'en passe**. La bonne séquence est publier → laisser Google indexer → optimiser sur Search Console, qui est gratuit et donne les requêtes réelles. GSC n'a aucune donnée tant que la boutique est sous mot de passe.

**Reste à traiter** : **35 renvois obsolètes dans 25 articles** (« nous consacrerons », « que nous préparons », « à paraître ») promettent des guides qui existent désormais. À convertir en liens.

## 6. Back-fill de maillage en attente

À câbler à la sortie des clusters concernés (les articles déjà produits contiennent des renvois en prose SANS `PLACEHOLDER_` vers les clusters non produits) :
- **Vers CH6** depuis CH1 (`marquage-facial-frottements-chat`→`marquage-urinaire-chat`), CH2 (`ressources-chat-regle-nplus1`→`combien-bacs-litiere-chat`), CH7 (`griffades-marquage-chat`→`marquage-urinaire-chat`).
- **Depuis CH6** vers CH5 (repas/eau), CH8 (territoire), CH9 (chaton), CH10 (conflits), CH12 (senior) à leur sortie.
- **Vers CH10** depuis CH1 (`agression-par-caresses-chat`/`signes-agacement-inconfort-chat`→`seuil-tolerance-agression-chat`), CH2 (`plusieurs-chats-harmonie-quotidien`/`ressources-chat-regle-nplus1`→`amenager-ressources-tensions-chats`, `conflits-entre-chats-foyer`), CH6 (`marquage-urinaire-chat`→`conflits-entre-chats-foyer`).
- **Depuis CH10** (renvois EN PROSE à convertir à leur sortie) vers CH3 (peur, depuis `peur-agression-defensive-chat`, `reprendre-presentation-chats-ratee`), CH8 (territoire, depuis `amenager-ressources-tensions-chats`, `conflits-entre-chats-foyer`, `cohabitation-chat-chien`, `presenter-deux-chats`), CH9 (chaton/jeu, depuis `jeu-brutal-jeune-chat`), CH11 (transitions/bébé, depuis `chat-et-arrivee-bebe`, `cohabitation-chat-chien`, `presenter-deux-chats`).

---

*Index mis à jour le 22/07/2026 (déploiement des 5 clusters chat en brouillon). Créé le 18/07/2026 (fin de CH6), mis à jour le 21/07/2026 à la fin de la production de CH10. À tenir à jour à chaque cluster : ajouter la ligne au registre (section 4), les slugs, et le résumé du dernier produit (section 5).*
