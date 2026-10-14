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
- [ ] Files — modes de lecture (`read()`/`readlines()` eager vs itération paresseuse sur le fichier/`readline()`) abordé en aparté le 2026-10-02 pendant le projet pipeline (étape extraction) ; sujet complet encore à couvrir. NB apprenant (2026-10-02) : démarrer ce sujet par une explication, pas par un diagnostic, car découvert via la pratique avant la théorie formelle.

Level: 🟡 Intermediate

## Python Advance

- [ ] Modules
- [ ] Package
- [ ] Imports
- [ ] Context managers
- [ ] Descriptor
- [ ] Protocols
- [ ] Type hints
- [ ] Virtual Environments
- [ ] pip
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