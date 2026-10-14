"""
On va maintenant voir le vrai intérêt pratique des générateurs — pas juste la syntaxe, mais pourquoi ça compte en vrai. 
Imagine que tu dois traiter un fichier de logs de 50 Go, ligne par ligne, pour compter combien contiennent le mot "ERROR". 
Écrirais-tu ça avec une liste (readlines() par exemple) ou avec un générateur ? Explique pourquoi, concrètement, en termes de mémoire.

"""
#  J'utiliserai un generateur car c'est plus economique en terme de memoire les lignes a compter seront traiter une a une suivant le dernier etat de l'iteration
# donc pas un space de 50 GO alloues d'un compte dans le cadre d'une liste.

def lire_erreurs(chemin_fichier):
    with open(chemin_fichier, "r") as f:
        for ligne in f:
            if "ERROR" in ligne:
                yield ligne

def  extraire_dates(lignes_erreur):
    for line in lignes_erreur:
        line = line.split()
        yield line[0]

test_chemin = ''
for date in extraire_dates(lire_erreurs(test_chemin)):
    print(date)

