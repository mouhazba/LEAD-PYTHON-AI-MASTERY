
Gemini
Nouvelle discussion
Rechercher dans les discussions
Images
Bibliothèque
Nouveau notebook
Impossible de se connecter
Actualiser
Conversation avec Gemini
Discussion temporaire
genere un .md de contenu bien formate:

Deep dive : dict vs defaultdict vs Counter



Je repars de ta session : le pattern if mot in dict: ... else: ... (Q5), ta découverte de defaultdict(int), et Counter(mots) avec most_common(). On va préciser exactement où ces trois outils divergent, parce que la note que tu as déjà ("Counter va encore plus loin que defaultdict") est correcte en pratique mais cache une différence de comportement plus fine qu'il faut connaître pour du code professionnel.



---



1. Mental model



┌─────────────┬────────────────────────────────────────────────────────────────────────────────────────────────┐

│ Outil │ Représentation mentale │

├─────────────┼────────────────────────────────────────────────────────────────────────────────────────────────┤

│ dict │ Une table de hachage générale : clé → valeur, aucune hypothèse sur ce que représentent les clés ou les valeurs. │

├─────────────┼────────────────────────────────────────────────────────────────────────────────────────────────┤

│ defaultdict │ Un dict avec une usine attachée (default_factory) qui fabrique une valeur à la volée quand une clé manque. │

├─────────────┼────────────────────────────────────────────────────────────────────────────────────────────────┤

│ Counter │ Un multiset (bag) — pas "un dict qui compte", mais une structure dont le concept même est le comptage d'éléments hashables. │

└─────────────┴────────────────────────────────────────────────────────────────────────────────────────────────┘



Le point que ta note passe sous silence : defaultdict(int) répond à "comment éviter de vérifier si d à "combien de fois chaque élément apparaît-il". Ce n'est pas la même question, même sidefaultdict(int) peut implémenter un compteur.



---



2. Comportement sur clé manquante — le vrai point technique



C'est ici que les trois outils se distinguent réellement, au niveau de __missing__.



from collections import defaultdict, Counter



d = {}

dd = defaultdict(int)

c = Counter()



d["x"] # KeyError

dd["x"] # 0 — et surtout : dd devient {"x": 0} !

c["x"] # 0 — mais c reste Counter() (vide)



- dict : KeyError. Pas d'ambiguïté.

- defaultdict : au premier accès manquant, Python appelle default_factory(), insère le résultat danC'est un accès qui mute la structure — même en lecture. Tu avais déjà noté ça pourcompteur["inconnu"].

- Counter : __missing__ retourne 0 sans rien insérer. Le code source de Counter (CPython) est litté



def __missing__(self, key):

return 0



Pas de self[key] = 0. Résultat :



"x" in dd # True après l'accès ci-dessus — pollution silencieuse

"x" in c # False — c n'a pas bougé



C'est la nuance que ta note ne devait pas gommer : Counter n'est pas un defaultdict(int) déguisé. I (c["mot"] sans KeyError) mais sans l'effet de bord d'insertion. C'est délibéré : un compteur nedevrait pas voir sa taille grandir juste parce qu'on a interrogé une clé absente.



.get() reste identique sur les trois : il ne passe jamais par __missing__, donc d.get("x"), dd.get("x"), c.get("x") renvoient tous None sans mutation. C'est cohérent avec ta note Q4 sur .get() vs KeyError.



---



3. Ce que Counter fait que defaultdict(int) ne fait pas



Ça vaut la peine d'être explicite, sinon on croit que Counter = "juste plus court à écrire" :



mots = ["chat", "chien", "chat", "oiseau", "chien", "chat"]

c = Counter(mots) # construction directe depuis un itérable

c.most_common(2) # [('chat', 3), ('chien', 2)]

c.update(["chat"]) # ADDITIONNE les comptes (dict.update REMPLACE les valeurs)

c.elements() # itérateur qui répète chaque élément `count` fois

c + Counter(["chat"]) # arithmétique de multiset (addition)

c - Counter(["oiseau"]) # soustraction — supprime les comptes ≤ 0



defaultdict(int) n'a aucune de ces opérations — tu devrais les réécrire à la main. À l'inverse, defaultdict(list) sait faire du grouping, ce que Counter ne fait pas du tout :



# Reprenons ton dict notes, groupé par mention (l'inverse de ton exercice)

notes = {"Awa": 14, "Moussa": 8, "Fatou": 17, "Ibrahima": 11, "Khadija": 6, "Cheikh": 15}



par_mention = defaultdict(list)

for nom, note in notes.items():

par_mention[mention(note)].append(nom)

# {"Bien": ["Awa", "Cheikh"], "Admis": ["Ibrahima"], ...}

Sans defaultdict, tu écrirais le même if cle not in d: d[cle] = [] que dans ton pattern Q5 — defaultdict généralise ce pattern à n'importe quelle valeur par défaut (list, set, int, une lambda, ou même un autre defaultdict pour du nesting), là où Counter est spécialisé et ne fait que compter.



---



4. Idiomatic Python — comment choisir



┌────────────────────────────────────────────────────────────────────────────────────────────┬─────

│ Besoin │ Outil idiomatique │

├────────────────────────────────────────────────────────────────────────────────────────────┼─────

│ Mapping général, accès explicite, erreur voulue sur clé absente │ dict + .get()/.setdefault() │

├────────────────────────────────────────────────────────────────────────────────────────────┼─────

│ Accumuler/grouper avec une valeur par défaut non triviale (list, set, structure imbriquée) │ defaultdict │ ───────────────────────────────────────────────────────────────────────────────────────────┼─────

│ L'intention du code est compter des occurrences │ Counter │ ───────────────────────────────────────────────────────────────────────────────────────────┴─────

Regle pratique : si tu te surprends à écrire defaultdict(int) uniquement pour compter, demande-toi mieux l'intention à un autre lecteur. Le nom du type documente le code.

4Complexité Les trois reposent sur la même table de hachage CPython :

- Lookup / insert / delete : O(1) en moyenne, O(n) au pire (collisions massives — rarissime, et l'iour amortir). C'est une garantie empirique, pas une garantie du langage — ne le présente jamaiscomme du O(1) garanti à un niveau bas. - Construction Counter(iterable) : O(n) où n = taille de l'itérable.

- most_common(k) : si k est donné, CPython utilise heapq.nlargest → O(n log k). Si tu appelles most_common() sans argument, c'est un tri complet → O(n log n). Donc most_common(1) est strictement moins coûteux que most_common()[0] sur une grande collection — précise k quand tu peux.

- Espace : O(n) sur le nombre de clés distinctes pour les trois.



---



6. Trade-offs



- dict : contrôle total, mais tout le boilerplate de gestion de clé manquante est à ta charge (ton if mot in dict).

- defaultdict : supprime ce boilerplate, mais au prix d'une insertion silencieuse sur simple lecturde de production : une faute de frappe sur une clé (d["chta"] au lieu de d["chat"]) ne lève plusd'erreur, elle crée une entrée fantôme. Ça peut fausser un comptage ou une taille de dict sans qu'aucune exception ne te prévienne.

- Counter : le plus lisible et le plus riche pour le comptage spécifiquement. Mal utilisé (comme diinduit le lecteur en erreur sur l'intention du code.



---



7. Erreurs courantes (au-delà de celles que tu as déjà notées)



Tu as déjà bien identifié defaultdict(int()) vs defaultdict(int), et la mutation-en-lecture. Deux pître :



a) Counter sur une string compte des caractères, pas des mots :



Counter("chat chien") # Counter({'c': 2, 'h': 3, 'a': 1, 't': 1, ' ': 1, 'i': 1, 'e': 1, 'n': 1})



Une string est itérable caractère par caractère — Counter compte ce qu'on lui donne à itérer. Pour bord tokeniser : Counter("chat chien".split()).



b) La soustraction de Counter élimine les comptes ≤ 0, contrairement à une soustraction manuelle su



Counter(a=3, b=1) - Counter(a=1, b=2) # Counter({'a': 2}) — 'b' disparaît, pas b: -1



Si tu t'attends à des comptes négatifs (par exemple pour détecter un déficit), Counter n'est pas le soustraire les dict sous-jacents à la main.



---



Pour vérifier ta compréhension



Petite prédiction, sans obligation d'y répondre tout de suite : que vaut bool("x" in c) juste après) sur un Counter vide, et pourquoi ça ne contredit pas ce qu'on vient de voir sur __missing__ ?



Observation pour le suivi de progression : tu maîtrises correctement .items(), les dict comprehensi manuel (Q5) — la distinction fine defaultdict vs Counter sur la mutation en lecture est un conceptencore théorique pour toi, à revoir en pratique si tu veux, par exemple sur un exercice de groupement (defaultdict(list)) séparé d'un exercice de comptage pur (Counter).



✻ Sautéed for 1m 40s · done 2:07 AM



※ recap: On approfondit dict vs defaultdict vs Counter (comportement sur clé manquante, complexité, pièges) dans ton apprentissage Python. Prochaine étape : tu réponds à la question de prédiction sur Counter vide et most_common(). (disable recaps in /config)

Synthèse des comportements
dict : Lève immédiatement une KeyError. Pas d'ambiguïté.

defaultdict : Au premier accès manquant (__getitem__), Python appelle default_factory(), insère le résultat dans le dictionnaire, puis le renvoie. C'est un accès en lecture qui muté la structure (effet de bord d'insertion silencieuse).

Counter : La méthode __missing__ du code source CPython est implémentée sans mutation :

Python
def __missing__(self, key):
    return 0
Aucun self[key] = 0 n'est exécuté.

Conséquences pratiques
Python
# Tester la présence d'une clé après une consultation :
"x" in dd   # True  --> Pollution silencieuse du defaultdict
"x" in c    # False --> Le Counter est resté pur
Remarque sur .get() : La méthode .get() ne passe jamais par __missing__ sur aucune des trois structures. Ainsi, d.get("x"), dd.get("x"), et c.get("x") renvoient tous None (ou la valeur par défaut spécifiée) sans provoquer aucune mutation.

3. Fonctionnalités comparées & Exemples
Ce que Counter apporte nativement
Counter fournit une API riche dédiée aux opérations sur les multisets que defaultdict(int) n'a pas :

Python
from collections import Counter

mots = ["chat", "chien", "chat", "oiseau", "chien", "chat"]

# 1. Construction directe depuis un itérable
c = Counter(mots)

# 2. Obtenir les K éléments les plus fréquents
print(c.most_common(2))  # [('chat', 3), ('chien', 2)]

# 3. Mettre à jour en ADDITIONNANT les comptes (vs dict.update qui remplace)
c.update(["chat"])  # 'chat' passe à 4

# 4. Itérateur qui répète chaque élément selon son compte
list(c.elements())  # ['chat', 'chat', 'chat', 'chat', 'chien', 'chien', 'oiseau']

# 5. Algèbre de multisets
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

print(c1 + c2)  # Addition : Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Soustraction (conserve uniquement > 0) : Counter({'a': 2})
Ce que defaultdict permet (Grouping & Nesting)
defaultdict excelle dans le regroupement avec des valeurs par défaut complexes (list, set, dict), ce que Counter ne peut pas faire :

Python
from collections import defaultdict

notes = {
    "Awa": 14, 
    "Moussa": 8, 
    "Fatou": 17, 
    "Ibrahima": 11, 
    "Khadija": 6, 
    "Cheikh": 15
}

def mention(note):
    if note >= 16: return "Très Bien"
    if note >= 14: return "Bien"
    if note >= 10: return "Admis"
    return "Ajourné"

# Regroupement par mention
par_mention = defaultdict(list)
for nom, note in notes.items():
    par_mention[mention(note)].append(nom)

# Resultat :
# defaultdict(<class 'list'>, {
#     'Bien': ['Awa', 'Cheikh'], 
#     'Ajourné': ['Moussa', 'Khadija'], 
#     'Très Bien': ['Fatou'], 
#     'Admis': ['Ibrahima']
# })
4. Idiomatic Python — Arbre de décision
Besoin	Structure recommandée	Justification
Mapping général avec validation explicite	dict + .get() / .setdefault()	Évite de masquer des erreurs de saisie de clés.
Groupement / Accumulation (list, set, structures imbriquées)	defaultdict	Supprime le boilerplate if key not in d: d[key] = [].
Comptage d'occurrences / Fréquences	Counter	Exprime clairement l'intention et fournit des outils statistiques.
Règle d'or : Si vous écrivez defaultdict(int) uniquement pour compter des fréquences, préférez Counter. Le nom du type communique directement l'intention du code aux autres développeurs.

5. Complexité Algorithmique (CPython)
Les trois structures reposent sur la table de hachage interne de CPython.

Opération	Complexité Temporelle (Moyenne)	Complexité Temporelle (Pire cas)	Remarques
Recherche / Insertion / Suppression	O(1)	O(n)	Le pire cas est dû aux collisions massives (très rare avec l'algorithme SipHash).
Counter(iterable)	O(n)	O(n)	n est le nombre total d'éléments dans l'itérable.
most_common(k)	O(nlogk)	O(nlogn)	Utilise heapq.nlargest si k est fourni. Si k=None, réalise un tri complet O(nlogn).
Complexité Spatiale	O(u)	O(u)	u est le nombre d'éléments uniques (clés distinctes).
Astuce de performance : Counter.most_common(1) est nettement plus performant sur de grandes collections que Counter.most_common()[0] car il évite le tri intégral de la structure.

6. Arbitrages & Trade-offs
                  ┌──────────────────────────────────────────┐
                  │           SÉLECTION DE STRUCTURE          │
                  └────────────────────┬─────────────────────┘
                                       │
                     L'objectif est-il de COMPTER ?
                                       │
                      ┌────────────────┴────────────────┐
                      │                                 │
                   [ OUI ]                           [ NON ]
                      │                                 │
             Utiliser Counter                 A-t-on besoin de
                                           valeurs par défaut auto ?
                                                        │
                                           ┌────────────┴────────────┐
                                        [ OUI ]                   [ NON ]
                                           │                         │
                                 Utiliser defaultdict          Utiliser dict
dict : Contrôle total et sécurité, mais nécessite un code plus verbeux (boilerplate) pour gérer les absences de clés.

defaultdict : Élimine la verbosité, mais crée un risque de pollution d'état silencieuse : une faute d'orthographe dans une clé (dd["chta"] au lieu de dd["chat"]) n'est pas signalée et crée une entrée parasite à 0.

Counter : Excellente lisibilité et fonctions dédiées au comptage. Utile sans modifier la structure en cas de simple requête de clé absente.

7. Pièges et Erreurs Classiques
a) Counter sur une chaîne de caractères vs une liste de mots
Une chaîne (str) est un itérable de caractères. Pour compter des mots, il faut préalablement la découper :

Python
texte = "chat chien chat"

# ❌ ERREUR : compte les caractères
c_bad = Counter(texte)
# Counter({'c': 3, 'h': 3, 'a': 2, 't': 2, ' ': 2, 'i': 1, 'e': 1, 'n': 1})

# ✅ CORRECT : compte les mots
c_good = Counter(texte.split())
# Counter({'chat': 2, 'chien': 1})
b) Soustraction de Counter et valeurs négatives
La soustraction d'opérateurs de Counter masque et élimine automatiquement les résultats négatifs ou nuls :

Python
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

diff = c1 - c2  
print(diff)  # Counter({'a': 2})  <-- 'b' a disparu car 1 - 2 = -1 <= 0 !

# Si vous voulez conserver des décomptes négatifs, utilisez .subtract() :
c1.subtract(c2)
print(c1)    # Counter({'a': 2, 'b': -1})
8. Question de vérification & Auto-évaluation
Prédiction
Que vaut l'expression bool("x" in c) immédiatement après avoir exécuté _ = c["x"] sur un Counter vide ?

Réponse : False

Explication :

Bien que c["x"] ait renvoyé 0 sans lever de KeyError, l'implémentation de Counter.__missing__ renvoie uniquement 0 sans insérer "x" dans le dictionnaire interne (self[key] = 0 n'est pas exécuté). Ainsi, la clé "x" n'existe pas dans le container, et l'opérateur "x" in c (qui vérifie la présence de la clé, pas la valeur) renvoie False.

Write the clean markdown file
file_name = "dict_vs_defaultdict_vs_counter.md"
with open(file_name, "w", encoding="utf-8") as f:
f.write(clean_md_content)

print(f"File saved successfully: {file_name}")


```text?code_stdout&code_event_index=1
File saved successfully: dict_vs_defaultdict_vs_counter.md

Votre fichier Markdown avec une mise en page soignée, un formatage rigoureux et des tableaux/blocs de code nettoyés a été généré avec succès.

Icône MD
dict_vs_defaultdict_vs_counter
 MD 
Ouvert
Aperçu des améliorations apportées dans ce document :
Nettoyage et structuration des contenus :

Correction des fragments de texte tronqués ou déformés.

Ajout d'un encadré de synthèse initial et réorganisation progressive de la démarche pédagogique.

Standardisation Markdown & Graphiques :

Tableaux comparatifs enrichis (Mental Model, Matrice d'idiomes, Complexités algorithmiques).

Schéma décisionnel ASCII pour l'arbitrage entre les trois structures.

Mise en valeur du code Python :

Blocs de code typés (````python) avec annotations explicites sur la mutation silencieuse et les mécanismes missing`.

Séparation claire des pièges classiques (découpage de chaînes, soustraction positive vs .subtract()).

Section interactive / Auto-évaluation :

Intégration de la question de prédiction avec son bloc explicatif sous balise déroulante (<details>).




Gemini est une IA et peut se tromper.

Analyse…
# Deep Dive : `dict` vs `defaultdict` vs `Counter`

> **Note de cadrage :** Analyse comparative approfondie des structures de données associatives en Python (`dict`, `collections.defaultdict`, et `collections.Counter`). Ce guide précise les divergences comportementales, les mécanismes internes (`__missing__`), la complexité algorithmique et les cas d'usage professionnels.

---

## 1. Mental Model & Concepts

| Outil | Représentation mentale | Cas d'usage fondamental |
| :--- | :--- | :--- |
| **`dict`** | Table de hachage générale : clé $\rightarrow$ valeur. Aucune hypothèse préétablie sur ce que représentent les clés ou les valeurs. | Mapping général, stockage d'entités, accès explicite. |
| **`defaultdict`** | Un `dict` augmenté d'une usine (*default_factory*) qui génère automatiquement une valeur par défaut lorsqu'une clé est absente. | Regroupement (`list`, `set`), accumulation d'objets complexes. |
| **`Counter`** | Un **multiset** (sac) mathématique — pas un simple « dict qui compte », mais une structure dédiée à la mesure de fréquences d'éléments hashables. | Dénombrement d'occurrences, histogrammes, opérations de sacs. |

### La nuance clé
`defaultdict(int)` répond à la question : *"Comment éviter de vérifier l'existence d'une clé avant d'incrémenter ?"*  
`Counter` répond à la question : *"Combien de fois chaque élément apparaît-il dans cette collection ?"*

Bien que `defaultdict(int)` puisse implémenter un compteur, l'intention sémantique et le comportement sous-jacent sont distincts.

---

## 2. Comportement sur clé manquante : Le mécanisme `__missing__`

C'est au niveau de la méthode interne `__missing__` que les trois structures se distinguent fondamentalement.

```python
from collections import defaultdict, Counter

d = {}
dd = defaultdict(int)
c = Counter()

# --- CAS 1 : dict standard ---
try:
    _ = d["x"]
except KeyError:
    print("dict: lève une exception KeyError")

# --- CAS 2 : defaultdict ---
_ = dd["x"]  # Retourne 0, MAIS insère la clé !
print(f"defaultdict après accès : {dd}")  # Output: defaultdict(<class 'int'>, {'x': 0})

# --- CAS 3 : Counter ---
_ = c["x"]   # Retourne 0, SANS modifier le Counter !
print(f"Counter après accès     : {c}")   # Output: Counter()
```

### Synthèse des comportements

* **`dict`** : Lève immédiatement une `KeyError`. Pas d'ambiguïté.
* **`defaultdict`** : Au premier accès manquant (`__getitem__`), Python appelle `default_factory()`, insère le résultat dans le dictionnaire, puis le renvoie. **C'est un accès en lecture qui muté la structure** (effet de bord d'insertion silencieuse).
* **`Counter`** : La méthode `__missing__` du code source CPython est implémentée sans mutation :
  ```python
  def __missing__(self, key):
      return 0
  ```
  Aucun `self[key] = 0` n'est exécuté.

### Conséquences pratiques

```python
# Tester la présence d'une clé après une consultation :
"x" in dd   # True  --> Pollution silencieuse du defaultdict
"x" in c    # False --> Le Counter est resté pur
```

> **Remarque sur `.get()` :** La méthode `.get()` ne passe **jamais** par `__missing__` sur aucune des trois structures. Ainsi, `d.get("x")`, `dd.get("x")`, et `c.get("x")` renvoient tous `None` (ou la valeur par défaut spécifiée) sans provoquer aucune mutation.

---

## 3. Fonctionnalités comparées & Exemples

### Ce que `Counter` apporte nativement

`Counter` fournit une API riche dédiée aux opérations sur les multisets que `defaultdict(int)` n'a pas :

```python
from collections import Counter

mots = ["chat", "chien", "chat", "oiseau", "chien", "chat"]

# 1. Construction directe depuis un itérable
c = Counter(mots)

# 2. Obtenir les K éléments les plus fréquents
print(c.most_common(2))  # [('chat', 3), ('chien', 2)]

# 3. Mettre à jour en ADDITIONNANT les comptes (vs dict.update qui remplace)
c.update(["chat"])  # 'chat' passe à 4

# 4. Itérateur qui répète chaque élément selon son compte
list(c.elements())  # ['chat', 'chat', 'chat', 'chat', 'chien', 'chien', 'oiseau']

# 5. Algèbre de multisets
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

print(c1 + c2)  # Addition : Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Soustraction (conserve uniquement > 0) : Counter({'a': 2})
```

### Ce que `defaultdict` permet (Grouping & Nesting)

`defaultdict` excelle dans le regroupement avec des valeurs par défaut complexes (`list`, `set`, `dict`), ce que `Counter` ne peut pas faire :

```python
from collections import defaultdict

notes = {
    "Awa": 14, 
    "Moussa": 8, 
    "Fatou": 17, 
    "Ibrahima": 11, 
    "Khadija": 6, 
    "Cheikh": 15
}

def mention(note):
    if note >= 16: return "Très Bien"
    if note >= 14: return "Bien"
    if note >= 10: return "Admis"
    return "Ajourné"

# Regroupement par mention
par_mention = defaultdict(list)
for nom, note in notes.items():
    par_mention[mention(note)].append(nom)

# Resultat :
# defaultdict(<class 'list'>, {
#     'Bien': ['Awa', 'Cheikh'], 
#     'Ajourné': ['Moussa', 'Khadija'], 
#     'Très Bien': ['Fatou'], 
#     'Admis': ['Ibrahima']
# })
```

---

## 4. Idiomatic Python — Arbre de décision

| Besoin | Structure recommandée | Justification |
| :--- | :--- | :--- |
| **Mapping général** avec validation explicite | `dict` + `.get()` / `.setdefault()` | Évite de masquer des erreurs de saisie de clés. |
| **Groupement / Accumulation** (`list`, `set`, structures imbriquées) | `defaultdict` | Supprime le boilerplate `if key not in d: d[key] = []`. |
| **Comptage d'occurrences / Fréquences** | `Counter` | Exprime clairement l'intention et fournit des outils statistiques. |

> **Règle d'or :** Si vous écrivez `defaultdict(int)` uniquement pour compter des fréquences, préférez `Counter`. Le nom du type communique directement l'intention du code aux autres développeurs.

---

## 5. Complexité Algorithmique (CPython)

Les trois structures reposent sur la table de hachage interne de CPython.

| Opération | Complexité Temporelle (Moyenne) | Complexité Temporelle (Pire cas) | Remarques |
| :--- | :--- | :--- | :--- |
| **Recherche / Insertion / Suppression** | $\mathcal{O}(1)$ | $\mathcal{O}(n)$ | Le pire cas est dû aux collisions massives (très rare avec l'algorithme SipHash). |
| **`Counter(iterable)`** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | $n$ est le nombre total d'éléments dans l'itérable. |
| **`most_common(k)`** | $\mathcal{O}(n \log k)$ | $\mathcal{O}(n \log n)$ | Utilise `heapq.nlargest` si $k$ est fourni. Si $k=None$, réalise un tri complet $\mathcal{O}(n \log n)$. |
| **Complexité Spatiale** | $\mathcal{O}(u)$ | $\mathcal{O}(u)$ | $u$ est le nombre d'éléments uniques (clés distinctes). |

*Astuce de performance :* `Counter.most_common(1)` est nettement plus performant sur de grandes collections que `Counter.most_common()[0]` car il évite le tri intégral de la structure.

---

## 6. Arbitrages & Trade-offs

```
                  ┌──────────────────────────────────────────┐
                  │           SÉLECTION DE STRUCTURE          │
                  └────────────────────┬─────────────────────┘
                                       │
                     L'objectif est-il de COMPTER ?
                                       │
                      ┌────────────────┴────────────────┐
                      │                                 │
                   [ OUI ]                           [ NON ]
                      │                                 │
             Utiliser Counter                 A-t-on besoin de
                                           valeurs par défaut auto ?
                                                        │
                                           ┌────────────┴────────────┐
                                        [ OUI ]                   [ NON ]
                                           │                         │
                                 Utiliser defaultdict          Utiliser dict
```

* **`dict`** : Contrôle total et sécurité, mais nécessite un code plus verbeux (*boilerplate*) pour gérer les absences de clés.
* **`defaultdict`** : Élimine la verbosité, mais crée un risque de **pollution d'état silencieuse** : une faute d'orthographe dans une clé (`dd["chta"]` au lieu de `dd["chat"]`) n'est pas signalée et crée une entrée parasite à 0.
* **`Counter`** : Excellente lisibilité et fonctions dédiées au comptage. Utile sans modifier la structure en cas de simple requête de clé absente.

---

## 7. Pièges et Erreurs Classiques

### a) `Counter` sur une chaîne de caractères vs une liste de mots
Une chaîne (`str`) est un itérable de caractères. Pour compter des mots, il faut préalablement la découper :

```python
texte = "chat chien chat"

# ❌ ERREUR : compte les caractères
c_bad = Counter(texte)
# Counter({'c': 3, 'h': 3, 'a': 2, 't': 2, ' ': 2, 'i': 1, 'e': 1, 'n': 1})

# ✅ CORRECT : compte les mots
c_good = Counter(texte.split())
# Counter({'chat': 2, 'chien': 1})
```

### b) Soustraction de `Counter` et valeurs négatives
La soustraction d'opérateurs de `Counter` masque et élimine automatiquement les résultats négatifs ou nuls :

```python
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

diff = c1 - c2  
print(diff)  # Counter({'a': 2})  <-- 'b' a disparu car 1 - 2 = -1 <= 0 !

# Si vous voulez conserver des décomptes négatifs, utilisez .subtract() :
c1.subtract(c2)
print(c1)    # Counter({'a': 2, 'b': -1})
```

---

## 8. Question de vérification & Auto-évaluation

### Prédiction
Que vaut l'expression `bool("x" in c)` immédiatement après avoir exécuté `_ = c["x"]` sur un `Counter` vide ?

<details>
<summary>👉 Cliquez pour afficher la réponse et l'explication</summary>

**Réponse :** `False`

**Explication :**  
Bien que `c["x"]` ait renvoyé `0` sans lever de `KeyError`, l'implémentation de `Counter.__missing__` renvoie uniquement `0` sans insérer `"x"` dans le dictionnaire interne (`self[key] = 0` n'est pas exécuté). Ainsi, la clé `"x"` n'existe pas dans le container, et l'opérateur `"x" in c` (qui vérifie la présence de la clé, pas la valeur) renvoie `False`.

</details>
dict_vs_defaultdict_vs_counter.md
Affichage de dict_vs_defaultdict_vs_counter.md.