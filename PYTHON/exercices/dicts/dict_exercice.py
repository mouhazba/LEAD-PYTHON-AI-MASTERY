#T u disposes du dictionnaire suivant, associant le nom de chaque étudiant à sa note sur 20 :
sep = "---" * 50

notes = {
    "Awa": 14,
    "Moussa": 8,
    "Fatou": 17,
    "Ibrahima": 11,
    "Khadija": 6,
    "Cheikh": 15
}

# Ta mission :
"""
Écris une fonction etudiants_admis(notes, seuil) qui :

1. Parcourt le dictionnaire notes en utilisant .items().
2. Construit et retourne un nouveau dictionnaire (via une dict comprehension) contenant uniquement les étudiants dont la note est supérieure ou égale 
    au seuil passé en paramètre.
3. Dans ce nouveau dictionnaire, chaque valeur ne doit pas être la note brute, mais la mention associée selon ce barème :
  - note ≥ 16 → "Très bien"
  - 14 ≤ note < 16 → "Bien"
  - seuil ≤ note < 14 → "Admis"

Exemple d'appel attendu :
etudiants_admis(notes, 10)
devrait retourner quelque chose comme :
{"Awa": "Bien", "Fatou": "Très bien", "Ibrahima": "Admis", "Cheikh": "Bien"}

Prends ton temps — j'attends ta solution.

"""
print(sep)
def etudiants_admis(notes, seuil):
    admis = {nom: note for nom, note in notes.items() if  note >= seuil}
    for nom, valeur in admis.items():
        if seuil <= valeur and valeur < 14:
            admis[nom] = "Admis"
        elif 14 <= valeur and valeur < 16:
            admis[nom] = "Bien"
        elif valeur >= 16:
            admis[nom] = "Tres bien"
    return admis

print("Solution simple")
print(etudiants_admis(notes, 10))
print(sep)

# ============ solution amelioree =======================
def mention(note):
    if note < 14:
        return "Admis"
    elif note < 16:
        return "Bien"
    else:
        return "Tres bien"

def etudiants_admis_bis(notes, seuil):
    return {
        nom: mention(note)
        for nom, note in notes.items()
        if note >= seuil
    }

print("solution avec une comprehension de dict")
print(etudiants_admis_bis(notes, 10))
print(sep)

# Option B — tout inline, avec des ternaires imbriqués
def etudiants_admis(notes, seuil):
    return {
        nom: ("Admis" if note < 14 else "Bien" if note < 16 else "Tres bien")
        for nom, note in notes.items()
        if note >= seuil
    }