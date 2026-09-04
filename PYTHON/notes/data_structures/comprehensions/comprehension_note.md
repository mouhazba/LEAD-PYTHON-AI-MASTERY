merci j'ai bien compris, pour mes notes ulterieures genere moi  .md bien formate de ceci
:
Comprehensions — approfondissement (Engineering / Advanced)

Niveau 2 — Scope propre (piège que tu n'as pas encore vu)

Depuis Python 3, une comprehension a son propre scope, comme une fonction — contrairement à une boucle for classique qui laisse fuir sa variable dans l'espace englobant.

x = 100
carres = [x for x in range(5)]
print(x)  # 100 — la variable de la comprehension n'a pas fuité

x = 100
for x in range(5):
    pass
print(x)  # 4 — la boucle for a écrasé x dans le scope englobant

Conséquence pratique : tu peux réutiliser un nom de variable dans une comprehension sans risquer d'écraser une variable du même nom à l'extérieur. C'est un changement volontaire par rapport à Python 2 (où les comprehensions fuyaient aussi), corrigé précisément parce que ça causait des bugs silencieux.

Nuance importante : seule l'expression itérable la plus externe (le premier for ... in <ICI>) est évaluée dans le scope englobant — donc si cette expression lève une erreur, elle a accès aux variables extérieures normalement.

Niveau 2 — for multiples : flatten, pas produit cartésien par erreur

matrice = [[1, 2, 3], [4, 5, 6]]
plat = [n for ligne in matrice for n in ligne]
# [1, 2, 3, 4, 5, 6]

L'ordre des for reflète l'ordre de boucles imbriquées classiques : le premier for est la boucle la plus externe. Erreur fréquente : inverser l'ordre en pensant lire "de droite à gauche" — ça ne marche pas comme ça, c'est littéralement la traduction 1:1 de :

plat = []
for ligne in matrice:
    for n in ligne:
        plat.append(n)

Plusieurs if s'enchaînent aussi en ET logique :
[x for x in range(20) if x % 2 == 0 if x % 3 == 0]
# équivalent à : if x % 2 == 0 and x % 3 == 0

Niveau 3 — Walrus operator (:=) dans une comprehension

Utile quand tu dois filtrer sur le résultat d'un calcul coûteux sans le recalculer :

# Sans walrus — appelle f(x) DEUX fois si la condition passe
resultats = [f(x) for x in data if f(x) is not None]

# Avec walrus — appelle f(x) UNE fois
resultats = [y for x in data if (y := f(x)) is not None]

C'est le cas d'usage principal légitime : éviter un double appel (perf) ou une double évaluation (ee cas, ne force pas le walrus — la lisibilité prime.

Niveau 4/5 — Seuil de lisibilité (le point théorique que tu avais en Q5, maintenant concret)

Règle pratique que suivent la plupart des style guides pro (Google, la tienne à construire) : une cor/if combinés, ou un niveau d'imbrication > 1, devient moins lisible qu'une boucle explicite.

# Illisible — 2 for + 1 if + walrus, à éviter en prod
resultat = [
    (u, v) for u in users if u.active
    for v in u.orders if (total := v.amount) > 100
]

Alternative pro : soit une boucle explicite, soit itertools :

- itertools.chain.from_iterable(...) pour aplatir plusieurs itérables sans comprehension imbriquée.
- itertools.product(...) pour un vrai produit cartésien, plus explicite qu'un double for en comprehension.
- Extraire une fonction nommée (get_big_orders(user)) plutôt qu'empiler la logique dans une seule e

Niveau 5 — Piège de consommation unique (generator expression)

Directement lié à ce qu'on a vu sur les Sets et la paresse : un generator expression s'épuise après

gen = (x for x in range(3))
print(list(gen))  # [0, 1, 2]
print(list(gen))  # [] — épuisé, aucune erreur, juste vide

Contrairement à une list, aucune exception n'est levée — le bug est silencieux. C'est un piège claseering où on pense pouvoir réutiliser une variable "itérable" plusieurs fois.

---

Challenge

Prédis, sans exécuter, ce que fait ce code — et explique la raison technique précise (pas juste "ça

seuils = [10, 20, 30]
resultat = [n for n in range(50) for seuils in [seuils] if n > seuils[-1]]
print(seuils)

Indice pour cadrer ta réponse : combien de fois la variable seuils est-elle définie ici, et dans qu
resultat = [n for n in range(50) for seuils in [seuils] if n > seuils[-1]]                                              ^^^^^^
UnboundLocalError: cannot access local variable 'seuils' where it is not associated with a value

La leçon pro à retenir : ne réutilise jamais, comme variable cible d'un for dans une comprehension, un nom que tu veux encore lire (dans sa version extérieure) à l'intérieur de cette même comprehension. Ici il aurait fallu nommer différemment (seuil_courant par exemple).