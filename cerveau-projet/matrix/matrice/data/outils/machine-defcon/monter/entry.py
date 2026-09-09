"""Categorie monter : montee libre (sauts permis) vers defcon 3-5."""
from commun import (
    appliquer_transition,
    charger_classeur,
    extraire_options,
    journaliser_transition,
    trouver_defcon,
)
from constants import NOMS_NIVEAUX
from monter.fonctions import verifier_montee

# M-080 : a defcon 5, la Matrice met la session-matrix EN PAUSE (protocole
# de pause). Le cameleon est arrete, la maintenance est reveillee. La pause
# part par la PORTE UNIQUE pause-session (sous-processus, jamais bloquant ici).

def declencher_pause_auto():
    """Declenche la pause de session-matrix si defcon 5 vient d'etre pose."""
    import subprocess
    import sys
    from pathlib import Path

    chemin_outil = Path(__file__).resolve().parent.parent.parent / "pause-session"
    if not (chemin_outil / "main.py").is_file():
        print("ECART : outil pause-session introuvable pour la pause automatique.")
        return
    resultat = subprocess.run(
        [sys.executable, str(chemin_outil / "main.py"), "pause", "--raison", "defcon 5 automatique"],
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

NOMS_OPTIONS = ("--niveau", "--raison")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    if "--niveau" not in options or not options.get("--raison"):
        print("Usage : python main.py monter --niveau <3-5> --raison \"...\"")
        return 2
    try:
        cible = int(options["--niveau"])
    except ValueError:
        print("Usage : --niveau <1-5>")
        return 2
    raison = options["--raison"]

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
