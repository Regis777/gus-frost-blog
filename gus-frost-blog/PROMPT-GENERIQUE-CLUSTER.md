# Prompt de reprise — Cluster **C__** « ______ »
### Gus et Frost · Pinterest · production d'épingles

> **Mode d'emploi :** remplace `C__` par le numéro du cluster (C2, C3, C4, C9, C12, C14…) et colle ce document en **premier message** d'une nouvelle conversation du projet Pinterest. Une conversation neuve ne sait **rien** — ce document remplace la mémoire.
> Traite **un seul cluster par conversation**. C'est la leçon de C12 : une conversation surchargée produit du travail à moitié juste, et un CSV faux ne se voit qu'au moment où le pipeline casse.

---

## 0. État du projet au 16/07/2026

- **C1** (anxiété de séparation, 47 épingles) : **produit**, images dans `📤 PNG prêts`, statut « À dater ».
- **C13** (chien anxieux, 52 épingles) : CSV prêts, production à faire.
- **332 épingles en « Brouillon »** réparties sur 6 clusters restants (**C2, C3, C4, C9, C12, C14**).
- **Total : 379 épingles Pinterest**, 83 URLs × 4 variantes (+ C1).
- Templates, pipeline Make, planificateur : **tous validés**. On ne reconstruit rien, on produit.

---

## 1. Marque

- **Gus et Frost** — `gusetfrost.fr` — bien-être premium pour chiens et chats, marché **français**.
- **Promesse :** ramener le calme dans le foyer. Cœur émotionnel : *sérénité partagée*.
- **Voix :** calme, concrète, experte mais chaleureuse. **Jamais vendeuse, jamais alarmiste, jamais culpabilisante.** Vouvoiement.
- **Palette :** vert profond `#314431`, beige sable `#EFE7DA`, terracotta `#C16B47` (accent **rare**), vert sauge `#9DAE8B`.
- **Typo :** Fraunces (titres) + Inter Tight (corps/CTA).
- **Casse « GusetFrost.fr »** dans certains CTA de template : **volontaire**, ne pas corriger.
- **Typographie française :** espace insécable (U+00A0) avant `? ! : ;`.
- Tout sujet santé → renvoi au **vétérinaire**. Jamais de promesse thérapeutique.

---

## 2. La seule règle dure de Pinterest

**Règle d'or de la variété (anti-spam) :** pour une **même URL**, jamais deux épingles avec le **même modèle ET le même fond**.

- Format **2:3 / 1000 × 1500 px** obligatoire.
- Réutiliser un même fond sur **plusieurs URLs** est autorisé — la règle est par URL.
- Les kits respectent déjà cette règle (vérifié sur C13 : 0 doublon). **À revérifier par script**, jamais à l'œil.
- Une épingle Pinterest **ne meurt pas** (moteur de recherche visuel) : ne jamais republier à l'identique. Une « vague 2 » = de *nouvelles* épingles vers les *mêmes* articles, avec d'autres couples template+fond.

---

## 3. Les 8 templates (relookés, validés — **on ne les modifie pas**)

Aucun reskin par cluster : même univers, même marque. Le reskin ne se posera que pour le **chat** ou les **produits**.

| Template | Design ID Canva | Rôle | Accroche | Sujet du fond |
|---|---|---|---|---|
| **T1** | `DAHNwc1elDE` | Question | **Haut** (100-405), pastille verte | centre / bas |
| **T2** | `DAHNwZ-wyHI` | Émotionnel | **Haut** (86-387), pastille **sauge** | centre / bas |
| **T3** | `DAHNw_6Q80M` | Liste / chiffre | **Haut** (→630), gros chiffre | **bas** |
| **T4** | `DAHNw-aTIeE` | Guide | Haut-centre (254-620) **+ CTA au milieu (750)** | **bas** |
| **T5** | `DAHNw-kqEZk` | Diagnostic | **Bas** (panneau sauge, top 1056) | **haut / centre** |
| **T6** | `DAHNwytTcAw` | Contre-pied | **Centre** (611-780), ruban terracotta | haut **ou** bas, **jamais centre** |
| **T7** | `DAHNw2U5F5I` | Explication | Sous l'image (1110-1270) | centré dans l'encart |
| **T8** | `DAHNw4XJxxE` | Solution | **Haut** (35-327), pastille translucide | centre / bas |

- **CTA :** sur les 8, top **1400**, **une seule ligne** → ne pas dépasser ~36 caractères.
- **T5 est le seul « texte en bas »** → c'est lui qui contraint le plus les fonds.
- ⚠️ **Vérifier l'état réel dans Canva avant de conseiller** — ne jamais se fier à la mémoire : les positions ont bougé plusieurs fois.
- **Piège API Canva :** un cadre **vide est invisible** (`fills:[]`). « Aucun cadre » à l'inspection ≠ cadre absent.
- Certains templates gardent un **placeholder résiduel** caché derrière la photo : sans impact sur l'export.

---

## 4. Les fonds — cahier de cadrage ⚠️ LE POINT CRITIQUE

**C'est ici qu'on a perdu le plus de temps sur C1.** 11 fonds sur 22 avaient le chien trop bas → texte par-dessus le sujet → il a fallu déplacer T2, puis revenir en arrière sur T5.

**Règle :** le texte du template et le sujet du fond ne doivent **jamais occuper la même bande**.
Repères sur 1000×1500 : haut `0-500` · centre `500-1100` · bas `1100-1500`.

**À faire pour chaque fond :** lister les templates où il sert (via les CSV), prendre l'intersection des contraintes, et **écrire le cadrage dans le prompt image**.

| Sert sur | Phrase à ajouter à la scène |
|---|---|
| T1, T2, T8 | *« Le chien occupe la moitié basse du cadre, tiers supérieur dégagé (mur, sol ou flou). »* |
| T3, T4 | *« Le chien est dans le tiers inférieur, large espace vide au-dessus. »* |
| T5 | *« Le chien occupe la moitié haute du cadre, tiers inférieur dégagé. »* |
| T6 | *« Le chien est en haut ou en bas, jamais au centre. »* |
| T7 | *« Le chien est centré dans le cadre. »* |
| **T1 + T5** (contrainte double) | *« Le chien est centré verticalement (zone 450-1050 px). »* — la seule zone qui satisfait les deux |

### Le prompt image : méthode SOCLE + SCÈNE

**SOCLE (constant, à coller avant chaque scène) :**

> Photographie lifestyle éditoriale, format vertical portrait 2:3 (1000x1500 px), pour une épingle Pinterest. Style photoréaliste, qualité éditoriale, naturelle — pas d'illustration, pas de cartoon, pas de rendu 3D. Lumière naturelle douce. Palette de tons naturels et chaleureux (vert profond, beige sable, vert sauge, touche de terracotta), image ni trop claire ni délavée, du contraste et de la profondeur. Mise au point nette sur l'animal, léger flou d'arrière-plan. À ÉVITER : aucun texte ni lettrage, pas de logo, pas de filigrane, pas de visage humain net, pas de fond blanc clinique, pas de sursaturation, pas de membres ou traits déformés. SCÈNE :

Puis : **SCÈNE = description + phrase de cadrage** (tableau ci-dessus).

- Générer 2-3 variantes par scène, garder la plus nette.
- **Aucun texte dans l'image** — accroche et CTA s'ajoutent dans Canva.
- **Vraie photo obligatoire dès qu'un produit réel est montré** (IA = décors et ambiances uniquement).
- Nommage : `FOND_C__01_slug-court`. Ranger dans un dossier Canva `Fonds C__`.

---

## 5. Notion — **source de vérité**

- **Base :** « 🗓️ Calendrier éditorial »
- `data_source_id` : `dd95def5-119b-409f-a85e-95592f46a792`
- **Vue Pinterest :** `https://www.notion.so/8cd292df81c04080a372cc6c464a7d58?v=382c1254cd8481e58cb1000c3fda2e6f`
- **Champs :** `Titre` (= l'**accroche**), `CTA visuel`, `Fond`, `Modèle`, `Date de publication`, `Nom fichier`, `Lien destination`, `Statut`, `Cible`, `Contenu` (description Pinterest), `Texte alternatif`, `Tableau Pinterest`, `Image URL`
- Colonnes **`Prompt image` et `Decalage` : OBSOLÈTES**.

🔴 **Les entrées existent déjà pour TOUS les clusters** (créées par le processus cowork). **Ne rien créer, ne rien renommer.** Elles sont complètes : Titre, CTA (avec domaine et mot « article »), Fond, Modèle, Lien, Contenu, Tableau.

**Nommage : `PIN_AAAA-MM-JJ_{slug}-v{01-04}.png`** — c'est ce qui est dans Notion, et le pipeline fait une correspondance **stricte**. Toute divergence = épingle introuvable. *(La convention C1 `PIN_C1-…` est un héritage ; ne pas l'étendre.)*

**Requêtes qui marchent :**
```
notion-query-data-sources  →  {"data": {"data_source_urls": [...], "query": "SELECT ..."}}
notion-update-page         →  command="update_properties", UN appel par page (pas de batch)
```

---

## 6. Générer les 8 CSV du cluster

**Étape 1 — récupérer les données depuis Notion** (jamais depuis le .md du kit : ses CTA sont incomplets et son nommage diverge) :

```sql
SELECT "Nom fichier", "Titre", "CTA visuel", "Fond", "Modèle", "Statut"
FROM "collection://dd95def5-119b-409f-a85e-95592f46a792"
WHERE "Lien destination" IN ('/slug-1', '/slug-2', …)   -- les 13 URLs du cluster, prises dans le kit
ORDER BY "Modèle", "Nom fichier"
```

**Étape 2 — construire les CSV** (script rejouable, adapté de `build_csv_C13_notion.py`) :

| Colonne | Connectée dans Canva ? |
|---|---|
| `Nom fichier` | ❌ **NON** — sert au pipeline Make uniquement |
| `Accroche` | ✅ oui |
| `CTA visuel` | ✅ oui |
| `Chiffre` (T3 seulement) | ✅ oui |
| `Fond` | ❌ non — guide pour choisir l'image ligne par ligne |
| `Image` (colonne créée dans Canva) | ✅ **oui — sur le cadre de fond** |

Traitements à appliquer :
- **Accroche** = `Titre` Notion + espaces insécables.
- **CTA** = celui de Notion, **tel quel** (il porte déjà domaine + mot « article »).
- **T3** : extraire le chiffre en tête du `Titre` (« 10 signes d'un chien anxieux ») vers la colonne `Chiffre`, l'accroche devient « signes d'un chien anxieux ».
- **Fond** = `F09 · description de la scène` (description reprise du kit).

**Contrôles obligatoires avant livraison :**
```python
assert len(noms) == len(set(noms))                 # noms uniques
for url in urls: assert pas_de_doublon(modele, fond)   # règle d'or
assert max(len(cta)) <= 36                          # CTA sur une ligne
```

---

## 7. Procédure Bulk Create (rodée — suivre à la lettre)

1. Importer les fonds dans Canva (menu **Imports**).
2. Ouvrir le template `Tx`.
3. Bulk Create → **« Importer les données »** ⚠️ **jamais « saisir manuellement »** (l'insertion d'images y est cassée au-delà de la 1re ligne).
4. Charger le CSV → colonnes texte remplies automatiquement.
5. **Ajouter une colonne Image** (le tableau doit déjà avoir ses lignes), remplir **ligne par ligne** selon la colonne `Fond`.
6. 🔴 **CONNECTER LES DONNÉES — l'erreur n°1, celle qui revient à chaque fois.** Clic droit sur chaque élément → « Connecter les données » :
   - accroche → `Accroche`
   - CTA → `CTA visuel`
   - chiffre (T3) → `Chiffre`
   - **cadre de fond → `Image`** ← l'oubli classique : le texte apparaît, pas la photo
7. Générer → **vérifier que le sujet n'est pas couvert par le texte**.
8. **Supprimer les pages vides** — Canva exporte TOUTES les pages, y compris vides (c'était le bug « 22 pages au lieu de 8 »).
9. Exporter en PNG → nommer le ZIP **`C__T1.zip`** … **`C__T8.zip`**.
10. Déposer **un seul ZIP** dans `📥 ZIP à traiter` → lancer le scénario `6324761`.

**Ordre recommandé :** T2 → T4 → T5 → T6 → T7 → T1 → T3 → T8.
**Vérifier Notion avant chaque run** (statut « Brouillon ») **et après** (passage à « À dater »).

**Technique Canva utile :** l'effet **« Arrière-plan »** sur un champ texte fait tracer le panneau coloré **autour du texte réel**, quelle que soit la longueur de l'accroche. Déjà appliqué sur les 8 templates.

---

## 8. Le pipeline Make `6324761` — 9 modules

- **Org** `7996217` · **Team** `1912350` · Drive `8312683` · Notion `8104817` · Cloudinary `8313330`
- `📥 ZIP à traiter` = `1RvjoU7RihYN1bWdyey_zYkqozrfg3ZPp` · `📤 PNG prêts` = `1Qz04l86q6LOtmWNejDVtcyycNcgZlvA3`

```
1 google-drive:watchFilesInAFolder (limit 1)
2 google-drive:getAFile            (select:"value" → {{2.data}})
3 archive:UnpackAction             (champ = data, PAS sourceFile)
4 util:FunctionIncrement           (reset:"run" — sortie = i, PAS value)
5 util:SetVariable2 → targetName   (switch() sur le nom du ZIP)
6 google-drive:uploadAFile → 📤    (+ filtre `exist` sur targetName — gate tout l'aval)
7 cloudinary:UploadResource        (public_id SANS extension → sinon URL en .png.png)
8 notion:searchObjects1            (Nom fichier |&*^%$#@| rich_text / rich_text:equals)
9 notion:updateADatabaseItem       (Image URL = {{7.secure_url}} + Statut = « À dater »)
```

### ⚠️ À FAIRE pour chaque nouveau cluster
Le module 5 contient les noms de fichiers cibles indexés par le nom du ZIP. **Ajouter 8 branches `"C__T1"; "nom1,nom2,…"` au `switch`, sans toucher aux branches existantes.** Les clusters cohabitent ainsi sans risque.

### Cycle de vie des statuts
```
Brouillon → [Canva + pipeline 6324761] → À dater
          → [planificateur 6299952]    → À publier
          → [Publer 6261329]           → Programmé (Publer) → Publié
```
Le pipeline dit « l'image est prête ». Le planificateur dit « et voici quand ». *(Avant correction, le pipeline écrivait « À publier » et court-circuitait la datation — cause des dates périmées de C1.)*

### Leçons de débogage (ne pas les réapprendre)
- Canva nomme les fichiers du ZIP « untitled » → **seul l'ordre des pages compte**. L'ordre est **fiable** : page 1 = ligne 1 du CSV.
- `__IMTINDEX__` **n'est pas** accessible dans les formules.
- `Make:validate_module_configuration` est précieux, **mais** son énumération d'opérateurs Notion est fausse : **`rich_text:equals` marche en production**.
- Diagnostic très efficace : **injecter les variables dans le nom du fichier de sortie** (`idx_v={{4.value}}_i={{4.i}}.png`).
- Vider `📥 ZIP à traiter` avant chaque dépôt (un « T1 (1).zip » casse la clé du switch).
- **Ne pas** vider `📤 PNG prêts` : les PNG s'y accumulent, c'est leur place.

---

## 9. Le planificateur `6299952` — 🔴 UNE SEULE FOIS

Lit les épingles **Cible = Pinterest + Statut = À dater**, triées par `Nom fichier`, puis via `util:FunctionIncrement` (`reset:"run"`) :

```
position = ((i-1) × 95) mod 379      ← round-robin (379 est premier)
jour     = floor(position / 8)       ← 8 épingles/jour
date     = 2026-08-01 + jour
Statut   → « À publier »
```

Les variantes d'une même URL étant **consécutives** au tri (`-v01`…`-v04`), le pas de 95 les éloigne de ~11 jours : la règle des 7 jours est tenue **par construction**.
**Vérifié :** aucune collision, écart min 11 jours, max 8/jour, 01/08 → 17/09/2026.

🔴 **Ne le lancer QUE lorsque les 379 épingles sont TOUTES en « À dater ».** Les constantes `95 / 379 / 8` dépendent du total : le lancer sur un sous-ensemble, ou deux fois, produit des dates en collision. **Produire tous les clusters d'abord, planifier ensuite.**

---

## 10. Publer (dernière brique, non encore validée)

Le scénario `6261329` doit lire Notion (Cible = Pinterest, Statut = À publier) et produire un **CSV d'import Publer**. Le modèle est le scénario Facebook `6256355`, qui fonctionne :
- colonne **« Media URL(s) »** ← champ Notion **`Image URL`** (d'où Cloudinary : Publer a besoin d'une **URL publique**, il héberge l'image *après* import) ;
- date formatée `formatDate(...) 08:00` → **une date vide ou périmée casse la ligne**.

⚠️ **À vérifier au moment de brancher Publer :** la colonne **« Pin board »** du CSV (vide côté Facebook, mais indispensable pour Pinterest → c'est le champ `Tableau Pinterest` de Notion).

---

## 11. Ce que j'attends de toi (Claude)

1. **Vérifier l'état réel dans Canva et Notion avant de conseiller.** Ne jamais se fier à la mémoire ni au kit .md.
2. **Notion est la source de vérité** — les CSV en découlent, jamais l'inverse.
3. **Un template à la fois**, vérification avant et après chaque run, **pas de batch**.
4. **Me signaler les incohérences** plutôt que les contourner en silence.
5. **Corriger tes propres erreurs à voix haute** quand tu en trouves une.

**Priorité : automatisation + simplicité** sur l'artisanat épingle par épingle. Mes jugements de composition visuelle sont fiables : si je dis qu'un fond ne va pas, il ne va pas.

---

## Annexe — Les 83 URLs en « Brouillon » (4 épingles chacune)

À répartir par cluster d'après le kit correspondant (`Kit_production_C__*.md`, dans Drive → `Gus et Frost / Pinterest`). **Confirmer la liste exacte depuis le kit du cluster traité — ne pas deviner.**

```
/aides-anti-stress-inutiles              /amenager-promenades-chien-reactif
/amenager-vie-chien-anxieux              /anxiete-chien-alimentation
/anxiete-chien-races-predispositions     /anxiete-situationnelle-vs-generalisee
/apprendre-le-calme-chien                /attachement-sain-chien
/baillement-chien-stress                 /causes-anxiete-chien
/chien-anxieux-adopte                    /chien-anxieux-comprendre-apaiser
/chien-anxieux-quand-consulter           /chien-calme-serenite-quotidien
/chien-excitation-retrouvailles-invites  /chien-frustration-laisse-congeneres
/chien-hyperactif-trop-excite            /chien-hypersensible
/chien-hypervigilant                     /chien-leche-truffe-babines
/chien-petards-14-juillet                /chien-peur-bruit-phobie
/chien-peur-feux-artifice                /chien-peur-inconnus-autres-chiens
/chien-peur-orage                        /chien-peureux-en-ville
/chien-reactif-laisse                    /chien-reactif-quand-consulter
/chien-s-ebroue-signal                   /chien-surexcite-vue-autre-chien
/coherence-cadre-rassure-chien           /communiquer-calme-chien
/complements-calmants-chien              /crise-panique-sonore-chien
/croiser-chien-personne-promenade        /desensibiliser-chien-bruits
/echelle-stress-chien-morsure            /environnement-apaisant-chien-maison
/erreurs-chien-agite                     /erreurs-chien-anxieux
/erreurs-chien-qui-a-peur                /erreurs-communication-chien
/exercices-desensibilisation-chien-reactif  /faire-redescendre-chien-reactif
/gerer-ses-emotions-pour-son-chien       /gestes-qui-rassurent-chien
/gilet-anti-stress-couverture-ponderee-chien  /haletement-tremblements-chien-stress
/idees-recues-langage-canin              /langage-corporel-chien
/massage-ttouch-chien                    /mastication-lechage-chien
/materiel-chien-reactif                  /musique-apaisante-chien
/observer-chien-carnet-signaux           /oeil-de-baleine-chien
/oreilles-chien-emotions                 /pheromones-apaisantes-chien
/postures-stress-chien                   /pourquoi-chien-peur-bruits
/promenade-depense-chien-equilibre       /queue-chien-signification
/rassurer-chien-moment-difficile         /rassurer-chien-qui-a-peur
/rassurer-sans-surproteger               /rassurer-son-chien
/reactivite-chien                        /reactivite-chien-comprendre
/reactivite-peur-agression-difference    /rester-calme-chien-agite
/routine-apaisement-chien                /routine-rythme-quotidien-chien
/seuil-de-reactivite-chien               /signaux-apaisement-chien
/signaux-humains-vers-chien              /signes-chien-anxieux
/solutions-apaiser-chien                 /sommeil-du-chien
/stimulation-mentale-chien               /stress-se-transmet-chien
/suivre-progres-chien-anxieux            /tapis-fouille-chien
/tapis-lechage-apaiser-chien
```

Les **13 URLs de C13** (déjà traité, pour référence) : `/chien-anxieux-comprendre-apaiser`, `/signes-chien-anxieux`, `/anxiete-situationnelle-vs-generalisee`, `/chien-hypervigilant`, `/chien-hypersensible`, `/causes-anxiete-chien`, `/chien-anxieux-quand-consulter`, `/amenager-vie-chien-anxieux`, `/chien-anxieux-adopte`, `/erreurs-chien-anxieux`, `/anxiete-chien-races-predispositions`, `/anxiete-chien-alimentation`, `/suivre-progres-chien-anxieux`.
