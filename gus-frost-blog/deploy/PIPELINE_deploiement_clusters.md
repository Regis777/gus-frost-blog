# Pipeline de déploiement des clusters — process standardisé

Objectif : rendre chaque nouveau cluster **turnkey**, sans travail manuel répété. Deux scripts génériques remplacent le clonage et l'alignement à la main.

## Les deux scripts génériques (à réutiliser tels quels)

**1. `scripts/ingest_cluster.py`** — stage un cluster produit (dossier Cowork) vers le repo.
Il fait, pour n'importe quel cluster N, tout ce qui était manuel :
- copie les fragments datés `AAAA-MM-JJ_(PILIER|SATxx)_<slug>_v1.html` en `articles/cluster-N-<tag>/<slug>.html`,
- construit `C<N>_images_map.csv` à partir des marqueurs « Image N » des fragments (num, nouveau_fichier hero-/-n, article_slug, role, alt),
- renomme les images `1.png…K.png` en `images/cluster-N-<tag>/<nouveau_fichier>.png`,
- écrit `manifest_C<N>_rows.csv` aligné (type `PILIER`/`SATxx`, `file` = chemin repo),
- **append-only** des lignes dans `manifest.csv` (ignoré si les slugs existent déjà).

```bash
python scripts/ingest_cluster.py --cluster 8 --src "<dossier Cowork du cluster>"          # PLAN (aucune écriture)
python scripts/ingest_cluster.py --cluster 8 --src "<dossier Cowork du cluster>" --apply  # exécute
```

**2. `deploy/deploy_cluster.py`** — déploie n'importe quel cluster (auto-découverte par numéro).
Remplace les `deploy_cN_to_shopify.py`. Transforme les fragments (retire `<style>`/`<h1>`, résout `PLACEHOLDER_` → `/blogs/chiens/`, insère les `<img>`), crée les articles **en brouillon** (upsert idempotent), image à la une = hero, `summary_html` = excerpt.

```bash
python deploy/deploy_cluster.py --cluster 8 --dry-run   # récap + diagnostic, aucune écriture
python deploy/deploy_cluster.py --cluster 8 --bake      # upload images + crée/MAJ les brouillons
```

## Flux complet d'un cluster (de la production au déploiement)

1. **Production (Cowork)** : arborescence validée → 13 articles deploy-ready (`shared.py`/`build.py`/`check.py`), prompts d'images, maillage, `manifest_C<N>_rows.csv`, dossier `images/`.
2. **Images** : Régis crée les visuels et les dépose `1.png…K.png` dans le dossier `images/` du cluster (ordre de création).
3. **Ingestion** : `python scripts/ingest_cluster.py --cluster N --src "…" --apply` (une commande).
4. **Contrôle** : `python scripts/check_cluster.py --dir articles/cluster-N-<tag> --faq 5` → viser 13 OK / 0 WARN / 0 FAIL.
5. **Dry-run** : `python deploy/deploy_cluster.py --cluster N --dry-run` → 0 anomalie attendue.
6. **Bake** : `python deploy/deploy_cluster.py --cluster N --bake` (après revue) → brouillons créés.
7. **Git** : branche `deploy/cN-<tag>`, commit, PR (pas de merge auto).

## Garde-fous permanents
- Draft-first : `published=false` ; jamais `--publish` sans validation explicite.
- `manifest.csv` **append-only** ; ne jamais réécrire les lignes existantes ni toucher aux clusters en ligne.
- Blog `chiens` uniquement ; images sur **Shopify Files** (pas Cloudinary).
- Tout passe par `--dry-run` avant `--bake`.

---

## PROMPT CLAUDE CODE — modèle réutilisable (remplacer N et le dossier)

> Colle ceci dans Claude Code à la racine du repo `gus-frost-blog`, en remplaçant `N` et le chemin source.

```
Déploie le cluster CN dans le blog « chiens » de Gus & Frost, en brouillon, avec le pipeline standardisé.

1. Ingestion (si pas déjà staged) :
   python scripts/ingest_cluster.py --cluster N --src "Blogs cowork/CN-<tag>"
   Vérifie le PLAN, puis relance avec --apply.
2. Contrôle : python scripts/check_cluster.py --dir articles/cluster-N-<tag> --faq 5  (attendu 13 OK / 0 WARN / 0 FAIL).
3. Dry-run : python deploy/deploy_cluster.py --cluster N --dry-run
   STOP : montre-moi le récap (13 articles, 0 anomalie) et attends mon « go ».
4. Après mon « go » : python deploy/deploy_cluster.py --cluster N --bake
5. Git : crée la branche deploy/cN-<tag>, commit (articles + images + manifest), ouvre une PR sans merger.

Règles : draft-first (jamais --publish sans validation), manifest.csv append-only, blog chiens uniquement, images sur Shopify Files. Si une anomalie apparaît au contrôle ou au dry-run, arrête-toi et signale-la.
```
