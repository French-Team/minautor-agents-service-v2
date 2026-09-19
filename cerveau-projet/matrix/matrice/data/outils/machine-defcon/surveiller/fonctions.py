"""Surveiller : les DECLENCHEURS declares sont-ils REMPLIS ? (voie A, EO-181)

Le LANCEMENT du mesureur et la POSE du niveau sont injectes, pour que le cobaye
eprouve la DECISION sans toucher au niveau reel : aucun test ne doit mettre la
Matrice en securite pour de vrai.

Ce module n'ecrit JAMAIS le classeur : poser un niveau passe par la PORTE de la
machine (`monter`), qui seule journalise la transition et declenche la pause
automatique de defcon 5.
"""
import subprocess
import sys
from pathlib import Path

from cible import racine_matrice
from constants import DECLENCHEURS, NIVEAU_NORMAL


def chemin_mesureur(declencheur):
    """Le chemin ABSOLU du mesureur, ancre sur la racine de la Matrice.

    Les chemins de la table sont relatifs a matrix/ : la racine se RESOUT
    (moteur partage cible.py), jamais le cwd (convention 1.1).
    """
    return racine_matrice(__file__) / Path(declencheur["mesureur"])


def lancer_mesureur(declencheur, delai=600):
    """(code, motif) : le verdict de la porte mesureuse. code None = non joignable."""
    chemin = chemin_mesureur(declencheur)
    if not chemin.is_file():
        return None, "mesureur INTROUVABLE : " + str(chemin)
    commande = [sys.executable, str(chemin)] + list(declencheur["arguments"])
    try:
        resultat = subprocess.run(commande, capture_output=True, timeout=delai)
    except (OSError, subprocess.SubprocessError) as erreur:
        return None, "mesureur en echec (" + type(erreur).__name__ + ")"
    return resultat.returncode, "code " + str(resultat.returncode)


def evaluer(table=None, lancer=None):
    """Les verdicts, un par declencheur : (id, rempli, niveau, motif). FONCTION PURE.

    Un mesureur NON JOIGNABLE ou EN ECHEC n'est PAS rempli : il est rapporte.
    Un echec de mesure ne doit jamais passer pour un non-declenchement muet.
    """
    table = DECLENCHEURS if table is None else table
    lancer = lancer_mesureur if lancer is None else lancer
    verdicts = []
    for declencheur in table:
        code, motif = lancer(declencheur)
        verdicts.append((declencheur["id"], code is not None and code == 1,
                         int(declencheur["niveau"]), motif))
    return verdicts


def decider(verdicts, niveau_courant):
    """(niveau a poser, motifs) : le PLUS HAUT declencheur NON ENCORE atteint.

    Deux garanties, et c'est la raison d'etre de cette fonction pure : JAMAIS de
    baisse (un declencheur MONTE ; redescendre est une DECISION, par la porte) et
    JAMAIS de re-pose inutile (idempotent : pas de bruit dans le journal des
    transitions quand le niveau est deja tenu).
    """
    if niveau_courant is None:
        niveau_courant = NIVEAU_NORMAL
    remplis = [(niveau, ident, motif) for ident, rempli, niveau, motif in verdicts if rempli]
    if not remplis:
        return None, []
    niveau = max(un_niveau for un_niveau, _, _ in remplis)
    if niveau <= int(niveau_courant):
        return None, []
    motifs = [ident + " -> defcon " + str(un_niveau) + " : " + motif
              for un_niveau, ident, motif in remplis if un_niveau == niveau]
    return niveau, motifs
