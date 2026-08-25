#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: vision
#   commun: false
"""
routines-server.py -- DAEMON RESIDENT des routines JARVIS (D15).

Decision utilisateur 2026-08-25 : les declenchements des routines
tournent EN PERMANENCE - ce daemon tick les routines en boucle,
independamment des invocations de jarvis.py (qui restent un filet de
securite). Lance par jarvis.py demarrage via fonctions/hooks.py
(detache, survit a la console) ; arrete par jarvis.py arret.

Usage :
    python3 routines-server.py --boucle [--intervalle N]

Boucle : toutes les N secondes (defaut 30), executer les routines du
manifest dont l intervalle est ecoule (mem logique que le tic de
jarvis.py - une seule source : fonctions/routines.py).

Proprietaire : Vision (perimetre JARVIS)
Version : 0.1.0
"""

import os
import sys
import time
from pathlib import Path

_d = os.path.dirname(os.path.abspath(__file__))
# P10 : la racine se DETECTE en remontant jusqu'a AGENTS.md
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)
sys.path.insert(0, str(RACINE / "cerveau-projet" / "freelance"
                       / "tools-commun" / "jarvis" / "fonctions"))

VERSION = "0.1.0"
PID_FILE = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
    / "jarvis" / "routines-server.pid"


def ecrire_pid():
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")


def nettoyer_pid():
    try:
        PID_FILE.unlink()
    except OSError:
        pass


def boucler(intervalle_secondes):
    from routines import executer_routines
    ecrire_pid()
    print("[ROUTINES-SERVER] daemon demarre (tic toutes les %ds, pid %d)"
          % (intervalle_secondes, os.getpid()), flush=True)
    try:
        while True:
            try:
                executer_routines()
            except Exception as e:  # le daemon ne meurt jamais sur un tic
                print("[ROUTINES-SERVER] ERREUR tic : %s" % e, flush=True)
            time.sleep(intervalle_secondes)
    finally:
        nettoyer_pid()


def main():
    if "--boucle" not in sys.argv:
        print("usage : python3 routines-server.py --boucle [--intervalle N]")
        return 2
    intervalle = 30
    if "--interval" in " ".join(sys.argv) or "--intervalle" in sys.argv:
        try:
            intervalle = int(sys.argv[sys.argv.index("--intervalle") + 1])
        except (ValueError, IndexError):
            pass
    boucler(intervalle)
    return 0


if __name__ == "__main__":
    sys.exit(main())
