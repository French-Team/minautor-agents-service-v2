#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-041-outils-critiques-anti-residus.py
GARDE-FOU ANTI-RECURRENCE : chaque OUTIL CRITIQUE doit integrer le garde-fou
anti-residus verifier_residus_racine (detection des fichiers nommes comme des
versions semver pures a la racine, ex: 0.2.1, v0.2.6).

Contexte (2026-08-13) :
  - Les residus "0.2.1" / "v0.2.6" a la racine (commit b051714) contenaient la
    sortie d une reactivation - redirections accidentelles de la commande
    d appel vers des fichiers nommes comme des versions du contexte.
  - Le garde-fou verifier_residus_racine (WARNING encadre + regle anti-residu,
    sources de verite de version dans cerveau-projet/agents/clio/) a ete ajoute
    dans activer-agent-principal (v0.5.2) puis etendu a guider-parcours
    (v0.5.1), valider-cartes-decision (v0.4.1) et editer-parcours (v0.1.1).
  - Demande utilisateur : un garde-fou verifie en permanence que TOUT outil
    critique integre verifier_residus_racine - si un nouvel outil critique est
    cree sans le garde-fou, la non-regression le signale immediatement.

REGLE D AJOUT : tout NOUVEL outil critique (modifie des fichiers du cerveau ou
guide les agents) doit etre ajoute a OUTILS_CRITIQUES ci-dessous ET recevoir
verifier_residus_racine (fonction + REGEX_RESIDU + appel dans les actions
reelles).

Invariants verifies (par grep sur chaque .py d outil critique) :
  1. Le fichier .py existe (chemin relatif a TOOLS_DIR)
  2. La fonction def verifier_residus_racine est presente
  3. La constante REGEX_RESIDU est presente
  4. L appel verifier_residus_racine() est present (def + appel = 2 occurrences
     de la chaine, sinon le garde-fou n est pas declenche)
  5. Normes : ASCII strict + LF pur (4 outils + test)
"""
import importlib.util
import io
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

# Liste des OUTILS CRITIQUES (chemins .py relatifs a TOOLS_DIR).
# REGLE : ajouter ici tout nouvel outil critique ET lui ajouter le garde-fou.
OUTILS_CRITIQUES = [
    ("activer-agent-principal", os.path.join("activer", "activer-agent-principal",
                                             "activer-agent-principal.py")),
    ("guider-parcours", os.path.join("guider", "guider-parcours", "guider-parcours.py")),
    ("valider-cartes-decision", os.path.join("valider", "valider-cartes-decision",
                                             "valider-cartes-decision.py")),
    ("editer-parcours", os.path.join("editer", "editer-parcours", "editer-parcours.py")),
]

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


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
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Test formel outils-critiques-anti-residus ===")
    try:
        for nom, rel in OUTILS_CRITIQUES:
            chemin = os.path.join(TOOLS_DIR, rel)
            verifier("1. %s : fichier .py present" % nom,
                     os.path.isfile(chemin), chemin)
            if not os.path.isfile(chemin):
                continue
            code = io.open(chemin, encoding="utf-8", errors="replace").read()
            verifier("2. %s : def verifier_residus_racine presente" % nom,
                     "def verifier_residus_racine" in code)
            verifier("3. %s : REGEX_RESIDU presente" % nom,
                     "REGEX_RESIDU" in code)
            # la def contient "verifier_residus_racine()" ; un appel reel ajoute
            # une 2e occurrence -> au moins 2 = def + appel declenche
            nb_appel = code.count("verifier_residus_racine()")
            verifier("4. %s : appel verifier_residus_racine() present (%d)" % (nom, nb_appel),
                     nb_appel >= 2, "occ=%d (1 = def seule, garde-fou non declenche)" % nb_appel)

        # Normes : ASCII strict + LF pur (les .py des outils critiques + le test)
        fichiers = [os.path.join(TOOLS_DIR, rel) for _, rel in OUTILS_CRITIQUES]
        fichiers.append(os.path.abspath(__file__))
        total_non_ascii = sum(ascii_count(f) for f in fichiers if os.path.isfile(f))
        verifier("5. ASCII strict : 0 non-ASCII (4 outils + test)",
                 total_non_ascii == 0, "total=%d" % total_non_ascii)
        total_crlf = sum(crlf_count(f) for f in fichiers if os.path.isfile(f))
        verifier("6. LF pur : 0 CRLF (4 outils + test)",
                 total_crlf == 0, "total=%d" % total_crlf)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
