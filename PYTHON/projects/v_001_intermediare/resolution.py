import csv
import json
from pathlib import Path
import re


sources_folder = Path(__file__).resolve().parent/"sources"

CSV_PATH= sources_folder/"srce.csv"
JSON_PATH= sources_folder/"srce.json"
LOG_PATH= sources_folder/"srce.log"

PATRON_LOG = re.compile(
    r"^\[(?P<date>[^\]]+)\]\s*"          # Date : tolère [] (vide)
    r"(?P<event>\w*)\s*"                 # Event : tolère chaîne vide
    r"(?:id=(?P<id>\d*))?\s*"            # 'id=' optionnel
    r'(?:name="(?P<name>[^"]*)")?\s*'    # 'name="..."' optionnel
    r"(?:email=(?P<email>\S*))?$"        # 'email=' optionnel
)

class AppError(Exception):
    "levee a la frontiere commune"

class SourceInvalidError(AppError):
    def __init__(self, source_erreur):
        super().__init__(source_erreur)
        self.erreur = str(source_erreur) # a voir pourquoi

class DonneeInvalidError(AppError):
    def __init__(self, erreur_donnee):
        super().__init__(erreur_donnee)
        self.erreur_donnee = str(erreur_donnee)

def parser(ligne):
    if isinstance(ligne, dict):
        if any(v is None for v in ligne.values()): # any(v is None for v in ligne.values()) exception colonne cvs absente=None
            raise SourceInvalidError("Ligne inexploitable")
        return ligne
    
    if isinstance(ligne, str):
        match = PATRON_LOG.match(ligne)
        if match is None:
            raise SourceInvalidError("Ligne inexploitable")
        if match:
            return match.groupdict()
        
    raise SourceInvalidError("Type de ligne non supporté")

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


sep = "***" * 30

def traduire_csv(enregistrement, num):
    id = enregistrement.get("id")
    nom = enregistrement.get("nom")
    email = enregistrement.get("email")
    return num, {"id": id if id else None, "nom": nom if nom else None, "email": email if email else None}

def traduire_json(enregistrement, num):
    id = enregistrement.get("user_id")
    nom = enregistrement.get("full_name")
    email = enregistrement.get("contact")
    return num, {"id": id if id else None, "nom": nom if nom else None, "email": email if email else None}
    
def traduire_log(enregistrement, num):
    id = enregistrement.get("id")
    nom = enregistrement.get("name")
    email = enregistrement.get("email")
    return num, {"id": id if id else None , "nom": nom if nom else None, "email": email if email else None}

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
    numero_ligne = enregistrement[0]
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

EXTRACTEURS_FILE = {
    "csv": extraction_csv,
    "json": extraction_json,
    "log": extraction_log,
}
TRADUCTEURS_FILE = {
    "csv": traduire_csv,
    "json": traduire_json,
    "log": traduire_log,
}

def extracteur_path(source):
    extension_propre = source.suffix.lstrip(".")
    extracteur = EXTRACTEURS_FILE.get(extension_propre)
    traducteur = TRADUCTEURS_FILE.get(extension_propre)
    if extracteur is None:
        raise SourceInvalidError(f"Format non supporté : .{extension_propre}")
    return extracteur, traducteur, extension_propre

def traitement(source, ids_vus=None):
    if ids_vus is None:
        ids_vus = set()
    try:
        lignes_correctes = []
        lignes_incorrectes = []
        doublons_ignores = 0

        try:
            extracteur, traducteur, extension = extracteur_path(source)
        except SourceInvalidError as e:
            print(f"Erreur d'extraction: {e}")
            return
        
        else:
            for ok, num, ligne in extracteur(source):
                
                if ok:
                    trd = traducteur(ligne, num)
                    try:
                        verification_val = verification_presence(trd)
                        vf_format = verification_format(verification_val)
                        enregistrement = vf_format[1]
                        num_ligne = vf_format[0]
                        id_enregistrement = enregistrement.get("id")
                        if id_enregistrement in ids_vus:
                            doublons_ignores += 1
                        else:
                            ids_vus.add(id_enregistrement)
                            lignes_correctes.append({num_ligne: enregistrement})
                    except DonneeInvalidError as e:
                        lignes_incorrectes.append({num: e.erreur_donnee})
                else:
                    lignes_incorrectes.append({num: ligne})

            count_corrects = len(lignes_correctes)
            count_incorrects = len(lignes_incorrectes)
            rapport_incident = count_corrects/count_incorrects if count_incorrects != 0 else count_corrects
                
    
            rapport_par_source = [
                {extension: 
                 {
                    "valides":
                        {
                            "nombre": count_corrects,
                            "enregistrement(s)": lignes_correctes
                        },
                    "incident(s)":
                        {
                            "nombre": count_incorrects,
                            "ligne(s)": lignes_incorrectes
                        },
                    "rapport valides/incidents": format(rapport_incident, ".2f"),
                    "stats":
                        {
                            "totale_valide": count_corrects,
                            "totale_invalide": count_incorrects,
                            "doublons_ignores": doublons_ignores
    
                        }
                }
            }
            ]
            
            print(json.dumps(rapport_par_source, indent=2, ensure_ascii=False))
    
            print(sep)
        
    except SourceInvalidError as e:
        print(f"Erreur globale source : {e}")

def main():
    ids_traites = set()
    print(f"Enregistrements valides et normalises par source:")
    traitement(JSON_PATH, ids_traites)
    traitement(CSV_PATH, ids_traites)
    traitement(LOG_PATH, ids_traites)
print(sep)
if __name__ == "__main__":
    main()


"""ouput


"""