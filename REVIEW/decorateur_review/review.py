#Dernier exercice pour ce cycle : une revue de code, comme si c'était la PR d'un collègue. Voici un décorateur retry :

def retry(func):
    def wrapper(*args, **kwargs):
        tentatives = 0
        while tentatives < 3:
            try:
                return func(*args, **kwargs)
            except:
                tentatives += 1
        print(f"Echec apres 3 tentatives")
    return wrapper

#Identifie tous les problèmes que tu vois (il y en a plusieurs, de nature différente)
#et propose les corrections. Tu as tout ce qu'il faut avec ce qu'on vient de voir sur les décorateurs et ce que tu maîtrises déjà sur les exceptions.

# les erreurs:
# le bloc try-except doit permettre decider de collecter-continuer ou le Fail-fast arrter et traiter


# correction:
from functools import wraps

def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        tentatives = 0
        while tentatives < 3:
            try:
                resultat = func(*args, **kwargs)
                return resultat
            except Exception as e:
                tentatives += 1
                if tentatives >=3:
                    raise RuntimeError(f"Echec de {func.__name__} après {tentatives} tentatives")
    return wrapper

