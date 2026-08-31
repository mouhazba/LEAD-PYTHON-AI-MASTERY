==================================== bilan diagnostic 1 assess ====================================
Bon travail, on a de la matière. Avant de corriger, voici l'évaluation brute — je ne vais pas encore tout expliquer, mais je te renvoie deux points pour que tu les retravailles toi-même.

Ce qui est solide :
- Q2 : correct.
- Q3 : a & b, a | b, a - b tous corrects. Bon raisonnement sur les opérations d'ensemble de base.
- Q3 (a ^ b) et Q5 : tu identifies honnêtement que tu ne sais pas — c'est une info utile, pas une faute.

Deux points à retravailler avant que j'explique quoi que ce soit :

Sur Q1 — tu écris « un set est hashable ». Relis ta phrase : est-ce que c'est le set lui-même qui est hashable, ou autre chose ? Indice : essaie mentalement hash({1, 2, 3}) — qu'est-ce que tu penses qu'il se passe ?

Sur Q4 — tu écris que le set « n'accepte pas un élément [3, 4] immuable ». Une list comme [3, 4], est-elle immuable ou muable (mutable) ? Et est-ce que le problème vient du fait qu'elle est immuable, ou l'inverse ?

Réponds à ces deux questions avant qu'on continue — c'est le genre d'erreur qu'il vaut mieux clarifier maintenant, ça conditionne toute la compréhension des sets.

==================================== bilan diagnostic 2 assess ====================================

Niveau démontré : 🟡 Developing, proche de 🟢 Competent sur la mécanique, mais pas encore sur le jugement d'usage.

Preuves :
- Tu as retrouvé &, |, - par raisonnement, et déduit ^ uniquement à partir du nom de l'opérateur — bon réflexe.
- Deux erreurs initiales (hashabilité du set vs de ses éléments ; mutable vs immutable) corrigées seul après question guidée, et tu es allé jusqu'à tester empiriquement hash({1,2,3}) pour trancher — c'est une bonne démarche d'ingénieur, pas juste "j'ai deviné".
- Point faible net : Q5. Tu sais que les sets éliminent les doublons, mais tu ne sais pas encore justifier un choix set vs list dans un contexte réaliste — c'est le point qu'on va travailler.

Explication (précision technique)

- Structure : un set est une table de hachage, comme un dict sans valeurs (juste des clés). C'est pour ça que ses éléments doivent être hashables (donc immuables pour les types de base : int, str, tuple, frozenset — mais pas list, dict, ni set lui-même).
- Complexité : recherche/ajout/suppression en O(1) en moyenne (average-case), grâce au hachage — mais O(n) dans le pire cas (collisions de hash), à nuancer par rapport à une list qui est O(n) garanti. Cette nuance moyenne/pire-cas est importante à retenir.
- Non ordonné : contrairement à une list, aucun ordre garanti (ni d'insertion, contrairement aux dict depuis Python 3.7).
- Type cousin : frozenset — version immuable (donc hashable) d'un set, utilisable comme clé de dict ou élément d'un autre set.

Cas d'usage réel (réponse à Q5) : deux familles d'usage bien distinctes, pas juste "dédupliquer" :
1. Test d'appartenance rapide : ex. un système d'autorisations où tu vérifies if "admin" in user_roles des milliers de fois — avec une list de 10 000 rôles, 
O(n) à chaque check ; avec un set, O(1).
2. Opérations d'ensemble entre deux collections : ex. trouver les utilisateurs inscrits à une formation ET ayant validé le quiz (inscrits & valides), ceux inscrits mais pas encore actifs (inscrits - actifs), etc. — ça serait beaucoup plus lourd à coder avec des boucles sur des list.
