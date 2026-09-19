Séance précédente (2026-09-02) : comprehensions list/dict solides, niveau 🟢 Competent. Je note un point : le dernier commit dit "list, dict, set, done" mais en relisant comprehension_exercice.py, code_assess.py et les notes, je ne trouve aucune trace d'exercice sur la set comprehension ({expr for x in iterable}) — seulement list et dict ont été réellement pratiquées et évaluées. Je ne vais donc pas la compter comme acquise tant qu'elle n'a pas été testée.

Plusieurs points restent aussi en attente depuis les séances Dict/Sets : dictionnaires imbriqués (nested dicts) et fusion de dicts (|, .update()).

● User answered Claude's questions:
· Sur quoi veux-tu travailler pour cette séance ? → Exceptions

On attaque les Exceptions. Diagnostic d'abord — pas de cours, juste pour voir précisément où tu en es. Réponds avec ton raisonnement, pas juste du code produit sans explication.

Diagnostic (5 questions)

1. Quelle est la différence entre except Exception: et except: (bare except) ? Pourquoi l'un des deux est-il généralement déconseillé ?
2. Écris un bloc try/except/else/finally qui : essaie de convertir une chaîne en int, affiche le résultat si ça réussit (else), affiche un message d'erreur si ValueError est levée, et affiche "Terminé" dans tous les cas (finally). Explique en une phrase le rôle précis de else par rapport à mettre ce code directement à la fin du try.
3. Ce code lève une exception :
def diviser(a, b):
    return a / b

diviser(10, 0)
Quel est le type exact de l'exception levée ? Et si je veux capturer à la fois une ZeroDivisionError et une TypeError dans le même bloc except, comment j'écris ça ?

4. Explique la différence entre lever une nouvelle exception avec raise ValueError("msg") à l'intérieur d'un except, et faire raise ValueError("msg") from original_exception. Qu'est-ce que ça change concrètement dans le traceback ?
5. Dans quel cas est-ce que tu créerais une exception personnalisée (classe héritant d'Exception) plutôt que d'utiliser une exception standard de Python ? Donne un exemple concret de nom de classe que tu créerais dans un projet réel.



Ton erreur initiale : "raise dans un except évite un arrêt brusque." C'est l'inverse. raise interrompt l'exécution à cet endroit précis, exactement comme n'importe quel raise — la fonction en cours s'arrête là, et l'exception remonte la pile d'appels jusqu'à un except qui la capture (ou jusqu'au crash du programme).

Alors pourquoi re-lever une exception depuis un except ? Généralement pour traduire une erreur de bas niveau en une erreur de sens métier, plus utile pour l'appelant :

def charger_config(chemin):
    try:
        with open(chemin) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigurationError(f"Config introuvable: {chemin}") from e

L'appelant de charger_config n'a pas à savoir que ça vient d'un fichier JSON manquant — il a juste besoin de savoir que la config a échoué.

Maintenant le point que tu n'avais pas vu : le chaînage se fait automatiquement, même sans from.

try:
    int("abc")
except ValueError:
    raise RuntimeError("échec du traitement")
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 10: 'abc'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  ...
RuntimeError: échec du traitement

Python affiche les deux automatiquement, avec le message "During handling of the above exception, another exception occurred". C'est le chaînage implicite : Python stocke la première exception dans l'attribut __context__ de la seconde, dès qu'une exception est levée à l'intérieur d'un bloc except.

raise ... from e fait autre chose : il fixe explicitement l'attribut __cause__, et le message devient "The above exception was the direct cause of the following exception". C'est toi qui affirmes le lien de causalité, plutôt que Python qui le déduit du simple fait que tu étais dans un except.

Troisième cas, utile à connaître : raise RuntimeError("...") from None supprime l'affichage du chaînage — utile quand l'exception d'origine est un détail d'implémentation sans intérêt pour qui lit le traceback.

En résumé : from e ne "crée" pas le chaînage, il le rend explicite et intentionnel plutôt que le laisser implicite. Sans raise, le chaînage automatique existe déjà dès que tu es dans un bloc except.