# CH6 — Litière, propreté et marquage — Prompts d'images

> 27 images (pilier 3, chaque satellite 2). Numérotation `Image N` alignée sur les marqueurs des articles (ingest_cluster.py les mappe). Diversité imposée : plan, angle et posture uniques d'une image à l'autre (règle de cluster). Le chat est TOUJOURS dans la scène ; aucun packshot produit, aucun texte incrusté.

## Style visuel Gus & Frost (à préfixer à chaque prompt)
Photographie lifestyle premium, intérieur domestique français réaliste et chaleureux, lumière naturelle douce, profondeur de champ marquée, palette sobre et naturelle (bois, crème, touches de vert forêt et terracotta), rendu authentique non publicitaire. Chat photographié avec justesse anatomique, dans une scène de vie réelle. Pas de texte, pas de logo, pas d'objet de marque au premier plan. Les scènes de litière restent sobres et pudiques, jamais explicites.

## Prompts par article


### PILIER — `litiere-proprete-chat`

**Image 1.** plan moyen en légère plongée d'un chat assis bien droit à côté de son bac à litière ouvert dans une pièce calme et lumineuse, tête tournée vers l'objectif, posture attentive et paisible
   _Légende article :_ Un chat en bonne santé utilise sa litière d'instinct. Quand il s'en détourne, c'est un signal à écouter, pas un caprice à corriger.

**Image 2.** plan rapproché en légère contre-plongée d'un chat en train de gratter la litière fine de son bac ouvert, patte avant en mouvement, concentration visible, grains de litière en léger déplacement
   _Légende article :_ Gratter et enfouir est un geste instinctif. Une litière fine et propre, dans un bac assez grand, laisse le chat l'accomplir sans contrainte.

**Image 3.** plan large d'un salon domestique clair et rangé, un chat détendu traversant la pièce d'un pas tranquille, un bac à litière propre visible au fond dans un coin calme, ambiance de foyer apaisé
   _Légende article :_ Un coin toilette propre et bien pensé, tenu à l'écart du passage, est la meilleure prévention contre les problèmes de propreté.


### SAT01 — `choisir-litiere-chat`

**Image 4.** gros plan au ras du sol sur les coussinets d'un chat posés sur une litière fine agglomérante, grains bien visibles, le chat en train de tester le substrat, cadrage bas et net
   _Légende article :_ Le chat évalue sa litière par le contact des coussinets. Une texture fine et sableuse, proche du sol meuble qu'il aurait choisi dans la nature, l'invite à gratter et à enfouir.

**Image 5.** plan moyen de face, un chat qui renifle avec méfiance une litière parfumée fraîchement versée, museau plissé et léger mouvement de recul, lumière douce d'intérieur
   _Légende article :_ Ce que nous percevons comme une senteur fraîche peut saturer l'odorat bien plus fin du chat. Devant un substrat parfumé, beaucoup marquent un recul plutôt qu'un plaisir.


### SAT02 — `choisir-bac-litiere-chat`

**Image 6.** plan large de profil, un grand chat qui se retourne à l'aise à l'intérieur d'un grand bac ouvert rectangulaire, corps entier visible dans le bac, pièce claire
   _Légende article :_ Un bac assez grand laisse le chat se retourner, choisir son orientation et gratter sans contrainte. C'est le premier critère, celui qui règle le plus de problèmes.

**Image 7.** plan moyen en légère plongée, un chat hésitant à l'entrée d'un bac couvert à rabat, seule la tête engagée dans l'ouverture, corps resté à l'extérieur, expression dubitative
   _Légende article :_ Le bac couvert plaît à certains chats et en rebute d'autres. Un chat qui hésite à franchir le rabat vous dit clairement sa préférence.


### SAT03 — `ou-placer-litiere-chat`

**Image 8.** plan large d'un coin buanderie tranquille, un chat entrant sereinement dans un bac ouvert placé à bonne distance d'une gamelle visible à l'autre bout de la pièce, ambiance calme
   _Légende article :_ Un coin retiré et paisible, avec le bac tenu à distance de la gamelle, invite le chat à s'installer sereinement.

**Image 9.** plan moyen en légère contre-plongée, un chat qui interrompt son approche d'un bac coincé près d'un lave-linge, oreilles orientées en arrière, posture méfiante
   _Légende article :_ Un bac coincé près d'un appareil bruyant devient un piège sonore : le chat s'en méfie et finit par l'éviter.


### SAT04 — `combien-bacs-litiere-chat`

**Image 10.** plan large d'un couloir clair avec deux bacs à litière placés à deux points distincts et éloignés, un chat au premier plan se dirigeant tranquillement vers l'un d'eux
   _Légende article :_ Deux bacs comptent pour deux seulement s'ils sont éloignés l'un de l'autre. C'est la distance entre eux qui crée deux vrais accès.

**Image 11.** plan moyen de deux chats se croisant à bonne distance dans une pièce ouverte, chacun ayant un accès dégagé à un bac séparé, postures détendues et sans tension
   _Légende article :_ À plusieurs chats, des bacs répartis garantissent à chacun un accès libre. Personne n'a besoin de négocier un passage ni de se retenir.


### SAT05 — `entretenir-litiere-chat`

**Image 12.** plan rapproché en plongée sur une main tenant une pelle à litière qui retire les amas d'un bac ouvert, le chat assis juste à côté observant l'opération avec attention
   _Légende article :_ Retirer les amas au moins une fois par jour est le geste central de l'entretien. C'est aussi le meilleur moment pour surveiller la santé du chat.

**Image 13.** plan moyen d'un chat qui inspecte son bac fraîchement nettoyé et regarni de litière propre, une patte posée sur le bord, expression satisfaite, pièce lumineuse
   _Légende article :_ Un bac lavé à l'eau chaude et au savon doux, puis regarni de litière propre, redevient un espace neutre et accueillant pour le chat.


### SAT06 — `chat-fait-hors-litiere`

**Image 14.** plan large sobre d'un chat accroupi sur un tapis juste à côté de son bac à litière ouvert, posture d'élimination, air préoccupé, scène de vie mesurée et non explicite
   _Légende article :_ Faire juste à côté du bac n'est pas un défi lancé au maître : c'est un message qu'il faut apprendre à lire, en commençant par la santé.

**Image 15.** plan moyen d'un chat calme examiné avec douceur par des mains de vétérinaire sur une table de consultation, ambiance rassurante et clinique feutrée
   _Légende article :_ La consultation n'est pas la dernière option, c'est la première étape. Elle écarte la douleur avant toute interprétation du comportement.


### SAT07 — `marquage-urinaire-chat`

**Image 16.** plan de profil pudique d'un chat debout près d'un mur, queue dressée à la verticale et légèrement frémissante, posture caractéristique du marquage, cadrage discret sans détail explicite
   _Légende article :_ La signature du marquage : le chat debout, la queue dressée et frémissante, face à une surface verticale. Une posture qui n'a rien à voir avec celle de l'élimination.

**Image 17.** plan large d'un chat perché sur le rebord intérieur d'une fenêtre, corps tendu et fixe, observant un chat extérieur dans le jardin, contexte de déclencheur territorial
   _Légende article :_ Un chat du voisinage aperçu par la fenêtre suffit à mettre le chat de la maison sous tension. L'intrusion visuelle est un déclencheur fréquent de marquage.


### SAT08 — `elimination-inappropriee-chat`

**Image 18.** plan moyen d'un chat qui gratte le rebord de son bac ouvert puis se détourne sans y entrer, expression d'aversion, une patte encore levée
   _Légende article :_ Un chat qui gratte le bord de son bac puis s'en détourne sans y entrer exprime une aversion : quelque chose, dans ce bac, le repousse.

**Image 19.** gros plan sobre d'un chat installé accroupi sur une pile de linge moelleux posée au sol, illustrant une préférence de substrat, ambiance domestique feutrée
   _Légende article :_ Accroupi sur une pile de linge moelleux, ce chat illustre la préférence : il a adopté une surface qui lui plaît davantage que son bac.


### SAT09 — `nettoyer-odeurs-urine-chat`

**Image 20.** plan rapproché en plongée d'une personne nettoyant une tache sur un parquet avec un chiffon, le chat observant la scène à distance, lumière naturelle
   _Légende article :_ Un accident se traite vite et à fond : éponger d'abord, puis neutraliser en profondeur, sans se contenter d'effacer ce que l'on voit.

**Image 21.** plan moyen d'un chat qui renifle longuement un endroit du sol fraîchement nettoyé, museau au ras du sol, vérification olfactive attentive
   _Légende article :_ Le vrai juge du nettoyage, c'est le nez du chat : s'il revient renifler longuement la zone, c'est qu'une trace subsiste pour lui.


### SAT10 — `litiere-chaton-apprentissage`

**Image 22.** gros plan attendri d'un tout petit chaton en train de gratter maladroitement dans un bac à bords très bas, patte avant hésitante, grande litière fine autour de lui
   _Légende article :_ Le geste de gratter est déjà là, même maladroit. Un bac à bords très bas et une litière fine laissent l'instinct s'exprimer sans obstacle.

**Image 23.** plan large d'un chaton sortant d'un petit bac accessible posé près de son couchage douillet, démarche fière et assurée, pièce chaleureuse
   _Légende article :_ Un bac accessible, tout près de son couchage, et l'instinct fait le reste. Le chaton en ressort sûr de lui, sa propreté déjà installée.


### SAT11 — `litiere-chat-age-senior`

**Image 24.** plan moyen de profil d'un chat âgé au pelage grisonnant enjambant avec précaution le bord bas et découpé d'un bac, mouvement lent et prudent, patte levée
   _Légende article :_ Un rebord bas ou découpé transforme un obstacle douloureux en un passage facile. Pour un chat âgé, ce détail change tout.

**Image 25.** plan large d'un vieux chat reposant paisiblement près d'un bac à bords bas accessible dans une pièce de plain-pied lumineuse, atmosphère sereine
   _Légende article :_ Un bac accessible, à portée facile et sans obstacle, rend au chat âgé son confort et sa tranquillité.


### SAT12 — `idees-recues-litiere-chat`

**Image 26.** plan moyen d'un chat qui détourne nettement la tête de l'entrée d'un bac couvert, expression de refus, illustrant le rejet d'une litière parfumée ou d'un bac fermé
   _Légende article :_ Un parfum trop présent ou un bac qui enferme peut suffire à détourner un chat de sa litière. Ce qui nous rassure n'est pas ce qui le rassure.

**Image 27.** plan large d'un maître accroupi qui remplace calmement la litière d'un bac pendant que le chat observe à côté, scène de bonne pratique posée et bienveillante
   _Légende article :_ La bonne réponse à une malpropreté n'est jamais une sanction : c'est un bac propre, une litière adaptée, et le calme retrouvé.
