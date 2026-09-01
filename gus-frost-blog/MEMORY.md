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
  - `meta_title` **35 à 45 caractères, SANS suffixe de marque** : le thème ajoute déjà « – Gus et Frost » (15 c.). Corrigé le 22/07/2026 après réécriture de 160 titres trop longs. Vérifier l'unicité contre les 420 titres existants.
  - `meta_description` **120 à 155 caractères**, factuelle, annonce le contenu réel de l'article (pas une paraphrase du titre). Au-delà de 160, Google tronque. Corrigé le 22/07/2026.
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

**Le blog chat est COMPLET et EN LIGNE depuis le 22/07/2026** (publié sur décision de Régis ; la boutique reste sous mot de passe encore ~1 semaine, donc rien n'est public tant que le mot de passe n'est pas levé). Les 12 clusters, soit **156 articles**, 324 images sur le CDN, **1 250 liens internes** (1 063 avant la conversion des renvois obsolètes du 22/07/2026, cf. §5 ter), 156 cibles, **aucun lien orphelin, aucun article non cité, aucun lien mort**. Vérifié via l'API Shopify. **Au 23/07/2026, le blog compte 158 articles, TOUS PUBLIÉS** (les 2 neufs `deuil-perte-chat-cote-maitre` et `toilettage-brossage-chat-adulte` publiés sur décision de Régis, cf. §5 quater), tous avec image à la une et excerpt. **1 265 liens internes, 0 lien mort, 0 orphelin, 0 PLACEHOLDER**. Page hub `/pages/conseils-chats` publiée, régénérée à **158 articles**.

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

**CH7 — griffades** (pilier `pourquoi-chat-griffe`) — liste COMPLÈTE des 12 satellites, relevée sur les fichiers déployés le 01/08/2026 : `choisir-griffoir-chat`, `griffoir-vertical-ou-horizontal-chat`, `ou-placer-griffoir-chat`, `entretenir-changer-griffoir-chat`, `proteger-meubles-griffades-chat`, `griffades-marquage-chat`, `degriffage-chat`, `griffes-du-chat-entretien`, `griffades-chaton-apprentissage`, `chat-n-utilise-pas-griffoir`, `chat-griffe-canape-meubles`, `arbre-a-chat-ou-griffoir`.

> ⚠ Correction du 01/08/2026 : les 5 derniers manquaient. `griffes-du-chat-entretien` couvre la coupe des griffes, la griffe incarnée, le chat âgé ET une section « Manipuler les pattes sans conflit » : **tout cluster traitant la manipulation ou le toilettage doit y renvoyer et ne jamais traiter la griffe.**

**CH10 — cohabitation** (pilier `cohabitation-chats-vie-sociale`) : `presenter-deux-chats`, `reprendre-presentation-chats-ratee`, `conflits-entre-chats-foyer`, `agression-redirigee-chat`, `seuil-tolerance-agression-chat`, `cohabitation-chat-chien`, `chat-et-arrivee-bebe`, `amenager-ressources-tensions-chats`, `jeu-brutal-jeune-chat`, `peur-agression-defensive-chat`, `consulter-comportementaliste-chat`, `idees-recues-agression-cohabitation-chat` (autorité : `Gus-Frost_CH10_arborescence.md`).

> ⚠ **Chantier en cours (01/08/2026) — slugs CH9 instables.** Le cluster CH9 chaton est absorbé dans le super-silo Chaton (CH19, six sous-clusters : accueil, propreté, socialisation, jeu et mordillements, alimentation, santé). Ses 13 slugs sont susceptibles d'être renommés, redistribués ou fusionnés. Tout cluster produit avant l'achèvement de CH19 doit **signaler ses liens vers CH9** dans son fichier de maillage, pour revérification à la migration. Voir `Blogs cowork\PROMPT_demarrage_CH19_super-silo-chaton.md`.

## 5. CH10 — dernier cluster produit (résumé)

13 articles (pilier 3 747 mots ck ; satellites 3 168-4 019 ck), 13/13 `ck.py` 0 erreur. Cluster le plus sensible du blog : **option prudente** (comprendre, sécuriser, séparer, renvoyer au vétérinaire comportementaliste ; aucune rééducation autonome d'une agression installée). Deux mécanismes tenus partout où l'agression est approchée : **« médical d'abord »** et **le point de bascule**. Socle : sociabilité facultative du chat (Crowell-Davis 2004), besoins environnementaux / cinq piliers (AAFP-ISFM Ellis 2013), lien douleur/comportement (Mills 2020), agression dirigée (Amat & Manteca 2019), ressources > nombre (Finka 2022), chat-chien (Feuerstein & Terkel 2008 ; Kinsman 2022), toxoplasmose (CDC). 93 liens internes, 28 cibles. Prénoms CAS à exclure : Vadim, Filou, Zélie, Gribouille, Tibère, Réglisse, Ficelle, Sésame, Lupin, Kiro, Naïa, Marcel, Anouk. Détail complet : `CH10-cohabitation\gus-frost-ch10-cohabitation.md`.

**CH10 — déployé le 22/07/2026** en même temps que CH1, CH2, CH6 et CH7 : 13 brouillons sur le blog `chats`, 27 images sur le CDN, 93 liens internes résolus. Il restait 2 renvois vers `agression-par-caresses-chat` (slug inexistant, cf. §4) : convertis en prose, tracés dans `articles/cluster-10-cohabitation-chat/_BACKFILL_liens.md`.

### Pipeline à deux blogs (levé le 22/07/2026)

Le pré-requis en suspens depuis CH1 est traité : `publish.py` porte une table `BLOGS` qui associe à chaque blog son manifest et sa collection de CTA (`chiens` → `manifest.csv` + `/collections/stress` ; `chats` → `manifest_chat.csv` + `/collections/chat`). `ingest_cluster.py`, `deploy_cluster.py`, `check_cluster.py` et `unlink_placeholders.py` prennent tous `--blog chats` ; sans ce drapeau le comportement chien est strictement inchangé.

- **`--tag` est obligatoire** dès qu'un `cluster_num` porte plusieurs dossiers : `deploy_cluster.py` refuse désormais de tourner sans (C10 chien « transitions » vs CH10 chat « cohabitation-chat »).
- `ingest_cluster.py --blog chats` accepte la nomenclature Cowork `CH<N>_…` en plus de `C<N>_…`.
- `scripts/unlink_placeholders.py` convertit en prose les renvois dont la cible n'existe pas encore, et écrit un `_BACKFILL_liens.md` dans le dossier du cluster : c'est la liste de ce qu'il faudra recâbler à la sortie des clusters cibles.
- **Piège** : `--bake` réécrit le fragment avec le corps résolu. Un `--dry-run` relancé APRÈS un `--bake` signale « images 0!=N » sur tout le cluster ; c'est un artefact, pas un défaut. Le contrôle qui fait foi est celui d'avant le bake, ou l'API Shopify.
- **Méta SEO** : les dossiers Cowork chat ne livraient pas de `manifest_CH<N>_rows.csv` (sauf CH7). Les 4 fichiers manquants ont été rédigés le 22/07/2026, initialement à l'ancienne norme (`meta_title` 48-62 c. suffixé « | Gus & Frost », `meta_description` 160-195 c.) **depuis abandonnée** — voir §2 et « 5 quater — SEO technique » pour les specs en vigueur : `meta_title` **35 à 45 c., SANS suffixe de marque**, `meta_description` **120 à 155 c.**, `excerpt` 100-145 c. à la 2ᵉ personne, insécables normalisées par script. **À produire par la session Cowork pour les prochains clusters, à la norme actuelle.**

## 5 bis. Maillage : back-fill SOLDÉ le 22/07/2026

Les 12 clusters étant tous ingérés, tous les renvois se résolvent. Les 11 liens de CH1 et les 2 de CH10 neutralisés en cours de route ont été recâblés, **d'après le TEXTE du lien et non le slug supposé** : les slugs cités par les rédacteurs (`agression-par-caresses-chat`, `chat-peureux-se-cache`, `chaton-socialisation`, `gamelle-vibrisses-chat`, `territoire-chat-amenagement`) n'ont jamais existé, mais chaque texte désignait sans ambiguïté un pilier réel. Un même slug supposé pouvait couvrir deux sujets différents (`territoire-chat-amenagement` servait aussi pour la litière) : **toujours trancher sur le texte promis au lecteur.**

Outils : `scripts/unlink_placeholders.py` (neutralise + écrit `_BACKFILL_liens.md`) et `scripts/relink_backfill.py` (recâble, mapping par texte ou par cible). Piège : un cluster déjà déployé a ses fragments « bakés » ; pour le redéployer, **le ré-ingérer d'abord** depuis le dossier Cowork, sinon le contrôle d'images échoue.

## 5 ter. SEO — audit de cannibalisation (22/07/2026)

`Blogs cowork\AUDIT_cannibalisation_blog-chat.md`. Sur les 12 870 paires possibles : **6 signalements, 1 réel, 1 modéré, 2 faibles, 2 faux positifs** — l'architecture en silos a tenu. Les deux premiers sont **corrigés et redéployés** : le duo « chat et bébé » (CH10 recentré sur sécurité/toxoplasmose, CH11 sur le calendrier de préparation, liens croisés posés) et le trio « routine et prévisibilité » (CH2 redescend désormais vers ses variantes CH3 et CH4).

**Pas de données de volume** : l'abonnement Ahrefs n'inclut pas l'API (« Insufficient plan ») et l'offre est disproportionnée pour le projet (119 €/mois mini). Décision du 22/07/2026 : **on s'en passe**. La bonne séquence est publier → laisser Google indexer → optimiser sur Search Console, qui est gratuit et donne les requêtes réelles. GSC n'a aucune donnée tant que la boutique est sous mot de passe.

**Renvois obsolètes : SOLDÉ le 22/07/2026.** Le relevé initial (35 occurrences / 25 fichiers) était partiel : le balayage complet des fragments a trouvé **185 promesses au futur sur 12 clusters**, sous une trentaine de tournures (« nous consacrerons », « que nous préparons », « fera / feront l'objet d'un guide », « un guide à part », « nous traiterons », « vers lequel nous renverrons », « aura son propre guide »…). Toutes converties au présent avec pose d'un lien interne, d'après le SUJET ANNONCÉ et jamais d'après un slug supposé.

- 3 des 35 occurrences initiales étaient des **faux positifs** : « le chat cherche *à paraître* plus gros » (CH1). Ne pas les re-signaler.
- **Les 5 slugs fantômes ont disparu du corpus** (`agression-par-caresses-chat`, `territoire-chat-amenagement`, `chat-peureux-se-cache`, `chaton-socialisation`, `gamelle-vibrisses-chat`). `unlink_placeholders.py` répond désormais « aucun renvoi non résoluble » sur les 12 clusters : plus rien à back-filler.
- Résultat : **1 250 liens internes** (contre 1 063), 0 lien mort, 0 article orphelin, 0 `PLACEHOLDER_` non résolu, 324 images.
- 2 promesses laissées en prose sans lien, faute de cible réelle : le **deuil du côté du maître** (CH12 pilier et SAT10 ; `deuil-perte-compagnon-chat` traite du *chat* qui perd un compagnon, pas du chagrin humain) et le **toilettage du chat adulte** (CH9 SAT05 ; `toilettage-soins-chat-age` ne couvre que le senior). Ces deux trous du plan éditorial ont été **comblés le 23/07/2026** — voir §5 quater.

## 5 quater. Deux articles neufs (23/07/2026) — RÉDIGÉS, en attente d'images

Deux satellites ajoutés pour combler les trous du §5 ter, sur décision de Régis (placement et périmètre arbitrés) :

- **CH11 SAT13 `deuil-perte-chat-cote-maitre`** — le deuil *du maître* (chagrin humain, culpabilité après euthanasie, enfants et autres animaux, quand se faire aider). Pendant humain de `deuil-perte-compagnon-chat` (côté chat).
- **CH12 SAT13 `toilettage-brossage-chat-adulte`** — brossage du chat *adulte* (fréquence selon le poil, outils, nœuds, mue, réflexe vétérinaire quand le pelage change). Pendant adulte de `toilettage-soins-chat-age` (senior).

État au 23/07/2026 : fragments source écrits (~2 790 mots chacun, `check_cluster` 0 FAIL, faq 5, 6 liens), méta ajoutée à `manifest_chat.csv` (**158 lignes**) et aux `manifest_CH11/CH12_rows.csv`, prompts des images 28-29 ajoutés aux fichiers `CH11/CH12_prompts_images.md`. Liens **entrants** posés pour éviter l'orphelinat : vers le deuil depuis CH12 pilier + `confort-grand-age-fin-de-vie-chat` ; vers le toilettage depuis CH9 `manipuler-habituer-chaton`. Maillage source : 1 265 liens, 0 mort, 0 orphelin.

**DÉPLOYÉS EN BROUILLON le 23/07/2026.** Les 4 images ont été générées par Régis (fournies en 1024×572, un peu plus panoramiques que les 1536×1024 du reste du blog — cosmétique ; les 2 CH11 livrées en `.jpg`, converties en `.png` car la chaîne exige `N.png`). CH11 et CH12 ré-ingérés (14 fragments, 29 images), les 2 articles créés sur Shopify en **brouillon** (`published=false`), vérifiés : image à la une, 6 liens, 0 lien mort.

**SOLDÉ le 23/07/2026.** Les 2 articles sont publiés (`set_published.py --publish`), les 3 liens **entrants** sont en ligne (redéploiement de `chat-senior-vieillissement`, `confort-grand-age-fin-de-vie-chat`, `manipuler-habituer-chaton`, publiés donc statut préservé), et le hub est régénéré à 158. Vérifié : deuil = 2 liens entrants en ligne, toilettage = 1. Rien en attente.

**Correctif thème du 24/07/2026 (rendu des encadrés).** Le gabarit chat écrit `<p class="gf-encadre-titre">` (libellé CONSEIL/CAS) et une boîte `<div class="gf-cas">` « nue », or `gf-article.css` ne stylait ni l'un ni l'autre (il attend `.gf-conseil strong` et `.gf-box.gf-cas`, conventions chien C1–C5). Sur les 158 articles, le libellé s'affichait en texte simple et la boîte CAS PRATIQUE sans fond ni liseré. Deux règles ajoutées à `theme/gf-article.css` (scopées `.gf-article`, `:not(.gf-box)` pour ne pas toucher le chien) : `.gf-encadre-titre` (majuscules sans-serif, vert #314431 ; terracotta #c16b47 en contexte `.gf-cas`) et `.gf-cas:not(.gf-box)` (fond blanc, liseré gauche terracotta 4px). **Poussé sur le thème LIVE Dawn (id 158654333149)** via `PUT /themes/<id>/assets.json` (asset `assets/gf-article.css`), vérifié en ligne. Corrige les 158 articles d'un coup, aucun contenu redéployé. Le thème non publié « Copie de Dawn » (id 162807808221) a reçu le même `assets/gf-article.css` le 24/07/2026 (identique au live). **NE PAS chercher à « resynchroniser » le reste : c'est un bac à sable produit assumé (Régis, 24/07/2026).** La comparaison des 2 thèmes (370 assets live / 367 copie, 352 identiques) montre une divergence VOLONTAIRE : la copie porte des sections `conversion-*` + `templates/product.conversion.json` (expériences CRO page produit) que le live n'a pas ; le live porte la fonctionnalité Carnet + `gf-blog-search` que la copie n'a pas. Écraser dans un sens ou l'autre détruirait du travail. Seul `gf-article.css` devait être aligné, ce qui est fait.

Deux autres pièges rencontrés et gérés, à retenir : (1) les images fournies par Régis étaient en 1024×572 et 2 en `.jpg` — le format du blog est **1536×1024** et la chaîne exige `N.png` (converties). (2) Remplacer une image sous le **même nom de fichier** ne suffit pas : `upload_images.existing_file_url` resert l'ancienne URL CDN par nom. Pour vraiment changer une image déjà déployée, **supprimer d'abord le fichier de la bibliothèque Shopify** (mutation GraphQL `fileDelete` sur l'id `MediaImage`), puis ré-ingérer + redéployer.
- **Piège typographique découvert :** la normalisation des insécables insère une insécable avant le `;` **y compris à l'intérieur d'une entité HTML**. `&amp;` devient `&amp<U+00A0>;`, entité invalide affichée littéralement (« Gus &amp ; Frost »). Deux articles touchés et corrigés (CH3 `erreurs-idees-recues-peur-chat`, CH12 `arthrose-chat-senior`). **Contrôle à ajouter au montage : `grep -P "&[a-zA-Z]+\s+;"` doit ne rien renvoyer.**
- Corrigé au passage : 8 `href` sans préfixe `PLACEHOLDER_` dans CH2 (SAT04, SAT09), un accord fautif dans CH11 SAT03, et la colonne `links_to_resolve` du manifest, que `ingest_cluster.py` **ne recalcule pas** quand les slugs sont déjà présents (« pas de ré-append ») : elle était restée à 1 063. À recalculer à la main après toute réécriture de fragments déjà ingérés.

## 5 quater. SEO technique — corrections du 22/07/2026

**Le thème ajoute déjà « – Gus et Frost » à chaque `title`.** Ne JAMAIS suffixer le `meta_title` par « | Gus & Frost » : la marque apparaissait deux fois sur 258 articles et poussait 348 titres au-delà de 60 caractères (tronqués par Google). Suffixe retiré partout. **Les 160 titres trop longs (140 chien + 20 chat) ont été réécrits le 22/07/2026** : **0/420 dépasse 60 caractères rendus** (médiane 53 chien, 55 chat). Le `<h1>` de la page conserve le titre éditorial long — titre SERP court et H1 riche, c'est voulu et non un compromis.

**Les 85 `meta_description` chien >160 car. ont été RÉÉCRITES, pas tronquées.** Quatre tentatives de troncature automatique ont plafonné à ~75 % de coupures propres : découper une phrase française sans en comprendre le sens laisse un quart de fins bancales (« …et pourquoi bannir. »). Pour ce genre de tâche, **réécrire coûte moins cher que raffiner un algorithme.** Médiane finale : 140 chien / 137 chat, 0 au-delà de 160.

**Cible de rédaction : `meta_title` ≤ 45 caractères** (45 + 15 de suffixe = 60). Vérifier aussi l'unicité : aucun doublon de titre sur les 420. **Consigne de rédaction corrigée : `meta_title` = 35 à 45 caractères, SANS marque.**

**Insécables** : 881 champs chien ont été re-normalisés le 22/07/2026 (43 titres violaient la règle) — la normalisation n'avait jamais été appliquée aux métas, seulement aux corps.

**`meta_description` : viser 120-155 caractères** (et non 160-195). Au-delà, Google tronque. Les 156 descriptions chat ont été raccourcies à une frontière de phrase ou de proposition.

**Balisage FAQPage** : `scripts/faq_schema.py` construit le JSON-LD à partir du bloc `.gf-faq` visible (jamais de contenu réécrit — règle Google). Branché dans `deploy_cluster.py`, donc tout déploiement le régénère. **420/420 articles balisés, 2 219 questions.** Piège corrigé : délimiter le bloc en comptant les `<div>` imbriqués, pas avec une regex non gourmande — celle-ci échouait silencieusement sur 48 articles des premiers clusters.

`scripts/seo_refresh.py --blog <chiens|chats> --apply` réaligne métafields + FAQPage sur des articles DÉJÀ en ligne, sans redéployer.

**Piège majeur** : `deploy_cluster.py` forçait `published=false` à chaque écriture et **dépubliait donc en silence** tout cluster déjà publié qu'on redéployait. Corrigé le 22/07/2026 : création = brouillon, mise à jour = état conservé.

## 6. Back-fill de maillage en attente

À câbler à la sortie des clusters concernés (les articles déjà produits contiennent des renvois en prose SANS `PLACEHOLDER_` vers les clusters non produits) :
- **Vers CH6** depuis CH1 (`marquage-facial-frottements-chat`→`marquage-urinaire-chat`), CH2 (`ressources-chat-regle-nplus1`→`combien-bacs-litiere-chat`), CH7 (`griffades-marquage-chat`→`marquage-urinaire-chat`).
- **Depuis CH6** vers CH5 (repas/eau), CH8 (territoire), CH9 (chaton), CH10 (conflits), CH12 (senior) à leur sortie.
- **Vers CH10** depuis CH1 (`agression-par-caresses-chat`/`signes-agacement-inconfort-chat`→`seuil-tolerance-agression-chat`), CH2 (`plusieurs-chats-harmonie-quotidien`/`ressources-chat-regle-nplus1`→`amenager-ressources-tensions-chats`, `conflits-entre-chats-foyer`), CH6 (`marquage-urinaire-chat`→`conflits-entre-chats-foyer`).
- **Depuis CH10** (renvois EN PROSE à convertir à leur sortie) vers CH3 (peur, depuis `peur-agression-defensive-chat`, `reprendre-presentation-chats-ratee`), CH8 (territoire, depuis `amenager-ressources-tensions-chats`, `conflits-entre-chats-foyer`, `cohabitation-chat-chien`, `presenter-deux-chats`), CH9 (chaton/jeu, depuis `jeu-brutal-jeune-chat`), CH11 (transitions/bébé, depuis `chat-et-arrivee-bebe`, `cohabitation-chat-chien`, `presenter-deux-chats`).

---

*Index mis à jour le 22/07/2026 (déploiement des 5 clusters chat en brouillon). Créé le 18/07/2026 (fin de CH6), mis à jour le 21/07/2026 à la fin de la production de CH10. À tenir à jour à chaque cluster : ajouter la ligne au registre (section 4), les slugs, et le résumé du dernier produit (section 5).*

---

## 7. Super-silo Chaton CH19 — CH19-1 déployé (01/09/2026)

L'absorption de CH9 a commencé. **CH19-1 « Accueil et premiers jours » est en ligne** : 13 articles sur le blog `chats`, tag `cluster-chaton-accueil-chat`, 27 images.
- **5 slugs repris de CH9** (`accueillir-chaton`, `preparer-arrivee-chaton`, `securiser-maison-chaton`, `premiers-jours-chaton`, `erreurs-accueil-chaton`) : mis à jour en place, slugs conservés, **statut publié préservé**, aucune 301 (boutique sous mot de passe, non indexée). **CH9 tombe de 13 à 8 articles** ; le tag `cluster-chaton-chat` disparaîtra quand les 8 derniers seront redistribués vers CH19-2 à CH19-6.
- **8 articles neufs en brouillon**, en attente de relecture de Régis. Leur back-fill entrant (≥ 5 liens depuis CH1, CH2, CH4, CH10, CH11) est **volontairement différé jusqu'à leur publication** : les clusters sources sont publiés, on ne pointe pas vers des brouillons.

`manifest_chat.csv` passe de 158 à 166 lignes (8 append + 5 lignes réécrites en place). Sauvegarde : `manifest_chat.csv.bak_avant_CH19-1`.

**L'état détaillé de l'extension CH13→CH19 fait foi dans `Blogs cowork/ETAT_avancement_blog-chat.md` §7** (inventaire réel du Drive, pièges de la chaîne d'ingestion sous-cluster, correctif `faq_schema.py`).

