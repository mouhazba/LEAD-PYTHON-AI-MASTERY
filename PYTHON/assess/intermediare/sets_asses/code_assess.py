# 1. Qu'est-ce qui différencie fondamentalement un set d'une list en Python ? (donne au moins 2 différences)
# Reponses:
"""
Un set est fondementalement different diiferent d'une liste:
1. un set est un structure python non ordonne et dont les elements sont hashables d'ou le fait qu'il n'accepte pas les doublons.
2. comme avec les cles du dictionnaire les elements du set sont hashables donc unique ce qui confere au set a son time O(1) de recherche d'elements.
"""

# 2. Que va afficher ce code, et pourquoi ?
s = {1, 2, 2, 3, "a", "a"}
print(s)
# Reponse:
s = {1, 2, 2, 3, "a"} # car le doublon n'est pas permis avec les set.

# 3. Tu as deux sets :
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
# Sans exécuter le code, donne le résultat de a & b, a | b, a - b, et a ^ b.
# Reponse:
# a & b = {3, 4}
# a | b = {1, 2, 3, 4, 5, 6}
# a-b = {1, 2}
# a ^ b = {1, 2, 5, 6} # je pense que cela renvoie distinctement les differences systemiques de a et b

# 4. Ce code lève une erreur. Laquelle, et pourquoi ?
# s = {1, 2, [3, 4]}
# Reponse:
# un set n'accepte pas un element mutable [3, 4] en son sein.

# 5. Donne un exemple concret (métier ou technique) où tu utiliserais un set plutôt qu'une list, et explique pourquoi ce choix serait justifié.
# Reponse: je ne sais pas exactement pour etre honnete, tout ce que je sais c'est que dans tout project ou on aurait besoin de conserver d'elements 
# distinctement sans doublon on peut utiliser ou passer par un set pour eliminer les doublons.

# test de hash({1, 2, 3})
print(hash({1, 2, 3})) # unshashable