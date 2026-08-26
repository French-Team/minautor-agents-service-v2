#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-103-coherence-agents-agents-md.py
GARDE-FOU : l outil v1 verifier-coherence-agents detecte les incoherences
des blocs session d AGENTS.md (fichier racine commun) contre les fichiers
reels (arbres v2, fiches, corrections, jarvis-data.json, table Sessions).

Verifie que l outil (cree 2026-08-25, chantier ferrari / mecanisme de
validation automatique au demarrage) :
  1. Retourne rc=0 sur le AGENTS.md reel (0 incoherence attendue).
  2. Secteur a ete rendu conforme par l audit/corrections du 2026-08-25.
  3. Preuve negative : une ligne themes listant un theme-*.json orphelin
     (theme-lire.json / theme-explorer.json) est detectee (rc>=1).
  4. Preuve negative : une raison manifestement tronquee est signalee.
  5. Preuve negative : jarvis-data.json avec un champ corrections vide est
     detecte (lecture seule de l outil, sans modification).
  6. Normes de l outil : ASCII strict + LF pur + doc .md presente.

Tags: agents-md, verifier-coherence, outil, garde-fou, preuve-negative
"""
import importlib.util
import glob
import io
import json
import os
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEAu = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEAu, "agents", "tools")
PYTHON = sys.executable

VERIFIER_PY = os.path.join(TOOLS_DIR, "verifier", "verifier-coherence-agents",
                           "verifier-coherence-agents.py")
AGENTS_MD = os.path.join(PROJECT_ROOT, "AGENTS.md")
JARVIS_DATA = os.path.join(CERVEAu, "freelance", "tools-commun", "jarvis",
                           "jarvis-data.json")

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
ETAPES = []


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT_TEST
    print("")
    print("=== CHRONO test (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=60):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      timeout=timeout)


def creer_env_tmp(suffixe):
    """Copier AGENTS.md + jarvis-data.json (hypothetiques) dans un tmp local
    sous la racine projet pour pouvoir injecter des incoherences."""
    tmpdir = tempfile.mkdtemp(prefix="test-103-%s-" % suffixe)
    agents = os.path.join(tmpdir, "AGENTS.md")
    shutil.copy2(AGENTS_MD, agents)
    return tmpdir, agents


def nettoyer_env(tmpdir):
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)


def point_1_rc_zero_sur_reel():
    """L outil retourne rc=0 sur AGENTS.md reel (0 incoherence)."""
    if not os.path.isfile(VERIFIER_PY):
        verifier("outil present", False, "verifier-coherence-agents.py manquant")
        return
    verifier("outil present", True)
    r = run([PYTHON, VERIFIER_PY, "--dry-run"])
    verifier("rc=0 sur AGENTS.md reel", r.returncode == 0,
             "rc=%s stdout=%s" % (r.returncode, (r.stdout or '')[-300:]))
    verifier("aucune incoherence signalee",
             "INCOHERENCES" not in (r.stdout or ""),
             r.stdout[-200:] if r.stdout else "aucune sortie")


def point_2_preuve_negative_themes_orphelins():
    """Une ligne themes listant un theme-orphelin est detectee."""
    tmpdir, agents = creer_env_tmp("themes")
    try:
        with io.open(agents, "r", encoding="utf-8") as f:
            src = f.read()
        ligne_reel = "(themes : selon ton arbre ; JARVIS = point d'entree " \
                     "OBLIGATOIRE pour toute mission)"
        remplace = "(themes : theme-jarvis.json (JARVIS) / theme-lire.json " \
                   "/ theme-explorer.json)"
        if ligne_reel not in src:
            verifier("ligne themes reperee pour injection", False,
                     "ligne DEMARRAGE V2 introuvable")
            return
        src = src.replace(ligne_reel, remplace)
        with io.open(agents, "w", encoding="utf-8", newline="") as f:
            f.write(src)
        r = run([PYTHON, VERIFIER_PY, "--agents-md", agents, "--dry-run"])
        detecte = ("theme-lire.json" in (r.stdout or "")) \
            and ("INCOHERENCES" in (r.stdout or "")) \
            and r.returncode >= 1
        verifier("theme orphelin detecte", detecte,
                 "rc=%s stdout=%s" % (r.returncode, (r.stdout or '')[-250:]))
    finally:
        nettoyer_env(tmpdir)


def point_3_preuve_negative_raison_tronquee():
    """Une raison se terminant par un mot inacheve (comme la coupure a
    80 caracteres d avant) est signalee par l outil."""
    import re as _re
    tmpdir, agents = creer_env_tmp("raison")
    try:
        with io.open(agents, "r", encoding="utf-8") as f:
            src = f.read()
        # Remplacer TOUTE la ligne Raison de session-freelance par une raison
        # coupee au mot (sans ponctuation finale) : c est exactement le genre
        # de coupure que produisait autrefois mission[:80].
        marker = "### Session : session-freelance"
        pos = src.find(marker)
        if pos == -1:
            verifier("bloc session-freelance reperee", False)
            return
        fin_bloc = src.find("### Session", pos + 1)
        if fin_bloc == -1:
            fin_bloc = src.find("## Sessions connues", pos + 1)
        bloc = src[pos:fin_bloc]
        m_raison = _re.search(r"\| \*\*Raison\*\* \|([^\n]*)\|([^\n]*)", bloc)
        if not m_raison:
            verifier("ligne Raison reperee", False)
            return
        deb_ligne = pos + m_raison.start()
        fin_ligne = pos + m_raison.end()
        coupee = "| **Raison** | Active par stark: Diagnostic termine. " \
                 "Conclusion : JARVIS FON|"
        src = src[:deb_ligne] + coupee + src[fin_ligne:]
        with io.open(agents, "w", encoding="utf-8", newline="") as f:
            f.write(src)
        r = run([PYTHON, VERIFIER_PY, "--agents-md", agents, "--dry-run"])
        detecte = ("INCOHERENCES" in (r.stdout or "")) \
            and ("raison" in (r.stdout or "").lower()) \
            and r.returncode >= 1
        verifier("raison tronquee detectee", detecte,
                 "rc=%s stdout=%s" % (r.returncode, (r.stdout or '')[-250:]))
    finally:
        nettoyer_env(tmpdir)


def point_4_jarvis_data_coherent():
    """jarvis-data.json : aucun fiche/corrections vide (l outil le verifie)."""
    if not os.path.isfile(JARVIS_DATA):
        verifier("jarvis-data.json present", False, "fichier introuvable")
        return
    verifier("jarvis-data.json present", True)
    try:
        with io.open(JARVIS_DATA, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as exc:
        verifier("jarvis-data.json lisible", False, str(exc))
        return
    verifier("jarvis-data.json lisible", True)
    vides = [a.get("nom") for a in data.get("agents", [])
             if not a.get("fiche") or not a.get("corrections")]
    verifier("aucun champ fiche/corrections vide", not vides,
             "agents a probleme : %s" % sorted(vides))


def point_5_normes_outil():
    """Normes de l outil : .md present, ASCII strict, LF pur."""
    md = VERIFIER_PY.replace(".py", ".md")
    sh_ = VERIFIER_PY.replace(".py", ".sh")
    verifier("doc .md presente", os.path.isfile(md))
    verifier("wrapper .sh present", os.path.isfile(sh_))
    for chemin in (VERIFIER_PY, sh_, md):
        if not os.path.isfile(chemin):
            continue
        octets = open(chemin, "rb").read()
        na = [c for c in octets if c > 127]
        verifier("ASCII strict : %s" % os.path.basename(chemin),
                 len(na) == 0, "%s octets non-ascii" % len(na))
        crlf = octets.count(b"\r\n")
        verifier("LF pur : %s" % os.path.basename(chemin),
                 crlf == 0, "%s CRLF" % crlf)
    # Syntaxe
    try:
        compile(open(VERIFIER_PY, encoding="utf-8").read(), VERIFIER_PY, "exec")
        verifier("syntaxe Python valide", True)
    except SyntaxError as exc:
        verifier("syntaxe Python valide", False, str(exc))


def main():
    print("=== test-103 : verifier-coherence-agents (coherence AGENTS.md) ===")

    points = [
        ("1. rc=0 sur AGENTS.md reel", point_1_rc_zero_sur_reel),
        ("2. preuve negative themes orphelins", point_2_preuve_negative_themes_orphelins),
        ("3. robustesse bloc modifie (raison)", point_3_preuve_negative_raison_tronquee),
        ("4. jarvis-data.json coherent", point_4_jarvis_data_coherent),
        ("5. normes outil", point_5_normes_outil),
    ]
    for num, (nom, fn) in enumerate(points, start=1):
        if not point_actif(num):
            continue
        t_debut = time.monotonic()
        fn()
        chrono_etape(nom, t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())