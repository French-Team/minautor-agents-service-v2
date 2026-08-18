#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-016-migration-buffy.py
Test formel de la migration du parcours-buffy v0.3.0
(nouveau format : indices REFERENCES + cases ACTION).

Contexte (etape 6 generalisee de la spec-refonte-cartes-decision) :
  - parcours-buffy passe de v0.2.11 (0 erreur / 15 a alleger) a
    v0.3.0 (0 erreur / 0 a alleger / CONFORME valider-case)
  - 17 cases en surcharge de nombre reduites au BUDGET PONDERE (<= 3,0)
  - textes regle longs migres en refs (pattern-2 ASCII, pattern-3
    combo, pattern-6 contexte, pattern-12 creation limitee, regles-
    perimetre-workspace) ou textes courts (< 160 car.)
  - 31 cases de pilotage 'indice' -> 'action' (enchaine sans question)
  - fiche buffy mise a jour (Pattern 14 : parcours v0.3.1)
  - test-009 adapte : temoin A ALLEGER bascule de buffy vers morpheus
  - v0.3.1 : branchement generateurs-ligne (case c10d, branche 'ligne' dans c10b)
  - v0.3.6 : branchement editer-fichier-agents (case c11b, branche 'fiche' dans c10b)
  - v0.4.1 : ajout case c0d LIRE LA DOCUMENTATION DE L OUTIL (REGLE ABSOLUE LECTURE DOC)   - v0.4.2 (2026-08-13) : Themis maillon automatique (actions c8a/c22a/c27a Activer Themis + controles c8b/c22b/
   - v0.4.3 (2026-08-14) : ajout indice outil valider-cartes-decision (case c14 RVAV)c27b Retour de Themis)
   - v0.4.4 (2026-08-15) : ajout indice outil generateurs-case (case c10c, coherence
     regle/indice outil - garde-fou test-055)
   - v0.4.6 (2026-08-15) : assignation bumper (case c10b, mettre-a-jour-versions) + evaluer-processus
     (case c26) - OUTIL_HORS_CARTE teste par evaluer-processus (garde-fou test-035)
   - v0.4.9 (2026-08-16) : branchage outils de controle (verifier-conformite-fiche, valider-case, valider-numerotation, detecter-usage-outils-externes)
   - v0.4.10 (2026-08-16) : migration relecture obligatoire (c0 action RELIRE + c0b question confirmation)
   - v0.4.8 (2026-08-16) : branchage corriger-symboles dans les cases de lecons (c15/c7/c20)
   - v0.4.7 (2026-08-15) : ajout indice outil guider-parcours (case c0, P0 de la fiche
     absent de la carte - OUTIL_HORS_CARTE teste par evaluer-processus, garde-fou test-035)

Cas couverts:   1. Version du parcours = 0.4.13
  2. Types : 40 action / 8 question / 5 controle / 10 fin, 0 indice
  3. valider-case : verdict CONFORME (0 erreur, 0 a alleger)
  4. valider-case --references : CONFORME (refs resolvables)
  5. Navigation chemin creation agent -> PARCOURS TERMINE
  6. Navigation chemin protocole -> PARCOURS TERMINE
  7. Case action enchaine SANS question (c0b -> c0c, pas de QUESTION)
  8. Refs resolues a la navigation (pattern-6, regles-perimetre-workspace)
  9. Aucun texte regle > 160 caracteres dans le parcours
 10. Budget pondere des indices <= 3,0 (regle autoritaire)
 11. Parcours inexistant : ERREUR + code non nul
 12. JSON invalide : ERREUR + code non nul
 13. Protection : aucun fichier cree dans le dossier outil
 14. ASCII strict : 0 non-ASCII (parcours + test + fiche)
 15. LF pur : 0 CRLF

Usage:
  python3 test-016-migration-buffy.py
Tags: agents, parcours, buffy
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


OUTIL_DIR = os.path.join(TOOLS_DIR, "valider", "valider-case")
OUTIL_PY = os.path.join(OUTIL_DIR, "valider-case.py")
GP_PY = os.path.join(TOOLS_DIR, "guider", "guider-parcours", "guider-parcours.py")
PARCOURS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "buffy",
                        "parcours", "parcours-buffy.json")
FICHE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "buffy", "buffy.md")

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
    """Compte les caracteres non-ASCII d'un fichier (0 = conforme)."""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-016-")
    try:
        print("=== Test formel migration parcours-buffy v0.3.0 ===")

        with io.open(PARCOURS, encoding="utf-8") as fh:
            d = json.load(fh)

        # 1. Version
        verifier("1. Version du parcours = 0.4.13",
                 d["parcours"].get("version") == "0.4.13",
                 d["parcours"].get("version"))

        # 2. Types
        types = {}
        for c in d["cases"].values():
            types[c.get("type")] = types.get(c.get("type"), 0) + 1
        verifier("2a. 40 cases action (37 anterieures + c8a/c22a/c27a Activer Themis)",
                 types.get("action") == 40, str(types))
        verifier("2b. 8 questions + 5 controles + 10 fins (Themis c8b/c22b/c27b)",
                 types.get("question") == 8 and types.get("controle") == 5
                 and types.get("fin") == 10, str(types))
        verifier("2c. 0 case indice restante (toutes converties en action)",
                 types.get("indice", 0) == 0, str(types))

        # 3. valider-case : CONFORME
        r = run([PYTHON, OUTIL_PY, PARCOURS, "--dry-run"])
        verifier("3a. valider-case retourne 0", r.returncode == 0,
                 r.stdout.strip()[-100:])
        verifier("3b. Verdict CONFORME (0 erreur, 0 a alleger)",
                 "CONFORME" in r.stdout and "erreurs: 0" in r.stdout
                 and "a alleger: 0" in r.stdout,
                 r.stdout.strip()[:120])
        verifier("3c. Aucune surcharge restante",
                 "a alleger:" in r.stdout
                 and int(r.stdout.split("a alleger:")[1].split("|")[0].strip()) == 0,
                 r.stdout.strip()[:120])

        # 4. --references : CONFORME (refs resolvables)
        r_ref = run([PYTHON, OUTIL_PY, PARCOURS, "--references", "--dry-run"])
        verifier("4. --references : CONFORME (refs resolvables)",
                 r_ref.returncode == 0 and "CONFORME" in r_ref.stdout,
                 r_ref.stdout.strip()[:120])

        # 5. Navigation chemin creation agent (OUI -> creer) -> TERMINE
        r_nav = run([PYTHON, GP_PY, PARCOURS, "--reponses",
                     "OUI|creer|OUI|OUI|OUI|OUI"])
        verifier("5. Navigation chemin creation agent -> PARCOURS TERMINE",
                 "PARCOURS TERMINE" in r_nav.stdout,
                 r_nav.stdout.strip()[-150:])

        # 6. Navigation chemin protocole (OUI -> protocole) -> TERMINE
        r_nav2 = run([PYTHON, GP_PY, PARCOURS, "--reponses",
                      "OUI|protocole|OUI|OUI|OUI|OUI"])
        verifier("6. Navigation chemin protocole -> PARCOURS TERMINE",
                 "PARCOURS TERMINE" in r_nav2.stdout,
                 r_nav2.stdout.strip()[-150:])

        # 7. Case action enchaine sans question (c0b -> c0c)
        r_act = run([PYTHON, GP_PY, PARCOURS, "--reponses", "NON"])
        verifier("7. c0b (action) enchaine sans question vers c0c",
                 "PARCOURS TERMINE" not in r_act.stdout
                 and r_act.stdout.strip() != "",
                 r_act.stdout.strip()[-120:])

        # 8. Refs resolues a la navigation (pattern-6, regles-perimetre)
        verifier("8a. Ref pattern-6 resolue a la navigation",
                 "pattern-6" in r_nav.stdout or "CONTEXTE TEMPS REEL" in r_nav.stdout,
                 r_nav.stdout.strip()[:150])
        verifier("8b. Ref fichier regles-perimetre-workspace resolue",
                 "regles-perimetre-workspace" in r_nav.stdout,
                 r_nav.stdout.strip()[:150])

        # 9. Aucun texte regle > 160 caracteres
        trop_long = []
        for k, c in d["cases"].items():
            for i, ind in enumerate(c.get("indices", [])):
                if isinstance(ind, dict) and ind.get("type") == "regle":
                    t = ind.get("texte", "")
                    if len(t) > 160:
                        trop_long.append("%s#%d (%d)" % (k, i, len(t)))
        verifier("9. Aucun texte regle > 160 caracteres",
                 not trop_long, "; ".join(trop_long[:5]))

        # 10. Budget pondere des indices (regle autoritaire, spec v0.1.3 /
        # Pattern 16 2026-08-11) : indice COURT (texte <= 100 car. ou sans
        # texte) = 0,5 ; LONG (> 100 car.) = 1 ; budget 3,0 par case
        # (6 courts = 3,0 OK). Meme calcul que valider-case (poids_indices).
        def _poids_indices(indices):
            p = 0.0
            for ind in indices:
                t = ind.get("texte", "")
                p += 1.0 if (isinstance(t, str) and len(t) > 100) else 0.5
            return p
        trop_ind = [k for k, c in d["cases"].items()
                    if _poids_indices(c.get("indices", [])) > 3.0]
        verifier("10. Budget pondere des indices <= 3,0",
                 not trop_ind, "; ".join(trop_ind[:5]))

        # 11. Parcours inexistant : ERREUR
        r_abs = run([PYTHON, OUTIL_PY, os.path.join(tmp, "absent.json")])
        verifier("11. Parcours inexistant : ERREUR + code non nul",
                 r_abs.returncode != 0 and "ERREUR" in (r_abs.stdout + r_abs.stderr),
                 "code=%d" % r_abs.returncode)

        # 12. JSON invalide : ERREUR
        invalide = os.path.join(tmp, "invalide.json")
        with io.open(invalide, "w", encoding="utf-8") as fh:
            fh.write("{ ceci n est pas du json ")
        r_inv = run([PYTHON, OUTIL_PY, invalide])
        verifier("12. JSON invalide : ERREUR + code non nul",
                 r_inv.returncode != 0 and "ERREUR" in (r_inv.stdout + r_inv.stderr),
                 "code=%d" % r_inv.returncode)

        # 13. Protection : aucun fichier cree dans le dossier outil
        avant = set(os.listdir(OUTIL_DIR))
        run([PYTHON, OUTIL_PY, PARCOURS, "--dry-run"])
        apres = set(os.listdir(OUTIL_DIR))
        verifier("13. Protection : aucun fichier cree dans le dossier outil",
                 avant == apres, "cree: %s" % (apres - avant))

        # 14. ASCII strict : 0 non-ASCII (parcours + test + fiche)
        total_non_ascii = (ascii_count(PARCOURS) + ascii_count(FICHE)
                           + ascii_count(os.path.abspath(__file__)))
        verifier("14. ASCII strict : 0 non-ASCII (parcours + fiche + test)",
                 total_non_ascii == 0, "total = %d" % total_non_ascii)

        # 15. LF pur : 0 CRLF (parcours)
        raw = open(PARCOURS, "rb").read()
        verifier("15. LF pur : 0 CRLF (parcours)",
                 raw.count(b"\r\n") == 0, "CRLF = %d" % raw.count(b"\r\n"))

        print("")
        bilan_chrono()
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
