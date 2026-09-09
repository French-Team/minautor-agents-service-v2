"""Categorie reprendre : relance la session-matrix, restaure la mission a l'identique."""
from commun import (
    enregistrer_file,
    etat_existe,
    journaliser,
    lire_etat,
    retirer_etat,
    lire_perimetre,
    charger_file,
)
from constants import (
    CLE_PERIMETRE,
    NOM_ETAT,
)
from reprendre.fonctions import restaurer_mission


def executer(arguments):
    if not etat_existe():
        print("REFUS : aucune session-matrix en pause (aucun etat pose : " + str(NOM_ETAT) + ").")
        return 1

    etat = lire_etat()
    mission = etat.get("mission", {})
    id_mission = mission.get("id", "M-???")

    # Zones exclues de la lecture cameleon (regle matrice-utilise-cameleon) :
    # la reduction peut etre posee PENDANT la maintenance (cote maintenance).
    _, zones, _ = lire_perimetre()
    if zones:
        print("Perimetre cameleon : " + str(len(zones)) + " zone(s) exclue(s) de SA lecture (reprise conforme).")

    file_missions = charger_file()
    en_cours = any(m.get("statut") == "en-cours" for m in file_missions.get("missions", []))
    if en_cours:
        print("REFUS : une mission est deja EN COURS dans la file du pilote (serie stricte) -- reprise impossible sans incoherence.")
        return 1

    restaurer_mission(etat, file_missions)
    enregistrer_file(file_missions)
    retirer_etat()

    from reprendre.fonctions import notifier_cameleon
    notifier_cameleon(id_mission)
    journaliser("reprise", {"mission": id_mission})

    print("SESSION-MATRIX REPRISE : mission " + id_mission + " restoree a l'identique (meme place dans la file).")
    print("  Cameleon notifie : maintenance terminee -- sans aucun detail de la maintenance.")
    print("  Perimetre actuel : cle '" + CLE_PERIMETRE + "' du classeur (zones exclues : " + (", ".join(zones) if zones else "aucune") + ").")
    print("  Le niveau defcon reste le fait de la machine-defcon (pause-session ne le touche jamais).")
    return 0
