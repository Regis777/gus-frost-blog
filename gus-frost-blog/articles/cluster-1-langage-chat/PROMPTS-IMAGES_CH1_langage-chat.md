# CH1 — Le langage du chat — Prompts images consolidés

> 27 images, numérotation séquentielle sur tout le cluster (marqueur « Image N » par `<figure>`).
> Destination : Shopify Files. Nommage attendu après ingestion : `hero-langage-du-chat.png` (Image 1) + secondaires renommés par `ingest_cluster.py` depuis `CH1_images_map.csv`.
> Style de marque commun (à rappeler dans chaque génération) : **photographie réaliste, lumière naturelle douce, ambiance premium et chaleureuse, situations réelles de la vie avec un chat, aucun texte incrusté. Chats crédibles et expressifs (races et robes variées), maîtres attentionnés, décors francophones / européens ordinaires (appartement, maison, rebord de fenêtre, cuisine, salon). Palette en harmonie avec la marque : vert forêt, crème, sauge, touches terracotta et lime.** Ratio paysage 16:9 pour le hero, 4:3 pour les secondaires. Densité de sujets faible, beaucoup d'air, mise au point nette sur le chat.
>
> **Variété visuelle (important) :** ce cluster comporte beaucoup de gros plans de visage et de scènes de chat calme en intérieur. Pour éviter que les images se ressemblent, chaque prompt impose un **type de plan** et un **angle** distincts (large / medium / gros plan / macro ; plongée / contre-plongée / profil / niveau des yeux / ras du sol / vue de dessus), une **posture** différente du chat (assis, en marche, couché en sphinx, en boule, sur le flanc, sur le dos, dressé sur les pattes avant, tête posée) et des **accents de palette** variés. Le type de plan est indiqué en tête de chaque prompt. Ne pas générer deux images avec la même composition. En particulier, différencier nettement les paires proches : Image 2 (gros plan face, clignement) vs Image 16 (gros plan face, pupilles dilatées) ; Image 3 vs Image 22 (frottement de joue) ; Image 11 vs Image 26 (chat qui ronronne, tension) ; Image 4 vs Image 5 (queue dressée).
>
> **Sensibilité CH1 :** montrer des chats sereins, dignes et expressifs, jamais souffrants ni caricaturaux ; aucune scène clinique ni anxiogène (pas de cabinet vétérinaire, pas de matériel médical). Pour les images de tension, de peur ou d'agacement (Images 7, 11, 20, 26), rester subtil et pédagogique : le signal doit être lisible sans dramatisation, le chat n'est jamais maltraité et l'humain reste bienveillant et respectueux.

Légende des champs : **Objectif** (rôle pédagogique dans l'article) · **Plan** (cadrage/angle imposé pour la variété) · **Prompt** (à donner au générateur, EN) · **Alt** (texte alternatif SEO FR) · **Rationale** (pourquoi cette image ici).

---

## PILIER — langage-du-chat

### Image 1 — HERO
- **Objectif** : incarner d'emblée l'idée d'un chat qui « parle » avec tout son corps.
- **Plan** : plan large, niveau des yeux, 16:9. Chat assis de profil, queue enroulée autour des pattes.
- **Prompt** : Photorealistic wide shot at eye level, soft natural daylight from a window. A calm cat sitting in profile on a wooden floor, ears upright and forward, tail neatly curled around its paws, attentive and serene. Muted forest green and cream tones, warm premium editorial mood, plenty of negative space, shallow depth of field. No text.
- **Alt** : Chat assis de profil, oreilles dressées et queue enroulée autour des pattes, attentif près d'une fenêtre.
- **Rationale** : Pose le thème du langage corporel global dès le hero, tous signaux visibles ensemble.

### Image 2
- **Objectif** : illustrer le clignement lent, signal de confiance.
- **Plan** : gros plan, niveau des yeux, face. Chat couché, yeux mi-clos.
- **Prompt** : Photorealistic tight close-up at eye level. A relaxed cat's face with half-closed eyes in a slow blink, soft and trusting expression, chin low, warm window light, cream and sage tones, serene premium mood. No text.
- **Alt** : Gros plan sur le visage d'un chat aux yeux mi-clos dans un clignement lent, expression douce et détendue.
- **Rationale** : Introduit le signal d'apaisement le plus emblématique du chat.

### Image 3
- **Objectif** : montrer le marquage par frottement comme communication.
- **Plan** : plan medium, légère plongée, chat debout de profil en mouvement.
- **Prompt** : Photorealistic medium shot, slight high angle. A cat standing in profile rubbing its cheek against the wooden corner of a piece of furniture, tail up, cosy home interior, terracotta and cream accents, soft natural light. No text.
- **Alt** : Chat debout qui frotte sa joue contre le coin d'un meuble en bois dans une ambiance chaleureuse d'intérieur.
- **Rationale** : Clôt le pilier sur le marquage affectueux, pont vers le territoire.

---

## SAT01 — queue-chat-signification

### Image 4
- **Objectif** : montrer la queue haute au bout recourbé, signal de confiance.
- **Plan** : plan large, ras du sol (contre-plongée), chat en marche vers la caméra.
- **Prompt** : Photorealistic wide shot from a low ground-level angle. A cat trotting toward the camera with its tail held high and straight, the tip curled into a question-mark hook, bright open living room, sage and lime accents, soft daylight. No text.
- **Alt** : Chat qui s'avance, queue dressée bien verticale avec le bout recourbé en point d'interrogation, allure joyeuse.
- **Rationale** : Image d'ouverture claire du signal positif le plus lisible de la queue.

### Image 5
- **Objectif** : illustrer la queue dressée qui vibre, excitation joyeuse.
- **Plan** : plan medium, vue de dos en légère plongée, chat de dos.
- **Prompt** : Photorealistic medium shot from behind, slight high angle. A cat seen from the back with its tail raised straight and quivering, oriented toward a person and a food bowl in a bright kitchen, warm cream tones, soft light. No text.
- **Alt** : Chat vu de dos, queue dressée qui vibre légèrement, tourné vers son humain et sa gamelle.
- **Rationale** : Montre le tremblement joyeux de la queue lors des retrouvailles.

---

## SAT02 — oreilles-chat-emotions

### Image 6
- **Objectif** : montrer les oreilles dressées vers l'avant, intérêt serein.
- **Plan** : gros plan, niveau des yeux, face. Chat assis attentif.
- **Prompt** : Photorealistic close-up at eye level. A cat's face with both ears upright and rotated forward, curious and attentive expression, calm home background, sage and cream tones, soft natural light. No text.
- **Alt** : Portrait d'un chat aux oreilles bien dressées et orientées vers l'avant, regard curieux et attentif.
- **Rationale** : Ancre la position positive des oreilles en ouverture.

### Image 7
- **Objectif** : illustrer les oreilles plaquées en arrière, peur ou tension.
- **Plan** : plan medium, profil, chat légèrement reculé.
- **Prompt** : Photorealistic medium shot in profile. A cat with its ears flattened back against its head, body slightly withdrawn and low, wary but not distressed expression, neutral muted background, soft light. No text.
- **Alt** : Chat aux oreilles couchées en arrière contre la tête, posture légèrement reculée et méfiante.
- **Rationale** : Montre le signal fort de peur, à lire pour laisser de l'espace au chat.

---

## SAT03 — clignement-lent-chat

### Image 8
- **Objectif** : illustrer le clignement lent chez un chat installé.
- **Plan** : plan medium, niveau des yeux, chat couché en sphinx.
- **Prompt** : Photorealistic medium shot at eye level. A cat lying comfortably in a sphinx pose on a sofa, eyes half closed in a gentle slow blink, calm trusting mood, cream and forest green tones, soft window light. No text.
- **Alt** : Chat allongé confortablement en sphinx, les yeux à demi fermés dans un clignement lent.
- **Rationale** : Montre le signal dans un contexte de détente typique.

### Image 9
- **Objectif** : montrer l'échange de clignements lents entre humain et chat.
- **Plan** : plan large, profil, personne assise au sol face au chat.
- **Prompt** : Photorealistic wide shot in profile. A person sitting on the floor facing their cat a short distance away, both with half-closed eyes exchanging a slow blink, calm living room, warm light, sage and terracotta accents. No text.
- **Alt** : Une personne assise face à son chat, tous deux les yeux mi-clos, échangeant un clignement lent.
- **Rationale** : Illustre le dialogue silencieux, cœur de l'article.

---

## SAT04 — ronronnement-chat-signification

### Image 10
- **Objectif** : montrer le ronronnement de bien-être.
- **Plan** : plan medium, vue de dessus douce, chat lové en boule.
- **Prompt** : Photorealistic medium shot from a soft top-down angle. A cat curled up in a ball on its owner's lap, eyes half closed, body fully relaxed, a hand resting gently on its fur, warm cosy tones, soft light. No text.
- **Alt** : Chat lové en boule sur les genoux de son humain, yeux mi-clos, dans un ronronnement de bien-être.
- **Rationale** : Incarne le ronron de plaisir, le plus connu.

### Image 11
- **Objectif** : illustrer un ronronnement à surveiller, chat isolé.
- **Plan** : plan medium, niveau du sol, chat tassé dans un coin.
- **Prompt** : Photorealistic medium shot at floor level. A cat sitting hunched and compact in a quiet corner of a room, slightly withdrawn, softer muted light, calm but subtly off mood, neutral tones. No text, nothing clinical or distressing.
- **Alt** : Chat au corps un peu tassé, seul dans un coin, dans une posture à surveiller.
- **Rationale** : Montre que le ronron isolé se lit en contexte, sans dramatiser.

---

## SAT05 — miaulements-chat-comprendre

### Image 12
- **Objectif** : montrer un miaulement adressé à l'humain.
- **Plan** : plan medium, niveau des yeux, chat assis gueule ouverte.
- **Prompt** : Photorealistic medium shot at eye level. A cat sitting and looking up at a person, mouth open mid-meow, expressive and communicative, bright kitchen setting, cream and sage tones, soft daylight. No text.
- **Alt** : Chat assis la gueule ouverte en plein miaulement, tourné vers son humain, dans une cuisine.
- **Rationale** : Illustre le miaulement comme langage tourné vers nous.

### Image 13
- **Objectif** : illustrer le gazouillis face à une proie hors de portée.
- **Plan** : plan large, contre-jour de fenêtre, chat dressé sur les pattes avant.
- **Prompt** : Photorealistic wide shot, backlit by a window. A cat propped on its hind legs at a windowsill, front paws up, body tense and focused on a bird outside, chattering, soft rim light, muted tones. No text.
- **Alt** : Chat posté à la fenêtre qui gazouille devant un oiseau, corps tendu vers la vitre.
- **Rationale** : Montre le caquètement et l'instinct de chasse frustré.

---

## SAT06 — vibrisses-moustaches-chat

### Image 14
- **Objectif** : mettre en valeur les vibrisses comme organe sensoriel.
- **Plan** : macro, profil serré, museau.
- **Prompt** : Photorealistic macro close-up in profile. Sharp detail of a cat's muzzle with long whiskers fanned out and catch-lit, fine texture, softly blurred neutral background, natural light. No text.
- **Alt** : Gros plan latéral sur le museau d'un chat mettant en valeur ses longues vibrisses déployées.
- **Rationale** : Rend visible la finesse et l'importance des vibrisses.

### Image 15
- **Objectif** : illustrer la gamelle large qui respecte les vibrisses.
- **Plan** : plan medium, légère plongée, chat penché sur une gamelle.
- **Prompt** : Photorealistic medium shot, slight high angle. A cat eating comfortably from a wide, shallow bowl, whiskers relaxed and free, tidy kitchen floor, cream and sage tones, soft light. No text.
- **Alt** : Chat qui mange dans une gamelle large et peu profonde, vibrisses détendues et libres.
- **Rationale** : Montre le confort des vibrisses au repas, pont vers le cluster gamelle.

---

## SAT07 — pupilles-yeux-chat

### Image 16
- **Objectif** : illustrer des pupilles dilatées par l'émotion en pleine lumière.
- **Plan** : gros plan, niveau des yeux, face frontale.
- **Prompt** : Photorealistic tight close-up at eye level, frontal. A cat's face in a well-lit room with strongly dilated round pupils, alert and stimulated expression, crisp catchlights, muted background. No text.
- **Alt** : Portrait rapproché d'un chat aux pupilles très dilatées dans une pièce éclairée, expression d'excitation.
- **Rationale** : Montre l'information émotionnelle portée par la pupille.

### Image 17
- **Objectif** : illustrer la grammaire du regard entre deux chats.
- **Plan** : plan large, ras du sol, deux chats de profil face à face.
- **Prompt** : Photorealistic wide shot at ground level. Two cats facing each other a short distance apart, one holding a hard fixed stare, the other turning its head away to look aside, quiet tension, neutral floor setting, soft light. No text.
- **Alt** : Deux chats qui se font face, l'un au regard fixe soutenu, l'autre détournant les yeux.
- **Rationale** : Rend visibles le défi du regard fixe et l'apaisement du regard détourné.

---

## SAT08 — postures-corps-chat

### Image 18
- **Objectif** : montrer la posture pleinement détendue.
- **Plan** : plan large, ras du sol, chat allongé sur le flanc.
- **Prompt** : Photorealistic wide shot at ground level. A cat lying stretched out on its side in a warm patch of sunlight on the floor, legs extended, completely relaxed, cream and lime accents, soft warm light. No text.
- **Alt** : Chat allongé sur le flanc, pattes étirées, dans un rayon de soleil, parfaitement détendu.
- **Rationale** : Incarne la détente corporelle de référence.

### Image 19
- **Objectif** : illustrer le ventre offert comme signe de confiance à ne pas surinterpréter.
- **Plan** : plan medium, vue de dessus, chat sur le dos.
- **Prompt** : Photorealistic medium shot from above. A cat rolled onto its back showing its belly on a rug, relaxed, a person nearby seated calmly without touching the belly, warm cosy tones, soft light. No text.
- **Alt** : Chat sur le dos, ventre exposé dans une posture de confiance, un humain à proximité sans le toucher.
- **Rationale** : Illustre le malentendu du ventre offert.

---

## SAT09 — signes-agacement-inconfort-chat

### Image 20
- **Objectif** : montrer les signaux d'arrêt pendant une caresse.
- **Plan** : gros plan, niveau des yeux, main et arrière-train du chat.
- **Prompt** : Photorealistic close-up at eye level. A hand stroking a cat's back while the cat's tail begins to lash and its ears rotate back, subtle rising tension, calm home setting, muted tones. No text, nothing violent.
- **Alt** : Une main caresse un chat dont la queue commence à fouetter et les oreilles à reculer, tension naissante.
- **Rationale** : Rend lisibles les signaux d'arrêt à respecter.

### Image 21
- **Objectif** : illustrer le respect du choix du chat de ne pas être touché.
- **Plan** : plan medium, profil, chat qui se détourne.
- **Prompt** : Photorealistic medium shot in profile. A cat calmly turning and stepping away from a gently offered open hand, unhurried, respectful mood, bright neutral room, sage tones, soft light. No text.
- **Alt** : Chat qui se détourne calmement d'une main tendue, choisissant de ne pas interagir.
- **Rationale** : Montre le consentement respecté qui construit la confiance.

---

## SAT10 — marquage-facial-frottements-chat

### Image 22
- **Objectif** : illustrer le marquage facial contre un objet.
- **Plan** : gros plan, niveau des yeux, chat de trois-quarts.
- **Prompt** : Photorealistic close-up at eye level, three-quarter view. A cat pressing and rubbing the side of its head firmly against the corner of a piece of furniture, content expression, warm home tones, soft light. No text.
- **Alt** : Chat qui frotte vigoureusement sa joue contre l'angle d'un meuble, expression satisfaite.
- **Rationale** : Rend visible le dépôt de phéromones faciales.

### Image 23
- **Objectif** : montrer le coup de tête affectueux vers l'humain.
- **Plan** : gros plan, légère contre-plongée, tête du chat contre une main.
- **Prompt** : Photorealistic close-up, slight low angle. A cat gently head-butting the open hand of a person, foreheads of trust, warm intimate mood, cream and terracotta tones, soft light. No text.
- **Alt** : Chat qui donne un coup de tête affectueux contre la main de son humain, échange de confiance.
- **Rationale** : Illustre le bunting comme marque d'appartenance.

---

## SAT11 — observer-chat-carnet-signaux

### Image 24
- **Objectif** : montrer l'observation attentive et bienveillante du chat.
- **Plan** : plan large, profil, personne assise regardant le chat.
- **Prompt** : Photorealistic wide shot in profile. A person sitting quietly observing their cat resting on a sofa a short distance away, calm attentive posture, bright airy living room, sage and cream tones, soft light. No text.
- **Alt** : Une personne observe attentivement son chat installé sur le canapé, regard bienveillant et posé.
- **Rationale** : Incarne la posture d'observation, cœur de la méthode.

### Image 25
- **Objectif** : illustrer le carnet d'observation.
- **Plan** : gros plan, vue de dessus, carnet ouvert au premier plan.
- **Prompt** : Photorealistic close-up from above. An open notebook with a few handwritten notes on a table, a pen beside it, a relaxed cat softly blurred in the background, warm daylight, cream tones. No readable text.
- **Alt** : Un carnet d'observation ouvert avec quelques notes, un chat détendu en arrière-plan flou.
- **Rationale** : Rend concret l'outil du carnet d'observation.

---

## SAT12 — idees-recues-langage-chat

### Image 26
- **Objectif** : contredire l'idée que ronron rime toujours avec bonheur.
- **Plan** : plan medium, niveau des yeux, chat assis corps un peu tendu.
- **Prompt** : Photorealistic medium shot at eye level. A cat sitting upright with a subtly tense body and slightly sideways ears, quietly purring yet not fully relaxed, neutral room, muted tones, soft light. No text, nothing distressing.
- **Alt** : Chat au corps un peu tendu qui ronronne, contredisant l'idée que le ronron rime toujours avec bonheur.
- **Rationale** : Illustre le mythe du ronronnement corrigé.

### Image 27
- **Objectif** : clore sur une relation bien comprise et complice.
- **Plan** : plan large, légère contre-plongée, humain et chat ensemble.
- **Prompt** : Photorealistic wide shot, slight low angle. A person and their cat sharing a gentle mutual gaze, close and complicit, bright warm home, forest green and lime accents, soft natural light, plenty of air. No text.
- **Alt** : Un humain et un chat en pleine complicité, échange de regards doux, illustrant une relation bien comprise.
- **Rationale** : Referme le cluster sur le chat lisible et compris, message clé.

---

## Contrôle final de variété (à vérifier avant génération)

- **Aucune paire d'images ne partage le même cadrage + angle + posture.** Récapitulatif des plans : large (1, 9, 13, 17, 18, 24, 27), medium (3, 5, 8, 10, 11, 12, 15, 19, 21, 26), gros plan / macro (2, 6, 7 medium-profil, 14, 16, 20, 22, 23, 25). Angles répartis : niveau des yeux, profil, plongée / vue de dessus (3, 5, 10, 15, 19, 25), contre-plongée / ras du sol (4, 17, 18, 23, 27), contre-jour (13).
- **Postures distinctes** : assis (1, 6, 12, 26), en marche (4), de dos (5), sphinx (8), en boule (10), tassé (11), dressé sur les pattes avant (13), sur le flanc (18), sur le dos (19), debout en mouvement (3, 21), tête contre objet/main (22, 23).
- **Paires proches explicitement différenciées** : 2 (clignement, yeux mi-clos) vs 16 (pupilles dilatées) ; 3 (frottement profil plongée) vs 22 (frottement gros plan trois-quarts) ; 4 (queue, contre-plongée en marche) vs 5 (queue, vue de dos) ; 11 (ronron tassé, niveau du sol) vs 26 (ronron assis tendu, niveau des yeux) ; 20 (agacement pendant caresse) vs 7 (peur, oreilles plaquées).
- **Palette** : alterner les accents (crème, sauge, terracotta, lime, vert forêt) et l'heure/lumière (matin, plein jour, contre-jour) d'une image à l'autre.
- **Identité de scène préservée** : les légendes et les alt des articles restent valables ; on diversifie l'exécution visuelle, pas le sujet.
