On attaque les comprehensions. Diagnostic d'abord — pas de cours, juste pour voir où tu en es.

Diagnostic (5 questions)

1. Écris une list comprehension qui donne les carrés des nombres pairs de 1 à 10.
2. Quelle est la différence entre [x for x in range(5)] et (x for x in range(5)) ? (nom des deux constructions, et différence de comportement)
3. Explique la différence entre ces deux syntaxes — qu'est-ce que chacune fait, et pourquoi la position du if change tout :
a = [x if x % 2 == 0 else -x for x in range(5)]
b = [x for x in range(5) if x % 2 == 0]
Donne le résultat de chacune.

4. Écris une dict comprehension qui construit {mot: longueur_du_mot} à partir de ["python", "ai", "lead"].
5. D'après toi, dans quel cas est-ce qu'une comprehension devient une mauvaise idée (moins lisible qu'une boucle classique) ?


