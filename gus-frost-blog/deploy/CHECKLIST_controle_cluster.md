# Checklist de contrôle d'un cluster (gabarit « standard C5 »)

Réutilisable pour C6 et les suivants. À passer sur les 13 fichiers `articles/cluster-N-…/{slug}.html`
**après** rédaction et résolution du maillage, **avant** publication Shopify.

## Contrôle automatique (à lancer en premier)

```bash
# après maillage (liens résolus, images en CDN) :
python scripts/check_cluster.py --dir articles/cluster-6-xxx --faq 5 --blog chiens
# avant maillage (tolère PLACEHOLDER_ et noms d'images nus) :
python scripts/check_cluster.py --dir articles/cluster-6-xxx --pre-maillage
```
`FAIL` = à corriger ; `WARN` = à vérifier ; sortie 0 si aucun `FAIL`.

## Le gabarit C5, point par point

### Structure
- [ ] Un seul `<article class="gf-article"> … </article>` par fichier.
- [ ] Pas de bloc `<style>` dans le corps envoyé à Shopify (le style vient de `theme/gf-article.css`).
- [ ] Ordre de fin d'article : **… contenu … → FAQ → CTA → `</article>`**. Pas de bloc références (`gf-refs`) en C5.

### FAQ
- [ ] `<h2 id="faq">Questions fréquentes</h2>` puis `<div class="gf-faq">`.
- [ ] **5 questions** exactement : 5 paires `<h3>` question `</h3>` + `<p>` réponse `</p>`.
- [ ] **Pas de JSON-LD / `FAQPage`** dans le corps (balisage géré au thème, pas dans l'article).
- [ ] `id="faq"` sur le `<h2>` (ancre) — **à mettre sur TOUS les articles** (voir « écarts connus »).

### CTA produit
- [ ] Un seul `<div class="gf-cta">`, **dernier bloc avant `</article>`**, après la FAQ.
- [ ] 1–2 phrases de prose reliant le sujet au besoin produit, puis
      `<span class="gf-cta-call">À retrouver dans notre : <a href="/collections/stress">univers Anti-stress &amp; Sérénité</a></span>`.
- [ ] Lien = **collection `/collections/stress`** (réel, jamais `/products/`, jamais un `PLACEHOLDER_`).
- [ ] **Un CTA par article**, même sans produit central : la cible reste la collection, seule la prose s'adapte
      (nommer tapis de léchage / tapis de fouille quand c'est pertinent).
- [ ] Les produits restent **tissés dans le corps** en plus du CTA (« conséquence d'un besoin, jamais en accroche »).

### Images
- [ ] 2 images par article (1 `hero-…` d'ouverture + 1 secondaire), noms descriptifs de la table de renommage.
- [ ] Chaque `<img>` a un `alt` non vide (FR).
- [ ] `src` en URL CDN Shopify après téléversement (ou nom nu en pré-maillage).

### Maillage interne
- [ ] Aucun `PLACEHOLDER_` restant après résolution.
- [ ] Liens internes au format `/blogs/chiens/{slug}`, cibles présentes dans `manifest.csv`.
- [ ] Le lien CTA `/collections/stress` **ne compte pas** comme lien interne à résoudre.

### Typo FR (insécable)
- [ ] Espace **insécable** (U+00A0 ou U+202F) avant `; : ! ? »` et après `«`.
- [ ] Vérifier aussi apostrophes typographiques et guillemets « … » (pas `"`).

### Encadrés
- [ ] Encadrés `CONSEIL` (`gf-box gf-conseil`) et `CAS PRATIQUE` (`gf-box gf-cas`) au standard.
- [ ] Classes spécifiques éventuelles (`gf-recette`, `gf-etapes`, `gf-meta`) : déjà dans `theme/gf-article.css`.

## Champs Shopify (à la création/MAJ, comme C4)
- [ ] Titre = `title` ; Handle = `slug`.
- [ ] Corps = fragment `{slug}.html` (FAQ + CTA compris).
- [ ] **Extrait** = `summary_html` (fichier `C*_extraits.csv`), **distinct** de la méta-description.
- [ ] SEO = métachamps `global.title_tag` (= `meta_title`) et `global.description_tag` (= `meta_description`).
- [ ] Tags = colonne `tags` ; Auteur = « Gus & Frost ».
- [ ] Image mise en avant = image `hero-` + son `alt`.
- [ ] Statut = brouillon (`published:false`) tant que non validé.

## Écarts connus dans C5 (à NE PAS reproduire — corriger le standard)
Le contrôle automatique les remonte en `WARN` sur C5 lui-même :
1. **`id="faq"`** : présent sur le **pilier** `repas-du-chien`, **absent des 12 satellites**. → Canonique retenu : **le mettre partout**.
2. **Insécables** : le **corps** des articles C5 utilise des espaces normales avant `; : ! ? »` (8 à 33 par article) ;
   seuls la FAQ et le CTA (ajoutés en 2ᵉ passe) sont propres. → Canonique retenu : **insécable partout** (corps + FAQ + CTA).

Pour C6, viser le **canonique** ci-dessus (cohérent et propre), pas l'état actuel de C5.
