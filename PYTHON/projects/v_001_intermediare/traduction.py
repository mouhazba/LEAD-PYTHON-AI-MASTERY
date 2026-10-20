def traduire_csv(enregistrement, num):
    id = enregistrement.get("id")
    nom = enregistrement.get("nom")
    email = enregistrement.get("email")
    return num, {"id": id if id else None, "nom": nom if nom else None, "email": email if email else None}

def traduire_json(enregistrement, num):
    id = enregistrement.get("user_id")
    nom = enregistrement.get("full_name")
    email = enregistrement.get("contact")
    return num, {"id": id if id else None, "nom": nom if nom else None, "email": email if email else None}
    
def traduire_log(enregistrement, num):
    id = enregistrement.get("id")
    nom = enregistrement.get("name")
    email = enregistrement.get("email")
    return num, {"id": id if id else None , "nom": nom if nom else None, "email": email if email else None}