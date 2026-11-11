# Questionnaire Tally → Notion (Le Programme du Foyer Apaisé)

Chaîne en production depuis le 7 novembre 2026 :

```
Tally (formulaire pbgAZZ) → webhook → Make (scénario 8430553) → Notion (3 bases) → e-mail
```

| Maillon | Identifiant |
|---|---|
| Formulaire Tally | `pbgAZZ`, public sur `https://tally.so/r/pbgAZZ` |
| Webhook Make | `4058042`, zone **eu1** (donc UE), capture des en-têtes activée |
| Scénario Make | `8430553`, équipe 1912350, organisation 7996217 |
| Purge RGPD | scénario Make `8509120`, le 1ᵉʳ de chaque mois à 6 h |
| Base Clients | `3ddfde7b-711d-4824-8cd7-c7f893911dc0` |
| Base Animaux | `de7e8e55-5bb7-4521-8aa1-eab0d6431faf` |
| Base Dossiers | `6cfb904e-03b1-44b6-8f18-0be7f2656ddf` |

## Ce que fait le scénario

1. Reçoit la soumission, et ne traite que ce qui porte `eventType = FORM_RESPONSE`
   et `formId = pbgAZZ`.
2. Cherche le client par e-mail dans **Clients** ; s'il est inconnu, le crée.
3. **Le recherche à nouveau**, pour disposer de son identifiant dans tous les cas.
4. Cherche l'animal par **son nom ET son client** ; s'il est inconnu, le crée,
   puis le recherche à nouveau.
5. Crée le **Dossier**, relié à l'animal, avec le motif, le niveau de risque et
   le statut vétérinaire.
6. Écrit le questionnaire **dans le corps de la page Dossier**, en vrais blocs
   Notion : deux intitulés et trente lignes « étiquette en gras : réponse ».
7. Rafraîchit la fiche Client : dernier contact, consentements et leurs dates.
8. Prévient `contact@gusetfrost.fr`.

Coût : 11 à 12 opérations Make par questionnaire.

## Rejouer une soumission

```
python -I charge_utile_test.py <url du webhook> [--nom ZZTest] [--email x@y]
```

Le script lit le schéma du formulaire publié et fabrique une charge utile de la
même forme que celle de Tally (118 champs, les vrais identifiants d'options).
C'est le seul moyen de tester la chaîne sans remplir les sept pages à la main.
L'URL du webhook se passe en argument : c'est un secret, elle n'est pas écrite
dans le dépôt.

## Régénérer le blueprint

```
python -I blueprint_v2.py blueprint.json
```

puis pousser le contenu de `blueprint.json` dans le scénario 8430553.
Le script lit `schema_formulaire_pbgAZZ.json`, extrait par `extrait_tally.py`.
Il refuse de livrer si le blueprint contient un saut de ligne, s'il manque une
insécable devant un signe double, si un libellé Tally est inconnu, ou **si une
formule référence un module situé dans une autre route**.

## Les pièges, tous rencontrés et tous payés comptant

1. **Tally n'envoie pas l'intitulé affiché de la question.** Le champ `label`
   de la charge utile porte le **nom interne** du bloc (`Nom du chien`,
   `Niveau de risque`…), pas le titre vu par le client (`Son nom`).
   `noms_champs.py` affiche la correspondance. Avantage : ces noms ne
   contiennent aucune espace insécable, contrairement aux titres et aux textes
   d'options.

2. **Le type Notion s'écrit `rich_text`, pas `text`.** Avec `"type": "text"`,
   Make envoie une propriété vide et Notion répond
   `400 body failed validation … should be defined, instead was undefined`,
   en nommant deux propriétés au hasard.

3. **La connexion Make doit être ajoutée à la page Notion parente.**
   `Dossiers clients — Le Programme du Foyer Apaisé` → menu `•••` → Plus →
   Connexions → Make. Sans cela : `404 Could not find data_source`. Le
   sous-menu Notion ne s'ouvre qu'avec un **survol progressif** de la souris.

4. **Rejouer une charge utile depuis le navigateur exige `mode: 'cors'`.**
   En `no-cors`, le `Content-Type` est rétrogradé et Make ne parse pas le JSON.
   `charge_utile_test.py` évite entièrement le navigateur.

5. **Le module Notion de Make remplace tout saut de ligne par « <br /> »**
   dans une propriété texte. Mesuré le 08/11/2026 : un saut, deux sauts et un
   saut produit par une formule donnent le même résultat, le remplacement ayant
   lieu après l'évaluation. Aucun saut de ligne ne peut donc atteindre une
   propriété ; les textes longs vont dans le corps de la page.

6. **Un contenu réduit à « espace + formule » est ramené par Make à la valeur
   brute**, espace comprise. L'espace qui sépare l'étiquette de la réponse est
   donc un troisième fragment de texte, statique, à part.

7. **Un champ numérique renvoie un nombre**, que Notion refuse dans un bloc :
   d'où le `toString()` autour de chaque valeur.

8. **Un module ne peut pas lire la sortie d'un module situé dans une AUTRE
   route du routeur.** Make résout la référence par du vide, sans rien dire.
   `ifempty(get(map(3.array; "id"); 1); 5.id)` ne valait donc rien dès que la
   route 1 venait de créer le client : **la chaîne échouait à la fiche Animal
   pour tout client nouveau**, et seule la présence préalable du client la
   faisait passer. Remède : après le routeur, rechercher à nouveau la fiche.
   Le garde-fou `controle_routes` refuse désormais ce motif, et `essai_garde.py`
   vérifie le garde-fou lui-même.

9. **Make n'expose les en-têtes que si la capture est activée sur le hook**
   (`data.headers`), et il les expose sous **`__IMTHEADERS__`** : un *tableau*
   d'objets `name`/`value`, dont les noms sont en **minuscules**. Un accès du
   genre `1.headers.x-gf-jeton` ne résout rien, et un filtre bâti dessus
   bloque tout sans rien dire. La bonne lecture, mesurée le 11/11/2026 :

   ```
   {{get(map(1.__IMTHEADERS__; "value"; "name"; "x-gf-jeton"); 1)}}
   ```

10. **Une erreur arrête le scénario.** Make le désactive et garde la charge
    utile dans la file du webhook. Après correction : réactiver, puis vider
    la file (un `scenarios_run` suffit, il consomme la soumission en attente).

11. **Une question à cases se relit en une formule, pas en huit.** Tally
    envoie les identifiants cochés dans `value` et le dictionnaire
    identifiant → texte dans `options`. Le quatrième argument de `map()`
    accepte plusieurs valeurs séparées par une virgule, donc :

    ```
    join(map(options; "text"; "id"; join(value; ",")); " · ")
    ```

    Le séparateur est un point médian et non une virgule : trois options
    en contiennent une (« Décès, humain ou animal »). Vérifié le
    11/11/2026 sur les huit questions, avec plusieurs cases cochées.
    Les booléens par option que Tally envoie en plus ne servent à rien.

## Ce qu'il faut savoir sur les données écrites

- Les propriétés « Analyse » et « Réponses brutes » ont été **supprimées** de la
  base Dossiers le 11/11/2026 : leur contenu est dans le corps de la page, et
  elles plafonnaient de toute façon à 2 000 caractères.
- Une réponse de plus de **1 900 caractères est coupée** (`substring`), pour la
  même raison : un bloc Notion plafonne à 2 000 caractères, et une erreur ferait
  perdre tout le questionnaire. L'original reste consultable dans Tally.
- Les **huit questions à cases** (contexte d'apparition, déclencheurs,
  enfants au foyer, solitude, type de sorties, matériel, occupation, signes
  de douleur) sont recopiées depuis le 11/11/2026, une ligne chacune, les
  réponses cochées séparées par un point médian.
- La date du dernier examen vétérinaire n'est recopiée nulle part : elle
  ne se lit que dans Tally.
- Un champ laissé vide s'écrit **« non renseigné »** plutôt que rien.
- Un animal existant **n'est pas mis à jour** : son âge et son poids restent
  ceux de la première commande. C'est voulu, pour ne pas écraser une correction
  faite à la main.

## La purge RGPD (scénario 8509120)

Le 1ᵉʳ de chaque mois, les fiches Clients dont « À purger le » (dernier contact
+ 3 ans) est échu passent au statut « À purger » et déclenchent un e-mail.
**La suppression reste manuelle**, et volontairement : elle doit entraîner celle
des fiches Animal et Dossier liées, et une purge automatique qui se tromperait
de filtre détruirait des dossiers clients sans retour possible.
Chaque fiche n'est signalée qu'une fois, le statut servant de mémoire.

## Reste à faire

- **La signature du webhook : deux collages, dans cet ordre.** Tout le
  câblage est fait et mesuré, il ne manque que la valeur du jeton, que
  l'environnement m'interdit de manipuler. Le jeton est dans le `.env`
  sous `JETON_WEBHOOK_TALLY`.

  1. **Tally d'abord** : formulaire → Integrations → Webhooks → Edit →
     « Add HTTP headers » → nom `X-Gf-Jeton`, valeur = le jeton. Tant que
     Make ne vérifie rien, cet en-tête est simplement ignoré : aucune
     coupure.
  2. **Make ensuite** : scénario 8430553 → le filtre « Une soumission
     de CE formulaire » → ajouter une règle **ET** → à gauche l'expression
     du piège 9, opérateur **`Text: Equal to`**, à droite le même jeton.

  Vérifié le 11/11/2026 sur un webhook jetable : avec le bon jeton la
  charge utile passe, en-tête absent ou valeur fausse elle est écartée. Le
  mécanisme est donc fermé par défaut.

  **Le générateur connaît cette règle** : il lit `JETON_WEBHOOK_TALLY` dans
  l'environnement et, s'il le trouve, ajoute la troisième condition de
  lui-même, en refusant alors d'écrire le blueprint dans un dossier
  versionné ou synchronisé. Sans le jeton, il produit un blueprint **sans**
  vérification et l'annonce en clair. Donc : un `blueprint.json` du dépôt
  poussé tel quel **retire la signature**. Pour la garder, régénérer avec le
  jeton en environnement, vers un fichier hors dépôt, et l'importer dans Make.
- Un questionnaire envoyé sans e-mail (formulaire ouvert hors du lien de
  commande) créerait une fiche client sans adresse. Non traité.
