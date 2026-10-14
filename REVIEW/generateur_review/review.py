 # Voici un générateur censé regrouper les éléments d'un itérable par lots de 3 :

def grouper_par_lot(iterable, lot=[], taille=3):
    for element in iterable:
        lot.append(element)
        if len(lot) == taille:
            yield lot
            lot = []

# test
#print(list(grouper_par_lot([1, 2, 3, 4, 5, 6, 7])))
#print(list(grouper_par_lot(["a", "b"])))

# Trouve tous les problèmes (il y en a au moins deux, de nature différente), explique précisément pourquoi chacun se produit, et corrige. 
# Essaie de prédire ce qu'affichent les deux print() avant de corriger quoi que ce soit — ça t'aidera à repérer les bugs.


"""
Le piège des arguments par défaut mutables

Règle précise de Python : les valeurs par défaut des paramètres sont évaluées une seule fois, au moment où le def est exécuté 
(donc à la définition de la fonction), pas à chaque appel. Cet objet par défaut est stocké une fois pour toutes sur la fonction elle-même, 
et partagé par tous les appels qui n'overrident pas explicitement ce paramètre.

Pour lot=[], ça veut dire qu'il n'existe qu'une seule liste [], créée une fois, que tous les appels sans lot=... explicite vont réutiliser — le même objet, pas une copie fraîche à chaque fois.

Trace précise de ton exemple :

Appel 1 : grouper_par_lot([1,2,3,4,5,6,7]) — lot démarre sur l'objet partagé D (vide).
- D devient [1,2,3] (via .append(), donc mutation en place de D) → yield D (donc [1,2,3]) → puis lot = [] crée un nouvel objet local (ça ne touche plus D, D reste [1,2,3] pour toujours).
- Nouveau lot devient [4,5,6] → yield → lot = [] (encore un nouvel objet).
- Nouveau lot devient [7] (1 seul élément, jamais 3) → boucle finie → jamais yield → perdu (ton bug n°1).

Résultat print(1) : [[1, 2, 3], [4, 5, 6]]. Mais surtout : D (l'objet par défaut de la fonction) contient maintenant [1, 2, 3] pour toujours, tant que la fonction existe — pas vide.

Appel 2 : grouper_par_lot(["a", "b"]) — pas de lot= explicite → réutilise le même D, qui vaut déjà [1, 2, 3] (pollué par le premier appel, sans rapport avec ce deuxième appel !).
- D devient [1,2,3,"a"] (len 4, jamais exactement 3 ue tu pensais (pas "trop court"), c'est en fait la contamination du premier appel qui empêche la comparaison == taille de tomber juste. Le symptôme visible ([]) masque complètement la vraie cause — c'est le genre de bug le plus dangereux : silencieusement faux, sans erreur, sans warning.
"""

# Correction:
# laisse lot elnve des parametres
def grouper_par_lot(iterable, taille=3):
    lot = []
    for element in iterable:
        lot.append(element)
        if len(lot) == taille:
            yield lot
            lot = []
    if lot:
        yield lot
# test
print(list(grouper_par_lot([1, 2, 3, 4, 5, 6, 7])))
print(list(grouper_par_lot(["a", "b"])))
# output: [[1, 2, 3], [4, 5, 6], [7]] [['a', 'b']]

"""
### Aides-Mémoires Rapides

| Problème | Symptôme / Danger | Bonne Pratique |
| :--- | :--- | :--- |
| **`def func(a=[])`** | Contamination silencieuse des données d'un appel à l'autre. | `def func(a=None):` puis `a = a if a is not None else []` |
| **`lot = []` après `yield lot`** | Ne nettoie pas l'objet initial, crée juste une variable locale différente. | Initialiser proprement par appel. |
| **Reste dans les générateurs** | Perte silencieuse des derniers éléments de l'itération. | Ajouter `if lot: yield lot` après la boucle. |
"""