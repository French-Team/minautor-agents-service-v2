"""Domicile unique de la carte ASCII de la Matrice (MO-210).

Une seule carte, DEUX consommateurs : le scan de maintenance (outil
corriger-ascii, lance par la routine veille-flux) et la porte `ecrire`, passage
oblige de TOUTE ecriture. La carte vivait dans les constantes de l'outil : la
porte aurait alors lu un fichier d'outil, et une seconde copie aurait ete deux
verites -- l'une corrigeant ce que l'autre ignorait.

Les deux outils s'ajoutent deja data/commun a sys.path (motif M-076) : ce
domicile est importable tel quel, sans machinerie nouvelle.

Doctrine : tout caractere ABSENT de la carte est laisse tel quel et SIGNALE --
il n'est jamais devine. La porte `ecrire` en fait un REFUS (rien n'est ecrit).
"""

CARTE_CONVERSION = {
    "\u00e0": "a", "\u00e2": "a", "\u00e4": "a",
    "\u00e9": "e", "\u00e8": "e", "\u00ea": "e", "\u00eb": "e",
    "\u00ee": "i", "\u00ef": "i",
    "\u00f4": "o", "\u00f6": "o",
    "\u00f9": "u", "\u00fb": "u", "\u00fc": "u",
    "\u00e7": "c",
    "\u00ff": "y",
    "\u00c0": "A", "\u00c2": "A", "\u00c4": "A",
    "\u00c9": "E", "\u00c8": "E", "\u00ca": "E",
    "\u00ce": "I",
    "\u00d4": "O",
    "\u00d9": "U", "\u00db": "U",
    "\u00c7": "C",
    "\u0153": "oe", "\u0152": "OE",
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u00ab": "<", "\u00bb": ">",
    "\u2013": "-", "\u2014": "-",
    "\u2026": "...",
    "\u00a0": " ",
    "\u2192": "->",
}


def convertir_texte(texte):
    """Retourne (texte_converti, caracteres_non_convertis) via la carte."""
    non_convertis = []
    morceaux = []
    for caractere in texte:
        if ord(caractere) <= 127:
            morceaux.append(caractere)
            continue
        remplacement = CARTE_CONVERSION.get(caractere)
        if remplacement is None:
            non_convertis.append(caractere)
            morceaux.append(caractere)
        else:
            morceaux.append(remplacement)
    return "".join(morceaux), non_convertis
