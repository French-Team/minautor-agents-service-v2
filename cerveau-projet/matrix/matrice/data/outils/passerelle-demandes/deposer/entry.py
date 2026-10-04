"""Entry point du verbe `deposer` : le WET de la passerelle user.

IL DEMANDE AVANT D ECRIRE. Deposer 35 items est irreversible dans les faits : un
id est consomme, un item apparait dans l entonnoir du createur. L outil montre
donc TOUT ce qu il va deposer, et attend `--confirmer`. Sans elle il n ecrit rien
et le dit : un WET qui s execute sans dire ce qu il fait est un DRY deguise.

CE QU IL NE FAIT PAS. Il ne RETIRE rien du canal. Le contrat du canal dit qu une
demande extraite est retiree, mais le canal est la ZONE HORS JUGEMENT du createur
(MO-475) : l ecriture la-dessus demande une voie qui n existe pas encore, et le
createur n a pas valide ce retrait. Le canal reste INTACT, et l outil le dit.
"""
from commun import afficher_preparation, deposer_un, preparer
from constants import NOM_CONFIRMER
from options import extraire_options

USAGE = ("Usage : python main.py deposer [--confirmer]\n"
         "  Sans --confirmer : preparation affichee, RIEN depose.\n"
         "  Avec --confirmer   : les items sont deposes PAR LA PORTE.")
OPTIONS = (NOM_CONFIRMER,)


def executer(arguments):
    trouvees = extraire_options(arguments, OPTIONS, drapeaux=OPTIONS,
                                outil="passerelle-demandes",
                                usage=USAGE)
    confirme = NOM_CONFIRMER in trouvees
    print("== passerelle-demandes : deposer ==")
    deposes, retenues, anomalies, deja_deposees = preparer()
    for ligne in afficher_preparation(deposes, retenues, anomalies, deja_deposees):
        print(ligne)
    print()
    if not confirme:
        print("  DRY : rien n a ete depose.")
        print("  Pour deposer reellement : --" + NOM_CONFIRMER)
        print("  (le canal n est pas touche : le retrait n est pas valide)")
        return 0
    deposes_ok = 0
    echecs = []
    for item in deposes:
        code, sortie = deposer_un(item)
        if code == 0:
            deposes_ok += 1
        else:
            dernier = sortie.strip().splitlines()[-1] if sortie.strip() else "sans sortie"
            echecs.append("l." + str(item["ligne"]) + " " + item["theme"][:50]
                          + " -> " + dernier[:70])
    print("  DEPOSES : " + str(deposes_ok) + " / " + str(len(deposes)))
    for echec in echecs:
        print("    [ECHEC] " + echec)
    if retenues:
        print("  RETENUES (non deposees, type non devine) : " + str(len(retenues)))
    print("  Le CANAL n est PAS touche : une demande extraite doit etre retiree,")
    print("  mais ce retrait n est pas valide -- le canal reste intact.")
    return 1 if echecs else 0
