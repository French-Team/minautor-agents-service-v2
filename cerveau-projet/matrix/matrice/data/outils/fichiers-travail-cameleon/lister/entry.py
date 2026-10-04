"""Categorie lister : montre la ZONE, element par element.

Interface entre main.py et les fonctions simples (lister/fonctions.py).
"""

from pathlib import Path

from commun import _options
from constants import JOURNAL, ZONE
from lister.fonctions import executer_lister

NOMS_OPTIONS = ("mission", "zone", "journal", "strict", "json")
DRAPEAUX = ("strict", "json")


def executer(arguments):
    options, _, refus = _options(arguments, NOMS_OPTIONS, DRAPEAUX)
    if refus:
        print(refus)
        return 2
    zone = Path(options.get("zone") or ZONE)
    chemin_journal = Path(options.get("journal") or JOURNAL)
    return executer_lister(zone, chemin_journal, options.get("mission"),
                           bool(options.get("strict")), bool(options.get("json")))
