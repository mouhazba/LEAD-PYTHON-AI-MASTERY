
1. .items() — parcourir clé et valeur ensemble

L'idée et pourquoi c'est utile
Tu fais actuellement for cle in eleve: eleve[cle] — ça marche, mais Python doit refaire une recherche par clé (eleve[cle]) à chaque tour de boucle. 
.items() te donne directement les deux en une seule fois, sous forme de tuple (clé, valeur), sans recherche supplémentaire.

Il existe trois méthodes sœurs, à connaître ensemble :
- .keys() → juste les clés
- .values() → juste les valeurs
- .items() → les paires (clé, valeur)

Exemple
eleve = {"nom": "Awa", "age": 21}

for cle, valeur in eleve.items():
    print(cle, valeur)
Remarque : cle, valeur fait un unpacking du tuple retourné à chaque itération — c'est le même mécanisme que a, b = (1, 2).

Pièges fréquents
- Écrire for cle, valeur in eleve (oublier .items()) → erreur, car parcourir un dict brut ne donne que les clés (des strings ici), pas des tuples de 2 éléments à décompresser.
- Modifier le dict (ajouter/supprimer une clé) pendant qu'on itère dessus avec .items() → RuntimeError: dictionary changed size during iteration.
  Si tu dois modifier en cours de route, itère sur une copie : for cle, valeur in list(eleve.items()):.

Lien avec ce que tu sais
Ton intuition sur enumerate() était juste : .items() est au dict ce que enumerate() est à la liste — un moyen d'obtenir deux informations synchronisées par itération, sans recherche manuelle.

---
2. Dict comprehensions

L'idée et pourquoi c'est utile
Tu connais sûrement les list comprehensions ([x**2 for x in range(5)]). Le dict comprehension est la même logique, mais pour construire un dictionnaire en une seule ligne, sans boucle explicite avec dict_name[cle] = valeur répété.

C'est directement utile pour ta réponse à la Q5 : au lieu d'initialiser un dict vide puis de le remplir dans une boucle classique, tu peux parfois construire le dict directement.

Exemple
mots = ["chat", "chien", "oiseau", "chat", "chien", "chat", "oiseau", "chat", "chien"]

# longueur de chaque mot
longueurs = {mot: len(mot) for mot in mots}
# {'chat': 4, 'chien': 3, 'oiseau': 2}

# avec condition (filtre)
longs = {mot: len(mot) for mot in mots if len(mot) > 2}
# {'chat': 4, 'chien': 3}

Pièges fréquents
- Utiliser une dict comprehension quand la logique nécessite un état qui dépend d'itérations précédent comme dans la question Q5, où la valeur dépend de si le mot a déjà été vu
- → impossible proprement en comprehension simple, il faut alors une boucle classique ou Counter (point 3). Ne force pas une comprehension là où ça complexifie plus que ça ne simplifie.
- Confondre avec un set comprehension : {x for x in ...} (sans :) crée un set, pas un dict. La présun dict comprehension.

Lien avec ce que tu sais
C'est une manière plus concise d'écrire ce que tu fais déjà en Q2(b) (eleve["filiere"] = "Info") ou en Q1(c) (dict(cle_x=val_x)) — juste appliqué à une transformation depuis un itérable existant plutôt qu'à des valeurs écrites à
la main.

---

---
3. Hashabilité des clés

L'idée et pourquoi c'est utile
Tu as évoqué en Q1 que le dict permet un accès rapide par clé. La raison technique : un dict est une table de hashage. Chaque clé est passée dans une fonction de hachage (hash()) qui produit un nombre, utilisé pour localiser directement la valeur — d'où l'accès quasi-instantané, sans parcourir tous les éléments (contrairement à une recherche dans une liste).

Conséquence directe : une clé de dict doit être hashable, c'est-à-dire immuable. En pratique :
- ✅ Autorisé comme clé : str, int, float, bool, tuple (si son contenu est lui-même hashable)
- ❌ Interdit comme clé : list, dict, set (ce sont des objets mutables, donc non hashables)

Exemple
d = {(1, 2): "point A"}   # OK, tuple hashable
d = {[1, 2]: "point A"}   # TypeError: unhashable type: 'list'

Pièges fréquents
- Vouloir utiliser une liste comme clé (ex : coordonnées [x, y]) → erreur. Solution : convertir en tuple (x, y).
- Oublier que si tu utilises un tuple comme clé, ce tuple doit lui-même ne contenir que des éléments hashables ((1, [2,3]) n'est pas hashable, car il contient une liste).

Lien avec ce que tu sais
Ça explique pourquoi dict est plus rapide que liste pour la recherche par clé (ta réponse Q1) — c'est le hashable qui rend cela possible, et c'est ce même mécanisme qui impose la contrainte sur le type des clés (contrairement aux valeurs, qui peuvent être n'importe quoi, y compris des listes).

---
4. Ordre d'insertion

L'idée et pourquoi c'est utile
Depuis Python 3.7, les dicts conservent l'ordre d'insertion des clés (c'est une garantie officielle du langage, pas un détail d'implémentation). 
Avant 3.7, l'ordre n'était pas garanti.

Concrètement : quand tu parcours un dict avec .items(), .keys() ou une boucle, tu obtiens toujours les clés dans l'ordre où elles ont été ajoutées — pas un ordre aléatoire, pas trié alphabétiquement.

Exemple
d = {}
d["z"] = 1
d["a"] = 2
d["m"] = 3
print(list(d.keys()))  # ['z', 'a', 'm'] — ordre d'insertion, PAS alphabétique

Pièges fréquents
- Croire qu'un dict est trié par clé — non, il faut faire sorted(d.items()) explicitement si tu veux un ordre alphabétique/numérique.
- Modifier la valeur d'une clé existante ne change pas sa position ; mais supprimer une clé puis la place a la fin.