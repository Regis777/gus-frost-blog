# C11 — Le chien senior et le vieillissement — Prompts images consolidés

> 27 images, numérotation séquentielle sur tout le cluster (marqueur « Image N » par `<figure>`).
> Destination : Shopify Files. Nommage attendu après ingestion : `hero-chien-senior-vieillissement.png` (Image 1) + secondaires renommés par `ingest_cluster.py` depuis `C11_images_map.csv`.
> Style de marque commun (à rappeler dans chaque génération) : **photographie réaliste, lumière naturelle douce, ambiance premium et chaleureuse, situations réelles de la vie avec un chien âgé, aucun texte incrusté, aucune scène de dressage coercitif (jamais de collier étrangleur / à pointes / électrique). Chiens seniors crédibles (museau grisonnant, regard doux), maîtres attentionnés, décors francophones / européens ordinaires (appartement, maison, jardin, parc, chemin). Palette en harmonie avec la marque : vert forêt, crème, sauge, touches terracotta et lime.** Ratio paysage 16:9 pour le hero, 4:3 pour les secondaires. Densité de sujets faible, beaucoup d'air, mise au point nette sur le chien.
>
> **Variété visuelle (important) :** ce cluster comporte beaucoup de scènes intérieures de chien âgé au repos. Pour éviter que les images se ressemblent, chaque prompt impose un **type de plan** et un **angle** distincts (large / medium / gros plan ; plongée / contre-plongée / profil / niveau des yeux / niveau du sol), une **posture** différente du chien (couché sur le flanc, en boule, sphinx, debout en marche, assis, tête posée, museau baissé) et des **accents de palette** variés. Le type de plan est indiqué en tête de chaque prompt. Ne pas générer deux images avec la même composition.
>
> **Sensibilité C11 :** dimension médicale et émotionnelle forte. Montrer des chiens âgés dignes et sereins, jamais souffrants ni pitoyables ; aucune scène clinique anxiogène (pas de cabinet vétérinaire, pas de matériel médical). Pour les scènes de fin de vie (Images 26-27), rester pudique, tendre et lumineux : un chien paisible et une présence affectueuse, aucun élément morbide, lumière chaude et douce.

Légende des champs : **Objectif** (rôle pédagogique dans l'article) · **Plan** (cadrage/angle imposé pour la variété) · **Prompt** (à donner au générateur, EN) · **Alt** (texte alternatif SEO FR) · **Rationale** (pourquoi cette image ici).

---

## PILIER — chien-senior-vieillissement

### Image 1 — HERO
- **Objectif** : incarner d'emblée la tendresse et la sérénité de l'accompagnement d'un chien qui vieillit.
- **Plan** : plan large, niveau des yeux, 16:9. Chien couché sur le flanc.
- **Prompt** : Photorealistic wide shot at eye level, soft natural daylight from a window. A calm senior dog with a greying muzzle lying stretched on its side on a thick soft rug near a window, an owner's hand resting gently on its back. Muted forest green and cream tones, warm premium editorial mood, shallow depth of field. No text.
- **Alt** : Chien âgé au museau grisonnant couché paisiblement sur un tapis moelleux près d'une fenêtre, la main de son maître posée sur lui.
- **Rationale** : Pose le thème du grand âge accompagné avec douceur dès le hero.

### Image 2
- **Objectif** : illustrer l'aménagement du confort et l'aide à la mobilité.
- **Plan** : plan medium, légère contre-plongée, chien de profil.
- **Prompt** : Photorealistic medium shot, slight low angle. A senior dog calmly walking up a gentle low ramp toward a sofa, an owner beside it offering quiet encouragement, bright living room, sage and terracotta accents, soft natural light. No text.
- **Alt** : Chien âgé montant tranquillement une petite rampe vers le canapé, aidé par son maître.
- **Rationale** : Montre l'adaptation concrète du logement, fil rouge du pilier.

### Image 3
- **Objectif** : créer un lien émotionnel avec le chien senior.
- **Plan** : gros plan, niveau des yeux, tête posée.
- **Prompt** : Photorealistic tight close-up at eye level. The gentle face of an old dog with a white greying muzzle and soft expressive eyes, chin resting on a cushion, warm window light, cream and green tones, serene premium mood. No text.
- **Alt** : Gros plan tendre sur le museau grisonnant et le regard doux d'un vieux chien, menton posé sur un coussin.
- **Rationale** : Clôt le pilier sur l'attachement au compagnon qui vieillit.

---

## SAT01 — reconnaitre-signes-vieillissement-chien

### Image 4
- **Objectif** : montrer un premier signe physique, le lever plus lent.
- **Plan** : plan medium, légère plongée, chien à demi levé.
- **Prompt** : Photorealistic medium shot, slight high angle. A senior dog slowly getting up from its bed, unfolding in stages with visible mild effort, calm home interior, soft cool morning light, muted tones. No text.
- **Alt** : Vieux chien qui se lève lentement de son couchage, un léger effort visible dans sa posture.
- **Rationale** : Illustre le signe le plus parlant du vieillissement corporel.

### Image 5
- **Objectif** : rendre visibles les marques du temps sur le visage.
- **Plan** : gros plan serré, niveau des yeux, face.
- **Prompt** : Photorealistic tight close-up at eye level. Close view of a dog's greying muzzle and pale eyebrows, eyes slightly cloudy, gentle natural light, soft neutral background. No text.
- **Alt** : Gros plan sur un museau et des sourcils grisonnants, les yeux légèrement troubles.
- **Rationale** : Ancre la lecture des signes visibles du grand âge.

---

## SAT02 — amenager-maison-chien-senior

### Image 6
- **Objectif** : montrer un intérieur sécurisé contre les sols glissants.
- **Plan** : plan large intérieur, plongée douce, chien debout en marche.
- **Prompt** : Photorealistic wide interior shot, soft high angle. A senior dog walking confidently across a living room fitted with non-slip runners and rugs over a smooth floor, tidy warm home, cream and sage palette, soft natural light. No text.
- **Alt** : Chien âgé marchant sereinement dans un salon équipé de tapis et de chemins antidérapants.
- **Rationale** : Illustre la sécurisation des sols, cœur de l'article.

### Image 7
- **Objectif** : montrer un accès facilité vers le mobilier.
- **Plan** : plan medium de profil, niveau du sol.
- **Prompt** : Photorealistic medium side-on shot at floor level. A senior dog stepping onto a low padded ramp leading up to a bed, calm bedroom, warm soft light, terracotta accents. No text.
- **Alt** : Chien âgé empruntant une rampe douce pour accéder au lit.
- **Rationale** : Concrétise l'aide aux accès sans sauts.

---

## SAT03 — chien-senior-arthrose-mobilite

### Image 8
- **Objectif** : montrer une promenade douce adaptée à la mobilité réduite.
- **Plan** : plan large extérieur, niveau des yeux, chien debout en marche lente.
- **Prompt** : Photorealistic wide outdoor shot at eye level. A senior dog walking slowly and carefully on soft grass in a quiet park, careful gait, owner walking calmly nearby, gentle diffuse daylight, green tones. No text.
- **Alt** : Chien âgé marchant prudemment sur l'herbe lors d'une promenade douce, son maître à ses côtés.
- **Rationale** : Illustre le mouvement doux qui entretient les articulations.

### Image 9
- **Objectif** : montrer un geste de confort doux, sans caractère médical.
- **Plan** : plan medium, plongée, chien couché sur le flanc.
- **Prompt** : Photorealistic medium shot, high angle. An owner gently resting and softly massaging the hindquarters of a relaxed senior dog lying on its side on a soft blanket at home, warm calm mood, cream tones, soft light. No text.
- **Alt** : Maître massant doucement l'arrière-train d'un chien âgé allongé et détendu.
- **Rationale** : Représente un geste de confort, en complément du suivi vétérinaire.

---

## SAT04 — couchage-confort-chien-age

### Image 10
- **Objectif** : valoriser un couchage orthopédique et le repos profond.
- **Plan** : gros plan, niveau du sol, chien en boule endormi.
- **Prompt** : Photorealistic close-up at floor level. A senior dog sleeping deeply curled on a thick orthopedic memory-foam bed, body softly supported, warm cozy light, cream and sage tones. No text.
- **Alt** : Chien âgé profondément endormi, bien soutenu sur un couchage orthopédique épais.
- **Rationale** : Montre le soutien articulaire d'un bon couchage.

### Image 11
- **Objectif** : illustrer le bon emplacement du couchage.
- **Plan** : plan large intérieur, niveau des yeux.
- **Prompt** : Photorealistic wide interior shot at eye level. A plush dog bed placed in a quiet warm corner away from foot traffic near a sunlit window, a senior dog settling into it, homely premium mood, soft golden light. No text.
- **Alt** : Couchage douillet installé dans un coin calme et chaud près d'une fenêtre, où un chien âgé s'installe.
- **Rationale** : Concrétise le choix de l'emplacement, calme et chaud.

---

## SAT05 — sommeil-chien-senior

### Image 12
- **Objectif** : montrer le sommeil diurne allongé du senior.
- **Plan** : plan medium, niveau du sol, chien en sphinx assoupi.
- **Prompt** : Photorealistic medium shot at floor level. A senior dog dozing peacefully in a warm patch of daylight on a soft blanket, sphinx position drifting to sleep, serene atmosphere, cream and sage tones. No text.
- **Alt** : Chien âgé sommeillant paisiblement dans un rai de lumière douce en journée.
- **Rationale** : Illustre les longues siestes diurnes du chien âgé.

### Image 13
- **Objectif** : illustrer l'apaisement nocturne et la veilleuse.
- **Plan** : plan medium, ambiance nuit, contre-plongée douce.
- **Prompt** : Photorealistic medium shot, gentle low angle, nighttime interior. A senior dog resettling calmly into its basket in a dim hallway softly lit by a small night light, warm reassuring glow, muted tones. No text.
- **Alt** : Chien âgé se rendormant paisiblement dans son panier la nuit, éclairé par une veilleuse douce.
- **Rationale** : Représente le rituel du soir et le repère lumineux nocturne.

---

## SAT06 — dysfonction-cognitive-chien-age

### Image 14
- **Objectif** : évoquer une désorientation douce, sans dramatiser.
- **Plan** : plan medium, niveau des yeux, chien debout de profil.
- **Prompt** : Photorealistic medium shot at eye level. A senior dog standing still and pensive, facing a corner of a familiar room, a slightly lost but calm expression, soft neutral daylight, quiet home. No text.
- **Alt** : Vieux chien immobile et songeur face à un coin de la pièce, l'air un peu perdu mais paisible.
- **Rationale** : Illustre un signe de confusion cognitive avec pudeur.

### Image 15
- **Objectif** : montrer la réassurance apportée par le maître.
- **Plan** : plan medium, niveau du sol, maître accroupi et chien assis.
- **Prompt** : Photorealistic medium shot at floor level. An owner crouching to gently reassure a senior dog sitting close, calm eye contact and soft touch, warm living room, tender mood, cream and green tones. No text.
- **Alt** : Maître accroupi rassurant calmement son vieux chien assis près de lui.
- **Rationale** : Ancre le rôle apaisant du maître, en complément du vétérinaire.

---

## SAT07 — stimuler-chien-senior-mental

### Image 16
- **Objectif** : montrer une stimulation par le flair, à faible effort.
- **Plan** : gros plan, plongée, chien museau baissé.
- **Prompt** : Photorealistic close-up, high angle. A senior dog nose-deep in a snuffle mat, focused and content, sniffing for treats, soft indoor light, sage and lime accents. No text.
- **Alt** : Chien âgé le museau plongé dans un tapis de fouille, concentré sur sa recherche.
- **Rationale** : Illustre le jeu de flair, idéal pour un corps qui bouge moins.

### Image 17
- **Objectif** : montrer un petit jeu de recherche accompagné.
- **Plan** : plan medium, niveau des yeux, mains + chien assis attentif.
- **Prompt** : Photorealistic medium shot at eye level. An owner's hands hiding treats under upturned cups on the floor while an attentive senior dog watches, playful gentle mood, warm home, cream tones. No text.
- **Alt** : Maître proposant un jeu de flair avec des friandises cachées sous des gobelets, le chien âgé attentif.
- **Rationale** : Représente un apprentissage doux et positif adapté au grand âge.

---

## SAT08 — activite-promenade-chien-age

### Image 18
- **Objectif** : montrer une promenade courte centrée sur le reniflage.
- **Plan** : plan large extérieur, niveau des yeux, chien qui renifle au sol.
- **Prompt** : Photorealistic wide outdoor shot at eye level. A senior dog calmly sniffing the grass in a park on a loose leash, relaxed exploratory walk, soft daylight, green and sage tones. No text.
- **Alt** : Chien âgé reniflant tranquillement l'herbe au parc, la laisse détendue.
- **Rationale** : Illustre la promenade au rythme du chien, l'odorat qui comble.

### Image 19
- **Objectif** : montrer la pause et le respect du rythme.
- **Plan** : plan medium, niveau des yeux, chien couché à l'ombre.
- **Prompt** : Photorealistic medium shot at eye level. A senior dog resting lying down on a shaded path during a walk, a patient owner sitting nearby, dappled soft light, calm mood, terracotta accents. No text.
- **Alt** : Chien âgé se reposant à l'ombre d'un chemin pendant la balade, son maître patient à côté.
- **Rationale** : Rappelle qu'on adapte l'effort et qu'on laisse le chien souffler.

---

## SAT09 — chien-senior-perte-vue-audition

### Image 20
- **Objectif** : montrer comment aborder un chien malvoyant sans le surprendre.
- **Plan** : gros plan, niveau des yeux, main tendue vers le museau.
- **Prompt** : Photorealistic close-up at eye level. A hand held out gently for a senior dog to sniff before being touched, the dog calm and trusting, soft warm light, cream background. No text.
- **Alt** : Maître tendant la main pour que son chien âgé la sente avant de le toucher, le chien confiant.
- **Rationale** : Illustre la communication douce avec un chien dont la vue baisse.

### Image 21
- **Objectif** : montrer la sécurisation de l'environnement.
- **Plan** : plan large intérieur, plongée, chien près d'une barrière d'escalier.
- **Prompt** : Photorealistic wide interior shot, high angle. A senior dog resting calmly near a stair safety gate in a hallway softly lit by a night light, secure homely feel, muted warm tones. No text.
- **Alt** : Chien âgé près d'un escalier sécurisé par une barrière, un éclairage doux dans le couloir.
- **Rationale** : Concrétise la sécurité pour un chien aux sens qui faiblissent.

---

## SAT10 — alimentation-appetit-chien-age

### Image 22
- **Objectif** : montrer la posture confortable à une gamelle surélevée.
- **Plan** : plan medium, niveau du sol, profil.
- **Prompt** : Photorealistic medium side-on shot at floor level. A senior dog eating comfortably from a raised bowl stand, neck and back in a relaxed line, tidy warm kitchen corner, cream and sage tones, soft light. No text.
- **Alt** : Chien âgé mangeant à une gamelle surélevée, le cou et le dos dans une posture détendue.
- **Rationale** : Illustre le confort au repas pour un chien arthrosique.

### Image 23
- **Objectif** : montrer une ration rendue plus appétente.
- **Plan** : plan medium, plongée, mains préparant la gamelle.
- **Prompt** : Photorealistic medium shot, high angle. An owner's hands preparing a moistened, appetising meal in a bowl on a kitchen counter while an attentive senior dog waits nearby, warm homely mood, soft light. No text.
- **Alt** : Maître préparant une ration humidifiée et appétente, le chien âgé attentif à côté.
- **Rationale** : Représente les ajustements de confort au repas, sans conseil médical.

---

## SAT11 — soins-adaptes-chien-senior

### Image 24
- **Objectif** : montrer un soin des griffes doux et coopératif.
- **Plan** : gros plan, plongée, mains et patte, chien couché calme.
- **Prompt** : Photorealistic close-up, high angle. An owner gently trimming the claws of a calm senior dog lying relaxed, cooperative care, careful soft hands, warm light, neutral cozy background. No text.
- **Alt** : Maître coupant délicatement les griffes d'un vieux chien calme et détendu.
- **Rationale** : Illustre les soins adaptés, plus fréquents et tout en douceur.

### Image 25
- **Objectif** : montrer le soin comme moment de lien.
- **Plan** : plan medium, niveau des yeux, brossage, chien couché.
- **Prompt** : Photorealistic medium shot at eye level. An owner softly brushing a senior dog resting comfortably on a blanket, tender bonding moment, warm natural light, sage and cream tones. No text.
- **Alt** : Brossage doux d'un chien âgé installé confortablement, un moment de tendresse.
- **Rationale** : Ancre le soin comme attention affectueuse, pas comme corvée.

---

## SAT12 — accompagner-fin-de-vie-chien

### Image 26
- **Objectif** : incarner la présence tendre et le confort, avec pudeur.
- **Plan** : plan large, lumière chaude, chien blotti contre le maître.
- **Prompt** : Photorealistic wide shot, warm soft light. A very peaceful old dog nestled against its owner sitting on the floor by a cozy padded bed, gentle embrace, serene dignified atmosphere, warm golden tones. No text, nothing morbid.
- **Alt** : Chien âgé paisible blotti contre son maître sur un couchage douillet, dans une lumière chaude.
- **Rationale** : Représente le réconfort et la présence, cœur de l'accompagnement.

### Image 27
- **Objectif** : clore le cluster sur une image sereine et digne.
- **Plan** : gros plan, niveau des yeux, main sur le flanc du chien endormi.
- **Prompt** : Photorealistic close-up at eye level. An owner's hand resting tenderly on a sleeping old dog's flank, calm and dignified mood, soft warm light, muted cream tones. No text, nothing morbid.
- **Alt** : Main du maître posée tendrement sur son chien âgé endormi, atmosphère sereine et digne.
- **Rationale** : Referme le cluster sur la tendresse et la dignité de la fin de vie.
