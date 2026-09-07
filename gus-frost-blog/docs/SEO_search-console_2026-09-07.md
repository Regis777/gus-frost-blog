# Search Console — 4 alertes du 5 au 7 septembre 2026

Branche `seo/gsc-donnees-structurees`. **Rien n'est déployé** : le thème en ligne
(`165265047773`) est intact.

---

## 1. Le diagnostic

Les alertes ne viennent pas d'un défaut de Liquid isolé. Elles ont **deux causes
distinctes**, et l'une d'elles ne se corrige pas dans le code.

### Cause A — neuf fiches produit vides, publiées

Neuf produits « squelettes » de février 2026 sont **actifs et indexables**, avec :

* **aucune image** (`media` vide) ;
* une description de remplissage : « … — description à compléter (bénéfices,
  matières, usage, garanties). » ;
* un prix et une disponibilité réels.

Le gabarit par défaut rendait pour eux, via le filtre `structured_data` de Shopify :

```json
{ "@type": "ProductGroup", "description": "… description à compléter …",
  "hasVariant": [ { "@type": "Product", "offers": { "@type": "Offer",
                    "price": "29.90", "availability": "…InStock" } } ] }
```

Pas de clé `image` — non parce que le Liquid l'oublie, mais **parce qu'il n'y a
pas d'image à mettre**. C'est le « champ image manquant » critique. Et les offres
n'ont ni `shippingDetails` ni `hasMerchantReturnPolicy`, d'où les deux avis non
critiques.

> Aucune ligne de thème ne corrige ça. Il faut des images, ou dépublier.

### Cause B — un second balisage produit, tronqué, sur la fiche tapis

`sections/avis-produit.liquid` émettait son propre bloc `"@type": "Product"`,
réduit à `name` + `aggregateRating` + `review` : **sans image, sans description,
sans offers**.

Le gabarit `product.tapis-lechage.json` **n'inclut pas** `main-product`. Sur cette
fiche, ce bloc tronqué était donc le *seul* balisage produit de la page.

Relevé sur la page en ligne le 07/09/2026 : deux blocs JSON-LD, `Organization`
puis ce `Product` amputé. Exactement le motif que Google remonte.

### ⚠ Trois avis de démonstration sont publiés comme s'ils étaient réels

Ce même bloc publie, **en ligne**, trois avis inventés (Sandrine L., Marc D.,
Julie P.) et une note agrégée de 4,7/5 sur 3 avis. C'est un balisage d'avis sans
avis réels : une violation des règles Google exposant à une action manuelle.

Le retrait du bloc (ci-dessous) supprime le balisage. **Les trois avis restent
affichés visuellement** : leur suppression est une décision éditoriale, pas
technique — métaobjets « Avis produit » dans l'admin Shopify.

### Cartographie des cinq gabarits produit

| Gabarit | Section principale | Balisage produit AVANT |
|---|---|---|
| `product.json` (défaut) | `main-product` | `ProductGroup` sans image |
| `product.conversion.json` | `main-product` | `ProductGroup` sans image |
| `product.tapis-lechage.json` | `tapis-lechage` + `avis-produit` | `Product` tronqué + faux avis |
| `product.monoproduit.json` | `monoproduit` | **aucun** |
| `product.produit-digital.json` | `rituel-du-calme` | **aucun** |

Deux gabarits sur cinq n'avaient aucun balisage produit. C'est le défaut qui aurait
silencieusement touché les vraies fiches à venir.

---

## 2. Ce qui est corrigé dans le thème

### `snippets/gf-product-schema.liquid` — nouveau

Source unique du balisage produit. Écrit à la main, donc éditable, contrairement
au filtre `structured_data`.

* `image` : tableau d'URL **absolues** (`| image_url: width: 1946 | prepend: 'https:'`),
  jusqu'à 8 visuels, la photo de la variante choisie en tête. **La clé est omise
  s'il n'y a pas d'image** — jamais une chaîne vide.
* `description` : `strip_html` seul collait les mots des listes (`</li><li>`) et
  laissait les entités (« Gus &amp; Frost » serait parti tel quel). Le fragment
  insère une espace avant chaque balise, décode les entités (`&amp;` en dernier,
  sinon `&amp;lt;` se décoderait deux fois) puis recolle la ponctuation basse.
  Les espaces insécables du corpus sont préservées.
* `offers` : une `Offer` par variante, avec `shippingDetails` et
  `hasMerchantReturnPolicy` (voir §4).
* Produit sans expédition (le guide PDF) : pas de `shippingDetails`, et
  `MerchantReturnNotPermitted` — conforme à l'exception de rétractation des
  contenus numériques (politique de remboursement, section 8).
* **Aucun `review` ni `aggregateRating`.** Point de branchement documenté en fin
  de fichier, à activer quand de vrais avis existeront.

### `layout/theme.liquid` — 9 lignes ajoutées

```liquid
{%- if request.page_type == 'product' -%}
  {%- render 'gf-product-schema', product: product -%}
{%- endif -%}
```

Appelé depuis le layout, et non depuis les sections : le balisage couvre ainsi
**les cinq gabarits**, y compris les deux qui n'en avaient aucun, et il ne peut
pas exister en double.

### `sections/main-product.liquid` — filtre retiré

`{{ product | structured_data }}` supprimé, remplacé par un commentaire qui
explique pourquoi ne pas le rétablir.

### `sections/avis-produit.liquid` — JSON-LD retiré

Le bloc `Product` tronqué et ses trois faux avis sont retirés. L'affichage visuel
des avis est conservé à l'identique.

---

## 3. Vérifications faites

* Balises Liquid équilibrées sur les quatre fichiers.
* Plus aucun second `"@type": "Product"` dans le thème.
* `scripts/simule_product_schema.py` rejoue hors ligne la logique du fragment sur
  les données réelles d'un produit et valide le JSON obtenu :
  **15 offres, 7 images, description de 1 755 caractères, JSON valide.**
  Sortie : `build/jsonld_tapis-de-lechage-chien-chat.json`.

C'est une **simulation fidèle**, pas un rendu Shopify. Pour un rendu réel avant
publication, le plus propre est de dupliquer le thème en un thème non publié et
d'y déposer les quatre fichiers : le connecteur MCP l'autorise sur un thème non
publié, et la boutique en ligne n'est pas touchée.

---

## 4. Livraison et retours : mon avis

**Déclare-les dans Google Merchant Center, pas dans le balisage.** Trois raisons,
dans l'ordre de poids :

1. **Le balisage ne sait pas dire ta grille.** Zone France : 8,80 €, **gratuit à
   partir de 50 €**. `schema.org` n'a pas de champ pour un seuil de gratuité :
   `shippingRate` est un montant, point. Le fragment annonce donc 8,80 € — le
   tarif sous le seuil, jamais sous-estimé, mais faux dès qu'un panier dépasse
   50 €. Merchant Center, lui, gère le seuil nativement.
2. **Les délais dépendent du stock, pas du produit.** Ta politique d'expédition
   annonce 2 à 6 jours depuis la France et **12 à 25 jours** quand l'article part
   de Chine. Le balisage est figé par produit ; il sera faux la moitié du temps.
3. **Une seule grille à tenir.** Merchant Center couvre les fiches gratuites *et*
   Shopping. Le balisage ne couvre que l'organique — et tu tiendrais deux sources.

Le fragment contient donc un interrupteur en tête de fichier :

```liquid
assign gf_livraison_retours = true
```

Il est à `true` aujourd'hui pour répondre aux deux avis Search Console tout de
suite. **Passe-le à `false` une fois Merchant Center configuré** : ce n'est pas
« les deux à la fois », c'est un relais.

Valeurs actuelles, relevées le 07/09/2026 sur le « Profil général » et les
politiques du 02/09/2026 :

| Champ | Valeur | Source |
|---|---|---|
| `shippingRate` | 8,80 € | zone France + Monaco |
| `handlingTime` | 1 à 2 jours | politique d'expédition, §3 |
| `transitTime` | 2 à 6 jours | politique d'expédition, §4 (**stock France uniquement**) |
| `merchantReturnDays` | 14 | politique de remboursement, §3 |
| `returnFees` | `ReturnFeesCustomerResponsibility` | politique de remboursement, §5 |
| `refundType` | `FullRefund` | politique de remboursement, §7 |

**Deux incohérences relevées, à trancher :**

* La politique d'expédition annonce les 27 pays de l'UE + Norvège + Suisse. Les
  zones de livraison réelles ne contiennent **ni la Norvège ni la Suisse** : elles
  tomberaient dans « Autres destinations » à 29 €. Un client suisse lit une
  promesse que le paiement ne tient pas.
* `transitTime` 2–6 jours ne vaut que pour un article en stock en France. Ne pas
  laisser ce balisage sur un produit expédié depuis la Chine.

---

## 5. Indexation — 404 et pages avec redirection

### Ce que le sitemap dit

`scripts/audit_sitemap.py` lit `sitemap.xml`, descend dans les sous-sitemaps et
teste chaque URL. **499 URL** trouvées.

**Résultat définitif : 499 réponses 200. Aucun 404, aucune redirection.**

Le pare-feu Shopify a limité mon adresse IP (HTTP 429) au premier passage ;
`scripts/audit_sitemap_reprise.py` a repris les 302 URL restantes après une pause,
à 4 s par requête. Le sitemap est donc sain de bout en bout.

### Ce que le sitemap ne peut pas dire

C'est le point important : **les URL qui déclenchent l'alerte ne sont pas dans le
sitemap.** Un sitemap Shopify ne liste que les pages vivantes. Les 404 que Google
signale sont, par définition, des URL qu'il a connues ailleurs et qui n'y sont
plus. Le crawl du sitemap vérifie que rien n'est cassé *à l'intérieur* — utile,
mais ce n'est pas la réponse à l'alerte.

**Il me faut l'export du rapport d'indexation** pour produire le CSV de
redirections. Sans lui, toute liste serait inventée.

### Deux explications très probables, à confirmer par l'export

1. **Le nettoyage des locales du 02/09/2026.** 1 989 URL ramenées à 498 en
   retirant `de`/`es`/`it` du marché France. Des centaines d'URL `/de/…`, `/es/…`,
   `/it/…` étaient indexées et ne répondent plus. L'alerte arrive quatre jours
   après. **C'est le comportement voulu : rien à corriger.**
2. **Les 16 redirections déjà en place** (relevées dans l'admin) — 12 anciens
   handles d'articles chiot renommés, 3 anciennes pages piliers, 1 fichier
   IndexNow. Google les classe « Page avec redirection, non indexée », ce qui est
   le résultat attendu d'une redirection 301. **Rien à corriger non plus.**

Autrement dit : les deux alertes d'indexation décrivent probablement le résultat
normal de deux nettoyages volontaires. À confirmer sur l'export avant de conclure.

### Aucune redirection à créer pour l'instant

Le CSV `Redirect from,Redirect to` est donc vide à ce stade. Les liens internes du
corpus pointent vers des **collections**, pas vers des fiches produit
(`reference/placeholder-map.json` : aucun `PLACEHOLDER_produit-*` dans les corps
d'articles) — 235 liens vers `/collections/stress`, 220 vers `/collections/chat`.

---

## 6. Ce qui reste, par canal

**Shopify admin — fait le 07/09/2026, sur ta décision**

* ✅ **Les 12 produits publiés sont passés en brouillon.** Le catalogue en ligne est
  vide. Cela supprime à la source l'erreur critique « champ image manquant » et les
  deux avis sur les offres : plus aucune page produit n'est servie.
* ✅ **Le champ « Avis clients » de la fiche tapis est vidé** (metafield
  `custom.avis` supprimé). Le balisage de faux avis et leur affichage à l'écran ont
  disparu sans attendre le déploiement du thème. Les trois métaobjets « Avis
  produit » restent en base comme gabarit de saisie.

**Shopify admin — à faire**

* ⚠ **Quatre collections sont désormais vides** : `/collections/stress` (liée 235
  fois depuis les articles), `/collections/chat` (220 fois), `/collections/education`
  et `/collections/senior` (déjà vides avant). Elles répondent 200 mais ne montrent
  rien. À repeupler dès les premières vraies fiches, sinon ce sont 455 liens
  internes qui mènent à du vide.
* Trancher la Norvège et la Suisse dans la politique d'expédition.
* Déployer les quatre fichiers du thème quand tu auras relu — **avant** de publier
  les vraies fiches produit, sinon deux gabarits sur cinq sortiront sans balisage.

**Merchant Center** (compte 5847008347)

* Renseigner les paramètres de livraison et de retour au niveau du compte.
* Puis passer `gf_livraison_retours` à `false`.

**Search Console**

* Exporter le rapport d'indexation → je produis le CSV de redirections.
* Après déploiement : tester une fiche sur
  <https://search.google.com/test/rich-results>.

**Volontairement non fait**

* `review` et `aggregateRating` : en attente de volume d'avis.
* Suppression des trois faux avis affichés : décision éditoriale.
* Tout déploiement.

---

## 7. Ce que le test des résultats enrichis devrait afficher

Sur une fiche avec image et description :

* **Extraits de produit** : détecté, sans erreur. Avertissement attendu sur
  `review` / `aggregateRating` absents — voulu.
* **Fiches de marchand** : détecté, sans erreur critique. `image`, `description`,
  `offers.shippingDetails` et `offers.hasMerchantReturnPolicy` sont présents.
* Avertissement possible sur `gtin`/`mpn` : aucun code-barres n'est renseigné dans
  le catalogue. À combler sur les vrais produits.

Sur une fiche **sans image** (les neuf squelettes), l'erreur critique
« champ image manquant » **reste** : le fragment omet correctement la clé, mais
Google la réclame. Seules des images, ou la dépublication, la font disparaître.
