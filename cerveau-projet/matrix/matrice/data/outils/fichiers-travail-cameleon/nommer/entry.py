"""Categorie nommer : orchestre la pose d un fichier de travail canonique.

Interface entre main.py et la fonction simple (nommer/fonctions.py).
"""

from pathlib import Path

from commun import _options
from constants import JOURNAL, PAR_DEFAUT, ZONE
from nommer.fonctions import nommer

NOMS_OPTIONS = ("mission", "libelle", "extension", "par", "zone", "journal")


def executer(arguments):
    options, _, refus = _options(arguments, NOMS_OPTIONS)
    if refus:
        print(refus)
        return 2
    if not options.get("mission") or not options.get("libelle"):
        print("REFUS : nommer exige --mission et --libelle.")
        return 2
    zone = Path(options.get("zone") or ZONE)
    chemin_journal = Path(options.get("journal") or JOURNAL)
    code, message, _ = nommer(zone, options["mission"], options["libelle"],
                              options.get("extension") or "txt",
                              options.get("par") or PAR_DEFAUT, chemin_journal)
    print(message)
    return code
