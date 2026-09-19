"""Entree du verbe signal : cameleon signale un probleme outil a la Matrice."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commun import (
    valider_signal,
    valider_expediteur,
    construire_message,
    deposer_signal,
    formater_sortie,
    extraire_options,
)
from constants import EXPEDITEURS, NOMS_OPTIONS, NIVEAUX


def signaler(arguments):
    """Verbe signal : --outil <nom> --niveau <critique|haute|moyenne|basse>
    --description <texte> [--mission <id>] [--erreur <texte>]
    [--expediteur <cameleon|routine|matrice>] [--json]
    
    Codes retour :
      0 = signal depose
      2 = erreur (validation)
    """
    options = extraire_options(arguments, NOMS_OPTIONS)

    outil = options.get("outil", "").strip()
    niveau = options.get("niveau", "").strip()
    description = options.get("description", "").strip()
    mission = options.get("mission", "").strip()
    erreur = options.get("erreur", "").strip()
    expediteur, msg_expediteur = valider_expediteur(options.get("expediteur", ""))
    mode_json = "json" in options

    # Validation
    if msg_expediteur:
        print("ERREUR : " + msg_expediteur)
        print("  Expediteurs autorises : " + ", ".join(EXPEDITEURS))
        return 2
    est_valide, msg = valider_signal(outil, niveau, description)
    if not est_valide:
        print("ERREUR : " + msg)
        print("")
        print("Usage : signaler --outil <nom> --niveau <niveau> --description <texte>")
        print("        [--mission <id>] [--erreur <texte>] [--json]")
        print("")
        print("Niveaux : " + ", ".join(NIVEAUX.keys()))
        for n, info in NIVEAUX.items():
            print(f"  {n:10s} {info['desc']}")
        return 2

    # Construction
    message = construire_message(outil, niveau, description, mission, erreur, expediteur)

    # Depot
    succes, msg_erreur = deposer_signal(message)
    if not succes:
        print("ERREUR depot : " + msg_erreur)
        return 2

    # Sortie
    print(formater_sortie(message, mode_json))
    return 0
