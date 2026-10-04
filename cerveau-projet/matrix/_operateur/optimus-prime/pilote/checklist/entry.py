"""Categorie checklist : LA checklist d'une mission, selon son type.

Interface entre main.py et les fonctions simples (checklist/stockage.py).
"""
from commun import charger_file, enregistrer_file, horodater
from checklist.listes import TYPES
from checklist.stockage import fabrique_checklist


def executer(arguments):
    options = extraire_options(arguments, ("id",))
    identifiant = options.get("id", "")
    reconstruire = "--reconstruire" in arguments
    if not identifiant:
        print("Usage : python main.py checklist --id MO-XXX [--reconstruire]")
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
        origine = "proposee (type/theme : " + type_mission + ")"
        if type_mission not in TYPES:
            print(
                "ECART : " + identifiant + " sans type ferme (" + type_mission
                + ") -- les garde-fous COMMUNS s'appliquent, le specifique du type manque."
            )
        if reconstruire:
            # Reconstruire APRES coup ne rejoue pas l'injection : la trace le dit
            # (checklist_reconstruite_le), personne ne peut croire qu'elle fut
            # remise a l'agent le jour de l'injection.
            mission["checklist"] = checklist
            mission["checklist_reconstruite_le"] = horodater()
            enregistrer_file(file_missions)
            origine += " -- RECONSTRUITE et enregistree (JAMAIS injectee)"
    print("Checklist de " + identifiant + " (" + origine + ") :")
    for entree in checklist:
        print("  - " + entree)
    return 0


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)
