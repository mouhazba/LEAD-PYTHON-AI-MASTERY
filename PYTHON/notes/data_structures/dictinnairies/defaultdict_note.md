1. Counter et defaultdict (module collections)

L'idée et pourquoi c'est utile
Ta solution à Q5 (if mot in dict: ... else: ...) est correcte, mais c'est un pattern tellement courant(compter des occurences) que Python fournit des outils tout faits.

- defaultdict : un dict qui, quand tu accèdes à une clé absente, la crée automatiquement avec une valeur par defaut (au lieu delever  une KeyError). 
    Ça élimine ton if mot in dict.
- Counter : une sous-classe de dict spécialisée dans le comptage d'éléments. pour compter, qui en plus peut construire le compte directement depuis un itérable, sans boucle du tout.
NB:
> 1 If your code is heavily base on dictionaries and you’re dealing with missing keys all the time, then you should consider using a defaultdict rather than a regular dict.

> 2 If your dictionary items need to be initialized with a constant default value, then you should consider using a defaultdict instead of a dict.

> 3 If your code relies on dictionaries for aggregating, accumulating, counting, or grouping values, and performance is a concern, then you should consider using a defaultdict.

Exemple
from collections import defaultdict, Counter

mots = ["chat", "chien", "chat", "oiseau", "chien", "chat"]

# Version defaultdict — remplace ton if/else
compteur = defaultdict(int)  # int() renvoie 0 par défaut
for mot in mots:
    compteur[mot] += 1

# Version Counter — remplace toute la boucle
compteur2 = Counter(mots)
# Counter({'chat': 3, 'chien': 2, 'oiseau': 1})

compteur2.most_common(1)  # [('chat', 3)] — le plus fréquent

Pièges fréquents
- defaultdict(int) : le int n'est pas appelé tout de suite — c'est une factory function passée sans parenthese, appelee par le dict quand une clé manque. - Écrire defaultdict(int()) est une erreur fréquente (ça asse 0, pas une fonction).
- defaultdict crée réellement la clé dès que tu y accèdes, même en lecture simple (compteur["inconnu"] cree "i"nconnu": 0). Contairement à .get() qui ne    modifie jamais le dict. C'est une différence de comportement importante à retenir.
- Counter est un sous-type de dict — toutes tes méthodes habituelles (.items(), .get()) fonctionnen

Lien avec ce que tu sais
defaultdict est essentiellement une version automatisée de ton pattern Q5 (if mot not in dict: init sinon incrémente). Counter va encore plus loin en supprimant la boucle explicite. Et le piège defaultdict vs .get() rejoint directement ta réponse Q4 sur la gestion de KeyError — ce sont deux philosophies différentes face à une cle absente: .get ne cree rien, defaultdict crée automatiquement.
