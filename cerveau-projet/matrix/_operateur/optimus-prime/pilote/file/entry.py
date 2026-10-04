"""Categorie file : orchestre le chargement et l'affichage de la file.

Interface entre main.py et les fonctions simples (file/fonctions.py).
"""
from commun import (
    avancer_du_lot,
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
    # LA PORTE RECOIT DEUX FORMES : `<verbe> ...` et `file <verbe> ...` (l appelant
    # prefixe le nom de la porte). On NORMALISE ICI, UNE FOIS. Mesure du 2026-09-25 :
    # `python main.py file charger --item EO-432` ne matchait AUCUNE branche (elles
    # testaient arguments[0] == "charger") et tombait dans l AFFICHAGE -- un charge
    # demande se lisait comme une liste, sans un mot pour le dire.
    if arguments and arguments[0] == "file":
        arguments = arguments[1:]
    # MESURE DU 2026-09-25 (MO-417 / EO-437) : ces DEUX branches ne pouvaient JAMAIS
    # matcher -- elles testaient `arguments[0] == "file"` APRES la normalisation
    # ci-dessus, qui vient justement de retirer ce mot. Consequence mesuree :
    # `file verser` tombait dans l AFFICHAGE de la file, SANS UN MOT -- le pont
    # < brin entier -> UN lot > (EO-148) etait inatteignable depuis la ligne de
    # commande, et `file consommer` ne survivait que par sa SECONDE branche, plus
    # bas, qui portait deja la bonne forme (c est elle qui a masque le defaut).
    # C est la MEME faute que `file charger` (C-010), dont le remede n avait ete
    # pose que sur UNE seule branche. Le verbe se lit donc desormais SOUS LA MEME
    # FORME dans toutes les branches, et ses options se lisent APRES lui (l ancien
    # decalage `arguments[2:]` etait faux lui aussi).
    if arguments and arguments[0] == "verser":
        # 'python main.py verser [--lot <nom>]' : le BRIN ENTIER -> UN lot (EO-148).
        # Le pont ne servait que la tete : N items demandaient N appels a la main.
        options = extraire_options(arguments[1:], ("lot",))
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
    if len(arguments) >= 3 and arguments[0] == "lot" and arguments[1] == "avancer":
        # lot avancer --vers MO-XXX : PORTE DE SAUT (MO-470 / EO-445) -- la mission
        # visee passe en tete du lot et sera servie au prochain round. Les refus
        # nommes vivent dans commun.avancer_du_lot : ici on ne fait que router
        # (convention-architecture-outils).
        options = extraire_options(arguments[2:], ("vers",))
        identifiant = options.get("vers", "").strip()
        if not identifiant:
            print("Usage : python main.py lot avancer --vers MO-XXX")
            return 2
        code, message = avancer_du_lot(charger_file(), identifiant)
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
