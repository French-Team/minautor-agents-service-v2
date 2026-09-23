"""Categorie file : orchestre le chargement et l'affichage de la file.

Interface entre main.py et les fonctions simples (file/fonctions.py).
"""
from commun import (
    charger_file,
    consommer_tete_tresse,
    enregistrer_file,
    extraire_options,
    retirer_du_lot,
    verser_tresse,
)
from file.fonctions import (
    afficher_file,
    afficher_lot,
    charger_lot,
    charger_mission,
    enregistrer_mission,
    retiqueter_mission,
    transformer_mission,
)


def executer(arguments):
    if len(arguments) >= 2 and arguments[0] == "file" and arguments[1] == "consommer":
        # 'python main.py file consommer' : le verbe 'file' est en tete des arguments.
        file_missions = charger_file()
        code, message = consommer_tete_tresse(file_missions)
        if code == 0:
            enregistrer_file(file_missions)
        print(message)
        return code
    if len(arguments) >= 2 and arguments[0] == "file" and arguments[1] == "verser":
        # 'python main.py file verser [--lot <nom>]' : le BRIN ENTIER -> UN lot (EO-148).
        # Le pont ne servait que la tete : N items demandaient N appels a la main.
        options = extraire_options(arguments[2:], ("lot",))
        file_missions = charger_file()
        code, message = verser_tresse(file_missions, options.get("lot", ""))
        print(message)
        return code
    if arguments and arguments[0] == "charger":
        return charger_mission(arguments[1:], charger_file, afficher_file)
    if len(arguments) >= 2 and arguments[0] == "lot" and arguments[1] == "retirer":
        # lot retirer --ids MO-001,MO-002 [--motif ...] : REDUIT un lot ARME
        # (EO-265). Les refus nommes vivent dans commun.retirer_du_lot : ici on
        # ne fait que router (convention-architecture-outils).
        options = extraire_options(arguments[2:], ("ids", "motif"))
        ids = [i.strip() for i in options.get("ids", "").split(",") if i.strip()]
        if not ids:
            print("Usage : python main.py lot retirer --ids MO-001,MO-002 [--motif ...]")
            return 2
        code, message = retirer_du_lot(charger_file(), ids, options.get("motif", ""))
        print(message)
        return code
    if len(arguments) >= 2 and arguments[0] == "lot" and arguments[1] == "etat":
        # lot etat : AFFICHE le lot ARME -- rang k/n, item d'origine, type, urgence,
        # statut (MO-380). Le lot ne se lisait qu'en ouvrant le JSON a la main ; le
        # cockpit appelle ce verbe au lieu de redecouper la source lui-meme.
        return afficher_lot(charger_file())
    if arguments and arguments[0] == "lot":
        return charger_lot(arguments[1:], charger_file)
    if arguments and arguments[0] == "transformer":
        return transformer_mission(arguments[1:], charger_file)
    if arguments and arguments[0] == "retiqueter":
        return retiqueter_mission(arguments[1:], charger_file)
    if arguments and arguments[0] == "enregistrer":
        return enregistrer_mission(arguments[1:], charger_file)
    if arguments and arguments[0] == "consommer":
        file_missions = charger_file()
        code, message = consommer_tete_tresse(file_missions)
        if code == 0:
            enregistrer_file(file_missions)
        print(message)
        return code
    return afficher_file(charger_file())
