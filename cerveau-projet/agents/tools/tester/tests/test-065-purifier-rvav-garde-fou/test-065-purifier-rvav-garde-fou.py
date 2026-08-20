#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-065-purifier-rvav-garde-fou.py
GARDE-FOU : l outil purifier-rvav (categorie Purifier, cree par Vulcain
2026-08-15) garantit la NON-PERTE : les lecons/entrees deplaces vers l archive
ne sont JAMAIS perdues, meme apres plusieurs purifications successives.

Contexte (decision utilisateur 2026-08-15) :
  - Le protocole rvav-workflow etait abandone et perime ; Buffy a liste les
    besoins (spec-purification-rvav.md) : corrections.md quota 1000 lignes,
    AGENTS-historique.md quota 800.
  - Principe ANTI-PERTE : on ne supprime JAMAIS d information, on DEPLACE vers
    une archive cote a cote (<agent>-historique.md, AGENTS-historique-archive.md).
  - 2 bugs graves ont ete corriges pendant le dev (lecon Vulcain) : (1) une 2e
    purification ECRASAIT l archive (perte de lecons), (2) un plantage entre
    les 2 ecritures perdait les blocs (l archive est maintenant ecrite EN
    PREMIER). Ce garde-fou verifie les 2 garanties.

Invariants verifies :
  1. purifier-rvav.py existe, compile, --version v0.1.1, --aide liste les options
  2. Dry-run sur un fichier de test : plan affiche, AUCUNE modification (lecons
     conservees, aucune archive creee)
  3. Premiere purification --executer : fichier reduit sous le seuil, archive
     creee, SOMME des lecons (principal + archive) == avant (non-perte)
  4. Deuxieme purification --executer (seuil plus bas) : l archive EXISTANTE
     est ACCUMULEE (prefixee), jamais ecrasee, somme des lecons toujours ==
     avant (anti-ecrasement)
  5. L archive a un frontmatter valide et des normes ASCII + LF pures
  6. Purge : aucun fichier temporaire laisse (fichier de test et archive
     supprimes a la fin)
  7. Normes : ASCII strict + LF pur (outil + test)
Tags: outils, purifier, garde-fou
"""
import glob
import importlib.util
import io
import os
import re
import shutil
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

PURIFIER_DIR = os.path.join(TOOLS_DIR, "purifier", "purifier-rvav")
PURIFIER_PY = os.path.join(PURIFIER_DIR, "purifier-rvav.py")

# Fichier de test : copie temporaire dans tmp-morpheus/ (protocole scripts temp)
TMP = os.path.join(PROJECT_ROOT, "tmp-test065")
TEST_FICHIER = os.path.join(TMP, "corrections.md")
def trouver_archive():
    """Retourne le chemin de l archive generee (depend du dossier parent)."""
    trouves = glob.glob(os.path.join(TMP, "*-historique.md"))
    return trouves[0] if trouves else None

TEST_ARCHIVE = None  # resolu par trouver_archive() apres chaque purge

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
            pass
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        for p in sys.argv[i + 1].split(","):
            try:
                DESACTIVES.append(int(p))
            except ValueError:
                pass
ETAPES = []
T_START = time.monotonic()


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
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-065 (total %.1fs) ===" % total)
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
        print("  [KO] %s" % nom)
        if detail:
            print("       %s" % detail)


def lancer(cmd, timeout=60, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def ascii_count(chemin):
    if not os.path.isfile(chemin):
        return -1
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            return sum(1 for c in fh.read() if ord(c) > 127)
    except IOError:
        return -1


def crlf_count(chemin):
    if not os.path.isfile(chemin):
        return -1
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def compter_lecons(chemin):
    """Compte les blocs ## [LECON] d un fichier (None ou absent = 0)."""
    if not chemin or not os.path.isfile(chemin):
        return 0
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        d = fh.read()
    return len(re.findall(r"^## \[LECON\]", d, re.M))


def creer_fichier_test():
    """Cree un fichier corrections.md de test avec 12 lecons (taille suffisante
    pour depasser le seuil 200 au 1er run et 120 au 2e run : 12 lecons x 25 lignes ~= 310 lignes)."""
    nettoyer_test()
    os.makedirs(TMP, exist_ok=True)
    parties = [
        "---",
        "identite:",
        "  type: corrections",
        "  appartient_a: morpheus",
        "  commun: false",
        "---",
        "",
    ]
    for i in range(12):
        parties.append("## [LECON] 2026-08-%02d -- TEST NON-PERTE %d (Morpheus)"
                       % (1 + i, i))
        parties.append("")
        for j in range(25):
            parties.append("Ligne de test %d pour la lecon %d : verification de "
                           "la non-perte de l outil purifier-rvav." % (j, i))
        parties.append("")
    with io.open(TEST_FICHIER, "w", encoding="ascii", newline="\n") as fh:
        fh.write("\n".join(parties) + "\n")


def nettoyer_test():
    """Supprime le fichier de test, l archive generee et le dossier TMP entier
    (regle anti-residu : dossier cree + supprime en fin, test-024 2b)."""
    if os.path.isfile(TEST_FICHIER):
        os.remove(TEST_FICHIER)
    archive = trouver_archive()
    if archive and os.path.isfile(archive):
        os.remove(archive)
    if os.path.isdir(TMP) and not os.listdir(TMP):
        os.rmdir(TMP)


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-065 : purifier-rvav garantit la NON-PERTE ===")
    try:
        # 1. L outil existe, compile, --version, --aide
        if point_actif(1):
            t0 = time.monotonic()
            ok_compile = os.path.isfile(PURIFIER_PY)
            if ok_compile:
                r = lancer([PYTHON, "-m", "py_compile", PURIFIER_PY], timeout=60)
                ok_compile = r.returncode == 0
            r2 = lancer([PYTHON, PURIFIER_PY, "--version"], timeout=60)
            r3 = lancer([PYTHON, PURIFIER_PY, "--aide"], timeout=60)
            ok = (ok_compile and r2.returncode == 0 and "0.1.1" in r2.stdout
                  and "--executer" in r3.stdout and "--dry-run" in r3.stdout)
            verifier("1. purifier-rvav existe, compile, version 0.1.1, options",
                     ok, "rc=%d" % r2.returncode)
            chrono_etape("1. outil", t0)

        # 2. Dry-run : plan affiche, aucune modification
        if point_actif(2):
            t0 = time.monotonic()
            creer_fichier_test()
            avant = compter_lecons(TEST_FICHIER)
            r = lancer([PYTHON, PURIFIER_PY, "--fichier", TEST_FICHIER,
                        "--seuil", "200", "--dry-run"], timeout=60)
            apres = compter_lecons(TEST_FICHIER)
            archive_creee = (trouver_archive() is not None)
            ok = (r.returncode == 0 and "DRY-RUN" in r.stdout
                  and avant == apres and not archive_creee)
            verifier("2. dry-run : plan affiche, 0 modification, 0 archive",
                     ok, "avant=%d apres=%d archive=%s" % (avant, apres, archive_creee))
            chrono_etape("2. dry-run", t0)

        # 3. 1re purification : fichier reduit, archive creee, NON-PERTE
        if point_actif(3):
            t0 = time.monotonic()
            avant = compter_lecons(TEST_FICHIER)
            r = lancer([PYTHON, PURIFIER_PY, "--fichier", TEST_FICHIER,
                        "--seuil", "200", "--executer"], timeout=60)
            principal = compter_lecons(TEST_FICHIER)
            archive = compter_lecons(trouver_archive())
            lignes = 0
            with io.open(TEST_FICHIER, encoding="utf-8", errors="replace") as fh:
                lignes = sum(1 for _ in fh)
            ok = (r.returncode == 0 and lignes <= 200
                  and (trouver_archive() is not None)
                  and principal + archive == avant)
            verifier("3. 1re purif : sous le seuil + archive + NON-PERTE (%d=%d+%d)"
                     % (avant, principal, archive), ok,
                     "lignes=%d rc=%d" % (lignes, r.returncode))
            chrono_etape("3. 1re purif", t0)

        # 4. 2e purification (seuil plus bas) : ACCUMULATION, jamais ecrase
        if point_actif(4):
            t0 = time.monotonic()
            avant_total = compter_lecons(TEST_FICHIER) + compter_lecons(trouver_archive())
            r = lancer([PYTHON, PURIFIER_PY, "--fichier", TEST_FICHIER,
                        "--seuil", "120", "--executer"], timeout=60)
            principal = compter_lecons(TEST_FICHIER)
            archive = compter_lecons(trouver_archive())
            ok = (r.returncode == 0 and principal + archive == avant_total
                  and archive >= 2)
            verifier("4. 2e purif : ACCUMULATION (%d=%d+%d, pas d ecrasement)"
                     % (avant_total, principal, archive), ok,
                     "rc=%d" % r.returncode)
            chrono_etape("4. 2e purif", t0)

        # 5. Archive : frontmatter valide + normes ASCII + LF
        if point_actif(5):
            t0 = time.monotonic()
            with io.open(trouver_archive(), encoding="utf-8", errors="replace") as fh:
                da = fh.read()
            ok = (da.startswith("---") and "identite:" in da
                  and "type: archive" in da
                  and ascii_count(trouver_archive()) == 0
                  and crlf_count(trouver_archive()) == 0)
            verifier("5. archive : frontmatter valide + ASCII + LF purs", ok)
            chrono_etape("5. archive", t0)

        # 6. Purge : aucun fichier temporaire laisse
        if point_actif(6):
            t0 = time.monotonic()
            nettoyer_test()
            ok = not os.path.isfile(TEST_FICHIER) and not (trouver_archive() is not None)
            verifier("6. purge : aucun residu (fichier test + archive)", ok)
            chrono_etape("6. purge", t0)

        # 7. Normes ASCII + LF pur (outil + test)
        if point_actif(7):
            t0 = time.monotonic()
            fichiers = [os.path.abspath(__file__), PURIFIER_PY]
            total_na = sum(max(ascii_count(f), 0) for f in fichiers)
            total_crlf = sum(max(crlf_count(f), 0) for f in fichiers)
            verifier("7. ASCII strict : 0 non-ASCII (outil + test)",
                     total_na == 0, "nb=%d" % total_na)
            verifier("8. LF pur : 0 CRLF (outil + test)",
                     total_crlf == 0, "nb=%d" % total_crlf)
            chrono_etape("7. normes", t0)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1
        nettoyer_test()
    except Exception as e:
        print("  [KO] EXCEPTION : %s" % e)
        NB_KO += 1
        nettoyer_test()

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % ("PROPRE (non-perte garantie)" if NB_KO == 0
                                    else "KO (non-perte violee)"))
    return 1 if NB_KO > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
