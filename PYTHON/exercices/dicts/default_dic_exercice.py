"""Deux points essentiels de la séance précédente, en une ligne chacun :
- defaultdict(type_factory) crée automatiquement une valeur par défaut (ex: list, set, int) dès qu'on accède à une clé absente — plus besoin de if cle not in dict.
- Counter est un dict spécialisé pour compter ; on peut l'incrémenter avec += sur des clés absentes sans erreur, et il fournit .most_common(n).
"""
#Exercice — Analyse des commandes d'une boutique

commandes = [
    {"produit": "stylo", "categorie": "papeterie", "quantite": 3},
    {"produit": "cahier", "categorie": "papeterie", "quantite": 5},
    {"produit": "stylo", "categorie": "papeterie", "quantite": 2},
    {"produit": "clavier", "categorie": "informatique", "quantite": 1},
    {"produit": "souris", "categorie": "informatique", "quantite": 4},
    {"produit": "clavier", "categorie": "informatique", "quantite": 2},
]

"""Écris une fonction analyse_commandes(commandes) qui retourne un tuple de 3 éléments :

1. produits_par_categorie : un dict associant chaque catégorie à l'ensemble (set) des noms de produits distincts vendus dans cette catégorie. → utilise defaultdict(set).
2. quantites_par_produit : un Counter associant chaque nom de produit à la somme totale des quantités vendues pour ce produit (pas le nombre de commandes, la somme des quantite).
3. produit_le_plus_vendu : le produit avec la plus grande quantité totale vendue, sous forme de tuple (nom, quantite). → utilise une méthode de Counter vue la dernière fois, pas une boucle manuelle.

Résultat attendu pour ces données :
(
    {"papeterie": {"stylo", "cahier"}, "informatique": {"clavier", "souris"}},
    Counter({"stylo": 5, "cahier": 5, "clavier": 3, "souris": 4}),
    ("stylo", 5)  # ou ("cahier", 5) — égalité possible, les deux sont acceptés
)
"""
sep = "---" * 50

from collections import defaultdict, Counter


# solition 1
def analyse_commandes(commandes):
    produit_par_category = defaultdict(set)
    quantites_par_produit = Counter()
    for commande in commandes:
        produit_name = commande['produit']
        produit_categorie = commande['categorie']
        produit_quantite = commande['quantite']

        produit_par_category[produit_categorie].add(produit_name)
        quantites_par_produit[produit_name] += produit_quantite
        
    produit_le_plus_vendu = quantites_par_produit.most_common(1)[0]

    return (produit_par_category, quantites_par_produit, produit_le_plus_vendu)

print(analyse_commandes(commandes))
print(sep)
