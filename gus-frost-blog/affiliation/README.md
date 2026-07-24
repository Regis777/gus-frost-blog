# Programme Ambassadeurs — moteur codes promo

Alternative maison à Goaffpro, sans app tierce, sans serveur, sans abonnement.
**Le code promo de chaque ambassadeur EST la clé d'attribution** : Shopify compte
nativement les commandes portant un code, donc pas de cookie ni de tracking fragile.

## Fichiers

| Fichier | Rôle |
|---|---|
| `ambassadeurs.csv` | **La source de vérité.** Un ambassadeur par ligne. C'est le seul fichier que tu édites à la main. |
| `creer_codes.py` | Crée sur Shopify les codes promo des ambassadeurs `actif` (idempotent). |
| `calcul_commissions.py` | Attribue les ventes du mois par code et calcule les commissions. |
| `moteur.py` | Briques communes (réutilise le client Shopify de `scripts/publish.py`). |
| `rapports/` | Rapports mensuels générés (`commissions_AAAA-MM.csv`). Créé automatiquement. |

Aucune dépendance à installer : stdlib Python uniquement, comme le reste de la pipeline.
Le `.env` (racine du dépôt) fournit les identifiants Shopify — déjà en place.

## Le registre `ambassadeurs.csv`

```
code,prenom,nom,email,taux,remise_client,statut,date_inscription,reseaux,notes
SOPHIE15,Sophie,Durand,sophie@exemple.fr,0.10,15,actif,2026-07-24,instagram.com/sophie,
```

- **code** : le code promo, unique, en MAJUSCULES, sans espace (ex. `SOPHIE15`).
- **taux** : ta commission, en décimal. `0.10` = 10 %.
- **remise_client** : la remise offerte à sa communauté, en %. `15` = −15 %.
- **statut** : `actif` (traité), `en_attente`, `inactif` ou `exemple` (ignorés par `creer_codes`).
- Les colonnes `reseaux` / `notes` sont libres (pour toi), les scripts les ignorent.

## Workflow

### 1. Ajouter un ambassadeur
Ajoute une ligne dans `ambassadeurs.csv`, `statut=actif`, choisis son `code`.

### 2. Créer ses codes promo sur Shopify
```bash
python affiliation/creer_codes.py --dry-run   # vérifie ce qui va être créé (aucune écriture)
python affiliation/creer_codes.py             # crée réellement les codes manquants
```
Idempotent : relançable sans risque, ne recrée jamais un code existant.

### 3. Calculer les commissions du mois
```bash
python affiliation/calcul_commissions.py                 # mois précédent (défaut)
python affiliation/calcul_commissions.py --mois 2026-07  # un mois précis
python affiliation/calcul_commissions.py --mois 2026-07 --base brut --details
```
Produit `rapports/commissions_AAAA-MM.csv` (une ligne par ambassadeur payé) + un
récap à l'écran. Ce CSV alimentera ensuite les e-mails Klaviyo (étape suivante).

## Base de commission

Par défaut la commission se calcule sur le **net** (sous-total produits après la
remise ambassadeur, hors livraison et taxes) : tu paies sur ce que le client a
réellement dépensé. `--base brut` calcule sur le total avant remise, si tu préfères.

## Limites assumées (MVP)

Ce moteur couvre : codes uniques, attribution fiable, calcul et rapport mensuel.
Il ne fait PAS (volontairement, à ton échelle actuelle) : portail avec login
temps réel, inscription 100 % en libre-service, ni versement automatique des
paiements. Ces briques ne se justifient qu'au passage à grande échelle
(cf. la discussion « app auto-hébergée vs Goaffpro »).
