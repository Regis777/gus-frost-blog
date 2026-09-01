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
