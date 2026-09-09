"""Correspondance par MOTS ENTIERS pour le classement propose de l'entonnoir.

Mission M-026 : 'preparer' ne doit plus proposer 'reparation' (la sous-chaine
'reparer' glissait au milieu du mot). Un mot-cle ne parle que s'il est un mot
ENTIER du texte ; casse ignoree, pluriel simple tolere.
"""


def mots_de(texte):
    """Retourne l'ensemble des mots du texte en bas de casse (lettres et chiffres)."""
    import re
    return set(re.findall(r"[a-z0-9]+", texte.lower()))


def mot_parcourt(mots, mot_cle):
    """True si le mot-cle est un mot ENTIER du texte (pluriel simple tolere).

    Un mot-cle compose (avec espace) est cherche comme ensemble de mots entiers.
    """
    mots_cle = mots_de(mot_cle)
    if not mots_cle:
        return False
    if mots_cle <= mots:
        return True
    return any(mot + "s" in mots for mot in mots_cle)
