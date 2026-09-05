#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-034-cerberus-sans-outils-tests.py
GARDE-FOU ANTI-RECURRENCE : la carte de Cerberus n assigne AUCUN outil de test
(lecon 2026-08-13, demande utilisateur).

Contexte (2026-08-13) :
  - L utilisateur a remarque que Cerberus avait lance la non-regression
    complete lui-meme (round performance, 43.8s) alors que ce n est pas son
    role. Diagnostic : la carte de Cerberus est CORRECTE (aucun outil de test
    assigne) mais l execution a derive : Cerberus a utilise
    tester-lancer-non-regression (domaine Morpheus) et a modifie le lanceur
    (domaine Vulcain/Morpheus) hors carte, au lieu de suivre c5/c6 (identifier
    puis activer l agent habilite).
  - Correction : lecon Cerberus enregistree (CERBERUS COORDONNE, IL N EXECUTE
    PAS) + ce garde-fou qui verifie que la carte ne reprend jamais d outil de
    test.

Invariants verifies :
  1. La carte cerberus (arbre-cerberus.json) ne contient AUCUN outil de
     test dans ses indices (ni tester-lancer-non-regression, ni
     tester-protections, ni chrono/reference/temps/mesurer)
  2. La carte contient les cases c5 (Identifier l agent habilite) et c6
     (Activer l agent habilite)
  3. La fiche cerberus.md interdit d executer les tests (mot-cles de la lecon)
  4. Normes : ASCII strict + LF pur (carte + fiche + test)
Tags: agents, cerberus, garde-fou, anti-recurrence
"""
import importlib.util
import io
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

PARCOURS_CERBERUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                 "cerberus", "parcours", "arbre-cerberus.json")
FICHE_CERBERUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                              "cerberus", "cerberus.md")

# Mots d outils de test INTERDITS dans la carte de Cerberus (le gardien ne
# doit JAMAIS executer de tests lui-meme : c est le domaine de Morpheus).
OUTILS_TESTS_INTERDITS = [
    "tester-lancer-non-regression",
    "tester-protections",
    "chrono",
    "reference",
    "mesurer",
    "non-regress",
    "lancer-non-regression",
]

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


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def collecter_texte_json(donnees):
    """Recolte tout le texte d une structure JSON (arbre v2 : branches,
    descriptions, etapes, regles) pour le scan des outils de test interdits."""
    morceaux = []
    if isinstance(donnees, dict):
        for v in donnees.values():
            morceaux.extend(collecter_texte_json(v))
    elif isinstance(donnees, list):
        for v in donnees:
            morceaux.extend(collecter_texte_json(v))
    elif isinstance(donnees, str):
        morceaux.append(donnees)
    return morceaux


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-034 : Cerberus sans outils de test (garde-fou gardien) ===")
    try:
        with io.open(PARCOURS_CERBERUS, encoding="utf-8") as fh:
            parcours = json.load(fh)

        # 1. Aucun outil de test dans TOUTE la structure de la carte v2
        # (arbre + themes + fins : le texte des branches/etapes/regles).
        texte_carte = " ".join(collecter_texte_json(parcours)).lower()
        trouve = []
        for mot in OUTILS_TESTS_INTERDITS:
            if mot.lower() in texte_carte:
                trouve.append(mot)
        verifier("1. Carte Cerberus : AUCUN outil de test dans la structure v2",
                 len(trouve) == 0, "; ".join(trouve[:5]) if trouve else "")

        # 2. La racine v2 contient la branche VERS-ORACLE (Oracle identifie
        # et active l agent habilite - jamais Cerberus directement) : la
        # description de la branche et du theme le materialisent.
        branches = parcours.get("racine", {}).get("branches", [])
        vers_oracle = None
        for b in branches:
            if b.get("reponse") == "VERS-ORACLE":
                vers_oracle = b
        # L'agent habilite est identifie/active par ORACLE (regle D8 + theme
        # vers-oracle) - on verifie la presence du concept dans l arbre.
        def normaliser(t):
            return t.lower().replace("'", " ").replace("\u2019", " ")

        verifier("2a. Branche VERS-ORACLE presente (Oracle identifie l agent habilite)",
                 vers_oracle is not None and "habilite" in normaliser(
                     vers_oracle.get("description", "")),
                 str((vers_oracle or {}).get("description", ""))[:80])
        verifier("2b. Oracle ACTIVE l agent habilite (pas Cerberus)",
                 "lance l agent habilite" in normaliser(
                     vers_oracle.get("description", ""))
                 or "active l agent habilite" in normaliser(
                     vers_oracle.get("description", ""))
                 or "lance l agent habilite" in normaliser(
                     parcours.get("arbre", {}).get("regles", {}).get("D8", "")),
                 "regle D8 ou description VERS-ORACLE")

        # 3. La fiche cerberus interdit d executer les tests (lecon)
        with io.open(FICHE_CERBERUS, encoding="utf-8", errors="replace") as fh:
            fiche = fh.read()
        lecon_ok = ("n execute jamais les tests" in fiche
                    or "N EXECUTE JAMAIS LES TESTS" in fiche
                    or "N EXECUTE PAS" in fiche
                    or "ne doit jamais executer" in fiche
                    or "COORDONNE, IL N EXECUTE PAS" in fiche)
        verifier("3. Fiche Cerberus : lecon interdisant d executer les tests",
                 lecon_ok, "")
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    # 4-5. Normes ASCII strict + LF pur (carte + fiche + test)
    fichiers = [PARCOURS_CERBERUS, FICHE_CERBERUS, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("4. ASCII strict : 0 non-ASCII (carte + fiche + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("5. LF pur : 0 CRLF (carte + fiche + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
