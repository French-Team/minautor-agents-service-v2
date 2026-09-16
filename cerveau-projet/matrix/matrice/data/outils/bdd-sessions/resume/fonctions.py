"""Categorie resume : lecteur BORNE de la BDD sessions (MO-092, MO-121).

Une lecture doit etre BORNEE (L-068) : on ne relit jamais la BDD entiere
pour en tirer une seule chose -- la DERNIERE session (moteur partage
data/commun/derniere_session.py, jamais recopie ici).

MO-121 -- GARDE DE RETARD : cette porte annoncait S-026 / MO-099 quand le
dernier travail reel etait MO-118 (19 missions plus tard) : elle ne
regardait que les entrees TAGUEES et se taisait sur les autres. Elle DIT
desormais le retard -- une reponse en retard qui se tait passe pour la
verite (friction 41, lecon L-093).

Precision mesuree : le retard ne se crie que sur une session FERMEE. Une
session OUVERTE absorbe legitimement les faits qui la suivent (le pilote
note chaque fin de mission en travail) : crier a chaque fin de mission
serait un faux positif qui userait le garde.
"""
import json

from constants import CHEMIN_BDD, ENCODAGE

# Moteurs partages (M-076) : data/commun est deja sur sys.path par constants.
from derniere_session import derniere_session, entrees_apres  # noqa: E402
from trace_session import ETAT_FERMEE, MARQUEUR_RETARD  # noqa: E402


def ligne_retard(entrees, entree, etat):
    """La ligne qui DIT le retard de trace, ou '' s'il n'y en a pas (MO-121)."""
    if etat != ETAT_FERMEE:
        return ""
    nombre, derniere = entrees_apres(entrees, entree)
    if nombre == 0 or derniere is None:
        return ""
    return (
        "  " + MARQUEUR_RETARD + str(nombre) + " entree(s) plus recente(s) que cette"
        " session (derniere : " + str(derniere.get("id", "?")) + " / "
        + str(derniere.get("date", "?")) + ") -- la session ci-dessus n'est PAS le"
        " dernier travail : lire la derniere entree avant de reprendre."
    )


def lire_derniere():
    """Charge la BDD et affiche la DERNIERE session (lecture bornee a UNE entree)."""
    if not CHEMIN_BDD.exists():
        print("Aucune session enregistree : " + str(CHEMIN_BDD) + " absent.")
        return 0
    with open(CHEMIN_BDD, "r", encoding=ENCODAGE) as flux:
        donnees = json.load(flux)
    entrees = donnees.get("sessions", [])
    entree, etat = derniere_session(entrees)
    if entree is None:
        # Une BDD PLEINE sans aucune session taguee n'est pas une BDD vide :
        # le dire est le contraire d'une reponse qui se tait (MO-121).
        if entrees:
            print("Aucune session TAGUEE dans " + str(CHEMIN_BDD) + " ("
                  + str(len(entrees)) + " entree(s) presente(s)) : la trace de session"
                  " n'a JAMAIS ete posee -- lire la derniere entree du fichier.")
        else:
            print("Aucune session trouvee dans " + str(CHEMIN_BDD) + " (BDD vide).")
        return 0
    print("DERNIERE SESSION (" + etat + ") :")
    print("  " + entree.get("id", "?") + " [" + entree.get("date", "?") + "]")
    print("  " + str(entree.get("session", "")))
    print("  tags : " + ", ".join(entree.get("tags", [])))
    retard = ligne_retard(entrees, entree, etat)
    if retard:
        print(retard)
    return 0
