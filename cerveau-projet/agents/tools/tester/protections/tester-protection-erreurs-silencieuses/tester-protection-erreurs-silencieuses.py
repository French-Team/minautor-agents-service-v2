#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
tester-protection-erreurs-silencieuses.py

Protection qui encadre l'execution des tests pour detecter les erreurs
silencieuses : code de sortie inattendu, stdout vide, erreurs dans
stderr, mots-cles d'erreur dans la sortie. Chaque test est journalise
dans un dossier de logs et un rapport peut etre genere automatiquement.

Utilisation:
  tester-protection-erreurs-silencieuses.py "<commande>" [nom] [exit-attendu]

Proprietaire : Morpheus (outil partage)
Version : 0.2.1-py
Statut : prepare

Regle v0.2.11 du protocole creation-scripts-temporaires (demande
utilisateur 2026-08-16) : JAMAIS d ecriture vers le /tmp du systeme.
Les logs de cette protection vont dans le workspace :
<racine>/cerveau-projet/agents/traces/protection-logs/ (surclassable par
la variable d environnement PROTECTION_LOG_DIR).
"""

import datetime
import io
import os
import re
import signal
import subprocess
import sys

VERSION = "0.2.1-py"
STATUT = "prepare"

MOTS_CLES_ERREUR = ("error", "erreur", "failed", "echec", "exception", "fatal")


def racine_projet():
    """Remonte depuis le dossier de l outil jusqu a la racine (AGENTS.md)."""
    chemin = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(chemin, "AGENTS.md")):
            return chemin
        parent = os.path.dirname(chemin)
        if parent == chemin:
            return None
        chemin = parent


def log_dir():
    """Dossier des logs : TOUJOURS dans le workspace (jamais /tmp systeme)."""
    override = os.environ.get("PROTECTION_LOG_DIR")
    if override:
        return override
    racine = racine_projet()
    if racine:
        return os.path.join(racine, "cerveau-projet", "agents", "traces",
                            "protection-logs")
    return os.path.join(os.getcwd(), "cerveau-projet", "agents", "traces",
                        "protection-logs")


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
    print("=== tester-protection-erreurs-silencieuses v%s ===" % VERSION)
    print("")
    print("Usage: tester-protection-erreurs-silencieuses.py <commande> [nom] [exit-attendu]")
    print("")
    print("Exemples :")
    print("  tester-protection-erreurs-silencieuses.py './mon-outil.sh --test' 'Mon test' 0")
    print("  tester-protection-erreurs-silencieuses.py './mon-outil.sh' 'Test avec erreur' 1")


def executer_test_securise(test_cmd, test_name, expected_exit):
    """Executer un test avec verification des erreurs silencieuses."""
    print("[PROTECTION] Test securise: %s" % test_name)

    dossier_logs = log_dir()
    os.makedirs(dossier_logs, exist_ok=True)
    nom_clean = test_name.replace(" ", "_")
    log_file = os.path.join(dossier_logs, nom_clean + ".log")
    stdout_file = os.path.join(dossier_logs, nom_clean + "_stdout.log")
    stderr_file = os.path.join(dossier_logs, nom_clean + "_stderr.log")

    # Initialiser le log
    lignes_log = []
    lignes_log.append("=== Test: %s ===" % test_name)
    lignes_log.append("Date: %s" % datetime.datetime.now().isoformat())
    lignes_log.append("Commande: %s" % test_cmd)
    lignes_log.append("---")

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
        sortie_out, sortie_err = proc.communicate(timeout=120)
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        print("[ERREUR] Timeout: %s a depasse 120s, arret force" % test_name, flush=True)
        lignes_log.append("Resultat: TIMEOUT")
        tuer_arbre(proc.pid)
        try:
            sortie_out, sortie_err = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            sortie_out = ""
            sortie_err = ""
        with io.open(log_file, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lignes_log) + "\n")
        return 1
    except OSError:
        print("[ERREUR] Impossible de lancer la commande: %s" % test_cmd)
        return 1

    lignes_log.append("Code de sortie: %d" % exit_code)
    lignes_log.append("Attendu: %d" % expected_exit)

    erreurs = 0

    # Verifier le code de sortie
    if exit_code != expected_exit:
        print("[ERREUR] Code de sortie inattendu: %d (attendu: %d)" % (exit_code, expected_exit))
        lignes_log.append("Erreur: Code de sortie inattendu")
        erreurs += 1

    # Verifier si le stdout est vide
    if sortie_out.strip() == "":
        print("[ATTENTION] Sortie stdout vide")
        lignes_log.append("Attention: Sortie stdout vide")

    # Verifier si le stderr contient des erreurs
    if sortie_err.strip():
        print("[ATTENTION] Erreurs dans stderr:")
        for ligne in sortie_err.splitlines()[:5]:
            print(ligne)
        lignes_log.append("Erreur: Erreurs detectees dans stderr")
        erreurs += 1

    # Verifier les mots-cles d'erreur dans la sortie
    if re.search("|".join(MOTS_CLES_ERREUR), sortie_out, re.IGNORECASE):
        print("[ATTENTION] Mots-cles d'erreur detectes dans stdout")
        for ligne in sortie_out.splitlines():
            if re.search("|".join(MOTS_CLES_ERREUR), ligne, re.IGNORECASE):
                print(ligne)
        lignes_log.append("Erreur: Mots-cles d'erreur dans stdout")
        erreurs += 1

    # Enregistrer les sorties dans le log
    lignes_log.append("--- STDOUT ---")
    lignes_log.extend(sortie_out.splitlines())
    lignes_log.append("")
    lignes_log.append("--- STDERR ---")
    lignes_log.extend(sortie_err.splitlines())

    with io.open(log_file, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lignes_log) + "\n")

    if os.path.exists(stdout_file):
        os.remove(stdout_file)
    if os.path.exists(stderr_file):
        os.remove(stderr_file)

    if erreurs > 0:
        print("[ERREUR] %d erreur(s) detectee(s)" % erreurs)
        lignes_log.append("Resultat: ECHEC")
        return 1
    else:
        print("[OK] Test reussi sans erreur silencieuse")
        lignes_log.append("Resultat: SUCCES")
        return 0


def main(argv):
    if not argv:
        afficher_aide()
        return 1

    if argv[0] in ("--help", "--aide", "-h"):
        afficher_aide()
        return 0

    if argv[0] == "--version":
        print("tester-protection-erreurs-silencieuses v%s (%s)" % (VERSION, STATUT))
        return 0

    test_cmd = argv[0]
    test_name = argv[1] if len(argv) > 1 else "Test"
    expected_exit = int(argv[2]) if len(argv) > 2 else 0

    return executer_test_securise(test_cmd, test_name, expected_exit)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
