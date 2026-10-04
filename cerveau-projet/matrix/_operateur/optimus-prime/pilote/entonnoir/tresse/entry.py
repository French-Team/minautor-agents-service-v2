"""Categorie tresse : echelon 4 -- la file principale (le brin d'ADN).

Interface entre main.py et les fonctions simples (tresse/fonctions.py).
"""
from stockage import charger_entonnoir, enregistrer_entonnoir
from tresse.fonctions import marquer_brin, tresser


def afficher_brin(brin):
    """Affiche le brin tresse (position, urgence, type/categorie, theme)."""
    if not brin:
        print("  (brin vide)")
        return 0
    for mission in brin:
        print(
            "  " + str(mission["position_brin"]).rjust(2) + ". [" + mission["urgence"] + "] "
            + mission.get("type", "?") + "/" + mission["categorie"]
            + "  " + mission["id"] + "  " + mission["theme"]
        )
    return 0


def executer(arguments):
    if not arguments or arguments[0] not in ("brin", "tisser"):
        print("Usage : python main.py tresse brin | python main.py tresse tisser")
        return 2
    sous_commande = arguments[0]
    etat = charger_entonnoir()
    if sous_commande == "brin":
        return afficher_brin(etat.get("brin", []))
    brin = marquer_brin(tresser(etat.get("files", {})))
    etat["brin"] = brin
    enregistrer_entonnoir(etat)
    print("Brin tisse : " + str(len(brin)) + " mission(s) (deterministe : meme contenu = meme sequence).")
    return afficher_brin(brin)
