"""Point d'entree global de l'entonnoir (echelons 0-3).

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py deposer  --theme "..." --objectif "..." [--urgence u] [--source s]
    python main.py classer  --id E-XXX --type <dev|reparation|doc|audit|revision> [--categorie c]
    python main.py urgencer --id E-XXX --urgence <bloquante|haute|normale|basse>
    python main.py retirer  --id E-XXX    (sortie PROPRE du vrac, M-058)
    python main.py tresse brin    (affiche le brin tisse)
    python main.py tresse tisser  (recompose le brin : deterministe)
    python main.py file     (affiche vrac + files, echelon par echelon)
"""
import sys

from classer.entry import executer as classer_executer
from retirer.entry import executer as retirer_executer
from stockage import charger_entonnoir
from tresse.entry import executer as tresse_executer
from urgencer.entry import executer as urgencer_executer
from vrac.entry import executer as deposer_executer

COMMANDES = {
    "deposer": deposer_executer,
    "classer": classer_executer,
    "urgencer": urgencer_executer,
    "retirer": retirer_executer,
    "tresse": tresse_executer,
}


def afficher_file():
    """Affiche l'entonnoir echelon par echelon (le vrac puis chaque file-type)."""
    etat = charger_entonnoir()
    vrac = etat.get("vrac", [])
    print("== ECHELON 0 : vrac (" + str(len(vrac)) + " mission(s)) ==")
    for mission in vrac:
        print(
            "  " + mission["id"] + "  urgence " + mission["urgence"]
            + "  " + mission["theme"] + " -- " + mission["objectif"]
            + "  (source " + mission["source"] + ")"
        )
    files = etat.get("files", {})
    for type_file, missions in files.items():
        print("== FILE " + type_file + " (" + str(len(missions)) + " mission(s)) ==")
        for mission in missions:
            print(
                "  " + mission["id"] + "  [" + mission["categorie"] + "]  urgence "
                + mission["urgence"] + "  " + mission["theme"]
            )
    return 0


def principal(arguments):
    if not arguments:
        print(__doc__)
        return 2
    if arguments[0] == "file":
        return afficher_file()
    if arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
