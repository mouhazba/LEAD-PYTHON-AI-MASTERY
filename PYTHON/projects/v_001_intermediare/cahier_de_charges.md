# Cahier de charges

## Source A — export CRM (CSV)

id,nom,email,date_inscription
101,Awa Diop,<awa.diop@example.com>,2024-01-15
102,,<jean@example.com>,2024-02-03
103,Marc Leroy,pas-un-email,2024-03-10

## Source B — événements service moderne (JSONL, une ligne = un JSON)

{"user_id": "104", "full_name": "Fatou Ndiaye", "contact": "<fatou@example.com>", "signup_ts": "2024-04-01T10:00:00Z"}
{"user_id": "105", "full_name": "Ibrahima Sarr", "contact": "not-ayn-email", "signup_ts": "2024-05-20T08:30:00Z"}

Source C — logs texte ad hoc
[2024-06-01] NEW_USER id=106 name="Omar Ba" email=<omar@example.com>
[2024-06-02] NEW_USER id=107 name="" email=bad-format

## bjectif du pipeline

1. Produire une liste/flux d'enregistrements valides et normalisés vers un format commun (par exemple {"id": ..., "nom": ..., "email": ..., "source": ...}).
2. Produire un rapport des enregistrements invalides (id + raison précise), sans que ça arrête le traitement du reste du lot.
3. Produire quelques statistiques agrégées (ex : nombre de valides/invalides par source).

Pas de contrainte de volume énorme pour l'instant (pas la peine de simuler 50 Go) — on introduira cette contrainte plus tard si besoin, pour éviter justement d'imposer un générateur artificiellement dès le départ.

Avant d'écrire une seule ligne de code : comment découperais-tu ce problème en étapes/fonctions ? Qu'est-ce qui doit se passer en premier, et qu'est-ce qui dépend de quoi ? Donne-moi ton découpage (juste les noms d'étapes et leur enchaînement, pas encore le code).