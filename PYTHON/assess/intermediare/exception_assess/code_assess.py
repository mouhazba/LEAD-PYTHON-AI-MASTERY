# Reponse Q-1
# Except Exception ne capture que les erreurs derivees de la class Exception alors que except tout cours capture la racine absolue BaseException tel que
# KeyboarInterrupt ou CTL + C ou SystemExit.

# Reponse Q-2

chaine_1 = "12"
try:
    int_chaine = int(chaine_1)
except ValueError as e:
    print(f"Valeur incorrecte: {e}")
else:
    print(int_chaine)
finally:
    print("Termine")

# ouput chaine_1 : 12, Termine

chaine_2 = "abc"
try:
    int_chaine = int(chaine_2)
except ValueError as e:
    print(f"Valeur incorrecte: {e}")
else:
    print(int_chaine)
finally:
    print("Termine")

# ouput chaine_2 : Valeur incorrecte invalid literal for int() with base 10: 'abc', Termine

# else permet de separer le test(ici: conversion) et la capture, et ne s'excute que si le test passe.

# Reponse Q-3. Ce code lève une exception :
def diviser(a, b):
    return a / b

diviser(10, 0)
# une exception de type Division par ZeroDivisionError est levee
# pour capturer les deux on fait : except (ZeroDivisionError, TypeError) dans une meme paire de parentheses.

# Reponse Q-4
"""
> La j'ai besoin d'expications pour combler mon erreur conceptuelle et le gap.
"""

# Reponse Q-5
"""
> Je créerais une exception personnalisée (classe héritant d'Exception) plutôt que d'utiliser une exception standard de Python car cela permettre a l'appelant
de mieux distinguer le type d'erreur au lieu de parser un message d'erreur.
> exemple:
"""
class SoldeInsuffisantError(Exception):
    #Levée quand un retrait dépasse le solde disponible.
    pass
