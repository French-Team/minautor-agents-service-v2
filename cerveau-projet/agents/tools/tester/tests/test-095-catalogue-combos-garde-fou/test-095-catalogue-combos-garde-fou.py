#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-095-catalogue-combos-garde-fou.py
GARDE-FOU : synchronisation combo -> outils. Verifie la coherence
bidirectionnelle entre la source de verite (catalogue-combos.json) et les
declarations inverses (champ 'combos:' du frontmatter des fiches outils).

Contexte (2026-08-19, demande utilisateur "les outils manquent d une option
qui signale s ils font partie d un combo") : les combos savaient quels outils
ils appelaient (definition-combo.json + scripts) mais les outils ne
declaraient pas leur appartenance - impossible de repondre "ou est utilise
cet outil et par qui". Correctif Vulcain : catalogue-combos.json (21 combos
-> proprietaire + membres), champ 'combos:' dans 40 fiches outils membres,
outil consulter-combos. Ce test verrouille la synchronisation.

Invariants verifies :
  1. Le catalogue existe, JSON valide, version 0.1.0.
  2. Chaque combo du catalogue a une fiche outil existante.
  3. Chaque membre declare au catalogue a le champ 'combos' dans sa fiche.
  4. Reciproquement : chaque fiche avec champ 'combos' est declaree membre
     dans le catalogue (pas de declaration orpheline).
  5. L outil consulter-combos repond : --outil evaluer-coherence affiche
     combos-audit-general (proprietaire themis).
  6. Normes : ASCII strict + LF pur (catalogue + outil + test).

Tags: outils, combos, catalogue, garde-fou, preuve-negative
"""
import importlib.util
import io
import json
import os
import re
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

CATALOGUE_COMBOS = os.path.join(TOOLS_DIR, "combos", "catalogue-combos.json")
CONSULTER_COMBOS_PY = os.path.join(TOOLS_DIR, "consulter",
                                   "consulter-combos", "consulter-combos.py")

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


def lire_frontmatter(chemin):
    """Retourne le bloc frontmatter (entre --- et ---) ou None."""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        t = fh.read()
    m = re.search(r"^---\n(.*?)\n---", t, re.DOTALL)
    return m.group(1) if m else None


def champ_combos(frontmatter):
    """Extrait la liste des combos du champ 'combos:' du frontmatter."""
    m = re.search(r"^  combos:\n((?:    - [a-z0-9-]+\n?)+)", frontmatter,
                  re.MULTILINE)
    if not m:
        return []
    return re.findall(r"    - ([a-z0-9-]+)", m.group(1))


def main():
    t0 = time.monotonic()
    print("=== test-095 : synchronisation catalogue-combos <-> fiches outils ===")

    # 1. Le catalogue existe et est un JSON valide, version 0.1.0
    t_debut = time.monotonic()
    if not os.path.isfile(CATALOGUE_COMBOS):
        verifier("1. catalogue-combos.json existe", False, CATALOGUE_COMBOS)
        chrono_etape("1. catalogue existe", t_debut)
        print("=== RESULTAT : %d OK / %d KO ===" % (NB_OK, NB_KO))
        return 1 if NB_KO else 0
    try:
        with io.open(CATALOGUE_COMBOS, encoding="utf-8") as fh:
            catalogue = json.load(fh)
        version_ok = catalogue.get("version") == "0.1.0"
        combos = catalogue.get("combos", [])
        verifier("1. catalogue-combos.json : JSON valide + version 0.1.0 + 21 combos",
                 version_ok and len(combos) >= 20,
                 "version=%s combos=%d" % (catalogue.get("version"), len(combos)))
    except (ValueError, IOError) as e:
        verifier("1. catalogue-combos.json : JSON valide + version 0.1.0",
                 False, str(e))
        combos = []
    chrono_etape("1. catalogue JSON", t_debut)

    # 2. Chaque combo a un fichier de definition : fiche .md (combos
    #    scriptes) OU definition-combo.json (combos declaratifs executes
    #    par combos-moteur). Convention 2026-08-19 : les combos declaratifs
    #    n ont pas de fiche .md, seule leur definition JSON existe.
    t_debut = time.monotonic()
    sans_fichier = []
    for combo in combos:
        nom = combo.get("nom", "")
        dossier = os.path.join(TOOLS_DIR, "combos", nom)
        fiche_md = os.path.join(dossier, "%s.md" % nom)
        definition = os.path.join(dossier, "definition-combo.json")
        if not os.path.isfile(fiche_md) and not os.path.isfile(definition):
            sans_fichier.append(nom)
    verifier("2. chaque combo a une fiche .md ou une definition-combo.json (%d combos)"
             % len(combos),
             not sans_fichier, "manquants=%s" % sans_fichier)
    chrono_etape("2. fiches combos", t_debut)

    # 3. Chaque membre declare au catalogue est un OUTIL REEL (fiche .md)
    #    ou une COMMANDE du catalogue-commandes (generateur). Un membre
    #    inconnu (ni fiche ni commande) est une declaration fantome a
    #    signaler (preuve negative 2026-08-19).
    t_debut = time.monotonic()
    fiche_par_nom = {}
    for base, dossiers, fichiers in os.walk(TOOLS_DIR):
        for nom_f in fichiers:
            if nom_f.endswith(".md"):
                nom_outil = nom_f[:-3]
                fiche_par_nom.setdefault(nom_outil,
                                         os.path.join(base, nom_f))
    # commandes du generateur (source de verite des commandes composees)
    commandes_generateur = set()
    catalogue_cmd = os.path.join(TOOLS_DIR, "generateurs",
                                 "generateurs-commande",
                                 "catalogue-commandes.json")
    try:
        with io.open(catalogue_cmd, encoding="utf-8") as fh:
            commandes_generateur = {c.get("nom") for c in
                                    json.load(fh).get("commandes", [])}
    except (ValueError, IOError):
        pass
    non_declares = []
    fantomes = []
    total_membres = 0
    for combo in combos:
        for membre in combo.get("membres", []):
            total_membres += 1
            fiche = fiche_par_nom.get(membre)
            if not fiche:
                # membre sans fiche : doit au moins etre une commande
                # generateur connue (ex: corriger-accents), sinon fantome
                if membre not in commandes_generateur:
                    fantomes.append("%s (combo %s)" % (membre,
                                                        combo.get("nom")))
                continue
            fm = lire_frontmatter(fiche)
            if fm is None:
                non_declares.append(membre + " (pas de frontmatter)")
                continue
            combos_declares = champ_combos(fm)
            if combo.get("nom") not in combos_declares:
                non_declares.append("%s -> fiche sans %s" % (membre,
                                                             combo.get("nom")))
    verifier("3. chaque membre du catalogue est un outil reel ou une commande (%d membres)"
             % total_membres,
             not fantomes, "fantomes=%s" % fantomes[:5])
    verifier("3b. chaque membre reel a le champ combos dans sa fiche",
             not non_declares, "manquants=%s" % non_declares[:5])
    chrono_etape("3. champ combos des fiches", t_debut)

    # 4. Reciproque : aucune declaration 'combos' orpheline (fiche declare
    #    un combo absent du catalogue ou non membre)
    t_debut = time.monotonic()
    membre_par_combo = {}
    for combo in combos:
        membre_par_combo[combo.get("nom", "")] = set(combo.get("membres", []))
    orphelines = []
    for nom_outil, fiche in fiche_par_nom.items():
        fm = lire_frontmatter(fiche)
        if fm is None:
            continue
        for combo_declare in champ_combos(fm):
            if combo_declare not in membre_par_combo:
                orphelines.append("%s -> %s (combo inconnu)"
                                  % (nom_outil, combo_declare))
            elif nom_outil not in membre_par_combo[combo_declare]:
                orphelines.append("%s -> %s (non membre)"
                                  % (nom_outil, combo_declare))
    verifier("4. aucune declaration combos orpheline (bidirectionnel)",
             not orphelines, "orphelines=%s" % orphelines[:5])
    chrono_etape("4. declarations orphelines", t_debut)

    # 5. L outil consulter-combos repond (preuve positive)
    t_debut = time.monotonic()
    if not os.path.isfile(CONSULTER_COMBOS_PY):
        verifier("5. consulter-combos : outil present + reponse correcte",
                 False, "outil absent")
    else:
        # --agent themis : sans agent, l outil journalise agent=inconnu et
        # pollue le registre (test-079 KO). Themis est le proprietaire du
        # combo audite (combos-audit-general).
        r = run([PYTHON, CONSULTER_COMBOS_PY, "--outil", "evaluer-coherence",
                 "--agent", "themis"])
        ok_outil = ("combos-audit-general" in r.stdout
                    and "proprietaire : themis" in r.stdout)
        verifier("5. consulter-combos --outil evaluer-coherence : reponse correcte",
                 ok_outil, "rc=%d out=%s" % (r.returncode, r.stdout[-80:]))
    chrono_etape("5. outil consulter-combos", t_debut)

    # 6. Normes ASCII strict + LF pur
    t_debut = time.monotonic()
    fichiers = [CATALOGUE_COMBOS, CONSULTER_COMBOS_PY,
                os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("6. ASCII strict : 0 non-ASCII (catalogue + outil + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("6b. LF pur : 0 CRLF (catalogue + outil + test)",
             total_crlf == 0, "total=%d" % total_crlf)
    chrono_etape("6. normes ASCII/LF", t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
