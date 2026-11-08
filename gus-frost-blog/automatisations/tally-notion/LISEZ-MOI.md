# Questionnaire Tally → Notion (Le Programme du Foyer Apaisé)

Chaîne en production depuis le 7 novembre 2026 :

```
Tally (formulaire pbgAZZ) → webhook → Make (scénario 8430553) → Notion (3 bases) → e-mail
```

| Maillon | Identifiant |
|---|---|
| Formulaire Tally | `pbgAZZ`, public sur `https://tally.so/r/pbgAZZ` |
| Webhook Make | `4058042`, zone **eu1** (donc UE) |
| Scénario Make | `8430553`, équipe 1912350, organisation 7996217 |
| Base Clients | `3ddfde7b-711d-4824-8cd7-c7f893911dc0` |
| Base Animaux | `de7e8e55-5bb7-4521-8aa1-eab0d6431faf` |
| Base Dossiers | `6cfb904e-03b1-44b6-8f18-0be7f2656ddf` |

## Ce que fait le scénario

1. Reçoit la soumission.
2. Cherche le client par e-mail dans **Clients**.
3. S'il est inconnu, crée sa fiche ; sinon, la réutilise.
4. Crée la fiche **Animal**, reliée au client.
5. Crée le **Dossier**, relié à l'animal, avec le motif, le niveau de risque
   et le statut vétérinaire.
6. Écrit le questionnaire **dans le corps de la page Dossier**, en vrais blocs
   Notion : deux intitulés et vingt-deux lignes « étiquette en gras : réponse ».
7. Rafraîchit la fiche Client : dernier contact, consentements et leurs dates.
8. Prévient `contact@gusetfrost.fr`.

Coût : 9 à 10 opérations Make par questionnaire.

## Régénérer le blueprint

```
python -I blueprint_v2.py blueprint.json
```

puis pousser le contenu de `blueprint.json` dans le scénario 8430553.
Le script lit `schema_formulaire_pbgAZZ.json`, qui est le schéma du formulaire
publié (extrait par `extrait_tally.py` depuis `https://tally.so/r/pbgAZZ`).
Il refuse de livrer si un saut de ligne traîne dans le blueprint, si une
insécable manque devant un signe double, ou si un libellé cherché dans la
charge utile Tally n'existe pas dans le formulaire.

## Les pièges, tous rencontrés et tous payés comptant

1. **Tally n'envoie pas l'intitulé affiché de la question.** Le champ `label`
   de la charge utile porte le **nom interne** du bloc (`Nom du chien`,
   `Niveau de risque`, `Consentement e-mail`…), pas le titre vu par le client
   (`Son nom`, `Y a-t-il déjà eu un contact physique…`). `noms_champs.py`
   affiche la correspondance. Avantage : ces noms ne contiennent aucune
   espace insécable, contrairement aux titres.

2. **Le type Notion s'écrit `rich_text`, pas `text`.** Avec `"type": "text"`,
   Make envoie une propriété vide et Notion répond
   `400 body failed validation … should be defined, instead was undefined`,
   en nommant deux propriétés au hasard. Le message ne désigne pas le
   coupable : chercher les champs texte.

3. **La connexion Make doit être ajoutée à la page Notion parente.**
   `Dossiers clients — Le Programme du Foyer Apaisé` → menu `•••` → Plus →
   Connexions → Make. Sans cela : `404 Could not find data_source`.
   Dans l'interface Notion, le sous-menu ne s'ouvre qu'avec un **survol
   progressif** de la souris ; un clic direct le referme.

4. **Rejouer une charge utile depuis le navigateur exige `mode: 'cors'`.**
   En `no-cors`, le navigateur rétrograde le `Content-Type` en `text/plain`,
   Make ne parse pas le JSON et toutes les formules renvoient du vide.

5. **Le module Notion de Make remplace tout saut de ligne par la chaîne
   littérale « <br /> »** dans une propriété texte. Mesuré le 08/11/2026 : un
   saut, deux sauts et un saut produit par une formule (`decodeURL("%0A")`)
   donnent tous le même résultat, car le remplacement a lieu après l'évaluation
   de la formule. **Aucun saut de ligne ne peut donc atteindre une propriété
   Notion par Make.** Les deux textes longs passent désormais par le corps de
   la page, où chaque ligne est un bloc.

6. **Un contenu réduit à « espace + formule » est ramené par Make à la valeur
   brute**, espace comprise. L'espace qui sépare l'étiquette de la réponse est
   donc un troisième fragment de texte, statique, à part.

7. **Un champ numérique renvoie un nombre**, et Notion exige une chaîne dans un
   bloc : d'où le `toString()` autour de chaque valeur.

8. **Une erreur arrête le scénario.** Make le désactive et garde la charge utile
   dans la file du webhook. Après correction : réactiver, puis vider la file
   (un `scenarios_run` suffit, il consomme la soumission en attente).

## Ce qu'il faut savoir sur les données écrites

- Les propriétés **« Analyse »** et **« Réponses brutes »** de la base Dossiers
  ne sont plus remplies : leur contenu est dans le corps de la page. Elles
  peuvent être supprimées de la base, ou « Analyse » gardée pour les notes
  personnelles. Elles plafonnaient de toute façon à 2 000 caractères.
- Une réponse de plus de **1 900 caractères est coupée** (`substring`), pour la
  même raison : un bloc Notion plafonne à 2 000 caractères, et une erreur ferait
  perdre tout le questionnaire. L'original reste consultable dans Tally.
- Un champ laissé vide s'écrit **« non renseigné »** plutôt que rien.

## Reste à faire

- **Huit questions à choix multiples ne sont pas reprises** : contexte
  d'apparition, déclencheurs, enfants au foyer, solitude, type de sorties,
  matériel, occupation, signes de douleur. Elles ne sont ni dans les bases ni
  dans le corps du Dossier, alors que les déclencheurs et les signes de douleur
  comptent cliniquement. Tally envoie un champ booléen par option, ce qui rend
  la reconstitution possible mais verbeuse ; à ajouter si Régis le souhaite.
- Dédoublonnage des **Animaux** : une seconde commande du même client pour le
  même chien créerait une deuxième fiche animal. Le dédoublonnage n'est posé
  que sur Clients.
- Signature du webhook (Tally sait signer ; Make ne vérifie pas encore).
- Purge annuelle des fiches échues (propriété « À purger le » déjà calculée).
