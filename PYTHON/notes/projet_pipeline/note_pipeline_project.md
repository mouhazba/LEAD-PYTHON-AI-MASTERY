# Documentation Technique & Guide du Pipeline de Données Multi-Sources

Ce document regroupe l'analyse d'amélioration, le code complet du pipeline ainsi que l'ensemble des jeux de données de test pour la validation.

---

## 🎯 PARTIE 1 : Récapitulatif des Améliorations & REX

### 1. Optimisation de la Regex (ex: `parser(ligne)`)

* **Problème :** Instancier `re.compile(...)` dans une fonction appelée à chaque ligne récompile le motif Regex à chaque itération, ce qui dégrade fortement les performances processeur.
* **Leçon & Piège à éviter :** Ne jamais compiler une Regex statique dans une boucle.
* **Solution :** Déclarer et pré-compiler toutes les Regex globales au démarrage du script.

### 2. Normalisation et Formatage des Exceptions

* **Problème :** Stocker directement des instances d'exceptions (`SourceInvalidError`, `JSONDecodeError`) crée des structures imbriquées complexes (`SourceInvalidError(SourceInvalidError(...))`) et fait planter la sérialisation JSON.
* **Leçon & Piège à éviter :** Ne pas conserver d'objets Python bruts dans les rapports d'erreurs.
* **Solution :** Convertir systématiquement le message d'erreur en chaîne de caractères (`str(e)`).

### 3. Séparation de la Validation (Présence vs Format)

* **Problème :** Mélanger la vérification des champs manquants (`None`) et la validation de format (Regex `@`, `.isdigit()`) déclenche des faux positifs ou des plantages (`NoneType` n'a pas de méthode `.match()`).
* **Leçon & Piège à éviter :** Valider le format avant de s'assurer que la valeur existe.
* **Solution :** Découper la validation en 2 étapes étanches : 
  1. `verification_presence` (la clé existe et n'est pas vide).
  2. `verification_format` (la valeur présente respecte le schéma).

### 4. Sérialisation JSON Propre

* **Problème :** Faire un `print()` brut d'un dictionnaire Python génère des guillemets simples `'` et une syntaxe non conforme aux standards JSON.
* **Leçon & Piège à éviter :** Confondre `str(dict)` en Python avec du vrai JSON.
* **Solution :** Utiliser `json.dumps(..., indent=2, ensure_ascii=False)` pour la sortie.
