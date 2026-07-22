# PROMPTS IMAGES — Cluster 6-3 « Socialiser son chiot » (blog CHIEN Gus & Frost)

> **Numérotation GLOBALE du super-silo chiot : 54 → 78** (pilier 54-56, puis 2 par satellite). Les marqueurs `Image N` des `<figure>` dans les corps HTML reprennent ces numéros globaux, **jamais** une numérotation qui repart de 1. Le mapping `ingest_cluster.py` dépend de cette continuité (6-2 s'arrête à 53, 6-4 reprendra à 79).
> **Aucun texte incrusté, aucun logo, aucun packaging, aucune infographie.** Photographie documentaire, pas d'illustration. Le chiot est TOUJOURS présent et net.

## Directive esthétique de marque (à concaténer à CHAQUE prompt)

`natural documentary photography, soft diffused warm daylight, muted earthy Gus & Frost palette (deep forest green, cream, sage, warm terracotta accents), realistic contemporary French home or street setting, believable ordinary people, no stock-photo smiles, no posing, gentle film grain, a real puppy always present and in sharp focus, ethologically correct relaxed body language, no text, no logo, no watermark, no infographic, no product packaging, landscape format 16:9`

- **Taille / format : 16:9 paysage** pour toutes les images d'article (standard maison, cf. C15). Un jeu de déclinaisons **verticales 1000 × 1500 px** pour Pinterest peut être tiré ensuite des heros, hors de ce lot.
- **Nommage** (résolu par `C6-3_images_rename_map.csv`) : `hero-<slug>.png` pour l'image d'ouverture de chaque article, `<slug>-2.png` (et `-3` pour le pilier) pour les secondaires.

## Diversité des races (nouveauté 6-3)

Les clusters précédents fixaient un chiot « type labrador/golden » par défaut, ce qui uniformise tout le blog. Ici, **une race distincte est assignée par article**, choisie parmi des races et croisés courants en France, en variant gabarit, robe et longueur de poil. Règles :

1. **Même chiot dans les 2 (ou 3) images d'un même article** : la race reste constante à l'intérieur d'un article, pour la cohérence visuelle.
2. **La race change d'un article à l'autre** : sur les 12 pages, on croise petit et grand gabarit, poil ras et poil long, robes claires et foncées.
3. Toujours un **chiot (0-6 mois)**, morphologie de chiot (pattes rondes, proportions juvéniles), jamais un adulte miniature.
4. Les scènes de groupe (cours du chiot) montrent **plusieurs races ensemble**.

Rotation retenue : Golden retriever, Beagle, Berger australien (merle), Cavalier King Charles, Border collie, Croisé griffon fauve, Cocker anglais (rouan), Jack Russell, Épagneul breton, Labrador (sable), Croisé bâtard noir et feu, Bouledogue français, plus des groupes mixtes (teckel, berger allemand, bichon-croisé, caniche-croisé).

## Contrôle anti-répétition (cadrage)

Le duo chiot + humain revient souvent : les plans sont donc imposés et variés. Répartition du lot : **7 plans larges, 12 plans moyens, 6 gros plans / plans de détail**. Aucune image ne répète le couple plan + décor d'une autre. Décors variés : salon, cuisine, couloir, perron, trottoir, marché, jardin, sentier, parc, salle de cours, cabinet vétérinaire.

---

## 1. Table globale de renommage (54 → 78)

| N | Nom cible | Slug · rôle | Race | Plan | Alt FR |
|---|---|---|---|---|---|
| 54 | `hero-socialiser-son-chiot.png` | `socialiser-son-chiot` · hero | Golden retriever | large | Chiot golden assis dans un salon, observant calmement un enfant et un adulte, socialisation à la maison |
| 55 | `socialiser-son-chiot-2.png` | `socialiser-son-chiot` · sec. | Beagle | moyen | Chiot beagle en laisse recevant une friandise sur un trottoir, découverte de la ville en douceur |
| 56 | `socialiser-son-chiot-3.png` | `socialiser-son-chiot` · sec. | Groupe mixte | large | Petit groupe de chiots de races différentes en cours collectif sous l'œil d'une éducatrice |
| 57 | `hero-fenetre-socialisation-chiot.png` | `fenetre-socialisation-chiot` · hero | Berger australien | gros plan | Chiot berger australien merle dans sa portée reniflant un objet, socialisation précoce chez l'éleveur |
| 58 | `fenetre-socialisation-chiot-2.png` | `fenetre-socialisation-chiot` · sec. | Berger australien | moyen | Chiot berger australien explorant un carton à la maison, encouragé par sa famille |
| 59 | `hero-sortir-chiot-avant-vaccins.png` | `sortir-chiot-avant-vaccins` · hero | Cavalier King Charles | moyen | Chiot cavalier king charles porté dans les bras le long d'un marché, découverte des bruits |
| 60 | `sortir-chiot-avant-vaccins-2.png` | `sortir-chiot-avant-vaccins` · sec. | Cavalier King Charles | large | Chiot cavalier rencontrant chez soi un chien adulte calme et vacciné, cadre maîtrisé |
| 61 | `hero-chiot-rencontre-autres-chiens.png` | `chiot-rencontre-autres-chiens` · hero | Border collie | moyen | Chiot border collie et chien adulte calme se reniflant dans un jardin sous surveillance |
| 62 | `chiot-rencontre-autres-chiens-2.png` | `chiot-rencontre-autres-chiens` · sec. | Deux jeunes chiens | large | Deux jeunes chiens de races différentes jouant à jeu égal sur une pelouse |
| 63 | `hero-habituer-chiot-personnes-inconnues.png` | `habituer-chiot-personnes-inconnues` · hero | Croisé griffon | moyen | Chiot croisé fauve s'avançant vers un visiteur accroupi qui tend une friandise |
| 64 | `habituer-chiot-personnes-inconnues-2.png` | `habituer-chiot-personnes-inconnues` · sec. | Croisé griffon | large | Enfant assis respectant la distance d'un chiot sous la surveillance d'un adulte |
| 65 | `hero-habituer-chiot-manipulation.png` | `habituer-chiot-manipulation` · hero | Cocker anglais | gros plan | Main tenant délicatement la patte d'un chiot cocker avec une friandise, habituation douce |
| 66 | `habituer-chiot-manipulation-2.png` | `habituer-chiot-manipulation` · sec. | Cocker anglais | moyen | Chiot cocker détendu brossé doucement dans le sens du poil |
| 67 | `hero-habituer-chiot-bruits.png` | `habituer-chiot-bruits` · hero | Jack Russell | moyen | Chiot jack russell recevant une friandise pendant qu'on passe l'aspirateur à distance |
| 68 | `habituer-chiot-bruits-2.png` | `habituer-chiot-bruits` · sec. | Jack Russell | détail | Chiot jack russell somnolant près d'une machine à laver en marche |
| 69 | `hero-habituer-chiot-ville-exterieur.png` | `habituer-chiot-ville-exterieur` · hero | Épagneul breton | moyen | Chiot épagneul breton observant une foule à distance sur un trottoir |
| 70 | `habituer-chiot-ville-exterieur-2.png` | `habituer-chiot-ville-exterieur` · sec. | Épagneul breton | gros plan | Chiot épagneul posant une patte sur une grille métallique, encouragé par une friandise |
| 71 | `hero-habituer-chiot-veterinaire-soins.png` | `habituer-chiot-veterinaire-soins` · hero | Labrador | moyen | Chiot labrador sable détendu sur une table d'examen recevant une friandise |
| 72 | `habituer-chiot-veterinaire-soins-2.png` | `habituer-chiot-veterinaire-soins` · sec. | Labrador | large | Chiot labrador explorant sa caisse de transport ouverte garnie d'une couverture |
| 73 | `hero-ecole-du-chiot-cours-collectifs.png` | `ecole-du-chiot-cours-collectifs` · hero | Groupe mixte | large | Petit groupe de chiots de races variées explorant une salle sous l'œil d'une éducatrice |
| 74 | `ecole-du-chiot-cours-collectifs-2.png` | `ecole-du-chiot-cours-collectifs` · sec. | Croisé bichon | moyen | Chiot timide observant le groupe à distance sans être forcé |
| 75 | `hero-chiot-peureux-craintif.png` | `chiot-peureux-craintif` · hero | Croisé noir et feu | moyen | Chiot croisé un peu en retrait qu'on laisse observer un visiteur sans le forcer |
| 76 | `chiot-peureux-craintif-2.png` | `chiot-peureux-craintif` · sec. | Croisé noir et feu | gros plan | Le même chiot gagnant en confiance, oreilles détendues, recevant une friandise |
| 77 | `hero-erreurs-socialisation-chiot.png` | `erreurs-socialisation-chiot` · hero | Bouledogue français | détail | Chiot bouledogue débordé, oreilles en arrière, entouré de mains d'inconnus, erreur à éviter |
| 78 | `erreurs-socialisation-chiot-2.png` | `erreurs-socialisation-chiot` · sec. | Bouledogue français | moyen | Le même chiot bien accompagné, à distance et récompensé, observant l'agitation en confiance |

---

## 2. Prompts de génération par image

> Chaque `Prompt EN` est prêt à coller : il se termine par le token `[DIRECTIVE MARQUE]` à remplacer par la directive esthétique ci-dessus. La race et le plan sont rappelés pour verrouiller la cohérence intra-article et la variété inter-articles.

### PILIER — socialiser-son-chiot

**Image 54 (HERO)** — `hero-socialiser-son-chiot.png` · Golden retriever · plan large
`Wide bright living-room shot, a Golden retriever puppy sitting with relaxed ears, curiously watching a child and an adult sitting on the floor a little further away, calm warm French interior. [DIRECTIVE MARQUE]`
Alt FR : Chiot golden retriever assis dans un salon, observant calmement un enfant et un adulte, socialisation à la maison.

**Image 55** — `socialiser-son-chiot-2.png` · Beagle · plan moyen
`Medium shot of a Beagle puppy on a leash on a city sidewalk, relaxed, sniffing the ground while a person rewards it with a treat, blurred passers-by, soft late-afternoon light. [DIRECTIVE MARQUE]`
Alt FR : Chiot beagle en laisse recevant une friandise sur un trottoir, découverte de la ville en douceur.

**Image 56** — `socialiser-son-chiot-3.png` · groupe mixte · plan large
`Wide shot of a puppy group class, three or four puppies of different breeds (a Border collie, a French bulldog, a fawn crossbreed) exploring calmly while their families and a trainer watch crouched down, relaxed caring atmosphere. [DIRECTIVE MARQUE]`
Alt FR : Petit groupe de chiots de races différentes en cours collectif sous l'œil d'une éducatrice.

### SAT01 — fenetre-socialisation-chiot

**Image 57 (HERO)** — `hero-fenetre-socialisation-chiot.png` · Berger australien (merle) · gros plan
`Soft close-up of a six-to-seven-week-old blue merle Australian shepherd puppy still among its litter in a warm breeder corner, sniffing an everyday object on the floor, blurred littermates behind, soft natural light. [DIRECTIVE MARQUE]`
Alt FR : Chiot berger australien merle dans sa portée reniflant un objet du quotidien, socialisation précoce chez l'éleveur.

**Image 58** — `fenetre-socialisation-chiot-2.png` · Berger australien (merle) · plan moyen
`Medium shot of a nine-week-old blue merle Australian shepherd puppy in a bright living room, calmly exploring an open cardboard box, a crouching woman encouraging it with an open hand while a child watches from behind. [DIRECTIVE MARQUE]`
Alt FR : Chiot berger australien explorant un carton à la maison, encouragé par sa famille, confiance en construction.

### SAT02 — sortir-chiot-avant-vaccins

**Image 59 (HERO)** — `hero-sortir-chiot-avant-vaccins.png` · Cavalier King Charles · plan moyen
`Outdoor medium shot, a Cavalier King Charles puppy carried in the arms of a person walking along a lively village market, the puppy calm and attentive watching the stalls from the safety of the arms, soft morning light. [DIRECTIVE MARQUE]`
Alt FR : Chiot cavalier king charles porté dans les bras le long d'un marché, découverte des bruits sans poser les pattes au sol.

**Image 60** — `sortir-chiot-avant-vaccins-2.png` · Cavalier King Charles · plan large
`Wide shot in a bright living room, a Cavalier King Charles puppy approaching a large calm adult dog lying on the floor, both relaxed, a person sitting nearby watching kindly. [DIRECTIVE MARQUE]`
Alt FR : Chiot cavalier rencontrant chez soi un chien adulte calme et vacciné, rencontre sociale maîtrisée.

### SAT03 — chiot-rencontre-autres-chiens

**Image 61 (HERO)** — `hero-chiot-rencontre-autres-chiens.png` · Border collie · plan moyen
`Medium shot in a bright garden, a Border collie puppy and a calm light-coated adult dog sniffing each other muzzle to muzzle, both bodies loose, a person crouched nearby supervising, soft late-afternoon light. [DIRECTIVE MARQUE]`
Alt FR : Chiot border collie et chien adulte calme se reniflant dans un jardin sous surveillance, première rencontre réussie.

**Image 62** — `chiot-rencontre-autres-chiens-2.png` · deux jeunes chiens (aussie + labrador) · plan large
`Wide shot on a lawn, two young dogs of similar size and different breeds (an Australian shepherd and a sandy Labrador) playing on equal terms, one in a play-bow, joyful symmetrical movement, two families sitting back. [DIRECTIVE MARQUE]`
Alt FR : Deux jeunes chiens de races différentes jouant à jeu égal sur une pelouse, jeu sain et symétrique.

### SAT04 — habituer-chiot-personnes-inconnues

**Image 63 (HERO)** — `hero-habituer-chiot-personnes-inconnues.png` · Croisé griffon fauve · plan moyen
`Warm medium shot of a fawn wire-haired crossbreed puppy in a bright living room, moving on its own toward a crouching visitor who offers a treat on a flat hand without leaning over, puppy relaxed with soft ears. [DIRECTIVE MARQUE]`
Alt FR : Chiot croisé fauve s'avançant de lui-même vers un visiteur accroupi qui tend une friandise.

**Image 64** — `habituer-chiot-personnes-inconnues-2.png` · Croisé griffon fauve · plan large
`Peaceful wide shot in a garden, a child sitting cross-legged on the floor with a soft gaze while a fawn wire-haired crossbreed puppy rests calmly a short distance away without being touched, a parent crouched close by watching. [DIRECTIVE MARQUE]`
Alt FR : Enfant assis respectant la distance d'un chiot sous la surveillance d'un adulte, rencontre calme et sûre.

### SAT05 — habituer-chiot-manipulation

**Image 65 (HERO)** — `hero-habituer-chiot-manipulation.png` · Cocker anglais (rouan) · gros plan
`Warm close-up of an adult hand gently holding the front paw of a blue roan English cocker spaniel puppy sitting relaxed on a light sofa, the other hand offering a small treat, trusting gaze. [DIRECTIVE MARQUE]`
Alt FR : Main tenant délicatement la patte d'un chiot cocker avec une friandise, habituation douce aux manipulations.

**Image 66** — `habituer-chiot-manipulation-2.png` · Cocker anglais (rouan) · plan moyen
`Medium shot of a blue roan English cocker spaniel puppy lying on its side, perfectly relaxed, while a person sitting on the floor gently brushes it in the direction of the coat, soft brush visible, peaceful bright living room. [DIRECTIVE MARQUE]`
Alt FR : Chiot cocker détendu brossé doucement dans le sens du poil, le brossage comme moment de détente.

### SAT06 — habituer-chiot-bruits

**Image 67 (HERO)** — `hero-habituer-chiot-bruits.png` · Jack Russell · plan moyen
`Medium shot of a Jack Russell terrier puppy sitting in a bright living room, relaxed, receiving a treat from a crouching person, while another family member vacuums a few metres back in slightly blurred background. [DIRECTIVE MARQUE]`
Alt FR : Chiot jack russell recevant une friandise pendant qu'on passe l'aspirateur à distance, habituation positive aux bruits.

**Image 68** — `habituer-chiot-bruits-2.png` · Jack Russell · plan de détail
`Detail shot of a calm Jack Russell terrier puppy lying on a kitchen floor, ears relaxed, a few steps from a running washing machine, a person sitting close by reading quietly, soft morning light. [DIRECTIVE MARQUE]`
Alt FR : Chiot jack russell somnolant près d'une machine à laver en marche, un bruit du quotidien devenu banal.

### SAT07 — habituer-chiot-ville-exterieur

**Image 69 (HERO)** — `hero-habituer-chiot-ville-exterieur.png` · Épagneul breton · plan moyen
`Medium shot of an orange-and-white Brittany spaniel puppy on a leash on a wide sidewalk, sitting and relaxed, sniffing the ground, watching from a distance a blurred crowd and a lively market, soft morning light. [DIRECTIVE MARQUE]`
Alt FR : Chiot épagneul breton observant une foule à distance sur un trottoir, la ville apprivoisée de loin d'abord.

**Image 70** — `habituer-chiot-ville-exterieur-2.png` · Épagneul breton · gros plan
`Slight high-angle close-up of a curious orange-and-white Brittany spaniel puppy stepping one paw onto a metal sidewalk grate, ears attentive, a kind hand offering a treat just in front, textured urban ground visible. [DIRECTIVE MARQUE]`
Alt FR : Chiot épagneul posant une patte sur une grille métallique encouragé par une friandise, découverte d'une surface nouvelle.

### SAT08 — habituer-chiot-veterinaire-soins

**Image 71 (HERO)** — `hero-habituer-chiot-veterinaire-soins.png` · Labrador (sable) · plan moyen
`Medium shot of a sandy Labrador puppy sitting calmly on an examination table with a non-slip mat, relaxed, receiving a treat from a person crouched to its level, soft light of a warm veterinary office. [DIRECTIVE MARQUE]`
Alt FR : Chiot labrador sable détendu sur une table d'examen recevant une friandise, la visite vétérinaire vécue positivement.

**Image 72** — `habituer-chiot-veterinaire-soins-2.png` · Labrador (sable) · plan large
`Wide shot of a sandy Labrador puppy calmly exploring its open transport crate on the floor of a warm living room, half inside, muzzle toward a treat on a soft blanket, peaceful domestic mood. [DIRECTIVE MARQUE]`
Alt FR : Chiot labrador explorant sa caisse de transport ouverte garnie d'une couverture, la caisse comme abri rassurant.

### SAT09 — ecole-du-chiot-cours-collectifs

**Image 73 (HERO)** — `hero-ecole-du-chiot-cours-collectifs.png` · groupe mixte · plan large
`Bright wide shot of a small group of puppies of different breeds (a dachshund, a young German shepherd, a bichon-type crossbreed) exploring a room on a non-slip floor, a trainer crouched in the middle watching, families sitting back. [DIRECTIVE MARQUE]`
Alt FR : Petit groupe de chiots de races variées explorant une salle sous l'œil d'une éducatrice, une séance d'école du chiot.

**Image 74** — `ecole-du-chiot-cours-collectifs-2.png` · croisé bichon · plan moyen
`Medium shot of a shy small bichon-type crossbreed puppy sitting a little apart from the group, ears slightly back, watching the other puppies play from a distance, a trainer's hand resting calmly on the floor near it without forcing. [DIRECTIVE MARQUE]`
Alt FR : Chiot timide observant le groupe à distance sans être forcé, un bon cours respecte son rythme.

### SAT10 — chiot-peureux-craintif

**Image 75 (HERO)** — `hero-chiot-peureux-craintif.png` · Croisé noir et feu · plan moyen
`Medium shot of a black-and-tan medium crossbreed puppy slightly withdrawn in a bright living room, sitting a few steps from a visitor seated on the floor, ears a little low but attentive, a person crouched near it letting it observe without pushing. [DIRECTIVE MARQUE]`
Alt FR : Chiot croisé un peu en retrait qu'on laisse observer un visiteur sans le forcer, aider un chiot craintif en douceur.

**Image 76** — `chiot-peureux-craintif-2.png` · Croisé noir et feu · gros plan
`Close shot of the same black-and-tan crossbreed puppy a little later, now sitting closer to the visitor, relaxed ears and loose tail, calmly taking a treat from an outstretched hand, curious rather than worried. [DIRECTIVE MARQUE]`
Alt FR : Le même chiot gagnant en confiance, oreilles détendues, recevant une friandise, la curiosité prend le dessus.

### SAT11 — erreurs-socialisation-chiot

**Image 77 (HERO)** — `hero-erreurs-socialisation-chiot.png` · Bouledogue français (bringé) · plan de détail (plongée)
`Slight high-angle close-up of a brindle French bulldog puppy visibly overwhelmed in an over-intense scene, ears pinned back, body crouched and gaze averted while several strangers' hands reach toward it, busy blurred background, shown soberly to illustrate what to avoid. [DIRECTIVE MARQUE]`
Alt FR : Chiot bouledogue débordé, oreilles en arrière, entouré de mains d'inconnus, l'erreur de la sur-socialisation à éviter.

**Image 78** — `erreurs-socialisation-chiot-2.png` · Bouledogue français (bringé) · plan moyen (contre-plongée)
`Medium slight low-angle shot of the same brindle French bulldog puppy, this time calm and relaxed at a good distance from a busy scene, sitting near its crouching person who offers a treat, soft ears and curious gaze toward the distant activity. [DIRECTIVE MARQUE]`
Alt FR : Le même chiot bien accompagné, à distance et récompensé, observant l'agitation en confiance.

---

## 3. Tableau de variété (contrôle anti-répétition)

| N | Plan | Décor | Race | Sujet |
|---|---|---|---|---|
| 54 | Large | Salon | Golden retriever | Observation calme du foyer |
| 55 | Moyen | Trottoir | Beagle | Récompense en ville |
| 56 | Large | Salle de cours | Groupe mixte | Cours collectif |
| 57 | Gros plan | Coin d'élevage | Berger australien | Découverte dans la portée |
| 58 | Moyen | Salon | Berger australien | Exploration encouragée |
| 59 | Moyen | Marché | Cavalier | Porté dans les bras |
| 60 | Large | Salon | Cavalier | Rencontre chien adulte |
| 61 | Moyen | Jardin | Border collie | Reniflage sous surveillance |
| 62 | Large | Pelouse | Aussie + Labrador | Jeu à jeu égal |
| 63 | Moyen | Salon | Croisé griffon | Approche d'un visiteur |
| 64 | Large | Jardin | Croisé griffon | Enfant à distance |
| 65 | Gros plan | Canapé | Cocker | Patte tenue + friandise |
| 66 | Moyen | Salon | Cocker | Brossage doux |
| 67 | Moyen | Salon | Jack Russell | Aspirateur à distance |
| 68 | Détail | Cuisine | Jack Russell | Sommeil près d'une machine |
| 69 | Moyen | Trottoir | Épagneul breton | Foule à distance |
| 70 | Gros plan | Trottoir | Épagneul breton | Patte sur une grille |
| 71 | Moyen | Cabinet véto | Labrador | Table d'examen |
| 72 | Large | Salon | Labrador | Caisse de transport |
| 73 | Large | Salle de cours | Groupe mixte | Groupe en exploration |
| 74 | Moyen | Salle de cours | Croisé bichon | Chiot timide à l'écart |
| 75 | Moyen | Salon | Croisé noir et feu | Observation en retrait |
| 76 | Gros plan | Salon | Croisé noir et feu | Confiance qui vient |
| 77 | Détail | Lieu animé | Bouledogue français | Chiot débordé (à éviter) |
| 78 | Moyen | Lieu animé | Bouledogue français | Chiot bien accompagné |

**Contrôle final** : 7 plans larges, 12 plans moyens, 6 gros plans / plans de détail. 12 races/robes distinctes plus 2 scènes de groupe multi-races. Aucun couple plan + décor identique à un autre. Format 16:9 pour tout le lot.
