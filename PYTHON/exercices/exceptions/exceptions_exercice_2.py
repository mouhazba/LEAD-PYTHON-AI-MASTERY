#Exercice de conception maintenant, sans indice de ma part cette fois.

#Contexte : tu écris une fonction traiter_commande(commande: dict) -> dict pour un petit système e-commerce. commande ressemble
#  à {"id": 42, "articles": [...], "client_email": "..."}.
"""
Contraintes :
1. Si commande["articles"] est une liste vide, c'est une erreur métier — invente et lève l'exception personnalisée de ton choix.
2. Le traitement appelle une fonction externe simulée envoyer_email(client_email) qui peut lever une ConnectionError (panne réseau simulée). 
Si ça arrive, tu dois la traduire en une exception métier à toi, en conservant la cause d'origine de façon explicite.
3. Que la commande réussisse ou échoue, il faut logger f"Commande {id} traitée" — une seule fois, un seul endroit dans le code, garanti dans tous les cas.
4. Si tout se passe bien, retourne {"status": "ok", "commande_id": ...}.

Écris traiter_commande en entier (tu peux simuler envoyer_email toi-même, par exemple une fonction qui lève ConnectionError selon une condition simple
 pour pouvoir tester les deux chemins). Réfléchis à la structure avant d'écrire — dis-moi d'abord comment tu comptes organiser les try avant de coder,
   si tu veux valider l'approche avant d'écrire tout le code.
"""
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 2. Create the logger instance
logger = logging.getLogger(__name__)

class CommandeVideError(Exception):
    """levee quand une commande est vide"""

class ArticleVideError(Exception):
    """levee quand la liste des articles est vide"""

class EnvoiEmailError(Exception):
    """levee quand une erreur d'envoie se produit"""



def traiter_commande(commande: dict) -> dict :
    commande_id = commande.get("id", "N/A") if isinstance(commande, dict) else "N/A"

    try:
        if not commande:
            raise CommandeVideError("Commande vide")
        
        if not commande["articles"]:
            raise ArticleVideError("Articles vides")
        try:
            envoyer_email(commande["client_email"])
        except ConnectionError as e:
            raise EnvoiEmailError("Erreur d'envoi") from e
        else:
            return {"status": "ok", "commande_id": commande['id']}
    finally:
        logger.info(f"Commande {commande_id!r} traitée")



def envoyer_email(client_email):
    if len(client_email) != 3:
        raise ConnectionError("Format email invalide")

sep = "*" * 80
#commande = {"id": 42, "articles": [...], "client_email": ["emetteur", "destinataire", "message"]}
commande_vide = {}
# test cas 0 commande vide
try:
    cmd_0 = traiter_commande(commande_vide)
    print(cmd_0)
except Exception as e:
    #print(e)
    print(e, "| cause: ", e.__cause__)
    
# output: 2026-09-10 15:17:11,097 - __main__ - INFO - Commande 'N/A' traitée + Commande vide | cause:  None
print(sep)

# test cas 1 commande avec articles vides
commande_articles_vides = {"id": 42, "articles": [], "client_email": ["emetteur", "destinataire", "message"]}
try:
    cmd_1 = traiter_commande(commande_articles_vides)
    print(cmd_1)
except Exception as e:
    #print(e)
    print(e, "| cause: ", e.__cause__)

# ouput: 2026-09-10 15:17:11,097 - __main__ - INFO - Commande 42 traitée + Articles vides | cause:  None
print(sep)

# test cas 2 commande avec email erreur
commande_emetteur_vide = {"id": 44, "articles": ["A_1", "A_2"], "client_email": ["emetteur", "message"]}
try:
    cmd_2 = traiter_commande(commande_emetteur_vide)
    print(cmd_2)
except Exception as e:
    print(e, "| cause: ", e.__cause__)
# ouput: 2026-09-10 15:17:11,098 - __main__ - INFO - Commande 44 traitée + Erreur d'envoi | cause:  Format email invalide
print(sep)

# test cas 3 commande normale
commande_normale = {"id": 43, "articles": ["A_1", "A_2"], "client_email": ["emetteur", "emetteur", "message"]}
try:
    cmd_3 = traiter_commande(commande_normale)
    print(cmd_3)
except Exception as e:
    print(e, "| cause: ", e.__cause__)
# ouput: 2026-09-10 15:17:11,098 - __main__ - INFO - Commande 43 traitée + {'status': 'ok', 'commande_id': 43}

#Exercice de conception maintenant, sans indice de ma part cette fois.

#Contexte : tu écris une fonction traiter_commande(commande: dict) -> dict pour un petit système e-commerce. commande ressemble
#  à {"id": 42, "articles": [...], "client_email": "..."}.
"""
Contraintes :
1. Si commande["articles"] est une liste vide, c'est une erreur métier — invente et lève l'exception personnalisée de ton choix.
2. Le traitement appelle une fonction externe simulée envoyer_email(client_email) qui peut lever une ConnectionError (panne réseau simulée). 
Si ça arrive, tu dois la traduire en une exception métier à toi, en conservant la cause d'origine de façon explicite.
3. Que la commande réussisse ou échoue, il faut logger f"Commande {id} traitée" — une seule fois, un seul endroit dans le code, garanti dans tous les cas.
4. Si tout se passe bien, retourne {"status": "ok", "commande_id": ...}.

Écris traiter_commande en entier (tu peux simuler envoyer_email toi-même, par exemple une fonction qui lève ConnectionError selon une condition simple
 pour pouvoir tester les deux chemins). Réfléchis à la structure avant d'écrire — dis-moi d'abord comment tu comptes organiser les try avant de coder,
   si tu veux valider l'approche avant d'écrire tout le code.
"""

"""architecture
foncton traiter_commande():
    try: global
        verifier d'abord si la commande n'est pas vide sinon lever une exception.
        verifier ensuite si la commande['articles] est une liste vide sinon lever une exception personalisee.
        try:
            appel de la fonction envoyer_email(client_email)
        except ConnectionError:
            raisse ExceptionMetier(...) from e

        else:
            retourne {"status": "ok", "commande_id": ...}
    finally:
        logger f"Commande {id} traitée"


fonction envoyer_email(client_email):
    - verifier l'emetteur ou le distinataire du mail, ou encore si le message contient..., sinon lever une exception
"""
