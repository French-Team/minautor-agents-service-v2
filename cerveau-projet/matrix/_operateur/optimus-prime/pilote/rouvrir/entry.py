"""Categorie rouvrir : RENDRE A FAIRE une mission close par erreur.

MO-548 / EO-553. Interface entre main.py et les fonctions de la categorie.

Ce que ce verbe NE fait PAS, et c est delibere : il ne reecrit pas le bilan
fautif (il le RETIRE et le conserve), il ne touche pas au journal des fins deja
posees, et il ne cree aucune mission. Il ne fait que remettre en attente une
mission dont la cloture ne tient pas.
"""
from commun import charger_file, extraire_options
from rouvrir.fonctions import rouvrir_mission

NOMS_OPTIONS = ("id", "motif")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = (options.get("id") or "").strip().upper()
    motif = (options.get("motif") or "").strip()
    if not identifiant:
        print('Usage : python main.py rouvrir --id MO-00X --motif "..."')
        print("        Le --id est celui d une mission CLOSE de la FILE ; le motif est")
        print("        OBLIGATOIRE et doit NOMMER ce qu il retire : une rouverture se")
        print("        TRACE, et une trace qui ne dit pas quoi elle annule n est rien.")
        return 2
    return rouvrir_mission(charger_file, identifiant, motif)
