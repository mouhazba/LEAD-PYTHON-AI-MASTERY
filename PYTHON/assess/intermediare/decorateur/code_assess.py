# 1 Un decorateur est une fonction python qui prend comme parametre une fonction en y ajoutant d'autres logiques sans alterer sa fonction metier premiere.
# puis retourne un callable

# Si on empile deux decorateur sur une meme fonction selon moi elle vont s'appliquer comme suite:
# b va s'appliuer sur la fonction en premiere puisque englobe la fonction
# puis a va s'appliquer sur b et la fonction car a englobe b ainsi que la fonction elle meme.

# 3 decorateur chrono
import time
from functools import wraps

def time_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        som_ca = [x for x in args]
        resultat = func(*args, **kwargs)
        end_time = time.perf_counter()
        duree = end_time - start_time
        print(f"La fonction {func.__name__} a pris {duree:.7f} temps d'execution.")
        return resultat, som_ca
    return wrapper

@time_execution
def addition(a, b):
    return a + b

addition(5,4) # output : La fonction addition a pris 0.0000014 temps d'execution.
print("*" * 70)

# 4 deocrateur avec parametre oui je crois
def func_decorateur_avec_parametre(n):
    def fun_decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(n):
                rslt = func(*args, **kwargs)
                print(f"Excution de {func.__name__} {i + 1} fois")
            return rslt
        return wrapper
    return fun_decor

@func_decorateur_avec_parametre(3)
def saluer(nom, message ="Bonjour"):
    return f"{message} {nom}."

saluer("Mouaz", "Nanga def")
# output:
"""
Excution de saluer 1 fois
Excution de saluer 2 fois
Excution de saluer 3 fois
"""
print("*" * 70)
print("@time_execution > @func_decorateur_avec_parametre > addition_bis")
@time_execution
@func_decorateur_avec_parametre(3)
def addition_bis(a, b):
    return a + b

addition_bis(5,4)
# ouput: 
"""
@time_execution > @func_decorateur_avec_parametre > addition_bis
Excution de addition_bis 1 fois
Excution de addition_bis 2 fois
Excution de addition_bis 3 fois
La fonction addition_bis a pris 0.0000385 temps d'execution.
"""

print("*" * 70)
print("@func_decorateur_avec_parametre > @time_execution > addition_bis")
@func_decorateur_avec_parametre(3)
@time_execution
def addition_bis(a, b):
    return a + b

addition_bis(5,4)
# ouput:
"""
@func_decorateur_avec_parametre > @time_execution > addition_bis
La fonction addition_bis a pris 0.0000006 temps d'execution.
Excution de addition_bis 1 fois
La fonction addition_bis a pris 0.0000005 temps d'execution.
Excution de addition_bis 2 fois
La fonction addition_bis a pris 0.0000004 temps d'execution.
Excution de addition_bis 3 fois
"""
print("*" * 70)

# Decoration a une methode de la classe: Oui je pense bien que c'est tout a fait possible de decorer une methode en particulier.
# Pour la diffference de comportement je ne suis pas sur.

# cas pratique dans une classe
class Operation:

    @time_execution
    def calculer(self, x, y):
        return x + y

op_ins = Operation()
op_slt, aut = op_ins.calculer(2, 3)
print(aut)
# output:
"""
La fonction calculer a pris 0.0000009 temps d'execution.
[<__main__.Operation object at 0x7169728912b0>, 2, 3]
"""
