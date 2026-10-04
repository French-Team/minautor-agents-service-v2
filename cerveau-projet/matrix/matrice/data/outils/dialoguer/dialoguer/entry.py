"""Entree du verbe dialoguer : interaction createur (Flux 2 seul)."""
import sys
import os

# L-013 : aucun niveau compte a la main. Le dossier de CET outil est celui qui
# porte son commun.py (marqueur) : la remontee est VERIFIEE, jamais supposee (MO-177).
REPERTOIRE_ENTREE = os.path.dirname(os.path.abspath(__file__))
REPERTOIRE_OUTIL = os.path.dirname(REPERTOIRE_ENTREE)
if not os.path.isfile(os.path.join(REPERTOIRE_OUTIL, "commun.py")):
    raise RuntimeError("Dossier de l'outil introuvable depuis " + REPERTOIRE_ENTREE
                       + " : commun.py est absent de " + REPERTOIRE_OUTIL)
sys.path.insert(0, REPERTOIRE_OUTIL)

from commun import (
    valider_question,
    valider_choix,
    poser_question,
    tracer_decision,
    formater_reponse,
    extraire_options,
)
from constants import NOMS_OPTIONS_DIALOGUER


def dialoguer(arguments):
    """Verbe dialoguer : --question <texte> [--choix a,b,c] [--timeout N] [--json]
    
    Codes retour :
      0 = reponse recue
      1 = timeout
      2 = erreur
    """
    options = extraire_options(arguments, NOMS_OPTIONS_DIALOGUER)

    question = options.get("question", "").strip()
    choix_str = options.get("choix", "").strip()
    timeout = int(options.get("timeout", "0"))
    mode_json = "json" in options

    # Validation
    est_valide, msg = valider_question(question)
    if not est_valide:
        print("ERREUR : " + msg)
        return 2

    choix, msg_choix = valider_choix(choix_str) if choix_str else ([], "")
    if msg_choix:
        print("ERREUR choix : " + msg_choix)
        return 2

    # Pose la question
    reponse, code = poser_question(question, choix=choix, timeout=timeout)

    # Trace
    if code == 0:
        tracer_decision("actuelle", question, reponse)

    # Sortie
    print(formater_reponse(reponse, code, mode_json))
    return code
