"""Categorie lire : affiche le journal, ou UN encart filtre (si --encart)."""
from constants import CHEMIN_JOURNAL, ENCARTS, ENCODAGE


def executer(arguments):
    """Affiche le journal entier ou l'encart demande. Retourne 0, ou 2 si encart inconnu."""
    encart = None
    if arguments and arguments[0] == "--encart":
        if len(arguments) < 2:
            print("Usage : python main.py lire --encart <nom>")
            return 2
        encart = arguments[1]
        if encart not in ENCARTS:
            print("Encart inconnu. Encarts : " + ", ".join(ENCARTS))
            return 2
    try:
        contenu = CHEMIN_JOURNAL.read_text(encoding=ENCODAGE)
    except OSError:
        print("Journal absent : lancer d'abord 'python main.py construire'.")
        return 1
    if encart is None:
        print(contenu)
        return 0
    lignes = contenu.splitlines()
    dedans = False
    for ligne in lignes:
        if ligne.startswith("## Encart : "):
            dedans = ligne == "## Encart : " + encart
            if dedans:
                print(ligne)
            continue
        if dedans:
            print(ligne)
    return 0