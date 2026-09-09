"""Categorie journal : les derniers evenements pause/reprise."""
from commun import lire_journal


def executer(arguments):
    evenements = lire_journal(10)
    if not evenements:
        print("Aucun evenement de pause enregistre (journal vide).")
        return 0
    print("Derniers evenements pause/reprise (10 max, recents d'abord) :")
    for evenement in evenements:
        print(
            "  [" + evenement.get("date", "?") + "] " + evenement.get("type", "?")
            + " -- mission " + evenement.get("mission", "?")
            + (" (origine : " + evenement.get("origine", "") + ")" if evenement.get("origine") else "")
            + (" (raison : " + evenement.get("raison", "") + ")" if evenement.get("raison") else "")
        )
    return 0
