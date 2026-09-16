"""Categorie vue : genere le fichier markdown dedie (decision createur 2026-09-09).

Interface entre main.py et les fonctions simples (vue/fonctions.py).
"""
from commun import lire_evenements
from constants import ACTIONS, CHEMIN_VUE, ENCODAGE, CHEMIN_FILE_PILOTE, CHEMIN_JOURNAL_MISSIONS
from vue.fonctions import composer_vue, lire_attente_pilote, lire_attente_journal


def executer(arguments):
    evenements = lire_evenements()
    # File du pilote OPTIMUS (en-attente/en-cours, revision createur E-072).
    attente_pilote = lire_attente_pilote(CHEMIN_FILE_PILOTE) if CHEMIN_FILE_PILOTE.exists() else []
    # Journal OPTIMUS (mission-creee sans terminee).
    attente_pilote += [i for i in lire_attente_journal(CHEMIN_JOURNAL_MISSIONS) if i not in attente_pilote]
    contenu = "\n".join(composer_vue(evenements, ACTIONS, attente_pilote)).rstrip() + "\n"
    CHEMIN_VUE.write_text(contenu, encoding=ENCODAGE)
    print(
        "Vue suivi-optimus regeneree : " + str(CHEMIN_VUE)
        + " (" + str(len(evenements)) + " evenement(s), "
        + str(len(attente_pilote)) + " en attente)"
    )
    return 0