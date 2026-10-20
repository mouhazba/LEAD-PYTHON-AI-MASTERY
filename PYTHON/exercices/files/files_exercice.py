"""
Exercice

Écris une petite fonction compter_mots(chemin) qui lit un fichier texte ligne par ligne (pas read()), 
compte le nombre total de mots (séparés par des espaces), et retourne ce total. Puis écris une seconde fonction ecrire_rapport(chemin_sortie, 
stats) qui prend un dict {"lignes": int, "mots": int} et écrit un petit rapport texte dans un nouveau fichier,
 une statistique par ligne, avec les \n correctement placés.

"""
from pathlib import Path

DIR_FILE = Path(__file__).resolve().parent
LOG = DIR_FILE/"srce.log"
LOG_SORTIE = DIR_FILE/"sortie.log"

def compter_mots(chemin):
    nombre_mots = 0
    nombre_lignes = 0
    with open(chemin, encoding="utf-8") as f:
        while line:= f.readline():
            nombre_lignes += 1
            line_cleaned = line.strip().split()
            nombre_mots += len(line_cleaned)
    
    return{"lignes": nombre_lignes, "mots": nombre_mots}


def ecrire_rapport(chemin_sortie, stats):
    nlignes = stats.get("lignes")
    nmots = stats.get("mots")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write(f"Nombre de lignes : {nlignes}\n")
        f.write(f"Nombre de mots : {nmots}\n")

if LOG.exists():
    stat = compter_mots(LOG)
    ecrire_rapport(LOG_SORTIE, stat)
    print("Complete process")
else:
    print("File not found")

"""ouput
process complete

et contenu de sortie.log
Nombre de lignes : 8
Nombre de mots : 45
"""