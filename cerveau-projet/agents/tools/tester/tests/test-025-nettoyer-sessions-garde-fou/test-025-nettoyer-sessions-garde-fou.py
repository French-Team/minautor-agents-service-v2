#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-025-nettoyer-sessions-garde-fou.py
Test formel du garde-fou anti-recurrence : en-tete ## Sessions LLM PRESERVE
(lecon 2026-08-12 : apres un nettoyage, sidentifier echouait avec
'Section ## Sessions LLM introuvable' car nettoyer-sessions supprimait
l'en-tete de section ## Sessions LLM a tort).

Contexte (mission Vulcain v0.1.2) :
  - nettoyer-sessions v0.1.1 supprimait l'en-tete '## Sessions LLM' en plus
    des blocs session et de la table Sessions connues.
  - v0.1.2 : l'en-tete est PRESERVE, seuls les blocs '### Session :
    session-llm-N' (titre + contenu) et la section '## Sessions connues'
    sont supprimes. Parite py/sh conservee.
  - Ce garde-fou verifie la BOUCLE COMPLETE sur copies : nettoyage ->
    en-tete conserve -> activer-agent-principal sidentifier recreer le bloc
    (le bug etait invisible sans l'etape de re-identification).

Cas couverts:
  1. nettoyer-sessions --version py = v0.1.2
  2. Parite --version py/sh
  3. Nettoyage sur copies : blocs '### Session :' supprimes (0)
  4. Nettoyage : en-tete '## Sessions LLM' PRESERVE (1) - coeur du bug
  5. Nettoyage : section '## Sessions connues' supprimee (0)
  6. Nettoyage : lignes profil-session-* supprimees (0)
  7. Nettoyage : frontmatter identite preserve
  8. INTEGRATION : sidentifier sur la copie nettoyee fonctionne + bloc recree
  9. Parite py/sh : fichiers resultants identiques
 10. ASCII strict : 0 non-ASCII (py/sh/md de l'outil + test)
 11. LF pur : 0 CRLF (py/sh/md de l'outil + test)

Usage:
  python3 test-025-nettoyer-sessions-garde-fou.py
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


OUTIL_DIR = os.path.join(TOOLS_DIR, "nettoyer", "nettoyer-sessions")
OUTIL_PY = os.path.join(OUTIL_DIR, "nettoyer-sessions.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "nettoyer-sessions.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "nettoyer-sessions.md")
ACTIVER = os.path.join(TOOLS_DIR, "activer", "activer-agent-principal",
                       "activer-agent-principal.py")
AGENTS_SRC = os.path.join(PROJECT_ROOT, "AGENTS.md")
CLASSEUR_SRC = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                            "classeur-variables", "stockage",
                            "variables-actuelles.md")
HISTORIQUE_SRC = os.path.join(PROJECT_ROOT, "AGENTS-historique.md")

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


def run(cmd, env=None, timeout=60):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, env=env,
                          timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def preparer_copies(espace):
    """Copier les 3 fichiers reels vers l'espace de test (copies uniquement)."""
    os.makedirs(espace, exist_ok=True)
    shutil.copy2(AGENTS_SRC, os.path.join(espace, "AGENTS.md"))
    shutil.copy2(CLASSEUR_SRC, os.path.join(espace, "classeur.md"))
    shutil.copy2(HISTORIQUE_SRC, os.path.join(espace, "historique.md"))


def env_test(espace):
    env = dict(os.environ)
    env["AGENTS_FILE"] = os.path.join(espace, "AGENTS.md")
    env["CLASSEUR_STOCKAGE"] = os.path.join(espace, "classeur.md")
    env["AGENTS_HISTORIQUE"] = os.path.join(espace, "historique.md")
    return env


def compter(chemin, motif):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for ligne in fh if ligne.startswith(motif))


def main():
    global NB_POINTS, NB_OK, NB_KO

    # 1-2. Version + parite
    r = run([PYTHON, OUTIL_PY, "--version"])
    verifier("1. nettoyer-sessions --version py = v0.1.2",
             r.returncode == 0 and "v0.1.2" in r.stdout, r.stdout.strip()[-60:])
    r_sh = run(["bash", OUTIL_SH, "--version"])
    verifier("2. parite --version py/sh",
             r_sh.returncode == 0 and r.stdout.strip() == r_sh.stdout.strip(),
             "py='%s' sh='%s'" % (r.stdout.strip(), r_sh.stdout.strip()))

    # 3-7. Nettoyage reel sur copies (py)
    espace = tempfile.mkdtemp(prefix="test-025-")
    try:
        preparer_copies(espace)
        env = env_test(espace)
        r = run([PYTHON, OUTIL_PY], env=env)
        agents = os.path.join(espace, "AGENTS.md")
        classeur = os.path.join(espace, "classeur.md")
        verifier("3. blocs '### Session :' supprimes (0)",
                 compter(agents, "### Session :") == 0,
                 "nb=%d" % compter(agents, "### Session :"))
        verifier("4. en-tete '## Sessions LLM' PRESERVE (1) - coeur du bug",
                 compter(agents, "## Sessions LLM") == 1,
                 "nb=%d" % compter(agents, "## Sessions LLM"))
        verifier("5. section '## Sessions connues' supprimee (0)",
                 compter(agents, "## Sessions connues") == 0,
                 "nb=%d" % compter(agents, "## Sessions connues"))
        verifier("6. lignes profil-session-* supprimees (0)",
                 compter(classeur, "| `profil-session-") == 0,
                 "nb=%d" % compter(classeur, "| `profil-session-"))
        verifier("7. frontmatter identite preserve",
                 compter(agents, "identite:") >= 1,
                 "nb=%d" % compter(agents, "identite:"))

        # 8. INTEGRATION : sidentifier sur la copie nettoyee
        r = run([PYTHON, ACTIVER, "sidentifier", "llm-1"], env=env)
        ok_sid = (r.returncode == 0 and "session-llm-1" in r.stdout
                  and "ERREUR" not in r.stdout)
        ok_bloc = compter(agents, "### Session : session-llm-1") == 1
        verifier("8. INTEGRATION: sidentifier fonctionne + bloc recree (anti-recurrence)",
                 ok_sid and ok_bloc,
                 "sid_ok=%s bloc=%d" % (ok_sid,
                                        compter(agents, "### Session : session-llm-1")))

        # 9. Parite py/sh : fichiers resultants identiques (copies neuves)
        espace_py = os.path.join(espace, "py")
        espace_sh = os.path.join(espace, "sh")
        preparer_copies(espace_py)
        preparer_copies(espace_sh)
        run([PYTHON, OUTIL_PY], env=env_test(espace_py))
        run(["bash", OUTIL_SH], env=env_test(espace_sh))
        d1 = open(os.path.join(espace_py, "AGENTS.md"), "rb").read()
        d2 = open(os.path.join(espace_sh, "AGENTS.md"), "rb").read()
        c1 = open(os.path.join(espace_py, "classeur.md"), "rb").read()
        c2 = open(os.path.join(espace_sh, "classeur.md"), "rb").read()
        verifier("9. parite py/sh fichiers resultants (AGENTS + classeur)",
                 d1 == d2 and c1 == c2)
    finally:
        shutil.rmtree(espace, ignore_errors=True)

    # 10-11. Normes sur les fichiers de l'outil + ce test
    fichiers = [OUTIL_PY, OUTIL_SH, OUTIL_MD, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("10. ASCII strict : 0 non-ASCII (outil + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("11. LF pur : 0 CRLF (outil + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
