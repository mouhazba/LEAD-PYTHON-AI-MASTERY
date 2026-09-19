1. Fail-fast vs continuer-et-collecter — le critère qui tranche

La question à te poser à chaque fois : est-ce que les éléments traités sont indépendants les uns des autres, ou est-ce que la suite dépend du succès de ce qui précède ?

- Indépendants → continuer et collecter. Ton process_users en est l'exemple parfait : l'échec de récupérer les données de l'utilisateur 2 n'a strictement aucun rapport avec la validité des données de l'utilisateur 1 ou 3. Autre exemple réel : envoyer une newsletter à 10 000 abonnés — si l'email de l'un bounce, tu ne vas pas annuler l'envoi aux 9 999 autres. Tu collectes les échecs pour les retraiter ou les rapporter.
- Dépendants → fail-fast. Exemple réel : appliquer une séquence de migrations de base de données (migration_1, migration_2, ... migration_10), où chacune suppose que la précédente a réussi. Si migration_3 échoue, continuer avec migration_4 appliquerait un changement sur un schéma dans un état incohérent — pire que de s'arrêter. Autre exemple : charger un fichier de configuration critique au démarrage d'une application — si une clé obligatoire manque, tu préfères que l'appli refuse de démarrer plutôt qu'elle tourne dans un état à moitié configuré.

Ton process_users traite des utilisateurs indépendants → ton choix de "continuer" était le bon, et tu l'as fait sans que je te le confirme d'avance.

2. Quand except: / BaseException large est légitime

Le point commun des cas légitimes : le catch large se trouve à la frontière la plus externe du système (pas enfoui dans une petite fonction utilitaire comme get_user_data), et il ne fait jamais disparaître l'erreur — il la logge intégralement (avec traceback) avant de continuer ou de la relever.

- Boucle principale d'un service long-running (un worker, un bot, un consommateur de queue de tâches) : tu veux qu'une erreur inattendue sur UNE tâche ne fasse pas planter tout le service. Tu catches large à ce niveau précis, tu logges tout, et tu passes à la tâche suivante.
- Système de plugins / sandbox (exécuter du code tiers non fiable — plugins, code soumis par un utilisateur, notebook) : tu ne peux pas prédire quel type d'exception du code que tu ne contrôles pas va lever, donc catcher large à la frontière entre ton système et ce code est légitime, pour éviter qu'il ne fasse tomber toute ton application.

Ce qui distingue ça de get_user_data : ce n'est pas la largeur du except en soi qui est le problème — c'est de catcher large et de jeter l'information (print générique + return None) dans une fonction technique enfouie, loin de toute frontière logique du système.