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

# --- DOMICILE DU LANCEMENT (EO-430 / MO-416, lot -- fin du residu) -----------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
# Bloc AUTOSUFFISANT : il ne depend ni de l ordre des imports du fichier, ni de la
# presence d un `import subprocess` de module (mesure du 2026-09-25 : deux fichiers
# casses par ces deux pieges, invisibles au py_compile).
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())


def popen_enfant(*arguments, **options):
    """Le lancement DETACHE de cet outil : jamais de fenetre."""
    return subprocess.Popen(*arguments, **options, **drapeaux_popen())

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
        resultat = lancer_enfant(commande, capture_output=True, timeout=delai)
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
