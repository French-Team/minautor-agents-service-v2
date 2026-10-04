"""Fonctions simples de la categorie file : une seule tache chacune."""
from commun import (
    armer_lot,
    defcon_bloque_theme,
    enregistrer_file,
    horodater,
    prochain_id,
    extraire_options,
    valider_theme,
)
from constants import STATUT_EN_ATTENTE


def charger_mission(arguments, charger_file, afficher_file):
    """Ajoute une mission a la file (theme FERME + objectif obligatoires)."""
    options = extraire_options(arguments, ("theme", "objectif"))
    theme = options.get("theme", "")
    objectif = options.get("objectif", "")
    if not theme or not objectif:
        print('Usage : python main.py charger --theme <nom> --objectif "..."')
        return 2
    code, theme = valider_theme(theme)
    if code != 0:
        return code
    code, message = defcon_bloque_theme(theme)
    if code != 0:
        print(message)
        return code
    file_missions = charger_file()
    mission = {
        "id": prochain_id(file_missions),
        "theme": theme,
        "objectif": objectif,
        "statut": STATUT_EN_ATTENTE,
        "chargee_le": horodater(),
    }
    file_missions.setdefault("missions", []).append(mission)
    enregistrer_file(file_missions)
    print("Mission " + mission["id"] + " chargee (theme : " + theme + ").")
    return 0


def transformer_mission(arguments, charger_file):
    """Re-etiquette une mission EN ATTENTE (theme + objectif) avant injection.

    Serie stricte : une mission en cours ou terminee ne se transforme plus.
    """
    options = extraire_options(arguments, ("id", "theme", "objectif"))
    identifiant = options.get("id", "")
    theme = options.get("theme", "")
    objectif = options.get("objectif", "")
    if not identifiant or not theme or not objectif:
        print('Usage : python main.py transformer --id M-00X --theme <nom> --objectif "..."')
        return 2
    code, theme = valider_theme(theme)
    if code != 0:
        return code
    code, message = defcon_bloque_theme(theme)
    if code != 0:
        print(message)
        return code
    file_missions = charger_file()
    for mission in file_missions.get("missions", []):
        if mission.get("id") == identifiant:
            if mission.get("statut") != STATUT_EN_ATTENTE:
                print("REFUS : " + identifiant + " n'est plus en attente (statut : " + mission["statut"] + ").")
                return 1
            mission["theme"] = theme
            mission["objectif"] = objectif
            mission["transformee_le"] = horodater()
            enregistrer_file(file_missions)
            print("Mission " + identifiant + " transformee (theme : " + theme + ").")
            return 0
    print("Mission inconnue : " + identifiant)
    return 1


def charger_lot(arguments, charger_file):
    """Charge PLUSIEURS missions d'un coup, dans l'ordre fourni, et ARME le lot.

    Format : --theme a=x,b=y --objectif "o1|o2" --lot "nom"
    Un lot = plusieurs rounds dans la meme boucle : le pilote enchainra les
    missions dans l'ordre, avec DEBUT/FIN annonces pour chacune.
    """
    options = extraire_options(arguments, ("theme", "objectif", "lot"))
    nom_lot = options.get("lot", "")
    themes = [t.strip() for t in options.get("theme", "").split(",") if t.strip()]
    objectifs = [o.strip() for o in options.get("objectif", "").split("|") if o.strip()]
    if not nom_lot or not themes or not objectifs or len(themes) != len(objectifs):
        print('Usage : python main.py charger --lot "nom" --theme "t1,t2" --objectif "o1|o2"')
        return 2
    themes_canoniques = []
    for theme in themes:
        code, theme = valider_theme(theme)
        if code != 0:
            return code
        themes_canoniques.append(theme)
    file_missions = charger_file()
    ids = []
    for theme, objectif in zip(themes_canoniques, objectifs):
        mission = {
            "id": prochain_id(file_missions),
            "theme": theme,
            "objectif": objectif,
            "statut": STATUT_EN_ATTENTE,
            "chargee_le": horodater(),
            "lot": nom_lot,
        }
        file_missions.setdefault("missions", []).append(mission)
        ids.append(mission["id"])
    armer_lot(file_missions, ids)
    enregistrer_file(file_missions)
    print("Lot " + nom_lot + " arme : " + str(len(ids)) + " missions (" + ", ".join(ids) + ").")
    return 0


def afficher_file(file_missions):
    """Affiche la file : en cours d'abord, puis les en attente."""
    missions = file_missions.get("missions", [])
    if not missions:
        print("File vide : aucune mission chargee.")
        return 0
    for mission in missions:
        print(
            mission["id"]
            + " [" + mission["statut"] + "] "
            + "theme : " + mission["theme"]
            + " -- " + mission["objectif"]
        )
    return 0
