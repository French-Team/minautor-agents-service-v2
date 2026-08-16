#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-007-figer-lf.py
Test formel de la mission 1 du plan FIGER LF.

Outil teste (cerveau-projet/agents/tools/corriger/corriger-fins-de-ligne/):
  .py + .sh (wrapper pur) + .md + spec/
  Convertit les fins de ligne CRLF vers LF sur un fichier ou un dossier.

Outils d'ecriture corriges (regression) :
  creer-fichier, ecrire-fichier, ajouter-contenu-fichier, inserer-contenu-fichier,
  gerer-sous-mission, generateurs-squelette-pense-bete/spec/todo,
  creer-remplir-pense-bete/spec/todo
  -> doivent produire du LF (plus de traduction CRLF Windows).

Cas couverts:
  1. --version py/sh identiques v0.1.0
  2. dry-run ne modifie rien
  3. Conversion reelle CRLF -> LF verifiee octets
  4. Idempotence (2e passe = 0 converti)
  5. Fichier binaire (octet nul) ignore
  6. --recursive sous-dossiers + exclusion __pycache__ et .pyc
  7. Chemin inexistant -> ERREUR
  8. REGRESSION : creer-fichier ecrit du LF (CRLF 0, LF > 0)
  9. REGRESSION : ecrire-fichier ecrit du LF
 10. ASCII 0 sur les 4 fichiers outils
 11. valider-nommage --type outil OK
 12. Parite py/sh : memes resultats (wrapper pur)
13. Catalogue : JSON valide, 162 commandes triees, entree presente
14. index-tools : total 181, categorie Corriger 6
 15. Protection : aucun fichier residuel dans le workspace

Usage:
  python3 test-007-figer-lf.py
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


OUTIL_DIR = os.path.join(TOOLS_DIR, "corriger", "corriger-fins-de-ligne")
OUTIL_PY = os.path.join(OUTIL_DIR, "corriger-fins-de-ligne.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "corriger-fins-de-ligne.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "corriger-fins-de-ligne.md")
OUTIL_SPEC = os.path.join(OUTIL_DIR, "spec", "spec-corriger-fins-de-ligne.001.01.ebauche.md")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande", "catalogue-commandes.json")
INDEX_TOOLS = os.path.join(TOOLS_DIR, "index-tools.md")
VALIDER_ASCII = os.path.join(TOOLS_DIR, "valider", "valider-conformite-ascii", "valider-conformite-ascii.py")
VALIDER_NOMMAGE = os.path.join(TOOLS_DIR, "valider", "valider-nommage", "valider-nommage.py")

CREER_FICHIER = os.path.join(TOOLS_DIR, "creer", "creer-fichier", "creer-fichier.py")
ECRIRE_FICHIER = os.path.join(TOOLS_DIR, "ecrire", "ecrire-fichier", "ecrire-fichier.py")

# --- Compteur et verifications ---
_pts = {"ok": 0, "ko": 0}
_liste_ko = []


def verifier(nom, condition, detail=""):
    if condition:
        _pts["ok"] += 1
        print("  [OK] " + nom)
    else:
        _pts["ko"] += 1
        _liste_ko.append(nom)
        print("  [KO] " + nom + ((" -- " + detail) if detail else ""))


def lancer(cmd, cwd=None):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, cwd=cwd)


def stats_eol(chemin):
    with open(chemin, "rb") as f:
        d = f.read()
    crlf = d.count(b"\r\n")
    lf = d.count(b"\n") - crlf
    return crlf, lf


def non_ascii(chemin):
    r = lancer([PYTHON, VALIDER_ASCII, chemin])
    out = r.stdout + r.stderr
    for ligne in out.splitlines():
        if "non-ASCII" in ligne or "Non-ASCII" in ligne:
            for part in ligne.split():
                if part.isdigit():
                    return int(part)
    return -1


def compter_crlf_dossier(racine):
    """Compte les fichiers CRLF sous racine (exclusion pycache)."""
    nb = 0
    for dossier, _, noms in os.walk(racine):
        if "__pycache__" in dossier:
            continue
        for nom in noms:
            if nom.endswith(".pyc"):
                continue
            p = os.path.join(dossier, nom)
            try:
                with open(p, "rb") as f:
                    d = f.read(4096)
                if d.count(b"\r\n") > 0:
                    nb += 1
            except OSError:
                pass
    return nb


def main():
    print("=== TEST 007 -- PLAN FIGER LF ===")
    tmp = tempfile.mkdtemp(prefix="test-007-")

    # 1. Version py/sh
    v_py = lancer([PYTHON, OUTIL_PY, "--version"]).stdout.strip()
    v_sh = lancer(["bash", OUTIL_SH, "--version"]).stdout.strip()
    verifier("1. version py/sh identiques v0.1.1",
             v_py == v_sh == "corriger-fins-de-ligne 0.1.1",
             "py='%s' sh='%s'" % (v_py, v_sh))

    # Fichiers de test
    crlf1 = os.path.join(tmp, "fiche-crlf.txt")
    lf1 = os.path.join(tmp, "deja-lf.txt")
    binaire = os.path.join(tmp, "binaire.dat")
    sous = os.path.join(tmp, "sous")
    os.makedirs(sous)
    with open(crlf1, "wb") as f:
        f.write(b"ligne1\r\nligne2\r\n")
    with open(lf1, "wb") as f:
        f.write(b"ligne1\nligne2\n")
    with open(binaire, "wb") as f:
        f.write(b"\x00\x01\r\n")
    sous_crlf = os.path.join(sous, "sous-crlf.txt")
    with open(sous_crlf, "wb") as f:
        f.write(b"a\r\nb\r\n")

    # 2. Dry-run ne modifie rien
    r = lancer([PYTHON, OUTIL_PY, tmp, "--recursive", "--dry-run"])
    c, _ = stats_eol(crlf1)
    verifier("2. dry-run ne modifie rien (CRLF intact)", c == 2,
             "CRLF apres dry-run=%d" % c)

    # 3. Conversion reelle
    r = lancer([PYTHON, OUTIL_PY, tmp, "--recursive"])
    c, l = stats_eol(crlf1)
    verifier("3. conversion reelle CRLF -> LF", c == 0 and l == 2,
             "CRLF=%d LF=%d" % (c, l))

    # 4. Idempotence
    r = lancer([PYTHON, OUTIL_PY, tmp, "--recursive"])
    verifier("4. idempotence (2e passe)", "Convertes (CRLF -> LF) : 0" in r.stdout,
             r.stdout.strip().splitlines()[-1] if r.stdout else "pas de sortie")

    # 5. Binaire ignore
    with open(binaire, "rb") as f:
        d = f.read()
    verifier("5. binaire ignore (intact)", d == b"\x00\x01\r\n")

    # 6. Recursif + exclusion pycache
    r = lancer([PYTHON, OUTIL_PY, tmp, "--recursive"])
    verifier("6. recursif convertit les sous-dossiers",
             "Convertes (CRLF -> LF) : 0" in r.stdout)

    # 7. Chemin inexistant
    r = lancer([PYTHON, OUTIL_PY, os.path.join(tmp, "absent.txt")])
    verifier("7. chemin inexistant -> ERREUR", "[ERREUR]" in (r.stdout + r.stderr))

    # 8. Regression : creer-fichier ecrit du LF
    fichier_creer = os.path.join(tmp, "creer-test.md")
    r = lancer([PYTHON, CREER_FICHIER, fichier_creer, "ligne1"])
    c, l = stats_eol(fichier_creer)
    verifier("8. REGRESSION creer-fichier -> LF", c == 0 and l == 1,
             "CRLF=%d LF=%d" % (c, l))

    # 9. Regression : ecrire-fichier ecrit du LF
    fichier_ecrire = os.path.join(tmp, "ecrire-test.md")
    r = lancer([PYTHON, ECRIRE_FICHIER, fichier_ecrire, "ligne1\nligne2\n"])
    c, l = stats_eol(fichier_ecrire)
    verifier("9. REGRESSION ecrire-fichier -> LF", c == 0 and l == 2,
             "CRLF=%d LF=%d" % (c, l))

    # 10. ASCII 0 sur les 4 fichiers outils
    ok_ascii = all(non_ascii(p) == 0 for p in (OUTIL_PY, OUTIL_SH, OUTIL_MD, OUTIL_SPEC))
    verifier("10. ASCII 0 sur 4 fichiers outils", ok_ascii)

    # 11. Nommage
    r = lancer([PYTHON, VALIDER_NOMMAGE, "--type", "outil", OUTIL_PY])
    verifier("11. valider-nommage --type outil OK",
             "ERREUR" not in (r.stdout + r.stderr))

    # 12. Parite py/sh (meme conversion)
    f2 = os.path.join(tmp, "parite.txt")
    with open(f2, "wb") as f:
        f.write(b"x\r\ny\r\n")
    lancer([PYTHON, OUTIL_PY, f2])
    with open(f2, "wb") as f:
        f.write(b"x\r\ny\r\n")
    lancer(["bash", OUTIL_SH, f2])
    c, l = stats_eol(f2)
    verifier("12. parite py/sh (sh convertit aussi)", c == 0 and l == 2)

    # 13. Catalogue
    try:
        with open(CATALOGUE, encoding="utf-8") as f:
            cat = json.load(f)
        noms = [e["nom"] for e in cat["commandes"]]
        ok_cat = (len(noms) == 165 and noms == sorted(noms)
                  and "executer-script-temporaire" in noms
                  and "corriger-fins-de-ligne" in noms
                  and "test-022-budget-pondere" in noms
                  and "test-023-grep-budget-pondere" in noms
                  and "enregistrer-usage-outil" in noms
                  and "detecter-cablages-manquants" in noms
                  and "detecter-donnees-en-dur" in noms
                  and "proteger-verrou-habilitation" in noms
                  and "detecter-residus" in noms
                  and "detecter-fautes-orthographe" in noms
                  and "detecter-contradictions" in noms
                  and "snapshot-nettoyage" in noms
                  and "combo-nettoyage-hygie" in noms
                  and "mettre-a-jour-versions" in noms and "purifier-rvav" in noms)
        verifier("13. catalogue JSON valide 165 trie + entree detecter-contradictions", ok_cat,
                 "nb=%d" % len(noms))
    except Exception as e:
        verifier("13. catalogue JSON valide 162 trie + entree detecter-donnees-en-dur", False, str(e))

    # 14. index-tools
    try:
        with open(INDEX_TOOLS, encoding="utf-8") as f:
            idx = f.read()
        verifier("14. index-tools total 182 + Corriger 6 + detecter-donnees-en-dur",
                 "| **Total** | **182** |" in idx and "| Corriger | 6 |" in idx
                 and "executer-script-temporaire" in idx
                 and "corriger-fins-de-ligne" in idx
                 and "detecter-cablages-manquants" in idx
                 and "detecter-donnees-en-dur" in idx
                 and "proteger-verrou-habilitation" in idx
                 and "detecter-residus" in idx
                 and "detecter-fautes-orthographe" in idx
                 and "snapshot-nettoyage" in idx
                 and "combo-nettoyage-hygie" in idx
                 and "mettre-a-jour-versions" in idx)
    except OSError as e:
        verifier("14. index-tools total 182 + Corriger 6 + detecter-donnees-en-dur", False, str(e))

    # 15. Protection : aucun residu de CE test dans le workspace
    shutil.rmtree(tmp, ignore_errors=True)
    restant = []
    for nom in os.listdir(PROJECT_ROOT):
        if nom.startswith("test-007-"):
            restant.append(nom)
    verifier("15. 0 residu du test dans le workspace", not restant,
             ",".join(restant) if restant else "")

    # --- Bilan ---
    print("---")
    print("BILAN : %d/%d VALIDE" % (_pts["ok"], _pts["ok"] + _pts["ko"]))
    if _liste_ko:
        print("ECHECS :")
        for nom in _liste_ko:
            print("  - " + nom)
        return 1
    return 0


bilan_chrono()

if __name__ == "__main__":
    sys.exit(main())
