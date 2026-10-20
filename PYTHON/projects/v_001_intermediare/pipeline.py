import json
from .extractions import extraction_csv, extraction_json, extraction_log
from .traduction import traduire_csv, traduire_json, traduire_log
from .exceptions import SourceInvalidError, DonneeInvalidError
from .validations import verification_presence, verification_format


sep = "***" * 30

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
