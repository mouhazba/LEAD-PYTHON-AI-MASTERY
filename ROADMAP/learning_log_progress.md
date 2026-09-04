# Journal des séances d'apprentissage

---

## 2026-08-22 — Dictionnaires Python (dict)

### Concept étudié
Dictionnaires Python : création, accès, ajout, suppression, parcours avec `.items()`,
dict comprehensions, gestion d'erreurs (`KeyError`, `.get()`, `try/except`),
hashabilité des clés, ordre d'insertion, introduction à `Counter`/`defaultdict`.

### Niveau démontré
🟢 Competent

### Compétences démontrées (preuves)
- Diagnostic initial (5 questions) : réponses correctes et sans erreur conceptuelle sur
  la création, l'accès sécurisé, l'ajout, la suppression, le parcours, la gestion de
  `KeyError`, et la logique de comptage par dict.
- Exercice pratique (`etudiants_admis`) : première version contenait un bug de
  raisonnement (chevauchement de bornes à la valeur 14 entre "Admis" et "Bien", et
  filtre `>` au lieu de `>=` par rapport au seuil). Bug identifié seul à partir d'une
  trace manuelle guidée par une question ouverte, puis corrigé correctement dès la
  deuxième tentative avec un seul niveau d'indice.
- A suivi et compris la démonstration de la version single-pass (dict comprehension
  avec ternaires imbriqués vs fonction auxiliaire), y compris la distinction de
  lisibilité entre les deux approches.

### Points encore faibles
- `Counter` et `defaultdict` : expliqués mais jamais pratiqués dans un exercice —
  à ne pas considérer comme acquis.
- Tendance initiale à découper la logique en deux passages (comprehension puis boucle
  de réécriture) plutôt qu'en un seul passage — corrigé seulement après démonstration,
  pas trouvé seul.
- Non testé pendant cette séance : dictionnaires imbriqués (nested dicts), fusion de
  dicts (`|`, `update()`), et les sets.

### Prochain point recommandé
Exercice dédié sur `Counter`/`defaultdict` (ex. comptage réel avec `most_common()`),
puis passage aux Sets pour compléter le sous-thème "Lists / Dicts / Sets" du roadmap.

---

## 2026-08-25 — Counter et defaultdict (pratique)

### Concept étudié
`collections.defaultdict` (factory `set`) et `collections.Counter` (accumulation via
`+=`, extraction du maximum via `.most_common(n)`), appliqués dans un scénario combiné
en un seul passage sur les données.

### Niveau démontré
🟢 Competent, en progression vers 🔵 Advanced sur ce point précis

### Compétences démontrées (preuves)
- Exercice pratique (`analyse_commandes`) : solution correcte et complète dès la
  première tentative, sans indice ni correction nécessaire.
- Structure en **un seul passage** sur la liste `commandes`, remplissant simultanément
  `defaultdict(set)` et `Counter` — pas de double itération, choix efficace non
  suggéré explicitement dans l'énoncé.
- Usage correct de `.add()` sur les valeurs `set` du `defaultdict`, de `+=` pour
  accumuler les quantités dans le `Counter` (et non simplement compter des occurrences),
  et de `.most_common(1)[0]` plutôt qu'une recherche de maximum manuelle.

### Points encore faibles
- Nommage incohérent (mélange français/anglais : `produit_par_category`) — remarque
  cosmétique, pas fonctionnelle.
- Toujours non testé : dictionnaires imbriqués (nested dicts), fusion de dicts
  (`|`, `update()`), et les sets en tant que sujet à part entière.

### Prochain point recommandé
Passer aux Sets (opérations d'ensemble, cas d'usage) pour clore le sous-thème
"Lists / Dicts / Sets", ou approfondir avec un exercice sur dictionnaires imbriqués
et fusion de dicts si l'apprenant préfère rester sur les dicts.

---

## 2026-08-29 — Sets (opérations d'ensemble)

### Concept étudié
`set` Python : structure et hachage, hashabilité des éléments (vs hashabilité du
set lui-même), complexité O(1) moyenne / O(n) pire cas, opérations d'ensemble
(`&`, `|`, `-`, `^`), `frozenset`, cas d'usage réels (test d'appartenance rapide,
opérations entre collections).

### Niveau démontré
🟢 Competent

### Compétences démontrées (preuves)
- Diagnostic initial (5 questions) : opérations `&`, `|`, `-` déduites correctement
  par raisonnement ; `^` (différence symétrique) déduite seul à partir du nom de
  l'opérateur, avant toute explication.
- Deux erreurs conceptuelles initiales identifiées et corrigées **seul**, sans
  qu'on lui donne la réponse :
  1. confusion entre « le set est hashable » et « les éléments du set doivent être
     hashables » — résolue en partie par question guidée, confirmée par test
     empirique (`hash({1,2,3})` → `TypeError`) que l'apprenant a exécuté lui-même ;
  2. confusion initiale mutable/immuable comme cause du `TypeError` sur
     `{1, 2, [3, 4]}` — corrigée dès la question guidée.
- Exercice pratique (logs de connexion, `utilisateurs_connectes_lundi/mardi`) :
  réussi du premier coup sur les 3 sous-questions, avec justification de
  l'opérateur choisi **avant** l'écriture du code à chaque fois — bon signe de
  raisonnement plutôt que de pattern-matching.

### Points encore faibles
- Justification métier/design du choix `set` vs `list` (Q5 du diagnostic) : gap
  reconnu honnêtement par l'apprenant, comblé partiellement par l'explication
  (test d'appartenance O(1), opérations entre collections) mais pas encore
  pratiqué dans un exercice dédié — à ne pas considérer comme acquis.
- Nuance complexité moyenne (O(1)) vs pire cas (O(n) en cas de collisions) :
  expliquée mais non vérifiée par un exercice.
- `frozenset` : mentionné mais jamais pratiqué.
- Toujours non testés : dictionnaires imbriqués (nested dicts), fusion de dicts
  (`|`, `update()`).

### Prochain point recommandé
Soit un exercice de "Design" sur set/list/frozenset (ex. quand *ne pas* utiliser
un set) pour viser 🔵 Advanced sur ce sous-thème, soit fermer le thème
"Lists / Dicts / Sets" en traitant les Lists (non encore abordées formellement)
et les dictionnaires imbriqués / fusion de dicts, restés en attente depuis les
séances précédentes.

---

## 2026-09-02 — Comprehensions (list/dict/generator)

### Concept étudié
List comprehension, dict comprehension, generator expression (`()` vs `[]`),
filtre (`if` en fin) vs expression ternaire (`if/else` avant le `for`), limites
des comprehensions pour l'accumulation (écrasement de clés dupliquées), et par
extension révision `defaultdict` vs `Counter` (comportement de `Counter.__add__`
avec des valeurs négatives).

### Niveau démontré
🟢 Competent

### Compétences démontrées (preuves)
- Diagnostic (5 questions) : list/dict comprehension et distinction filtre vs
  ternaire correctes du premier coup. Deux erreurs identifiées et corrigées
  **seul** :
  1. oubli du filtre "pairs" dans l'énoncé (erreur de lecture, pas conceptuelle) ;
  2. fausse croyance que `(x for x in range(5))` produit un tuple — corrigée par
     vérification empirique (`type(...)`), même réflexe que lors de la séance
     Sets avec `hash()`.
- Exercice design (agrégation de transactions par utilisateur) : a correctement
  identifié que le dict comprehension écrase les clés dupliquées au lieu
  d'accumuler, formulé la règle précise lui-même ("les clés retiennent les
  dernières valeurs"), et implémenté une solution `defaultdict(int)` propre.
- A testé de façon autonome une alternative `Counter()`, découvert que
  `Counter.__add__` supprime silencieusement les clés à valeur ≤ 0 (comportement
  documenté de la stdlib), et — après explication (non déductible seul, culture
  stdlib) — a compris pourquoi `defaultdict(int)` est le choix sémantiquement
  correct pour un total signé, `Counter` étant réservé au comptage
  d'occurrences non négatives.
- Bon réflexe général : prédire avant d'exécuter, et admettre explicitement
  "je ne comprends pas" plutôt que d'improviser une explication approximative.

### Points encore faibles
- Set comprehension (`{expr for x in iterable}`) : jamais pratiquée, syntaxe
  non testée malgré la maîtrise du dict comprehension équivalent.
- Lisibilité/seuil comprehension vs boucle classique : réponse correcte en
  théorie (Q5), jamais mise à l'épreuve sur un cas concret de comprehension
  imbriquée à refactorer.
- Walrus operator (`:=`) dans une comprehension : non abordé.
- Toujours non testés (en attente depuis plusieurs séances) : dictionnaires
  imbriqués (nested dicts), fusion de dicts (`|`, `.update()`).

### Prochain point recommandé
Clore les points en attente (dicts imbriqués/fusion, ou set comprehension en
pratique rapide), ou avancer vers `Exceptions` — au choix de l'apprenant.
