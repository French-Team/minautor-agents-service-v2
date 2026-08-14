#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-031-chrono-reference.py
GARDE-FOU : le lanceur de non-regression affiche un chrono global et gere
une reference de temps persistee (temps-reference.json) selon des regles
precises de la demande utilisateur.

Contexte (demande utilisateur 2026-08-13) :
  - L utilisateur avait l impression que le mode parallele ne gagnait rien :
    les mesures reelles (1m53 parallele vs 2m17 serie) ont montre un gain de
    17% mais masque par la serie D en serie apres A/B/C.
  - Il a demande un CHRONO qui demarre au debut de la premiere serie et finit
    a la fin de la derniere, compare a une REFERENCE de temps persistee :
    mise a jour automatique quand le temps est meilleur, SIGNAL quand le
    temps ecoule depasse la reference (seuil, defaut 25%), --rebase-reference
    pour forcer, --no-reference pour les sous-processus paralleles.
  - REGLE DE SECURITE : la reference globale n est geree QUE par le run
    complet sans --tests - un run cible (--tests) ou un appel interne (ex :
    test-027 lance le lanceur) ne doit JAMAIS la lire ni l ecrire (sinon une
    reference partielle fausserait la comparaison).

Invariants verifies :
  1. --version affiche v0.3.2
  2. Les options --seuil, --rebase-reference, --no-reference existent (--help)
  3. Le chrono est affiche (Temps ecoule) en fin de run cible
  4. Un run cible NE CREE PAS la reference si absente (preuve reelle)
  5. Un run cible NE MODIFIE PAS la reference existante (preuve reelle)
  6. Le code du lanceur contient la regle : reference uniquement pour le run
     complet sans filtre (reference_globale = not args.tests)
  7. Normes : ASCII strict + LF pur (test + lanceur + doc)
"""
import importlib.util
import io
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

LANCER = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression",
                      "tester-lancer-non-regression.py")
LANCER_DIR = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression")
REFERENCE = os.path.join(LANCER_DIR, "temps-reference.json")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=180):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lire_fichier(chemin):
    if not os.path.isfile(chemin):
        return None
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-031 : chrono + reference de temps non-regression ===")
    etat_initial = lire_fichier(REFERENCE)
    try:
        # 1. Version du lanceur (round 12 : v0.3.2 tri registre-tests)
        r = run([PYTHON, LANCER, "--version"])
        verifier("1. --version v0.3.2",
                 r.returncode == 0 and "v0.3.2" in r.stdout,
                 r.stdout.strip()[-60:])

        # 2. Options du round 11 presentes dans l aide
        r = run([PYTHON, LANCER, "--help"])
        aide = r.stdout + r.stderr
        verifier("2a. --seuil present dans --help",
                 "--seuil" in aide, "")
        verifier("2b. --rebase-reference present dans --help",
                 "--rebase-reference" in aide, "")
        verifier("2c. --no-reference present dans --help",
                 "--no-reference" in aide, "")

        # 3. Le chrono est affiche a la fin d un run cible (Temps ecoule).
        #    Le run cible (--tests) ne doit PAS toucher a la reference.
        r = run([PYTHON, LANCER, "--serial", "--journal",
                 "--tests", "test-010"])
        verifier("3. Le chrono est affiche (Temps ecoule)",
                 "Temps ecoule" in r.stdout, r.stdout.strip()[-120:])

        # 4. Un run cible ne cree PAS la reference si absente.
        sauvee = lire_fichier(REFERENCE)
        if sauvee is not None:
            os.remove(REFERENCE)
        r = run([PYTHON, LANCER, "--serial", "--journal",
                 "--tests", "test-010"])
        creee = os.path.isfile(REFERENCE)
        verifier("4. Run cible : la reference absente n est PAS creee",
                 not creee, "creee=%s" % creee)
        if creee:
            os.remove(REFERENCE)

        # 5. Un run cible ne modifie PAS la reference existante.
        if sauvee is not None:
            with io.open(REFERENCE, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(sauvee)
        r = run([PYTHON, LANCER, "--serial", "--journal",
                 "--tests", "test-010"])
        apres = lire_fichier(REFERENCE)
        if sauvee is not None:
            verifier("5. Run cible : la reference existante est inchangee",
                     apres == sauvee, "")
        else:
            verifier("5. Run cible : pas de reference creee (etat initial absent)",
                     apres is None, "")

        # 6. Regle statique : la reference n est geree que par le run complet
        #    sans filtre (reference_globale = not args.tests).
        with io.open(LANCER, encoding="utf-8", errors="replace") as fh:
            code_lanceur = fh.read()
        regle_ok = ("reference_globale = not args.tests" in code_lanceur
                    and "temps-reference.json" in code_lanceur
                    and "SIGNAL" in code_lanceur)
        verifier("6. Regle de securite : reference uniquement run complet sans filtre",
                 regle_ok, "")
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1
    finally:
        # Restauration de l etat initial de la reference.
        if etat_initial is not None:
            with io.open(REFERENCE, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(etat_initial)
        elif os.path.isfile(REFERENCE):
            os.remove(REFERENCE)

    # 7. Normes ASCII strict + LF pur (test + lanceur)
    fichiers = [os.path.abspath(__file__), LANCER]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("7. ASCII strict : 0 non-ASCII (test + lanceur)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("8. LF pur : 0 CRLF (test + lanceur)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
