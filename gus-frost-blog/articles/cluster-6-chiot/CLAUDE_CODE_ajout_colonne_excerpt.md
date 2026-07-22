# Prompt Claude Code — Ajout de la colonne `excerpt` au manifest et backfill C1 à C5

> À coller dans une conversation Claude Code, à la racine du repo `gus-frost-blog`.
> Fichier requis dans le dossier de travail : `manifest_excerpts_C1-C5.csv` (colonnes `cluster_num,slug,excerpt`).
> À lancer de préférence après que les lignes C5 sont déjà présentes dans `manifest.csv`, pour que tous les articles soient couverts en une passe. La passe est idempotente : une seconde exécution ne casse rien.

---

Tu fais évoluer le schéma de `manifest.csv` en y ajoutant une colonne `excerpt` (résumé de blog Shopify), puis tu la remplis pour tous les articles existants.

## 1. Ajout de la colonne
Insère une nouvelle colonne `excerpt` dans `manifest.csv`, **juste après la colonne `meta_description`**. Le nouvel ordre des colonnes devient :

```
cluster_num,cluster_tag,type,slug,parent_pilier_slug,title,meta_title,meta_description,excerpt,tags,file,prompts_file,links_to_resolve,images_to_resolve
```

Mets à jour la ligne d'en-tête en conséquence, et décale toutes les lignes de données pour respecter le nouvel ordre (chaque valeur existante conserve sa colonne d'origine, l'`excerpt` s'intercale, vide pour l'instant).

## 2. Backfill depuis le fichier fourni
Pour chaque ligne de `manifest.csv`, renseigne la colonne `excerpt` en cherchant le `slug` correspondant dans `manifest_excerpts_C1-C5.csv` et en recopiant le texte de la colonne `excerpt`. Respecte les règles CSV (le champ contient des virgules et des guillemets « » : encadre-le de guillemets doubles et échappe correctement).

## 3. Vérifications
- La ligne d'en-tête contient bien `excerpt` en 9e position, juste après `meta_description`.
- Toutes les lignes de données ont un `excerpt` non vide. Liste les slugs éventuellement non trouvés dans le fichier de correspondance (il ne devrait en rester aucun pour C1 à C5).
- Le nombre de colonnes est identique sur toutes les lignes (14).
- Aucune autre valeur n'a été modifiée ou décalée par erreur.

## 4. Commit
Travaille sur une branche `manifest-colonne-excerpt`, commit avec le message `Ajout colonne excerpt au manifest et backfill C1 à C5`, puis ouvre une pull request vers `main`. Ne modifie aucun autre fichier que `manifest.csv`.

---

**Note pour la suite (C6 et au-delà) :** la colonne `excerpt` fait désormais partie du schéma standard du manifest. Les nouveaux clusters doivent la renseigner dès leur création, sans repasser par un backfill.
