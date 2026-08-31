# Exercice (pratique)

# Tu gères les logs d'accès de ton app. Tu as :

utilisateurs_connectes_lundi = {"alice", "bob", "chloe", "david"}
utilisateurs_connectes_mardi = {"bob", "chloe", "eve", "frank"}
"""
Écris le code (pas juste le résultat) pour répondre à ces 3 questions :
1. Quels utilisateurs se sont connectés les deux jours ?
2. Quels utilisateurs se sont connectés lundi seulement (pas mardi) ?
3. Quels utilisateurs se sont connectés exactement un jour (l'un ou l'autre, pas les deux) ?

Avant de coder : pour chacune des 3 questions, dis-moi quelle opération de set tu vas utiliser et pourquoi — sans écrire le code d'abord.
"""
# Solution:
# 1 je vais utiliser l'operateur & car il va permettre de savoir l'intersection des gens connectes durant ces des 2 jours.
connectes_deux_jours = utilisateurs_connectes_lundi & utilisateurs_connectes_mardi
print(connectes_deux_jours) # {'chloe', 'bob'}

# 2 je vais utiliser l'operateur - car il va permettre de determiner ceux connectes uniquement le lundi au detriment de gens connectes mardi.
connectes_lundi = utilisateurs_connectes_lundi - utilisateurs_connectes_mardi
print(connectes_lundi) # {'david', 'alice'}

# 3 je vais utiliser l'operateur ^ car il va permettre de determiner ceux connectes uniquement le lundi ou ceux connectes uniquement le mardi et 
# non les deux jours a la fois(difference systemique).
connectes_uniquement_lundi_ou_mardi = utilisateurs_connectes_lundi ^ utilisateurs_connectes_mardi
print(connectes_uniquement_lundi_ou_mardi) # {'alice', 'eve', 'david', 'frank'}
