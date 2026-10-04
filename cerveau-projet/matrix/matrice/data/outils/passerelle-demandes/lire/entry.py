"""Entry point du verbe `lire` : LECTURE SEULE de la passerelle user.

Ce verbe n ecrit RIEN : il lit le canal, type les demandes, compte, et DIT. Il
n est pas un dry-run du depot -- c est sa lecture a part entiere, celle qui
permet de verifier que la table crochet -> type fait ce qu on croit avant que le
createur voie 35 items dans son entonnoir.
"""
from commun import afficher_preparation, preparer
from constants import CHEMIN_CANAL
from options import extraire_options

OPTIONS = ()

USAGE = "Usage : python main.py lire   (LECTURE SEULE : aucune option)"


def executer(arguments):
    # `lire` n a AUCUNE option. Sans ce contrat, une option inconnue serait
    # AVALEE en silence -- l appel croirait avoir filtre, alors qu il n a rien
    # lu du tout. Le refus se nomme (EO-179).
    extraire_options(arguments, OPTIONS, outil="passerelle-demandes", usage=USAGE)
    print("== passerelle-demandes : lire ==")
    print("  canal : " + str(CHEMIN_CANAL))
    deposes, retenues, anomalies, deja_deposees = preparer()
    for ligne in afficher_preparation(deposes, retenues, anomalies, deja_deposees):
        print(ligne)
    print()
    print("  (LECTURE SEULE : aucun item depose, le canal n est pas touche)")
    return 0
