import requests

def get_user_data(user_id):
    # cas 1
    """
    response = requests.get(f"https://api.example.com/users/{user_id}")
    if response.raise_for_statut():
        raise ConnectionError
    data = response.json()
    return data
    """
    # cas 2
    try:
        response = requests.get(f"https://api.example.com/users/{user_id}")
    except requests.RequestException as e:
       raise requests.RequestException("API request fail") from e
    else:
        data = response.json()
        return data


def process_users(user_ids):
    results = []
    for uid in user_ids:
        try:
            user = get_user_data(uid)
        except requests.RequestException as e:
            print(f"Erreur lors du traitement du user: {uid} du a {e}")
            continue
        else:
            results.append(user["name"])
    return results


#uid = get_user_data(2)
#print(uid)
process_uid = process_users([1, 2, 3])
# ouput: 
"""
Erreur lors du traitement du user: 1 du a API request fail
Erreur lors du traitement du user: 2 du a API request fail
Erreur lors du traitement du user: 3 du a API request fail
[]
"""
print("*" * 30)
# +++++++++++++++++++++++++++++++++++++++++++++++ review code +++++++++++++++++++++++++++++++
import logging

logger = logging.getLogger(__name__)

# 1. Exception métier dédiée
class UserFetchError(Exception):
    """Erreur survenue lors de la récupération d'un utilisateur."""

def get_user_data(user_id: int) -> dict:
    try:
        response = requests.get(f"https://api.example.com/users/{user_id}", timeout=5)
        response.raise_for_status()  # Lève HTTPError si status code >= 400
        return response.json()
    except (requests.RequestException, ValueError) as e:
        # Traduction nette vers une exception du domaine de notre application
        raise UserFetchError(f"Impossible de récupérer l'utilisateur {user_id}") from e

def process_users(user_ids: list[int]) -> list[str]:
    results = []
    for uid in user_ids:
        try:
            user = get_user_data(uid)
            results.append(user["name"])
        except UserFetchError as e:
            # L'orchestrateur attrape l'exception MÉTIER, pas l'exception technique (requests)
            logger.warning("Échec pour le user %s : %s", uid, e)
            continue
    return results

process_uid = process_users([1, 2, 3])