# -*- coding: ascii -*-
"""routine : harnais-jarvis -- detecter les ecarts de comportement de
JARVIS et alerter Vision (le seul habilite a modifier JARVIS).

Declenchee par le manifest des routines (D15) a intervalle regle.
Le harnais scanne les files JARVIS en lecture seule, applique les regles
de harnais-jarvis-data.json et ecrit UNE alerte format JARVIS standard
dans inbox/vision.jsonl (dedup : un meme ecart n est signale qu une fois).
"""
import os
import sys

# P10 : racine via os_path
_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "tools-commun", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = trouver_racine(__file__)
_sys_dir_h = os.path.join(RACINE, "cerveau-projet", "freelance",
                          "tools-commun", "harnais-jarvis", "fonctions")
sys.path.insert(0, _sys_dir_h)
from harnais_jarvis import verifier_comportement, rapport


def main():
    ecarts, nouveaux = verifier_comportement(alerter=True)
    if ecarts:
        for ligne in rapport(ecarts)[:10]:
            print("  %s" % ligne)
        print("[HARNAIS-JARVIS] %d ecart(s) detecte(s), "
              "%d alerte(s) envoyee(s) a Vision"
              % (len(ecarts), len(nouveaux)))
    else:
        print("[HARNAIS-JARVIS] AUCUN ECART : JARVIS se comporte "
              "conformement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
