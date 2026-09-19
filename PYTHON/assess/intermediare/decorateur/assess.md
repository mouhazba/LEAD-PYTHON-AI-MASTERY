 # Decorators.

Cible de maîtrise : 🔵 Advanced — les décorateurs sont explicitement listés comme sujet structurant du roadmap Lead (comme Exceptions), et ils sont omniprésents dans FastAPI (@app.get(...), @router.post(...), dépendances) et dans du code professionnel en général. L'objectif ici n'est pas juste "savoir écrire un décorateur simple" mais pouvoir en concevoir un correctement, éviter les pièges classiques, et défendre les choix (décorateur vs composition simple, etc.).

Petit diagnostic (pas de correction pour l'instant, réponds du mieux que tu peux) :

1. En une phrase, comment définirais-tu ce qu'est un décorateur en Python, indépendamment de l'exemple logger qu'on a fait ?

2. Si on empile deux décorateurs sur la même fonction :
@decorateur_a
@decorateur_b
def ma_fonction():
    ...
Dans quel ordre s'appliquent-ils ? Explique ton raisonnement.

3. Exercice pratique — écris un décorateur chrono qui mesure et affiche le temps d'exécution d'une fonction décorée (utilise time.perf_counter()), en utilisant functools.wraps pour préserver le nom original de la fonction.

4. Sais-tu comment écrire un décorateur qui prend lui-même des arguments, par exemple @repeat(3) pour exécuter la fonction décorée 3 fois ? Si tu en as une idée, essaie un squelette même imparfait. Si tu ne sais pas, dis-le simplement.

5. Un décorateur peut-il s'appliquer à une méthode d'une classe (pas juste une fonction libre) ? Y a-t-il une différence de comportement ?
