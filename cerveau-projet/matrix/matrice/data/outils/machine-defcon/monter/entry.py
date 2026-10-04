"""Categorie monter : montee libre (sauts permis) vers defcon 3-5."""


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

from commun import (
    appliquer_transition,
    charger_classeur,
    extraire_options,
    journaliser_transition,
    trouver_defcon,
)
from constants import NOM_OUTIL_PAUSE, NOMS_NIVEAUX
from monter.fonctions import verifier_montee

# M-080 : a defcon 5, la Matrice met la session-matrix EN PAUSE (protocole
# de pause). Le cameleon est arrete, la maintenance est reveillee. La pause
# part par la PORTE UNIQUE pause-session (sous-processus, jamais bloquant ici).

def declencher_pause_auto():
    """Declenche la pause de session-matrix si defcon 5 vient d'etre pose."""
    import subprocess
    import sys

    from resolution_outils import OutilIntrouvable, chemin_outil

    # EO-287 : l outil se NOMME ; la resolution et son refus nomme vivent au
    # domicile partage -- un chemin recopie ne se plaint jamais, il plante.
    try:
        principal = chemin_outil(NOM_OUTIL_PAUSE)
    except OutilIntrouvable as refus:
        print("ECART : " + str(refus))
        return
    resultat = lancer_enfant(
        [sys.executable, str(principal), "pause", "--raison", "defcon 5 automatique"],
        capture_output=True,
        text=True,
        check=False,
    )
    if resultat.returncode == 0:
        print("PROTOCOLE PAUSE (M-080) : session-matrix mise en pause, cameleon notifie (maintenance).")
        for ligne in (resultat.stdout or "").strip().splitlines():
            print("  " + ligne)
    else:
        print("Pause automatique non effectuee (code " + str(resultat.returncode) + ") :")
        for ligne in (resultat.stdout or "").strip().splitlines():
            print("  " + ligne)

NOMS_OPTIONS = ("niveau", "raison")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    if "niveau" not in options or not options.get("raison"):
        print("Usage : python main.py monter --niveau <3-5> --raison \"...\"")
        return 2
    try:
        cible = int(options["niveau"])
    except ValueError:
        print("Usage : --niveau <1-5>")
        return 2
    raison = options["raison"]

    donnees = charger_classeur()
    courant, entree = trouver_defcon(donnees)
    if entree is None:
        print("Variable 'defcon' absente du classeur : la definir via bdd-variables.")
        return 1
    code, message = verifier_montee(courant, cible)
    if code != 0:
        print(message)
        return code

    source = "machine-defcon monter"
    appliquer_transition(donnees, entree, cible, source)
    journaliser_transition(courant, cible, raison, source)
    print(
        "defcon " + str(courant) + " -> " + str(cible)
        + " (" + NOMS_NIVEAUX[cible] + ") -- raison : " + raison
    )
    if cible == 5:
        print(
            "DEFCON 5 : l'agent par defaut est stoppe, maintenance reveillee "
            "-- seules les missions themees DEFCON restent injectables."
        )
        declencher_pause_auto()
    return 0
