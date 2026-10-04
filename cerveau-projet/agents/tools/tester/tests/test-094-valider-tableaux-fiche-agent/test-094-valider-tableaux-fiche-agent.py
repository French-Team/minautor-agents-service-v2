#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-094-valider-tableaux-fiche-agent.py
GARDE-FOU : valider-tableaux (v0.2.1) ne compte comme agent QUE les dossiers
avec une fiche au frontmatter `type: fiche-agent` (faux positif
classeur-variables corrige), et le .sh est un wrapper pur vers le .py
(regression du bug stdin Windows du heredoc, preexistant en 0.2.0).

Contexte (2026-08-18, demande utilisateur) : valider-tableaux signalait
`classeur-variables` (dossier de donnees, `type: classeur`) comme un agent
manquant dans le tableau "Agents disponibles" de cerberus.md. Le filtre
`est_fiche_agent` a ete ajoute (meme pattern que les autres outils du
projet). Le .sh embarquant un heredoc python cassait l'interpretation sous
`python3 -` (stdin) sur Windows : il est devenu un wrapper pur
(`exec python3 valider-tableaux.py "$@"`), parite garantie par construction.

Invariants verifies :
  1. L outil existe et compile (.py + .sh).
  2. --version affiche 0.2.1-py.
  3. Le .sh (wrapper) fonctionne : bash valider-tableaux.sh --version.
  4. Fiche cerberus.md : CONFORME (1 fichier, 0 probleme).
  5. Dossier agents complet : CONFORME ET "classeur-variables" absent du
     rapport (faux positif corrige).
  6. --agent argus : CONFORME.
  7. Parite .sh/.py : meme nombre de fichiers analyses sur la meme cible.
  8. Normes : ASCII strict + LF pur (outil .py/.sh/.md + test).

Tags: outils, valider, garde-fou, anti-recurrence
"""
import importlib.util
import io
import os
import py_compile
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

OUTIL_DIR = os.path.join(TOOLS_DIR, "valider", "valider-tableaux")
OUTIL_PY = os.path.join(OUTIL_DIR, "valider-tableaux.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "valider-tableaux.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "valider-tableaux.md")
AGENTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")
# La liste de routage "Agents disponibles" vit chez ORACLE (decision
# utilisateur 2026-08-30 : Cerberus ne porte plus la liste des agents).
ORACLE_MD = os.path.join(AGENTS_DIR, "oracle", "oracle.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            ISOLE = None
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        DESACTIVES = [int(x) for x in sys.argv[i + 1].split(",")
                      if x.strip().isdigit()]

DEBUT_TEST = time.monotonic()
ETAPES = []  # (nom, duree_secondes) alimente le bilan chrono


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    """True si le point N doit s executer (options on/off du test)."""
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    """Enregistre la duree d une etape (no-op si --no-chrono)."""
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    """Affiche le bilan des durees : total + detail par etape."""
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT_TEST
    detail = " | ".join("%s=%.2fs" % e for e in ETAPES)
    print("=== CHRONO : total %.2fs (%s) ===\n" % (total, detail))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=120):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== [TEST-094 : valider-tableaux filtre fiche-agent + wrapper] ===")
    try:
        # 1. L outil existe et compile (.py + .sh)
        if point_actif(1):
            t = time.monotonic()
            ok_py = os.path.isfile(OUTIL_PY)
            ok_sh = os.path.isfile(OUTIL_SH)
            compile_ok = False
            if ok_py:
                try:
                    py_compile.compile(OUTIL_PY, doraise=True)
                    compile_ok = True
                except Exception:
                    compile_ok = False
            verifier("1. Outil present (.py + .sh) et .py compile",
                     ok_py and ok_sh and compile_ok,
                     "py=%s sh=%s compile=%s" % (ok_py, ok_sh, compile_ok))
            chrono_etape("1. presence/compile", t)

        # 2. --version affiche 0.2.1-py
        if point_actif(2):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, "--version"])
            verifier("2. .py --version affiche v0.2.1-py",
                     "v0.2.1-py" in (r.stdout + r.stderr), r.stdout.strip())
            chrono_etape("2. version py", t)

        # 3. Le .sh (wrapper pur) fonctionne -- anti-regression bug stdin
        if point_actif(3):
            t = time.monotonic()
            r = run(["bash", OUTIL_SH, "--version"])
            sortie = r.stdout + r.stderr
            verifier("3. .sh --version fonctionne (wrapper, plus de bug stdin)",
                     "v0.2.1-py" in sortie and "IndentationError" not in sortie,
                     sortie.strip()[-160:])
            chrono_etape("3. wrapper sh", t)

        # 4. Fiche oracle.md : CONFORME (liste de routage, decision 2026-08-30)
        if point_actif(4):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, ORACLE_MD])
            sortie = r.stdout + r.stderr
            PROTECTIONS.verifier_critique(
                "4. oracle.md CONFORME (1 fichier, 0 probleme) - STOP si KO",
                "CONFORME" in sortie and "Problemes : 0" in sortie,
                sortie.strip()[-200:])
            chrono_etape("4. fiche oracle", t)

        # 5. Dossier agents complet : CONFORME ET classeur-variables absent
        if point_actif(5):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, AGENTS_DIR], timeout=180)
            sortie = r.stdout + r.stderr
            conforme = "CONFORME" in sortie and "Problemes : 0" in sortie
            faux_positif_absent = "classeur-variables" not in sortie
            PROTECTIONS.verifier_critique(
                "5. Dossier agents CONFORME sans classeur-variables (faux positif corrige)",
                conforme and faux_positif_absent,
                sortie.strip()[-300:])
            chrono_etape("5. dossier agents", t)

        # 6. --agent argus : CONFORME
        if point_actif(6):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, "--agent", "argus"])
            sortie = r.stdout + r.stderr
            verifier("6. --agent argus CONFORME",
                     "CONFORME" in sortie and "Problemes : 0" in sortie,
                     sortie.strip()[-160:])
            chrono_etape("6. --agent argus", t)

        # 7. Parite .sh/.py : meme nombre de fichiers analyses
        if point_actif(7):
            t = time.monotonic()
            r_py = run([PYTHON, OUTIL_PY, AGENTS_DIR], timeout=180)
            r_sh = run(["bash", OUTIL_SH, AGENTS_DIR], timeout=180)
            extrait_py = [l for l in (r_py.stdout + r_py.stderr).splitlines()
                          if "Fichiers analyses" in l]
            extrait_sh = [l for l in (r_sh.stdout + r_sh.stderr).splitlines()
                          if "Fichiers analyses" in l]
            verifier("7. Parite .sh/.py (meme rapport sur la meme cible)",
                     bool(extrait_py) and extrait_py == extrait_sh,
                     "py=%r sh=%r" % (extrait_py, extrait_sh))
            chrono_etape("7. parite sh/py", t)

        # 8. Normes : ASCII strict + LF pur (outil .py/.sh/.md + test)
        if point_actif(8):
            t = time.monotonic()
            fichiers = [OUTIL_PY, OUTIL_SH, OUTIL_MD,
                        os.path.abspath(__file__)]
            total_non_ascii = sum(ascii_count(f) for f in fichiers)
            verifier("8a. ASCII strict : 0 non-ASCII (outil + test)",
                     total_non_ascii == 0, "total=%d" % total_non_ascii)
            total_crlf = sum(crlf_count(f) for f in fichiers)
            verifier("8b. LF pur : 0 CRLF (outil + test)",
                     total_crlf == 0, "total=%d" % total_crlf)
            chrono_etape("8. normes", t)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    if NB_KO:
        print("  [AIDE] OU CHERCHER / REPARER (KO = agent manquant dans un tableau de fiche) :")
        print("    [AIDE] Fichier inspecte : agents/oracle/oracle.md (tableau des agents disponibles, liste de routage)")
        print("    [AIDE] Diagnostic : python3 cerveau-projet/agents/tools/valider/valider-tableaux/valider-tableaux.py agents/oracle/oracle.md")
        print("    [AIDE] Correctif : ajouter l agent absent signale par le rapport a la liste de routage de la fiche oracle.md")
    PROTECTIONS.afficher_rating(os.path.basename(__file__).replace(".py", ""))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
