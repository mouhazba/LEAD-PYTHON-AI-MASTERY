# 1. Écris une list comprehension qui donne les carrés des nombres pairs de 1 à 10.
carre_nombre = [n**2 for n in range(1, 10) if n % 2 == 0]
print(carre_nombre) # output: # [4, 16, 36, 64] Nb la question ne precise pas si 10 est inclu ou pas.

# 2. Quelle est la différence entre [x for x in range(5)] et (x for x in range(5)) ? (nom des deux constructions, et différence de comportement)
# [x for x in range(5)] est une comprehension de liste(utilisant les []) donc produit une liste et est plus lourde en ressource memoire car alloue toute la liste en un coup.
# (x for x in range(5)) est un generateur d'expression(utilisant les ()) donc produit un generateur et est plus leger en ressource memoire car yield les items un a un au fur et a mesure.
print(type((x for x in range(5)))) # produit une class generateur.

# 3. Explique la différence entre ces deux syntaxes — qu'est-ce que chacune fait, et pourquoi la position du if change tout :
#Donne le résultat de chacune.

# Reponse: la difference principale entre ces deux syntaxes qui change la donne est la condition et position du if et le else present dans l'une et absente dans l'autre.
 # la syntaxe a garde le signe des nombres paires du range et change le signe des nombres impaire suivant la condition du if.
a = [x if x % 2 == 0 else -x for x in range(5)]
# [0, -1, 2, -3, 4]

 # tandis que la syntaxe b filtre que les nombres paires du range suivant le if sans else.
b = [x for x in range(5) if x % 2 == 0]
# [0, 2, 4]

# 4. Écris une dict comprehension qui construit {mot: longueur_du_mot} à partir de ["python", "ai", "lead"].
mots = ["python", "ai", "lead"]
longueur_mots = {mot: len(mot) for mot in mots}
print(longueur_mots) # output: {'python': 6, 'ai': 2, 'lead': 4}

# 5. D'après toi, dans quel cas est-ce qu'une comprehension devient une mauvaise idée (moins lisible qu'une boucle classique) ?
# Une compreheshion devient une mauvaise idee lorque les boucles ou conditions dedans deviennent complexes et moins lisibles.
# Je tiens a preciser aussi que dans le type de syntaxe il faut privillegier une liste comprehension pluto qu'un generateur d'expression si la reutililisation de la liste est envisageable.