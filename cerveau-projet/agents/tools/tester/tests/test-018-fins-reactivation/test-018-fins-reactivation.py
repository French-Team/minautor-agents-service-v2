#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-018-fins-reactivation.py
Test formel des fins REACTIVER-CERBERUS precisees dans les 11 parcours.

Contexte (missions 2026-08-10) :
  - La mission Buffy a precise la condition 'activation directe par Cerberus'
    sur les fins REACTIVER-CERBERUS de 4 parcours (atlas c11, clio c12,
    minerve c10, themis c13) ; morpheus c14 porte '(activation directe)'.
  - janus c10 est le DERNIER MAILLON de la chaine (bilan consolide) : il ne
    porte pas la condition 'activation directe' mais le bilan consolide.
  - Le piege 'reactiver' a ete corrige : la commande reactiver ramene TOUJOURS
    a Cerberus. Aucune fin 'Activer l agent precedent' ne doit contenir la
    commande reactiver.

Regle verifiee (Pattern 13 de la spec-guider-parcours) :
  Toute fin REACTIVER-CERBERUS porte la condition (activation directe) SAUF
  le dernier maillon de chaine (bilan consolide).

Cas couverts:
  1. Chaque parcours des 11 agents contient au plus une fin REACTIVER-CERBERUS
  2. Toute fin REACTIVER-CERBERUS porte 'activation directe' dans son message
     OU est le dernier maillon (bilan consolide) : regle Pattern 13
  3. Les 4 fins precisees (atlas c11, clio c12, minerve c10, themis c13)
     portent EXACTEMENT 'activation directe par Cerberus'
  4. Navigation reelle vers les 4 fins precisees (guider-parcours --case) :
     la sortie affiche 'activation directe par Cerberus' + PARCOURS TERMINE
  5. Anti-regression : aucune fin 'Activer l agent precedent' ne contient
     la commande reactiver (le piege corrige reste elimine)
  6. ASCII strict : 0 non-ASCII (test + 11 parcours)
  7. LF pur : 0 CRLF (test + 11 parcours)

Usage:
  python3 test-018-fins-reactivation.py
"""
import io
import glob
import json
import os
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

GUIDER = os.path.join(TOOLS_DIR, "guider", "guider-parcours", "guider-parcours.py")
PARCOURS_GLOB = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                             "*", "parcours", "parcours-*.json")

# Fins precisees par la mission Buffy : condition exacte attendue
FINS_PRECISEES = {
    "atlas": "c11",
    "clio": "c12",
    "minerve": "c10",
    "themis": "c13",
}
# Dernier maillon de chaine (bilan consolide, sans condition activation directe)
DERNIER_MAILLON = {"janus": "c10"}

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


def run(cmd, timeout=60):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def charger_parcours(chemin):
    with io.open(chemin, encoding="utf-8", newline="") as fh:
        return json.load(fh)


def agent_de_parcours(chemin):
    base = os.path.basename(chemin)  # parcours-<agent>.json
    return base.replace("parcours-", "").replace(".json", "")


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO

    parcours_liste = sorted(glob.glob(PARCOURS_GLOB))
    verifier("0. 11 parcours trouves",
             len(parcours_liste) == 11, str(len(parcours_liste)))

    print("=== Test formel fins reactivation (11 parcours) ===")

    # --- Passe 1 : analyse statique des fins REACTIVER-CERBERUS ---
    fins_reactiver = {}  # agent -> (case_id, titre, message)
    fins_par_agent = {}  # agent -> [cases] (detection des doublons)
    for chemin in parcours_liste:
        agent = agent_de_parcours(chemin)
        d = charger_parcours(chemin)
        for k, c in d.get("cases", {}).items():
            if c.get("type") != "fin":
                continue
            titre = c.get("titre", "")
            msg = c.get("message", "")
            if "reactiver cerberus" in titre.lower():
                fins_par_agent.setdefault(agent, []).append(k)
                fins_reactiver[agent] = (k, titre, msg)

    # 1. Aucun parcours n'a plus d'une fin REACTIVER-CERBERUS (le controleur
    #    de la chaine est unique : reactiver ne ramene qu'a Cerberus)
    doubles = ["%s:%s" % (a, ",".join(v)) for a, v in sorted(fins_par_agent.items()) if len(v) > 1]
    verifier("1. Au plus une fin REACTIVER-CERBERUS par parcours",
             not doubles, "; ".join(doubles))
    verifier("1b. Les 6 fins REACTIVER identifiees (atlas, clio, janus, minerve, morpheus, themis)",
             len(fins_reactiver) == 6, "agents=%s" % sorted(fins_reactiver))

    # 2. Regle Pattern 13 : condition activation directe OU dernier maillon
    sans_condition = []
    for agent, (k, titre, msg) in sorted(fins_reactiver.items()):
        if "activation directe" in msg.lower():
            continue
        if agent in DERNIER_MAILLON and "bilan consolide" in msg.lower():
            continue
        sans_condition.append("%s %s" % (agent, k))
    verifier("2. Toute fin REACTIVER-CERBERUS: condition OU dernier maillon (Pattern 13)",
             not sans_condition, "; ".join(sans_condition))

    # 3. Les 4 fins precisees portent EXACTEMENT la condition complete
    ko_precises = []
    for agent, k in sorted(FINS_PRECISEES.items()):
        if agent not in fins_reactiver:
            ko_precises.append("%s: aucune fin reactiver" % agent)
            continue
        k2, titre, msg = fins_reactiver[agent]
        if k2 != k:
            ko_precises.append("%s: case %s != %s" % (agent, k2, k))
            continue
        if "activation directe par Cerberus" not in msg:
            ko_precises.append("%s %s: condition incomplete" % (agent, k))
    verifier("3. 4 fins precisees portent 'activation directe par Cerberus'",
             not ko_precises, "; ".join(ko_precises))

    # --- Passe 2 : navigation reelle vers les 4 fins precisees ---
    nav_ok = 0
    nav_ko = []
    for agent, k in sorted(FINS_PRECISEES.items()):
        chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", agent,
                              "parcours", "parcours-%s.json" % agent)
        r = run([PYTHON, GUIDER, chemin, "--case", k])
        if (r.returncode == 0 and "PARCOURS TERMINE" in r.stdout
                and "activation directe par Cerberus" in r.stdout):
            nav_ok += 1
        else:
            nav_ko.append("%s %s (code=%d)" % (agent, k, r.returncode))
    verifier("4. Navigation reelle vers les 4 fins: PARCOURS TERMINE + condition",
             nav_ok == 4, "; ".join(nav_ko))

    # --- Passe 3 : anti-regression du piege reactiver ---
    piege = []
    for chemin in parcours_liste:
        agent = agent_de_parcours(chemin)
        d = charger_parcours(chemin)
        for k, c in d.get("cases", {}).items():
            if c.get("type") != "fin":
                continue
            titre = c.get("titre", "")
            msg = c.get("message", "")
            if titre.startswith("FIN - Activer"):
                # Une fin qui ACTIVE un agent ne doit jamais utiliser reactiver
                if "activer-agent-principal.py reactiver" in msg:
                    piege.append("%s %s" % (agent, k))
    verifier("5. Anti-regression: aucune fin 'Activer X' avec commande reactiver",
             not piege, "; ".join(piege))

    # --- Passe 4 : ASCII + LF ---
    fichiers = [os.path.abspath(__file__)] + parcours_liste
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("6. ASCII strict: 0 non-ASCII (test + 11 parcours)",
             total_non_ascii == 0, "total = %d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("7. LF pur: 0 CRLF (test + 11 parcours)",
             total_crlf == 0, "total = %d" % total_crlf)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
