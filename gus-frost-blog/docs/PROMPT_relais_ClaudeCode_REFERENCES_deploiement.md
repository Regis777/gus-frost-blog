# Passage de relais — Claude Code — Mise en ligne des blocs « Sources et références » (460 articles)

> Rédigé le 05/09/2026 en session Cowork. À coller tel quel dans Claude Code, **à la racine du dépôt `gus-frost-blog`** (`C:\Users\regis\gfbrepo\gus-frost-blog`).
> **Tu ne publies et ne dépublies aucun article. Tu ne modifies que le `body_html` des articles déjà en ligne, via le script fourni.** Tout passe par un dry-run avant écriture.

---

## 0. Contexte (pourquoi ce chantier)

Gus & Frost tient deux blogs Shopify en silos SEO : **chiens** (handle `chiens`, `manifest.csv`, 252 articles) et **chats** (handle `chats`, `manifest_chat.csv`, 219 articles). Chaque cluster a été rédigé à partir d'une bibliographie de sources primaires vérifiées (`C{n}_bibliographie.md`), mais le standard interne prescrivait jusqu'ici « citation sobre dans la prose, sans bibliographie visible ». Résultat : 439 articles sur 471 n'affichaient aucune référence.

Décision de Régis (05/09/2026) : **chaque article porte désormais, en fin d'article, un bloc visible « Sources et références »**, sans aucun lien sortant (préserver le jus SEO). Le standard `Gus-Frost_STANDARD_references-verifiees.md` est passé en v2 (§6).

Ce qui a été fait en amont (session Cowork, pas toi) :
- **460 fichiers `articles/<dossier>/<slug>.html` du dépôt contiennent maintenant le bloc** `<aside class="gf-refs"><h2>Sources et références</h2><ul>…</ul></aside>`, placé après le CTA et le JSON-LD FAQ, juste avant `</article>`. 1 576 références au total, toutes issues des bibliographies de cluster (champs relevés sur page éditeur, jamais complétés de mémoire). Les 32 blocs déjà présents sur C4 (langage corporel) et C15 (alimentation chiot) ont seulement changé de titre (« Pour aller plus loin » → « Sources et références »).
- **11 articles n'ont volontairement pas de bloc** (aucune source attribuable, décision Régis) : `massage-ttouch-chien`, `tapis-lechage-apaiser-chien`, `premieres-nuits-chiot`, `premiers-jours-chiot`, `preparer-arrivee-chiot`, `securiser-maison-chiot`, `nettoyer-pipi-chiot-odeurs`, `assurance-budget-sante-chiot` (chiens) ; `deuil-perte-chat-cote-maitre`, `choisir-nom-chaton`, `presenter-chaton-enfants` (chats). Le script les signalera `SANS-BLOC` : c'est normal, ne rien faire.
- **`theme/gf-article.css`** a reçu la règle `.gf-refs` (fond crème, bordure, titre en capitales vertes). Sans elle, le bloc s'affiche en texte brut.
- **`scripts/push_refs.py`** (nouveau) : pour chaque article du manifest, lit le bloc dans le fichier du dépôt, récupère l'article en ligne, insère le bloc avant `</article>` (ou remplace le bloc existant), et renvoie **uniquement `body_html`**. Statut de publication, titre, tags, métas, image à la une : intouchés. Dry-run par défaut, `--apply` pour écrire.

**Pourquoi ne pas utiliser `deploy/deploy_cluster.py` :** il rebâtit le corps complet (images, placeholders, FAQ) et exige `images/cluster-*` + `*images_map.csv`, absents du dépôt pour la majorité des clusters (et jamais créés pour C1-C5 chien). `push_refs.py` part du corps en ligne, donc aucun risque de casser les images ou le maillage baké.

Rien n'est encore en ligne. C'est l'objet de ce relais.

---

## 1. Ta mission, en cinq étapes

### Étape 1 — Vérifier l'état du dépôt (ne rien corriger toi-même)

```bash
git status --short | grep -c "articles/.*\.html"        # attendu ≈ 462
git status --short theme/scripts/ 2>/dev/null ; git status --short theme/gf-article.css scripts/push_refs.py
grep -c "gf-refs" theme/gf-article.css                     # attendu ≥ 5
grep -l 'class="gf-refs"' articles/*/*.html | wc -l         # attendu 461 (460 + doublon litiere-chaton-apprentissage dans cluster-6-litiere-chat)
grep -L 'class="gf-refs"' articles/*/*.html                 # attendu : les 11 slugs listés en §0 (+ éventuels fichiers hors manifest)
python -c "import re,glob;print(sum(1 for f in glob.glob('articles/*/*.html') for b in re.findall(r'<aside class=\"gf-refs\">.*?</aside>',open(f,encoding='utf-8').read(),re.S) if '<a ' in b or 'http' in b))"   # attendu 0 (aucun lien dans les blocs)
```

Le `git status` montre aussi des modifications **sans rapport** avec ce chantier (`theme/gf-quiz-anxiete.liquid`, `theme/page.quiz-anxiete.json`, `.env.example`, `README.md`, `CHECKLIST_images_INDEX.md`, quelques CSV) : **ne les commite pas et ne les écrase pas.**

Si un des comptages ne colle pas, arrête-toi et montre-moi.

### Étape 2 — Git : branche et commit ciblé

```bash
git checkout -b refs/sources-et-references
git add articles/*/*.html theme/gf-article.css scripts/push_refs.py
git commit -m "Références : bloc « Sources et références » sur 460 articles + CSS .gf-refs + push_refs.py"
```

Pas de push, pas de PR avant la fin de l'étape 5.

### Étape 3 — Pousser le CSS du thème (avant les articles)

```bash
python scripts/theme_file.py themes                                    # repérer le thème live (role main)
python scripts/theme_file.py pull assets/gf-article.css /tmp/gf-article.live.css   # sauvegarde de la version en ligne
python scripts/theme_file.py push assets/gf-article.css theme/gf-article.css --allow-live
```

Vérifie ensuite dans le navigateur qu'un article quelconque s'affiche toujours normalement (le CSS n'ajoute que des règles `.gf-refs`, rien d'autre ne change).

### Étape 4 — Dry-run complet, blog par blog

```bash
python scripts/push_refs.py --blog chats  > /tmp/refs_dryrun_chats.txt
python scripts/push_refs.py --blog chiens > /tmp/refs_dryrun_chiens.txt
tail -3 /tmp/refs_dryrun_chats.txt /tmp/refs_dryrun_chiens.txt
```

Attendu : `INSERT` pour la quasi-totalité, `REPLACE` pour les 32 articles C4/C15, `SANS-BLOC` pour les 11 articles de la §0, **0 `ERREUR`, 0 `ABSENT-SHOPIFY`** (sauf si un article du manifest n'est effectivement pas en ligne : dans ce cas liste-le-moi, ne le crée pas).

**STOP : montre-moi le bilan des deux dry-runs et attends mon « go ».**

### Étape 5 — Application, par paliers, avec contrôle visuel

1. Un seul cluster test : `python scripts/push_refs.py --blog chats --dir cluster-19-chaton-socialisation-chat --apply` (13 articles). Ouvre `/blogs/chats/fenetre-socialisation-chaton-age` en ligne et confirme : bloc présent en fin d'article, stylé, aucun lien dedans, article toujours avec ses images, son CTA, sa FAQ et son statut d'origine (brouillon ou publié).
2. Si c'est bon : `python scripts/push_refs.py --blog chats --apply` puis `python scripts/push_refs.py --blog chiens --apply`. Le script attend 0,6 s entre deux écritures (limite API Shopify) : compter environ 10 minutes au total.
3. Relance les deux commandes **sans** `--apply` : tout doit ressortir `IDENTIQUE` (ou `SANS-BLOC` pour les 11). C'est la preuve que l'en-ligne et le dépôt concordent.
4. Contrôle visuel sur 3 articles au hasard par blog, dont un C4 ou C15 (titre du bloc renommé) et un ancien cluster chien (C1 à C5).
5. Git : `git push -u origin refs/sources-et-references`, ouvre une PR sans merger. Dans le corps de la PR : les bilans des étapes 4 et 5.3.

---

## 2. Règles

- Draft-first reste la règle : `push_refs.py` ne touche pas au statut de publication ; ne le contourne pas avec un autre script.
- Aucun lien sortant dans un bloc, jamais. Si tu en vois un en ligne, signale-le, ne le corrige pas seul.
- Ne modifie aucun fichier `articles/*.html`, aucune bibliographie, aucun manifest. Si un bloc te semble faux, signale-le.
- Si l'API renvoie une erreur 429 (rate limit), relance la même commande : le script est idempotent (`IDENTIQUE` pour ce qui est déjà passé).
- Ne touche pas aux fichiers hors chantier présents dans `git status`.

## 3. Documents de référence (sur le Drive, `BLOGS_Gus et Frost\Blogs cowork\`)

- `AUDIT_references_articles_2026-09-05.csv` : état article par article (bloc, nb de refs).
- `REFS_notes-mapping_2026-09-05.md` : arbitrages par cluster et affirmations d'articles à relire (Régis s'en charge, hors périmètre).
- `refs_mapping/<CODE>_refs.json` + `insert_refs.py` : mapping sources → articles et outil d'insertion (déjà exécuté).
- `Gus-Frost_STANDARD_references-verifiees.md` §6 (v2) : gabarit du bloc.
- `_backup_avant_refs_2026-09-05/` : originaux des 461 fichiers avant insertion.

## 4. Rapport attendu en fin de session

Nombre d'articles `INSERT` / `REPLACE` / `IDENTIQUE` / `SANS-BLOC` par blog, les éventuels `ABSENT-SHOPIFY` ou `ERREUR` avec leur slug, le lien de la PR, et toute anomalie visuelle constatée.
