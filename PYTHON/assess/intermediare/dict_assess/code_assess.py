# Reponse Q-1
"""
a- un dictionnaire en python est une structure qui organise les donnnees sour forme de cle-valeur.
b- un dictionnaire est different d'une liste dans"
    * le mesure ou il est plus facile de retrouver la valeur d'un element du dictionnaire via sa cle que son indice comme on le ferait avec une liste.
    * eviter le declenchement d'une erreur suite a la tenetative de retrouver une valeur qui n'existe pas dans le dictionnaire grace a sa methode get()
      qui renverait une valeur par defaut ou un message.
c- on peut creer un dictionnaire par:
    * la methode directe: dict_name = {cl_1: val_1, cle_2: val_2, ...cle_n: val_n}
    * ou utiliser le mot cle dict: dict_name = dict(cle_x=val_x, cle_y=val_y)
"""
sep = "---" * 50
print(sep)
# Reponse Q-2
# a- afficher la valeur de age:
eleve = {"nom": "Awa", "age": 21, "ville": "Dakar"}
valeur_age = eleve.get("age", 0)
print(f"la valeur de age avec la methode get(): {valeur_age}")
print(f"Amelioration avec la methode pop: {eleve.pop("age", None)}")
print(sep)

# b- ajout d'une nouvelle cle filiere:
eleve["filiere"] = "Info"
print(f'eleve mis ajour apres ajoute de la cle "filiere": {eleve}')
print(sep)

# c- suppresions de la cle ville:
if "ville" in eleve:
    del eleve["ville"]

print(f'eleve mis ajour apres suppression de la cle "Ville" avec la methode del: "ville": {eleve}')
print(sep)


# Reponse Q-3 parcours du dict:
"""
> J'utiliserais une boucle pour parcourir toutes les cles et ainsi afficherais une paire cle, valeur par ligne comme suite:
```python
for cle in eleve:
    print(cle, eleve[cle])
```
NB je pourrais utiliser aussi la methode enumerate() mais dans ce cas j'aurais des indices et valeur a la place des cle et valeur

"""
print("Affichage du dic: parcours avec for simple")
for cle in eleve:
    print(cle, eleve[cle])

print("Affichage du dict: parcours avec for enumerate cle, val")
for cle, val in enumerate(eleve):
    print(cle, val)
print(sep)

# ====================== amelioration ==================
# ameliorations avec la methode idiomatique .items()
print("Affichage du dict: ameliorations avec la methode idiomatique .items()")
for cle, val in eleve.items():
    print(cle, val)
print(sep)

"""
Question 5 (application/design)
Tu dois compter le nombre d'occurrences de chaque mot dans une liste de mots :"""
mots = ["chat", "chien", "chat", "oiseau", "chien", "chat"]
dict_occ = {}
for mot in mots:
    if mot in dict_occ:
        dict_occ[mot] += 1
    else:
        dict_occ[mot] = 1
        
print(f"Occurence des mots: {dict_occ}")
print(sep)

# Reponse Q-4:
"""
Reponse a la question 3:
> eleve["telephone"] delencherait une erreur key error indiquant que la cle "telephone n'existe pas"
> pour eviter cette erreur on pourrait utiliser la methode get avec une valeur ou message par defaut si la cle n'existe pas comme suite:
    eleve.get("telephone", "la cle telephone n'existe pas")
    on pourrait aussi utiliser le bloc try-except pour capturer l'erreur.
"""

# Reponse Q-5:
"""
> j'initialise d'abord un dictionnaire vide en dehor de la boucle
> puis je parcours la liste et je verifie pour chaque mot de la liste:
    > si le mot est absent du dictionnaire alors j'ajoute une nouvelle paire cle-valeur ou cle: le mot et valeur: son occurence
    > sinon j'incremente la valeur de l'occurence du mot en question dans le dictionnaire.

"""
# ==================== solution amelioree  de la question 5 ====================
from collections import defaultdict, Counter


# Version defaultdict — remplace le if/else
compteur_1 = defaultdict(int) # int()renvoie 0 par defaut
for mot in mots:
    compteur_1[mot] += 1

print(f"Occurence des mots avec defaultdict: {compteur_1}")
print(sep)

# avec Counter remplace toute la boucle
compteur_2 = Counter(mots)
print(f"Occurence des mots avec Counter: {compteur_2}")
print(f"Occurence du mot la plus elevee: {compteur_2.most_common(1)}")
print(sep)

# ========================== differences entre set_default_dict & defaultdict ==========
from collections import defaultdict
from timeit import timeit

animals = [('cat', 1), ('rabbit', 2), ('cat', 3), ('dog', 4), ('dog', 1)]
std_dict = dict()
def_dict = defaultdict(list)

# setdefaultdict
def group_with_dict():
    for animal, count in animals:
        std_dict.setdefault(animal, []).append(count)
    return std_dict

# defaultdict
def group_with_defaultdict():
    for animal, count in animals:
        def_dict[animal].append(count)
    return def_dict

print(f'dict.setdefault() takes {timeit(group_with_dict)} seconds.') # dict.setdefault() takes 1.0281260240008123 seconds.
print(f'defaultdict takes {timeit(group_with_defaultdict)} seconds.') # defaultdict takes 0.6704721650003194 seconds.

