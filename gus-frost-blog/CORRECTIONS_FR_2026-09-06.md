# Corrections du corpus français — clusters « Langage du chat » (13) et « Langage corporel du chien » (13)

Journal d'exécution du 06/09/2026. Source : passage de relais du 05/09/2026 (audits `EN/CH1_EN_audit.md` et `EN/CD1_EN_audit.md`).

Méthode appliquée à chaque article : relecture du `body_html` **en ligne juste avant écriture** (coexistence avec la conversation « références »), remplacements de chaînes exactes avec nombre d'occurrences attendu, contrôle structurel avant/après (h2, h3, figure, img, a, div.gf-, aside, li, p, script JSON-LD unique et valide), écriture par `articleUpdate`, puis **relecture de contrôle** du champ écrit.

**Écritures refusées par construction** : aucun `articleCreate`, aucun `translationsRegister`, aucun script de la chaîne d'ingestion (`ingest_cluster.py`, `deploy_cluster.py`, `mkfinal.py`) n'a été employé.

---

## 0. Décision hors périmètre du prompt : propagation aux sources du dépôt

Le prompt ne raisonnait que sur l'API. Or les 26 articles ont une **source locale** dans le dépôt
(`articles/cluster-1-langage-chat/` et `articles/cluster-4-langage-corporel/`), et un rebake écrase le corps en ligne.
Une correction faite uniquement en ligne aurait donc été **perdue au prochain rebake** (cf. mémoire `tao-ulysse-divergence`).

→ **Toutes les corrections de corps ont été appliquées deux fois : en ligne ET dans la source du dépôt.**
Les métadonnées ont été propagées de la même façon dans `manifest_chat.csv` et `manifest.csv`
(remplacement au niveau octet pour préserver les fins de ligne CRLF — piège `git-workflow`).

---

## 1. Récapitulatif

| Lot | Objet | Articles touchés | Remplacements |
|---|---|---|---|
| A1 | Encart « Le Carnet » parlant du chien sur le blog chat | 13 (chat) | 13 |
| A2 | Mot « cluster » visible par le lecteur | 4 (chat) | 9 |
| A3 | Fautes de langue | 5 | 5 |
| A4 | Espaces insécables / apostrophes | 1 | 1 (voir §4 : défaut inexistant) |
| A5a | Classe `gf-cas` (chien) | 0 | 0 — **en attente d'arbitrage** |
| A5b | `id="faq"` sur les satellites chien | 12 | 12 |
| A6 | Métadonnées tronquées ou fausses | 4 | 6 |
| **Total** | | **26 articles lus, 25 modifiés** | **46** |

Contrôle final sur les 26 corps relus en ligne après écriture : **0 anomalie**
(0 « votre chien » dans le cluster chat, 0 « cluster » en texte visible, `id="faq"` partout,
1 seul JSON-LD valide par article, chaque question du JSON-LD retrouvée à l'identique dans un `<h3>`).

---

## 2. Détail par article

### Cluster CHAT (blog `chats`, tag `cluster-langage-chat`)

| Code | Handle | Corrections appliquées |
|---|---|---|
| PILIER | `langage-du-chat` | A1 ×1 ; A2 ×3 |
| CH-S01 | `clignement-lent-chat` | A1 ×1 |
| CH-S02 | `idees-recues-langage-chat` | A1 ×1 ; A2 ×1 ; A6 ×1 |
| CH-S03 | `marquage-facial-frottements-chat` | A1 ×1 ; A3 ×1 |
| CH-S04 | `miaulements-chat-comprendre` | A1 ×1 ; A6 ×1 (meta) |
| CH-S05 | `observer-chat-carnet-signaux` | A1 ×1 ; A2 ×4 |
| CH-S06 | `oreilles-chat-emotions` | A1 ×1 |
| CH-S07 | `postures-corps-chat` | A1 ×1 |
| CH-S08 | `pupilles-yeux-chat` | A1 ×1 ; A6 ×1 (meta) |
| CH-S09 | `queue-chat-signification` | A1 ×1 |
| CH-S10 | `ronronnement-chat-signification` | A1 ×1 ; A3 ×2 |
| CH-S11 | `signes-agacement-inconfort-chat` | A1 ×1 ; A2 ×1 |
| CH-S12 | `vibrisses-moustaches-chat` | A1 ×1 ; A3 ×1 |

### Cluster CHIEN (blog `chiens`, tag `cluster-langage-corporel`)

| Code | Handle | ID | Corrections appliquées |
|---|---|---|---|
| PILIER | `langage-corporel-chien` | 597529854173 | A4 ×1 (apostrophe) |
| CD-S01 | `signaux-apaisement-chien` | 597529886941 | A5b ×1 |
| CD-S02 | `queue-chien-signification` | 597529919709 | A5b ×1 |
| CD-S03 | `baillement-chien-stress` | 597529952477 | A5b ×1 ; A6 ×2 (meta + excerpt) |
| CD-S04 | `chien-leche-truffe-babines` | 597529985245 | A5b ×1 ; A3 ×1 |
| CD-S05 | `oreilles-chien-emotions` | 597530018013 | A5b ×1 |
| CD-S06 | `oeil-de-baleine-chien` | 597530050781 | A5b ×1 |
| CD-S07 | `postures-stress-chien` | 597530083549 | A5b ×1 |
| CD-S08 | `chien-s-ebroue-signal` | 597530116317 | A5b ×1 |
| CD-S09 | `echelle-stress-chien-morsure` | 597530149085 | A5b ×1 |
| CD-S10 | `haletement-tremblements-chien-stress` | 597530181853 | A5b ×1 |
| CD-S11 | `observer-chien-carnet-signaux` | 597530214621 | A5b ×1 |
| CD-S12 | `idees-recues-langage-canin` | 597530247389 | A5b ×1 |

Les deux identifiants manquants du prompt ont été résolus par requête sur le tag `cluster-langage-corporel`
(13 articles retournés, aucun de plus).

---

## 3. Chaînes avant / après

### A1 — encart « Le Carnet » (13 articles chat, 1 occurrence chacun)

- avant : `Gardez tout le suivi de votre chien au même endroit`
- après : `Gardez tout le suivi de votre chat au même endroit`

Le reste du bloc (« Vaccins, poids, rappels du vétérinaire, budget ») est neutre et n'a pas bougé.
Le même bloc dans les 13 articles chien n'a pas été touché.

### A2 — mot « cluster » (9 occurrences, 4 articles)

Le prompt en relevait 5. La lecture des corps en ligne en a montré **9** : les 4 occurrences supplémentaires
sont toutes dans `observer-chat-carnet-signaux`, que l'audit ne relevait pour aucune.
Le mot retenu est **« dossier »**, déjà employé par le thème dans les blocs générés
(« Le dossier complet », « À lire aussi dans ce dossier »).

| Article | avant | après |
|---|---|---|
| `langage-du-chat` | est le fil rouge de tout ce **cluster** | …de tout ce **dossier** |
| `langage-du-chat` | relève d'une autre logique et d'un autre **cluster** | …et d'un autre **dossier** |
| `langage-du-chat` | les **articles satellites de ce cluster** vous y invitent | les **autres articles de ce dossier** vous y invitent |
| `idees-recues-langage-chat` | Tout ce **cluster** démontre le contraire. | Tout ce **dossier** démontre le contraire. |
| `observer-chat-carnet-signaux` | tout au long de ce **cluster**, comment lire | tout au long de ce **dossier**, comment lire |
| `observer-chat-carnet-signaux` | qui traverse tout le **cluster** | qui traverse **l'ensemble de ces articles** |
| `observer-chat-carnet-signaux` | décrite tout au long de ce **cluster**. | décrite **au fil de ces articles**. |
| `observer-chat-carnet-signaux` | explorée canal par canal dans ce **cluster** | …dans ce **dossier** |
| `signes-agacement-inconfort-chat` | vers lesquels ce **cluster du langage** fait le pont. | vers lesquels ce **dossier sur le langage** fait le pont. |

Deux reformulations dépassent le remplacement mot à mot, comme le prompt y autorisait :
« articles satellites » est du jargon de production au même titre que « cluster », et
`observer-chat-carnet-signaux` aurait sinon porté quatre fois « dossier » dans un seul texte.

### A3 — fautes de langue (5)

| Article | avant | après |
|---|---|---|
| `ronronnement-chat-signification` | chez des **chates** en train de mettre bas | chez des **chattes** |
| `ronronnement-chat-signification` | `<h2>Comment le chat ronronne-t-il</h2>` | `<h2>Comment le chat ronronne-t-il ?</h2>` (insécable avant le `?`) |
| `marquage-facial-frottements-chat` | un chat qui **s'y approprie** et s'y sent en sécurité | un chat qui **se l'approprie** et s'y sent en sécurité |
| `vibrisses-moustaches-chat` | **Les priver** de ses vibrisses reviendrait à **priver le chat d'**un sens essentiel | **Le priver** de ses vibrisses reviendrait à **lui retirer** un sens essentiel |
| `chien-leche-truffe-babines` | il « **fait la timide** » | il « **fait le timide** » |

### A5b — `id="faq"` (12 satellites chien)

- avant : `<h2>Questions fréquentes</h2>`
- après : `<h2 id="faq">Questions fréquentes</h2>`

Aligné sur le pilier `langage-corporel-chien` et sur les 13 articles chat, qui le portaient déjà.

### A6 — métadonnées

| Article | Champ | avant | après |
|---|---|---|---|
| `pupilles-yeux-chat` | `global.title_tag` | Les yeux et pupilles du chat : décoder (38 c.) | …**: décoder son regard** (49 c.) |
| `miaulements-chat-comprendre` | `global.description_tag` | Miaou, trille, **roucoulement**, feulement, gazouillis… (146 c.) | roucoulement retiré (132 c.) |
| `baillement-chien-stress` | `global.description_tag` | du bâillement **de sommeil** | du bâillement **physiologique** (129 c.) |
| `baillement-chien-stress` | `summary_html` (excerpt) | du bâillement **de sommeil** | du bâillement **physiologique** |
| `idees-recues-langage-chat` | corps | Bien des signaux **que nous avons décrits**, le clignement lent… | Bien des signaux **détaillés dans les autres articles de ce dossier**, le clignement lent… |

Vérifié avant écriture : `roucoul` apparaît **0 fois** dans le corps de `miaulements-chat-comprendre`
(`gazouillis` 7, `trille` 5, `feulement` 6) — la meta promettait bien une section inexistante.
Aucune section n'a été créée. Dans `baillement-chien-stress`, le corps dit « physiologique » 5 fois
et « sommeil » 1 fois, dans une phrase de contraste : c'est bien la dénomination du corps qui a été retenue.

---

## 4. Corrections NON appliquées, et pourquoi

### A4 — espaces insécables : **le défaut n'existe pas**

Le prompt affirmait : « **Aucun** des 26 articles ne contient d'espace insécable avant `:` `;` `?` `!` ni à
l'intérieur des guillemets ». **C'est inexact.** Mesure sur les 26 corps réellement déployés :

- **1 906 espaces insécables U+00A0** au total, de 46 à 197 par article ;
- **0 violation** de la règle maison (regex de `scripts/check_insecables.py`, restreinte aux nœuds de texte) ;
- les métafields SEO portent eux aussi leurs insécables.

L'audit a très probablement cherché la chaîne `&nbsp;` : Shopify **décode l'entité à l'enregistrement** et
stocke le caractère U+00A0 littéral. La chaîne `&nbsp;` est effectivement absente ; les insécables, non.
La passe de recherche-remplacement sur du HTML — le point risqué que le prompt signalait lui-même — **n'a donc pas eu lieu**,
faute d'objet.

### A4 — apostrophes : **le constat est inversé**

Le prompt demandait de remplacer les apostrophes droites par des typographiques. Or la convention du corpus
est **l'apostrophe droite** : sur les 485 fichiers du dépôt, **95 898 apostrophes droites contre 373 typographiques (0,4 %)**.
Convertir ces 26 articles les aurait mis en rupture avec les 459 autres.

Seule correction retenue, dans l'autre sens : **l'unique apostrophe typographique U+2019** de
`langage-corporel-chien`, isolée au milieu de 307 apostrophes droites dans le même article, ramenée à la droite.

### A5a — classe `gf-cas` sur les encadrés « CAS PRATIQUE » chien : **en attente d'arbitrage**

Le constat est exact : les 13 articles chien portent **19 encadrés `<div class="gf-conseil">` dont la première ligne est
`<strong>CAS PRATIQUE</strong>`**, visuellement identiques aux encadrés « CONSEIL ».

Le prompt conditionnait la correction à une vérification de rendu. Faite en direct sur
`https://gusetfrost.fr/blogs/chiens/signaux-apaisement-chien`, en basculant la classe dans le DOM :

| | `.gf-conseil` (actuel) | `.gf-cas` (proposé) |
|---|---|---|
| Fond de la boîte | beige `#EFE7DA` | blanc |
| Filet gauche | vert `#314431` | **orange `#c16b47`** ✅ |
| Libellé : couleur | vert de marque `#314431` | **gris de corps de texte `#2a2a2a`** ⚠️ |
| Libellé : taille / affichage | 13 px, `inline-block`, capitales | **15 px, `inline`, sans traitement** ⚠️ |
| Puce | 💡 | aucune (correct pour un cas pratique) |

La **boîte** est bien stylée (`.gf-article .gf-cas:not(.gf-box)` existe dans `theme/gf-article.css` et s'applique).
Mais le **libellé** ne l'est pas : le CSS du libellé vise `.gf-conseil strong` (markup chien) et
`.gf-cas .gf-encadre-titre` (markup chat), et le markup chien utilise `<strong>`.
Basculer la seule classe distinguerait donc enfin conseil et cas pratique, **au prix d'un libellé qui redevient
du gras nu**. Le prompt interdisant de toucher au libellé, la correction n'a pas été appliquée.

Trois issues possibles : (a) basculer la classe seule et accepter le libellé nu ; (b) basculer la classe **et**
passer le libellé au format chat `<p class="gf-encadre-titre">Cas pratique</p>`, ce qui donne un rendu
parfaitement aligné sur le cluster chat mais touche au libellé ; (c) ajouter une règle
`.gf-article .gf-cas strong { … }` au thème, ce qui sort du périmètre « articles ».

### A3 — le `<h2>` interrogatif de `chien-s-ebroue-signal` : **il n'existe pas**

Le prompt demandait de le repérer. Les 14 `<h2>` de cet article ont été relus un par un : le seul interrogatif,
`Qu'est-ce que le shake-off ?`, **porte déjà son point d'interrogation**. Les autres sont des titres déclaratifs
ouverts par « Comment / Quand » (« Comment reconnaître un shake-off de décompression »), qui est la convention
du corpus entier : les `<h2>` de section sont déclaratifs, seuls les `<h3>` de FAQ sont interrogatifs.

Recherche élargie aux 26 articles (inversion pronominale `-t-il` / `-elle` / `-on`) : **une seule** vraie question
sans point d'interrogation dans tout le périmètre, `Comment le chat ronronne-t-il` — celle que le prompt signalait
déjà, et qui est corrigée.

---

## 5. Défauts nouveaux, repérés et NON corrigés

1. **`observer-chat-carnet-signaux` était absent de l'audit A2** alors qu'il portait 4 des 9 occurrences de
   « cluster » — près de la moitié du défaut. Corrigé ici, mais cela suggère que l'audit source n'était
   pas exhaustif sur ce point.
2. **« articles satellites »** est un second terme de production visible par le lecteur, de même nature que
   « cluster ». Une seule occurrence dans le périmètre (`langage-du-chat`), traitée à cette occasion.
   **À vérifier sur les 459 autres articles du corpus** : le terme n'a pas été cherché hors périmètre.
3. **Le `<h1>` dupliqué est toujours dans les sources locales du cluster chien** (`articles/cluster-4-langage-corporel/*.html`),
   alors que les corps en ligne ne l'ont plus. Un rebake de ce cluster **réintroduirait le défaut**
   (cf. mémoire `h1-duplique-clusters-anciens`). Hors périmètre, non touché.
4. Les sources locales du cluster chien **divergent des corps en ligne** au-delà du `<h1>` (mise en forme des
   listes, FAQ). Les corrections y ont été appliquées, mais un rebake de ce cluster ne serait pas neutre.

---

## 6. Points restés ouverts

- **A5a** — classe `gf-cas` sur les 19 encadrés « CAS PRATIQUE » chien (voir §4).
- **B1** — les 13 CTA « griffoir » du cluster chat, hors sujet.
- **B2** — les 3 CTA problématiques du cluster chien, dont `echelle-stress-chien-morsure` (chaîne causale
  produit → réduction du risque de morsure, sans source).
- **B3** — 8 contradictions internes.
- **B4** — 9 affirmations non étayées.
- **B5** — 2 références mal appariées (Quaranta 2007, Caeiro 2017) + entrées `gf-refs` orphelines : **relève de la
  conversation « références »**, pas de celle-ci.
- **B6** — 4 promesses de titre non tenues.
- **B7** — maillage interne en prose.
- **§7 du prompt** — défauts hors articles (témoignages dupliqués sur les fiches produit, chaînes d'exemple du
  thème, « 19 € OFFERT », alt des infographies) : signalés à Régis, non traités ici.
