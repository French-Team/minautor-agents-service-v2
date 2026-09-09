"""Categorie etat : montre l'etat de pause pose (mission, position, horodatage)."""
from commun import etat_existe, lire_etat
from constants import NOM_ETAT


def executer(arguments):
    if not etat_existe():
        print("Aucune session-matrix en pause (" + NOM_ETAT + " absent) -- session active ou jamais passee.")
        return 0
    etat = lire_etat()
    mission = etat.get("mission", {})
    print("SESSION-MATRIX EN PAUSE (etat : " + NOM_ETAT + ")")
    print("  Mission       : " + mission.get("id", "M-???") + " [" + mission.get("theme", "") + "]")
    print("  Objectif      : " + mission.get("objectif", ""))
    print("  Position file : index " + str(etat.get("position", "?")))
    print("  Pause posee   : " + etat.get("pause_le", "?"))
    print("  Restantes     : " + str(len(etat.get("file_restante", []))) + " mission(s) dans la file du pilote.")
    print("  Reprise       : python main.py reprendre (apres maintenance user + optimus).")
    return 0
