"""Categorie lire : affiche le journal, ou UN encart filtre (si --encart)."""
from constants import CHEMIN_JOURNAL, ENCARTS, ENCODAGE

USAGE = "Usage : python main.py lire [--encart <nom>]"
# Options DECLAREES par ce verbe : le domicile refuse tout le reste et NOMME le
# fautif (T2 de PB-002). Avant, --encartx etait simplement ignore et le journal
# ENTIER partait : le defaut se lisait comme le resultat demande (EO-179, L-055).
OPTIONS = ("encart",)


def executer(arguments):
    """Affiche le journal entier ou l'encart demande. Retourne 0, ou 2 si encart inconnu."""
    from options import CLE_SANS_VALEUR, extraire_options
    options = extraire_options(arguments, OPTIONS, outil="journal-multi-encarts", usage=USAGE)
    if "encart" in (options.get(CLE_SANS_VALEUR) or []):
        # Une option PRIVEE de valeur n est jamais lue "pas de contenu" : elle est DITE.
        print(USAGE)
        return 2
    encart = options.get("encart")
    if encart is not None and encart not in ENCARTS:
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