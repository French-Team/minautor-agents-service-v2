#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-072-c0-c0b-relecture.py
GARDE-FOU : chaque parcours (carte de decision) doit porter le mecanisme
de relecture obligatoire de la fiche avant mission : la case c0 (question
honnete) et la case c0b (RELIRE OBLIGATOIRE corrections puis fiche).

Contexte (mission 2026-08-16) :
  - La regle "RELIRE SA FICHE AVANT MISSION (IMMUABLE)" a ete gravee dans
    regles-groupes-agents.md (zone du marbre) apres des derives ou un agent
    agissait sans avoir relu SA fiche + SES corrections.
  - Le mecanisme vit dans les PARCOURS : c0 pose la question honnete
    (OUI -> c0c, INCERTAIN/NON -> c0b) et c0b ordonne la relecture
    (corrections puis fiche) via les outils lire-fichier.
  - Un scan prealable a revele que argus et gardien avaient c0b sans outil
    de lecture : Buffy les a corriges (argus v0.1.9, gardien v0.1.2).
    Ce test verrouille l etat pour les 15 parcours.

Invariants verifies :
  1. Chaque parcours a une case c0 de type 'question' dont la question
     contient 'EN MEMOIRE ta fiche et tes corrections'.
  2. c0 a les branches OUI -> c0c, INCERTAIN -> c0b, NON -> c0b.
  3. Chaque parcours a une case c0b de type 'action' dont le titre
     contient 'RELIRE' et dont suivant = c0c.
  4. c0b contient au moins 2 indices outil 'lire-fichier' (le premier vers
     corrections.md, le second vers <agent>.md).
  5. Preuve negative : une copie sans c0b (ou sans outil lire-fichier)
     est DETECTEE par le scan interne, puis SUPPRIMEE (0 trace).
  6. Normes : ASCII strict + LF pur (test + parcours).
"""

import glob
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PARCOURS_GLOB = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "*",
                             "parcours", "parcours-*.json")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 10


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-072 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, str(detail)[-100:]))


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def charger_parcours(f):
    """Charge un parcours JSON + nom de l agent."""
    p = json.load(io.open(f, encoding="utf-8"))
    parts = f.replace(os.sep, "/").split("/")
    agent = parts[-1].replace("parcours-", "").replace(".json", "")
    return agent, p


def analyser_parcours(agent, p):
    """Analyse un parcours : retourne la liste des problemes c0/c0b.

    Retourne une liste de tuples (type, detail) :
      - C0_ABSENT : aucune case c0
      - C0_MAUVAIS_TYPE : c0 n est pas de type question
      - C0_QUESTION : la question ne contient pas le motif attendu
      - C0_BRANCHES : branches OUI/INCERTAIN/NON absentes ou mal dirigees
      - C0B_ABSENT : aucune case c0b
      - C0B_MAUVAIS_TYPE : c0b n est pas de type action
      - C0B_TITRE : le titre ne contient pas RELIRE
      - C0B_SUIVANT : suivant != c0c
      - C0B_OUTILS : moins de 2 outils lire-fichier (ou mauvaises cibles)
    """
    problemes = []
    cases = p.get("cases", {})
    c0 = cases.get("c0")
    c0b = cases.get("c0b")

    # --- c0 ---
    if not isinstance(c0, dict):
        problemes.append(("C0_ABSENT", "%s : c0 absent" % agent))
    else:
        if c0.get("type") != "question":
            problemes.append(("C0_MAUVAIS_TYPE",
                              "%s : c0 type=%s (attendu question)" %
                              (agent, c0.get("type"))))
        question = c0.get("question", "")
        if "EN MEMOIRE ta fiche et tes corrections" not in question:
            problemes.append(("C0_QUESTION",
                              "%s : question sans le motif relecture" % agent))
        branches = c0.get("branches", [])
        vers_oui = [b.get("vers") for b in branches if b.get("reponse") == "OUI"]
        vers_inc = [b.get("vers") for b in branches if b.get("reponse") == "INCERTAIN"]
        vers_non = [b.get("vers") for b in branches if b.get("reponse") == "NON"]
        if vers_oui != ["c0c"] or vers_inc != ["c0b"] or vers_non != ["c0b"]:
            problemes.append(("C0_BRANCHES",
                              "%s : branches OUI=%s INCERTAIN=%s NON=%s "
                              "(attendu c0c/c0b/c0b)" %
                              (agent, vers_oui, vers_inc, vers_non)))

    # --- c0b ---
    if not isinstance(c0b, dict):
        problemes.append(("C0B_ABSENT", "%s : c0b absent" % agent))
    else:
        if c0b.get("type") != "action":
            problemes.append(("C0B_MAUVAIS_TYPE",
                              "%s : c0b type=%s (attendu action)" %
                              (agent, c0b.get("type"))))
        titre = c0b.get("titre", "")
        if "RELIRE" not in titre.upper():
            problemes.append(("C0B_TITRE",
                              "%s : c0b titre sans RELIRE : %s" % (agent, titre)))
        if c0b.get("suivant") != "c0c":
            problemes.append(("C0B_SUIVANT",
                              "%s : c0b suivant=%s (attendu c0c)" %
                              (agent, c0b.get("suivant"))))
        outils = [i for i in c0b.get("indices", [])
                  if i.get("type") == "outil" and i.get("nom") == "lire-fichier"]
        cibles = [i.get("commande", "") for i in outils]
        nb_corr = sum(1 for c in cibles if "corrections.md" in c)
        nb_fiche = sum(1 for c in cibles if ("%s.md" % agent) in c)
        if len(outils) < 2 or nb_corr < 1 or nb_fiche < 1:
            problemes.append(("C0B_OUTILS",
                              "%s : c0b outils lire-fichier=%d "
                              "(corrections=%d, fiche=%d) - attendu 2 (1+1)" %
                              (agent, len(outils), nb_corr, nb_fiche)))

    return problemes


def scanner_tous_les_parcours(racine_parcours):
    """Scanne tous les parcours et retourne la liste des problemes."""
    problemes = []
    for f in sorted(glob.glob(racine_parcours)):
        try:
            agent, p = charger_parcours(f)
        except Exception as e:
            problemes.append(("JSON_INVALIDE", "%s : %s" % (f, str(e)[-60:])))
            continue
        problemes.extend(analyser_parcours(agent, p))
    return problemes


def main():
    print("=== Garde-fou : c0/c0b relecture obligatoire sur tous les parcours ===")

    # 1. Scan : chaque parcours a c0 (question honnete)
    t0 = time.monotonic()
    problemes = scanner_tous_les_parcours(PARCOURS_GLOB)
    c0_manquants = [p for p in problemes if p[0] == "C0_ABSENT"]
    verifier("1. 15 parcours : c0 present", len(c0_manquants) == 0,
             c0_manquants[:3] if c0_manquants else "")
    chrono_etape("1. scan c0 present", t0)

    # 2. c0 type question + question honnete
    t0 = time.monotonic()
    c0_types = [p for p in problemes if p[0] in ("C0_MAUVAIS_TYPE", "C0_QUESTION")]
    verifier("2. c0 : type question + motif 'EN MEMOIRE ta fiche...'",
             len(c0_types) == 0, c0_types[:3] if c0_types else "")
    chrono_etape("2. scan c0 question", t0)

    # 3. c0 branches OUI->c0c, INCERTAIN->c0b, NON->c0b
    t0 = time.monotonic()
    c0_branches = [p for p in problemes if p[0] == "C0_BRANCHES"]
    verifier("3. c0 : branches OUI->c0c / INCERTAIN->c0b / NON->c0b",
             len(c0_branches) == 0, c0_branches[:3] if c0_branches else "")
    chrono_etape("3. scan c0 branches", t0)

    # 4. c0b present, action, titre RELIRE
    t0 = time.monotonic()
    c0b_manquants = [p for p in problemes
                     if p[0] in ("C0B_ABSENT", "C0B_MAUVAIS_TYPE", "C0B_TITRE")]
    verifier("4. c0b : present, type action, titre RELIRE",
             len(c0b_manquants) == 0, c0b_manquants[:3] if c0b_manquants else "")
    chrono_etape("4. scan c0b present", t0)

    # 5. c0b suivant = c0c
    t0 = time.monotonic()
    c0b_suiv = [p for p in problemes if p[0] == "C0B_SUIVANT"]
    verifier("5. c0b : suivant = c0c", len(c0b_suiv) == 0,
             c0b_suiv[:3] if c0b_suiv else "")
    chrono_etape("5. scan c0b suivant", t0)

    # 6. c0b outils lire-fichier (corrections puis fiche)
    t0 = time.monotonic()
    c0b_outils = [p for p in problemes if p[0] == "C0B_OUTILS"]
    verifier("6. c0b : 2 outils lire-fichier (corrections puis fiche)",
             len(c0b_outils) == 0, c0b_outils[:3] if c0b_outils else "")
    chrono_etape("6. scan c0b outils", t0)

    # 7. Preuve negative : copie sans c0b detectee puis supprimee
    t0 = time.monotonic()
    tmp = tempfile.mkdtemp(prefix="tmp-test072-")
    try:
        src = None
        for f in glob.glob(PARCOURS_GLOB):
            if "parcours-buffy.json" in f:
                src = json.load(io.open(f, encoding="utf-8"))
                break
        if src is None:
            verifier("7. preuve negative : copie trouvee", False,
                     "parcours buffy introuvable")
        else:
            # copie sans c0b : on retire la case c0b et l indice outil de c0
            src2 = json.loads(json.dumps(src))
            src2["cases"].pop("c0b", None)
            sous = os.path.join(tmp, "parcours-buffy.json")
            with io.open(sous, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(src2, fh, ensure_ascii=True, indent=1)
            # copie sans outil lire-fichier dans c0b
            src3 = json.loads(json.dumps(src))
            src3["cases"]["c0b"]["indices"] = [
                {"type": "regle", "texte": "ACTION OBLIGATOIRE"}]
            sous3 = os.path.join(tmp, "parcours-clio.json")
            with io.open(sous3, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(src3, fh, ensure_ascii=True, indent=1)
            # scanner les copies avec le meme analyseur
            pb2 = analyser_parcours("buffy", json.load(io.open(sous, encoding="utf-8")))
            pb3 = analyser_parcours("clio", json.load(io.open(sous3, encoding="utf-8")))
            detecte = any(x[0] == "C0B_ABSENT" for x in pb2) and \
                any(x[0] == "C0B_OUTILS" for x in pb3)
            verifier("7. preuve negative : c0b absent + outils manquants DETECTES",
                     detecte, "non detecte: %s / %s" % (pb2[:2], pb3[:2]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        verifier("7b. preuve negative : copies SUPPRIMEES (0 trace)",
                 not os.path.exists(tmp), "copies encore presentes")
    chrono_etape("7. preuve negative", t0)

    # 8. Normes ASCII + LF (test + parcours)
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    fichiers = [os.path.abspath(__file__)]
    fichiers.extend(sorted(glob.glob(PARCOURS_GLOB)))
    for f in fichiers:
        try:
            d = io.open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        na_total += sum(1 for ch in d if ord(ch) > 127)
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("8. normes : 0 non-ASCII (test + parcours)",
             na_total == 0, "non-ascii=%d" % na_total)
    verifier("8b. normes : 0 CRLF (test + parcours)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("8. normes", t0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" %
          (NB_OK, NB_KO, NB_POINTS))
    bilan_chrono()
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
