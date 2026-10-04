"""Estimation de tokens : motif UNIQUE de la Matrice (E-097, imperatif 56).

La Matrice ne voit PAS la tokenisation du LLM : tout comptage de tokens ici est
une ESTIMATION DETERMINISTE (1 token ~ CARACTERES_PAR_TOKEN caracteres). Elle ne
vaut pas comme comptage exact, elle vaut comme MESURE DE POIDS : comparer
l'entree d'un outil a sa sortie, reperer un outil qui gonfle le contexte, suivre
le poids d'une injection. C'est la metrique que le sac-a-dos enregistre a chaque
appel (tokens avant / tokens apres), et que les injections du pilote portent.

Aucun autre fichier ne recopie cette formule (M-076 : motif unique, jamais
duplique) : on importe ce module.
"""
CARACTERES_PAR_TOKEN = 4


def estimer_tokens(texte):
    """Retourne le nombre de tokens ESTIME d'un texte (0 si vide ou None)."""
    if not texte:
        return 0
    return (len(texte) + CARACTERES_PAR_TOKEN - 1) // CARACTERES_PAR_TOKEN


def peser_tokens(*morceaux):
    """Retourne le poids total estime d'un ensemble de morceaux de texte."""
    return sum(estimer_tokens(morceau) for morceau in morceaux)
