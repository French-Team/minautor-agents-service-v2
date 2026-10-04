"""Categorie verifier : le JUGE d une source -- il ACCUSE, il ne repare pas.

LECTURE SEULE, toujours : ce verbe n ecrit rien, quoi qu il trouve. Une incoherence
qu on repare dans le meme geste que celui qui la mesure est une incoherence qu on ne
peut plus compter.

CODE : 0 = aucune incoherence, 1 = des incoherences (nommees une par une), 2 = refus
(source inconnue, fichier illisible). Le code 1 est un VERDICT, pas une panne : c est
ce qui permet de le brancher dans un controle.
"""
from commun import extraire_options
from constants import SOURCE_PARCOURS, SOURCES
from mermaid.entry import modele_de

NOMS_OPTIONS = ("source", "theme", "arbre")

USAGE = (
    "    python main.py verifier [--source " + "|".join(SOURCES) + "] [--theme <NOM>]\n"
    "                             [--arbre <fichier.json>]\n"
    "                                       (juge la source : fichiers absents, themes\n"
    "                                       orphelins, renvois casses, cases vides, ids et\n"
    "                                       categories hors liste. LECTURE SEULE)\n"
)


def executer(arguments):
    """Juge la source demandee et rend son verdict (0, 1 ou 2)."""
    options = extraire_options(arguments, NOMS_OPTIONS)
    source = (options.get("source") or SOURCE_PARCOURS).strip().lower()
    theme = (options.get("theme") or "").strip()
    arbre = (options.get("arbre") or "").strip()
    modele, incoherences = modele_de(source, theme, arbre)
    if modele is None:
        print("REFUS : source inconnue (" + repr(source) + "). Sources : "
              + ", ".join(SOURCES) + ".")
        print(USAGE)
        return 2
    incoherences = incoherences or []
    print("VERDICT : " + modele["titre"])
    if not incoherences:
        print("  AUCUNE INCOHERENCE -- la source tient ("
              + str(len(modele["noeuds"])) + " noeud(s) mesure(s)).")
        return 0
    print("  " + str(len(incoherences)) + " INCOHERENCE(S) :")
    for numero, incoherence in enumerate(incoherences, 1):
        print("    " + str(numero).rjust(3) + ". [" + incoherence.get("code", "?") + "] "
              + str(incoherence.get("detail", "")))
    return 1
