"""Categorie injection : orchestre le statut et l'injection ordonnee.

Interface entre main.py et les fonctions simples (injection/fonctions.py).
Integre le gestionnaire de cycle pour les injections automatiques.
"""
from commun import charger_file, extraire_options, lire_bilan, noter_prise_round
from injection.fonctions import (afficher_ordres, afficher_statut, conduire, enchainer,
                                 preparer_injection)

# Le gestionnaire de cycle vit DANS la porte qu'il sert : import qualifie, et
# AUCUNE insertion dans sys.path. Le nom qualifie determine le fichier charge.
from injection.cycle import CycleOptimus


def executer(arguments):
    if arguments and arguments[0] == "statut":
        # Afficher le statut du cycle et de la file
        cycle = CycleOptimus()
        cycle.statut()
        return afficher_statut(charger_file())
    if arguments and arguments[0] == "injecter":
        # Demarrer le cycle et preparer l'injection
        cycle = CycleOptimus()
        cycle.demarrer()
        # LA PRISE DE ROUND (EO-360, demande du createur 2026-09-22) : le GESTE DE
        # RECEPTION note l acte de PRENDRE le round. Sans lui, trois traces (file
        # en-cours, debut pose par la machine, injection deposee) disent que le round
        # a commence alors que PERSONNE ne l a pris -- et AUCUN garde ne les separe.
        # Il est note APRES la preparation : l injection vient peut-etre d etre
        # servie, et le refus de la serie stricte (round DEJA arme) est exactement le
        # cas de la reprise apres une cloture. JAMAIS bloquant.
        code = preparer_injection(charger_file)
        noter_prise_round(charger_file)
        return code
    if arguments and arguments[0] == "prendre":
        # EO-360 : PRENDRE LE ROUND ARME. C est le geste de la BOUCLE (ORDRE 4.7) :
        # apres un `fin`, la chaine a DEJA servi et arme la mission suivante, donc
        # `injecter` REFUSE (serie stricte -- il n y a plus rien a injecter pour lui).
        # Un refus n est pas une prise : ce verbe ne prepare RIEN, il DECLARE la prise
        # de la mission courante, par le meme chemin que la reception.
        return noter_prise_round(charger_file)
    if arguments and arguments[0] == "enchainer":
        return enchainer(charger_file)
    if arguments and arguments[0] == "conduire":
        # EO-185 : conduit une mission chargee HORS lot (elle devient courante).
        options = extraire_options(arguments[1:], ("id",))
        identifiant = options.get("id", "")
        if not identifiant:
            print('Usage : python main.py conduire --id MO-00X')
            return 2
        code = conduire(charger_file, identifiant)
        # EO-360 : `conduire` EST un geste de reception (la mission chargee devient
        # COURANTE et son injection part). La PRISE est donc tracee ici comme pour
        # `injecter` -- sans cela, la seule voie HORS lot serait accusee a tort par la
        # panne round-arme-jamais-pris (un round pris sans prise tracee).
        noter_prise_round(charger_file)
        return code
    if arguments and arguments[0] == "ordres":
        # `ordres --id MO-XXX [--complet|--peser]` : la FICHE TECHNIQUE DE TRAVAIL
        # (MO-471, decisions D2/D3/D4) -- version BORNEE de l injection remise (noyau dit,
        # ajustables resumes, plafond global). `--complet` rend l injection ENTIERE ;
        # `--peser` rend la MESURE de remise (MO-473 : poids fiche / plafond de remise,
        # poids de l injection entiere, gain). LECTURE SEULE : aucun etat modifie.
        options = extraire_options(arguments[1:], ("id", "complet", "peser"),
                                   drapeaux=("complet", "peser"),
                                   outil="pilote",
                                   usage="python main.py ordres --id MO-00X [--complet|--peser]")
        identifiant = options.get("id", "").strip()
        if not identifiant:
            print('Usage : python main.py ordres --id MO-00X [--complet|--peser]')
            return 2
        return afficher_ordres(charger_file(), identifiant,
                               bool(options.get("complet")), bool(options.get("peser")))
    if arguments and arguments[0] == "mission":
        # Gestion des phases de mission via le cycle
        if len(arguments) < 2:
            print('Usage : python main.py mission --action <debut|pendant|fin|retracter> [--id ID] [--theme THEME] '
                  '[--motif "..." (retracter)] [--horodatage <ts> (retracter : vise UNE trace)] '
                  '[--bilan BILAN | --bilan-fichier <chemin>]')
            return 2
        cycle = CycleOptimus()
        # Parser les arguments
        action = None
        mission_id = None
        theme = None
        bilan = None
        motif = None
        horodatage = None
        for i, arg in enumerate(arguments):
            if arg == "--action" and i + 1 < len(arguments):
                action = arguments[i + 1]
            elif arg == "--id" and i + 1 < len(arguments):
                mission_id = arguments[i + 1]
            elif arg == "--motif" and i + 1 < len(arguments):
                motif = arguments[i + 1]
            elif arg == "--horodatage" and i + 1 < len(arguments):
                horodatage = arguments[i + 1]
            elif arg == "--theme" and i + 1 < len(arguments):
                theme = arguments[i + 1]
            elif arg == "--bilan" and i + 1 < len(arguments):
                bilan = arguments[i + 1]
            elif arg == "--bilan-fichier" and i + 1 < len(arguments):
                # Meme lecture que `fin` et `enregistrer` (EO-132) : le recit long
                # peut venir d'un FICHIER, donc hors du shell.
                code_bilan, bilan, message_bilan = lire_bilan(
                    {"bilan-fichier": arguments[i + 1]})
                if code_bilan != 0:
                    print("REFUS : " + message_bilan)
                    return 2
        
        if not action:
            print("ERREUR : --action requis (debut, pendant, fin)")
            return 2
        
        if action == "debut":
            if not mission_id:
                print("ERREUR : --id requis pour le debut de mission")
                return 2
            return cycle.mission_debut(mission_id, theme)
        elif action == "retracter":
            # MO-551 : retirer une trace de debut FAUSSE sans l effacer (l archive du
            # cycle est en ajout seul). Distinct de `fin` : rien n est ferme ici,
            # seul l historique porte le retrait.
            return cycle.mission_retracter(mission_id or "", motif or "", horodatage)
        elif action == "pendant":
            cycle.mission_pendant()
            return 0
        elif action == "fin":
            # L id EST transmis (mesure du 2026-09-25) : sans lui, un `--id MO-412`
            # etait IGNORE EN SILENCE et la cloture tombait sur la mission EN COURS
            # (MO-408 close sous le nom de MO-412 -- exactement le defaut que la
            # convention refuse : une option CONNUE ne s ignore jamais en silence).
            return cycle.mission_fin(bilan, mission_id)
        else:
            print("ERREUR : action invalide (debut, pendant, fin)")
            return 2
    print('Usage : python main.py statut | injecter | enchainer | conduire --id MO-00X'
          ' | mission --action <debut|pendant|fin>')
    return 2
