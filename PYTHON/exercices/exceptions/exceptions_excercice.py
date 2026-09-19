# Exercice — retrait bancaire

class SoldeInsuffisantError(Exception):
    """Levée quand un retrait dépasse le solde disponible."""

class CompteInvalideError(Exception):
    """Levee quand la cle solde n'existe pas"""

def retirer(compte: dict, montant: float) -> float:
    try:
        if not compte:
            raise CompteInvalideError("Compte vide")
        
        if not isinstance(montant, (int, float)):
            raise TypeError(f"Montant invalide: {montant!r}")
        

        try:
            solde = compte["solde"]
        except KeyError as e:
            raise CompteInvalideError("Dict mal forme!") from e
        else:
            if montant > solde:
                raise SoldeInsuffisantError("Solde insuffisant")
            compte['solde'] -= montant
            return compte['solde']
    finally:
        print("Operation terminee")
    
   

# test 1
try:
    print(retirer({}, 100))
except Exception as e:
    print(e)
#output: Opration Terminee + Compte vide

# cas 2
try:
    print(retirer({"titulaire": "alice", "solde": 200}, "100"))
except Exception as e:
    print(e)
#output: Opration Terminee + Montant invalide

# cas 3
try:
    print(retirer({"titulaire": "alice", "solde": 200}, 250))
except Exception as e:
    print(e)
#output: Opration Terminee + Solde insuffisant

# cas 4
try:
    print(retirer({"titulaire": "alice"}, 50))
except Exception as e:
    print(e)
#output: Opration Terminee + Dict mal forme

# cas 5
try:
    print(retirer({"titulaire": "alice", "solde": 200}, 100))
except Exception as e:
    print(e)
#output: Opration Terminee + 100

# compte est un dict du type {"titulaire": "alice", "solde": 200}.

# Écris le corps de retirer pour que :
"""
1. Si montant n'est pas un int ou un float, on lève un TypeError avec un message clair.
2. Si montant > compte["solde"], on lève ta SoldeInsuffisantError (pas besoin de from ici — ce n'est pas une traduction d'une autre exception).
3. Si la clé "solde" n'existe pas dans compte (dict mal formé), on doit lever une nouvelle exception CompteInvalideError (à créer) qui traduit la KeyError d'origine — en utilisant le chaînage explicite qu'on vient de voir.
4. Si tout est correct, on déduit le montant du solde et on retourne le nouveau solde.
5. Dans tous les cas (succès ou échec), on affiche "Opération terminée" — un seul endroit dans le code pour ça, pas répété dans chaque branche.
"""