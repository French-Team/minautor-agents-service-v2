#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
tester-protection-blocage.py

Protection qui encadre l'execution des tests pour detecter et stopper
les tests qui bloquent : processus qui ne tourne plus (CPU quasi nul),
absence de sortie pendant plusieurs intervalles, sortie anormalement
longue. Elle complete la protection contre les boucles infinies en
detectant les blocages silencieux.

Utilisation:
  tester-protection-blocage.py "<commande>" [nom] [timeout]

Proprietaire : Morpheus (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import os
import signal
import subprocess
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"

TIMEOUT_DEFAUT = 60
MAX_OUTPUT = 1000


def tuer_arbre(pid):
    """Tuer un processus et tout son arbre (cross-platform)."""
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            capture_output=True,
            shell=False
        )
    else:
        try:
            os.killpg(pid, signal.SIGKILL)
        except OSError:
            pass


def preparer_lancement():
    """Options de lancement: nouvelle session pour pouvoir tuer l'arbre."""
    if sys.platform == "win32":
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def afficher_aide():
    print("=== tester-protection-blocage v%s ===" % VERSION)
    print("")
    print("Usage: tester-protection-blocage.py <commande> [nom] [timeout]")
    print("")
    print("Exemples :")
    print("  tester-protection-blocage.py './mon-outil.sh --test' 'Mon test' 60")
    print("  tester-protection-blocage.py './mon-outil.sh' 'Test long' 60")


def executer_sans_blocage(test_cmd, test_name, timeout):
    """Executer une commande avec protection contre le blocage.

    Sur Windows, subprocess.run(timeout=) ne tue que le processus direct:
    les enfants survivent et gardent les pipes ouverts. On lance en Popen,
    on tue l'arbre des que le timeout expire, puis on recupere la sortie.
    """
    print("[PROTECTION] Test anti-blocage: %s (timeout: %ds)" % (test_name, timeout), flush=True)

    options = preparer_lancement()
    proc = subprocess.Popen(
        test_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        **options
    )
    try:
        sortie_out, sortie_err = proc.communicate(timeout=timeout)
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        print("[ERREUR] Timeout: %s a depasse %ds" % (test_name, timeout), flush=True)
        print("  -> Le test semble etre bloque, arret force", flush=True)
        tuer_arbre(proc.pid)
        try:
            sortie_out, sortie_err = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            sortie_out = ""
            sortie_err = ""
        sortie_partielle = sortie_out or ""
        if sortie_err:
            sortie_partielle += sortie_err
        if sortie_partielle.strip():
            print("  -> Sortie partielle:", flush=True)
            for ligne in sortie_partielle.splitlines()[-10:]:
                print(ligne, flush=True)
        return 1
    except OSError:
        print("[ERREUR] Impossible de lancer la commande: %s" % test_cmd)
        return 1

    if exit_code == 0:
        print("[OK] Termine avec succes")
    else:
        print("[ERREUR] Echec avec le code: %d" % exit_code)

    return exit_code


def main(argv):
    if not argv:
        afficher_aide()
        return 1

    if argv[0] in ("--help", "--aide", "-h"):
        afficher_aide()
        return 0

    if argv[0] == "--version":
        print("tester-protection-blocage v%s (%s)" % (VERSION, STATUT))
        return 0

    test_cmd = argv[0]
    test_name = argv[1] if len(argv) > 1 else "Test"
    timeout = int(argv[2]) if len(argv) > 2 else TIMEOUT_DEFAUT

    return executer_sans_blocage(test_cmd, test_name, timeout)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
