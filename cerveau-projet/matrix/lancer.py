#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lancer.py -- lanceur UNIQUE des outils de la Matrice.

Le NOM suffit : le lanceur resout l outil vers son main.py, pose l INTERPRETEUR
(sys.executable) et le CHEMIN ABSOLU -- la commande n est plus jamais ecrite a la
main (question du createur : moins d erreurs de syntaxe).

Usage :
  python3 cerveau-projet/matrix/lancer.py <outil> [arguments...]
  python3 cerveau-projet/matrix/lancer.py --lister
  python3 cerveau-projet/matrix/lancer.py --aide

Resolution (source UNIQUE, EO-287 : matrice/data/commun/resolution_outils.py) :
  1. un outil de la Matrice : matrix/matrice/data/outils/<nom>/main.py
  2. une routine            : matrix/matrice/routines/<nom>/main.py
  3. un chemin explicite    : un fichier .py EXISTANT (chemin ancre)

Refus NOMMES (code 2) : nom inconnu (avec les noms proches), aucun main.py.
Le lanceur ne devine JAMAIS : il DIT quoi faire.

Cette facade ne recopie AUCUNE regle de resolution : elle lit le module partage,
comme les appelants internes (un seul domicile, M-076).
"""

import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
DOSSIER_COMMUN = RACINE / "matrice" / "data" / "commun"
if not DOSSIER_COMMUN.is_dir():
    print("REFUS : data/commun introuvable : " + str(DOSSIER_COMMUN))
    sys.exit(2)
sys.path.insert(0, str(DOSSIER_COMMUN))

from resolution_outils import entrer_outils, resoudre  # noqa: E402


def lister():
    for famille, nom, _ in entrer_outils():
        print(famille + "  " + nom)
    return 0


def main():
    arguments = sys.argv[1:]
    if not arguments:
        print(__doc__)
        return 2
    if arguments[0] in ("--aide", "-h", "--help"):
        print(__doc__)
        return 0
    if arguments[0] == "--lister":
        return lister()
    nom, suite = arguments[0], arguments[1:]
    cible, refus = resoudre(nom)
    if refus is not None:
        print("REFUS : " + refus)
        return 2
    interieur = subprocess.run([sys.executable, str(cible), *suite])
    return interieur.returncode


if __name__ == "__main__":
    sys.exit(main())
