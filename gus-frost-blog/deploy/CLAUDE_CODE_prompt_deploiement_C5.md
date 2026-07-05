# Prompt Claude Code — Déploiement du cluster C5 (repas / gamelle)

> À coller tel quel dans Claude Code, à la racine du repo `gus-frost-blog`.
> Les 13 fichiers HTML, le fichier `PROMPTS-IMAGES_C5_repas-gamelle.md` et les 26 images `1.png`…`26.png` doivent être accessibles dans le dossier de travail.

---

Tu déploies le cluster C5 (repas/gamelle) dans le repo `gus-frost-blog`. Règle générale : suis exactement les mêmes conventions que le cluster C4, déjà déployé et résolu dans ce repo. En cas de doute sur un format d'URL ou une structure, regarde comment c'est fait dans les articles de `articles/cluster-4-langage-corporel/` et reproduis-le.

Travaille sur une nouvelle branche `cluster-5-repas-gamelle`, ne pousse jamais directement sur `main`, et termine par une pull request.

## 1. Placement des articles
Pour chacun des 13 fichiers HTML fournis (nommés `2026-07-03_TYPE_slug_v1.html`), la destination est la colonne `file` de sa ligne manifest (voir section 6), c'est-à-dire `articles/cluster-5-repas-gamelle/{slug}.html`. Crée le dossier `articles/cluster-5-repas-gamelle/` si besoin, et enregistre chaque article sous son nom de slug (sans la date ni le suffixe `_v1`).

## 2. Bloc <style> de prévisualisation
Chaque article contient un bloc `<style>` de prévisualisation en tête. Traite-le exactement comme pour les articles C4 : s'ils conservent le bloc inline, garde-le ; s'ils s'appuient sur `theme/gf-article.css`, retire le bloc.
Attention : deux articles C5 utilisent des classes absentes de C4, `.gf-recette` (dans `recettes-tapis-lechage-chien`) et `.gf-etapes` (dans `transition-alimentaire-chien`). Si tu retires les blocs inline, ajoute ces deux classes à `theme/gf-article.css` en reprenant leurs définitions depuis les blocs `<style>` des fichiers concernés.

## 3. Images
Les 26 images fournies sont nommées `1.png`…`26.png`. Renomme-les selon la table « Renommage Shopify Files » présente à la fin de `PROMPTS-IMAGES_C5_repas-gamelle.md` (ex. `1.png` → `hero-repas-du-chien.png`).
Téléverse-les ensuite vers Shopify Files via l'app Admin API décrite dans le README de déploiement. Dans les articles, chaque `src` porte déjà le nom de fichier seul (ex. `src="hero-repas-du-chien.png"`) : résous-le vers l'URL CDN complète en suivant exactement le format d'URL utilisé pour les images des articles C4.
Si les identifiants Admin API ne sont pas disponibles dans cet environnement, effectue quand même le renommage des 26 fichiers, laisse les `src` en nom de fichier seul, et signale-le clairement dans la PR pour que le téléversement soit fait à la main.

## 4. Résolution du maillage interne
Dans les 13 articles, tous les liens internes sont en `href="PLACEHOLDER_{slug}"`. Pour chacun :
- cherche `{slug}` dans `manifest.csv` (après ajout des lignes C5 en section 6, tous les slugs C1 à C5 y figurent) ;
- remplace le lien par l'URL on-site de l'article cible, dans le même format exact que les liens déjà résolus des articles C4.
Après cette étape, il ne doit rester aucune occurrence de `PLACEHOLDER_` dans les fichiers C5.

## 5. Liens entrants depuis l'existant
Ajoute, dans les articles existants ci-dessous, un lien contextuel unique vers l'article C5 indiqué (place-le naturellement dans le corps, pas en accroche) :
- `articles/cluster-3-calme-serenite/mastication-lechage-chien.html` → vers `recettes-tapis-lechage-chien`
- `articles/cluster-3-calme-serenite/stimulation-mentale-chien.html` → vers `nourrir-chien-sans-gamelle`
- `articles/cluster-1-anxiete-separation/jouets-occupation-chien-seul.html` → vers `ralentir-repas-chien`
- `articles/cluster-3-calme-serenite/apprendre-le-calme-chien.html` → vers `chien-quemande-table`
- `articles/cluster-3-calme-serenite/chien-calme-serenite-quotidien.html` → vers `repas-du-chien`
Utilise le même format d'URL on-site qu'aux étapes précédentes.

## 6. Mise à jour du manifest
Ajoute les 13 lignes suivantes à la fin de `manifest.csv`, sans toucher aux lignes existantes ni à l'en-tête. Colonnes identiques à l'existant : `cluster_num,cluster_tag,type,slug,parent_pilier_slug,title,meta_title,meta_description,tags,file,prompts_file,links_to_resolve,images_to_resolve`.

```csv
5,cluster-repas-gamelle,pilier,repas-du-chien,,Le repas du chien : en faire un moment de calme et d'équilibre,Le repas du chien : calme, rythme et anti-glouton,"Manger trop vite, quémander, bouder la gamelle ? Rythme, ralentissement, matériel et bons réflexes pour faire du repas un moment serein. Guide complet.","cluster-repas-gamelle, pilier, repas_chien, alimentation, anti_glouton, bien_etre",articles/cluster-5-repas-gamelle/repas-du-chien.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,16,2
5,cluster-repas-gamelle,satellite,chien-mange-trop-vite,repas-du-chien,Chien qui mange trop vite : pourquoi et comment le ralentir,Chien qui mange trop vite : risques et solutions,"Votre chien engloutit sa gamelle en dix secondes ? Pourquoi c'est un vrai risque (dont la dilatation-torsion), et les solutions douces pour le ralentir.","cluster-repas-gamelle, satellite, anti_glouton, alimentation, sante_digestive, repas_chien",articles/cluster-5-repas-gamelle/chien-mange-trop-vite.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,5,2
5,cluster-repas-gamelle,satellite,gamelle-anti-glouton-chien,repas-du-chien,Gamelle anti-glouton : laquelle choisir pour votre chien ?,Gamelle anti-glouton chien : bien la choisir,"Gamelle labyrinthe, tapis de fouille, alternatives maison : comment choisir le bon ralentisseur selon votre chien, et comment l'y habituer sans le frustrer.","cluster-repas-gamelle, satellite, anti_glouton, materiel, gamelle, repas_chien",articles/cluster-5-repas-gamelle/gamelle-anti-glouton-chien.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,5,2
5,cluster-repas-gamelle,satellite,ralentir-repas-chien,repas-du-chien,Ralentir le repas de son chien : les méthodes qui marchent,Ralentir le repas du chien : méthodes efficaces,"Au-delà de la gamelle anti-glouton : toutes les méthodes pour ralentir le repas d'un chien, du tapis de léchage à la ration éparpillée. Ce qui marche vraiment.","cluster-repas-gamelle, satellite, anti_glouton, methode, lechage, repas_chien",articles/cluster-5-repas-gamelle/ralentir-repas-chien.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,6,2
5,cluster-repas-gamelle,satellite,nourrir-chien-sans-gamelle,repas-du-chien,Nourrir son chien sans gamelle : distribuer la ration autrement,Nourrir son chien sans gamelle : les alternatives,"Et si la gamelle disparaissait ? Tapis de fouille, distribution éparpillée, recherche : donner la ration autrement pour un repas plus lent et plus stimulant.","cluster-repas-gamelle, satellite, alimentation, enrichissement, tapis_fouille, repas_chien",articles/cluster-5-repas-gamelle/nourrir-chien-sans-gamelle.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,5,2
5,cluster-repas-gamelle,satellite,recettes-tapis-lechage-chien,repas-du-chien,Recettes de tapis de léchage : idées saines à base de sa ration,Recettes de tapis de léchage pour chien,"Des recettes de tapis de léchage saines, à base de la ration de votre chien : garnitures, versions congelées et bonnes portions. Simple, sûr et apaisant.","cluster-repas-gamelle, satellite, lechage, recettes, alimentation, repas_chien",articles/cluster-5-repas-gamelle/recettes-tapis-lechage-chien.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,4,2
5,cluster-repas-gamelle,satellite,chien-gourmand-toujours-faim,repas-du-chien,Chien gourmand toujours affamé : comment le gérer sereinement,Chien toujours affamé : que faire ?,"Votre chien semble affamé en permanence ? Ce qui se cache derrière, quand s'inquiéter, et comment gérer un chien gourmand sans céder ni le frustrer.","cluster-repas-gamelle, satellite, comportement_alimentaire, gourmandise, alimentation, repas_chien",articles/cluster-5-repas-gamelle/chien-gourmand-toujours-faim.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,5,2
5,cluster-repas-gamelle,satellite,chien-quemande-table,repas-du-chien,Chien qui quémande à table : comment lui apprendre à s'abstenir,Chien qui quémande à table : quoi faire,"Regard insistant, patte, gémissements pendant vos repas ? Pourquoi votre chien quémande et la méthode douce pour installer des repas tranquilles, sans l'exclure.","cluster-repas-gamelle, satellite, comportement_alimentaire, education, quotidien, repas_chien",articles/cluster-5-repas-gamelle/chien-quemande-table.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,4,2
5,cluster-repas-gamelle,satellite,repas-plusieurs-chiens,repas-du-chien,Gérer les repas dans un foyer à plusieurs chiens,Repas à plusieurs chiens : éviter les tensions,"Vol de gamelle, tension, un chien trop rapide face à un lent : comment organiser les repas dans un foyer multi-chiens pour que chacun mange au calme.","cluster-repas-gamelle, satellite, multi_chiens, organisation, repas_chien, cohabitation",articles/cluster-5-repas-gamelle/repas-plusieurs-chiens.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,3,2
5,cluster-repas-gamelle,satellite,combien-repas-chien-par-jour,repas-du-chien,Combien de repas par jour pour un chien ? Les repères par âge,Combien de repas par jour pour un chien ?,"Un, deux, trois repas ? Les repères selon l'âge, du chiot au senior, pourquoi le fractionnement compte et comment installer un rythme de repas régulier.","cluster-repas-gamelle, satellite, rythme_repas, alimentation, chiot, senior",articles/cluster-5-repas-gamelle/combien-repas-chien-par-jour.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,4,2
5,cluster-repas-gamelle,satellite,chien-ne-mange-pas-gamelle,repas-du-chien,Chien difficile qui boude sa gamelle : comprendre et réagir,Chien qui ne mange pas sa gamelle : que faire ?,"Votre chien boude sa gamelle ou trie ? Distinguer le vrai problème du caprice, les causes à écarter et comment redonner l'appétit sans mauvaises habitudes.","cluster-repas-gamelle, satellite, chien_difficile, appetit, alimentation, repas_chien",articles/cluster-5-repas-gamelle/chien-ne-mange-pas-gamelle.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,3,2
5,cluster-repas-gamelle,satellite,transition-alimentaire-chien,repas-du-chien,Changer l'alimentation de son chien sans troubles digestifs,Transition alimentaire du chien : le bon rythme,"Changer de croquettes ou de régime sans diarrhée ni refus : le calendrier de transition sur plusieurs jours, les signes à surveiller et les erreurs à éviter.","cluster-repas-gamelle, satellite, transition_alimentaire, alimentation, sante_digestive, repas_chien",articles/cluster-5-repas-gamelle/transition-alimentaire-chien.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,3,2
5,cluster-repas-gamelle,satellite,choisir-gamelle-chien,repas-du-chien,Bien choisir la gamelle de son chien : matière, forme, hygiène,Choisir la gamelle de son chien : le guide,"Inox, céramique, plastique, gamelle surélevée : quelle gamelle pour quel chien, comment l'entretenir et pourquoi la matière compte plus qu'on ne croit.","cluster-repas-gamelle, satellite, materiel, gamelle, hygiene, repas_chien",articles/cluster-5-repas-gamelle/choisir-gamelle-chien.html,images-prompts/cluster-5-repas-gamelle/PROMPTS-IMAGES_C5_repas-gamelle.md,3,2
```

## 7. Vérifications avant commit
- `grep -r "PLACEHOLDER_" articles/cluster-5-repas-gamelle/` ne renvoie plus rien.
- Aucun `src` ne pointe encore vers un nom de fichier nu si le téléversement Shopify a réussi (tous en URL CDN).
- Les 13 fichiers `.html` sont présents dans `articles/cluster-5-repas-gamelle/`.
- `manifest.csv` contient 13 lignes de données supplémentaires, en-tête inchangé, lignes C1 à C4 intactes.
- Les 5 liens entrants de la section 5 sont bien ajoutés.

## 8. Commit et pull request
- Branche : `cluster-5-repas-gamelle`.
- Message de commit : `Ajout cluster C5 (repas/gamelle) : 13 articles, 26 images, maillage résolu`.
- Ouvre une pull request vers `main` avec un résumé des étapes réalisées et, le cas échéant, la mention si le téléversement Shopify reste à faire manuellement.

Ne touche à rien en dehors de ce périmètre (pas d'autres clusters, pas de modification de `build_article.py` ni de `fr_typo.py`).
