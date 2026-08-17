#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-038-badge-readme-synchronise.py
GARDE-FOU ANTI-RECURRENCE : le badge Outils-N du README (header) doit etre
synchronise avec le compte reel des outils - tant l AFFICHAGE que le HREF
(lecon Clio/Janus 2026-08-13 : le badge affichait 128 mais le lien pointait
vers 121 apres la grosse MAJ README).

Contexte (2026-08-13) :
  - Lecon Clio/Janus : combos-maj-readme-massive reconstruisait les tables
    de categories mais pas le badge Outils-N en dur du header, et le lien
    href pouvait rester obsolete (ex : affichage 128, lien 121).
  - Buffy a ameliore combos-maj-readme-massive v0.1.1 : la fonction
    aligner_badge_header(racine) aligne automatiquement l affichage ET le
    href sur le compte reel (source de verite : compter_outils de
    combos-analyse-projet).
  - Ce garde-fou verifie en permanence que le badge reste synchronise :
    l affichage et le href doivent tous deux egaler le compte reel.

Invariants verifies :
  1. Le README contient un badge Outils-N dans le header (au moins 2
     occurrences de badge/Outils-<n>- : affichage + href)
  2. L affichage du badge == compte reel des outils (compter_outils)
  3. Le href du badge == compte reel des outils (pas de divergence
     display/href comme le bug 128/121)
  4. Badge Version == v + contenu de clio/version-readme.txt
     (source de verite maintenue par Clio, ex : v0.2.0)
  5. Badge Statut == contenu de clio/statut-projet.txt
     (source de verite : prepare/dev/stable)
  6. Coherence href des badges statiques (Plateforme, Fait_avec,
     Langages) : l affichage et le href sont identiques
  7. Normes : ASCII strict + LF pur (README + test)
Tags: conventions, readme, garde-fou, anti-recurrence
"""
import importlib.util
import io
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
README = os.path.join(PROJECT_ROOT, "README.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


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


def charger_compter_outils():
    """Charger compter_outils depuis combos-analyse-projet (source de verite).
    importlib requis : le nom du module source contient des tirets."""
    chemin = os.path.join(TOOLS_DIR, "combos", "combos-analyse-projet",
                          "combos-analyse-projet.py")
    spec = importlib.util.spec_from_file_location("combos_analyse_projet", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def verifier(nom, ok, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if ok:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, detail))


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Test formel badge-readme-synchronise ===")

    # 1. README lisible et contient un badge Outils-N
    try:
        texte = io.open(README, encoding="utf-8", errors="replace").read()
    except Exception as e:
        verifier("1. README lisible et badge Outils-N present", False, str(e))
        texte = ""

    occurrences = re.findall(r"badge/Outils-([0-9]+)-", texte)
    verifier("1. README contient un badge Outils-N (affichage + href)",
             len(occurrences) >= 2, "occurrences=%s" % occurrences)

    # 2. L affichage == compte reel
    try:
        analyse = charger_compter_outils()
        categories = analyse.compter_outils(PROJECT_ROOT)
        nb_reel = sum(categories.values())
    except Exception as e:
        nb_reel = -1
        verifier("2. Affichage badge == compte reel", False, str(e))
    if nb_reel >= 0:
        affichage = int(occurrences[0]) if occurrences else -1
        verifier("2. Affichage badge (%d) == compte reel (%d)" % (affichage, nb_reel),
                 affichage == nb_reel, "affichage=%d reel=%d" % (affichage, nb_reel))

    # 3. Le href == compte reel (pas de divergence display/href)
    if len(occurrences) >= 2 and nb_reel >= 0:
        href = int(occurrences[1])
        verifier("3. Href badge (%d) == compte reel (%d)" % (href, nb_reel),
                 href == nb_reel, "href=%d reel=%d" % (href, nb_reel))

    # 3b. Badge Version == v + contenu de version-readme.txt
    try:
        f_version = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "clio", "version-readme.txt")
        v_src = io.open(f_version, encoding="utf-8").read().strip()
        v_occ = re.findall(r"badge/Version-v([0-9.]+)-", texte)
        # l occurrence est capturee sans le v (le v est dans le motif) ;
        # la source est un semver sans v -> comparaison directe
        ok_ver = len(v_occ) >= 2 and v_occ[0] == v_src and v_occ[1] == v_src
        verifier("3b. Badge Version (v%s) == source (v%s) affichage + href" %
                 (v_occ[0] if v_occ else "?", v_src), ok_ver,
                 "occ=%s source=%s" % (v_occ, v_src))
    except Exception as e:
        verifier("3b. Badge Version == source version-readme.txt", False, str(e))

    # 3c. Badge Statut == contenu de statut-projet.txt
    try:
        f_statut = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "clio", "statut-projet.txt")
        s_src = io.open(f_statut, encoding="utf-8").read().strip()
        s_occ = re.findall(r"badge/Statut-([^-?)]+)-", texte)
        ok_stat = len(s_occ) >= 2 and s_occ[0] == s_src and s_occ[1] == s_src
        verifier("3c. Badge Statut (%s) == source (%s) affichage + href" %
                 (s_occ[0] if s_occ else "?", s_src), ok_stat,
                 "occ=%s source=%s" % (s_occ, s_src))
    except Exception as e:
        verifier("3c. Badge Statut == source statut-projet.txt", False, str(e))

    # 3d. Coherence href des badges statiques (Plateforme, Fait_avec, Langages)
    statiques_ko = []
    for nom in ["Plateforme", "Fait_avec", "Langages"]:
        occ = re.findall(r"badge/" + re.escape(nom) + r"-([^?)]+)-([^?)]+)", texte)
        if len(occ) == 2 and occ[0] != occ[1]:
            statiques_ko.append(nom)
    verifier("3d. Badges statiques coherents (Plateforme, Fait_avec, Langages)",
             len(statiques_ko) == 0, "ko=%s" % statiques_ko)

    # 4. Normes : ASCII strict + LF pur (README + test)
    normes_ko = []
    for f in [README, os.path.abspath(__file__)]:
        try:
            txt = io.open(f, encoding="utf-8", errors="replace").read()
            if any(ord(c) > 127 for c in txt):
                normes_ko.append("%s non-ascii" % os.path.basename(f))
            raw = io.open(f, "rb").read()
            if b"\r\n" in raw:
                normes_ko.append("%s crlf" % os.path.basename(f))
        except Exception as e:
            normes_ko.append("%s ERR %s" % (os.path.basename(f), e))
    verifier("7. Normes ASCII strict + LF pur (README + test)",
             len(normes_ko) == 0, "ko=%s" % normes_ko)

    print()
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
