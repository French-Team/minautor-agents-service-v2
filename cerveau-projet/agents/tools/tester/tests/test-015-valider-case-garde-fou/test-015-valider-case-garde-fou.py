#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-015-valider-case-garde-fou.py
Test formel du garde-fou anti-pollution de valider-case v1.1.1
(lecon : rapport a la racine cree par une commande sans --rapport).

Contexte :
  - valider-case v1.0.0 ecrivait son rapport par defaut
    (rapport-valider-case-<date>.md) dans le repertoire courant quand
    --rapport et --dry-run etaient absents.
  - v1.0.2 : convention de nommage etendue (prefixe thematique cT* pour la ligne trio Janus) ; v1.0.1 : sans --rapport <fichier> explicite, AUCUN fichier n'est cree
    (message 'AUCUN RAPPORT ECRIT') ; --rapport <fichier> ecrit exactement
    au chemin fourni ; --dry-run simule sans ecrire.

Cas couverts:
  1. Parite --version py/sh v1.0.2
  2. Sans --rapport ni --dry-run (depuis un dossier vide) : aucun fichier cree
  3. Message 'AUCUN RAPPORT ECRIT' affiche
  4. --dry-run : aucun fichier cree
  5. --rapport <fichier> : fichier cree exactement au chemin fourni
  6. --rapport <fichier> --dry-run : fichier NON cree
  7. Verdict CONFORME sur parcours-cerberus (non-regression)
  8. ASCII strict : 0 non-ASCII (outil + test)
  9. LF pur : 0 CRLF (outil + test)
 10. Garde-fou positif v1.0.2 : ACCEPTATION d'un id cT* (convention etendue,
     prefixe thematique majuscule - ligne Trio de Janus)

Usage:
  python3 test-015-valider-case-garde-fou.py
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
OUTIL_SH = os.path.join(OUTIL_DIR, "valider-case.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "valider-case.md")
OUTIL_SPEC = os.path.join(OUTIL_DIR, "spec", "spec-valider-case.001.01.ebauche.md")
PARCOURS_CERBERUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                 "cerberus", "parcours", "parcours-cerberus.json")

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


def run(cmd, cwd=None, timeout=60):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout,
                          cwd=cwd)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-015-")
    try:
        print("=== Test formel valider-case v1.1.1 (garde-fou rapport) ===")

        # 1. Parite --version py/sh v1.0.2
        r_py = run([PYTHON, OUTIL_PY, "--version"])
        r_sh = run(["bash", OUTIL_SH, "--version"])
        verifier("1. --version py/sh identiques v1.0.2",
                 r_py.returncode == 0 and r_sh.returncode == 0
                 and "v1.1.1" in r_py.stdout
                 and r_py.stdout.strip() == r_sh.stdout.strip(),
                 "py=%r sh=%r" % (r_py.stdout.strip(), r_sh.stdout.strip()))

        # 2. Sans --rapport ni --dry-run depuis un dossier vide : aucun fichier
        dossier_vide = os.path.join(tmp, "vide")
        os.makedirs(dossier_vide)
        avant = set(os.listdir(dossier_vide))
        r_gf = run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS], cwd=dossier_vide)
        apres = set(os.listdir(dossier_vide))
        verifier("2. Sans --rapport ni --dry-run : aucun fichier cree",
                 r_gf.returncode == 0 and avant == apres,
                 "cree: %s" % (apres - avant))

        # 3. Message AUCUN RAPPORT ECRIT
        verifier("3. Message 'AUCUN RAPPORT ECRIT' affiche",
                 "AUCUN RAPPORT ECRIT" in r_gf.stdout,
                 r_gf.stdout.strip()[-80:])

        # 4. --dry-run : aucun fichier cree
        dossier_dr = os.path.join(tmp, "dry")
        os.makedirs(dossier_dr)
        avant = set(os.listdir(dossier_dr))
        r_dr = run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS, "--dry-run"],
                   cwd=dossier_dr)
        apres = set(os.listdir(dossier_dr))
        verifier("4. --dry-run : aucun fichier cree",
                 r_dr.returncode == 0 and avant == apres,
                 "cree: %s" % (apres - avant))

        # 5. --rapport <fichier> : fichier cree au chemin fourni
        rapport = os.path.join(tmp, "mon-rapport.md")
        r_rp = run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS, "--rapport", rapport])
        verifier("5. --rapport <fichier> : fichier cree au chemin fourni",
                 r_rp.returncode == 0 and os.path.isfile(rapport)
                 and "RAPPORT ECRIT" in r_rp.stdout,
                 "existe=%s" % os.path.isfile(rapport))

        # 6. --rapport + --dry-run : fichier NON cree
        rapport2 = os.path.join(tmp, "simule.md")
        r_dr2 = run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS, "--rapport", rapport2,
                     "--dry-run"])
        verifier("6. --rapport + --dry-run : fichier NON cree",
                 r_dr2.returncode == 0 and not os.path.isfile(rapport2)
                 and "DRY-RUN" in r_dr2.stdout,
                 "existe=%s" % os.path.isfile(rapport2))

        # 7. Verdict CONFORME sur parcours-cerberus (non-regression)
        verifier("7. Non-regression : cerberus CONFORME",
                 "CONFORME" in r_gf.stdout and "erreurs: 0" in r_gf.stdout,
                 r_gf.stdout.strip()[:100])

        # 10. GARDE-FOU POSITIF v1.0.2 (lecon Morpheus 2026-08-11) : la
        #      convention etendue doit ACCEPTER les ids cT* (prefixe
        #      thematique majuscule, ligne Trio de Janus). Parcours
        #      artificiel minimal : depart c0 -> fin cT10.
        ct = os.path.join(tmp, "parcours-ct.json")
        with io.open(ct, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({
                "parcours": {"agent": "test-ct", "version": "0.1.0",
                             "case_depart": "c0"},
                "cases": {
                    "c0": {"type": "question", "titre": "Depart",
                            "question": "Tester la fin cT ?",
                            "branches": [
                                {"reponse": "OUI", "vers": "cT10"},
                                {"reponse": "NON", "vers": "cT10"}]},
                    "cT10": {"type": "fin", "titre": "Fin ligne Trio"},
                },
            }, fh, ensure_ascii=True, indent=2)
        r_ct = run([PYTHON, OUTIL_PY, ct, "--dry-run"])
        verifier("10. Garde-fou positif : id cT10 ACCEPTE (0 erreur NOMMAGE)",
                 r_ct.returncode == 0 and "CONFORME" in r_ct.stdout
                 and "erreurs: 0" in r_ct.stdout
                 and "NOMMAGE" not in r_ct.stdout,
                 r_ct.stdout.strip()[:120])

        # 8. ASCII strict (outil 4 fichiers + test)
        total_non_ascii = sum(ascii_count(f) for f in
                              (OUTIL_PY, OUTIL_SH, OUTIL_MD, OUTIL_SPEC,
                               os.path.abspath(__file__)))
        verifier("8. ASCII strict : 0 non-ASCII (4 fichiers outil + test)",
                 total_non_ascii == 0, "total non-ASCII = %d" % total_non_ascii)

        # 9. LF pur (outil + test)
        total_crlf = sum(crlf_count(f) for f in
                         (OUTIL_PY, OUTIL_SH, OUTIL_MD, OUTIL_SPEC,
                          os.path.abspath(__file__)))
        verifier("9. LF pur : 0 CRLF (4 fichiers outil + test)",
                 total_crlf == 0, "total CRLF = %d" % total_crlf)

        print("")
        bilan_chrono()
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
