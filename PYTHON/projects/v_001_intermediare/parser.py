import re
from .exceptions import SourceInvalidError


PATRON_LOG = re.compile(
    r"^\[(?P<date>[^\]]+)\]\s*"          # Date : tolère [] (vide)
    r"(?P<event>\w*)\s*"                 # Event : tolère chaîne vide
    r"(?:id=(?P<id>\d*))?\s*"            # 'id=' optionnel
    r'(?:name="(?P<name>[^"]*)")?\s*'    # 'name="..."' optionnel
    r"(?:email=(?P<email>\S*))?$"        # 'email=' optionnel
)


def parser(ligne):
    if isinstance(ligne, dict):
        if any(v is None for v in ligne.values()): # any(v is None for v in ligne.values()) exception colonne cvs absente=None
            raise SourceInvalidError("Ligne inexploitable")
        return ligne
    
    if isinstance(ligne, str):
        match = PATRON_LOG.match(ligne)
        if match is None:
            raise SourceInvalidError("Ligne inexploitable")
        if match:
            return match.groupdict()
        
    raise SourceInvalidError("Type de ligne non supporté")
