#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-062-rating-protection.py
GARDE-FOU : le RATING (demande utilisateur 2026-08-15) est deploye partout :
  - la protection 'rating' est dans LISTE_PROTECTIONS de tester-protections
    (deploiement automatique sur tous les tests qui importent le module),
  - le template-test.md impose le bloc PROTECTIONS.afficher_rating en fin de
    main() (chaque futur test affiche le rating GENERAL des tests et le
    rating du test),
  - l outil evaluer-rating.py existe avec --profil/--cible/--tous/--general
    et produit une note /100,
  - le lanceur tester-lancer-non-regression v0.5.5 contient
    afficher_rating_fin_de_run (rating des series + rating general en fin de
    run).

Contexte :
  - Outil cree par Vulcain (evaluer/evaluer-rating, profils-rating.json),
    protection 'rating' ajoutee a tester-protections v0.2.0, template-test
    v0.4.0, lanceur v0.5.5.
  - Ce garde-fou verifie la chaine complete de deploiement - anti-recurrence
    d un rating present a un endroit mais oublie ailleurs.

Invariants verifies :
  1. tester-protections.py : la protection 'rating' est dans LISTE_PROTECTIONS
  2. tester-protections.py : la fonction afficher_rating existe
  3. template-test.md : le bloc PROTECTIONS.afficher_rating est present
  4. evaluer-rating.py existe, compile et affiche --version v0.1.0
  5. evaluer-rating --aide contient --profil/--cible/--tous/--general
  6. Le lanceur v0.5.5 contient afficher_rating_fin_de_run (--version v0.5.5)
  7. Preuve reelle : evaluer-rating --profil test --general retourne 0 et
     affiche RATING GENERAL
  8. profils-rating.json : les 5 profils (test, serie, outil, script-temp,
     fiche) avec poids somme = 100
  9. Normes : ASCII strict + LF pur (outil + doc + profils + test)
"""
import importlib.util
import io
import json
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

RATING_DIR = os.path.join(TOOLS_DIR, "evaluer", "evaluer-rating")
RATING_PY = os.path.join(RATING_DIR, "evaluer-rating.py")
RATING_MD = os.path.join(RATING_DIR, "evaluer-rating.md")
PROFILS = os.path.join(RATING_DIR, "profils-rating.json")
PROTECTIONS_PY = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                              "tester-protections.py")
TEMPLATE = os.path.join(TOOLS_DIR, "tester", "template-test.md")
LANCEUR_PY = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression",
                          "tester-lancer-non-regression.py")

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
    print("=== CHRONO test-062 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("[OK] %s" % nom)
    else:
        NB_KO += 1
        print("[KO] %s" % nom)
        if detail:
            print("     %s" % detail)


def lancer(cmd, timeout=60, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def lire(chemin):
    if not os.path.exists(chemin):
        return ""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def ascii_count(chemin):
    if not os.path.exists(chemin):
        return -1
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    if not os.path.exists(chemin):
        return -1
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    try:
        # 1. Protection 'rating' dans LISTE_PROTECTIONS
        if point_actif(1):
            t0 = time.monotonic()
            contenu = lire(PROTECTIONS_PY)
            verifier("1. protection 'rating' dans LISTE_PROTECTIONS",
                     '"rating"' in contenu and "afficher_rating" in contenu,
                     "fichier=%s" % PROTECTIONS_PY)
            chrono_etape("1. protection rating", t0)

        # 2. Fonction afficher_rating dans tester-protections
        if point_actif(2):
            t0 = time.monotonic()
            contenu = lire(PROTECTIONS_PY)
            verifier("2. def afficher_rating existe",
                     "def afficher_rating" in contenu, "")
            chrono_etape("2. fonction afficher_rating", t0)

        # 3. Bloc rating dans le template-test
        if point_actif(3):
            t0 = time.monotonic()
            contenu = lire(TEMPLATE)
            verifier("3. template-test : PROTECTIONS.afficher_rating",
                     "PROTECTIONS.afficher_rating" in contenu,
                     "fichier=%s" % TEMPLATE)
            chrono_etape("3. template-test", t0)

        # 4. evaluer-rating.py existe + compile + version
        if point_actif(4):
            t0 = time.monotonic()
            r = lancer([PYTHON, "-m", "py_compile", RATING_PY])
            rv = lancer([PYTHON, RATING_PY, "--version"])
            ok = (os.path.isfile(RATING_PY) and r.returncode == 0
                  and "v0.1.0" in (rv.stdout or ""))
            verifier("4. evaluer-rating v0.1.0 compile + --version", ok,
                     "rc=%s version=%s" % (r.returncode,
                                           (rv.stdout or "").strip()))
            chrono_etape("4. evaluer-rating", t0)

        # 5. Options cles dans l aide
        if point_actif(5):
            t0 = time.monotonic()
            r = lancer([PYTHON, RATING_PY, "--aide"])
            aide = (r.stdout or "") + (r.stderr or "")
            ok = all(o in aide for o in ["--profil", "--cible", "--tous",
                                         "--general"])
            verifier("5. --profil/--cible/--tous/--general dans l aide", ok,
                     "manquantes dans l aide (--aide)")
            chrono_etape("5. options", t0)

        # 6. Lanceur v0.5.5 + afficher_rating_fin_de_run
        if point_actif(6):
            t0 = time.monotonic()
            r = lancer([PYTHON, LANCEUR_PY, "--version"])
            contenu = lire(LANCEUR_PY)
            ok = ("v0.5.5" in (r.stdout or "")
                  and "afficher_rating_fin_de_run" in contenu)
            verifier("6. lanceur v0.5.5 + afficher_rating_fin_de_run", ok,
                     "version=%s" % (r.stdout or "").strip())
            chrono_etape("6. lanceur", t0)

        # 7. Preuve reelle : --general retourne 0 et affiche RATING GENERAL
        if point_actif(7):
            t0 = time.monotonic()
            r = lancer([PYTHON, RATING_PY, "--profil", "test", "--general",
                        "--no-chrono"], timeout=120)
            ok = (r.returncode == 0 and "RATING GENERAL" in (r.stdout or ""))
            verifier("7. evaluer-rating --profil test --general", ok,
                     "rc=%s sortie=%s" % (r.returncode,
                                          (r.stdout or "").strip()[-60:]))
            chrono_etape("7. preuve reelle", t0)

        # 8. profils-rating.json : 5 profils, poids somme = 100
        if point_actif(8):
            t0 = time.monotonic()
            try:
                with io.open(PROFILS, encoding="utf-8") as fh:
                    profils = json.load(fh)
                noms = set(profils["profils"].keys())
                ok_noms = {"test", "serie", "outil", "script-temp",
                           "fiche"}.issubset(noms)
                poids_ok = True
                for nom, cfg in profils["profils"].items():
                    total = sum(c.get("poids", 0)
                                for c in cfg.get("criteres", []))
                    if total != 100:
                        poids_ok = False
                verifier("8. 5 profils + poids somme=100",
                         ok_noms and poids_ok,
                         "profils=%s" % sorted(noms))
            except Exception as exc:
                verifier("8. 5 profils + poids somme=100", False,
                         "exception=%s" % exc)
            chrono_etape("8. profils", t0)

        # 9. Normes ASCII + LF pur (outil + doc + profils + test)
        if point_actif(9):
            t0 = time.monotonic()
            fichiers = [RATING_PY, RATING_MD, PROFILS,
                        os.path.abspath(__file__)]
            total_na = sum(ascii_count(f) for f in fichiers)
            total_crlf = sum(crlf_count(f) for f in fichiers)
            verifier("9. ASCII strict : 0 non-ASCII (outil + doc + profils + test)",
                     total_na == 0, "total=%d" % total_na)
            verifier("10. LF pur : 0 CRLF (outil + doc + profils + test)",
                     total_crlf == 0, "total=%d" % total_crlf)
            chrono_etape("9. normes", t0)

        # 11. Doc .md existe avec categorie Evaluer
        if point_actif(11):
            t0 = time.monotonic()
            contenu = lire(RATING_MD)
            verifier("11. doc .md existe avec categorie Evaluer",
                     os.path.isfile(RATING_MD) and "Evaluer" in contenu
                     and "Categorie" in contenu, "")
            chrono_etape("11. doc", t0)

    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO,
                                                               NB_POINTS))
    PROTECTIONS.afficher_rating("test-062-rating-protection")
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
