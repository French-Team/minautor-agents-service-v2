#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-119-flux-mot-theme-fin-oracle-garde-fou.py
GARDE-FOU : toute demande utilisateur commencant par [mot] doit passer par
le theme dedie puis finir vers ORACLE (decision utilisateur 2026-09-02,
mission 119cfe78 - constat : une demande [question] avait ete traitee sans
theme ni fin).

Contexte (2026-09-02) :
  - L utilisateur a constate que sa demande commencant par [question] avait
    ete traitee SANS servir le theme dedie (theme-question.json) et SANS
    faire la fin vers Oracle (reactiver-fin cerberus --cible oracle).
  - L infrastructure [mot] existe : pilote.py _type_mission_auto detecte
    les prefixes [attente]/[attention]/[urgent]/[question]/[creer]/
    [probleme]/[stop]/[socrate] et _resoudre_racine route vers le theme
    dedie ; chaque theme [mot] pointe vers fins.json qui impose la fin
    reactiver cerberus -> oracle.
  - Buffy a reecrit theme-question.json (partie 1/2) : le besoin
    'Repondre directement (dialogue)' a ete RETIRE - Cerberus transmet la
    question a Oracle qui active l agent detenteur de l information.

Invariants verifies :
  1. pilote.py _type_mission_auto : les 8 prefixes [mot] sont detectes
     (attente/attention/urgent/question/creer/probleme/stop/socrate) et
     retournent le type attendu
  2. _resoudre_racine (cerberus) : mission_type=QUESTION route vers
     theme-question.json ; les autres declencheurs routent vers LEUR theme
     dedie (jamais theme-de-user)
  3. theme-question.json : le besoin 'Repondre directement' a disparu, les
     2 besoins transmettent par Oracle
  4. Chaque theme [mot] (9 themes) pointe vers fins.json avec une case dont
     l action est 'reactiver' et la cible 'oracle' (fin jamais sautee)
  5. Preuve negative : une fin dont la cible est 'cerberus' (au lieu
     d'oracle) doit etre detectee par la verification
  6. Normes : ASCII strict + LF pur (pilote.py + themes + fins + test)
     + purge

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: flux-mot, declencheurs, theme, fin-oracle, garde-fou
"""
import importlib.util
import io
import json
import os
import shutil
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PILOTE_PY = os.path.join(TOOLS_DIR, "oracle", "fonctions", "pilote.py")
ARBRE_CERBERUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                              "cerberus", "parcours", "arbre-cerberus.json")
FINS_CERBERUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                             "cerberus", "parcours", "fins.json")
PARCOURS_CERBERUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                 "cerberus", "parcours")
THEMES_MOT = ["theme-attente.json", "theme-attention.json",
              "theme-urgent.json", "theme-question.json",
              "theme-creer.json", "theme-probleme.json",
              "theme-stop.json", "theme-socrate.json", "theme-trio.json"]

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

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

T_START = time.monotonic()
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
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-119 (total %.1fs) ===" % total)
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
        print("  [KO] %s" % nom)
        if detail:
            print("       %s" % detail)


def ascii_count(chemin):
    if not os.path.isfile(chemin):
        return -1
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    if not os.path.isfile(chemin):
        return -1
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def charger_pilote():
    spec = importlib.util.spec_from_file_location("pilote_mod", PILOTE_PY)
    p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)
    return p


def charger_json(chemin):
    with open(chemin, encoding="utf-8") as fh:
        return json.load(fh)


def chargement_fins_case(fin_case, fins_data):
    """Retrouver la case de fin dans fins.json (structure fiche/fins)."""
    fins = fins_data.get("fins", fins_data)
    if isinstance(fins, dict):
        return fins.get(fin_case)
    for f in fins:
        if f.get("nom") == fin_case or f.get("id") == fin_case:
            return f
    return None


# ------------------------------------------------------------------
# Points
# ------------------------------------------------------------------
def point_1_type_mission_auto():
    p = charger_pilote()
    cas = [
        ("[attente] mettre en file plus tard", "attente"),
        ("[attention] verifier le perimetre", "attention"),
        ("[urgent] serveur mort", "urgent"),
        ("[question] qui recoit les messages de la routine notation", "question"),
        ("[creer] un outil lister-flags", "creer"),
        ("[probleme] fichier corrompu", "probleme"),
        ("[stop] arret total", "stop"),
        ("[socrate] revision strategique", "socrate"),
    ]
    ko = []
    for mission, attendu in cas:
        got = p._type_mission_auto(mission)
        if got != attendu:
            ko.append("%s->%s attendu %s" % (mission[:25], got, attendu))
    verifier("1. _type_mission_auto : 8 prefixes [mot] detectes",
             not ko, "; ".join(ko[:3]))


def point_2_resoudre_racine():
    p = charger_pilote()
    arbre = charger_json(ARBRE_CERBERUS)
    racine = arbre.get("racine", {})
    attendus = {
        "QUESTION": "theme-question.json",
        "ATTENTION": "theme-attention.json",
        "URGENT": "theme-urgent.json",
        "CREER": "theme-creer.json",
        "PROBLEME": "theme-probleme.json",
        "STOP": "theme-stop.json",
        "ATTENTE": "theme-attente.json",
    }
    ko = []
    for mt, att in attendus.items():
        etat = {"agent": "cerberus", "mission_type": mt}
        got = p._resoudre_racine(racine, etat)
        nom = os.path.basename(got) if got else None
        if nom != att:
            ko.append("%s->%s attendu %s" % (mt, nom, att))
    verifier("2. _resoudre_racine : declencheurs -> theme dedie (jamais de-user)",
             not ko, "; ".join(ko[:3]))


def point_3_theme_question_reecrit():
    tq = charger_json(os.path.join(PARCOURS_CERBERUS, "theme-question.json"))
    besoins = [r.get("besoin", "") for r in tq.get("theme", {}).get("redirects", [])]
    direct = [b for b in besoins if "Repondre directement" in b
              or "repondre directement" in b.lower()]
    ok_retire = not direct and len(besoins) >= 2
    ok_etapes = all("oracle" in " ".join(r.get("etapes", [])).lower()
                    for r in tq.get("theme", {}).get("redirects", []))
    verifier("3. theme-question.json : 'Repondre directement' retire, besoins via Oracle",
             ok_retire and ok_etapes,
             "besoins=%s" % besoins)


def _verifier_fins_vers_oracle(fins_data):
    """Verifier que les 9 themes [mot] pointent vers une fin reactiver->oracle.
    Retourne la liste des ecarts (vide = conforme)."""
    ecarts = []
    fins = fins_data.get("fins", fins_data)
    for nom_theme in THEMES_MOT:
        chemin = os.path.join(PARCOURS_CERBERUS, nom_theme)
        if not os.path.isfile(chemin):
            ecarts.append("%s: fichier absent" % nom_theme)
            continue
        theme = charger_json(chemin)
        fin = theme.get("fin", {})
        vers = fin.get("vers")
        case = fin.get("case")
        if vers != "fins.json":
            ecarts.append("%s: fin.vers=%s (attendu fins.json)" % (nom_theme, vers))
            continue
        fin_case = chargement_fins_case(case, fins_data)
        if fin_case is None:
            ecarts.append("%s: case %s absente de fins.json" % (nom_theme, case))
            continue
        action = fin_case.get("action")
        cible = fin_case.get("cible")
        if action != "reactiver" or cible != "oracle":
            ecarts.append("%s: fin case %s action=%s cible=%s (attendu reactiver/oracle)"
                          % (nom_theme, case, action, cible))
    return ecarts


def point_4_fins_vers_oracle():
    fins_data = charger_json(FINS_CERBERUS)
    ecarts = _verifier_fins_vers_oracle(fins_data)
    verifier("4. 9 themes [mot] -> fin reactiver cerberus vers oracle",
             not ecarts, "; ".join(ecarts[:4]))


def point_5_preuve_negative():
    # Simuler une fin cassee (cible cerberus au lieu d oracle) : la
    # verification doit la DETECTER. On charge fins.json et on clone la
    # structure avec la case fin-declencheur corrompue.
    fins_data = charger_json(FINS_CERBERUS)
    clone = json.loads(json.dumps(fins_data))
    fins = clone.get("fins", clone)
    if isinstance(fins, dict) and "fin-declencheur" in fins:
        fins["fin-declencheur"] = dict(fins["fin-declencheur"], cible="cerberus")
    ecarts = _verifier_fins_vers_oracle(clone)
    verifier("5. Preuve negative : fin cible cerberus detectee comme ecart",
             len(ecarts) >= 1,
             "ecarts=%s" % ecarts[:3])


def point_6_normes():
    fichiers = [os.path.abspath(__file__), PILOTE_PY, FINS_CERBERUS]
    fichiers += [os.path.join(PARCOURS_CERBERUS, t) for t in THEMES_MOT]
    total_na = sum(max(ascii_count(f), 0) for f in fichiers)
    total_crlf = sum(max(crlf_count(f), 0) for f in fichiers)
    verifier("6. ASCII strict : 0 non-ASCII (pilote + themes + fins + test)",
             total_na == 0, "nb=%d" % total_na)
    verifier("7. LF pur : 0 CRLF (pilote + themes + fins + test)",
             total_crlf == 0, "nb=%d" % total_crlf)


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-119 : flux [mot] -> theme dedie + fin vers Oracle ===")
    try:
        if point_actif(1):
            t0 = time.monotonic()
            point_1_type_mission_auto()
            chrono_etape("1. _type_mission_auto", t0)
        if point_actif(2):
            t0 = time.monotonic()
            point_2_resoudre_racine()
            chrono_etape("2. _resoudre_racine", t0)
        if point_actif(3):
            t0 = time.monotonic()
            point_3_theme_question_reecrit()
            chrono_etape("3. theme-question", t0)
        if point_actif(4):
            t0 = time.monotonic()
            point_4_fins_vers_oracle()
            chrono_etape("4. fins -> oracle", t0)
        if point_actif(5):
            t0 = time.monotonic()
            point_5_preuve_negative()
            chrono_etape("5. preuve negative", t0)
        if point_actif(6):
            t0 = time.monotonic()
            point_6_normes()
            chrono_etape("6-7. normes", t0)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1
    except Exception as e:
        print("  [KO] EXCEPTION : %s" % e)
        NB_KO += 1

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % ("PROPRE (flux [mot] complet)"
                                    if NB_KO == 0 else "KO (flux [mot] casse)"))
    return 1 if NB_KO > 0 else 0


if __name__ == "__main__":
    sys.exit(main())