# Gus & Frost — Dépôt blog (cluster « stress du chien »)

Ce dépôt contient **33 articles prêts à publier** sur le blog Shopify de Gus & Frost,
plus tout ce qu'il faut pour automatiser la mise en ligne. Il est conçu pour être
opéré par **Claude Code** (configuration du thème + script de publication via l'API
Admin Shopify).

> Marque : Gus & Frost — produits premium chien/chat. Identité visuelle : vert `#314431`,
> beige `#EFE7DA`. Ton : voix « anti‑IA », factuel. Règle produit : les produits
> **aident à apaiser**, ils ne « soignent » ni ne « guérissent » jamais.

---

## 1. Contenu du dépôt

```
gus-frost-blog/
├── README.md                     ← ce fichier
├── manifest.csv                  ← source de vérité (1 ligne par article)
├── theme/
│   ├── gf-article.css            ← CSS partagé des articles (à charger 1× dans le thème)
│   └── related-articles.liquid   ← snippet de la section « articles liés » dynamique
├── articles/
│   ├── cluster-1-anxiete-separation/   (1 pilier + 10 satellites)
│   ├── cluster-2-peur-bruit/           (1 pilier + 10 satellites)
│   └── cluster-3-calme-serenite/       (1 pilier + 10 satellites)
├── images-prompts/               ← prompts d'images (1 .md par article) pour générer les visuels
│   ├── cluster-1-anxiete-separation/
│   ├── cluster-2-peur-bruit/
│   └── cluster-3-calme-serenite/
└── reference/
    ├── MAILLAGE_recap_placeholders.md          ← carte des liens internes (placeholders)
    └── 2026-06-18_INDEX_sommaire-blog-chien_v1.html
```

Chaque fichier article est nommé **par son slug** (= le handle Shopify visé).

---

## 2. Décisions de structure (important — ne pas casser)

Les articles ont été **nettoyés** par rapport aux fichiers d'origine :

1. **CSS retiré de chaque article** → centralisé une seule fois dans `theme/gf-article.css`.
2. **Blocs de liens du bas retirés** (les anciens `div.gf-satellites` / `div.gf-pilier`)
   → remplacés par la **section dynamique** `theme/related-articles.liquid`.
3. Le corps de chaque article **conserve son wrapper** `<article class="gf-article">`.
   → Le template Shopify doit injecter `{{ article.content }}` **tel quel**, sans
   ré‑emballer dans un second `.gf-article` (sinon double imbrication).
4. Sont **conservés** dans le corps : titres, images, encadrés `.gf-conseil`, tableaux,
   la FAQ, et le bloc CTA produit `.gf-cta`.

Restent à résoudre dans le corps (voir §6) :
- liens internes `href="PLACEHOLDER_..."` ;
- images `src="REMPLACER_..."`.

---

## 3. manifest.csv — colonnes

| Colonne | Rôle |
|---|---|
| `cluster_num` | 1, 2 ou 3 |
| `cluster_tag` | tag de cluster (ex. `cluster-anxiete-separation`) |
| `type` | `pilier` ou `satellite` |
| `slug` | handle Shopify visé |
| `parent_pilier_slug` | slug du pilier parent (vide pour un pilier) |
| `title` | titre de l'article (H1) |
| `meta_title` | balise SEO `<title>` |
| `meta_description` | meta description SEO |
| `tags` | tags à appliquer à l'article (cluster + type + thématiques) |
| `file` | chemin du HTML nettoyé dans ce dépôt |
| `prompts_file` | chemin du fichier de prompts d'images |
| `links_to_resolve` | nb de `PLACEHOLDER_` restants dans l'article |
| `images_to_resolve` | nb de `REMPLACER_` restants dans l'article |

---

## 4. À régler dans Shopify (checklist Claude Code)

**A. Blog.** Identifier ou créer le blog cible et noter son **handle** (ex. `conseils`).
Toutes les URLs d'articles en découleront (`/blogs/<handle>/<slug>`).

**B. Thème — CSS.** Ajouter `theme/gf-article.css` aux assets du thème et le charger
**uniquement sur les pages article du blog** (conditionner au template `article`).

**C. Thème — template article.** Afficher `{{ article.content }}` sans wrapper
supplémentaire (le wrapper `.gf-article` est déjà dans le contenu). Inclure ensuite
la section liés (point D) **après** le contenu.

**D. Section « articles liés » dynamique.** Intégrer `theme/related-articles.liquid`.
Elle fonctionne par tags : elle lit le `cluster-*` de l'article courant, puis affiche
le pilier + les satellites frères (sur un satellite) ou tous les satellites (sur un
pilier). **Pré‑requis : appliquer la colonne `tags` du manifest à chaque article.**

**E. App API (création par l'utilisateur, pas par Claude Code).**
Dans l'admin Shopify : créer une **app personnalisée**, activer l'**Admin API**, scopes
`write_content` + `read_content`, installer l'app et copier le **token Admin API**.
⚠️ Le token est un secret : il est saisi par l'utilisateur dans l'environnement de
Claude Code (variable d'environnement / `.env` non versionné). Ne jamais l'écrire dans
le dépôt ni dans un fichier suivi par Git.

**F. Script de publication (manifest‑driven).** Le script lit `manifest.csv` et, pour
chaque ligne : crée/maj l'article (`POST/PUT article`), pose `title`, `handle`=`slug`,
`body_html`=contenu du fichier, `tags`, et les métadonnées SEO (`metafields_global_title_tag`
= `meta_title`, `metafields_global_description_tag` = `meta_description`). Publier en
**brouillon** d'abord (`published: false`), vérifier, puis publier.

**G. Ordre.** Publier le **pilier de chaque cluster avant ses satellites** (les liens et
la section liés s'appuient sur l'existence du pilier).

---

## 5. Résolution des liens et des images (avant publication)

**Liens internes** `href="PLACEHOLDER_..."` — voir `reference/MAILLAGE_recap_placeholders.md`.
Remplacer chaque token par l'URL Shopify réelle :
- `PLACEHOLDER_pilier-...` → URL du pilier correspondant ;
- `PLACEHOLDER_satellite-0N` / `c2-sat-0N` / `c3-sat-0N` → URL du satellite ;
- `PLACEHOLDER_collection-anti-stress` → URL de la collection produit ;
- `PLACEHOLDER_produit-...` → URL produit (gilet, tapis de fouille, tapis de léchage).

Astuce : le `manifest.csv` donne le slug de chaque article → l'URL est
`/blogs/<handle-du-blog>/<slug>`. On peut donc résoudre la plupart des liens
automatiquement par correspondance slug.

**Images** `src="REMPLACER_..."` — chaque `<img>` porte un `id` relié à un prompt dans le
fichier `images-prompts/.../*_PROMPTS-IMAGES.md` de l'article. Générer les visuels
(palette Gus & Frost, photoréaliste, sans texte), les héberger (les visuels sociaux du
projet sont déjà sur **Cloudinary**), puis remplacer chaque `src`. Tailles : hero
1600×900, corps 1080×1080, infographies 1080×1350.

---

## 6. Garde‑fous

- **Pinterest** : les 47 épingles du cluster 1 sont déjà dans le calendrier Notion en
  **Brouillon**, avec un lien de destination = slug provisoire. **Ne pas les passer en
  « À publier » tant que les articles ne sont pas en ligne** (sinon liens 404). Préfixer
  alors les slugs du domaine réel.
- **Voix & marque** : ne pas réécrire le contenu. Respecter la voix anti‑IA et la règle
  « les produits aident à apaiser, ils ne soignent pas ».
- **Secrets** : aucun token / mot de passe dans le dépôt. Utiliser un `.gitignore` pour
  `.env`.

---

## 7. Récap chiffré

- 3 clusters × (1 pilier + 10 satellites) = **33 articles**.
- **139** liens internes à résoudre, **71** images à générer/insérer (détail par article
  dans `manifest.csv`).
