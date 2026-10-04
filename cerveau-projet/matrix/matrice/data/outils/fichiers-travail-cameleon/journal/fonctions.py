"""Fonction de la categorie journal : ce qui a ete pose, ce qui a ete solde."""

import json

from commun import chemin_relatif, journal_lire
from constants import ACTION_PURGE


def executer_journal(chemin_journal, limite, as_json):
    """Les derniers actes du journal, dans l ORDRE (voir sans fouiller)."""
    entrees = journal_lire(chemin_journal)
    tranche = entrees[-limite:]
    if as_json:
        print(json.dumps(tranche, ensure_ascii=True))
        return 0
    print("JOURNAL : " + chemin_relatif(chemin_journal) + " -- " + str(len(entrees))
          + " entree(s), " + str(len(tranche)) + " affichee(s)")
    for entree in tranche:
        detail = entree.get("nom", entree.get("brut", ""))
        complement = ""
        if entree.get("action") == ACTION_PURGE:
            complement = " (solde " + str(entree.get("solde", "?")) + ")"
        elif entree.get("resultat"):
            complement = " [" + str(entree["resultat"]) + "]"
        print("  " + str(entree.get("date", "")) + " " + str(entree.get("action", ""))
              + " " + str(detail) + " par " + str(entree.get("par", "")) + complement)
    return 0
