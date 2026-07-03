# Déploiement du cluster C4 (langage corporel) sur Shopify

Le contenu est prêt : 13 fragments dans `articles/cluster-4-langage-corporel/`, images déjà
sur le CDN Shopify, liens internes en `/blogs/chiens/…`, collection `/collections/stress`,
CTA conforme. Le script crée les 13 articles dans le blog **« Chiens »** (handle `chiens`).

## 1. Obtenir un token Admin API
Admin Shopify → **Paramètres → Applications et canaux de vente → Développer des apps** →
créer une app → **Configurer les scopes Admin API** : cocher `write_content` (et `read_content`)
→ **Installer** → copier le **token d'accès Admin API** (`shpat_…`).

## 2. Lancer (à la racine du repo)
```bash
export SHOPIFY_SHOP=TONSHOP.myshopify.com        # domaine .myshopify.com (pas gusetfrost.fr)
export SHOPIFY_ADMIN_TOKEN=shpat_xxxxxxxxxxxxx
python3 deploy/deploy_c4_to_shopify.py           # crée les 13 articles EN BROUILLON
```
- Idempotent : relançable sans créer de doublons (met à jour si le handle existe déjà).
- Pour publier directement au lieu de brouillon : `PUBLISH=true python3 deploy/deploy_c4_to_shopify.py`

## 3. Relire puis publier
Les articles sont créés en **brouillon**. Relis-les dans l'admin (blog « Chiens »),
vérifie le rendu (le CSS `gf-article` vient du thème, déjà en place pour C1-C3), puis publie.

## Notes
- Blog cible : « Chiens » = `gid://shopify/Blog/103894909149` (modifiable via `SHOPIFY_BLOG_ID`).
- SEO : méta-titre/description posés en métachamps `global.title_tag` / `global.description_tag`.
- Auteur : « Gus & Frost ». Tags repris du `manifest.csv`.
