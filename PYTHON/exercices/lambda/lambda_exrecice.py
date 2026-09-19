def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Avant traitement de {func.__name__}")
        rslt = func(*args, **kwargs)
        print(f"Apres traitement {func.__name__}")
        return rslt
    return wrapper


@logger
def addition(a, b):
    return a + b


@logger
def saluer(nom, message="Bonjours"):
    return f"{message} cher {nom}"

addition(1, 2)
print("*" * 20)
saluer("Mouaz")
print("*" * 20)
saluer("Mouaz", "Bonjour")

# output:
"""
Avant traitement de addition
Apres traitement addition
********************
Avant traitement de saluer
Apres traitement saluer
********************
Avant traitement de saluer
Apres traitement saluer
"""
