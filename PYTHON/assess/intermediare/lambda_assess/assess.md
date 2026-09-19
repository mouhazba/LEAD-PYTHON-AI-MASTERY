1. As-tu déjà utilisé lambda avant (même en le croisant dans du code) ? Si oui, dans quel contexte ?
2. Que fait ce code, selon toi ?
noms = ["Bob", "Alice", "Zoé", "eve"]
resultat = sorted(noms, key=lambda x: x.lower())

3. Petit exercice pratique — écris une fonction appliquer(fonction, valeur) qui prend une fonction et une valeur, et retourne le résultat de l'appel de cette fonction sur cette valeur. Puis appelle-la avec une lambda qui multiplie par 2.

4. Que fait ce code, et pourquoi écrire une fonction comme ça plutôt qu'avec des paramètres nommés classiques ?
def ma_fonction(*args, **kwargs):
    print(args)
    print(kwargs)

ma_fonction(1, 2, 3, nom="Alice", age=30)