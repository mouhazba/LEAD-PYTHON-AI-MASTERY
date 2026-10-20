# My Lead Python / AI Progress

## Python

- [x] Core syntax
- [x] Functions
- [x] Lists
- [x] tuple
- [~] Dictionnaires (dict) — 🟢 Competent séances du 2026-08-22 et 2026-08-25
- [ ] Dictionnaires imbriqués / fusion (`|`, `.update()`) — en attente depuis le 2026-08-22
- [~] Sets — 🟢 Competent séance du 2026-08-29
- [ ] Set comprehension — en attente depuis le 2026-09-02
- [~] comprehensions — 🟢 Competent séance du 2026-09-02
- [x] Exceptions — 🔵 Advanced séances du 2026-09-06 au 2026-09-16 (mécanique, translation pattern, revue de code, propagation multi-couches)
- [x] Generators — 🔵 Advanced séance du 2026-09-19/20 (yield, protocole itérateur/StopIteration, épuisement, générateurs infinis + itertools.islice, pipeline de générateurs, anti-pattern argument par défaut mutable)
- [x] *args-**kwargs — 🟢 Competent séance du 2026-09-17 (mécanique + rationale wrapper générique)
- [x] lambda — 🟢 Competent séance du 2026-09-17 (déjà solide au diagnostic)
- [x] Decorators — 🔵 Advanced séance du 2026-09-17 (empilement, propagation `@wraps`, décoration de méthodes, anti-pattern `lru_cache`/self, revue de code `retry` avec chaînage `from e`)
- [x] Files — 🟢 Competent séance du 2026-10-16 (lecture paresseuse `readline()`/walrus vs `read()` eager déjà vue le 2026-10-02 ; exercice `compter_mots`/`ecrire_rapport` : contrat de retour respecté après une déviation corrigée seul, choix de mode `"w"` vs `"a"` raisonné et justifié en mots propres, `with`+`encoding` systématiques). Différé volontairement (réemploi prévu en projet) : itération directe `for line in f`, gestion d'un fichier absent par exception plutôt que `if exists()`, autres modes (`"r+"`, `"x"`, binaire).
- [x] Modules — 🟢 Competent séance du 2026-10-16/18 : refactor réel de `PYTHON/projects/v_001_intermediare/resolution.py` (~270 lignes) en 6 modules (`exceptions.py`, `parser.py`, `extractions.py`, `traduction.py`, `validations.py`, `pipeline.py`) + `main.py`. Mécanique de `import`/`from...import`, `sys.path`, `__name__`/`"__main__"` expliquées puis appliquées correctement. Critère anti-cycle ("dépendance partagée → troisième module importé par les deux") appliqué deux fois par l'apprenant lui-même (exceptions, puis `extracteur_path`/dicts de dispatch), sans qu'on le redise la seconde fois. Pipeline testé, s'exécute sans erreur d'import.
- [x] Packages — 🟢 Competent séance du 2026-10-18 : même projet transformé en package réel (`__init__.py` vide, décidé après avoir évalué correctement qu'aucun import externe n'en avait besoin — pas de façade construite sans besoin). Imports absolus convertis en imports relatifs (`from .module import ...`) dans les 5 fichiers. Testé dans les deux sens : `python -m PYTHON.projects.v_001_intermediare.main` depuis la racine fonctionne, `python main.py` depuis le dossier échoue avec `ImportError: attempted relative import with no known parent package` — comprend pourquoi (pas de parent package connu hors `-m`).
- [x] Virtual Environments — 🟢 Competent séance du 2026-10-19 : `python3 -m venv`, activation, `pip install`, `pip freeze > requirements.txt` exécutés correctement. Deux erreurs réelles rencontrées et comprises : (1) venv nommé `.env` au lieu de `.venv` — confusion de convention avec les fichiers de variables d'environnement, corrigée après signalement ; (2) venv **renommé** après coup (`mv .env .venv`) plutôt que recréé — a cassé `bin/pip` (shebang à chemin absolu figé à la création, pointant vers l'ancien chemin), diagnostiqué concrètement (`bad interpreter`), conclusion correcte retenue : un venv n'est pas déplaçable, il faut le recréer. `.gitignore` corrigé (typo `__pycache__`, ajout explicite de `.venv/` en plus du `.gitignore` auto-généré à l'intérieur du venv lui-même).

Level: 🟡 Intermediate

## Python Advance

- [x] Modules — voir section "Python" ci-dessus
- [x] Package — voir section "Python" ci-dessus
- [ ] Imports
- [ ] Context managers
- [ ] Descriptor
- [ ] Protocols
- [ ] Type hints
- [x] Virtual Environments — 🟢 Competent séance du 2026-10-19 (voir note détaillée ci-dessous)
- [~] pip — pratiqué en passant (`pip install`, `pip freeze`), pas encore couvert pour lui-même
- [ ] Async Python

Level: 🔴 Beginner

---

## OOP

- [x] Classes
- [x] Objects
- [x] Inheritance
- [ ] Composition
- [ ] Polymorphism
- [ ] DataClasses
- [ ] Cuncurrency
- [ ] Memory Moddele
- [ ] SOLID

Level: 🔴 Beginner

---

## Design Patterns

- [ ] Factory
- [ ] Strategy
- [ ] Adapter
- [ ] Decorator
- [ ] Repository

Level: 🔴 Beginner

---

## FastAPI

Level: 🔴 Beginner

---

## Machine Learning

Level: 🔴 Beginner

---

## AI / LLM

Level: 🔴 Beginner

---

## Data Engineering

Level: 🔴 Beginner

---

## Architecture

- [x] Décomposition en responsabilités, frontières, choix de mécanismes
  tracés aux besoins réels, défense de décisions — 🟢 Competent, projet
  capstone `PYTHON/projects/v_001_intermediare` (2026-10-02 → 2026-10-11,
  skill `architecture_review`) : pipeline de normalisation multi-sources
  (CSV/JSONL/log), hiérarchie d'exceptions technique/métier justifiée
  (classes fusionnées quand elles ne changeaient rien en aval), smell de
  naming drift corrigé (`verification_presence` scindée en présence +
  format), dédup avec état partagé entre appels, documentation vivante
  tenue à jour (`conception.md`). Pas encore 🔵 : les smells (double
  emballage d'exception, bug de précédence, incohérence de forme du
  rapport) ont été repérés par la revue du mentor, pas de façon autonome
  par l'apprenant — prochaine étape pour viser 🔵 : un exercice où
  l'auto-revue (checklist Design Smells) précède la revue du mentor.

Level: 🟢 Competent

---

## Leadership

Level: 🔴 Beginner