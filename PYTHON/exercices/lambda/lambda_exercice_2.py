def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Avant traitement de {func.__name__}")
        rslt = func(*args, **kwargs)
        print(f"Apres traitement {func.__name__}")
        return rslt
    return wrapper

def addition(a, b):
    return a + b

addition = logger(addition)
print(addition.__name__) # ouput wrapper