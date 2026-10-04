"""Categorie profil : etat et guidage de la fiche utilisateur USER-PROFIL.

Trois usages :
    python main.py profil            -- etat de la fiche (rempli / non rempli)
    python main.py profil --guider   -- guide sur le parcours USER-PROFIL
                                        (+ charge la mission si elle manque)
    python main.py profil --remplir  -- questionnaire interactif direct

La fiche et son etat viennent du motif PARTAGE
`matrice/data/commun/fiche_profil.py` : le pilote ne recopie jamais la
logique de remplissage (meme verite que la routine vigie-profil).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import constants  # noqa: F401  (pose data/commun dans sys.path, motif M-076)

from profil.fonctions import afficher_etat, etat_fiche, guider, remplir


def executer(arguments):
    """Executer une commande profil."""
    if "--remplir" in arguments:
        return remplir()
    etat = etat_fiche()
    if "--guider" in arguments:
        return guider(etat)
    return afficher_etat(etat)
