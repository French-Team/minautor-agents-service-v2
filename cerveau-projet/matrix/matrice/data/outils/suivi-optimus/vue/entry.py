"""Categorie vue : genere le fichier markdown dedie (decision createur 2026-09-09).

Interface entre main.py et les fonctions simples (vue/fonctions.py).
"""
from commun import lire_evenements
from constants import ACTIONS, CHEMIN_VUE, ENCODAGE
from vue.fonctions import composer_vue


def executer(arguments):
    evenements = lire_evenements()
    contenu = "\n".join(composer_vue(evenements, ACTIONS)).rstrip() + "\n"
    CHEMIN_VUE.write_text(contenu, encoding=ENCODAGE)
    print(
        "Vue suivi-optimus regeneree : " + str(CHEMIN_VUE)
        + " (" + str(len(evenements)) + " evenement(s))"
    )
    return 0