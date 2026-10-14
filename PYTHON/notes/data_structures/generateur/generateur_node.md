# Générateurs infinis et cas où préférer une liste

## Pourquoi utiliser un générateur infini ?

Dans beaucoup de cas réels, **on ne connaît pas la limite à l'avance**. Et surtout, ce n'est pas nécessairement au producteur de données de décider combien de valeurs seront produites : **c'est le consommateur qui peut décider quand il en a assez**.

### Exemples

* Lire des données arrivant en continu :

  * capteur
  * flux réseau
  * file de messages
* Générer des nombres premiers un par un.
* Générer une séquence mathématique comme **Fibonacci**, où la quantité de valeurs nécessaires dépend entièrement de l'utilisation.

Écrire :

```python
range(1_000_000_000)
```

suppose une borne choisie à l'avance.

Cette borne peut être :

* **trop petite** → risque de ne pas avoir assez de données ;
* **trop grande** → travail ou mémoire potentiellement inutile.

Un générateur infini permet donc de séparer deux responsabilités :

> **Le générateur décide comment produire la prochaine valeur.**
> **Le consommateur décide combien de valeurs il veut.**

---

## Comment limiter un générateur sans le modifier ?

On peut utiliser :

```python
itertools.islice(iterable, n)
```

`islice()` peut prendre n'importe quel **itérable**, y compris un générateur infini, et ne récupérer que les `n` premiers éléments.

### Exemple

```python
import itertools

def compteur_infini(debut=0):
    n = debut

    while True:
        yield n
        n += 1

for x in itertools.islice(compteur_infini(), 5):
    print(x)
```

Résultat :

```text
0
1
2
3
4
```

Le générateur lui-même reste infini. On ne modifie pas son fonctionnement.

C'est `islice()` qui impose la limite.

### Principe important : séparation des responsabilités

```text
Générateur
    ↓
Produit la prochaine valeur
    ↓
islice()
    ↓
Décide combien de valeurs récupérer
    ↓
Consommateur
```

Le générateur ne sait donc pas et ne décide pas **"combien de valeurs faut-il ?"**.

C'est le consommateur qui prend cette décision, par exemple avec :

* `itertools.islice()`
* un `break` manuel dans une boucle

---

# Quand NE PAS utiliser un générateur ?

Les générateurs sont particulièrement utiles lorsque l'on veut :

* économiser la mémoire ;
* produire les données progressivement ;
* travailler avec des données potentiellement très grandes ou infinies ;
* ne produire que les valeurs réellement nécessaires.

Mais un générateur n'est pas toujours le meilleur choix.

Une **liste** peut être préférable lorsqu'on a besoin de conserver toutes les données en mémoire et de les manipuler plusieurs fois.

### Cas où une liste est préférable

#### 1. On doit itérer plusieurs fois

Un générateur est généralement **épuisé après un passage**.

```python
gen = (x for x in range(5))

list(gen)  # [0, 1, 2, 3, 4]
list(gen)  # []
```

Une liste, elle, peut être parcourue plusieurs fois :

```python
data = [0, 1, 2, 3, 4]

for x in data:
    print(x)

for x in data:
    print(x)
```

---

#### 2. On a besoin d'accéder aux éléments par index

Une liste permet :

```python
data[0]
data[3]
data[-1]
```

Un générateur ne permet pas un accès direct par index.

---

#### 3. On a besoin de `len()`

Avec une liste :

```python
data = [10, 20, 30]

len(data)
```

Avec un générateur :

```python
gen = (x for x in range(3))

len(gen)  # TypeError
```

Un générateur ne connaît pas nécessairement à l'avance le nombre total d'éléments qu'il produira.

---

#### 4. On doit trier les données

Le tri nécessite de disposer des éléments à trier.

```python
data = [5, 2, 8, 1, 3]

data.sort()
```

ou :

```python
sorted(data)
```

Dans ce cas, il faut de toute façon **récupérer les données en mémoire** pour effectuer le tri.

Il y a donc moins d'intérêt à conserver une approche paresseuse avec un générateur si l'objectif final est de tout avoir en mémoire pour trier.

---

# À retenir

| Générateur                                        | Liste                                          |
| ------------------------------------------------- | ---------------------------------------------- |
| Évaluation paresseuse                             | Toutes les valeurs sont déjà créées            |
| Économise généralement la mémoire                 | Occupe davantage de mémoire                    |
| Idéal pour les grands flux de données             | Idéal pour les données que l'on doit conserver |
| Peut être infini                                  | Généralement de taille finie                   |
| Parcours généralement une seule fois              | Peut être parcourue plusieurs fois             |
| Pas d'accès direct par index                      | Accès par index                                |
| Pas de `len()` direct                             | `len()` disponible                             |
| Très adapté aux données produites progressivement | Adaptée au tri et aux manipulations répétées   |

> **Idée clé :** utiliser un générateur lorsque l'on veut **produire les données au fur et à mesure**, et une liste lorsque l'on a besoin de **posséder et manipuler l'ensemble des données**.
