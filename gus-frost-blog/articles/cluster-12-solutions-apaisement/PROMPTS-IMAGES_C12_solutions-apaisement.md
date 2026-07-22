# C12 (NP2) — Les solutions d'apaisement — Prompts images consolidés

> 19 images, numérotation séquentielle sur tout le cluster (marqueur « Image N » par `<figure>`).
> Destination : Shopify Files. Nommage attendu après ingestion : `hero-solutions-apaiser-chien.png` (Image 1) + secondaires renommés par `ingest_cluster.py` depuis `C12_images_map.csv`.
> Style de marque commun (à rappeler dans chaque génération) : **photographie réaliste, lumière naturelle douce, ambiance premium et chaleureuse, situations réelles de la vie avec un chien, aucun texte incrusté, aucune scène de dressage coercitif (jamais de collier étrangleur / à pointes / électrique). Chiens crédibles et détendus, maîtres attentionnés, décors francophones / européens ordinaires (appartement, maison, cuisine, jardin, chemin). Palette en harmonie avec la marque : vert forêt, crème, sauge, touches terracotta et lime.** Ratio paysage 16:9 pour le hero, 4:3 pour les secondaires. Densité de sujets faible, beaucoup d'air, mise au point nette sur le chien ou l'objet.
>
> **Variété visuelle (important) :** ce cluster commercial montre beaucoup de scènes d'apaisement à la maison et deux produits héros (tapis de léchage, tapis de fouille). Pour éviter la répétition, chaque prompt impose un **type de plan** et un **angle** distincts (large / medium / gros plan ; plongée / contre-plongée / profil / niveau des yeux / niveau du sol), une **posture** différente du chien (couché sur le flanc, en boule, sphinx, debout en fouille, assis attentif, museau baissé, tête posée, endormi) et des **accents de palette** variés. Le type de plan est indiqué en tête de chaque prompt. Ne pas générer deux images avec la même composition.
>
> **Sensibilité C12 :** cluster commercial, mais registre honnête et non racoleur. Montrer les produits héros de façon crédible et désirable, jamais comme des gadgets clinquants ; scènes d'apaisement chaleureuses, jamais de chien visiblement en détresse. Pour les Images 16-17 (aides inutiles), rester factuel et neutre, sans caricature ni logo de marque réelle : un étal générique et un maître qui s'interroge, aucun texte lisible sur les emballages.

Légende des champs : **Objectif** (rôle pédagogique dans l'article) · **Plan** (cadrage/angle imposé pour la variété) · **Prompt** (à donner au générateur, EN) · **Alt** (texte alternatif SEO FR) · **Rationale** (pourquoi cette image ici).

---

## PILIER — solutions-apaiser-chien

### Image 1 — HERO
- **Objectif** : incarner d'emblée l'idée d'un chien apaisé dans un foyer serein.
- **Plan** : plan large, niveau des yeux, 16:9. Chien couché sur le flanc.
- **Prompt** : Photorealistic wide shot at eye level, soft natural daylight. A relaxed dog lying stretched on its side on a soft rug in a calm, airy living room, a discreet plug-in diffuser blurred in the background. Muted forest green and cream tones, warm premium editorial mood, shallow depth of field. No text.
- **Alt** : Chien détendu allongé sur le flanc sur un tapis moelleux dans un salon calme et lumineux.
- **Rationale** : Pose le thème du chien apaisé au sein d'une boîte à outils d'ambiance.

### Image 2
- **Objectif** : introduire visuellement le produit héros du flair.
- **Plan** : plan medium, légère contre-plongée, chien debout museau baissé.
- **Prompt** : Photorealistic medium shot, slight low angle. A dog with its muzzle buried into a green fabric snuffle mat on the floor, fully focused on foraging, bright home interior, sage and lime accents, soft natural light. No text.
- **Alt** : Chien concentré, le museau plongé dans un tapis de fouille en tissu vert.
- **Rationale** : Présente le tapis de fouille comme réponse concrète, sans accroche commerciale.

### Image 3
- **Objectif** : clore le pilier sur la sérénité partagée du soir.
- **Plan** : plan medium-large, contre-jour chaud, chien et maître assis.
- **Prompt** : Photorealistic medium-wide shot, warm backlight of late afternoon. An owner and a calm dog sharing a quiet moment on a rug, the person's hand resting gently on the dog, cream and terracotta tones, soft golden light. No text.
- **Alt** : Maître et chien partageant un moment calme sur un tapis dans la lumière douce de fin de journée.
- **Rationale** : Referme le hub sur l'apaisement comme rituel de lien.

---

## SAT01 — pheromones-apaisantes-chien

### Image 4
- **Objectif** : montrer un diffuseur en usage domestique discret.
- **Plan** : plan medium intérieur, niveau des yeux, chien en boule.
- **Prompt** : Photorealistic medium interior shot at eye level. A dog curled up calmly on a cushion, a discreet plug-in pheromone diffuser visible in a wall socket nearby, quiet tidy living room, cream and sage palette, soft daylight. No text.
- **Alt** : Chien couché paisiblement en boule près d'un diffuseur de phéromones branché dans un salon.
- **Rationale** : Illustre l'usage d'ambiance à la maison, forme la plus courante.

### Image 5
- **Objectif** : montrer la forme collier en situation d'extérieur.
- **Plan** : gros plan, de profil, chien en marche.
- **Prompt** : Photorealistic close-up, side profile. Close view of a calm dog wearing a soft pheromone collar during a quiet walk on a leafy path, gentle natural light, green and terracotta tones, shallow depth of field. No text.
- **Alt** : Gros plan d'un chien portant un collier apaisant lors d'une promenade tranquille.
- **Rationale** : Illustre le soutien mobile, en extérieur et en déplacement.

---

## SAT02 — complements-calmants-chien

### Image 6
- **Objectif** : montrer la remise d'un complément dans un cadre du quotidien.
- **Plan** : plan medium, légère plongée, chien assis attentif.
- **Prompt** : Photorealistic medium shot, slight high angle. A hand offering a small calming chew to an attentive dog sitting in a bright kitchen, warm domestic mood, cream and sage tones, soft window light. No text.
- **Alt** : Main tendant une friandise calmante à un chien attentif dans une cuisine lumineuse.
- **Rationale** : Ancre le complément dans un geste simple du quotidien.

### Image 7
- **Objectif** : rappeler que le complément s'inscrit dans une détente globale.
- **Plan** : plan large, niveau du sol, chien couché.
- **Prompt** : Photorealistic wide shot at floor level. A relaxed dog lying at the feet of an owner seated in a peaceful living room, calm everyday scene, muted forest green and cream palette, soft natural light. No text.
- **Alt** : Chien détendu allongé aux pieds de son maître assis dans un salon paisible.
- **Rationale** : Situe le complément comme appoint d'une démarche plus large.

---

## SAT03 — tapis-lechage-apaiser-chien

### Image 8
- **Objectif** : montrer le produit héros en usage, le léchage apaisant.
- **Plan** : plan medium, de profil, niveau des yeux, chien qui lèche.
- **Prompt** : Photorealistic medium side shot at eye level. A dog calmly licking a green silicone lick mat suctioned to a tiled floor, concentrated and relaxed expression, soft natural light, sage and cream tones. No text.
- **Alt** : Chien léchant avec application un tapis de léchage vert fixé au carrelage.
- **Rationale** : Montre le héros en action comme rituel de calme concret.

### Image 9
- **Objectif** : détailler l'objet et sa garniture.
- **Plan** : gros plan produit, vue en plongée (top-down).
- **Prompt** : Photorealistic top-down close-up. A green silicone lick mat with visible suction cups, its grooves spread with a thin layer of smooth pale purée, clean neutral surface, soft even light. No text.
- **Alt** : Gros plan d'un tapis de léchage garni de purée, ventouses visibles.
- **Rationale** : Explicite le garnissage fin, cœur du mode d'emploi.

---

## SAT04 — tapis-fouille-chien

### Image 10
- **Objectif** : montrer le héros du flair en pleine recherche.
- **Plan** : plan medium, contre-plongée, museau enfoui.
- **Prompt** : Photorealistic medium shot, low angle. A dog actively foraging with its muzzle deep between the fabric strips of a grey snuffle mat, tail relaxed, bright living room floor, lime and sage accents, soft light. No text.
- **Alt** : Chien fouillant activement un tapis de reniflage gris, le museau enfoui entre les lanières.
- **Rationale** : Illustre l'activité de flair, la mieux étayée du cluster.

### Image 11
- **Objectif** : détailler l'objet rangé et sa praticité.
- **Plan** : nature morte, gros plan à 45°.
- **Prompt** : Photorealistic still-life close-up at 45 degrees. A rolled-up grey fabric snuffle mat resting next to a simple bowl of kibble on a wooden floor, warm minimal styling, cream and terracotta tones, soft light. No text.
- **Alt** : Tapis de fouille roulé et rangé à côté d'un bol de croquettes.
- **Rationale** : Montre l'entretien et le rangement, gage d'un usage durable.

---

## SAT05 — musique-apaisante-chien

### Image 12
- **Objectif** : illustrer l'ambiance sonore apaisante à la maison.
- **Plan** : plan medium, légère plongée, chien endormi.
- **Prompt** : Photorealistic medium shot, soft high angle. A dog dozing peacefully on a sofa in a calm living room, a discreet speaker on a shelf in the background, warm soft light, cream and sage tones. No text.
- **Alt** : Chien assoupi sur un canapé dans un salon calme, une enceinte discrète en arrière-plan.
- **Rationale** : Associe visuellement fond sonore doux et repos du chien.

### Image 13
- **Objectif** : montrer le réglage d'un volume modéré.
- **Plan** : plan medium, par-dessus l'épaule, chien au repos.
- **Prompt** : Photorealistic medium over-the-shoulder shot. An owner gently adjusting the volume of a small speaker while a dog rests quietly nearby on the floor, calm home, soft natural light, muted green tones. No text.
- **Alt** : Maître réglant le volume d'une enceinte pendant qu'un chien se repose tranquillement à ses pieds.
- **Rationale** : Illustre le conseil clé du volume modéré et ponctuel.

---

## SAT06 — massage-ttouch-chien

### Image 14
- **Objectif** : montrer un geste de massage doux sur une zone appréciée.
- **Plan** : plan medium, niveau des yeux, chien allongé.
- **Prompt** : Photorealistic medium shot at eye level. An owner's hands gently massaging the shoulders of a relaxed dog lying on a rug, calm ambient home, warm soft light, sage and cream palette. No text.
- **Alt** : Mains d'un maître massant doucement les épaules d'un chien allongé et détendu sur un tapis.
- **Rationale** : Illustre un geste simple et sûr, sur une zone bien acceptée.

### Image 15
- **Objectif** : rendre visibles les signes de détente du chien.
- **Plan** : gros plan, niveau des yeux, tête posée, yeux mi-clos.
- **Prompt** : Photorealistic tight close-up at eye level. A dog with half-closed eyes and a soft relaxed expression during a gentle massage at the base of its ears, warm natural light, cream and terracotta tones. No text.
- **Alt** : Gros plan d'un chien aux yeux mi-clos pendant un massage doux de la base des oreilles.
- **Rationale** : Montre les signaux de consentement et de détente à repérer.

---

## SAT07 — aides-anti-stress-inutiles

### Image 16
- **Objectif** : évoquer l'abondance de produits sans caricature ni marque réelle.
- **Plan** : plan large, de face, étal (pas de chien).
- **Prompt** : Photorealistic wide straight-on shot. A cluttered generic store shelf filled with colourful unbranded anti-stress pet products and gadgets, neutral retail lighting, no readable text or logos on the packaging. No text.
- **Alt** : Étal encombré de produits anti-stress pour chien aux emballages génériques et colorés.
- **Rationale** : Plante le décor d'un marché saturé de promesses.

### Image 17
- **Objectif** : incarner l'esprit critique face à une promesse.
- **Plan** : plan medium, légère contre-plongée, maître debout, chien assis.
- **Prompt** : Photorealistic medium shot, slight low angle. A thoughtful owner examining the label of an unbranded anti-stress product in a store aisle, a calm dog sitting beside them, neutral lighting, no readable text on the packaging. No text.
- **Alt** : Maître dubitatif lisant l'étiquette d'un produit anti-stress en rayon, son chien assis à côté.
- **Rationale** : Illustre le réflexe de prudence encouragé par l'article.

---

## SAT08 — routine-apaisement-chien

### Image 18
- **Objectif** : illustrer un repère fort de la journée, le repas régulier.
- **Plan** : plan medium, niveau des yeux, chien assis en attente.
- **Prompt** : Photorealistic medium shot at eye level. A dog sitting patiently and calmly beside its bowl at mealtime in a tidy kitchen, orderly warm domestic scene, cream and sage tones, soft daylight. No text.
- **Alt** : Chien attendant sagement près de sa gamelle à l'heure du repas dans une cuisine ordonnée.
- **Rationale** : Incarne la régularité des repères, cœur de la routine.

### Image 19
- **Objectif** : clore le cluster sur le rituel apaisant du soir.
- **Plan** : plan large, niveau du sol, chien endormi.
- **Prompt** : Photorealistic wide shot at floor level. A dog sleeping peacefully curled in its basket in the evening, warm dim ambient light of a calm home, forest green and terracotta tones, cozy serene mood. No text.
- **Alt** : Chien paisiblement endormi dans son panier le soir, dans l'ambiance tamisée du foyer.
- **Rationale** : Referme le cluster sur le calme installé par une routine régulière.

---

*Établi juillet 2026. 19 prompts, un par marqueur `<figure>` du cluster, numérotés séquentiellement pour le renommage automatisé. Conforme au standard images de marque Gus & Frost (Montserrat + Lora côté texte, palette forêt / crème / sauge / terracotta / lime, situations réelles, aucun texte incrusté).*
