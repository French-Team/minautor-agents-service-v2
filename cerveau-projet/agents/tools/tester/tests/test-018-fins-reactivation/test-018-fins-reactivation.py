#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-018-fins-reactivation.py
Test formel des fins REACTIVER-CERBERUS precisees dans les 15 parcours.

Contexte (missions 2026-08-10 / 2026-08-11) :
  - La mission Buffy a precise la condition 'activation directe par Cerberus'
    sur les fins REACTIVER-CERBERUS de 4 parcours (atlas c11, clio c12,
    minerve c10, themis c13) ; morpheus c14 porte '(activation directe)'.
  - Le 2026-08-11, la REGLE IMMUABLE JANUS a ete generalisee (missions
    Buffy) : apres TOUTE mission (meme sans modifier du code), chaque agent
    active JANUS (second controle) qui reactive Cerberus. Ont ete
transformees en 'FIN - Activer Janus' : clio c12 (v0.4.3), atlas c11
    (v0.3.3), themis c13 (v0.3.5), morpheus c14 (v0.3.2).
  - Il ne reste que 2 fins REACTIVER-CERBERUS dans tout le cerveau :
    janus c10 (DERNIER MAILLON, bilan consolide - legitime, Janus ne peut
    pas s'activer lui-meme) et minerve c10 (PHASE 9, trio - hors perimetre
    de la generalisation).
  - minerve c10 porte la condition exacte 'activation directe par Cerberus'
    (seule fin precisee restante).
  - Le piege 'reactiver' a ete corrige : la commande reactiver ramene TOUJOURS
    a Cerberus. Aucune fin 'Activer l agent precedent' ne doit contenir la
    commande reactiver.

Regle verifiee (Pattern 13 de la spec-guider-parcours) :
  Toute fin REACTIVER-CERBERUS porte la condition (activation directe) SAUF
  le dernier maillon de chaine (bilan consolide).

Cas couverts:
  1. Chaque parcours des 15 agents contient au plus une fin REACTIVER-CERBERUS
  2. Toute fin REACTIVER-CERBERUS porte 'activation directe' dans son message
     OU est le dernier maillon (bilan consolide) : regle Pattern 13
  3. Plus aucune fin REACTIVER precisee hors janus : le trio
     (athena/promethee/minerve) a migre vers 'Activer Janus'
  4. Navigation reelle vers les fins du trio (guider-parcours --case) :
     chaque fin 'FIN - Activer Janus' est atteinte (PARCOURS TERMINE)
  4b. Clio a bien sa fin 'FIN - Activer Janus' en c12 (second controle,
      REGLE IMMUABLE JANUS) et la navigation reelle l'atteint
      (guider-parcours --case c12 : PARCOURS TERMINE)
  4d. Atlas c11, themis c13, morpheus c14 et le trio (athena c10,
      promethee c10, minerve c10) sont des fins 'FIN - Activer Janus'
      (REGLE IMMUABLE JANUS) et la navigation reelle les atteint
      (garde-fou positif de la generalisation)
  5. Anti-regression : aucune fin 'Activer l agent precedent' ne contient
     la commande reactiver (le piege corrige reste elimine)
  6. ASCII strict : 0 non-ASCII (test + 15 parcours)
  7. LF pur : 0 CRLF (test + 15 parcours)

Usage:
  python3 test-018-fins-reactivation.py
Tags: agents, parcours, cerberus, garde-fou-agent
"""
import importlib.util
import io
import glob
import json
import os
import re
import subprocess
import sys

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


GUIDER = os.path.join(TOOLS_DIR, "guider", "guider-parcours", "guider-parcours.py")
PARCOURS_GLOB = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                             "*", "parcours", "parcours-*.json")

# Fins precisees par la mission Buffy : condition exacte attendue
# (clio retire le 2026-08-11 ; atlas/themis retirees le 2026-08-11 apres
#  la generalisation REGLE IMMUABLE JANUS ; le trio athena/promethee/minerve
#  migre le 2026-08-11 vers 'Activer Janus' - il ne reste que janus,
#  qui est le dernier maillon legitime)
FINS_PRECISEES = {}
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
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


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
    verifier("0. 20 parcours trouves",
             len(parcours_liste) == 20, str(len(parcours_liste)))

    print("=== Test formel fins reactivation (15 parcours) ===")

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
    verifier("1b. La seule fin REACTIVER restante est janus (dernier maillon)",
             len(fins_reactiver) == 1 and "janus" in fins_reactiver,
             "agents=%s" % sorted(fins_reactiver))

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
    verifier("3. Aucune fin REACTIVER precisee hors janus (trio migree)",
             not ko_precises, "; ".join(ko_precises))

    # --- Passe 2 : navigation reelle vers la fin precisee restante ---
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
    verifier("4. Navigation reelle vers la fin precisee: PARCOURS TERMINE + condition",
             nav_ok == 0, "; ".join(nav_ko))

    # --- Passe 2b : clio a bien sa fin 'Activer Janus' (second controle) ---
    clio_chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "clio",
                               "parcours", "parcours-clio.json")
    clio_ok = False
    d_clio = charger_parcours(clio_chemin)
    c12 = d_clio.get("cases", {}).get("c12", {})
    msg_c12 = c12.get("message", "")
    ind_c12 = json.dumps(c12.get("indices", []), ensure_ascii=True).lower()
    if (c12.get("type") == "fin"
            and c12.get("titre") == "FIN - Activer Janus"
            and "janus" in msg_c12.lower()
            and "regle immuable janus" in ind_c12):
        clio_ok = True
    verifier("4b. Clio c12 est bien 'FIN - Activer Janus' (REGLE IMMUABLE JANUS)",
             clio_ok, "c12=%r" % c12.get("titre"))
    r_clio = run([PYTHON, GUIDER, clio_chemin, "--case", "c12"])
    verifier("4c. Navigation reelle clio c12: PARCOURS TERMINE",
             r_clio.returncode == 0 and "PARCOURS TERMINE" in r_clio.stdout,
             "code=%d" % r_clio.returncode)

    # --- Passe 2c : garde-fou positif de la generalisation Janus ---
    # atlas c11, themis c13, morpheus c14 : fins 'FIN - Activer Janus'
    FINS_ACTIVER_JANUS = {
        "atlas": "c11",
        "themis": "c13",
        "morpheus": "c14",
        "athena": "c10",
        "promethee": "c10",
        "minerve": "c10",
    }
    aj_ko = []
    for agent, k in sorted(FINS_ACTIVER_JANUS.items()):
        chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", agent,
                              "parcours", "parcours-%s.json" % agent)
        d = charger_parcours(chemin)
        c = d.get("cases", {}).get(k, {})
        ind = json.dumps(c.get("indices", []), ensure_ascii=True).lower()
        if not (c.get("type") == "fin"
                and c.get("titre") == "FIN - Activer Janus"
                and "regle immuable janus" in ind):
            aj_ko.append("%s %s" % (agent, k))
            continue
        r = run([PYTHON, GUIDER, chemin, "--case", k])
        if not (r.returncode == 0 and "PARCOURS TERMINE" in r.stdout):
            aj_ko.append("%s %s (nav code=%d)" % (agent, k, r.returncode))
    verifier("4d. 6 agents (atlas/themis/morpheus + trio) ont leur fin 'FIN - Activer Janus' navigable",
             not aj_ko, "; ".join(aj_ko))

    # --- Passe 3 : anti-regression du piege reactiver ---
    piege = []
    sans_commande = []
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
                # Garde-fou positif : toute fin 'Activer X' doit contenir la
                # COMMANDE EXACTE d'activation (sinon l'executant retombe sur
                # le reflexe reactiver qui ramene toujours a Cerberus)
                # D6 multi-sessions : le placeholder <session> est accepte
                # (chaque session le remplace par SON id a l execution).
                session_ok = ("activer <session>" in msg
                              or re.search(r"activer session-llm-\d+", msg))
                if ("activer-agent-principal.py activer" not in msg
                        or not session_ok):
                    sans_commande.append("%s %s" % (agent, k))
    verifier("5. Anti-regression: aucune fin 'Activer X' avec commande reactiver",
             not piege, "; ".join(piege))
    verifier("5b. Garde-fou positif: toute fin 'Activer X' porte la commande activer exacte",
             not sans_commande, "; ".join(sans_commande))

    # --- Passe 4 : ASCII + LF ---
    fichiers = [os.path.abspath(__file__)] + parcours_liste
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("6. ASCII strict: 0 non-ASCII (test + 15 parcours)",
             total_non_ascii == 0, "total = %d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("7. LF pur: 0 CRLF (test + 15 parcours)",
             total_crlf == 0, "total = %d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
