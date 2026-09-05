# Intégration thème — Gus & Frost (pages article du blog)

Trois opérations à faire **une seule fois** dans l'éditeur de thème Shopify
(Boutique en ligne → Thèmes → … → Modifier le code).

## 1. Charger le CSS, uniquement sur les pages article

1. Ajouter le fichier `theme/gf-article.css` dans **Assets** (`assets/gf-article.css`).
2. Dans `layout/theme.liquid`, juste avant `</head>`, charger l'asset **conditionnellement**
   pour ne l'injecter que sur le template `article` :

```liquid
{%- if template.name == 'article' -%}
  {{ 'gf-article.css' | asset_url | stylesheet_tag }}
{%- endif -%}
```

## 2. Template article : contenu SANS wrapper supplémentaire

Le corps de chaque article contient **déjà** son `<article class="gf-article">`.
Dans la section article du thème (souvent `sections/main-article.liquid`), afficher le
contenu **tel quel** — ne pas l'envelopper dans un second `.gf-article` :

```liquid
{{ article.content }}
```

> Si le thème enveloppe déjà le contenu dans un conteneur générique (`.article-template__content`,
> `.rte`, etc.), ce n'est pas grave : le souci serait un second élément **`.gf-article`**, pas un conteneur neutre.

## 3. Section « articles liés » dynamique, APRÈS le contenu

1. Ajouter `theme/related-articles.liquid` dans **Snippets** (`snippets/related-articles.liquid`).
2. Dans la section article, **après** `{{ article.content }}** :

```liquid
{{ article.content }}
{%- render 'related-articles' -%}
```

La section lit le tag `cluster-*` de l'article courant :
- sur un **pilier** → liste tous ses satellites ;
- sur un **satellite** → rappelle le pilier puis liste les satellites frères.

**Pré-requis indispensable** : chaque article doit porter les `tags` du `manifest.csv`
(cluster + `pilier`/`satellite` + thématiques). Le script `scripts/publish.py` les applique
automatiquement à la publication.

> Le style `.gf-related` est désormais inclus dans `gf-article.css` (plus besoin de copier
> le bloc commenté à la fin de `related-articles.liquid`).

---

# « Le Carnet » — l'app carnet de santé

Web app autonome : carnet de santé, rappels, budget et souvenirs, **entièrement dans le
navigateur du visiteur**. Aucun serveur, aucun compte, aucune donnée personnelle chez nous
(données JSON dans `localStorage`, photos dans `IndexedDB`). Rien à déclarer côté RGPD tant
qu'on n'ajoute pas de collecte.

## 1. Déposer les fichiers dans le thème

| Fichier du dépôt        | Emplacement dans le thème    |
| ----------------------- | ---------------------------- |
| `theme/gf-carnet.css`   | `assets/gf-carnet.css`       |
| `theme/gf-carnet.js`    | `assets/gf-carnet.js`        |
| `theme/gf-carnet.liquid`| `sections/gf-carnet.liquid`  |
| `theme/page.carnet.json`| `templates/page.carnet.json` |

Les noms comptent : la section s'appelle `gf-carnet` parce que le template la référence par
`"type": "gf-carnet"`, et le Liquid charge ses assets par `asset_url`.

## 2. Créer la page

Boutique en ligne → Pages → **Ajouter une page**
- Titre : `Le Carnet` (handle `/pages/le-carnet`)
- Modèle de thème : **page.carnet**
- Laisser le contenu vide : tout vient de la section.

Le titre et l'accroche restent modifiables dans l'éditeur de thème (section « Le Carnet »),
tout comme l'encart boutique du bas de page — pensez à y renseigner le lien du bouton.

## 3. Points de vigilance

- **Une seule section « Le Carnet » par page** : l'app est un singleton (`window.GFCarnet`).
- **Pas d'installation façon store.** Shopify n'autorise pas de service worker à la racine du
  domaine, donc pas de vraie PWA installable. La page invite à « Ajouter à l'écran d'accueil »,
  ce qui donne l'icône et l'ouverture plein écran sur iOS comme sur Android.
- **Les données vivent dans le navigateur.** Vider les données de navigation, ou passer en
  navigation privée, efface le carnet. L'app le dit et pousse à l'export ; c'est le compromis
  assumé du « sans compte ».
- **Pas de notification push** (impossible sans backend). La réponse est le bouton
  **Agenda (.ics)** : les échéances partent dans le calendrier natif, qui, lui, sonne.
- **Le partage** encode la fiche santé dans l'URL elle-même (rien n'est hébergé). Au-delà
  d'environ 6 000 caractères, l'app refuse et renvoie vers le PDF.

---

# Quiz diagnostic anxiété — l'aimant à e-mails

Équivalent maison d'un ScoreApp / Involve.me : un questionnaire qui note l'anxiété du chien,
affiche un résultat par palier (vert / orange / rouge) et capture l'e-mail dans Klaviyo en
échange du plan personnalisé. Sans app, sans abonnement.

## 1. Déposer les fichiers dans le thème

| Fichier local                  | Destination dans le thème            |
|--------------------------------|--------------------------------------|
| `theme/gf-quiz-anxiete.css`    | `assets/gf-quiz-anxiete.css`         |
| `theme/gf-quiz-anxiete.js`     | `assets/gf-quiz-anxiete.js`          |
| `theme/gf-quiz-anxiete.liquid` | `sections/gf-quiz-anxiete.liquid`    |
| `theme/page.quiz-anxiete.json` | `templates/page.quiz-anxiete.json`   |

Mêmes règles que pour le Carnet : le template référence la section par
`"type": "gf-quiz-anxiete"`, et le Liquid charge ses assets par `asset_url`. La section est
autonome — aucun patch de `layout/theme.liquid` n'est nécessaire.

## 2. Créer la page

Boutique en ligne → Pages → **Ajouter une page**
- Titre : `Quiz anxiété` (handle `/pages/quiz-anxiete`)
- Modèle de thème : **page.quiz-anxiete**
- Laisser le contenu vide : tout vient de la section.

## 3. Points de vigilance

- **Les clés Klaviyo sont dans le template**, pas dans le code : `klaviyo_cle` (clé publique
  du compte) et `klaviyo_liste` (id de la liste) sont des réglages de section, modifiables
  dans l'éditeur de thème. Le JSON versionné ici porte les valeurs de production.
- **Le code promo de fin de quiz** est un code Shopify ordinaire : il doit exister côté
  Réductions, sinon le message promet une remise qui ne s'applique pas.
- **Les 12 blocs sont l'ossature du diagnostic** (questions + paliers de résultat). En
  ajouter ou en retirer change la notation : relire le barème dans `gf-quiz-anxiete.js`
  avant de toucher aux blocs.
- **Une seule section quiz par page.**

---

# Typographie — Fraunces (titres) + Figtree (corps)

Remplace Montserrat 600 / Lora 400 **sans passer par le sélecteur de polices** du thème :
les deux familles ne sont pas dans la bibliothèque Shopify, elles sont auto-hébergées.
Déposé le 05/09/2026 sur le thème d'essai « Gus & Frost — essai typo (Fraunces + Figtree) »
(id `165258068189`, non publié). Le thème « Copie de Dawn » n'existe plus depuis la
migration Dawn 16 : ce thème d'essai est un duplicata frais du live.

## 1. Les 7 fichiers déposés dans `assets/`

| Asset | Source (licence SIL OFL) |
|---|---|
| `gf-fonts.css.liquid` | `theme/gf-fonts.css.liquid` de ce dépôt |
| `gf-fraunces-latin.woff2` (32 Ko) | Google Fonts, instance **figée** `opsz 36, wght 600, SOFT 40, WONK 0` |
| `gf-fraunces-latin-ext.woff2` (30 Ko) | idem, sous-ensemble latin-ext |
| `gf-figtree-latin.woff2` (20 Ko) | Google Fonts, **variable** `wght 400..700` |
| `gf-figtree-latin-ext.woff2` (10 Ko) | idem, latin-ext |
| `gf-figtree-italic-latin.woff2` (20 Ko) | idem, italique |
| `gf-figtree-italic-latin-ext.woff2` (10 Ko) | idem, italique latin-ext |

Pour re-télécharger les `.woff2` (curl avec un User-Agent de navigateur récent, sinon
Google sert du TTF), les URL `fonts.gstatic.com` se relisent dans ces deux feuilles :

```
https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@36,600,40,0&display=swap
https://fonts.googleapis.com/css2?family=Figtree:ital,wght@0,400..700;1,400..700&display=swap
```

> **Pourquoi une instance figée pour Fraunces ?** En variable 4 axes le fichier pèse
> 121 Ko ; figé, 32 Ko. L'axe optique est cuit à 36, bon compromis pour des titres de
> 19 à 34 px — donc `font-variation-settings` est inutile (et sans effet) dans le CSS.

## 2. Les deux patchs de `layout/theme.liquid`

Le fichier de la boutique est le Dawn v16.0.0 d'origine + la balise `yandex-verification`.
Deux modifications, toutes deux repérables par le marqueur `GF TYPO` :

1. **Les deux blocs de préchargement de police de Dawn** (`settings.type_body_font | font_url`
   et `type_header_font | font_url`) sont **remplacés** par le préchargement de
   `gf-fraunces-latin.woff2` et `gf-figtree-latin.woff2`. Sans ça, Dawn continuerait à
   télécharger Montserrat et Lora, que plus aucune règle n'utilise.
2. **Juste avant `</head>`** : `{{ 'gf-fonts.css' | asset_url | stylesheet_tag }}`.
   La position est essentielle — le `:root` de `gf-fonts.css` doit passer **après** celui
   du bloc de styles en ligne de Dawn, sinon les variables du thème gagnent.

Retour arrière : restaurer les deux blocs de préchargement d'origine (dépôt `Shopify/dawn`,
tag `v16.0.0`, `layout/theme.liquid`) et retirer la ligne `stylesheet_tag`.

## 3. Ce que le CSS bascule

`gf-fonts.css.liquid` redéfinit `--font-heading-family` / `--font-body-family` (et les
poids) : **tout le thème suit**, y compris `gf-article.css` qui consomme déjà
`var(--font-body-family)`. Il neutralise aussi les deux piles système codées en dur dans
`gf-article.css` (en-têtes de tableau, étiquette de l'encadré conseil).

Les `@font-face` Montserrat/Lora émis par le thème restent présents mais aucune règle ne
les appelle : les fichiers ne sont plus téléchargés.

## 4. Vérifié en aperçu le 05/09/2026

Sur `/blogs/chiens/ration-menagere-barf-chiot` : titres en Fraunces, corps en Figtree,
italique réelle sur les légendes de figure. **Deux fichiers de police téléchargés,
52 Ko au total** (Fraunces latin 32 Ko + Figtree latin 20 Ko), aucun appel à
`fonts.shopifycdn.com` ni à `fonts.gstatic.com`, aucun doublon de téléchargement.

## 5. Passage en live — par publication, pas par recopie

Paire validée par Régis le 05/09/2026. Le thème d'essai a été renommé
**« Gus & Frost — Dawn 16 (Fraunces + Figtree) »** (id `165258068189`) : il est publiable
tel quel.

**Pourquoi publier plutôt que rejouer les dépôts sur le thème en ligne ?** Diff md5 mené
sur `layout/*`, `sections/gf-*`, `snippets/gf-*`, `config/settings_data.json` et
`assets/gf-*` : **tous les fichiers communs sont identiques**, `settings_data.json`
compris. Le seul écart est `layout/theme.liquid` plus les 8 assets ajoutés. Publier est
donc atomique et sans état intermédiaire, là où une recopie fichier par fichier laisse le
site à moitié basculé.

**Le geste** (impossible par API — le connecteur MCP interdit `themePublish` comme
l'écriture sur le thème MAIN) : Boutique en ligne → Thèmes → « Gus & Frost — Dawn 16
(Fraunces + Figtree) » → **Publier**.

Après publication : l'ancien live `165203673309` bascule en brouillon et devient le
rollback naturel — plus récent et plus proche que `SAUVEGARDE — rollback Dawn 15`.
Ne pas laisser vivre les deux indéfiniment.

Le réglage `type_header_font` / `type_body_font` du thème peut rester sur Montserrat/Lora :
il n'est plus lu pour l'affichage, seulement pour des `@font-face` inertes.

> Note : Shopify génère automatiquement un `assets/gf-fonts.css` compilé à côté du
> `gf-fonts.css.liquid` déposé. C'est normal, et c'est ce fichier que sert le CDN.

## 6. Publié le 05/09/2026 — et un correctif en attente

Publié par Régis. Contrôles menés en ligne, anonymement puis dans un navigateur propre :
accueil, article, quiz et fiche produit en HTTP 200, aucune erreur Liquid, les 6 `.woff2`
servis en `font/woff2` et **byte-identiques** aux fichiers de référence, et l'URL du
`<link rel=preload>` strictement identique à celle du `@font-face` (un seul téléchargement).
Sur un article : Fraunces en titres, Figtree à 17 px en corps, italique réelle en légende.
**4 fichiers, 81 Ko** — contre 87 Ko et 4 fichiers pour Montserrat + Lora, sans plus aucun
appel à un hébergeur de polices tiers.

> **Piège de mesure** : un onglet qui a visité un aperçu de thème garde les entrées
> `performance` des polices de CE thème. Une mesure faite juste après fait croire que le
> live charge encore Montserrat et Lora. Toujours mesurer dans un onglet neuf.

**Correctif présent dans ce dépôt mais PAS encore en ligne** : l'ordre des `@font-face`.
Les plages `latin` et `latin-ext` se chevauchent sur U+0152-0153 (`œ`/`Œ`) et, quand deux
faces correspondent, le navigateur retient **la dernière déclarée**. La version publiée
déclare `latin` en premier : un seul « œ » (cœur, sœur, œil) fait donc télécharger les
10 Ko de `latin-ext` sur presque toutes les pages françaises. `gf-fonts.css.liquid` est
corrigé ici (latin-ext d'abord, comme le fait Google), **à redéployer** — le connecteur MCP
ne pouvant plus écrire sur le thème devenu MAIN, ça attend le prochain accès au `.env` ou
un nouveau cycle duplication/publication. Gain attendu : 10 Ko par page.

---

# « Le Club » — comptes clients et espace membre

Programme de fidélité maison, **gratuit**, sans application. Deux avantages
promis : les **guides réservés** et l'**accès anticipé**. Deux pages :

- `/pages/club` — la page publique qui présente le Club et recueille l'adhésion ;
- `/pages/espace-membre` — la page réservée, invisible tant qu'on n'est pas connecté.

## Le principe

**Être membre = avoir un compte client.** Rien d'autre. Le verrou de l'espace
membre s'appuie sur l'objet Liquid `customer`, disponible sur toute la boutique
que le magasin soit en comptes clients **classiques** ou en **nouveaux comptes
clients** : les deux pages fonctionnent dans les deux cas, sans retouche.

Le formulaire d'adhésion ne crée pas le compte (impossible sans application) :
il inscrit le profil dans Klaviyo, puis renvoie vers la création de compte
Shopify. On récupère donc l'e-mail même quand la personne abandonne à l'étape
du compte — c'est le principal intérêt du montage en deux temps.

## 1. Déposer les fichiers dans le thème

| Fichier local                     | Destination dans le thème              |
|-----------------------------------|----------------------------------------|
| `theme/gf-club.css`               | `assets/gf-club.css`                   |
| `theme/gf-club.js`                | `assets/gf-club.js`                    |
| `theme/gf-club.liquid`            | `sections/gf-club.liquid`              |
| `theme/gf-espace-membre.liquid`   | `sections/gf-espace-membre.liquid`     |
| `theme/page.club.json`            | `templates/page.club.json`             |
| `theme/page.espace-membre.json`   | `templates/page.espace-membre.json`    |

```
python scripts/push_club.py --list
python scripts/push_club.py --theme-id <id> --dry-run
python scripts/push_club.py --theme-id <id> --allow-live
```

Une seule feuille de style pour les deux pages (`gf-club.css`) : les deux
sections la chargent par `asset_url`. Aucun patch de `layout/theme.liquid`.

## 2. Créer les deux pages

Boutique en ligne → Pages → **Ajouter une page**, contenu laissé vide dans les
deux cas (tout vient de la section) :

| Titre           | Handle           | Modèle de thème  |
|-----------------|------------------|------------------|
| `Le Club`       | `club`           | `club`           |
| `Espace membre` | `espace-membre`  | `espace-membre`  |

Les deux modèles se référencent l'un l'autre par leurs réglages `espace_url` et
`club_url` : si un handle change, corriger les deux.

## 3. Klaviyo

La liste **« Le Club Gus et Frost »** existe déjà (id `WRcwhe`, double opt-in),
et le modèle de page porte la clé publique du compte (`VyiAUH`). Les propriétés
poussées sur le profil : `club_membre`, `club_date`, `source_lead`, `prenom`,
`prenom_animal`.

Le double opt-in impose une confirmation par e-mail avant tout envoi. Ce n'est
pas gênant : les guides ne sont pas livrés par e-mail, ils vivent dans l'espace
membre. L'e-mail sert à annoncer les nouveautés.

Reste à faire côté Klaviyo : le flow de bienvenue déclenché par l'inscription à
la liste.

## 4. Points de vigilance

- **Le verrou masque, il ne chiffre pas.** Le PDF d'un guide reste servi par le
  CDN Shopify : qui possède l'adresse exacte peut l'ouvrir sans être membre.
  C'est acceptable pour un club gratuit ; une vraie protection demanderait une
  application. Ne pas mettre derrière ce verrou un contenu vendu.
- **Le réglage « Tag requis » est vide par défaut**, et c'est voulu : tout client
  connecté entre. Le remplir (par exemple `club`) transforme la page en espace
  réservé à une partie des clients — mais il faut alors poser le tag sur chaque
  client, à la main, par Shopify Flow ou par Make.
- **Ne jamais activer « compte obligatoire au checkout »** : cela imposerait la
  création de compte pour acheter, et ferait chuter la conversion.
- **Insécables** : les textes des deux sections et des deux modèles en portent
  (U+00A0). `python scripts/check_insecables.py theme/gf-club.liquid
  theme/gf-espace-membre.liquid theme/page.club.json theme/page.espace-membre.json`
  doit rester à zéro violation. Attention : ne jamais lancer un correcteur
  automatique sur le corps d'un `.liquid` — une insécable glissée dans un `!=`
  casse la page.
- **Une seule section « Le Club » par page** (le JS est un singleton par racine).
