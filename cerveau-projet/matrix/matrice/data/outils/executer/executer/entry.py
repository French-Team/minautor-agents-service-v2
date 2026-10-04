"""Entree du verbe executer : execution Python seule (pas de shell)."""
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
    valider_commande,
    parser_commande,
    executer_python,
    formater_sortie,
    extraire_options,
)
from constants import NOMS_OPTIONS_EXECUTER


def executer(arguments):
    """Verbe executer : --cmd <commande> [--timeout N] [--contenu-chemin @file] [--json]
    
    Codes retour :
      0 = succes (code retour commande = 0)
      1 = echec (code retour commande != 0)
      2 = refus (commande interdite, timeout, erreur)
    """
    options = extraire_options(arguments, NOMS_OPTIONS_EXECUTER)

    # Recupere la commande
    cmd = options.get("cmd", "").strip()
    
    # Anti-heredoc : --contenu-chemin @file
    contenu_chemin = options.get("contenu-chemin", "").strip()
    if contenu_chemin:
        if contenu_chemin.startswith("@"):
            fichier = contenu_chemin[1:].strip()
            try:
                from pathlib import Path
                p = Path(fichier)
                if not p.is_file():
                    print("ERREUR : fichier @file introuvable : " + fichier)
                    return 2
                cmd = p.read_text(encoding="utf-8").strip()
            except OSError as e:
                print("ERREUR : lecture @file : " + str(e))
                return 2
        else:
            cmd = contenu_chemin

    if not cmd:
        print("ERREUR : --cmd requis. Ex: --cmd \"python3 -m py_compile foo.py\"")
        print("Usage: executer --cmd <commande> [--timeout 60] [--json]")
        return 2

    # Options
    timeout = int(options.get("timeout", "60"))
    mode_json = "json" in options

    # Validation commande
    est_valide, msg_erreur = valider_commande(cmd)
    if not est_valide:
        print("REFUS : " + msg_erreur)
        print("Commande refusee : " + cmd)
        return 2

    # Parse (sans shell)
    args, parse_err = parser_commande(cmd)
    if parse_err:
        print("ERREUR parse : " + parse_err)
        return 2
    if not args:
        print("ERREUR : commande vide apres parse")
        return 2

    # Execution
    stdout, stderr, code, duree_ms, exec_err = executer_python(
        args, timeout=timeout
    )
    if exec_err:
        print("ERREUR execution : " + exec_err)
        return 2

    # Sortie
    print(formater_sortie(stdout, stderr, code, duree_ms, mode_json))

    return 0 if code == 0 else 1
