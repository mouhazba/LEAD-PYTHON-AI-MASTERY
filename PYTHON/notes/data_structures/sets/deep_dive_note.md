Sets — approfondissement technique (Engineering / Advanced)



Niveau 2 — Sémantique réelle : comment un set est implémenté



Un set CPython est une table de hachage à adressage ouvert (open addressing), pas une table à chaînage comme dans d'autres langages. Concrètement :



- Chaque élément est placé dans un tableau interne à un index dérivé de hash(element) % taille_table.

- En cas de collision (deux éléments avec le même index), CPython sonde d'autres emplacements (probing) selon une séquence pseudo-aléatoire dérivée du hash.

- Quand le taux de remplissage dépasse ~2/3, la table est redimensionnée (resize) — c'est pour ça qu'ajouter des éléments un par un peut ponctuellement coûter plus cher qu'O(1) (le resize est O(n), mais amorti sur l'ensemble des insertions ça reste O(1) amorti).



Conséquence directe sur la complexité : O(1) moyen suppose une bonne distribution des hash. Si beaucoup d'éléments collisionnent (mauvaise fonction de hash, ou attaque volontaire — hash flooding), tu dégrades vers O(n). CPython mitige ça avec PYTHONHASHSEED randomisé par défaut pour les str/bytes, précisément pour empêcher un attaquant de forcer des collisions dans un service qui construit des sets/dicts à partir d'input utilisateur.



Niveau 2 — Le contrat __hash__/__eq__ (piège classique avec des objets custom)



class Utilisateur:

    def __init__(self, id_):

        self.id_ = id_



    def __eq__(self, other):

        return self.id_ == other.id_



s = {Utilisateur(1)}



Ça lève TypeError: unhashable type: 'Utilisateur'. Pourquoi, alors que tu n'as pas touché à __hash__ ?



Règle Python : dès que tu définis __eq__ sur une classe, Python met automatiquement __hash__ à None — parce que l'égalité par défaut (identité) et le hash par défaut (basé sur id()) ne seraient plus cohérents avec ta nouvelle notion d'égalité. Le contrat implicite : si a == b, alors hash(a) == hash(b). Si tu redéfinis l'un, tu dois redéfinir l'autre toi-même :



class Utilisateur:

    def __init__(self, id_):

        self.id_ = id_



    def __eq__(self, other):

        return self.id_ == other.id_



    def __hash__(self):

        return hash(self.id_)



C'est un des pièges les plus fréquents chez des devs intermédiaires — ils veulent mettre des objets métier dans un set/comme clé de dict, et ça casse silencieusement dès qu'ils ajoutent __eq__.



Niveau 3 — Pièges idiomatiques



- {} ne crée PAS un set vide — ça crée un dict vide. Pour un set vide : set().

- Ne jamais muter un set pendant qu'on itère dessus (RuntimeError: Set changed size during iteration) — comme pour dict/list, itère sur une copie (for x in set(s):) si tu dois modifier s pendant la boucle.

- set en argument par défaut mutable — même piège que def f(x=[]): : def f(x=set()): partage l'objeise None + création interne.



Niveau 4 — Quand NE PAS utiliser un set (c'est le point que tu n'as pas encore, d'après ton diagnos
### Niveau 4 — Quand NE PAS utiliser un set

| Besoin | Bon choix | Pourquoi pas `set` ? |
| :--- | :--- | :--- |
| **Garder l'ordre d'insertion** | `list`, ou `dict.fromkeys()` pour dédupliquer en gardant l'ordre | `set` n'offre aucune garantie d'ordre |
| **Compter des occurrences** | `Counter` | `set` écrase les doublons, tu perds l'info de fréquence |
| **Indexation / Slicing** (`s[0]`, `s[1:3]`) | `list`, `tuple` | Pas d'ordre = pas d'indexation |
| **Éléments non hashables** (dicts, lists imbriquées) | `list` de `dict` | `set` refuse les éléments mutables |
| **Petite collection** (< 5 éléments), lisibilité prime sur perf | `list` ou `tuple` | Le gain $\mathcal{O}(1)$ ne compense pas la lisibilité pour un tout petit volume |
| **Retour public d'API immuable** | `frozenset` | Un `set` mutable exposé publiquement peut être modifié par l'appelant (aliasing) |

Challenge (tu es 🟢, donc on monte d'un cran)



Prédis ce que fait ce code, sans l'exécuter, et explique pourquoi :



def dedupliquer_en_gardant_ordre(items):

    vu = set()

    resultat = []

    for item in items:

        if item not in vu:

            vu.add(item)

            resultat.append(item)

    return resultat



print(dedupliquer_en_gardant_ordre([3, 1, 2, 3, 1, 4]))



Puis, question de conception : cette fonction utilise à la fois un set et une list. Pourquoi ne pas se contenter d'un seul set (set(items)), et pourquoi ne pas se contenter d'un seul dict.fromkeys(items) ? Compare les trois approches (complexité, ordre, lisibilité

Problème
L'exécution de ce code lève une erreur : TypeError: unhashable type: 'Utilisateur'.
Pourquoi, alors que __hash__ n'a pas été explicitement modifié ?

Explication & Règle Python
Dès que vous définissez __eq__ sur une classe, Python règle automatiquement __hash__ à None. En effet, l'égalité par défaut (basée sur l'identité de l'objet) et le hash par défaut (basé sur id()) ne seraient plus cohérents avec votre nouvelle notion d'égalité.

Le contrat implicite :

Si a==b⟹hash(a)==hash(b)
Si vous redéfinissez la notion d'égalité (__eq__), vous devez impérativement redéfinir la fonction de hachage (__hash__) :

Python
class Utilisateur:
    def __init__(self, id_):
        self.id_ = id_

    def __eq__(self, other):
        if not isinstance(other, Utilisateur):
            return NotImplemented
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)
⚠️ Piège classique : C'est une erreur fréquente chez les développeurs intermédiaires lorsqu'ils souhaitent stocker des objets métier dans un set ou les utiliser comme clés de dict. Le code casse dès que __eq__ est implémenté sans __hash__.

Niveau 3 — Pièges idiomatiques
Raccourci {} vs set() :

{} ne crée PAS un set vide — cela crée un dict vide.

Pour instancier un set vide, utilisez impérativement set().

Mutation pendant l'itération :

Il ne faut jamais modifier un set pendant qu'on le parcourt, sous peine de lever : RuntimeError: Set changed size during iteration.

Solution : Itérer sur une copie du set :

Python
for x in set(s):
    if condition(x):
        s.remove(x)
Argument par défaut mutable :

Utiliser un set comme valeur par défaut dans une signature de fonction pose le même problème qu'une liste mutable :

Python
# ❌ À éviter : le set est partagé entre tous les appels
def ajouter_element(elem, conteneur=set()):
    conteneur.add(elem)
    return conteneur
Bonne pratique : Utiliser None et initialiser le set à l'intérieur de la fonction :

Python
# ✅ Idiomatique
def ajouter_element(elem, conteneur=None):
    if conteneur is None:
        conteneur = set()
    conteneur.add(elem)
    return conteneur
Niveau 4 — Quand NE PAS utiliser un set
Besoin	Bon choix	Pourquoi pas set ?
Garder l'ordre d'insertion	list, ou dict.fromkeys() pour dédupliquer en conservant l'ordre	Un set n'assure aucune garantie d'ordre.
Compter des occurrences	collections.Counter	Un set supprime les doublons, ce qui entraîne la perte de la fréquence d'apparition.
Indexation / Slicing (s[0], s[1:3])	list, tuple	Pas de notion d'ordre = pas d'indexation possible.
Éléments non hashables (ex: dict, list imbriquées)	list de dict	Un set refuse les éléments mutables (non hashables).
Petite collection (< 5 éléments) (lisibilité > perf)	list, tuple	Le gain algorithmique en O(1) ne compense pas le surcoût de lisibilité sur un volume minuscule.
Retour public d'API immuable	frozenset	Un set mutable exposé publiquement peut être altéré par l'appelant (aliasing).
Challenge Technique 🟢
Code à analyser
Python
def dedupliquer_en_gardant_ordre(items):
    vu = set()
    resultat = []
    for item in items:
        if item not in vu:
            vu.add(item)
            resultat.append(item)
    return resultat

print(dedupliquer_en_gardant_ordre([3, 1, 2, 3, 1, 4]))
1. Prédiction & Résultat
Résultat affiché :

Python
[3, 1, 2, 4]
Explication :
La fonction parcourt la liste items dans l'ordre original :

3 : non présent dans vu → ajouté à vu et resultat.

1 : non présent dans vu → ajouté à vu et resultat.

2 : non présent dans vu → ajouté à vu et resultat.

3 : déjà présent dans vu → ignoré.

1 : déjà présent dans vu → ignoré.

4 : non présent dans vu → ajouté à vu et resultat.

2. Conception : Comparaison des 3 approches
Approche A : set(items)
Python
resultat = list(set(items))
Complexité : O(n) temporel, O(n) spatial.

Ordre : ❌ L'ordre original des éléments est perdu.

Lisibilité : Très concise, mais inadéquate si la préservation de l'ordre est requise.

Approche B : dict.fromkeys(items)
Python
resultat = list(dict.fromkeys(items))
Complexité : O(n) temporel, O(n) spatial.

Ordre : ✅ Conserve l'ordre d'insertion (depuis Python 3.7+ où l'ordre des dict est garanti par la spécification du langage).

Lisibilité : Idiomatique et extrêmement rapide en CPython (optimisé en C sous le capot).

Approche C : La fonction hybride (set + list)
Python
def dedupliquer_en_gardant_ordre(items):
    vu = set()
    resultat = []
    for item in items:
        if item not in vu:
            vu.add(item)
            resultat.append(item)
    return resultat
Complexité : O(n) temporel (O(1) moyen pour item not in vu), O(n) spatial.

Ordre : ✅ Conserve l'ordre d'insertion explicitement via la structure list.

Comparatif / Analyse :

Pourquoi pas une liste seule ? Tester item not in resultat sur une liste coûte O(n), rendant l'algorithme global en O(n 
2
 ). L'utilisation conjointe du set permet de faire le test de présence en O(1).

Vs dict.fromkeys() : dict.fromkeys() est généralement plus court et implémenté directement en C. Cependant, la fonction explicite est plus explicite sur l'intention pour des développeurs venant d'autres langages et permet une adaptation facile (par exemple en ajoutant une clé de projection key=lambda x: ...).
"""

with open("sets_approfondissement_technique.md", "w", encoding="utf-8") as f:
f.write(content)

print("FILE_GENERATED_SUCCESSFULLY")


```text?code_stdout&code_event_index=1
FILE_GENERATED_SUCCESSFULLY

Voici le document .md nettoyé et structuré.

Icône MD
sets_approfondissement_technique
 MD 
Ouvert
Sets — Approfondissement Technique (Engineering / Advanced)
Niveau 2 — Sémantique réelle : comment un set est implémenté
Un set CPython est une table de hachage à adressage ouvert (open addressing), et non une table à chaînage (chaining) comme dans d'autres langages.

Concrètement :

Indexation : Chaque élément est placé dans un tableau interne à un index dérivé de hash(element) % taille_table.

Gestion des collisions : En cas de collision (deux éléments produisant le même index), CPython sonde d'autres emplacements (probing) selon une séquence pseudo-aléatoire dérivée du hash.

Redimensionnement (Resize) : Quand le taux de remplissage dépasse ~2/3, la table est redimensionnée.

C'est pour cela qu'ajouter des éléments un par un peut ponctuellement coûter plus cher qu'O(1) (le resize est O(n)).

Néanmoins, amorti sur l'ensemble des insertions, la complexité reste O(1) amorti.

Conséquence directe sur la complexité :
L'efficacité O(1) moyen suppose une bonne distribution des hash. Si beaucoup d'éléments entrent en collision (mauvaise fonction de hash, ou attaque par hash flooding), les performances se dégradent vers O(n).

CPython mitige cela grâce à la variable PYTHONHASHSEED randomisée par défaut pour les str et bytes, empêchant ainsi un attaquant de forcer des collisions dans un service construisant des set ou dict à partir d'entrées utilisateurs.

Niveau 2 — Le contrat __hash__ / __eq__ (Piège classique)
Considérons la classe suivante :

Python
class Utilisateur:
    def __init__(self, id_):
        self.id_ = id_

    def __eq__(self, other):
        return self.id_ == other.id_

s = {Utilisateur(1)}
Problème
L'exécution de ce code lève une erreur : TypeError: unhashable type: 'Utilisateur'.
Pourquoi, alors que __hash__ n'a pas été explicitement modifié ?

Explication & Règle Python
Dès que vous définissez __eq__ sur une classe, Python règle automatiquement __hash__ à None. En effet, l'égalité par défaut (basée sur l'identité de l'objet) et le hash par défaut (basé sur id()) ne seraient plus cohérents avec votre nouvelle notion d'égalité.

Le contrat implicite :

Si a==b⟹hash(a)==hash(b)
Si vous redéfinissez la notion d'égalité (__eq__), vous devez impérativement redéfinir la fonction de hachage (__hash__) :

Python
class Utilisateur:
    def __init__(self, id_):
        self.id_ = id_

    def __eq__(self, other):
        if not isinstance(other, Utilisateur):
            return NotImplemented
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)
⚠️ Piège classique : C'est une erreur fréquente chez les développeurs intermédiaires lorsqu'ils souhaitent stocker des objets métier dans un set ou les utiliser comme clés de dict. Le code casse dès que __eq__ est implémenté sans __hash__.

Niveau 3 — Pièges idiomatiques
Raccourci {} vs set() :

{} ne crée PAS un set vide — cela crée un dict vide.

Pour instancier un set vide, utilisez impérativement set().

Mutation pendant l'itération :

Il ne faut jamais modifier un set pendant qu'on le parcourt, sous peine de lever : RuntimeError: Set changed size during iteration.

Solution : Itérer sur une copie du set :

Python
for x in set(s):
    if condition(x):
        s.remove(x)
Argument par défaut mutable :

Utiliser un set comme valeur par défaut dans une signature de fonction pose le même problème qu'une liste mutable :

Python
# ❌ À éviter : le set est partagé entre tous les appels
def ajouter_element(elem, conteneur=set()):
    conteneur.add(elem)
    return conteneur
Bonne pratique : Utiliser None et initialiser le set à l'intérieur de la fonction :

Python
# ✅ Idiomatique
def ajouter_element(elem, conteneur=None):
    if conteneur is None:
        conteneur = set()
    conteneur.add(elem)
    return conteneur
Niveau 4 — Quand NE PAS utiliser un set
Besoin	Bon choix	Pourquoi pas set ?
Garder l'ordre d'insertion	list, ou dict.fromkeys() pour dédupliquer en conservant l'ordre	Un set n'assure aucune garantie d'ordre.
Compter des occurrences	collections.Counter	Un set supprime les doublons, ce qui entraîne la perte de la fréquence d'apparition.
Indexation / Slicing (s[0], s[1:3])	list, tuple	Pas de notion d'ordre = pas d'indexation possible.
Éléments non hashables (ex: dict, list imbriquées)	list de dict	Un set refuse les éléments mutables (non hashables).
Petite collection (< 5 éléments) (lisibilité > perf)	list, tuple	Le gain algorithmique en O(1) ne compense pas le surcoût de lisibilité sur un volume minuscule.
Retour public d'API immuable	frozenset	Un set mutable exposé publiquement peut être altéré par l'appelant (aliasing).
Challenge Technique 🟢
Code à analyser
Python
def dedupliquer_en_gardant_ordre(items):
    vu = set()
    resultat = []
    for item in items:
        if item not in vu:
            vu.add(item)
            resultat.append(item)
    return resultat

print(dedupliquer_en_gardant_ordre([3, 1, 2, 3, 1, 4]))
1. Prédiction & Résultat
Résultat affiché :

Python
[3, 1, 2, 4]
Explication :
La fonction parcourt la liste items dans l'ordre original :

3 : non présent dans vu → ajouté à vu et resultat.

1 : non présent dans vu → ajouté à vu et resultat.

2 : non présent dans vu → ajouté à vu et resultat.

3 : déjà présent dans vu → ignoré.

1 : déjà présent dans vu → ignoré.

4 : non présent dans vu → ajouté à vu et resultat.

2. Conception : Comparaison des 3 approches
Approche A : set(items)
Python
resultat = list(set(items))
Complexité : O(n) temporel, O(n) spatial.

Ordre : ❌ L'ordre original des éléments est perdu.

Lisibilité : Très concise, mais inadéquate si la préservation de l'ordre est requise.

Approche B : dict.fromkeys(items)
Python
resultat = list(dict.fromkeys(items))
Complexité : O(n) temporel, O(n) spatial.

Ordre : ✅ Conserve l'ordre d'insertion (depuis Python 3.7+ où l'ordre des dict est garanti par la spécification du langage).

Lisibilité : Idiomatique et extrêmement rapide en CPython (optimisé en C sous le capot).

Approche C : La fonction hybride (set + list)
Python
def dedupliquer_en_gardant_ordre(items):
    vu = set()
    resultat = []
    for item in items:
        if item not in vu:
            vu.add(item)
            resultat.append(item)
    return resultat
Complexité : O(n) temporel (O(1) moyen pour item not in vu), O(n) spatial.

Ordre : ✅ Conserve l'ordre d'insertion explicitement via la structure list.

Comparatif / Analyse :

Pourquoi pas une liste seule ? Tester item not in resultat sur une liste coûte O(n), rendant l'algorithme global en O(n 
2
 ). L'utilisation conjointe du set permet de faire le test de présence en O(1).

Vs dict.fromkeys() : dict.fromkeys() est généralement plus court et implémenté directement en C. Cependant, la fonction explicite est plus lisible/intuitive et s'adapte facilement (par exemple en ajoutant une fonction clé de transformation/filtrage key=lambda x: ...).




Gemini est une IA et peut se tromper.

Analyse…
# Sets — Approfondissement Technique (Engineering / Advanced)

## Niveau 2 — Sémantique réelle : comment un set est implémenté

Un `set` CPython est une **table de hachage à adressage ouvert** (*open addressing*), et non une table à chaînage (*chaining*) comme dans d'autres langages.

Concrètement :
- **Indexation :** Chaque élément est placé dans un tableau interne à un index dérivé de `hash(element) % taille_table`.
- **Gestion des collisions :** En cas de collision (deux éléments produisant le même index), CPython sonde d'autres emplacements (*probing*) selon une séquence pseudo-aléatoire dérivée du hash.
- **Redimensionnement (Resize) :** Quand le taux de remplissage dépasse **~2/3**, la table est redimensionnée.
  - C'est pour cela qu'ajouter des éléments un par un peut ponctuellement coûter plus cher qu'$\mathcal{O}(1)$ (le resize est $\mathcal{O}(n)$).
  - Néanmoins, amorti sur l'ensemble des insertions, la complexité reste **$\mathcal{O}(1)$ amorti**.

> **Conséquence directe sur la complexité :**
> L'efficacité $\mathcal{O}(1)$ moyen suppose une bonne distribution des hash. Si beaucoup d'éléments entrent en collision (mauvaise fonction de hash, ou attaque par *hash flooding*), les performances se dégradent vers **$\mathcal{O}(n)$**.
> 
> CPython mitige cela grâce à la variable `PYTHONHASHSEED` randomisée par défaut pour les `str` et `bytes`, empêchant ainsi un attaquant de forcer des collisions dans un service construisant des `set` ou `dict` à partir d'entrées utilisateurs.

---

## Niveau 2 — Le contrat `__hash__` / `__eq__` (Piège classique)

Considérons la classe suivante :

```python
class Utilisateur:
    def __init__(self, id_):
        self.id_ = id_

    def __eq__(self, other):
        return self.id_ == other.id_

s = {Utilisateur(1)}
```

### Problème
L'exécution de ce code lève une erreur : `TypeError: unhashable type: 'Utilisateur'`. 
*Pourquoi, alors que `__hash__` n'a pas été explicitement modifié ?*

### Explication & Règle Python
Dès que vous définissez `__eq__` sur une classe, Python règle automatiquement `__hash__` à `None`. En effet, l'égalité par défaut (basée sur l'identité de l'objet) et le hash par défaut (basé sur `id()`) ne seraient plus cohérents avec votre nouvelle notion d'égalité.

**Le contrat implicite :**
$$	ext{Si } a == b \implies 	ext{hash}(a) == 	ext{hash}(b)$$

Si vous redéfinissez la notion d'égalité (`__eq__`), vous devez impérativement redéfinir la fonction de hachage (`__hash__`) :

```python
class Utilisateur:
    def __init__(self, id_):
        self.id_ = id_

    def __eq__(self, other):
        if not isinstance(other, Utilisateur):
            return NotImplemented
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)
```

> ⚠️ **Piège classique :** C'est une erreur fréquente chez les développeurs intermédiaires lorsqu'ils souhaitent stocker des objets métier dans un `set` ou les utiliser comme clés de `dict`. Le code casse dès que `__eq__` est implémenté sans `__hash__`.

---

## Niveau 3 — Pièges idiomatiques

1. **Raccourci `{}` vs `set()` :**
   - `{}` ne crée **PAS** un set vide — cela crée un `dict` vide.
   - Pour instancier un `set` vide, utilisez impérativement `set()`.

2. **Mutation pendant l'itération :**
   - Il ne faut jamais modifier un `set` pendant qu'on le parcourt, sous peine de lever : `RuntimeError: Set changed size during iteration`.
   - **Solution :** Itérer sur une copie du set :
     ```python
     for x in set(s):
         if condition(x):
             s.remove(x)
     ```

3. **Argument par défaut mutable :**
   - Utiliser un `set` comme valeur par défaut dans une signature de fonction pose le même problème qu'une liste mutable :
     ```python
     # ❌ À éviter : le set est partagé entre tous les appels
     def ajouter_element(elem, conteneur=set()):
         conteneur.add(elem)
         return conteneur
     ```
   - **Bonne pratique :** Utiliser `None` et initialiser le `set` à l'intérieur de la fonction :
     ```python
     # ✅ Idiomatique
     def ajouter_element(elem, conteneur=None):
         if conteneur is None:
             conteneur = set()
         conteneur.add(elem)
         return conteneur
     ```

---

## Niveau 4 — Quand NE PAS utiliser un `set`

| Besoin | Bon choix | Pourquoi pas `set` ? |
| :--- | :--- | :--- |
| **Garder l'ordre d'insertion** | `list`, ou `dict.fromkeys()` pour dédupliquer en conservant l'ordre | Un `set` n'assure aucune garantie d'ordre. |
| **Compter des occurrences** | `collections.Counter` | Un `set` supprime les doublons, ce qui entraîne la perte de la fréquence d'apparition. |
| **Indexation / Slicing** (`s[0]`, `s[1:3]`) | `list`, `tuple` | Pas de notion d'ordre = pas d'indexation possible. |
| **Éléments non hashables** (ex: `dict`, `list` imbriquées) | `list` de `dict` | Un `set` refuse les éléments mutables (non hashables). |
| **Petite collection (< 5 éléments)** *(lisibilité > perf)* | `list`, `tuple` | Le gain algorithmique en $\mathcal{O}(1)$ ne compense pas le surcoût de lisibilité sur un volume minuscule. |
| **Retour public d'API immuable** | `frozenset` | Un `set` mutable exposé publiquement peut être altéré par l'appelant (*aliasing*). |

---

## Challenge Technique 🟢

### Code à analyser

```python
def dedupliquer_en_gardant_ordre(items):
    vu = set()
    resultat = []
    for item in items:
        if item not in vu:
            vu.add(item)
            resultat.append(item)
    return resultat

print(dedupliquer_en_gardant_ordre([3, 1, 2, 3, 1, 4]))
```

### 1. Prédiction & Résultat
**Résultat affiché :**
```python
[3, 1, 2, 4]
```

**Explication :**
La fonction parcourt la liste `items` dans l'ordre original :
1. `3` : non présent dans `vu` $
ightarrow$ ajouté à `vu` et `resultat`.
2. `1` : non présent dans `vu` $
ightarrow$ ajouté à `vu` et `resultat`.
3. `2` : non présent dans `vu` $
ightarrow$ ajouté à `vu` et `resultat`.
4. `3` : déjà présent dans `vu` $
ightarrow$ ignoré.
5. `1` : déjà présent dans `vu` $
ightarrow$ ignoré.
6. `4` : non présent dans `vu` $
ightarrow$ ajouté à `vu` et `resultat`.

---

### 2. Conception : Comparaison des 3 approches

#### Approche A : `set(items)`
```python
resultat = list(set(items))
```
* **Complexité :** $\mathcal{O}(n)$ temporel, $\mathcal{O}(n)$ spatial.
* **Ordre :** ❌ L'ordre original des éléments est perdu.
* **Lisibilité :** Très concise, mais inadéquate si la préservation de l'ordre est requise.

#### Approche B : `dict.fromkeys(items)`
```python
resultat = list(dict.fromkeys(items))
```
* **Complexité :** $\mathcal{O}(n)$ temporel, $\mathcal{O}(n)$ spatial.
* **Ordre :** ✅ Conserve l'ordre d'insertion (depuis Python 3.7+ où l'ordre des `dict` est garanti par la spécification du langage).
* **Lisibilité :** Idiomatique et extrêmement rapide en CPython (optimisé en C sous le capot).

#### Approche C : La fonction hybride (`set` + `list`)
```python
def dedupliquer_en_gardant_ordre(items):
    vu = set()
    resultat = []
    for item in items:
        if item not in vu:
            vu.add(item)
            resultat.append(item)
    return resultat
```
* **Complexité :** $\mathcal{O}(n)$ temporel ($\mathcal{O}(1)$ moyen pour `item not in vu`), $\mathcal{O}(n)$ spatial.
* **Ordre :** ✅ Conserve l'ordre d'insertion explicitement via la structure `list`.
* **Comparatif / Analyse :**
  - **Pourquoi pas une liste seule ?** Tester `item not in resultat` sur une liste coûte $\mathcal{O}(n)$, rendant l'algorithme global en $\mathcal{O}(n^2)$. L'utilisation conjointe du `set` permet de faire le test de présence en $\mathcal{O}(1)$.
  - **Vs `dict.fromkeys()` :** `dict.fromkeys()` est généralement plus court et implémenté directement en C. Cependant, la fonction explicite est plus explicite sur l'intention pour des développeurs venant d'autres langages et permet une adaptation facile (par exemple en ajoutant une clé de projection `key=lambda x: ...`).
sets_approfondissement_technique.md
Affichage de sets_approfondissement_technique.md.