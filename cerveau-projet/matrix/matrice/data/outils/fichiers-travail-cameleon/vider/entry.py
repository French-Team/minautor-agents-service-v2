"""Categorie vider : le solde de la zone, TRACE ligne par ligne.

Interface entre main.py et la fonction simple (vider/fonctions.py).
"""

from pathlib import Path

from commun import _options
from constants import JOURNAL, PAR_DEFAUT, ZONE
from vider.fonctions import vider

NOMS_OPTIONS = ("mission", "par", "zone", "journal")


def executer(arguments):
    options, _, refus = _options(arguments, NOMS_OPTIONS)
    if refus:
        print(refus)
        return 2
    zone = Path(options.get("zone") or ZONE)
    chemin_journal = Path(options.get("journal") or JOURNAL)
    code, rapport = vider(zone, options.get("mission"), options.get("par") or PAR_DEFAUT,
                          chemin_journal)
    print("PURGE : " + str(len(rapport["supprimes"])) + " retire(s) -- solde "
          + str(len(rapport["restants"])) + " element(s) dans la zone.")
    for nom in rapport["supprimes"]:
        print("  - retire : " + nom)
    for nom in rapport["echecs"]:
        print("  ! ECHEC  : " + nom + " (non retire -- la purge partielle se DIT)")
    for nom in rapport["restants"]:
        print("  = reste  : " + nom)
    if not rapport["supprimes"] and not rapport["restants"]:
        print("  (la zone etait deja vide)")
    return code
