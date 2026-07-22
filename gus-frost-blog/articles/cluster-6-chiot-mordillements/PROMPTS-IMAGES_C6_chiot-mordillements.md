# PROMPTS IMAGES — Cluster 6-5 « Mordillements, dentition & mastication du chiot » (blog CHIEN Gus & Frost)

> **Numérotation GLOBALE du super-silo chiot : 104 → 128** (pilier 104-106, puis 2 par satellite). Les marqueurs `Image N` des `<figure>` dans les corps HTML reprennent ces numéros globaux, **jamais** une numérotation qui repart de 1. Continuité : 6-3 s'arrête à 78 ; 6-4 occupe 79-103 ; 6-5 reprend à 104 et s'arrête à 128 (6-6 reprendra à 129).

> **Aucun texte incrusté, aucun logo, aucun packaging, aucune infographie.** Photographie documentaire, pas d'illustration. Le chiot est TOUJOURS présent et net. Renforcement positif : aucune scène de punition, aucune contrainte (seule l'Image 127 illustre SOBREMENT un geste à éviter, sans violence explicite).

## Directive esthétique de marque (à concaténer à CHAQUE prompt, remplace le token `[DIRECTIVE MARQUE]`)

`natural documentary photography, soft diffused warm daylight, muted earthy Gus & Frost palette (deep forest green, cream, sage, warm terracotta accents), realistic contemporary French home or street setting, believable ordinary people, no stock-photo smiles, no posing, gentle film grain, a real puppy always present and in sharp focus, ethologically correct relaxed body language, no text, no logo, no watermark, no infographic, no product packaging, landscape format 16:9`

- **Taille / format : 16:9 paysage** pour toutes les images d'article (standard maison). Déclinaisons Pinterest verticales 1000 × 1500 px à tirer ensuite des heros, hors de ce lot.
- **Nommage** (résolu par `C6-5_images_rename_map.csv`) : `hero-<slug>.png` pour l'image d'ouverture, `<slug>-2.png` (et `-3` pour le pilier) pour les secondaires.

## Diversité des races (12 races distinctes, comme 6-3)

Une race distincte par article, constante à l'intérieur d'un article (même chiot dans ses 2 ou 3 images), variée d'un article à l'autre (gabarit, robe, longueur de poil). Toujours un chiot 0-6 mois aux proportions juvéniles, jamais un adulte miniature. **SAT05 impose une petite race (Yorkshire)** pour illustrer la dent de lait persistante, plus fréquente chez les races naines.

Rotation retenue (par article) : PILIER Golden retriever · SAT01 Border collie · SAT02 Labrador (sable) · SAT03 Jack Russell terrier · SAT04 Beagle · SAT05 Yorkshire terrier · SAT06 Cocker anglais · SAT07 Berger australien · SAT08 Bouledogue français · SAT09 Croisé fauve · SAT10 Cavalier King Charles · SAT11 Épagneul breton.

## Contrôle anti-répétition (cadrage)

Répartition du lot de 25 : **2 plans larges, 14 plans moyens, 9 gros plans / détails**. Décors variés : salon, cuisine, couloir, panier, coin aménagé, carrelage. Aucune image ne répète le couple plan + décor d'une autre.

---

## 1. Table globale de renommage (104 → 128)

| N | Nom cible | Slug · rôle | Race | Plan | Alt FR |
|---|---|---|---|---|---|
| 104 | `hero-mordillements-dentition-chiot.png` | `mordillements-dentition-chiot` · hero | Golden retriever | large | Chiot golden retriever assis sur un tapis mâchouillant un jouet à mâcher, une personne l'observant, salon chaleureux |
| 105 | `mordillements-dentition-chiot-2.png` | `mordillements-dentition-chiot` · sec. | Golden retriever | gros plan | Gros plan sur la gueule d'un chiot golden, une main soulevant la babine, dent de lait et dent définitive |
| 106 | `mordillements-dentition-chiot-3.png` | `mordillements-dentition-chiot` · sec. | Golden retriever | moyen | Enfant tendant un jouet à mâcher en corde à un chiot golden, un parent supervisant, salon lumineux |
| 107 | `hero-chiot-mordille-pourquoi.png` | `chiot-mordille-pourquoi` · hero | Border collie | moyen | Chiot border collie mâchouillant le coin d'un tapis en explorant, une personne l'observant avec bienveillance |
| 108 | `chiot-mordille-pourquoi-2.png` | `chiot-mordille-pourquoi` · sec. | Border collie | moyen | Chiot border collie surexcité en fin de journée bondissant en jeu vers la manche d'une personne |
| 109 | `hero-chiot-mordille-inhibition-morsure.png` | `chiot-mordille-inhibition-morsure` · hero | Labrador (sable) | gros plan | Main se retirant doucement pendant qu'un chiot labrador marque un temps d'arrêt, oreilles attentives |
| 110 | `chiot-mordille-inhibition-morsure-2.png` | `chiot-mordille-inhibition-morsure` · sec. | Labrador (sable) | moyen | Chiot labrador sable mâchouillant avec satisfaction un jouet à mâcher tendu par une main |
| 111 | `hero-arreter-chiot-mordiller-mains-pieds.png` | `arreter-chiot-mordiller-mains-pieds` · hero | Jack Russell terrier | moyen | Chiot jack russell mordillant la cheville d'une personne calme dans une cuisine, scène non dramatisée |
| 112 | `arreter-chiot-mordiller-mains-pieds-2.png` | `arreter-chiot-mordiller-mains-pieds` · sec. | Jack Russell terrier | moyen | Personne accroupie tendant un jouet à mâcher qu'un chiot jack russell attrape à la place de la cheville |
| 113 | `hero-dentition-chiot-etapes.png` | `dentition-chiot-etapes` · hero | Beagle | gros plan | Gros plan sur les petites dents de lait d'un chiot beagle, gueule entrouverte tenue par une main |
| 114 | `dentition-chiot-etapes-2.png` | `dentition-chiot-etapes` · sec. | Beagle | moyen | Personne soulevant la babine d'un chiot beagle, dent définitive poussant près d'une dent de lait |
| 115 | `hero-chiot-perd-dents-lait.png` | `chiot-perd-dents-lait` · hero | Yorkshire terrier | gros plan | Minuscule dent de lait sur un doigt reniflée par un chiot yorkshire curieux, lumière du matin |
| 116 | `chiot-perd-dents-lait-2.png` | `chiot-perd-dents-lait` · sec. | Yorkshire terrier | gros plan | Personne examinant la canine d'un chiot yorkshire, dent de lait accolée à la dent définitive |
| 117 | `hero-soulager-douleur-dents-chiot.png` | `soulager-douleur-dents-chiot` · hero | Cocker anglais | gros plan | Chiot cocker allongé sur un carrelage frais mâchouillant un jouet givré sorti du congélateur |
| 118 | `soulager-douleur-dents-chiot-2.png` | `soulager-douleur-dents-chiot` · sec. | Cocker anglais | moyen | Personne présentant un linge humide refroidi qu'un chiot cocker mordille doucement |
| 119 | `hero-chiot-besoin-macher.png` | `chiot-besoin-macher` · hero | Berger australien | gros plan | Chiot berger australien dans son panier mâchouillant un jouet souple adapté à sa taille |
| 120 | `chiot-besoin-macher-2.png` | `chiot-besoin-macher` · sec. | Berger australien | moyen | Chiot berger australien occupé seul avec un jouet à fourrer, une personne vaquant en arrière-plan |
| 121 | `hero-jouets-mastication-chiot.png` | `jouets-mastication-chiot` · hero | Bouledogue français | moyen | Chiot bouledogue français choisissant parmi plusieurs jouets à mâcher, une personne l'observant |
| 122 | `jouets-mastication-chiot-2.png` | `jouets-mastication-chiot` · sec. | Bouledogue français | gros plan | Gros plan d'un jouet en caoutchouc souple mordillé par un chiot bouledogue, matière qui se déforme |
| 123 | `hero-chiot-mache-detruit-tout.png` | `chiot-mache-detruit-tout` · hero | Croisé fauve | moyen | Chiot croisé fauve près d'un coussin mâchouillé l'air innocent, une personne arrivant sans gronder |
| 124 | `chiot-mache-detruit-tout-2.png` | `chiot-mache-detruit-tout` · sec. | Croisé fauve | moyen | Chiot croisé fauve occupé avec un jouet dans un coin aménagé, parc bas et couchage moelleux |
| 125 | `hero-chiot-mordille-enfants.png` | `chiot-mordille-enfants` · hero | Cavalier King Charles | moyen | Enfant tendant à deux mains un jouet à mâcher à un chiot cavalier king charles, un parent supervisant |
| 126 | `chiot-mordille-enfants-2.png` | `chiot-mordille-enfants` · sec. | Cavalier King Charles | large | Chiot cavalier king charles endormi dans son panier pendant que deux enfants jouent plus loin |
| 127 | `hero-erreurs-mordillements-chiot.png` | `erreurs-mordillements-chiot` · hero | Épagneul breton | gros plan | Chiot épagneul breton inquiet reculant devant une main levée, scène sobre, geste à éviter |
| 128 | `erreurs-mordillements-chiot-2.png` | `erreurs-mordillements-chiot` · sec. | Épagneul breton | moyen | Le même chiot épagneul détendu mâchouillant un jouet tendu par une personne calme et souriante |

---

## 2. Prompts de génération par image

> Chaque `Prompt EN` est prêt à coller : il se termine par le token `[DIRECTIVE MARQUE]` à remplacer par la directive esthétique ci-dessus. La race et le plan sont rappelés pour verrouiller la cohérence intra-article et la variété inter-articles.

### PILIER — mordillements-dentition-chiot

**Image 104 (HERO)** — `hero-mordillements-dentition-chiot.png` · Golden retriever · plan large
`Wide bright living-room shot, a Golden retriever puppy about two months old sitting on a rug, a sausage-shaped chew toy tucked between its front paws, chewing calmly while a person sits on the floor watching a little further away, calm warm French interior. [DIRECTIVE MARQUE]`
Alt FR : Chiot golden retriever assis sur un tapis mâchouillant un jouet à mâcher, une personne l'observant, salon chaleureux.

**Image 105 ** — `mordillements-dentition-chiot-2.png` · Golden retriever · gros plan
`Soft close-up of a four-month-old Golden retriever puppy's slightly open mouth, gently held by a human hand lifting a lip to reveal the gum, a small milk tooth beside an erupting adult tooth, natural light, calm caring gesture. [DIRECTIVE MARQUE]`
Alt FR : Gros plan sur la gueule d'un chiot golden, une main soulevant la babine, dent de lait et dent définitive.

**Image 106 ** — `mordillements-dentition-chiot-3.png` · Golden retriever · plan moyen
`Warm medium shot of a six-or-seven-year-old child sitting on the floor holding out a rope chew toy to an attentive Golden retriever puppy, a parent crouched right beside supervising with a smile, bright living room, relaxed safe atmosphere. [DIRECTIVE MARQUE]`
Alt FR : Enfant tendant un jouet à mâcher en corde à un chiot golden, un parent supervisant, salon lumineux.

### SAT01 — chiot-mordille-pourquoi

**Image 107 (HERO)** — `hero-chiot-mordille-pourquoi.png` · Border collie · plan moyen
`Medium shot of a two-to-three-month-old Border collie puppy exploring, chewing the corner of a rug in a living room, focused and curious, a person sitting nearby watching kindly, soft late-afternoon light. [DIRECTIVE MARQUE]`
Alt FR : Chiot border collie mâchouillant le coin d'un tapis en explorant, une personne l'observant avec bienveillance.

**Image 108 ** — `chiot-mordille-pourquoi-2.png` · Border collie · plan moyen
`Lively medium shot of a Border collie puppy clearly over-excited at the end of the day, mouth open in play, bouncing toward the sleeve of a person sitting on the floor, shown tenderly to illustrate the evening excitement peak, warm evening light. [DIRECTIVE MARQUE]`
Alt FR : Chiot border collie surexcité en fin de journée bondissant en jeu vers la manche d'une personne.

### SAT02 — chiot-mordille-inhibition-morsure

**Image 109 (HERO)** — `hero-chiot-mordille-inhibition-morsure.png` · Labrador (sable) · gros plan
`Warm close-up of a human hand gently withdrawing while a three-month-old yellow Labrador puppy makes a clear pause, ears up and attentive, muzzle raised toward the hand, bright living room bathed in soft light, the exact moment play stops. [DIRECTIVE MARQUE]`
Alt FR : Main se retirant doucement pendant qu'un chiot labrador marque un temps d'arrêt, oreilles attentives.

**Image 110 ** — `chiot-mordille-inhibition-morsure-2.png` · Labrador (sable) · plan moyen
`Medium shot of a light-coated yellow Labrador puppy happily chewing a sausage-shaped chew toy held out by a human hand, visibly content with half-closed eyes, on a light rug in a warm bright interior, illustrating successful redirection to the right item. [DIRECTIVE MARQUE]`
Alt FR : Chiot labrador sable mâchouillant avec satisfaction un jouet à mâcher tendu par une main.

### SAT03 — arreter-chiot-mordiller-mains-pieds

**Image 111 (HERO)** — `hero-arreter-chiot-mordiller-mains-pieds.png` · Jack Russell terrier · plan moyen
`Everyday scene in a bright French kitchen, a three-month-old Jack Russell terrier puppy clinging to a trouser hem and mouthing the ankle of a person standing perfectly calm, relaxed arms, no abrupt gesture, slight high-angle shot showing the scene without drama. [DIRECTIVE MARQUE]`
Alt FR : Chiot jack russell mordillant la cheville d'une personne calme dans une cuisine, scène non dramatisée.

**Image 112 ** — `arreter-chiot-mordiller-mains-pieds-2.png` · Jack Russell terrier · plan moyen
`The same person now crouched at the Jack Russell puppy's level in the kitchen, holding out a chew toy the puppy happily grabs instead of the ankle, shared glance, relaxed kind posture, soft light, illustrating successful redirection. [DIRECTIVE MARQUE]`
Alt FR : Personne accroupie tendant un jouet à mâcher qu'un chiot jack russell attrape à la place de la cheville.

### SAT04 — dentition-chiot-etapes

**Image 113 (HERO)** — `hero-dentition-chiot-etapes.png` · Beagle · gros plan
`Tender close-up of a two-month-old Beagle puppy's slightly open mouth showing its small pointed milk teeth, gently held by a human hand, soft natural light, calm affectionate mood. [DIRECTIVE MARQUE]`
Alt FR : Gros plan sur les petites dents de lait d'un chiot beagle, gueule entrouverte tenue par une main.

**Image 114 ** — `dentition-chiot-etapes-2.png` · Beagle · plan moyen
`A person gently lifting the lip of a five-month-old Beagle puppy to look at an adult tooth erupting beside a milk tooth, calm caring gesture, warm domestic setting, natural light. [DIRECTIVE MARQUE]`
Alt FR : Personne soulevant la babine d'un chiot beagle, dent définitive poussant près d'une dent de lait.

### SAT05 — chiot-perd-dents-lait

**Image 115 (HERO)** — `hero-chiot-perd-dents-lait.png` · Yorkshire terrier · gros plan
`Soft close shot of a tiny white milk tooth resting on a fingertip, held out at the height of a curious young Yorkshire terrier puppy leaning in to sniff it, morning natural light, peaceful everyday interior. [DIRECTIVE MARQUE]`
Alt FR : Minuscule dent de lait sur un doigt reniflée par un chiot yorkshire curieux, lumière du matin.

**Image 116 ** — `chiot-perd-dents-lait-2.png` · Yorkshire terrier · gros plan
`Close shot of a person gently lifting the lip of a small-breed Yorkshire terrier puppy to examine a canine, revealing a small milk tooth next to the erupting adult tooth, calm caring gesture, domestic setting, natural light. [DIRECTIVE MARQUE]`
Alt FR : Personne examinant la canine d'un chiot yorkshire, dent de lait accolée à la dent définitive.

### SAT06 — soulager-douleur-dents-chiot

**Image 117 (HERO)** — `hero-soulager-douleur-dents-chiot.png` · Cocker anglais · gros plan
`Close shot of a four-month-old English Cocker spaniel puppy lying on cool floor tiles, chewing with visible relief a frosted chew toy just out of the freezer, a little condensation on the toy, soft late-afternoon light in a warm French kitchen. [DIRECTIVE MARQUE]`
Alt FR : Chiot cocker allongé sur un carrelage frais mâchouillant un jouet givré sorti du congélateur.

**Image 118 ** — `soulager-douleur-dents-chiot-2.png` · Cocker anglais · plan moyen
`Tender everyday scene, a person crouched offering a small rolled damp chilled cloth to an English Cocker spaniel puppy that mouths it gently while looking up, calm French living room bathed in natural light. [DIRECTIVE MARQUE]`
Alt FR : Personne présentant un linge humide refroidi qu'un chiot cocker mordille doucement.

### SAT07 — chiot-besoin-macher

**Image 119 (HERO)** — `hero-chiot-besoin-macher.png` · Berger australien · gros plan
`Peaceful close shot of an Australian shepherd puppy lying in its cosy bed, absorbed in chewing a soft size-appropriate chew toy, relaxed paws, calm cosy French interior in soft late-afternoon light. [DIRECTIVE MARQUE]`
Alt FR : Chiot berger australien dans son panier mâchouillant un jouet souple adapté à sa taille.

**Image 120 ** — `chiot-besoin-macher-2.png` · Berger australien · plan moyen
`Medium shot of an Australian shepherd puppy on a rug, focused on a stuffed food-dispensing chew toy it works at diligently, while in the blurred background a person goes calmly about their tasks, illustrating a puppy occupying itself alone in a warm interior. [DIRECTIVE MARQUE]`
Alt FR : Chiot berger australien occupé seul avec un jouet à fourrer, une personne vaquant en arrière-plan.

### SAT08 — jouets-mastication-chiot

**Image 121 (HERO)** — `hero-jouets-mastication-chiot.png` · Bouledogue français · plan moyen
`A French bulldog puppy choosing among several chew toys of different sizes and textures laid on a living-room floor, a person crouched right beside watching attentively, soft warm light, calm instructive mood in a French interior. [DIRECTIVE MARQUE]`
Alt FR : Chiot bouledogue français choisissant parmi plusieurs jouets à mâcher, une personne l'observant.

**Image 122 ** — `jouets-mastication-chiot-2.png` · Bouledogue français · gros plan
`Close shot of a hand holding a soft rubber chew toy while a French bulldog puppy chews it eagerly, the flexible material visibly deforming under the teeth, bright domestic setting, attentive gesture illustrating supervision. [DIRECTIVE MARQUE]`
Alt FR : Gros plan d'un jouet en caoutchouc souple mordillé par un chiot bouledogue, matière qui se déforme.

### SAT09 — chiot-mache-detruit-tout

**Image 123 (HERO)** — `hero-chiot-mache-detruit-tout.png` · Croisé fauve · plan moyen
`Candid living-room scene in bright French light, a three-month-old fawn crossbreed puppy sitting beside a slightly chewed cushion and shoe, looking perfectly innocent with head tilted, while a person walks calmly into frame without scolding, amused tender expression, soft end-of-day light. [DIRECTIVE MARQUE]`
Alt FR : Chiot croisé fauve près d'un coussin mâchouillé l'air innocent, une personne arrivant sans gronder.

**Image 124 ** — `chiot-mache-detruit-tout-2.png` · Croisé fauve · plan moyen
`Warm medium shot of a three-month-old fawn crossbreed puppy settled comfortably in a well-arranged corner of the living room, a low playpen and soft bed, quietly busy with a chew occupation toy between its paws, calm tidy atmosphere, natural light in a cosy French interior. [DIRECTIVE MARQUE]`
Alt FR : Chiot croisé fauve occupé avec un jouet dans un coin aménagé, parc bas et couchage moelleux.

### SAT10 — chiot-mordille-enfants

**Image 125 (HERO)** — `hero-chiot-mordille-enfants.png` · Cavalier King Charles · plan moyen
`Bright medium shot of a child sitting cross-legged on a living-room floor, holding out with both hands a soft chew toy to an attentive Cavalier King Charles puppy, a parent crouched right beside supervising with a calm smile, soft afternoon light, serene safe atmosphere. [DIRECTIVE MARQUE]`
Alt FR : Enfant tendant à deux mains un jouet à mâcher à un chiot cavalier king charles, un parent supervisant.

**Image 126 ** — `chiot-mordille-enfants-2.png` · Cavalier King Charles · plan large
`Peaceful wide shot of a Cavalier King Charles puppy curled up in its soft bed in a quiet corner of the living room, heavy eyelids, while two children play quietly further away at the back of the room without disturbing it, warm soft light, calm family interior. [DIRECTIVE MARQUE]`
Alt FR : Chiot cavalier king charles endormi dans son panier pendant que deux enfants jouent plus loin.

### SAT11 — erreurs-mordillements-chiot

**Image 127 (HERO)** — `hero-erreurs-mordillements-chiot.png` · Épagneul breton · gros plan
`Sober close shot in neutral light of a slightly worried three-month-old Brittany spaniel puppy, ears back and body leaning away, turning its head from a human hand raised above it, no explicit violence, clean neutral indoor background, illustrating a gesture to avoid. [DIRECTIVE MARQUE]`
Alt FR : Chiot épagneul breton inquiet reculant devant une main levée, scène sobre, geste à éviter.

**Image 128 ** — `erreurs-mordillements-chiot-2.png` · Épagneul breton · plan moyen
`Warm medium shot of the same Brittany spaniel puppy, now perfectly relaxed, soft ears and loose body, calmly chewing a chew toy held out by a calm smiling person crouched beside it, soft golden light of a welcoming interior, companionable mood. [DIRECTIVE MARQUE]`
Alt FR : Le même chiot épagneul détendu mâchouillant un jouet tendu par une personne calme et souriante.
