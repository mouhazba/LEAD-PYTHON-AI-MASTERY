# Exercice (niveau problem-solving/design)
from collections import Counter, defaultdict
transactions = [
    {"user": "alice", "amount": 120},
    {"user": "bob", "amount": -40},
    {"user": "alice", "amount": 30},
    {"user": "chloe", "amount": 75},
    {"user": "bob", "amount": 10},
]
"""
1. Essaie d'abord d'écrire un dict comprehension pur pour obtenir {user: total_des_montants} (somme par utilisateur). Écris-le, puis prédis ce que ça va donner pour "alice" et "bob" avant de l'exécuter.
2. Exécute-le. Est-ce que ta prédiction était juste ? Si le résultat est faux, explique pourquoi une comprehension ne peut pas résoudre ce problème correctement.
3. Écris la version qui fonctionne réellement, avec l'outil de ton choix (tu en as déjà pratiqué au moins un qui convient parfaitement à ce cas).
"""

# Reponse Q-1
somme_par_utilisateur = {transaction['user']: transaction['amount'] for transaction in transactions}
# prediction Alice: 30, bob: 10
print(somme_par_utilisateur) # output {'alice': 30, 'bob': 10, 'chloe': 75}

# Reponse Q-2
# ce qui se passe reelement c'est que less cles retiennent les dernieres valeurs qui leur sont associees.

# solution avec defaultdict
somme_par_utilisateur_2 = defaultdict(int)
for transaction in transactions:
    user = transaction['user']
    amount = transaction['amount']

    somme_par_utilisateur_2[user] += amount

print(somme_par_utilisateur_2)

# utilisation de Counter
somme_par_utilisateur_3 = Counter()
for transaction in transactions:
    user = transaction['user']
    amount = transaction['amount']

    somme_par_utilisateur_3[user] += amount

c1 = Counter(alice=150, bob=-30)
c2 = Counter()
print(c1 + c2) # output: Counter({'alice': 150}) mais je ne comprends encore ce que tu veux me faire remarquer a travers cet exemple.
print(somme_par_utilisateur_3)

 
