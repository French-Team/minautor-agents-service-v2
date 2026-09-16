"""Fonctions simples de la categorie retiqueter : une seule tache chacune.

POURQUOI CETTE PORTE (L-061, MO-076) : le ROLE d'un item est un champ FERME
(le vivier). Un item depose ou classe AVANT que ce champ existe n'en a pas --
et sans porte, la seule facon de le lui poser serait d'editer le JSON a la main
(geste interdit). Cette porte est le pendant de `urgencer` pour le role, et
c'est ELLE que nomme le refus de l'injection : une erreur doit designer le
geste qui la repare.
"""
from roles import CHAMP_ROLE, valider_role
from stockage import horodater, verifier_famille


def retiqueter_mission(etat, identifiant, role):
    """Pose le ROLE de la mission EO-XXX (n'importe quel echelon, vrac inclus).

    Role FERME : une valeur hors vivier est refusee (code 2, la porte a deja
    dit pourquoi + la liste). La trace `role_avant` est conservee : on ne
    reecrit jamais une identite en silence. Retourne (code, message).
    """
    code, canonical, ecart = valider_role(role)
    if ecart:
        print(ecart)
    if code != 0:
        return code, ""
    code, message = verifier_famille(identifiant)
    if code != 0:
        return code, message
    cibles = [etat.get("vrac", [])] + [f for f in etat.get("files", {}).values()]
    for file_missions in cibles:
        for mission in file_missions:
            if mission.get("id") == identifiant:
                avant = mission.get(CHAMP_ROLE, "")
                mission[CHAMP_ROLE] = canonical
                mission["role_source"] = "declaration"
                mission["role_le"] = horodater()
                if avant:
                    mission["role_avant"] = avant
                return 0, (
                    "Mission " + identifiant + " : role " + canonical
                    + (" (avant : " + avant + ")" if avant else " (etait sans role)")
                    + "."
                )
    return 1, "Mission inconnue dans l'entonnoir : " + identifiant
