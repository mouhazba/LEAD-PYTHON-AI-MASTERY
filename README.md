# 🐍 LEAD-PYTHON-AI-MASTERY

**My structured path from intermediate Python to lead-level Python & AI engineering.**
Notes, assessments, exercises, code reviews and real projects, with a progress log that records what I can actually *prove* I know.

🇫🇷 [Version française plus bas](#-français)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Level](https://img.shields.io/badge/level-intermediate%20%E2%86%92%20advanced-yellow?style=flat)
![AI-assisted](https://img.shields.io/badge/AI--assisted%20learning-Claude%20Code-D97757?style=flat)

---

## 🎯 Goal

Not just learning syntax, but building the skills of a lead developer:
deep Python knowledge · clean, maintainable code · testing & debugging · OOP & design patterns · software architecture · data engineering · AI/ML with Python · technical decision-making.

## 🧭 Learning method

1. **Understanding before memorization**
2. **Reasoning before copying solutions**: no solution is given before I try
3. **Practice before claiming mastery**: a topic is "done" only with evidence
4. **Progressive difficulty and real-world application**

Every topic follows the same loop:

```
notes  →  assessment  →  exercises  →  code review  →  project  →  progress log
```

## 🚀 Featured project: multi-source data pipeline

`PYTHON/projects/v_001_intermediare/`

Merges user records from **3 heterogeneous sources** into one clean format:

| Source | Format |
|---|---|
| CRM export | CSV |
| Modern service events | JSON Lines |
| Legacy application | Free-text logs |

**What it does**
- Parses each source, normalizes records to a common schema (`id`, `name`, `email`, `source`)
- Validates every record and reports invalid ones **with a precise reason**, without stopping the batch
- Produces aggregated statistics (valid / invalid per source)

**Design**
- Started from a written spec (`cahier_de_charges.md`) and a design document (`conception.md`) *before* coding
- Refactored a ~270-line script into a package of focused modules: `parser`, `extractions`, `traduction`, `validations`, `pipeline`, `exceptions`
- Custom exceptions with exception translation between layers, relative imports, no circular dependencies

```bash
# from the repository root
python -m PYTHON.projects.v_001_intermediare.main
```

## 📂 Repository structure

```
PYTHON/
  notes/        → my own notes per concept (dicts, sets, exceptions, generators, decorators…)
  assess/       → diagnostic assessments (questions + code)
  exercices/    → practice exercises
  projects/     → real projects, from spec to code
REVIEW/         → code reviews of my own solutions (decorators, generators)
ROADMAP/
  roapmap.md            → full roadmap, phase by phase
  progress.md           → current level per topic, with evidence
  learning_log_progress.md → session-by-session learning log
.claude/skills/ → AI mentoring workflows (see below)
```

## 🗺️ Roadmap & progress

| Phase | Topics | Status |
|---|---|---|
| 1. Python foundations | syntax, data structures, comprehensions, exceptions, modules, packages, files, venv | ✅ Done |
| 2. Advanced Python & OOP | generators ✅, decorators ✅, iterators, context managers, type hints, protocols, OOP, dataclasses | 🔄 In progress |
| 3. Software engineering | SOLID, clean code, design patterns, testing | ⏳ Next |
| 4+. APIs, data engineering, AI/ML | FastAPI, data pipelines, machine learning | ⏳ Planned |

Levels used in `progress.md`: 🟡 Intermediate · 🟢 Competent · 🔵 Advanced.
Each level is backed by what I actually did in a session, including the mistakes I made and fixed.

## 🤖 AI-assisted learning with Claude Code

I use Claude Code as a **mentor, not as a code generator**. The repository includes custom skills (`.claude/skills/`) that define how the AI must behave:

| Skill | Role |
|---|---|
| `python_mentor` | Teaches concepts, asks questions before giving answers |
| `learning_coach` | Plans sessions and adjusts difficulty |
| `oop_mentor` | Guides object-oriented design |
| `review` | Reviews my code like a senior developer |
| `architecture_review` | Challenges design and structure decisions |
| `system_design_interviewer` | Simulates system design interviews |
| `progress_tracker` | Updates the progress log with evidence |

The rules are in `CLAUDE.md`: the AI must challenge me and must not give solutions to exercises meant to build independent problem-solving.

---

## 🇫🇷 Français

**Mon parcours structuré pour passer de Python intermédiaire à un niveau lead en Python et IA.**

Chaque notion suit la même boucle : **notes → évaluation → exercices → revue de code → projet → journal de progression**. Une notion n'est validée que si je peux le prouver.

- **Projet phare** : un pipeline de données qui fusionne 3 sources hétérogènes (CSV, JSON Lines, logs texte), normalise et valide chaque enregistrement, signale les invalides avec leur raison et produit des statistiques. Conçu à partir d'un cahier des charges, puis découpé en modules et en package.
- **Progression** : la phase 1 (fondamentaux) est terminée, la phase 2 (Python avancé et POO) est en cours. Le détail par notion est dans `ROADMAP/progress.md`.
- **Apprentissage assisté par IA** : Claude Code sert de mentor, pas de générateur de code, grâce à des *skills* personnalisés (`.claude/skills/`) et aux règles de `CLAUDE.md`.

---

👤 [Mamadou (Mahadiou) Ba](https://github.com/mouhazba)
