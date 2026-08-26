# -*- coding: ascii -*-
"""fonctions/lecons.py - Lecons du harnais v2 (D10 : bible des lecons).

Le harnais DIFFUSE les lecons apprises par les agents (depuis la BDD
bdd-lecons) : avant chaque action, l agent voit les apprentissages
recents pertinents -- sans avoir a chercher (PROTOCOLE 22 : le harnais
donne, l agent n a pas a reflechir).

Tolerant : si la BDD n existe pas encore, retourne un message discret
au lieu de planter (le harnais ne bloque JAMAIS sur une lecon).
"""

import os
import sys

# BDD des lecons v2 (outil bdd-lecons, D10)
_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "bdd-lecons", "fonctions")
if os.path.isdir(_sys_dir):
    sys.path.insert(0, _sys_dir)

BDD_EXISTE = os.path.isfile(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "bdd-lecons",
    "lecons.db"))

try:
    from bdd_lecons import lister, chercher
except ImportError:
    lister = None
    chercher = None


def rappels_lecons(agent="", categorie="", n=2):
    """Retourner les n lecons recentes pertinentes, pretes a afficher.

    Priorite : lecons de l agent (si agent fourni), puis lecons de la
    categorie (si fournie), sinon lecons globales recentes.
    Retourne une liste de messages '[date] agent (categorie): titre'.
    """
    if lister is None or not BDD_EXISTE:
        return ["[BDD lecons absente - la bible v2 (D10) n est pas encore "
                "livree (outil bdd-lecons) ; les lecons ne peuvent pas etre "
                "rappelees]"]
    try:
        if agent:
            lignes = chercher(agent=agent)
        elif categorie:
            lignes = chercher(categorie=categorie)
        else:
            lignes = lister(n)
        if not lignes:
            return []
        return ["[%s] %s (%s): %s" % (l["date"][:10], l["agent"],
                                      l["categorie"], l["titre"])
                for l in lignes[:n]]
    except Exception:
        return ["[impossible de lire la BDD des lecons - signale, ne bloque "
                "pas]"]
