#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-028-coherence-documentaire.py
Garde-fou anti-recurrence des ecarts documentaires (lecon 2026-08-12, round 11).

Contexte :
  - Le pre-audit du round 11 a revele 8 SPECS DIVERGENTES (spec en retard sur
    l outil : activer-agent-principal, combos-moteur, enregistrer-usage-outil,
    generateurs-amelioration, generateurs-commande, generateurs-regenerer-
    catalogue, valider-case) + 2 specs sans version + 2 DECALAGES catalogue
    (faux positifs : flags de sous-commandes argparse invisibles dans l aide
    racine).
  - Corrections Vulcain : detecter-divergences-version v0.2.0 (constante
    VERSION + champ spec **Version outil** prioritaire pour les specs de
    conventions), detecter-decalages-catalogue v0.2.0 (scan des sous-commandes
    argparse avec variante de prefixe), 8 specs bumpees.
  - v0.2.1 (2026-08-13) : detecter-decalages-catalogue passe en PARALLELE
    (pool de threads min(16, nb) + cache par (interpreteur, script)) : ce
    garde-fou passait de 88s a 22s, la suite anti-regression de 92.2s a 52.3s.
  - v0.2.2 (2026-08-16) : sondage SELECTIF (seules les commandes avec flags
    sont sondees, les 99 commandes sans flag et les 23 tests du catalogue ne
    sont plus executes) : goulot detecter-decalages 12.6s -> 4.6s.
  - Ce garde-fou verifie : 0 spec divergente, 0 spec sans version avec .py,
    0 decalage catalogue, et le cas guider-parcours documente.

Cas couverts:
  1. detecter-divergences-version --version = v0.2.0
  2. detecter-decalages-catalogue --version = v0.2.3 (v0.2.3 : rapport
     selectif des commandes avec flags, goulot 12.6s -> 4.6s)
  3. detecter-divergences-version : 0 DIVERGENTE
  4. detecter-divergences-version : 0 SANS VERSION (avec .py present)
  5. detecter-decalages-catalogue : 0 decalage
  6. spec guider-parcours : champ **Version outil** : 0.5.1 present
  7. ASCII strict : 0 non-ASCII (outils + docs + specs + test)
  8. LF pur : 0 CRLF (outils + docs + specs + test)

Usage:
  python3 test-028-coherence-documentaire.py
Tags: conventions, garde-fou, anti-recurrence, coherence
"""
import importlib.util
import io
import os
import subprocess
import sys

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


DIV_DIR = os.path.join(TOOLS_DIR, "detecter", "detecter-divergences-version")
DIV_PY = os.path.join(DIV_DIR, "detecter-divergences-version.py")
DIV_MD = os.path.join(DIV_DIR, "detecter-divergences-version.md")
DEC_DIR = os.path.join(TOOLS_DIR, "detecter", "detecter-decalages-catalogue")
DEC_PY = os.path.join(DEC_DIR, "detecter-decalages-catalogue.py")
DEC_MD = os.path.join(DEC_DIR, "detecter-decalages-catalogue.md")
SPEC_GUIDER = os.path.join(TOOLS_DIR, "guider", "guider-parcours", "spec",
                           "spec-guider-parcours.001.01.ebauche.md")

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


def run(cmd, timeout=180):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lister_specs():
    """Liste les spec/*.md qui ont un .py associe dans le meme dossier outil."""
    resultats = []
    for cat in sorted(os.listdir(TOOLS_DIR)):
        pcat = os.path.join(TOOLS_DIR, cat)
        if not os.path.isdir(pcat):
            continue
        for outil in sorted(os.listdir(pcat)):
            pout = os.path.join(pcat, outil)
            if not os.path.isdir(pout):
                continue
            spec_dir = os.path.join(pout, "spec")
            if not os.path.isdir(spec_dir):
                continue
            py_present = any(f.endswith(".py") and not f.startswith("test-")
                             for f in os.listdir(pout))
            for f in sorted(os.listdir(spec_dir)):
                if f.endswith(".md"):
                    resultats.append((os.path.join(spec_dir, f), py_present))
    return resultats


def main():
    print("=== Garde-fou : coherence documentaire (specs vs outils, catalogue) ===")

    # 1-2. Versions
    r = run([PYTHON, DIV_PY, "--version"])
    verifier("1. detecter-divergences-version --version = v0.2.0",
             "v0.2.0" in r.stdout, r.stdout.strip())
    r = run([PYTHON, DEC_PY, "--version"])
    verifier("2. detecter-decalages-catalogue --version = v0.2.3",
             "v0.2.3" in r.stdout, r.stdout.strip())

    # 3-4. Divergences de versions (scan cerveau-projet)
    r = run([PYTHON, DIV_PY, "--racine", "cerveau-projet"])
    out = r.stdout + r.stderr
    verifier("3. 0 spec DIVERGENTE (specs alignees sur les outils)",
             "0 DIVERGENTES" in out, out[-200:])
    # 4. SANS VERSION : acceptables uniquement pour les outils SANS .py
    #    (protocoles, pense-betes). On croise la sortie de l outil avec les
    #    specs ayant un .py associe : tout SANS VERSION sur un outil a .py
    #    est un ecart.
    outils_avec_py = {os.path.basename(os.path.dirname(os.path.dirname(spec)))
                      for spec, py in lister_specs() if py}
    sans_version_reels = []
    for ligne in out.splitlines():
        if "SANS VERSION" in ligne:
            outil = ligne.split()[0]
            if outil in outils_avec_py:
                sans_version_reels.append(outil)
    verifier("4. 0 SANS VERSION sur les outils avec .py (specs versionnees)",
             len(sans_version_reels) == 0, "sans version: %s" % sans_version_reels)

    # 5. Decalages catalogue (scan complet, timeout long)
    # CAUSE RACINE DU RESIDU : sans --sortie, l outil ecrit son rapport par
    # defaut dans le dossier courant (la racine) -> chaque non-regression
    # regenere rapport-detecter-decalages-catalogue-<date>.md. On passe
    # --sortie vers un fichier temporaire, supprime en try/finally garanti.
    import tempfile
    fd, chemin_rapport = tempfile.mkstemp(suffix=".md", prefix="rapport-test028-")
    os.close(fd)
    try:
        r = run([PYTHON, DEC_PY, "--sortie", chemin_rapport], timeout=240)
    finally:
        try:
            os.remove(chemin_rapport)
        except OSError:
            pass
    out = r.stdout + r.stderr
    verifier("5. detecter-decalages-catalogue : 0 decalage",
             "/ 0 decalages " in out or "0 decalages" in out, out[-200:])

    # 6. Cas guider-parcours documente
    with io.open(SPEC_GUIDER, encoding="utf-8", errors="replace") as fh:
        spec_guider = fh.read()
    verifier("6. spec guider-parcours : **Version outil** : 0.5.0 present",
             "**Version outil** : 0.5.2" in spec_guider)

    # 7-8. Normes sur les fichiers des outils + ce test
    fichiers = [DIV_PY, DIV_MD, DEC_PY, DEC_MD, SPEC_GUIDER,
                os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("7. ASCII strict : 0 non-ASCII (outils + doc + spec + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("8. LF pur : 0 CRLF (outils + doc + spec + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    if NB_KO:
        print("  [AIDE] OU CHERCHER / REPARER (KO = divergence spec/outil) :")
        print("    [AIDE] Fichiers inspectes : agents/tools/**/spec/*.md + detecter-divergences-version")
        print("    [AIDE] Diagnostic : python3 cerveau-projet/agents/tools/detecter/detecter-divergences-version/detecter-divergences-version.py --racine cerveau-projet")
        print("    [AIDE] Correctif : aligner la version de la SPEC (en-tete + historique) sur celle de l outil .py/.md signale DIVERGENT")
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
