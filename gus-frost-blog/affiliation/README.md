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
| `page_ambassadeurs.html` + `deploy_page.py` | La page vitrine Shopify (`/pages/programme-ambassadeurs`). |
| `push_commissions_klaviyo.py` | Envoie le récap mensuel vers Klaviyo (1 événement/ambassadeur). |
| `email_recap_klaviyo.html` | Le modèle d'e-mail de marque à coller dans le Flow Klaviyo. |
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
récap à l'écran. Ce CSV alimente les e-mails Klaviyo (étape 4).

### 4. Envoyer le récap par e-mail (Klaviyo)
```bash
python affiliation/push_commissions_klaviyo.py --mois 2026-07 --dry-run   # aperçu
python affiliation/push_commissions_klaviyo.py --mois 2026-07             # envoi réel
```
Chaque ambassadeur reçoit un e-mail personnalisé avec ses chiffres du mois.

## Déployer la page vitrine
```bash
python affiliation/deploy_page.py --dry-run   # vérifie
python affiliation/deploy_page.py             # crée /pages/programme-ambassadeurs
```
La page utilise le **formulaire de contact natif Shopify** : les candidatures
arrivent sur l'e-mail de contact de la boutique (Réglages → Général). Zéro app.

## Configurer Klaviyo (une seule fois)

1. **Clé API privée** : Klaviyo → Settings → API keys → *Create Private API Key*
   (scope *Events: Write* et *Profiles: Write*). Colle-la dans `.env` :
   `KLAVIYO_PRIVATE_KEY=pk_...`
2. **Modèle d'e-mail** : crée un template Klaviyo, mode HTML, colle le contenu de
   `email_recap_klaviyo.html`. (Règle Montserrat/Lora dans Klaviyo si tu veux tes
   polices ; l'e-mail utilise des polices web-safe par défaut.)
3. **Flow** : Flows → Create → *Metric-triggered* → métrique
   **« Récap commission ambassadeur »**. La métrique n'apparaît dans Klaviyo
   qu'après le **1er envoi réel** (pas le dry-run) : fais donc un premier push
   réel d'un mois, puis construis le Flow. Ajoute une action *Email* utilisant le
   modèle. Pense à autoriser l'envoi aux profils concernés (ambassadeurs = liste
   consentie via le formulaire de candidature).
4. Chaque mois : lance l'étape 3 (calcul) puis l'étape 4 (push). Le Flow fait le reste.

Variables disponibles dans l'e-mail : `{{ person.first_name }}`,
`{{ event.mois_affichage }}`, `{{ event.nb_commandes }}`, `{{ event.ca_affichage }}`,
`{{ event.commission_affichage }}`, `{{ event.taux_affichage }}`, `{{ event.code }}`.

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
