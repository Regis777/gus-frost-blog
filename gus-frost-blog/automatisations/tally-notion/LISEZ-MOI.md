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
5. Crée le **Dossier**, relié à l'animal, avec le motif, le niveau de risque,
   le statut vétérinaire, l'analyse et le digest des réponses.
6. Rafraîchit la fiche Client : dernier contact, consentements et leurs dates.
7. Prévient `contact@gusetfrost.fr`.

Coût : 8 à 9 opérations Make par questionnaire.

## Régénérer le blueprint

```
python -I blueprint_v2.py blueprint.json
```

puis pousser le contenu de `blueprint.json` dans le scénario 8430553.
Le script lit `schema_formulaire_pbgAZZ.json`, qui est le schéma du formulaire
publié (extrait par `extrait_tally.py` depuis `https://tally.so/r/pbgAZZ`).

## Quatre pièges, tous rencontrés le 07/11/2026

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

## Défaut cosmétique connu

Dans les propriétés texte de Notion, Make convertit les sauts de ligne en
`<br />` littéraux, visibles dans « Réponses brutes » et « Analyse ».
Le contenu est complet et dans l'ordre ; seule la présentation souffre.

## Reste à faire

- Dédoublonnage des **Animaux** : une seconde commande du même client pour le
  même chien créerait une deuxième fiche animal. Le dédoublonnage n'est posé
  que sur Clients.
- Signature du webhook (Tally sait signer ; Make ne vérifie pas encore).
- Purge annuelle des fiches échues (propriété « À purger le » déjà calculée).
