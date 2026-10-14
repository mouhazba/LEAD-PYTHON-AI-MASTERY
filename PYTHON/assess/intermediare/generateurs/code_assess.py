# 1 Oui

# 2
"""
Une fonction generator est une fonction normale qui contient au moins un yield. La différence clé :

- Appeler la fonction n'exécute rien du tout — ça retourne immédiatement un objet generator (une sorte d'itérateur en pause).
- Chaque fois qu'on lui demande la valeur suivante (via next(), une boucle for, list(), etc.), l'exécution reprend là où elle s'était arrêtée au yield précédent,
 tourne jusqu'au yield suivant, s'y suspend (en gardant tout son état local en mémoire — variables, position dans une boucle), et renvoie la valeur.
"""


# 3 
def carre(n):
    i = 0
    while i < n:
        yield i ** 2
        i += 1

gen =  carre(5)
print(list(gen))
print(list(gen))

# 4 output [0, 1, 4, 9, 16] et []

# 5 
"""
Quand l'exécution de carre(n) sort de la boucle while (car i == n), la fonction se termine normalement — 
comme n'importe quelle fonction qui arrive à sa dernière ligne. En interne, Python traduit ça par : lever StopIteration.

for et list() sont tous les deux construits sur le protocole itérateur : ils appellent next() en boucle, et ont un try/except StopIteration implicite 
autour de cet appel — dès qu'ils la reçoivent, ils arrêtent proprement (pour list(), ça veut dire "renvoyer ce qui a été accumulé jusque-là"). 
C'est exactement le même mécanisme que le except que tu écris toi-même, sauf que celui-ci est intégré au langage et invisible pour toi : 
StopIteration n'est pas une erreur au sens propre, c'est un signal de fin de flux, prévu et géré par convention.

Une fois qu'un générateur a levé StopIteration une première fois, il reste épuisé pour toujours — pas de réinitialisation. 
Donc le deuxième list(gen) appelle next(), reçoit immédiatement StopIteration (rien à faire), et renvoie une liste vide sans avoir rien pu accumuler.

generator function vs generator expression — la vraie distinction

Les deux produisent un objet generator qui suit exactement la même règle d'épuisement à usage unique — donc "réutilisable" n'est pas le bon critère.

La vraie différence :

1. Expressivité : une generator expression (x**2 for x in range(n)) est limitée à une seule expression — comme une list comprehension. 
Pas de if/elif/else complexe, pas de plusieurs yield, pas d'état accumulé, pas de try/except. 
Une generator function (def + yield) peut contenir n'importe quelle logique.
2. La fonction est une "usine à générateurs" : carre elle-même n'est jamais épuisée — tu peux l'appeler carre(5), carre(10), autant de fois que tu veux, 
et chaque appel te donne un nouvel objet generator indépendant. Une expression, elle, tu l'écris et l'évalues une fois pour obtenir un seul objet ; 
si tu veux une deuxième "copie", il faut réécrire/réévaluer l'expression.
3. Style : l'expression est préférée pour une transformation courte, souvent directement inline : sum(x**2 for x in range(n)), 
max(len(mot) for mot in mots) — pas besoin de définir toute une fonction nommée pour ça.
"""
