"""Categorie pause : stoppe le cameleon, serialise l'etat, notifie la maintenance."""
from commun import (
    charger_file,
    enregistrer_file,
    etat_existe,
    extraire_options,
    journaliser,
    lire_perimetre,
    poser_etat,
    serialiser_etat,
)
from constants import (
    NOM_ETAT,
    NIVEAU_PAUSE_AUTO,
    RAISON_NOTIFIEE,
)
from pause.fonctions import notifier_cameleon

NOMS_OPTIONS = ("raison",)


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    raison = options.get("raison", "demande createur")

    if etat_existe():
        print("REFUS : une session-matrix est deja EN PAUSE (etat pose : " + str(NOM_ETAT) + " au niveau data/).")
        return 1

    niveau, _, _ = lire_perimetre()
    origine = "pause manuelle" if niveau != NIVEAU_PAUSE_AUTO else "defcon 5"

    file_missions = charger_file()
    etat, mission = serialiser_etat(file_missions)
    if etat is None:
        print("REFUS : aucune mission EN COURS a mettre en pause (file du pilote vide ou libre).")
        return 1

    poser_etat(etat)
    file_missions["missions"] = etat["file_restante"]
    enregistrer_file(file_missions)
    notifier_cameleon(mission["id"])
    journaliser("pause", {"origine": origine, "mission": mission["id"], "raison": raison})

    print("SESSION-MATRIX EN PAUSE (origine : " + origine + ").")
    print("  Mission sauvegardee : " + mission["id"] + " [" + mission.get("theme", "") + "] " + mission.get("objectif", "")[:60])
    print("  Etat serialise : " + NOM_ETAT + " (reprise a l'identique, sauvegarde SEULEMENT a la pause).")
    print("  Cameleon notifie : '" + RAISON_NOTIFIEE + "' -- la raison reelle n'est JAMAIS divulguee.")
    print("  Reprise : python main.py reprendre (maintenance terminee).")
    return 0
