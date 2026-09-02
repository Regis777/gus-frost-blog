# Migration Dawn 15 -> Dawn 16 — report motivé et procédure de rattrapage

**Date du constat : 01/09/2026.** Thème de référence : `Gus & Frost — consolidé (à publier)`
(theme id `163845112029`), basé sur Dawn 15.x. Version proposée par Shopify : **16.0.0**.

## Décision

**Mise à jour reportée, pas refusée.**

Le 01/09/2026, la mise à jour automatique a été lancée depuis l'admin. Shopify n'a pas
touché aux thèmes existants : il a créé trois brouillons `Updated copy of …` en Dawn 16.
Ces trois copies ont été **comparées fichier par fichier** à leur original (378 fichiers,
API Admin, checksums + contenu réel) puis **supprimées le 01/09/2026**, parce que la fusion
automatique casse quatre choses (détail plus bas).

Supprimer les copies ne consomme rien : le bouton « Version 16.0.0 available » reste
disponible sur le thème en ligne et régénère des copies fraîches à la demande, à partir de
l'état du thème au moment du clic.

**Pourquoi reporter plutôt que migrer maintenant :** un thème n'expire pas, Dawn 15
continue de fonctionner indéfiniment. En face, la fusion automatique coûterait la
typographie de 420 articles, le maillage interne et la landing monoproduit. Le calcul
n'est pas serré tant que la boutique est sous mot de passe et que la priorité est la mise
en ligne du blog.

**Ce qu'on se prive d'avoir**, sans urgence : les *standard events* Shopify (script de
tracking natif, utile le jour du pixel Facebook / analytics), les *cart disclosures*
(mentions légales panier), un layout `<body>` simplifié (grid -> flex).

## Sauvegarde qui fait autorité

`theme/backup-dawn15/` contient l'état Dawn 15 des fichiers concernés, extrait de Shopify
le 01/09/2026 :

- `consolide/` — 15 fichiers du thème `163845112029` (les 2 fichiers cœur patchés,
  les 6 templates custom, les templates blog, les settings) ;
- `copie-de-dawn/` — les 5 fichiers du modèle « conversion ». **Reportés dans le consolidé
  le 01/09/2026** (md5 vérifiés après relecture) : ce dossier reste la source versionnée
  du modèle, le consolidé en est désormais porteur.

⚠️ `templates/product.monoproduit.json` n'avait **aucune** copie locale avant cette
sauvegarde : Shopify était l'unique source de vérité pour les 26 blocs de la landing.

## Ce que la fusion automatique casse (mesuré, pas supposé)

Les 16 fichiers custom (`gf-*`, `monoproduit`, `tapis-lechage`, `rituel-du-calme`,
`avis-produit`, `related-articles`) survivent tous **intacts**. Ce sont les *branchements*
qui sautent.

### 1. `layout/theme.liquid` — injection `gf-article.css` supprimée

Dawn 16 réécrit le fichier et perd, juste avant `</head>` :

```liquid
  {%- if template.name == 'article' -%}
  {{ 'gf-article.css' | asset_url | stylesheet_tag }}
{%- endif -%}
</head>
```

Conséquence : Montserrat/Lora et le calibrage ×1,6 (corps 17 px) disparaissent sur les
420 articles, retour au Dawn par défaut.

### 2. `sections/main-article.liquid` — deux `render` supprimés

Perdus juste après `{{ article.content }}` (bloc `when 'content'`) :

```liquid
{%- render 'gf-carnet-promo' -%}
{%- render 'related-articles' -%}
```

Conséquence : plus d'articles liés ni d'encart Carnet en bas des articles.

### 3. `templates/product.monoproduit.json` — remis à zéro

| | Dawn 15 | après fusion |
|---|---|---|
| sections | `main` = `monoproduit`, **26 blocs** | `main` = `main-product` (8 blocs) + `related-products` |
| order | `["main"]` | `["main", "related-products"]` |

La section `sections/monoproduit.liquid` existe toujours : seul le template a été écrasé.
Restauration = réécrire le JSON depuis la sauvegarde.

### 4. Section Dawn parasite injectée en tête des templates custom

La fusion réinjecte la section par défaut **au-dessus** de la section maison :

| Template | Ajouté par la fusion |
|---|---|
| `page.quiz-anxiete.json` | `main` (`main-page`) |
| `page.carnet.json` | `main` (`main-page`) |
| `page.carnet-landing.json` | `main` (`main-page`) |
| `page.parrainage.json` | `main` (`main-page`) |
| `product.tapis-lechage.json` | `main` (`main-product`) + `related-products` |
| `product.produit-digital.json` | `main` (`main-product`) + `related-products` |

Conséquence : le formulaire produit Dawn s'affiche au-dessus des sections premium, et un
titre de page vide au-dessus du quiz et du Carnet.

### 5. Comptes clients classiques supprimés

Dawn 16 retire 15 fichiers : `assets/customer.css`, `sections/main-{account,activate-account,
addresses,login,order,register,reset-password}.liquid` et les 7 `templates/customers/*.json`.
Le réglage `enable_customer_avatar` disparaît aussi de `sections/header-group.json`.

C'est le sens de l'avertissement affiché dans l'admin :
« Publishing this theme will upgrade you to the new version of customer accounts. »
Bascule des clients de « e-mail + mot de passe » vers « code à 6 chiffres par e-mail »,
pages de compte hébergées par Shopify. **Décision à prendre à part** — c'est un sujet
comptes clients, pas un sujet thème.

### Ce qui passe sans dégât

`config/settings_data.json` (couleurs, polices, réglages) est **identique**. Idem pour
`templates/article.json`, `templates/blog.json`, `templates/index.json` et
`sections/footer-group.json`. Le quiz conserve ses clés Klaviyo (`VyiAUH` / `XsbyXa`).
Dawn 16 ajoute 9 fichiers neufs (`cart-disclosure-*.js`, `disclosures.js`,
`component-disclosures.css`, `icon-warning.svg`, `standard-actions-override.js`,
`sections/disclosures.liquid`, `snippets/{cart-disclosure-indicator,product-disclosures}.liquid`).

## Procédure de rattrapage (le jour où on migre)

Compter ~30 min. Ne jamais publier une `Updated copy` telle quelle.

1. **Déclencher** la mise à jour depuis l'admin (`Online Store > Themes`, bouton
   « Version 16.x available » du thème visé). Shopify crée une `Updated copy of …`.
2. **Re-patcher `layout/theme.liquid`** : réinsérer le bloc `gf-article.css` avant `</head>`
   (§1 ci-dessus).
3. **Re-patcher `sections/main-article.liquid`** : réinsérer les deux `render` après
   `{{ article.content }}` (§2).
4. **Restaurer `templates/product.monoproduit.json`** depuis
   `theme/backup-dawn15/consolide/templates/product.monoproduit.json`.
5. **Nettoyer les 6 templates custom** (§4) : retirer la section `main` réinjectée et,
   pour les deux templates produit, `related-products` — puis remettre `order` à sa valeur
   Dawn 15 (voir la sauvegarde, qui fait foi).
6. **Arbitrer les comptes clients** (§5) : vérifier `Settings > Customer accounts` avant de
   publier, la bascule est le vrai point de non-retour.
7. **Vérifier le modèle « conversion »** : les 5 fichiers (`templates/product.conversion.json`
   + `sections/conversion-{marquee,reviews,sticky-atc,trust}.liquid`) sont dans le consolidé
   depuis le 01/09/2026 ; la source versionnée reste `theme/backup-dawn15/copie-de-dawn/`.
   Ils sont autonomes (aucun `render`, aucun `asset_url`) et ne s'appuient que sur des
   sections Dawn standard : `main-product`, `image-with-text`, `multicolumn`,
   `collapsible-content`.
8. **Contrôler en preview** avant publication : un article (typo + articles liés + encart
   Carnet), `/pages/quiz-anxiete`, `/pages/mon-carnet`, la fiche tapis de léchage et la
   landing monoproduit.

## Méthode de contrôle

Le diff a été fait avec l'API Admin REST (`GET /themes/{id}/assets.json`, champ `checksum`),
puis contenu réel pour les fichiers suspects. Attention : le champ `size` de la liste
d'assets n'est **pas** la taille du contenu servi (JSON re-sérialisé) — comparer les
checksums, puis le contenu, jamais les tailles.

Identifiants utiles :

| Thème | id | rôle |
|---|---|---|
| Dawn | `158654333149` | en ligne |
| Gus & Frost — consolidé (à publier) | `163845112029` | brouillon, **thème à publier** |
| Copie de Dawn | `162807808221` | bac à sable (périmé : ni Carnet, ni parrainage, ni recherche blog) |

Depuis le report du modèle « conversion » (01/09/2026), le consolidé est un **sur-ensemble
strict** de `Copie de Dawn` : plus aucun fichier n'existe seulement dans le bac à sable.

Une seule divergence subsiste, **volontairement non reportée** : le
`templates/product.json` de `Copie de Dawn` porte une section `rituel-du-calme` (23 blocs)
greffée sur le modèle produit *par défaut*. Elle ferait apparaître le bloc guide PDF sur
**toutes** les fiches produit sans modèle dédié. C'est un reste d'essai : la version
aboutie (24 blocs) vit dans `templates/product.produit-digital.json`, qui est son bon
emplacement.

## Degreffage prepare (02/09/2026) — reduit la casse a la prochaine mise a jour

Les points §1 et §2 ci-dessus n'existent que parce qu'on avait greffe du code
dans deux fichiers de Dawn. Deux sections a nous les remplacent :

| Section | Position dans `templates/article.json` | Remplace |
|---|---|---|
| `gf-article-css` | en tete | l'injection de `gf-article.css` dans `layout/theme.liquid` |
| `gf-article-extras` | juste apres `main` | les deux `render` dans `sections/main-article.liquid` |

Bascule : `python scripts/degreffe_article.py --theme-id <id> --apply`
Retour arriere : le meme avec `--revert` (teste, le theme repasse byte-identique).

Verifie sur une copie du theme publie : geometrie identique au pixel et zero
difference sur 7 elements x 14 proprietes calculees.

**Une fois applique, la procedure de rattrapage perd ses etapes 2 et 3** : plus
aucun fichier de Dawn n'est modifie sur les pages article, donc une mise a jour
ne peut plus casser ni la typo, ni le maillage, ni l'encart Carnet. Restent les
modeles JSON (§3 monoproduit et §4 sections parasites), qui relevent du
comportement de fusion de Shopify et non de nos greffes.

**Non applique au theme publie a ce jour.**

