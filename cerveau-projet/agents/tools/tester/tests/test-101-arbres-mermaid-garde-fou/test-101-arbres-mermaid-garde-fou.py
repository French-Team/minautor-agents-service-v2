#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-101-arbres-mermaid-garde-fou.py
GARDE-FOU : synchronisation des ARBRES de decision v2 <-> vues Mermaid
(.mmd) ET images SVG (.svg) dans cerveau-projet/cartes-vues/arbres/.
Verifie que chaque arbre-<agent>.json de la v2 (freelance/<agent>/parcours/,
structure RACINE/BRANCHES vs les cartes v1) a ses fichiers .mmd et .svg
generes, qu ils sont synchronises avec l arbre (outil convertir-carte-mermaid
--arbres --verifier, rendu DETERMINISTE octet a octet), que les .svg sont des
XML bien formes, et que l index existe.

Contexte (2026-08-24, demande utilisateur) : les agents de la v2 ont un ARBRE
de decision (arbre-<agent>.json : racine -> branches vers theme-*.json ->
fins.json centralise) et PAS une simple carte de decision (parcours-<agent>.json
avec cases) comme la v1. Atlas doit pouvoir disposer d un dossier de vues pour
les agents v2. Extension de l outil convertir-carte-mermaid (Vulcain) :
mode --arbres qui genere les .mmd + .svg + index.md dans
cerveau-projet/cartes-vues/arbres/. Le rendu SVG est Python pur et
deterministe : ce test verrouille la synchronisation octet a octet, tout
arbre modifie sans regenerer ses vues est signale.

Invariants verifies :
  1. Chaque arbre-<agent>.json (9 agents v2) a son .mmd ET son .svg.
  2. verifier_arbres retourne rc=0 (9 arbres synchronises .mmd + .svg).
  3. La validation syntaxe mermaid integree ne signale rien (9 arbres).
  4. index.md existe et reference les 9 agents (.mmd et .svg).
  5. .mmd + .svg + index.md : ASCII strict + LF pur.
  6. Chaque .svg est un document XML bien forme (xml.dom.minidom).
  7. Determinisme : regenerer chaque .svg depuis l arbre donne exactement
     les memes octets (9/9).
  8. Preuve negative : une desynchronisation du .mmd d un arbre est detectee
     (verifier_arbres rc=1).
  9. Preuve negative : une desynchronisation du .svg d un arbre est detectee
     (verifier_arbres rc=1).

Tags: parcours, arbres-v2, outil, garde-fou, preuve-negative
"""
import importlib.util
import glob
import io
import json
import os
import sys
import time
import xml.dom.minidom

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

CONVERTIR_PY = os.path.join(TOOLS_DIR, "consulter", "convertir-carte-mermaid",
                            "convertir-carte-mermaid.py")
ARBRES_VUES = os.path.join(CERVEau, "cartes-vues", "arbres")
INDEX_MD = os.path.join(ARBRES_VUES, "index.md")

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


def run(cmd, timeout=120):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lister_arbres_fichiers():
    return sorted(glob.glob(os.path.join(CERVEau, "freelance", "*", "parcours",
                                         "arbre-*.json")))


def agents_arbres():
    """agent -> chemin arbre (nom du dossier parent du parcours)."""
    resultat = {}
    for p in lister_arbres_fichiers():
        try:
            with io.open(p, encoding="utf-8") as fh:
                d = json.load(fh)
        except (ValueError, IOError):
            continue
        agent = os.path.basename(os.path.dirname(os.path.dirname(p)))
        resultat[agent] = p
    return resultat


def charger_convertir():
    spec = importlib.util.spec_from_file_location("convertir_carte_mermaid",
                                                  CONVERTIR_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    t0 = time.monotonic()
    print("=== test-101 : synchronisation arbres v2 <-> vues mermaid "
          "(.mmd + .svg) ===")

    # 1. L outil existe ; chaque arbre v2 a son .mmd ET son .svg
    t_debut = time.monotonic()
    if not os.path.isfile(CONVERTIR_PY):
        verifier("1. outil convertir-carte-mermaid existe", False, CONVERTIR_PY)
        print("=== RESULTAT : %d OK / %d KO ====" % (NB_OK, NB_KO))
        return 1 if NB_KO else 0
    agents = agents_arbres()
    manquants_mmd = []
    manquants_svg = []
    for agent in sorted(agents.keys()):
        if not os.path.isfile(os.path.join(ARBRES_VUES, agent + ".mmd")):
            manquants_mmd.append(agent)
        if not os.path.isfile(os.path.join(ARBRES_VUES, agent + ".svg")):
            manquants_svg.append(agent)
    verifier("1. chaque arbre v2 a son .mmd (%d agents)" % len(agents),
             not manquants_mmd, "manquants=%s" % manquants_mmd[:5])
    verifier("1b. chaque arbre v2 a son .svg (%d agents)" % len(agents),
             not manquants_svg, "manquants=%s" % manquants_svg[:5])
    chrono_etape("1. .mmd + .svg presents", t_debut)

    # 2. verifier_arbres retourne rc=0 (synchronisation .mmd ET .svg)
    t_debut = time.monotonic()
    mod = charger_convertir()
    try:
        rc_arbres = mod.verifier_arbres(PROJECT_ROOT, ARBRES_VUES)
    except Exception as e:
        rc_arbres = 1
        print("  [ERREUR] verifier_arbres : %s" % e)
    verifier("2. verifier_arbres : %d arbres synchronises (.mmd + .svg, rc=0)"
             % len(agents), rc_arbres == 0, "rc=%d" % rc_arbres)
    chrono_etape("2. verifier_arbres", t_debut)

    # 3. La validation syntaxe integree ne signale rien sur les 9 .mmd arbres
    t_debut = time.monotonic()
    erreurs_syntaxe = []
    for agent, chemin_arbre in sorted(agents.items()):
        try:
            texte, _ = mod.convertir_arbre(chemin_arbre)
            errs = mod.verifier_syntaxe(texte, dict((i, {}) for i in mod.ids_arbre(texte)))
            if errs:
                erreurs_syntaxe.append("%s: %s" % (agent, errs[0]))
        except Exception as e:
            erreurs_syntaxe.append("%s: %s" % (agent, e))
    verifier("3. validation syntaxe integree : 0 ligne non conforme (%d arbres)"
             % len(agents), not erreurs_syntaxe,
             "erreurs=%s" % erreurs_syntaxe[:5])
    chrono_etape("3. syntaxe mermaid", t_debut)

    # 4. index.md existe et reference les 9 agents (.mmd ET .svg)
    t_debut = time.monotonic()
    if not os.path.isfile(INDEX_MD):
        verifier("4. index.md present + reference les %d agents (.mmd + .svg)"
                 % len(agents), False, "index.md absent")
    else:
        with io.open(INDEX_MD, encoding="utf-8") as fh:
            contenu = fh.read()
        absents = [a for a in sorted(agents.keys())
                   if ("| %s |" % a) not in contenu]
        sans_svg = [a for a in sorted(agents.keys())
                    if (a + ".svg") not in contenu]
        verifier("4. index.md present + reference les %d agents (.mmd + .svg)"
                 % len(agents), not absents and not sans_svg,
                 "absents=%s sans_svg=%s" % (absents[:5], sans_svg[:5]))
    chrono_etape("4. index.md", t_debut)

    # 5. ASCII strict + LF pur sur tous les .mmd + .svg + index.md
    t_debut = time.monotonic()
    fichiers = (sorted(glob.glob(os.path.join(ARBRES_VUES, "*.mmd")))
                + sorted(glob.glob(os.path.join(ARBRES_VUES, "*.svg")))
                + [INDEX_MD])
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("5. ASCII strict : 0 non-ASCII sur %d fichiers generes"
             % len(fichiers), total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("5b. LF pur : 0 CRLF sur les fichiers generes",
             total_crlf == 0, "total=%d" % total_crlf)
    chrono_etape("5. normes ASCII/LF", t_debut)

    # 6. Chaque .svg est un XML bien forme
    t_debut = time.monotonic()
    xml_ko = []
    for agent in sorted(agents.keys()):
        chemin = os.path.join(ARBRES_VUES, agent + ".svg")
        try:
            with io.open(chemin, encoding="ascii") as fh:
                xml.dom.minidom.parseString(fh.read())
        except Exception as e:
            xml_ko.append("%s: %s" % (agent, e))
    verifier("6. les %d .svg sont des XML bien formes" % len(agents),
             not xml_ko, "ko=%s" % xml_ko[:3])
    chrono_etape("6. XML bien forme", t_debut)

    # 7. Determinisme : regenerer chaque .svg donne exactement les memes octets
    t_debut = time.monotonic()
    diff = []
    for agent, chemin_arbre in sorted(agents.items()):
        try:
            with io.open(chemin_arbre, encoding="utf-8") as fh:
                donnees = json.load(fh)
            texte, _ = mod.convertir_arbre(chemin_arbre)
            version = (donnees.get("arbre", {}).get("version")
                       or donnees.get("identite", {}).get("version", "?"))
            svg = mod.rendre_svg(texte, agent, version)
            with io.open(os.path.join(ARBRES_VUES, agent + ".svg"),
                         encoding="ascii") as fh:
                existant = fh.read()
            if existant != svg:
                diff.append(agent)
        except Exception as e:
            diff.append("%s: %s" % (agent, e))
    verifier("7. determinisme : %d .svg regeneres octet a octet" % len(agents),
             not diff, "diff=%s" % diff[:5])
    chrono_etape("7. determinisme .svg", t_debut)

    # 8. Preuve negative : une desynchronisation du .mmd d un arbre est detectee
    t_debut = time.monotonic()
    cible = os.path.join(ARBRES_VUES, sorted(agents.keys())[0] + ".mmd")
    original = ""
    try:
        with io.open(cible, encoding="ascii") as fh:
            original = fh.read()
    except IOError:
        original = ""
    preuve_mmd = False
    if original:
        modifie = original.replace(" --> ", " --> X-", 1)
        if modifie != original:
            try:
                with io.open(cible, "w", encoding="ascii", newline="\n") as fh:
                    fh.write(modifie)
                rc2 = mod.verifier_arbres(PROJECT_ROOT, ARBRES_VUES)
                preuve_mmd = (rc2 == 1)
            finally:
                with io.open(cible, "w", encoding="ascii", newline="\n") as fh:
                    fh.write(original)
    verifier("8. preuve negative .mmd : desynchronisation detectee (rc=1)",
             preuve_mmd, "desynchronisation .mmd non detectee")
    chrono_etape("8. preuve negative .mmd", t_debut)

    # 9. Preuve negative : une desynchronisation du .svg d un arbre est detectee
    t_debut = time.monotonic()
    cible_svg = os.path.join(ARBRES_VUES, sorted(agents.keys())[0] + ".svg")
    original_svg = ""
    try:
        with io.open(cible_svg, encoding="ascii") as fh:
            original_svg = fh.read()
    except IOError:
        original_svg = ""
    preuve_svg = False
    if original_svg:
        modifie_svg = original_svg.replace("#64748b", "#ff0000", 1)
        if modifie_svg != original_svg:
            try:
                with io.open(cible_svg, "w", encoding="ascii",
                             newline="\n") as fh:
                    fh.write(modifie_svg)
                rc3 = mod.verifier_arbres(PROJECT_ROOT, ARBRES_VUES)
                preuve_svg = (rc3 == 1)
            finally:
                with io.open(cible_svg, "w", encoding="ascii",
                             newline="\n") as fh:
                    fh.write(original_svg)
    verifier("9. preuve negative .svg : desynchronisation detectee (rc=1)",
             preuve_svg, "desynchronisation .svg non detectee")
    chrono_etape("9. preuve negative .svg", t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
