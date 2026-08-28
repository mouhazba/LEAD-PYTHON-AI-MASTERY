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
