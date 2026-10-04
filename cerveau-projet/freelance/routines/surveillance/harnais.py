# -*- coding: ascii -*-
"""routine : harnais -- detecter les ecarts de comportement de JARVIS et
alerter Vision (le seul habilite a modifier JARVIS). Ex-harnais-jarvis,
renommee 2026-08-26 : nom simple qui exprime ce qu'elle est (la routine,
pas l'outil tools-commun/harnais-jarvis/ qui garde son nom).

Declenchee par le manifest des routines (D15) a intervalle regle.
Le harnais scanne les files JARVIS en lecture seule, applique les regles
de harnais-jarvis-data.json et ecrit UNE alerte format JARVIS standard
dans inbox/vision.jsonl (dedup : un meme ecart n est signale qu une fois).
Historise SOUS SON NOM uniquement quand de NOUVEAUX ecarts apparaissent
(evenementiel - la routine est un element surveille, rouge G4).
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
        print("[HARNAIS] %d ecart(s) detecte(s), "
              "%d alerte(s) envoyee(s) a Vision"
              % (len(ecarts), len(nouveaux)))
        if nouveaux:
            # Tracabilite : la routine harnais est un element surveille,
            # elle historise SOUS SON NOM quand de NOUVEAUX ecarts
            # apparaissent (rouge G4). Pas de trace si ecarts connus.
            try:
                _fo = RACINE / "cerveau-projet" / "freelance" / \
                    "tools-commun" / "os_path" / "fonctions"
                _fj = RACINE / "cerveau-projet" / "freelance" / \
                    "tools-commun" / "jarvis" / "fonctions"
                for p in (_fo, _fj):
                    if str(p) not in sys.path:
                        sys.path.insert(0, str(p))
                from historique import historiser
                historiser("harnais",
                           "%d nouveau(x) ecart(s) de comportement"
                           % len(nouveaux),
                           "R", session="session-freelance")
            except Exception:
                pass
    else:
        print("[HARNAIS] AUCUN ECART : JARVIS se comporte conformement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
