"""Categorie `solder-orphelines` : le point d'entree de la porte.

Interface entre main.py et la fonction simple (canoniser/ossuaires.py) : la
REGLE du domicile est passee en argument, la porte ne la connait pas.

L'ORDRE EST IMPOSE. On solder d'abord, on ne verifie qu'ensuite : solder est
l'acte qui change, verifier ne fait que dire. Si le temoin de non-perte est
rompu, la BDD n'est PAS ecrite -- on rend la main sans avoir rien deplace.
"""
from canoniser.fonctions import comparer_recensements
from canoniser.ossuaires import solder_les_orphelines
from cible import niveau_de_chemin
from commun import charger_bdd, enregistrer_bdd, extraire_options
from constants import CHEMIN_BDD

NOMS_OPTIONS = ("simuler", "motif")

MOTIF_DEFAUT = ("fiche ORPHELINE : la forme est canonique mais le fichier "
                "n existe plus (absent du disque et de l historique git) -- "
                "la fiche est mise au registre des ossuaires, entiere et "
                "reversible")

USAGE = ("Usage : python main.py solder-orphelines [--motif \"...\"] "
         "[--simuler oui]")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    motif = str(options.get("motif", "") or "").strip() or MOTIF_DEFAUT
    donnees = charger_bdd()
    rapport, avant, apres = solder_les_orphelines(donnees, _designer, motif)
    integre, message_integrite = comparer_recensements(avant, apres)
    if not integre:
        print(message_integrite)
        return 1
    if not rapport:
        print("Aucune cle orpheline : chaque cle designe un fichier existant ("
              + str(sum(avant.values())) + " modification(s) intacte(s)).")
        return 0
    for cle, nombre in rapport:
        print("  " + cle + " (" + str(nombre) + " modification(s) mise(s) "
              + "au registre des ossuaires)")
    porteuses = sum(nombre for _, nombre in rapport)
    print("Fiches soldees : " + str(len(rapport)) + " | modifications portees : "
          + str(porteuses) + " | temoin : " + message_integrite)
    if str(options.get("simuler", "") or "").strip().lower() in ("oui", "1", "true"):
        print("SIMULATION : la BDD n'a PAS ete ecrite.")
        return 0
    empreinte = enregistrer_bdd(donnees)
    print("Empreinte recalculee par la porte : " + empreinte[:16] + "...")
    return 0


def _designer(cle):
    """La regle du DOMICILE, passee en argument : un seul escalier (L-029)."""
    return niveau_de_chemin(cle, CHEMIN_BDD)[0]