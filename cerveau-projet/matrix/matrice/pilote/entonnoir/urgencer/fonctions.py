"""Fonctions simples de la categorie urgencer : une seule tache chacune."""
from listes import URGENCES
from stockage import horodater, verifier_famille


def urgencer_mission(etat, identifiant, urgence):
    """Pose l'urgence de la mission E-XXX (n'importe quel echelon, vrac inclus).

    Urgence FERMEE : une valeur hors liste est refusee. Retourne (code, message).
    """
    if urgence not in URGENCES:
        return 2, "Urgence inconnue : " + repr(urgence) + " (urgences fermees : " + ", ".join(URGENCES) + ")"
    code, message = verifier_famille(identifiant)
    if code != 0:
        return code, message
    cibles = [etat.get("vrac", [])] + [f for f in etat.get("files", {}).values()]
    for file_missions in cibles:
        for mission in file_missions:
            if mission.get("id") == identifiant:
                mission["urgence"] = urgence
                mission["urgence_le"] = horodater()
                return 0, "Mission " + identifiant + " : urgence " + urgence + "."
    return 1, "Mission inconnue dans l'entonnoir : " + identifiant
