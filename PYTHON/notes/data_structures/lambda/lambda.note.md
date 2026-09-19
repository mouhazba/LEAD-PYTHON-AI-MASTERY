# lambda — juste les points qui manquent

Quand l'utiliser : uniquement pour une fonction jetable, à une seule expression, généralement passée en argument (key=, sorted, map, filter, callback court).

# Quand NE PAS l'utiliser :
carre = lambda x: x ** 2  # mauvais style
Si tu l'assignes à un nom, autant écrire une def — c'est plus lisible, débogable (une lambda n'a pas de nom utile dans une stacktrace), et supporte les annotations de type. PEP 8 le déconseille explicitement.

# Piège classique : une lambda ne peut contenir qu'une expression, pas d'instructions (if/else va, mais pas d'affectation, pas de boucle for, pas de try).