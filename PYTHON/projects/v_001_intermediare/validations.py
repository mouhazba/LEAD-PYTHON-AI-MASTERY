from .exceptions import DonneeInvalidError
import re


def verification_presence(enregistrement):    
    numero_ligne = enregistrement[0]
    donnee = enregistrement[1]
    donnee_erreur = []

    for cle, val in donnee.items():
        if val is None or not isinstance(val, str) or not val.strip():
            donnee_erreur.append(cle)

    if len(donnee_erreur) == 1:
        raise DonneeInvalidError(f"{donnee_erreur[0]} a une valeur incorrect")
    elif len(donnee_erreur) > 1:
        raise DonneeInvalidError(f"les cles {donnee_erreur} ont des valeurs incorrectes")
    else:
        return enregistrement

def verification_format(enregistrement):
    email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    #numero_ligne = enregistrement[0]
    donnee = enregistrement[1]
    donnee_erreur = []

    for cle, val in donnee.items():
        if val is not None and not isinstance(val, str):
            donnee_erreur.append(cle)

        elif cle == "email" and (not  email_pattern.match(val)):
            donnee_erreur.append(cle)
        elif cle == "id" and not val.isdigit():
            donnee_erreur.append(cle)

    if len(donnee_erreur) == 1:
        raise DonneeInvalidError(f"{donnee_erreur[0]} a un format incorrect")
    elif len(donnee_erreur) > 1:
        raise DonneeInvalidError(f"les valeurs {donnee_erreur} ont des formats incorrects")
    else:
        return enregistrement