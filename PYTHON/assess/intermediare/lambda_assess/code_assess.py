# 1.Oui dans une formation python.

# 2. Que fait ce code, selon toi ?
noms = ["Bob", "Alice", "Zoé", "eve"]
resultat = sorted(noms, key=lambda x: x.lower())
# ce code trie les elements de la liste noms en les convertissant  d'abord en minuscule mais ne modie pas la liste elle meme.

# 3. Petit exercice pratique — écris une fonction appliquer(fonction, valeur) qui prend une fonction et une valeur, et retourne le résultat de 
# l'appel de cette fonction sur cette valeur. Puis appelle-la avec une lambda qui multiplie par 2.
def fonction_appliquee(func, val):
    return func(val)
reponse = fonction_appliquee(lambda x: x * 2, 5)
print(reponse) # output 10

#4. Que fait ce code, et pourquoi écrire une fonction comme ça plutôt qu'avec des paramètres nommés classiques ?
def ma_fonction(*args, **kwargs):
    print(args)
    print(kwargs)

ma_fonction(1, 2, 3, nom="Alice", age=30)
# ce code assigne tous les arguements de position (1, 2, 3) dans *arge sous forme de tuple 
# et les arguements nommes(nom="Alice", age=30) dans **kwargs sous forme de dictionnaire. 