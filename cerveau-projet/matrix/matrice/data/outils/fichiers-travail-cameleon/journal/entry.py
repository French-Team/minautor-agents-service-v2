"""Categorie journal : la MEMOIRE de la zone (voir sans fouiller).

Interface entre main.py et la fonction simple (journal/fonctions.py).
"""

from pathlib import Path

from commun import _options
from constants import JOURNAL
from journal.fonctions import executer_journal

NOMS_OPTIONS = ("n", "journal", "json")
DRAPEAUX = ("json",)


def executer(arguments):
    options, _, refus = _options(arguments, NOMS_OPTIONS, DRAPEAUX)
    if refus:
        print(refus)
        return 2
    chemin_journal = Path(options.get("journal") or JOURNAL)
    try:
        limite = int(options.get("n") or 20)
    except (TypeError, ValueError):
        print("REFUS : --n attend un nombre.")
        return 2
    return executer_journal(chemin_journal, limite, bool(options.get("json")))
