"""Categorie checklist : LA checklist d'une mission, selon son type.

Interface entre main.py et les fonctions simples (checklist/stockage.py).
"""
from commun import charger_file
from checklist.stockage import fabrique_checklist


def executer(arguments):
    options = extraire_options(arguments, ("id",))
    identifiant = options.get("id", "")
    if not identifiant:
        print("Usage : python main.py checklist --id M-XXX")
        return 2
    file_missions = charger_file()
    mission = next((m for m in file_missions.get("missions", []) if m.get("id") == identifiant), None)
    if mission is None:
        print("Mission inconnue : " + identifiant)
        return 1
    checklist = mission.get("checklist")
    origine = "stockee a l'injection"
    if not checklist:
        type_mission = mission.get("type") or mission.get("theme", "")
        checklist = fabrique_checklist(type_mission)
        origine = "proposee (theme : " + type_mission + ")"
        if not checklist:
            print("Checklist de " + identifiant + " : type hors listes fermees (" + type_mission + ") -- aucune checklist fermee.")
            return 0
    print("Checklist de " + identifiant + " (" + origine + ") :")
    for entree in checklist:
        print("  - " + entree)
    return 0


def extraire_options(arguments, noms_connus):
    """Extrait les options --nom valeur (forme seulement)."""
    options = {}
    index = 0
    while index < len(arguments):
        morceau = arguments[index]
        if morceau.startswith("--") and morceau[2:] in noms_connus:
            if index + 1 < len(arguments):
                options[morceau[2:]] = arguments[index + 1]
            index += 2
        else:
            index += 1
    return options
