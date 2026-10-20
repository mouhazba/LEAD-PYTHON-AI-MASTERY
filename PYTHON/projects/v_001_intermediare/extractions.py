from .parser import parser
from .exceptions import SourceInvalidError
import json
import csv


def extraction_csv(chemin_fichier):
    try:
        with open(chemin_fichier, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            une_ligne_lue = False
            for numero_ligne, ligne in enumerate(reader, start=1):
                une_ligne_lue = True
                try:
                    enregistrement = parser(ligne)   
                except SourceInvalidError as e:
                    yield(False, numero_ligne, str(e.erreur))
                except csv.Error as e:
                    yield(False, numero_ligne, f"Erreur CSV {e}")
                else:
                    yield(True, numero_ligne, enregistrement)
            if not une_ligne_lue:
                raise SourceInvalidError("Fichier Vide")
    except OSError:
        raise SourceInvalidError("Fichier CSV Introuvable")
    except ValueError:
        raise SourceInvalidError("Fichier CSV corrompu")

# Json case
def extraction_json(chemin_fichier):
    try:
        with open(chemin_fichier, encoding="utf-8") as f:
            une_ligne_lue = False
            for numero_ligne, ligne in enumerate(f, start=1):
                une_ligne_lue = True
                try:
                    enregistrement = parser(json.loads(ligne))
                except json.JSONDecodeError as e:
                    yield(False, numero_ligne, f"JSONDecodeError('{e.msg}': line{e.lineno} column{e.colno} (char {e.pos}))")
                except SourceInvalidError as e:
                    yield(False, numero_ligne, str(e.erreur))
                else:
                    yield(True, numero_ligne, enregistrement)
            if not une_ligne_lue:
                raise SourceInvalidError("Fichier Vide")
    except OSError:
        raise SourceInvalidError("Fichier Json Introuvable")
    except ValueError:
        raise SourceInvalidError("Fichier Log corrompu")



def extraction_log(chemin_fichier):
    try:
        with open(chemin_fichier, encoding="utf-8") as f:
            une_ligne_lue = False
            for numero_ligne, ligne in enumerate(f, start=1):
                une_ligne_lue = True
                try:
                    enregistrement = parser(ligne)
                except SourceInvalidError as e:
                    yield(False, numero_ligne, str(e.erreur))
                else:
                    yield(True, numero_ligne, enregistrement)
            if not une_ligne_lue:
                raise SourceInvalidError("Fichier Vide")
    except OSError:
        raise SourceInvalidError("Fichier Log Introuvable")
    except ValueError:
        raise SourceInvalidError("Fichier Log corrompu")

