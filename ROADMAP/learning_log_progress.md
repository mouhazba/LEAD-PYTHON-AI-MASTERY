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

---

## 2026-09-06/07 — Exceptions (try/except/else/finally, chaînage, exceptions custom)

### Concept étudié
`try/except/else/finally`, capture multi-types (`except (A, B):`), distinction
`except:` (bare, capture `BaseException`) vs `except Exception:`, création
d'exceptions personnalisées, chaînage d'exceptions implicite (`__context__`,
automatique dès qu'une exception est levée dans un `except`) vs explicite
(`raise ... from e`, `__cause__`), et placement d'un `try/finally` unique
enveloppant tout le corps d'une fonction pour garantir un log dans tous les
chemins de sortie (design/encapsulation).

### Niveau démontré
🟡 Developing

### Compétences démontrées (preuves)
- Diagnostic (5 questions) : bonne maîtrise immédiate de la syntaxe de base
  (`try/except/else/finally`, capture multi-types avec tuple, création d'une
  exception personnalisée avec docstring et justification métier correcte —
  "distinguer le type d'erreur au lieu de parser un message").
- `except:` vs `except Exception:` : première réponse imprécise ("capture
  silencieuse" / "sans préciser le type"), n'a pas identifié seul la vraie
  cause. Correction obtenue après un indice ciblé (hiérarchie `BaseException`,
  `KeyboardInterrupt`) — réponse finale techniquement exacte et bien formulée,
  mais pas trouvée de façon autonome dès le départ.
- Chaînage implicite vs explicite (`from e`) : gap de connaissance reconnu
  explicitement par l'apprenant ("j'ai besoin d'explications") plutôt que
  d'improviser — bon réflexe déjà noté en comprehensions. Explication complète
  donnée, pas de vérification indépendante ultérieure sur ce point précis.
- Exercice pratique (fonction `retirer`, retrait bancaire) : implémentation
  finale correcte sur les 5 cas testés (montant invalide, solde insuffisant,
  dict mal formé avec chaînage `from e`, compte vide, cas nominal). A exploré
  seul plusieurs structures (finally dans le petit try interne, puis chez
  l'appelant) avant la bonne solution — bon réflexe d'itération plutôt que
  blocage, mais la structure correcte ("un seul try/finally enveloppant tout
  le corps, gardes comprises") n'a pas émergé de deux questions guidées
  successives ; a fallu montrer un fragment de code pour débloquer.
- Réflexe empirique irrégulier sur cette séance : plusieurs "sorties prédites"
  données en commentaire sans exécution réelle du code (relevé deux fois),
  et une sortie réellement collée contenant encore une erreur de
  retranscription (message d'exception mal recopié). Contraste avec le bon
  réflexe "je prédis puis j'exécute" bien établi en Sets/Comprehensions — à
  resurveiller, pas encore fiable sur ce sujet.

### Points encore faibles
- `except:` (bare) vs `except Exception:` (`BaseException`) : compris mais pas
  démontré de façon autonome sans indice — à retester.
- Chaînage implicite (`__context__`) vs explicite (`__cause__`/`from`) : expliqué,
  jamais pratiqué dans un exercice où l'apprenant doit choisir/décider seul.
- Placement d'un `try/finally` unique autour de tout le corps d'une fonction
  (garantir un chemin de sortie unique) : acquis après démonstration, pas
  encore vérifié en conception indépendante.
- Rigueur "prédire avant d'exécuter, puis vérifier mot pour mot" : relâchée
  sur cette séance par rapport aux séances précédentes.

### Prochain point recommandé
Exercice de conception sur les exceptions **sans indice** (nouveau scénario,
pas de fragment de code fourni) pour vérifier si la structure try/finally
unique et la distinction Exception/BaseException sont acquises de façon
autonome avant de marquer 🟢 Competent. En parallèle, les points toujours en
attente depuis plusieurs séances restent ouverts : dictionnaires imbriqués,
fusion de dicts (`|`, `.update()`), set comprehension.

---

## 2026-09-10 — Exceptions (suite) : translation pattern / chaînage explicite en conception libre

### Concept étudié
Exercice de conception sans indice de structure (fonction `traiter_commande`) :
séparation entre exception technique (couche externe simulée, `ConnectionError`)
et exception métier (`EnvoiEmailError`), pattern de traduction d'exception
("exception translation") avec chaînage explicite (`raise ... from e`),
vérification programmatique du chaînage via `__cause__`.

### Niveau démontré
🟢 Competent

### Compétences démontrées (preuves)
- A construit seul toute la structure de `traiter_commande` (validations,
  exceptions personnalisées nommées de façon pertinente, `try` extérieur
  unique + `try/except/else` imbriqué + `finally`) sans qu'aucun fragment de
  code ne lui soit montré — contraste net avec l'exercice précédent
  (`retirer`) où un fragment avait été nécessaire pour débloquer la même
  structure générale.
- A lui-même affiné son plan en repositionnant le `else` sur le bon `try`
  (celui de l'appel à `envoyer_email`, pas le `try` extérieur) sans qu'on le
  lui demande explicitement.
- Premier jet contenait un bug de conception significatif : `envoyer_email`
  levait directement l'exception métier (`EnvoiEmailError`) au lieu de
  l'exception technique attendue (`ConnectionError`), rendant le
  `except ConnectionError` de `traiter_commande` — et donc toute la contrainte
  de chaînage explicite de l'exercice — invisible dans les tests, sans lever
  d'erreur apparente. Bug non détecté seul dans un premier temps (a fallu une
  question guidée pointant vers le message de sortie du test 2), mais une fois
  la cause du problème expliquée en détail (demande explicite d'explication,
  concept d'architecture — séparation couche technique / couche métier —
  jamais vu avant), correction appliquée immédiatement et correctement au bon
  endroit.
- Vérification empirique nettement plus rigoureuse que la séance précédente :
  a testé les 4 cas réellement, et a ajouté **de son propre chef** une
  inspection de `e.__cause__` pour prouver programmatiquement que le
  chaînage fonctionnait, plutôt que de se contenter d'observer le message
  affiché. C'est le réflexe empirique qu'on cherchait à consolider depuis le
  début de la séance sur les exceptions.

### Points encore faibles
- Distinction `except:`/`BaseException` vs `except Exception:` : toujours pas
  retestée de façon autonome depuis le diagnostic initial (où un indice avait
  été nécessaire) — à vérifier dans une future séance, sans indice.
- Le pattern "exception translation" (couche technique vs couche métier) a dû
  être expliqué explicitement — c'est une notion de culture d'architecture,
  pas déductible seul sans exposition préalable ; acquis après explication,
  pas encore réutilisé dans un contexte différent pour confirmer la
  généralisation.
- Cohérence sémantique message/type d'exception (ex. message "Format email
  invalide" sur un `ConnectionError`) : détail mineur, signalé mais pas
  corrigé dans cette séance.

### Prochain point recommandé
Les bases des exceptions (try/except/else/finally, exceptions personnalisées,
translation pattern avec chaînage explicite) sont maintenant solides et
démontrées de façon indépendante sur deux exercices de conception différents
→ 🟢 Competent justifié. Pour viser 🔵 Advanced : faire réutiliser le pattern
de traduction d'exception dans un contexte différent sans aide, faire
comparer/défendre le choix `except Exception` vs exceptions spécifiques dans
un cas réel, et retester `BaseException` sans indice. Sinon, avancer vers un
nouveau sujet du roadmap (`lambda`, `*args/**kwargs`, ou clore les points en
attente : dicts imbriqués/fusion, set comprehension).

---

## 2026-09-10 (suite) — Exceptions : revue de code, compromis fail-fast/collecte, légitimité du catch large

### Concept étudié
Revue critique d'une implémentation tierce (fonctions `get_user_data` /
`process_users` avalant les erreurs), tracé empirique d'un chaînage
d'exceptions à travers deux fonctions combinées, redesign indépendant
(exception précise + pattern "continuer et collecter" pour un traitement par
lot), et discrimination explicite entre usage légitime et illégitime d'un
`except` large selon la position dans l'architecture (frontière externe du
système vs fonction d'intégration bas niveau).

### Niveau démontré
🔵 Advanced

### Compétences démontrées (preuves)
- **Revue de code** : a identifié seul le `except:` nu (réutilisant
  correctement le concept `BaseException` du diagnostic initial) et le
  problème du `else` manquant. Deux affirmations initialement imprécises
  corrigées en cours d'échange : (1) a d'abord cru que `raise ... from e`
  n'était pas présent dans le code alors qu'il l'était — corrigé après
  relecture ciblée ; (2) a d'abord mal prédit le comportement de
  `user["name"]` avec `user=None` (pensait qu'un `None` serait simplement
  ajouté aux résultats) — corrigé en traçant/exécutant réellement le code,
  découvrant que `None["name"]` lève un `TypeError` qui masque totalement
  l'erreur d'origine déjà perdue par le `except:` nu.
- **Diagnostic architectural clé, formulé correctement par l'apprenant** :
  "`except` nu dans `get_user_data` résout déjà l'erreur en retournant
  `None`, donc l'erreur est perdue même avant d'arriver dans
  `process_users`" — comprend que le chaînage explicite (`from e`) ne peut
  chaîner que ce qu'on lui donne, et qu'un chaînage syntaxiquement correct
  plus loin dans la pile n'empêche pas une perte d'information définitive en
  amont.
- **Redesign indépendant** : a choisi seul, sans qu'on le lui suggère, un
  `except requests.RequestException` précis dans `process_users` et un
  pattern "continuer + collecter" (`continue` dans la boucle) plutôt que de
  laisser une erreur interrompre tout le traitement du lot — choix qui
  s'avère être le bon compte tenu de l'indépendance des éléments traités.
- **Compromis fail-fast vs continuer-et-collecter** : après explication avec
  exemples (migrations séquentielles vs newsletter/import indépendant),
  a généralisé correctement et seul le critère ("les éléments sont
  indépendants") à un nouveau scénario non vu (import de lignes CSV vers une
  base de données), sans qu'on le lui rappelle.
- **Piège sur la légitimité du catch large — erreur puis correction sous
  contrainte** : première réponse incorrecte sur un cas de paiement
  (`charger_carte` appelant un processeur tiers type Stripe) — a conflaté
  "je ne contrôle pas le service tiers" avec "donc je dois catcher large et
  continuer", exactement le même type d'erreur que `get_user_data`. Après
  explication des conséquences concrètes (livrer une commande non payée), a
  correctement reformulé seul : catch précis, puis choix explicite entre
  laisser propager ou traduire en exception métier (`PaiementEchoueError`
  `from e`). Preuve de raisonnement révisable sous confrontation aux
  conséquences réelles, pas seulement de mémorisation d'une règle.

### Points encore faibles
- Le chaînage explicite (`from e`) avait été omis dans la première version du
  redesign (`get_user_data` avec `requests.RequestException`) — signalé par
  le mentor, **corrigé spontanément par l'apprenant juste après** (ajout de
  `from e` + enrichissement du message de log dans `process_users` avec le
  détail de l'exception `{e}`), sans qu'on le lui redemande. Bon signe que le
  réflexe est en train de s'installer, mais à reconfirmer sur un exercice
  futur sans rappel préalable du mentor.
- Le critère "légitimité du catch large" a nécessité une correction
  explicite sur le premier cas réel testé (paiement) avant d'être appliqué
  correctement — acquis, mais pas encore résistant à un nouveau piège non
  testé dans cette séance.

### Prochain point recommandé
🔵 Advanced justifié sur les Exceptions : mécanique complète maîtrisée,
pattern de traduction appliqué en conception libre à deux reprises, capacité
démontrée à réviser du code tiers, identifier un mauvais usage, comparer des
alternatives et réviser son propre jugement sous confrontation à des
conséquences concrètes (paiement). Pour renforcer davantage : refaire du
chaînage explicite un réflexe systématique sans rappel. Prochain sujet du
roadmap : `lambda`, `*args/**kwargs`, ou clore les points en attente
(dictionnaires imbriqués/fusion, set comprehension) — au choix de
l'apprenant.

---

## 2026-09-11/16 — Exceptions (python_mentor) : deep-dive Lead + propagation multi-couches (repository → service → appelant)

### Concept étudié
Deep-dive technique niveau Lead (hors cycle diagnostic complet, via le skill
`python_mentor`) : hiérarchie et héritage des exceptions (mixins type
`Retryable`), critères de création d'une exception personnalisée, `raise`
bare vs `raise e` et préservation du traceback, nuances de chaînage
(`from None`, `__cause__` vs `__context__`, aperçu des `ExceptionGroup`
3.11+), portée d'un `try`, exceptions vs flux de contrôle, EAFP vs LBYL
(notamment le risque de race TOCTOU en LBYL), propagation d'exceptions à
travers des couches applicatives (repository → service → appelant), et
anti-patterns professionnels. Suivi d'un exercice de conception complet
(système d'emprunt de bibliothèque à 3 couches) appliquant directement le
point sur la propagation multi-couches.

### Niveau démontré
🔵 Advanced (confirme et approfondit le niveau déjà atteint le 2026-09-10,
sur un sujet nouveau : l'architecture multi-couches)

### Compétences démontrées (preuves)
- **Conception de hiérarchie d'exceptions à deux branches** (technique
  `RepositryError` / métier `ServiceError` sous une racine commune
  `AppError`) construite et itérée seul sur plusieurs cycles de révision,
  avec choix explicite et assumé de ne pas utiliser le mixin `Retryable` en
  héritage multiple (choix simplifié justifié plutôt que suivi par défaut).
- **Auto-correction de deux erreurs de conception réelles**, dans les deux
  cas après une question guidée plutôt qu'un correctif donné directement :
  1. `Retryable` initialement associée à "livre introuvable" (erreur
     définitive, non réessayable) plutôt qu'à la panne de connexion (erreur
     temporaire, réessayable) — inversion sémantique corrigée après question
     sur le sens réel de "retryable" ;
  2. catch générique (`except RepositryError`) qui effaçait la distinction
     entre les deux exceptions du repository — corrigé vers des `except`
     précis par type, préservant la distinction voulue à chaque frontière.
- **Instruction explicite d'architecture appliquée après correction** :
  injection de dépendance dans `EmpruntService.__init__` (recevoir le
  repository en paramètre plutôt que le construire en interne) — non fait au
  premier jet malgré la consigne, corrigé une fois signalé que cela forçait
  les tests à accéder à des attributs privés depuis l'extérieur.
- **Bug EAFP/LBYL diagnostiqué et corrigé de façon autonome** : après avoir
  reformulé correctement, de mémoire, la distinction EAFP/LBYL vue dans le
  deep-dive, a prédit correctement (`KeyError` sur la mauvaise clé) l'effet
  d'un test qu'on lui a demandé d'ajouter (`id_livre=2`), diagnostiqué que
  l'implémentation initiale de `obtenir_livre` (dict comprehension filtrant
  l'ensemble du stockage) était un balayage inefficace masqué en filtre — ni
  LBYL propre ni EAFP —, et corrigé vers un accès direct `self._livres[id]`
  protégé par `except KeyError` (EAFP), puis **vérifié la correction avec un
  nouveau cas de test qu'il a ajouté lui-même** (cas 5, `id_livre=2`).
- **Chaîne de causalité à trois niveaux obtenue et comprise** : après
  correction, `ServiceObtenirLivreError.__cause__` → `LivreIntrouvableError`
  → `.__cause__` → `KeyError` d'origine — preuve concrète que la traduction
  successive à travers les couches ne détruit pas la trace vers la cause
  technique racine.

### Points encore faibles
- **Le chaînage explicite (`from e`) reste oublié par défaut au premier
  jet**, cette fois précisément à la toute première frontière de traduction
  (`KeyError` → `LivreIntrouvableError` dans le repository lui-même) —
  troisième occurrence de ce type d'oubli sur la séquence de séances
  Exceptions (après `traiter_commande` et le redesign `get_user_data`). Le
  réflexe n'est toujours pas automatique sans rappel du mentor, même si la
  correction est désormais immédiate et bien comprise une fois signalée.
- **Nouvelle forme de manque de rigueur observée** : après une demande de
  correction, l'apprenant a recollé le code **identique** (non modifié) une
  première fois, sans s'en rendre compte, avant d'envoyer la vraie version
  corrigée au message suivant — distinct du problème "prédiction non
  vérifiée" déjà noté précédemment ; ici c'est une erreur de gestion de
  fichier/copier-coller (travailler sur la mauvaise version, ou oublier de
  sauvegarder avant de copier), à surveiller.
- Les sujets les plus avancés du deep-dive (`ExceptionGroup`/`except*`,
  nuances fines `raise` vs `raise e` en dehors du bloc `except` d'origine)
  n'ont été vus qu'en théorie, jamais pratiqués.

### Prochain point recommandé
Le sujet Exceptions est maintenant couvert en profondeur (mécanique,
translation pattern, revue de code, compromis architecturaux, propagation
multi-couches) avec preuves répétées d'application indépendante — niveau 🔵
Advanced solide. Reste un seul réflexe à automatiser : le chaînage explicite
systématique, y compris à la toute première frontière technique→métier,
sans qu'on ait à le rappeler. Prochain sujet suggéré par l'apprenant lors
d'une séance précédente : `lambda`, `*args/**kwargs`, `Decorators`,
`Generators`, ou clore les points en attente (dicts imbriqués/fusion, set
comprehension).

---

## 2026-09-17 — `lambda` et `*args`/`**kwargs` (learning_coach)

### Concept étudié
Diagnostic puis cycle complet sur `lambda` (syntaxe, usage comme argument,
piège de style quand assigné à un nom, limite à une seule expression) et sur
`*args`/`**kwargs` (mécanique de collecte vs déballage, cas d'usage central :
wrapper générique acceptant une signature inconnue). Exercice pratique de
construction d'un wrapper `logger(func)` avec fermeture (`closure`),
utilisation spontanée de la syntaxe `@logger`, et question piège sur la
perte de métadonnées (`__name__`) après décoration — préambule informel au
sujet `Decorators`.

### Niveau démontré
🟢 Competent sur les deux sujets (cible par défaut, non structurants au
niveau Lead contrairement aux Decorators).

### Compétences démontrées (preuves)
- **`lambda`** : identification correcte et précise au diagnostic du
  comportement de `sorted(noms, key=lambda x: x.lower())`, notamment la
  non-mutation de la liste d'origine (nuance souvent ratée par les
  débutants) ; écriture indépendante d'une fonction d'ordre supérieur
  (`fonction_appliquee(func, val)`) utilisée avec une `lambda`.
- **`*args`/`**kwargs`** : mécanique déjà précise dès le diagnostic
  (positionnels → tuple, nommés → dict) ; formulation correcte et autonome
  du cas d'usage central (wrapper générique ne connaissant pas la signature
  de la fonction interne) après une seule question guidée.
- **Application pratique avancée** : a écrit de mémoire un wrapper
  `logger(func)` correct avec fermeture, forwarding correct des arguments
  positionnels et nommés, préservation de la valeur de retour — et a
  anticipé seul, sans qu'on le lui montre, la syntaxe `@logger` pour
  l'appliquer à `addition` et `saluer`.
- **Correction rapide sous guidage** : after une confusion (voir
  ci-dessous), a correctement déduit en une étape, une fois recadré sur le
  bon code, que `logger(addition)` retourne l'objet `wrapper` et que donc
  `addition.__name__` vaut `"wrapper"` — bonne compréhension du mécanisme de
  perte de métadonnées après décoration.

### Points encore faibles
- **Nouvelle occurrence du pattern "ne pas vérifier le contexte avant de
  répondre"** (déjà noté sur les séances Exceptions sous une autre forme :
  coller du code non modifié par erreur) : à la question sur
  `addition.__name__`, l'apprenant a improvisé un **autre** `logger`
  (`def logger(func, a, b): return func(a, b)`, qui appelle `func`
  immédiatement au lieu de retourner un wrapper) plutôt que de repartir du
  vrai `logger` écrit quelques minutes plus tôt dans le même échange. La
  réponse produite (`AttributeError`) semblait plausible mais provenait
  d'un raisonnement sur un artefact différent. Corrigé immédiatement après
  une question de recadrage, sans nouvelle erreur. À surveiller : vérifier
  le bon contexte/code avant de répondre, plutôt que d'improviser une
  version proche mais différente.
- `functools.wraps` mentionné mais non pratiqué — délibérément différé au
  sujet `Decorators`.

### Prochain point recommandé
Enchaîner directement sur `Decorators` (demandé par l'apprenant) : le
mécanisme de closure + `*args`/`**kwargs` est déjà acquis et appliqué
spontanément, la transition est donc naturelle. Cible : 🔵 Advanced (sujet
structurant du roadmap Lead). Prévoir de traiter `functools.wraps` dans ce
cycle.

---

## 2026-09-17 — Decorators (learning_coach)

### Concept étudié
Diagnostic puis cycle complet niveau Lead sur les décorateurs : définition
précise, ordre d'application en cas d'empilement, mécanique et piège de
`functools.wraps` (propagation `__name__` couche par couche, pas globale),
décoration de méthodes d'instance (`self` via `*args`), anti-pattern réel
`lru_cache` sur méthode d'instance (fuite mémoire, dangerosité selon durée
de vie du processus), et revue de code d'un décorateur `retry` fourni par
le mentor (bare `except`, contrat générique cassé, échec avalé
silencieusement).

### Niveau démontré
🔵 Advanced (cible atteinte).

### Compétences démontrées (preuves)
- **Écriture autonome et correcte, du premier coup** : décorateur `chrono`
  avec `functools.wraps`, et décorateur paramétré à 3 niveaux de fermeture
  (`@repeat(3)`-like) — tous deux fonctionnels sans aide.
- **Démarche d'ingénieur spontanée** : a testé lui-même, sans qu'on le lui
  demande, l'empilement des deux décorateurs dans les deux ordres pour
  vérifier son propre raisonnement sur l'ordre d'application — et a ainsi
  généré lui-même la preuve empirique d'un bug réel (perte du nom via
  `@wraps` manquant sur un seul maillon de la chaîne).
- **Diagnostic autonome guidé d'un bug qu'il a lui-même produit** : après
  une réponse initiale imprécise ("niveau de profondeur"), a identifié
  correctement en une question guidée que `func_decorateur_avec_parametre`
  n'utilisait pas `@wraps`, corrigé le bug, et vérifié la correction dans
  les deux ordres d'empilement.
- **Prédiction et vérification correctes** sur la décoration d'une méthode
  de classe : a prédit que `self` serait simplement capté par `*args`, et
  vérifié en exécutant le code (sortie montrant `self` comme premier élément
  du tuple `args`).
- **Raisonnement correct sur un trade-off réel** (fuite mémoire
  `lru_cache`/`self`) : a identifié correctement qu'un serveur long-running
  est le cas dangereux ; explication initiale du "pourquoi" incorrecte
  (pensait que le cache se "vide" plus vite sur un script court) mais
  signalée honnêtement comme une supposition plutôt que présentée comme
  certaine — corrigée par le mentor (récupération mémoire par l'OS à la fin
  du processus, indépendante des fuites internes).
- **Revue de code convergente en 3 itérations** sur un décorateur `retry`
  fourni : a identifié seul le `@wraps` manquant et le `except:` nu dès la
  première lecture ; a appliqué correctement, une fois guidé, le pattern de
  traduction/chaînage d'exceptions (`raise ... from e`) déjà maîtrisé depuis
  les séances Exceptions, à un nouveau contexte (retry générique).

### Points encore faibles
- **Sur-interprétation du contrat d'une fonction générique** : première
  revue du décorateur `retry` a inventé un domaine métier (jeu de
  devinettes, exception `ChoixError`, valeur de retour `"Bravo"`) non
  présent dans l'énoncé, cassant la généricité du décorateur — corrigé après
  question guidée sur ce qu'un `retry` générique doit réellement observer
  pour décider de relancer (une exception, pas une valeur de retour
  spécifique).
- **Rigueur moindre en mode "revue/correction" qu'en mode "écriture from
  scratch"** : la 2e itération de la revue de `retry` a introduit une
  régression (perte du `return` sur succès, cassant à la fois la valeur de
  retour et la sortie de boucle) — nouvelle manifestation du pattern déjà
  noté sur les séances Exceptions et sur `*args`/`**kwargs` (ne pas
  vérifier le contexte/l'état du code avant de soumettre une réponse),
  cette fois sous forme de régression introduite plutôt que de code
  identique recollé ou de contexte halluciné.
- Confusion initiale sur le mécanisme exact de la "sécurité" d'une fuite
  mémoire dans un script court (a supposé, à tort, que le cache se vide
  plus vite) — connaissance factuelle non déductible par raisonnement,
  corrigée directement par le mentor.

### Prochain point recommandé
`Decorators` est maintenant couvert en profondeur (mécanique, empilement,
métadonnées, méthodes, anti-pattern réel, revue de code avec chaînage
d'exceptions) — 🔵 Advanced solide. Le point de vigilance transversal
(vérifier son travail avant de le soumettre, surtout en mode
correction/revue) reste à automatiser, comme pour les séances précédentes.
Suite recommandée : `Generators` (sujet structurant restant du roadmap
Lead), ou clore les points en attente (dictionnaires imbriqués/fusion, set
comprehension) si l'apprenant préfère des sujets plus courts avant le
prochain gros morceau.

---

## 2026-09-19/20 — Generators (learning_coach)

### Concept étudié
Cycle complet niveau Lead sur les générateurs : syntaxe `yield` (repartie de
zéro, syntaxe complètement oubliée), mécanique de suspension/reprise
d'exécution, protocole itérateur et `StopIteration` (relié explicitement à
la maîtrise déjà acquise sur les exceptions), épuisement définitif d'un
générateur après un passage complet, distinction précise generator function
vs generator expression, cas d'usage réel (lecture paresseuse d'un fichier
volumineux, `for ligne in f` vs `f.read()`), composition de générateurs en
pipeline sans matérialisation intermédiaire, générateurs infinis +
`itertools.islice`, trade-offs (quand NE PAS utiliser un générateur : accès
indexé, itérations multiples, tri), et revue de code d'un générateur de
regroupement par lots avec argument par défaut mutable.

### Niveau démontré
🔵 Advanced (cible atteinte).

### Compétences démontrées (preuves)
- **Reconstruction rapide après oubli complet** : syntaxe `yield`
  totalement oubliée au départ ("j'ai franchement oublié tout"), mais
  application autonome et correcte dès le premier indice minimal
  (`carres(n)`), puis application propre et rapide sur tous les exercices
  suivants sans nouvelle régression sur la syntaxe de base.
- **Diagnostic autonome d'un bug de lecture de fichier** : a identifié seul,
  après une seule question guidée, que `f.read()` charge tout le fichier en
  mémoire (contraire à l'objectif) et qu'itérer sur une chaîne de
  caractères produit des caractères et non des lignes — corrigé vers
  `for ligne in f` directement.
- **Pipeline de générateurs correct du premier coup** : `extraire_dates`
  écrite comme fonction générique (accepte n'importe quel itérable de
  lignes), composée directement avec `lire_erreurs` sans code fourni par le
  mentor au-delà du squelette conceptuel.
- **Trade-offs correctement identifiés sans aide** : cas d'usage légitime
  d'un générateur (fichier volumineux, mémoire), et limites (accès indexé,
  itérations multiples) formulés de façon autonome et précise.
- **Revue de code à deux niveaux, avec auto-correction remarquée** : a
  identifié seul le bug du lot final incomplet perdu (logique) ; sur le bug
  plus subtil (argument par défaut mutable `lot=[]`), a nécessité
  l'explication du mentor (connaissance factuelle non déductible par
  raisonnement) mais a ensuite, **de sa propre initiative**, testé une
  deuxième variante (garder `lot` en paramètre avec `is None`) et **repéré
  lui-même**, en observant sa propre sortie incorrecte (`[[1, 2, 3, 'a',
  'b']]`, 5 éléments au lieu de lots de 3), que son `is None` était du code
  mort puisque le défaut réel était toujours `lot=[]` — puis a choisi de
  conserver la solution la plus simple et la plus sûre (ne pas exposer
  `lot` comme paramètre) plutôt que de complexifier avec le pattern
  sentinelle `None`.

### Points encore faibles
- **Rétention à moyen terme faible sur la syntaxe de base** : la mécanique
  `yield` avait été vue en formation mais entièrement oubliée avant cette
  séance — à surveiller sur les prochains sujets (est-ce un cas isolé lié à
  un temps d'inactivité, ou un pattern de rétention à renforcer par de la
  pratique répétée espacée ?).
- **Distinction generator function / generator expression** a nécessité
  deux passages avant d'être correctement reformulée (le premier essai
  répétait la même explication imprécise "réutilisable vs non réutilisable"
  déjà donnée avant explication).
- **Progrès à noter sur le point faible transversal identifié depuis les
  séances Exceptions/Decorators** (vérifier son travail avant de le
  soumettre) : première réelle démonstration spontanée d'auto-vérification
  réussie dans cette séance (repérage du bug `is None` mort via sa propre
  sortie de test, sans qu'on le lui signale directement) — à confirmer sur
  les prochaines séances avant de considérer ce point comme résolu.

### Prochain point recommandé
Sujets structurants restants du roadmap Lead : `Context managers`,
`Type hints`, `Iterators` (approfondissement — vu en survol via le protocole
itérateur pendant cette séance, jamais implémenté à la main via
`__iter__`/`__next__`), `OOP`/`Composition`. Sinon, clore les points en
attente (dictionnaires imbriqués/fusion, set comprehension) si l'apprenant
préfère un sujet plus court avant le prochain gros morceau.

---

## 2026-10-02 → 2026-10-11 — Projet capstone : pipeline de normalisation multi-sources (`PYTHON/projects/v_001_intermediare`)

### Concept étudié
Projet de fin de cycle intermédiaire, choisi pour sa réutilisabilité dans
les phases ultérieures du roadmap plutôt que pour cocher des concepts :
pipeline à 4 étapes (extraction, mise en forme commune, validation métier,
déduplication) sur 3 sources hétérogènes (CSV, JSONL, log texte). Conception
menée via le skill `architecture_review` (Design Cycle complet : requirements
→ décomposition → frontières → points de variation → mécanismes → défense →
revue → itération), implémentation guidée par revue de code à chaque étape,
documentation vivante tenue à jour dans `conception.md`.

### Niveau démontré
🟢 Competent en conception/architecture (nouveau sous-thème évalué pour la
première fois) ; réemploi confirmé et appliqué en conception réelle des
acquis `Exceptions`/`Generators`/`Decorators` déjà 🔵 Advanced.

### Compétences démontrées (preuves)
- **Décomposition itérative jusqu'à une architecture propre** : 3 versions
  successives du découpage avant une version sans chevauchement de
  responsabilités (voir `conception.md` §10, historique v1→v5) — progression
  normale en conception, pas un échec des tentatives précédentes.
- **Hiérarchie d'exceptions défendue, pas suivie par défaut** : a justifié
  seul la fusion de 4 classes d'exception par champ en une seule
  `DonneeInvalidError`, avec le critère correct ("`except A` fait-il
  vraiment autre chose que `except B` en aval ?"), et a lui-même proposé
  puis abandonné une classe `LingeInvalidError` en reconnaissant qu'elle
  était systématiquement reconvertie en générique dès qu'attrapée.
- **Réutilisation correcte de l'épuisement des générateurs** (acquis
  🔵 Advanced de la séance Generators) dans un nouveau contexte : a compris
  et appliqué la règle "jamais `raise` pour une ligne, toujours `yield` un
  tuple" pour préserver la granularité ligne-par-ligne sans tuer le
  générateur prématurément.
- **Diagnostic autonome d'une limite du format JSON** (non vue en cours) :
  a identifié que `json.load` sur un tableau JSON casse la granularité
  ligne-par-ligne, et a reformaté la source en JSONL pour la restaurer —
  raisonnement transféré depuis le besoin déjà compris, pas une recette
  apprise par cœur.
- **Mutable default argument évité correctement en situation réelle**
  (`ids_vus=None` + sentinelle) sans qu'on ait eu à le rappeler — réemploi
  spontané de l'anti-pattern vu en revue de code pendant la séance
  Generators.
- **Revue de code sur plusieurs tours, avec correction complète à chaque
  fois** : bug de précédence d'opérateurs (`and`/`or`) dans
  `verification_presence`, double-emballage d'exception
  (`SourceInvalidError(SourceInvalidError(...))`), indexation erronée
  `e.erreur[0]`/`e.erreur[1]` sur une chaîne, variable utilisée avant
  affectation garantie, incohérence de forme du rapport d'incidents (dict
  vs chaîne, puis clé `"Ligne N"` vs `N`) — chaque fois corrigé complètement
  dès le tour suivant une fois le problème signalé et une piste de scénario
  concret donnée.
- **Dédup raisonnée correctement à partir de questions ouvertes, sans
  fragment de code** : a correctement déduit que la portée devait être
  globale (set partagé entre les 3 appels, passé en paramètre depuis
  `main()`), que le filtre ne devait s'appliquer qu'aux enregistrements
  déjà valides, et que l'insertion se faisait après les deux vérifications
  — les trois réponses tenaient déjà la bonne conception avant d'écrire une
  ligne de code.

### Points encore faibles
- **Les smells structurels ont presque toujours été repérés par la revue
  du mentor, pas de façon autonome** : double-emballage, bug de précédence,
  incohérence de forme du rapport, variable non garantie — aucun n'a été
  détecté en premier par l'apprenant lui-même avant d'être signalé. C'est
  précisément la barre qui distingue 🟢 Competent de 🔵 Advanced en
  conception (skill `architecture_review`) : il manque au moins une
  instance de smell repéré en premier par l'apprenant sur son propre
  travail.
- **Un lapsus de vérification** : deux exécutions différentes collées à la
  suite dans un seul message (étape 4), sans préciser laquelle reflétait
  le code actuel — signalé, pas encore récurrent sur ce projet, mais à
  surveiller (cf. [[feedback_verify_pasted_code]]).
- Reste cosmétique, non bloquant : variables `numero_ligne` inutilisées
  dans `verification_presence`/`verification_format`, espacement dans le
  message `JSONDecodeError`.

### Prochain point recommandé
Pour viser 🔵 Advanced en conception : un prochain exercice de design où
l'auto-revue (checklist Design Smells du skill `architecture_review`)
est demandée **avant** la revue du mentor, pour vérifier si l'apprenant
détecte un smell en premier sur son propre travail. Sur le roadmap
général : clore Phase 1 (`Files` — déjà abordé en aparté sur ce projet,
donc à démarrer par une explication et non un diagnostic ; puis `Modules`,
`Packages`, `Virtual environments`), puis Phase 2 (`Iterators`, `Context
managers`, `OOP`/`Composition` — ce même projet est explicitly prévu comme
terrain de réemploi pour un refactor OOP/Composition, cf. `conception.md`).
