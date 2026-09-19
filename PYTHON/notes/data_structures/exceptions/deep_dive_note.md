# Exceptions Python — perspective Lead / professionnelle
## Niveau 1
- Utilise if ... raise : Quand tu es l'auteur d'une fonction et que tu veux imposer des règles d'utilisation à celui qui l'appelle (ex: vérifier qu'un âge n'est pas négatif).

- Utilise try / except : Quand tu appelles une opération qui risque d'échouer indépendamment de la qualité de ton propre code (E/S, bases de données, requêtes HTTP).

## Resume:
Est-ce une condition prévisible sur tes arguments ?
├── OUI  ─► Utilise `if condition: raise MonException(...)`
└── NON  ─► Utilise `try / except` autour de l'opération risquée
             │
             ├── Peux-tu réparer l'erreur ou fournir une valeur par défaut ?
             │    ├── OUI  ─► Absorbe l'erreur (pas de `raise`)
             │    └── NON  ─► As-tu besoin de logger / traduire / nettoyer ?
             │                 ├── OUI  ─► Fais l'action puis fais `raise`
             │                 └── NON  ─► Ne mets AUCUN try/except (laisse propager)

- exemple:
```python
def controller_http():
    try:
        # 1. Le contrôleur tente d'exécuter la logique
        total = calculer_remise("deux cents", 0.1)
    except TypeError as e:
        # 3. L'exception est attrapée ICI, à la frontière externe de l'application
        return JSONResponse(status_code=400, content={"error": "Données invalides"})

def calculer_remise(prix, taux):
    # 2. L'erreur survient ici. Pas de try/except : l'erreur remonte immédiatement à controller_http()
    return prix * (1 - taux)

```
- NB Règle d'or : Laisser propager, c'est déléguer la responsabilité. Si ta fonction n'a rien d'utile à faire face à une erreur (ni correction, ni log, ni traduction, ni nettoyage avec finally), son rôle est de s'écarter et de laisser passer l'exception.

## Niveau adavance
1. Hiérarchie et héritage des exceptions

Modèle mental : ce n'est pas un sac plat de types d'erreurs, c'est un arbre, et la position dans l'arbre encode une intention de conception de la part de CPython.

BaseException
 ├── SystemExit, KeyboardInterrupt, GeneratorExit   # signaux, pas des "erreurs"
 └── Exception
      ├── ArithmeticError → ZeroDivisionError, OverflowError
      ├── LookupError     → IndexError, KeyError
      ├── OSError         → FileNotFoundError, PermissionError, ConnectionError, TimeoutError...
      ├── ValueError, TypeError, AttributeError, RuntimeError, ...

Deux points que la plupart des devs intermédiaires ignorent :

- LookupError est le parent commun de IndexError et KeyError. Si tu écris une fonction générique get_item(collection, key) qui accepte indifféremment une liste ou un dict, except LookupError: capture les deux cas sans dupliquer de logique.
- ConnectionError, TimeoutError, FileNotFoundError sont tous des sous-classes d'OSError. C'est pour ça qu'une lib réseau bien faite catch parfois OSError plutôt qu'une liste de dix types précis — c'est délibéré, pas un manque de rigueur.

Application Lead : construis ta propre hiérarchie applicative.

class AppError(Exception):
    """Racine commune de toutes les erreurs métier de l'application."""

class ValidationError(AppError):
    pass

class PaymentError(AppError):
    pass

class InsufficientFundsError(PaymentError):
    pass

Ça donne à l'appelant deux niveaux de granularité gratuits :
except InsufficientFundsError:   # réaction précise
except PaymentError:             # réaction générique à tout problème de paiement
except AppError:                 # frontière de l'application (ex: handler global FastAPI)

Erreur fréquente : hériter directement de BaseException pour une exception métier. Ne fais ça jamais — BaseException est réservé aux signaux d'interruption du langage. Toute exception applicative hérite d'Exception (directement
ou via ta propre racine).

Point avancé — mixins d'exception : l'héritage multiple est légal sur les exceptions, et parfois utnt transversal :

class Retryable:
    """Marqueur : signale au code appelant que réessayer a du sens."""

class PaymentTimeoutError(PaymentError, Retryable):
    pass

## ailleurs, sans connaître le type précis :
try:
    charger_carte(...)
except Retryable:
    retry()
except PaymentError:
    abandonner()

C'est une façon élégante d'attacher une propriété ("peut être retenté") indépendamment de la hiérar

---

2. Quand créer une exception personnalisée

Créer une exception quand :
- l'appelant a besoin de réagir différemment selon le type d'échec (pas juste afficher un message différent) ;
- tu veux transporter des données structurées sur l'échec, pas juste du texte ;
- tu traduis une frontière d'architecture (déjà pratiqué avec traiter_commande).

class InsufficientFundsError(Exception):
    def __init__(self, solde: float, montant: float):
        super().__init__(f"Solde {solde} insuffisant pour {montant}")
        self.solde = solde
        self.montant = montant
        self.manquant = montant - solde

## le code appelant peut réagir programmatiquement, pas juste logger :
except InsufficientFundsError as e:
    proposer_autorisation_decouvert(e.manquant)

C'est ça, la vraie valeur ajoutée d'une exception perso : pas le nom de classe, les attributs explo

Ne PAS créer une exception quand :
- elle n'ajoute aucune sémantique par rapport à un built-in (class MonValueError(ValueError): pass sans attribut ni distinction réelle → bruit) ;
- tu es tenté de créer une classe par fonction ("exception class explosion", voir anti-patterns).

Convention : suffixe Error, nom qui décrit la condition métier, pas l'implémentation (InsufficientFaintViolation remonté tel quel dans une couche métier).

---

3. raise (bare) vs raise e — préservation du traceback

raise seul (à l'intérieur d'un except) relève l'exception activement gérée, telle quelle, tracebacktruire de nouvel objet :

try:
    risky()
except ValueError as e:
    logger.error("échec", exc_info=e)
    raise          # ✅ idiomatique : relève EXACTEMENT ce qui a été attrapé

raise e relève explicitement l'objet référencé par e. En Python 3, e.__traceback__ est un attribut  — donc raise e conserve aussi le traceback (le mythe "raise e casse le traceback" vient de Python2, où le traceback vivait à part dans sys.exc_info()). Les deux formes sont fonctionnellement proches en Python 3.

Où est la vraie différence, alors ?

1. raise (bare) n'est utilisable que dans le bloc except qui gère activement l'exception — hors de ce contexte, ça lève RuntimeError: No active exception to re-raise. raise e marche n'importe où, tant que tu as une référence à e
   (utile si tu stockes des exceptions dans une liste pour les relever plus tard, ex. dans un mécan.
2. Le vrai piège de raise e : si tu le fais depuis un contexte différent de celui où e a été attrapée à l'origine (par exemple, tu la relèves depuis un autre except, ou après un finally qui a lui-même levé une exception
   intermédiaire), Python attache automatiquement au nouvel objet relevé un __context__ qui pointe  en cours de gestion à cet endroit-là — pas nécessairement celle que tu crois. Résultat : untraceback qui affiche un chaînage implicite trompeur, sans rapport avec la cause réelle.

Règle pratique : utilise raise (bare) par défaut — c'est plus court, sans ambiguïté, impossible à faire "un peu à côté". Réserve raise e explicite aux cas où tu relèves une exception stockée depuis un endroit différent de celui
où elle a été capturée, et dans ce cas, pense à raise e from None si tu veux explicitement éviter u avec le contexte du nouvel endroit.

Erreur classique à éviter : raise type(e)(str(e)) — ça reconstruit un nouvel objet exception, perd le message texte est repris), et ne préserve la cause que si tu ajoutes from e toi-même. Ne faisjamais ça pour "juste relever la même erreur" — utilise raise bare.

---

4. Chaînage — au-delà de from e

Tu maîtrises from e (__cause__) et le chaînage implicite (__context__). Trois nuances Lead :

raise ... from None — supprimer volontairement le chaînage. Utile quand la cause technique est un détail d'implémentation sans intérêt pour qui lit le traceback :

class Config:
    def get(self, key):
        try:
            return self._data[key]
        except KeyError:
            raise AttributeError(f"Config sans attribut {key!r}") from None

Sans from None, l'utilisateur verrait un KeyError interne accroché au AttributeError public — un déte. from None force __suppress_context__ = True, et Python n'affiche plus la ligne "During handlingof...".

__cause__ vs __context__ — coexistence, pas exclusion. Même quand tu utilises from e, __context__ est quand même rempli automatiquement (c'est __suppress_context__ qui décide si le traceback l'affiche ou non). Tu peux inspecter
les deux séparément en code (observabilité/logging structuré) :

except Exception as e:
    logger.error("échec", cause=e.__cause__, contexte_implicite=e.__context__)

Exception Groups (Python 3.11+) — le chaînage "horizontal". from e chaîne verticalement (une cause → une conséquence). Pour le cas "plusieurs opérations indépendantes échouent en parallèle et je veux TOUTES les remonter, pas
juste la première" (le pattern "continuer et collecter" qu'on a travaillé avec process_users) :

try:
    ...
except* ValueError as eg:
    for exc in eg.exceptions:
        ...

ExceptionGroup est la réponse native du langage à exactement ce besoin — pertinent avec asyncio.Tasncurrentes peuvent échouer indépendamment.

---

5. Choisir la portée d'un try

Deux responsabilités à ne pas confondre, chacune avec une portée différente :

- finally pour une garantie (nettoyage, log, libération de ressource) → portée large, doit envelopp garantie (le pattern qu'on a construit avec traiter_commande).
- except pour une récupération ciblée → portée minimale, entoure exactement l'appel qui peut lever l'exception précise que tu sais gérer.

Anti-pattern classique :
try:
    data = parse(raw)
    user = fetch_user(data["id"])
    user.update(data)
    save(user)
except Exception as e:                 # ❌ bien trop large
    logger.error(e)
Si save(user) lève une TypeError à cause d'un bug de programmation (faute de frappe sur un attribut), ce bloc l'avale silencieusement en même temps qu'une vraie erreur de parsing — tu perds la distinction entre "erreur métier
attendue" et "bug dans mon propre code".

Version correcte :
try:
    data = parse(raw)
except ParseError as e:
    raise DonneesInvalidesError(...) from e

user = fetch_user(data["id"])   # hors du try : si ça bug, ça doit planter fort
user.update(data)
save(user)

Règle : le try ne devrait contenir que la ligne (ou les quelques lignes étroitement liées) dont tu tion peut en sortir et précisément quoi faire de cette exception.

---

6. Exceptions vs flux de contrôle normal

En Python, les exceptions sont un mécanisme de flux de contrôle légitime — StopIteration est littérr sait s'arrêter. Ce n'est pas un accident, c'est un choix de design assumé (contrairement à deslangages où l'exception est réservée au vraiment exceptionnel).

Mais ça ne veut pas dire "utilise des exceptions partout". La distinction professionnelle :
- Flux normal et fréquent, résultat prévisible → if/else classique, pas d'exception.
- Condition limite, erreur de programmation, ou franchissement de frontière système (fichier absent, réseau down, donnée invalide en entrée) → exception.

Le point de performance concret : en CPython, entrer dans un try sans qu'aucune exception ne se déclenche est quasi gratuit (quelques instructions bytecode). Lever une exception (construire l'objet, remonter la pile, construire
le traceback) coûte réellement cher. Conséquence directe → section suivante.

---

7. EAFP vs LBYL

LBYL (Look Before You Leap) : vérifier avant d'agir.
EAFP (Easier to Ask Forgiveness than Permission) : agir, gérer l'échec s'il survient. C'est le style par défaut idiomatique en Python (le duck typing en dépend : on appelle la méthode et on catch AttributeError, plutôt que
hasattr puis appeler).

Argument le plus important, souvent oublié : la sécurité face aux races (TOCTOU).
if os.path.exists(path):    # ❌ LBYL : fenêtre de race
    with open(path) as f:   # le fichier peut disparaître ENTRE les deux lignes
        ...
try:                          # ✅ EAFP : atomique, pas de fenêtre
    with open(path) as f:
        ...
except FileNotFoundError:
    ...
Dans un contexte multi-thread, multi-process, ou simplement filesystem partagé, LBYL a un vrai bug de concurrence que EAFP n'a pas.

Argument de performance : ça dépend de la fréquence d'échec.
- Cas de succès fréquent (échec rare) → EAFP gagne : LBYL fait le lookup deux fois (une pour vérifile fait une fois et ne paie le "vrai" coût que dans le cas rare.
- Cas d'échec fréquent (ex : validation d'input utilisateur, où 80% des soumissions sont invalides) → LBYL gagne : payer le coût d'une exception à chaque itération d'une boucle à haute fréquence d'échec est plus lent qu'un
  simple test conditionnel.

Règle Lead : EAFP par défaut pour le code "métier" normal (c'est idiomatique et évite les races) ; nd tu valides des entrées avec un taux d'échec élevé et prévisible (validation de formulaire,parsing de données externes en masse).

---

8. Propagation à travers les couches (repository → service → API)

C'est la généralisation architecturale du translation pattern qu'on a pratiqué (traiter_commande, charger_carte).

Règle de couche : chaque couche traduit les exceptions de la couche en dessous (technique, spécifique à l'implémentation) en exceptions compréhensibles pour la couche au-dessus (métier), avec from e pour ne rien perdre.

## Repository — connaît SQLAlchemy, personne d'autre ne devrait le savoir
class UserRepository:
    def get_by_id(self, user_id: int) -> User:
        try:
            return self._session.query(User).filter_by(id=user_id).one()
        except NoResultFound as e:
            raise UserNotFoundError(user_id) from e
        except IntegrityError as e:
            raise DataIntegrityError(...) from e

## Service — ne connaît que UserNotFoundError, jamais SQLAlchemy
class UserService:
    def deactivate(self, user_id: int) -> None:
        user = self._repo.get_by_id(user_id)   # laisse UserNotFoundError se propager
        if user.has_pending_orders():
            raise CannotDeactivateError(user_id)  # nouvelle règle métier, pas une traduction
        user.deactivate()

## API (FastAPI) — traduit le vocabulaire métier en HTTP
@app.exception_handler(UserNotFoundError)
def handle_not_found(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(CannotDeactivateError)
def handle_conflict(request, exc):                                                                                                                                                                                                  return JSONResponse(status_code=409, content={"detail": str(exc)})
                                                                                                                                                                                                                                  ints clés :
- Le type d'exception qu'une fonction peut lever fait partie de son contrat public, au même titre que son type de retour. Le service ne doit jamais avoir besoin de except sqlalchemy.exc... — sinon tu as une fuite d'abstraction(changer d'ORM demain casserait le service).
- Toutes les exceptions ne se traduisent pas : une vraie erreur de programmation (TypeError, AssertionError) ne doit pas être avalée et transformée en exception métier "normale" — elle doit remonter et faire du bruit (ou être loggée à la frontière la plus externe, cf. point 6 de la séance précédente sur la légitimité du c
- Pour éviter la duplication de logique de traduction dans chaque méthode du repository, un décorateur ou context manager dédié est une solution Lead courante :
@contextmanager
def translate_db_errors():
    try:
        yield
    except IntegrityError as e:
        raise DataIntegrityError(...) from e
    except NoResultFound as e:
        raise UserNotFoundError(...) from e

---

9. Anti-patterns professionnels courants

1. except: pass — le pire. Aucune trace, aucun log, échec total et invisible. Pire encore que return None silencieux vu dans get_user_data.
2. Catch large enfoui profondément dans la logique métier "pour être safe" — déjà travaillé en détaement.
3. Log-and-raise dupliqué à chaque couche : chaque niveau logge la même exception en la relevant → la même erreur apparaît 5 fois dans les logs de prod, noyant l'observabilité. Corrige : logge une fois, en général à la frontière externe, ou attache du contexte sans re-logger.
4. Reconstruire une exception (raise type(e)(...)) au lieu de raise bare ou raise ... from e — perte de traceback, décrit au point 3.
5. Exception class explosion : une classe d'exception par fonction, sans réelle différence de sémantcher dix types pour un seul concept métier.
6. Utiliser les exceptions comme un goto pour sortir de boucles imbriquées au lieu de refactorer en fonction — code smell, sauf usage sanctionné (StopIteration dans un générateur).
7. Exposer des données sensibles dans un message d'exception (mot de passe, token, requête SQL brutne réponse API — risque de sécurité, pas juste de style.

---

À pratiquer avant d'avancer

Par ordre de priorité, du plus important au plus accessoire :

1. Propagation multi-couches (point 8) — le sujet le plus "Lead" du lot, jamais pratiqué concrètemecouches réelles (repository/service/API factices) te ferait passer de "je comprends la théorie" à"je l'ai fait".
2. EAFP vs LBYL sur un cas de race réelle — écris toi-même un exemple où LBYL introduit un vrai bugdict partagé entre threads), pour voir la faille plutôt que juste l'admettre en théorie.
3. raise e vs raise bare — teste toi-même le piège du __context__ trompeur en relevant une exception stockée depuis un endroit différent de sa capture ; observe le traceback réel.
4. ExceptionGroup/except* — nouveau (3.11+), jamais vu ; à mettre de côté tant que les points 1-3 ngarder en tête pour plus tard (pertinent avec asyncio).

Le reste (hiérarchie, custom exceptions, from None, portée du try, anti-patterns) est bien compris ore été mis à l'épreuve dans du code que tu écris toi-même. Dis-moi si tu veux qu'on bascule surlearning_coach pour un exercice de conception sur le point 1 (propagation multi-couches) — c'est le plus rentable des quatre.
