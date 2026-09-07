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

## 5. Indexation — chiffres relevés dans la Search Console

Rapport « Indexation des pages », propriété de domaine, dernière mise à jour du
04/09/2026 : **462 pages dans l'index, 237 non indexées**, en quatre motifs.

| Motif | Source | Pages |
|---|---|---|
| Introuvable (404) | Site Web | **56** |
| Page avec redirection | Site Web | **37** |
| Détectée, actuellement non indexée | Systèmes Google | 142 |
| Explorée, actuellement non indexée | Systèmes Google | 2 |

### Les 56 « Introuvable (404) » — rien à corriger

Les 56 URL ont été relevées, page par page. **56 sur 56 portent un préfixe de
locale** : `/de/`, `/es/`, `/it/`, plus un `/en/`. Aucune URL du site en français.
Exemples : `/es/blogs/chats/adopter-chaton-refuge-eleveur`,
`/it/blogs/chats/hydratation-eau-chat`, `/de/pages/conseils-chiens`,
`/es/products/tapis-de-lechage-chien-chat`.

Première détection : 05/09/2026 — trois jours après le retrait de `de`/`es`/`it`
du marché France, qui a ramené 1 989 URL à 498. **C'est le résultat exact de ce
nettoyage volontaire. Ces 404 sont légitimes et Google les retirera seul.**

### Les 37 « Page avec redirection » — rien à corriger non plus

Trois familles, toutes des 301 délibérées :
* l'ancien handle de blog **`/blogs/cats/…`**, renommé en `/blogs/chats/…` —
  l'essentiel du lot (`/blogs/cats/sommeil-chat`, `/blogs/cats/proprete-chaton`,
  `/blogs/cats/clignement-lent-chat`…) ;
* `http://gusetfrost.fr/` → HTTPS ;
* une page de locale résiduelle (`/es/password`).

« Page avec redirection, non indexée » est le résultat *attendu* d'une 301 : Google
indexe la cible, pas la source.

### Le CSV de redirections est donc vide, et c'est la bonne réponse

Les 93 URL des deux motifs sont soit des locales retirées volontairement, soit des
redirections déjà en place. **Aucune redirection à créer.** Créer une 301 pour ces
locales serait même une erreur : elle ferait vivre des URL qu'on vient de supprimer.

### Le sitemap, en confirmation

`scripts/audit_sitemap.py` a testé les **499 URL** du sitemap et de ses
sous-sitemaps : **499 réponses 200, aucun 404, aucune redirection.** Le pare-feu
Shopify a limité l'adresse IP (HTTP 429) au premier passage ;
`scripts/audit_sitemap_reprise.py` a repris les 302 URL restantes après une pause.
Cohérent avec ce qui précède : les URL problématiques ne sont pas dans le sitemap,
puisqu'elles n'existent plus.

### Les deux rapports de données structurées, chiffres au 06/09/2026

**Fiches de marchand** — 15 valides, **1 non valide**. L'unique élément critique
« champ image manquant » est
`/products/diffuseur-apaisant-maison-adaptateur-diffuseur-stress-anxiete` : une des
neuf fiches squelettes, confirmant la cause A. Les autres squelettes ne figurent
pas ici parce qu'ils sont restés « Détectée, actuellement non indexée » — Google ne
les a jamais validés. Améliorations : `hasMerchantReturnPolicy` manquant sur 16,
`shippingDetails` sur 16, `description` sur 16.

Le `description` manquant sur **16 éléments sur 16** confirme le diagnostic du §1 :
la description existe au niveau `ProductGroup`, mais **pas sur le `Product`
imbriqué** que Google lit comme fiche de marchand.

**Extraits de produits** — 3 valides, **0 non valide**. `aggregateRating` et
`review` manquants sur 2 éléments : c'est l'avertissement voulu, en attente de
vrais avis.

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

## 6 bis. Thème d'aperçu — dépôt du 07/09/2026

Thème **165320982749**, « APERCU — JSON-LD produit (ne pas publier) », dupliqué
depuis le thème en ligne. Le thème publié n'est pas touché.

Les quatre fichiers y sont déposés et vérifiés **par empreinte MD5**, à l'octet
près. Dépôt fait par `body: {type: URL}` vers le dépôt GitHub, SHA épinglé : une
chaîne de bloc GraphQL altère les insécables d'un gros Liquid.

Aperçu : `https://gusetfrost.fr/?preview_theme_id=165320982749` — page servie en
200, **aucune erreur Liquid**. `layout/theme.liquid`, le fichier à risque, est sain.

### Ce que le rendu réel a révélé, et que la simulation ne pouvait pas voir

Le tapis a été remis en ligne deux minutes pour charger sa fiche sur le thème
d'aperçu. Résultat : **un seul bloc `Product`**, avec `image`, `description`,
`offers` (15), `shippingDetails`, `hasMerchantReturnPolicy` — et **aucun balisage
d'avis**. Puis produit repassé en brouillon.

Un défaut réel est apparu là : **l'image de tête sortait deux fois.** Le
dédoublonnage comparait `media.preview_image.id` à `product.featured_image.id`,
qui ne désignent pas la même chose. Le simulateur hors ligne ne pouvait pas le
voir, puisqu'il parcourt les médias une seule fois. Corrigé : comparaison sur
l'URL rendue, parcours porté à 12 médias.

Deuxième écart, sans gravité : Shopify rend les images sur
`https://gusetfrost.fr/cdn/shop/files/…` et non `cdn.shopify.com`. C'est le domaine
canonique, c'est mieux ainsi.

**Le fragment corrigé est déposé et son empreinte est conforme, mais son rendu
n'a pas été revérifié** — il faudrait remettre une fiche en ligne une seconde
fois. À faire sur la première vraie fiche produit, avant tout déploiement.

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
