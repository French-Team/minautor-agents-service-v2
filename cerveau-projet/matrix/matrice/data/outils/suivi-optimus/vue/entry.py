"""Categorie vue : genere le fichier markdown dedie (decision createur 2026-09-09).

Interface entre main.py et les fonctions simples (vue/fonctions.py).
"""
from commun import lire_evenements, lire_inbox
from constants import ACTIONS, CHEMIN_VUE, ENCODAGE, CHEMIN_INBOX
from vue.fonctions import composer_vue


def executer(arguments):
    evenements = lire_evenements()
    # Lire l'inbox pour les missions en attente.
    inbox_evenements = lire_inbox() if CHEMIN_INBOX.exists() else []
    contenu = "\n".join(composer_vue(evenements, ACTIONS, inbox_evenements)).rstrip() + "\n"
    CHEMIN_VUE.write_text(contenu, encoding=ENCODAGE)
    print(
        "Vue suivi-optimus regeneree : " + str(CHEMIN_VUE)
        + " (" + str(len(evenements)) + " evenement(s), "
        + str(len(inbox_evenements)) + " en attente)"
    )
    return 0