class AppError(Exception):
    "levee a la frontiere commune"

class SourceInvalidError(AppError):
    def __init__(self, source_erreur):
        super().__init__(source_erreur)
        self.erreur = str(source_erreur) # a voir pourquoi

class DonneeInvalidError(AppError):
    def __init__(self, erreur_donnee):
        super().__init__(erreur_donnee)
        self.erreur_donnee = str(erreur_donnee)
