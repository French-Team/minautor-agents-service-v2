#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-127-evaluer-coherence-versioning-garde-fou.py
Garde-fou de l affinage evaluer-coherence v0.3.0 (mission cdd567d1) :
les liens des tableaux de versioning (changelog) sont ignores du scan des
liens casses, et les vrais liens casses restent detectes.

Corrections testees :
  1. ligne de tableau de versioning (| x.y.z | date | [lien](cible) |)
     -> lien IGNORE (placeholder documentaire)
  2. vrai lien casse hors tableau -> DETECTE
  3. lien valide hors tableau -> OK (existence resolue)
  4. parite py/sh : le .sh porte sa propre logique de liens (parseur
     embarque) - meme fixture, meme verdict
  5. versions alignees py 0.3.0-py / sh 0.3.0 / md 0.3.0

Tags: outils, evaluer, liens, versioning
"""
import importlib.util
import io
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


EVALUER_COHERENCE_PY = os.path.join(TOOLS_DIR, "evaluer", "evaluer-coherence",
                                    "evaluer-coherence.py")
EVALUER_COHERENCE_SH = os.path.join(TOOLS_DIR, "evaluer", "evaluer-coherence",
                                    "evaluer-coherence.sh")
EVALUER_COHERENCE_MD = os.path.join(TOOLS_DIR, "evaluer", "evaluer-coherence",
                                    "evaluer-coherence.md")

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


def run(cmd, timeout=120):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def creer_fixture():
    """Cree une fixture temporaire avec :
    - un fichier avec une ligne de tableau de versioning portant un lien
      vers une cible inexistante (doit etre IGNORE)
    - un vrai lien casse hors tableau (doit etre DETECTE)
    - un lien valide vers un fichier existant (doit rester OK)
    Retourne (dossier_fixture, chemin_test_md).
    """
    tmp = tempfile.mkdtemp(prefix="tmp-test127-")
    cerveau = os.path.join(tmp, "cerveau-projet")
    os.makedirs(cerveau)
    fichier = os.path.join(cerveau, "fiche.md")
    # Lien valide : cree le fichier cible a cote
    cible_valide = os.path.join(cerveau, "cible-valide.md")
    with io.open(cible_valide, "w", encoding="ascii", newline="\n") as fh:
        fh.write("# Cible valide\n")
    contenu = (
        "# Fiche de test\n"
        "\n"
        "Lien casse reel hors tableau:\n"
        "\n"
        "[fiche-inexistante](fiche-inexistante.md)\n"
        "\n"
        "Lien valide:\n"
        "\n"
        "[cible](cible-valide.md)\n"
        "\n"
        "Tableau de versioning (a ignorer):\n"
        "\n"
        "| Version | Date | Changements |\n"
        "|---|---|---|\n"
        "| 0.1.0 | 2026-01-01 | [ancien-ref](ancien-ref.md) |\n"
        "| 0.3.0 | 2026-09-05 | [protocole-X/](protocole-X/) |\n"
    )
    with io.open(fichier, "w", encoding="ascii", newline="\n") as fh:
        fh.write(contenu)
    return tmp, fichier


def charger_module_evaluer():
    ec_spec = importlib.util.spec_from_file_location(
        "evaluer_coherence_mod", EVALUER_COHERENCE_PY)
    ec_mod = importlib.util.module_from_spec(ec_spec)
    ec_spec.loader.exec_module(ec_mod)
    return ec_mod


def main():
    print("=== test-127 : evaluer-coherence exclut les tableaux de versioning ===")

    fixture = None
    try:
        # --- Point 1 : le lien du tableau de versioning est IGNORE ---
        if point_actif(1):
            _t0 = __import__("time").monotonic()
            fixture, _ = creer_fixture()
            ec_mod = charger_module_evaluer()
            # lister_liens_casses(racine) : racine = dossier contenant
            # cerveau-projet/ a scanner
            liens = ec_mod.lister_liens_casses(fixture)
            chemins = [c for _, c in liens]
            verifier("1. lien du tableau de versioning ignore (ancien-ref.md)",
                     "ancien-ref.md" not in chemins, "liens=%s" % chemins)
            verifier("2. lien protocole-X/ du versioning ignore",
                     "protocole-X/" not in chemins, "liens=%s" % chemins)
            chrono_etape("points 1-2 (fixture py)", _t0)

        # --- Point 3 : le vrai lien casse est DETECTE ---
        if point_actif(3):
            _t0 = __import__("time").monotonic()
            if fixture is None:
                fixture, _ = creer_fixture()
            ec_mod = charger_module_evaluer()
            liens = ec_mod.lister_liens_casses(fixture)
            chemins = [c for _, c in liens]
            verifier("3. vrai lien casse hors tableau detecte (fiche-inexistante.md)",
                     "fiche-inexistante.md" in chemins,
                     "liens=%s" % chemins)
            chrono_etape("point 3 (vrai lien casse)", _t0)

        # --- Point 4 : le lien valide n est PAS signale ---
        if point_actif(4):
            _t0 = __import__("time").monotonic()
            if fixture is None:
                fixture, _ = creer_fixture()
            ec_mod = charger_module_evaluer()
            liens = ec_mod.lister_liens_casses(fixture)
            chemins = [c for _, c in liens]
            verifier("4. lien valide non signale (cible-valide.md)",
                     "cible-valide.md" not in chemins, "liens=%s" % chemins)
            chrono_etape("point 4 (lien valide)", _t0)

        # --- Point 5 : parite .sh (parseur embarque, meme fixture) ---
        if point_actif(5):
            _t0 = __import__("time").monotonic()
            if fixture is None:
                fixture, _ = creer_fixture()
            r = run(["bash", EVALUER_COHERENCE_SH, fixture])
            sortie = (r.stdout or "") + (r.stderr or "")
            verifier("5. .sh detecte le vrai lien casse (parite py)",
                     "fiche-inexistante.md" in sortie,
                     "rc=%d sortie=%s" % (r.returncode, sortie[-200:]))
            verifier("6. .sh ignore le lien du tableau de versioning (parite py)",
                     "ancien-ref.md" not in sortie and "protocole-X/" not in sortie,
                     "sortie=%s" % sortie[-200:])
            chrono_etape("points 5-6 (parite sh)", _t0)

        # --- Points 7-8 : versions alignees ---
        if point_actif(7):
            _t0 = __import__("time").monotonic()
            r = run([PYTHON, EVALUER_COHERENCE_PY, "--version"])
            verifier("7. version py = 0.3.0-py", "0.3.0-py" in r.stdout,
                     "rc=%d sortie=%s" % (r.returncode, r.stdout))
            _tmp_vide = tempfile.mkdtemp(prefix="tmp-test127-vide-")
            try:
                r2 = run(["bash", EVALUER_COHERENCE_SH, _tmp_vide])
                verifier("8. version sh = 0.3.0", "v0.3.0" in (r2.stdout or ""),
                         "rc=%d sortie=%s" % (r2.returncode, r2.stdout))
            finally:
                shutil.rmtree(_tmp_vide, ignore_errors=True)
            verifier("9. version md = 0.3.0",
                     "**Version :** 0.3.0" in io.open(
                         EVALUER_COHERENCE_MD, encoding="utf-8",
                         errors="replace").read(),
                     "")
            chrono_etape("points 7-9 (versions)", _t0)

        # --- Points 10-11 : normes ASCII strict + LF pur ---
        if point_actif(10):
            _t0 = __import__("time").monotonic()
            fichiers = [EVALUER_COHERENCE_PY, EVALUER_COHERENCE_SH,
                        EVALUER_COHERENCE_MD, os.path.abspath(__file__)]
            total_non_ascii = sum(ascii_count(f) for f in fichiers)
            verifier("10. ASCII strict : 0 non-ASCII (outils + test)",
                     total_non_ascii == 0, "total=%d" % total_non_ascii)
            total_crlf = sum(crlf_count(f) for f in fichiers)
            verifier("11. LF pur : 0 CRLF (outils + test)",
                     total_crlf == 0, "total=%d" % total_crlf)
            chrono_etape("points 10-11 (normes)", _t0)
    finally:
        if fixture and os.path.isdir(fixture):
            shutil.rmtree(fixture, ignore_errors=True)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())