#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-013-cerberus-migration.py
Test formel de la migration pilote du parcours-cerberus v0.5.3
(nouveau format : indices REFERENCES + cases ACTION).

Contexte (etape 6 de la spec-refonte-cartes-decision) :
  - parcours-cerberus passe de v0.2.3 (0 erreur / 15 a alleger) a
    v0.4.6 (0 erreur / 0 a alleger / CONFORME valider-case)
  - 13 indices longs migres : 6 refs resolvables + 7 textes courts
  - 18 cases de pilotage 'indice' -> 'action' (enchaine sans question)   - 2 surcharges de nombre corrigees (c1b, c6 : 4 -> 3 indices)
   - v0.4.5 (2026-08-14) : GARDE-FOU C1 anti-derive - indice ajoute dans la
     case c1 (TOUTE tache d execution -> activer l agent habilite, jamais
     executer seul, 135 car - CONFORME) - lecon derive 2026-08-14
     (Cerberus a execute seul 19 taches)
   - v0.4.6 (2026-08-15) : + indice outil generateurs-commande dans la case
     c10 (usage reel Pattern 17, KO test-035 OUTIL_HORS_CARTE)
   - v0.4.7 (2026-08-15) : + indice outil combos-analyse-projet dans la case
     c17 (usage reel Pattern 17, KO test-035 OUTIL_HORS_CARTE)
   - v0.4.9 (2026-08-16) : branchage corriger-symboles dans les cases de lecons
   - v0.4.8 (2026-08-16) : GARDE-FOUS C1/C5/C18 renforces (VERIFICATION/AUDIT/
     ANALYSE -> Themis c22, jamais analyser avant activer) - lecon derive 2026-08-16
     (Cerberus analysait lui-meme au lieu d activer)
 
 Cas couverts:   1. Version du parcours = 0.5.3
  2. Types : 23 action / 5 question / 5 controle / 3 fin, 0 indice
  3. valider-case : verdict CONFORME (0 erreur, 0 a alleger)
  4. valider-case --references : CONFORME (refs resolvables)
  5. Navigation chemin accueil -> PARCOURS TERMINE
  6. Navigation chemin activation -> PARCOURS TERMINE
  7. Navigation chemin retour (reactiver) -> PARCOURS TERMINE
  8. Refs resolues a la navigation (pattern-8, protocole-activation)
  9. c0b question de confirmation (OUI -> c0c, NON -> c0)
 10. --case c11 demarre a c11 (pas de relecture c0)
 11. Parcours inexistant : ERREUR + code non nul
 12. JSON invalide : ERREUR + code non nul
 13. Protection : aucun fichier cree dans le dossier outil
 14. ASCII strict : 0 non-ASCII (parcours + test)
 15. LF pur : 0 CRLF

Usage:
  python3 test-013-cerberus-migration.py
Tags: agents, parcours, cerberus
"""
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PROTECTIONS = charger_protections()
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0, deploiement dynamique) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for _i, _arg in enumerate(sys.argv):
    if _arg == "--isoler" and _i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[_i + 1])
        except ValueError:
            pass
    if _arg == "--desactiver" and _i + 1 < len(sys.argv):
        for _p in sys.argv[_i + 1].split(','):
            try:
                DESACTIVES.append(int(_p))
            except ValueError:
                pass
ETAPES = []
T_START = __import__("time").monotonic()


def point_actif(numero):
    # True si le point N doit s executer (options on/off du test)
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    # Enregistre la duree d une etape (no-op si --no-chrono)
    if CHRONO_ACTIF:
        ETAPES.append((nom, __import__("time").monotonic() - t_debut))


def bilan_chrono():
    # Affiche le bilan des durees : total + detail par etape
    if not CHRONO_ACTIF:
        return
    _total = __import__("time").monotonic() - T_START
    print("")
    print("=== CHRONO test (total %.1fs) ===" % _total)
    for _nom, _duree in ETAPES:
        print("  %-34s %6.2fs" % (_nom, _duree))


GUIDER = os.path.join(TOOLS_DIR, "guider", "guider-parcours", "guider-parcours.py")
VALIDER_CASE = os.path.join(TOOLS_DIR, "valider", "valider-case", "valider-case.py")
PARCOURS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "cerberus",
                        "parcours", "parcours-cerberus.json")
FICHE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "cerberus",
                     "cerberus.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=90):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-013-")
    try:
        print("=== Test formel migration cerberus v0.5.3 ===")

        # 1. Version du parcours
        with io.open(PARCOURS, encoding="utf-8") as fh:
            donnees = json.load(fh)
        verifier("1. Parcours version 0.5.1",
                 donnees.get("parcours", {}).get("version") == "0.5.3",
                 str(donnees.get("parcours", {}).get("version")))

        # 2. Types de cases : 23 action / 5 question / 5 controle / 3 fin / 0 indice
        cases = donnees.get("cases", {})
        types = {}
        for c in cases.values():
            t = c.get("type", "?")
            types[t] = types.get(t, 0) + 1
        verifier("2a. 23 cases action (19 pilotage + c0d lecture doc + c19c/c19d Pattern 17 + c24 registre + c15c maillon rapport)",
                 types.get("action", 0) == 23, str(types.get("action")))
        verifier("2b. 5 questions + 5 controles + 3 fins (Pattern 17 c19b + maillon c15b ajoutent 2 controles)",
                 types.get("question", 0) == 5 and types.get("controle", 0) == 5
                 and types.get("fin", 0) == 3, str(types))
        verifier("2c. Aucune case 'indice' restante",
                 types.get("indice", 0) == 0, str(types))

        # 3. valider-case : CONFORME (0 erreur, 0 a alleger)
        r = run([PYTHON, VALIDER_CASE, PARCOURS, "--dry-run"])
        verifier("3a. valider-case retourne 0", r.returncode == 0,
                 r.stdout.strip()[-80:])
        verifier("3b. Verdict CONFORME",
                 "CONFORME" in r.stdout and "erreurs: 0" in r.stdout
                 and "a alleger: 0" in r.stdout,
                 r.stdout.strip()[:120])

        # 4. valider-case --references : CONFORME (refs resolvables)
        r_ref = run([PYTHON, VALIDER_CASE, PARCOURS, "--references", "--dry-run"])
        verifier("4. --references : CONFORME (refs resolvables)",
                 r_ref.returncode == 0 and "CONFORME" in r_ref.stdout,
                 r_ref.stdout.strip()[:120])

        # 5. Navigation chemin accueil
        r_nav = run([PYTHON, GUIDER, PARCOURS, "--reponses",
                     "OUI|accueil|OUI|OUI|NON|NON"])
        verifier("5. Chemin accueil -> PARCOURS TERMINE",
                 r_nav.returncode == 0 and "PARCOURS TERMINE" in r_nav.stdout,
                 r_nav.stdout.strip()[-100:])

        # 6. Navigation chemin activation
        r_nav = run([PYTHON, GUIDER, PARCOURS, "--reponses",
                     "OUI|activation|OUI|OUI|OUI|NON"])
        verifier("6. Chemin activation -> PARCOURS TERMINE",
                 r_nav.returncode == 0 and "PARCOURS TERMINE" in r_nav.stdout,
                 r_nav.stdout.strip()[-100:])

        # 7. Navigation chemin retour (reactiver)
        r_nav = run([PYTHON, GUIDER, PARCOURS, "--reponses",
                     "OUI|retour|OUI|NON|NON|NON"])
        verifier("7. Chemin retour -> PARCOURS TERMINE",
                 r_nav.returncode == 0 and "PARCOURS TERMINE" in r_nav.stdout,
                 r_nav.stdout.strip()[-100:])

        # 8. Refs resolues a la navigation (pattern-8, protocole-activation)
        r_nav = run([PYTHON, GUIDER, PARCOURS, "--reponses",
                     "OUI|accueil|OUI|OUI|NON|NON"])
        verifier("8a. [REFERENCE] pattern-8 resolue",
                 "[REFERENCE]" in r_nav.stdout and "pattern-8" in r_nav.stdout,
                 r_nav.stdout.strip()[-200:])
        verifier("8b. [REFERENCE] protocole-activation resolue",
                 "[REFERENCE]" in r_nav.stdout and "protocole-activation" in r_nav.stdout,
                 r_nav.stdout.strip()[-200:])

        # 9. c0b est maintenant une QUESTION de confirmation (migration
        #    relecture obligatoire) : elle s arrete et pose la question
        #    (OUI -> c0c, NON -> c0). On verifie que c0b affiche bien la
        #    question de confirmation et ne va PAS directement a c1.
        r_act = run([PYTHON, GUIDER, PARCOURS, "--case", "c0b"])
        verifier("9a. c0b (question) s arrete (returncode 0)", r_act.returncode == 0,
                 r_act.stdout.strip()[-80:])
        verifier("9b. c0b affiche la question de confirmation",
                 "QUESTION POUR L'AGENT" in r_act.stdout,
                 r_act.stdout.strip()[-100:])
        verifier("9c. c0b porte les branches OUI -> c0c / NON -> c0",
                 "OUI" in r_act.stdout and "NON" in r_act.stdout,
                 r_act.stdout.strip()[-100:])
        # 9d. Avec la reponse OUI, la navigation enchaine c0b -> c0c -> c1
        r_oui = run([PYTHON, GUIDER, PARCOURS, "--case", "c0b",
                     "--reponses", "OUI"])
        verifier("9d. OUI -> c0c (contexte) puis c1 Mission",
                 r_oui.returncode == 0 and "Mission" in r_oui.stdout
                 and "QUESTION POUR L'AGENT" in r_oui.stdout,
                 r_oui.stdout.strip()[-100:])

        # 10. --case c11 demarre a c11 (pas de relecture c0)
        r_c11 = run([PYTHON, GUIDER, PARCOURS, "--case", "c11"])
        verifier("10. --case c11 demarre a c11",
                 r_c11.returncode == 0 and "Relire MA fiche" in r_c11.stdout
                 and "RELIRE OBLIGATOIRE" not in r_c11.stdout,
                 r_c11.stdout.strip()[-120:])

        # 11. Parcours inexistant : ERREUR
        r_abs = run([PYTHON, GUIDER, os.path.join(tmp, "absent.json")])
        verifier("11. Parcours inexistant : ERREUR + code non nul",
                 r_abs.returncode != 0 and "ERREUR" in (r_abs.stdout + r_abs.stderr),
                 "code=%d" % r_abs.returncode)

        # 12. JSON invalide : ERREUR
        invalide = os.path.join(tmp, "invalide.json")
        with io.open(invalide, "w", encoding="utf-8") as fh:
            fh.write("{ pas du json ")
        r_inv = run([PYTHON, GUIDER, invalide])
        verifier("12. JSON invalide : ERREUR + code non nul",
                 r_inv.returncode != 0 and "ERREUR" in (r_inv.stdout + r_inv.stderr),
                 "code=%d" % r_inv.returncode)

        # 13. Protection : aucun fichier cree dans le dossier parcours
        avant = set(os.listdir(os.path.dirname(PARCOURS)))
        run([PYTHON, GUIDER, PARCOURS, "--reponses", "OUI|accueil|OUI|OUI|NON|NON"])
        apres = set(os.listdir(os.path.dirname(PARCOURS)))
        verifier("13. Protection : aucun fichier cree dans le dossier parcours",
                 avant == apres, "cree: %s" % (apres - avant))

        # 14. ASCII strict
        total_non_ascii = ascii_count(PARCOURS) + ascii_count(
            os.path.abspath(__file__))
        verifier("14. ASCII strict : 0 non-ASCII (parcours + test)",
                 total_non_ascii == 0, "total non-ASCII = %d" % total_non_ascii)

        # 15. LF pur
        total_crlf = crlf_count(PARCOURS) + crlf_count(os.path.abspath(__file__))
        verifier("15. LF pur : 0 CRLF (parcours + test)",
                 total_crlf == 0, "total CRLF = %d" % total_crlf)

        print("")
        bilan_chrono()
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
