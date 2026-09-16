"""Categorie coherence : orchestre le croisement file du pilote <-> journal.

Interface entre main.py et les fonctions simples (coherence/fonctions.py).
"""
import argparse
from pathlib import Path

from constants import REPERTOIRE_MATRIX
from coherence.fonctions import controler


def executer(arguments):
    """Croise les DEUX traces d'optimus (file du pilote + journal suivi-optimus).

    Code 0 = file et journal d'accord (des dettes peuvent etre signalees).
    Code 1 = au moins un ECART (une trace affirme ce que l'autre ignore).
    """
    analyseur = argparse.ArgumentParser(
        description="Coherence entre la file du pilote OPTIMUS et le journal suivi-optimus"
    )
    analyseur.add_argument(
        "--racine", default=None,
        help="Racine matrix/ a controler (defaut : celle du depot ; sert aux cobayes)",
    )
    options = analyseur.parse_args(arguments)

    matrice = Path(options.racine).resolve() if options.racine else REPERTOIRE_MATRIX
    ecarts, dettes, resume = controler(matrice)

    print("COHERENCE FILE <-> JOURNAL -- racine : " + str(matrice))
    if resume:
        print("  " + resume)
    for ecart in ecarts:
        print("ECART : " + ecart)
    for dette in dettes:
        print("DETTE : " + dette)
    print("RESULTAT : " + str(len(ecarts)) + " ecart(s), " + str(len(dettes)) + " dette(s)")
    return 0 if not ecarts else 1
