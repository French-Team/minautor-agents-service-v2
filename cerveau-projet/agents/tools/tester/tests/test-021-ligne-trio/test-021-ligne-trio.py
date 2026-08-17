#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-021-ligne-trio.py
Test formel de la LIGNE TRIO de Janus + boucle de correction du trio.

Contexte (missions 2026-08-11) :
  - Buffy a construit la LIGNE TRIO dans le parcours-janus v0.3.6 : branche
    'trio' en c1 -> cT1 (lire le protocole-controle-trio) -> cT2 (quel agent)
    -> cT3/cT4/cT5 (controle du livrable) -> OK : cT6 (Activer promethee) /
    cT7 (Activer minerve) / c10 (Reactiver Cerberus apres minerve) ; KO :
    cT8/cT9/cT10 (renvoyer le rapport a l agent concerne).
  - La BOUCLE DE CORRECTION : chaque parcours du trio (v0.2.3) a une branche
    'corriger' en c1 -> c9f (CORRIGER selon le rapport de Janus) -> c10
    (FIN - Activer Janus). Janus ne transmet jamais un livrable non conforme.

Cas couverts:
  1. Le parcours-janus v0.3.6 contient la branche 'trio' (c1 -> cT1)
  2. Les cases cT1..cT10 existent avec les bons types
  3. Les fins cT6/cT7/cT8/cT9/cT10 portent la commande activer exacte
     + 'PAS reactiver' (garde-fou P8, valider-cartes v0.4.0)
  4. Navigation reelle OUI : athena -> cT6 Activer promethee ;
     promethee -> cT7 Activer minerve ; minerve -> c10 Reactiver Cerberus
  5. Navigation reelle KO : athena -> cT8 ; promethee -> cT9 ;
     minerve -> cT10 (renvoi du rapport)
  6. Boucle de correction : branche 'corriger' + c9f sur athena/promethee/
     minerve, navigation 'OUI|corriger' atteint c10 (FIN - Activer Janus)
  7. valider-cartes-decision --agent janus/athena/promethee/minerve CONFORME
  8. ASCII strict : 0 non-ASCII (test + 4 parcours + protocole)
  9. LF pur : 0 CRLF (test + 4 parcours + protocole)

Usage:
  python3 test-021-ligne-trio.py
Tags: agents, janus, parcours
"""
import importlib.util
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
VALIDER = os.path.join(TOOLS_DIR, "valider", "valider-cartes-decision",
                       "valider-cartes-decision.py")
PROTOCOLE_TRIO = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                              "regles-immuables", "general",
                              "protocole-controle-trio",
                              "protocole-controle-trio.001.01.ebauche.md")

PARCOURS_JANUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "janus",
                              "parcours", "parcours-janus.json")

# Agents du trio et leur livrable
TRIO = {
    "athena": "pense-bete",
    "promethee": "spec",
    "minerve": "todo",
}

# Fins de transmission (OK) et de renvoi (KO) par maillon
FINS_OK = {"athena": "cT6", "promethee": "cT7", "minerve": "c10"}
FINS_KO = {"athena": "cT8", "promethee": "cT9", "minerve": "cT10"}
CIBLE_CMD = {"cT6": "promethee", "cT7": "minerve", "cT8": "athena",
             "cT9": "promethee", "cT10": "minerve"}

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


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO

    print("=== Test formel ligne trio (janus cT1..cT10 + boucle correction) ===")

    d_janus = charger_parcours(PARCOURS_JANUS)
    cases = d_janus["cases"]
    version_janus = d_janus["parcours"].get("version", "")

    # --- Passe 1 : structure statique ---
    # 1. Branche 'trio' dans c1
    c1_branches = cases.get("c1", {}).get("branches", [])
    branche_trio = any(b.get("reponse") == "trio" and b.get("vers") == "cT1"
                       for b in c1_branches)
    verifier("1. Branche 'trio' dans c1 -> cT1 (parcours-janus v%s)" % version_janus,
             branche_trio, "c1 branches=%s" % json.dumps(c1_branches, ensure_ascii=True))

    # 2. Cases cT1..cT10 presentes avec les bons types
    types_attendus = {
        "cT1": "action", "cT2": "question", "cT3": "controle",
        "cT4": "controle", "cT5": "controle", "cT6": "fin",
        "cT7": "fin", "cT8": "fin", "cT9": "fin", "cT10": "fin",
    }
    types_ko = []
    for k, t_att in sorted(types_attendus.items()):
        c = cases.get(k, {})
        if c.get("type") != t_att:
            types_ko.append("%s:%s" % (k, c.get("type")))
    verifier("2. Cases cT1..cT10 presentes avec les bons types",
             not types_ko, "; ".join(types_ko))

    # 3. Commandes exactes dans les fins cT6..cT10 (garde-fou P8)
    cmd_ko = []
    for k, cible in sorted(CIBLE_CMD.items()):
        msg = (cases.get(k, {}).get("message") or "").lower()
        attendu = "activer-agent-principal.py activer session-llm-1 %s" % cible
        if attendu not in msg or "pas reactiver" not in msg:
            cmd_ko.append("%s (activer %s)" % (k, cible))
    verifier("3. Fins cT6..cT10 : commande activer exacte + 'PAS reactiver'",
             not cmd_ko, "; ".join(cmd_ko))

    # --- Passe 2 : navigation reelle OK ---
    nav_ok_ko = []
    for agent, k in sorted(FINS_OK.items()):
        r = run([PYTHON, GUIDER, PARCOURS_JANUS, "--reponses",
                 "OUI|trio|%s|OUI" % agent])
        ok = (r.returncode == 0 and "Fin de parcours atteinte : case '%s'" % k in r.stdout)
        if not ok:
            nav_ok_ko.append("%s->%s (code=%d)" % (agent, k, r.returncode))
    verifier("4. Navigation OUI : athena->cT6, promethee->cT7, minerve->c10",
             not nav_ok_ko, "; ".join(nav_ok_ko))

    # --- Passe 3 : navigation reelle KO (renvoi du rapport) ---
    nav_ko_ko = []
    for agent, k in sorted(FINS_KO.items()):
        r = run([PYTHON, GUIDER, PARCOURS_JANUS, "--reponses",
                 "OUI|trio|%s|NON" % agent])
        ok = (r.returncode == 0 and "Fin de parcours atteinte : case '%s'" % k in r.stdout)
        if not ok:
            nav_ko_ko.append("%s->%s (code=%d)" % (agent, k, r.returncode))
    verifier("5. Navigation KO : athena->cT8, promethee->cT9, minerve->cT10",
             not nav_ko_ko, "; ".join(nav_ko_ko))

    # --- Passe 4 : boucle de correction dans le trio ---
    boucle_ko = []
    for agent in sorted(TRIO):
        p = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", agent,
                         "parcours", "parcours-%s.json" % agent)
        d = charger_parcours(p)
        c = d["cases"]
        b_corr = any(b.get("reponse") == "corriger" and b.get("vers") == "c9f"
                     for b in c.get("c1", {}).get("branches", []))
        c9f = c.get("c9f", {})
        # c9f -> c24 (Enregistrer mes usages d outils) -> c10 : le chemin passe
        # par la case registre dediee avant la fin (ajout Buffy 2026-08-11).
        c9f_suiv = c9f.get("suivant")
        c24 = c.get(c9f_suiv, {}) if c9f_suiv else {}
        r = run([PYTHON, GUIDER, p, "--reponses", "OUI|corriger"])
        nav_ok = (r.returncode == 0 and
                  "Fin de parcours atteinte : case 'c10'" in r.stdout)
        if not (b_corr and c9f.get("type") == "action" and c9f_suiv == "c24"
                and c24.get("suivant") == "c10" and nav_ok):
            boucle_ko.append(agent)
    verifier("6. Boucle correction : branche corriger + c9f -> c10 sur le trio",
             not boucle_ko, "; ".join(boucle_ko))

    # --- Passe 5 : valider-cartes-decision CONFORME ---
    vc_ko = []
    for agent in sorted(TRIO) + ["janus"]:
        r = run([PYTHON, VALIDER, "--agent", agent])
        if "Resultat : CONFORME" not in r.stdout:
            vc_ko.append(agent)
    verifier("7. valider-cartes-decision CONFORME (janus + trio)",
             not vc_ko, "; ".join(vc_ko))

    # --- Passe 6 : ASCII + LF ---
    fichiers = ([os.path.abspath(__file__), PARCOURS_JANUS, PROTOCOLE_TRIO] +
                [os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", a,
                              "parcours", "parcours-%s.json" % a)
                 for a in sorted(TRIO)])
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("8. ASCII strict: 0 non-ASCII (test + parcours + protocole)",
             total_non_ascii == 0, "total = %d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("9. LF pur: 0 CRLF (test + parcours + protocole)",
             total_crlf == 0, "total = %d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
