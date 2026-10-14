# Conception — Pipeline de normalisation d'événements hétérogènes

Document vivant : mis à jour à chaque itération de conception, pas figé.
Dernière mise à jour : 2026-09-26 (skill `architecture_review`).

---

## 1. Étapes du pipeline

| Étape | Responsabilité | Échec → |
|---|---|---|
| **1. Extraction** | Lire et parser chaque source dans son propre format (CSV, JSONL, log texte) | `SourceInvalideError` (technique) si la ligne/le fichier est illisible |
| **2. Mise en forme commune** | Extraire uniquement les champs utiles (`id`, `nom`, `email`) et les regrouper en dict au format commun | `DonneeInvalidError` (métier) si un champ obligatoire est absent |
| **3. Validation métier** | Vérifier la conformité des champs présents (ex : format d'email) | `DonneeInvalidError` (métier) si un champ est invalide |
| **4. Déduplication** | Filtrer les enregistrements déjà vus (par `id`, via un `set` d'ids rencontrés) | Pas d'exception — filtrage silencieux, compté à part dans les stats |

## 2. Hiérarchie d'exceptions

AppError(Exception)                 racine commune
├── SourceInvalideError             branche technique — échec d'extraction
└── DonneeInvalidError              branche métier — une seule classe,
        attribut `champ` (quel champ), utilisée pour absence ET invalidité

### Justifications retenues

- **Une seule classe `DonneeInvalidError`** plutôt qu'une classe par champ
  (`EmailInvalideError`, `NomInvalideError`, ...) : dans ce pipeline,
  `except EmailInvalideError` et `except NomInvalideError` finiraient de
  toute façon au même endroit (logger `id` + raison, continuer). La
  distinction de type n'ajoutait aucune décision différente en aval — smell
  "abstraction prématurée" évité. Si une règle métier future différenciait
  vraiment le traitement selon le champ, séparer les classes se
  justifierait à ce moment-là, pas avant.
- **Doublon ≠ erreur de donnée** : l'enregistrement lui-même est valide ;
  ce n'est qu'un état par rapport à l'historique du lot (dépend de ce qui a
  déjà été vu, pas de l'enregistrement isolé). Jugé non suspect dans ce
  contexte → filtré silencieusement plutôt que remonté dans le rapport
  d'incidents, qui reste réservé aux données réellement invalides.

## 3. Stratégie de gestion globale

**Collecter-continuer** partout : une erreur sur un enregistrement
(technique ou métier) est loguée et n'interrompt jamais le traitement du
reste du lot.

## 4. Sorties attendues

1. Enregistrements valides et normalisés (déduplication faite).
2. Rapport d'incidents : `(id, champ, raison)` pour chaque enregistrement
   rejeté par `DonneeInvalidError` ou `SourceInvalideError`.
3. Statistiques agrégées : valides / invalides par source, doublons
   ignorés.

## 5. Principe directeur

Ne mobiliser un concept/mécanisme Python (generator, decorator, classe,
hiérarchie...) que s'il résout un problème réel identifié à cette étape —
jamais pour démontrer qu'il est maîtrisé. Choix de mécanismes concrets
traités étape par étape, dans l'ordre de construction du pipeline.

## 6. Granularité

"Granularité" = à quel niveau/à quelle échelle une opération ou une décision s'applique. Ici, concrètement : est-ce que "réussite" ou "échec" se décide par fichier entier (tout ou rien : soit tout le fichier passe, soit rien) ou par ligne individuelle (chaque ligne réussit ou échoue indépendamment des autres) ?

## 7. Étape 1 (Extraction) — statut : terminée, décisions d'implémentation

Trois générateurs (`extraction_csv`, `extraction_json`, `extraction_log`),
tous construits sur le même squelette : ouvrir le fichier, itérer
ligne par ligne, tenter de parser chaque ligne, `yield (True, dict)` en
cas de succès ou `yield (False, SourceInvalidError(...))` en cas
d'échec **de cette ligne précise** (jamais `raise` pour une ligne —
casserait la granularité, voir section 6). Seules les pannes au niveau du
fichier entier (introuvable, vide) utilisent `raise` directement.

Décisions prises pendant l'implémentation :

- **Source B passée de "tableau JSON" à vrai JSONL** (une ligne = un objet
  JSON complet et indépendant, sans `[]` ni virgules de fin de ligne).
  Raison : un tableau JSON (`json.load`) est un document unique — une
  seule erreur de syntaxe n'importe où dans le fichier fait échouer
  **tout** le fichier, aucune granularité ligne par ligne possible avec le
  module `json` standard sur ce format. Le JSONL permet `json.loads(ligne)`
  par ligne, avec la même résilience que CSV/logs.
- **`csv.DictReader` plutôt que `csv.reader` + indexation positionnelle** :
  élimine l'écriture en dur des noms de colonnes et le `next(reader)`
  manuel pour sauter l'en-tête.
- **Détection explicite du fichier vide** : itérer sur un fichier/reader
  vide ne lève aucune exception nativement (la boucle `for` s'exécute
  zéro fois, ce n'est pas une erreur pour Python) — il faut un indicateur
  explicite (`une_ligne_lue = False`, mis à `True` dans la boucle, vérifié
  après) pour transformer ce cas en `SourceInvalidError` levée.
- **`parser()` ne valide plus le contenu métier** (ex: `len() != 4` sur un
  dict) — seulement la *parsabilité structurelle* (peut-on produire un
  enregistrement du tout ?). La vérification des champs métier (id/nom/
  email présents) est laissée à l'étape 2, pour éviter le travail en
  double entre étapes. Exception : les dicts (CSV via `DictReader`, JSON)
  gardent un contrôle minimal (`any(v is None...) or len(ligne) < 4`) car
  CSV (valeurs `None` sur colonnes manquantes) et JSON (clé carrément
  absente) ont des défauts de forme différents qui ne sont pas de la
  validation métier à proprement parler.
- **`LingeInvalidError` abandonnée** : retenue puis supprimée — elle était
  systématiquement reconvertie en `SourceInvalidError` générique dès
  qu'attrapée, donc n'apportait aucune décision différente en aval
  (même raisonnement que pour la fusion des exceptions de champ en
  section 2).
- Nettoyage de code mort trouvé en cours de route : `except StopIteration`
  (ne peut jamais se déclencher sur une itération `for` normale, legacy
  du `next(reader)` manuel abandonné avec `DictReader`), et
  `except json.JSONDecodeError` resté par copier-coller dans
  `extraction_log` (qui n'utilise jamais le module `json`).

## 8. Étape 2 (Mise en forme commune) — statut : terminée, décisions d'implémentation

Trois fonctions de traduction dédiées (`traduire_csv`, `traduire_json`,
`traduire_log`), chacune pur mapping (aucun jugement de validité) —
`enregistrement.get(cle_source)` traite "clé absente" et "valeur `None`"
de façon identique, et c'est voulu : les deux veulent dire la même chose
(pas de valeur utilisable), donc pas besoin de les distinguer.

Une seule fonction `verification_presence`, commune aux 3 sources,
appliquée après traduction (puisque le dict traduit a toujours la même
forme) : liste les clés dont la valeur est `None`, lève `DonneeInvalidError`
avec le numéro de ligne si au moins une clé manque, renvoie l'enregistrement
(numéro de ligne, dict) sinon. Décisions clés :

- **Le numéro de ligne voyage maintenant à travers tout le pipeline**
  (extraction → traduction → vérification), sous forme de tuple
  `(ok, numero_ligne, donnee_ou_erreur)` — ordre rendu cohérent entre
  succès et échec après un bug où l'ordre différait selon le cas. Ça
  résout le problème "quel id mettre dans le rapport quand id lui-même
  est manquant" : on utilise le numéro de ligne dans tous les cas.
- **Nom de la source : pas besoin de le faire voyager dans chaque
  enregistrement.** Résolu par l'orchestration : `traitement(source)`
  traite une source du début à la fin dans un seul appel, donc connaît
  déjà l'extension/source tout au long — pas de perte de contexte à
  gérer puisqu'il n'y a pas (pour l'instant) de fusion des 3 flux en une
  boucle unique.
- **Table de dispatch par extension** (`EXTRACTEURS_FILE`,
  `TRADUCTEURS_FILE`, fusionnées dans un seul lookup `extracteur_path`) :
  un seul `traitement()` générique gère les 3 sources — ajouter une 4ᵉ
  source = une entrée de plus dans chaque dict, aucune modification de
  `traitement()`/`main()`. Abstraction justifiée par un vrai point de
  variation identifié (plusieurs formats de source à traiter
  uniformément), pas ajoutée par anticipation.
- **`nom: ''` (chaîne vide) passe la vérification de présence** — choix
  délibéré : présence de la clé ≠ validité du contenu. À couvrir
  explicitement à l'étape 3 (validation métier), sinon une donnée
  vide passe indéfiniment entre les mailles du filet.

Reste à faire avant de clore le projet : remplacer les `print` de
`traitement()` par une vraie collecte (liste des enregistrements valides,
rapport d'incidents structuré, compteurs par source) — les sorties
attendues (section 4) ne sont pas encore produites sous forme de données
exploitables, seulement affichées.

## 9. Étape 3 (Validation métier) + collecte finale — statut : terminée, décisions d'implémentation

Deux fonctions distinctes plutôt qu'une seule élargie :

- **`verification_presence`** : une valeur est absente si elle est `None`,
  n'est pas une chaîne, ou est une chaîne vide/blanche après `strip()`.
- **`verification_format`** : valide le *format* des champs présents
  (email via regex, id via `isdigit()`).

Décision prise en revue : la première version de `verification_presence`
faisait les deux jobs (présence + format email) sous un nom qui ne
décrivait que la présence — smell "leaky naming" détecté et corrigé en
séparant avant que la fonction ne devienne le fourre-tout de toute
validation future. Les deux fonctions sont appelées en séquence dans
`traitement()` ; si la présence échoue, le format n'est jamais vérifié
pour cet enregistrement (pas de double rapport pour la même ligne).

Bugs corrigés pendant l'implémentation :

- **Précédence d'opérateurs** dans `verification_presence` : la première
  version écrivait `val is None or not isinstance(val, str) and not
  val.strip()` — `and` étant plus fort que `or`, la clause `not
  val.strip()` ne se déclenchait jamais tant que `val` était une chaîne
  (toujours le cas ici). Une valeur `"   "` (espaces) traversait tout le
  pipeline sans être détectée. Corrigé en remplaçant le `and` interne par
  un `or` explicite entre les trois conditions.
- **`SourceInvalidError`/`DonneeInvalidError.__init__`** forcent
  maintenant `str(...)` sur le message reçu, quel que soit ce qu'on leur
  passe (chaîne ou exception). Ça garantit l'invariant "l'attribut est
  toujours une chaîne propre" à la source (le constructeur), plutôt que
  de dépendre de la discipline de chacun des appelants — règle le
  double-emballage observé plus tôt (`SourceInvalidError(SourceInvalidError(...))`)
  sans avoir à corriger chaque site d'appel séparément.
- **Forme unique du rapport d'incidents** : `{numero_ligne: raison}` pour
  *tout* type d'échec (extraction ou validation), avec le numéro de ligne
  comme entier et la raison comme chaîne — jamais un type différent
  (chaîne brute vs dict) ni une convention de clé différente ("Ligne N"
  vs `N`) selon l'origine de l'échec. Décidé après avoir observé en revue
  que deux formes différentes dans la même liste auraient forcé tout
  consommateur du rapport à faire un `isinstance` avant de pouvoir lire
  numéro de ligne + raison.

Sorties désormais produites comme données réelles (plus de simples
`print` de diagnostic) : `lignes_correctes` et `lignes_incorrectes`
(listes), compteurs par source, ratio valides/incidents — assemblées
dans `rapport_par_source` et affichées via `json.dumps`. Reste pour
clore le projet : pas encore de déduplication (étape 4), et ces
structures ne sont encore qu'imprimées, pas persistées/retournées.

## 10. Historique des révisions de conception

- v1 : `check_donnees(source)` mélangeait extraction et validation, pas de
  distinction technique/métier, 4 classes d'exception par champ.
- v2 : séparation extraction (étape 1) / validation (étape 3), mais
  confusion de vocabulaire entre "normalisation" (mise en forme commune)
  et "normalisation" (unicité).
- v3 : étapes clarifiées et nommées sans chevauchement, hiérarchie
  d'exceptions simplifiée à 2 branches, doublon traité hors du mécanisme
  d'exception.
- v4 : étape 1 implémentée et vérifiée (voir section 7) ; source JSON
  reformatée en JSONL pour préserver la granularité ligne-par-ligne
  partout.
- v5 (actuelle) : étape 2 (mise en forme commune, section 8) et étape 3
  (validation métier, section 9) implémentées et vérifiées ; séparation
  présence/format après détection d'un naming drift ; rapport d'incidents
  unifié sous une forme unique ; sorties remplacées par de vraies
  structures de données (listes, compteurs).