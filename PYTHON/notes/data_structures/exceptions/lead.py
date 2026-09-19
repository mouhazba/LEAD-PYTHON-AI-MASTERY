#Bon choix — on garde ça 100% Python pur, sans FastAPI ni ORM réel : trois couches simulées avec juste des dicts en mémoire et des exceptions custom. 
# Le principe de propagation est identique, juste sans le vocabulaire framework.

#Scénario — Système d'emprunt de bibliothèque
"""
Trois couches :

LivreRepository   (technique, bas niveau)
      ↓
EmpruntService    (métier, règles de gestion)
      ↓
Code appelant     (joue le rôle de la "couche présentation" — pas d'API réelle)

LivreRepository — simule un accès à une base de données avec un simple dict interne (self._livres = {1: {"titre": "Dune", "exemplaires_disponibles": 2}, ...}). 
Pour simuler une vraie couche technique, elle doit pouvoir échouer de deux façons différentes :
- demander un livre_id qui n'existe pas dans le dict ;
- une panne technique simulée — par exemple une fonction _verifier_connexion() que tu écris toi-même et 
    qui lève aléatoirement (ou selon un flag que tu contrôles) une exception représentant "la base de données est injoignable".

EmpruntService — ne doit jamais savoir que le stockage est un dict Python. Elle appelle le repository, et applique une vraie règle métier 
    indépendante du stockage : par exemple, un utilisateur ne peut pas emprunter un livre s'il a déjà atteint son quota (max_emprunts = 3),
    une info que le service connaît, pas le repository.

Code appelant — n'a besoin de connaître que les exceptions du service (jamais celles du repository). Il décide quoi faire : afficher un message, journaliser, 
réessayer.

---

Avant d'écrire une ligne de code, dessine-moi l'architecture, comme on l'a fait pour traiter_commande :

1. Quelle hiérarchie d'exceptions tu prévois (quelles classes, et qui hérite de quoi) ?
2. Pour chaque type d'échec possible (livre inexistant, panne technique simulée, quota d'emprunt dépassé) — à quelle couche l'exception naît-elle, 
et à quelle couche est-elle traduite (avec from e) versus simplement créée directement parce que c'est une nouvelle règle métier qui n'a pas de cause
 technique sous-jacente ?
3. Où se trouve le try/except dans EmpruntService : autour de quoi exactement ?

Pas de code pour l'instant — juste le plan, comme texte ou pseudo-code.

"""

class AppError(Exception):
    """Racine commune de toutes les erreurs de l'application."""

# BRANCHE TECHNIQUE (Couche LivreRepository)  
class RepositryError(AppError):
    """Racine des erreurs de stockage / infrastructure."""

class ConnexionError(RepositryError):
    """Levée quand la base de données est injoignable."""

class LivreIntrouvableError(RepositryError):
    """Levée quand le livre_id n'existe pas dans le dictionnaire."""

# BRANCHE MÉTIER (Couche EmpruntService)
class ServiceError(AppError):
     """Racine des erreurs métier de l'application."""

class Retryable(ServiceError):
    """Levee quand la connexion est defectueuse""" 

class ServiceObtenirLivreError(ServiceError):
    """Levee quand un livre est introuvable au respository"""

class QuotaError(ServiceError):
     """Levée quand l'utilisateur a déjà 3 emprunts à son actif."""


class LivreRepository:
    def __init__(self, connexion_ok: bool = False):
        self._connexion_ok = connexion_ok
        self._livres = {1: {"title": "Dune", "exemplaires_disponibles": 2},  2: {"title": "1984", "exemplaires_disponibles": 5}}

    
    def verifier_connexion(self):
        if not self._connexion_ok:
            raise ConnexionError()
        return self._connexion_ok
         
    def obtenir_livre(self, id_livre):
        try:
            return self._livres[id_livre]
        except KeyError as e:
            raise LivreIntrouvableError() from e

class EmpruntService:
    def __init__(self, repository: LivreRepository):
        self._repository = repository
        self.numbre_emprunt = 0

    def emprunt_livre(self, user, id_livre):
        try:
            self._repository.verifier_connexion()
        except ConnexionError as e:
            raise Retryable("Connexion en panne") from e
        else:
            # connexion etablie   
            try:
                l = self._repository.obtenir_livre(id_livre)
            except LivreIntrouvableError as e:
                raise ServiceObtenirLivreError("Livre introuvable") from e

            if self.numbre_emprunt > 3:
                raise QuotaError("Quota d'emprunt atteint")
            
            self.numbre_emprunt += 1
            print(f"emprunt du livre {l} par {user} reussi")
# code appelant
# cas 1 Connexion en panne:

repo = LivreRepository()
emprunt = EmpruntService(repo)
try:
    emprunt.emprunt_livre("Modou", 1)
except Retryable as e:
    # action ex reesasyer
    print(e)
except ServiceObtenirLivreError as e:
    print(e)
except QuotaError as e:
    print(e)
# output: Connexion en panne

# cas 2 Livre introuvable:
repo = LivreRepository(True)
emprunt = EmpruntService(repo)
try:
    emprunt.emprunt_livre("Modou", 3)
except Retryable as e:
    # action ex reesasyer
    print(e)
except ServiceObtenirLivreError as e:
    print(e)
except QuotaError as e:
    print(e)
# output: Livre introuvable

# cas 3 Quota atteint:
repo = LivreRepository(True)
emprunt = EmpruntService(repo)
emprunt.numbre_emprunt = 4
try:
    emprunt.emprunt_livre("Modou", 1)
except Retryable as e:
    # action ex reesasyer
    print(e)
except ServiceObtenirLivreError as e:
    print(e)
except QuotaError as e:
    print(e)
# output: Quota d'emprunt atteint

# cas 4 Emprunt reussi:
repo = LivreRepository(True)
emprunt = EmpruntService(repo)
try:
    emprunt.emprunt_livre("Modou", 1)
except Retryable as e:
    # action ex reesasyer
    print(e)
except ServiceObtenirLivreError as e:
    print(e)
except QuotaError as e:
    print(e)
# output: emprunt du livre {'title': 'Dune', 'exemplaires_disponibles': 2} par Modou reussi

# cas 5 Emprunt reussi:
repo = LivreRepository(True)
emprunt = EmpruntService(repo)
try:
    emprunt.emprunt_livre("Modou", 2)
except Retryable as e:
    # action ex reesasyer
    print(e)
except ServiceObtenirLivreError as e:
    print(e)
except QuotaError as e:
    print(e)
# output: emprunt du livre {'title': '1984', 'exemplaires_disponibles': 5} par Modou reussi