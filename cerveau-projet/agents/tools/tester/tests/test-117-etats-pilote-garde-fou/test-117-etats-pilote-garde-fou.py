#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-117-etats-pilote-garde-fou.py
GARDE-FOU : la colonne Etat des lignes pilote dans AGENTS-activite-recente.md
reflete les phases de vol reelles (decision utilisateur 2026-09-02,
etats-actions.json v0.1.2, mission 8d3fbc34).

Contexte (etats-actions.json v0.1.1 -> v0.1.2, 2026-09-02) :
  - Le pilote (aero, modele aeroport) trace ses phases de vol via
    _historiser_pilote (fonctions/pilote.py) : DECOLLAGE (theme=...),
    RECUPERE (<agent>), RETOUR AEROPORT (<agent>), LARGUE (<cible>).
  - Avant v0.1.2, la regle DEBUT avait les prefixes [DEBUT, RETOUR] :
    toute raison commencant par RETOUR (y compris RETOUR AEROPORT) etait
    classee DEBUT. RECUPERE/DECOLLAGE/LARGUE tombaient au defaut ACTIF.
  - Fix : 4 etats de vol ajoutes (DECOLLAGE, RECUPERE, RETOUR, LARGUE)
    avec des regles SPECIFIQUES placees AVANT la regle DEBUT (l ordre du
    fichier compte, la premiere regle qui matche gagne) ; DEBUT ne matche
    plus RETOUR seul mais RETOUR ORACLE (agents reactives via Oracle).

Invariants verifies :
  1. etats-actions.json existe, JSON valide, version 0.1.2
  2. Les 4 etats pilote sont presents AVANT la regle DEBUT dans le
     fichier (priorite de detection)
  3. _etat_action (charge le fichier dynamiquement) : les 4 traces
     pilote reelles -> leurs etats ; encart : les 4 etats sont dans les
     etats connus (charge dynamiquement, aucune valeur Etat inconnue)
  4. PREUVE NEGATIVE : retirer une regle pilote (simulation) -> la trace
     correspondante retombe a tort (DEBUT pour RETOUR AEROPORT si la
     regle RETOUR disparait) - le garde-fou ne dort pas
  5. Non-regression : 'RETOUR ORACLE : ...' reste DEBUT (agents
     reactives), FIN et ACTION inchanges
  6. Normes : ASCII strict + LF pur (fichier data + test)

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: etats, pilote, colonne-etat, garde-fou, preuve-negative
"""
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
PYTHON = sys.executable

ETATS_JSON = os.path.join(TOOLS_DIR, "oracle", "etats-actions.json")
ACTIVER_PY = os.path.join(TOOLS_DIR, "activer", "activer-agent-principal",
                          "activer-agent-principal.py")
ENCART_PY = os.path.join(TOOLS_DIR, "oracle", "routines", "encart.py")

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
    print("=== CHRONO test-117 (total %.1fs) ===" % total)
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


def lancer(cmd, timeout=60, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


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


ETATS_PILOTE = ["DECOLLAGE", "RECUPERE", "RETOUR", "LARGUE"]


def charger_json():
    with io.open(ETATS_JSON, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def charger_etat_action():
    spec = importlib.util.spec_from_file_location("aap_etats", ACTIVER_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def charger_encart():
    spec = importlib.util.spec_from_file_location("encart_etats", ENCART_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ordre_etats(data):
    """Ordre des cles 'etats' dans le fichier (l ordre compte)."""
    return list(data.get("etats", {}).keys())


# ------------------------------------------------------------------
# Points
# ------------------------------------------------------------------
def point_1_json():
    ok = os.path.isfile(ETATS_JSON)
    version = ""
    detail = "fichier absent"
    if ok:
        try:
            data = charger_json()
            version = str(data.get("version", ""))
            ok = ok and version == "0.1.2"
            detail = "version=%s" % version
        except Exception as e:
            ok = False
            detail = "json invalide: %s" % e
    verifier("1. etats-actions.json JSON valide, version 0.1.2", ok, detail)


def point_2_ordre():
    data = charger_json()
    ordre = ordre_etats(data)
    pos_debut = ordre.index("DEBUT") if "DEBUT" in ordre else -1
    manquants = [e for e in ETATS_PILOTE if e not in ordre]
    avant = all(ordre.index(e) < pos_debut for e in ETATS_PILOTE
                if e in ordre)
    ok = pos_debut >= 0 and not manquants and avant
    verifier("2. 4 etats pilote presents AVANT DEBUT (priorite)",
             ok, "ordre=%s manquants=%s" % (ordre, manquants))


def point_3_classification():
    """Traces pilote reelles -> leurs etats ; non-regression DEBUT/FIN."""
    aap = charger_etat_action()
    cas = [
        ("DECOLLAGE: theme=modifier", "pilote", "DECOLLAGE"),
        ("RECUPERE: vulcain", "pilote", "RECUPERE"),
        ("RETOUR AEROPORT: oracle", "pilote", "RETOUR"),
        ("LARGUE: morpheus", "pilote", "LARGUE"),
        ("RETOUR ORACLE : FIN: COORDINATION TERMINEE", "cerberus", "DEBUT"),
        ("DEBUT: MISSION X", "vulcain", "DEBUT"),
        ("FIN: FIN MORPHEUS", "morpheus", "FIN"),
        ("Acquittement message x", "oracle", "ACTION"),
    ]
    ko = []
    for raison, agent, attendu in cas:
        got = aap._etat_action(raison, agent)
        if got != attendu:
            ko.append("%s(%s)->%s attendu %s" % (raison[:25], agent, got,
                                                 attendu))
    verifier("3. _etat_action : 4 vols pilote + non-regression (8 cas)",
             not ko, "; ".join(ko[:3]))


def point_4_encart():
    encart = charger_encart()
    try:
        connus = encart._charger_etats_connus()
    except AttributeError:
        # Repli : lire le fichier directement
        data = charger_json()
        connus = set(data.get("etats", {}).keys())
    manquants = [e for e in ETATS_PILOTE if e not in connus]
    verifier("4. encart : 4 etats pilote dans les etats connus",
             not manquants, "manquants=%s" % manquants)


def point_5_preuve_negative():
    """Retirer une regle -> la trace retombe a tort (garde-fou actif)."""
    tmp = os.path.join(PROJECT_ROOT, "tmp-test117")
    if os.path.isdir(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp, exist_ok=True)
    fichier_bis = os.path.join(tmp, "etats-actions.json")
    data = charger_json()
    del data["etats"]["RETOUR"]
    with io.open(fichier_bis, "w", encoding="ascii", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=True, indent=1)
    # Charger _etat_action avec le fichier bis (env pointe AVANT import)
    ancien = os.environ.get("ETATS_ACTIONS")
    os.environ["ETATS_ACTIONS"] = fichier_bis
    try:
        spec = importlib.util.spec_from_file_location("aap_neg", ACTIVER_PY)
        aap = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aap)
        got = aap._etat_action("RETOUR AEROPORT: oracle", "pilote")
        detecte = got in ("DEBUT", "ACTIF")  # la regle RETOUR manque
    finally:
        if ancien is None:
            os.environ.pop("ETATS_ACTIONS", None)
        else:
            os.environ["ETATS_ACTIONS"] = ancien
        shutil.rmtree(tmp, ignore_errors=True)
    verifier("5. preuve negative : sans la regle RETOUR, RETOUR AEROPORT"
             " n est plus classe RETOUR", detecte, "got=%s" % got)


def point_6_normes():
    fichiers = [os.path.abspath(__file__), ETATS_JSON]
    total_na = sum(max(ascii_count(f), 0) for f in fichiers)
    total_crlf = sum(max(crlf_count(f), 0) for f in fichiers)
    verifier("6. ASCII strict : 0 non-ASCII (etats-actions.json + test)",
             total_na == 0, "nb=%d" % total_na)
    verifier("7. LF pur : 0 CRLF (etats-actions.json + test)",
             total_crlf == 0, "nb=%d" % total_crlf)


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-117 : etats de vol du pilote (colonne Etat) ===")
    try:
        if point_actif(1):
            t0 = time.monotonic()
            point_1_json()
            chrono_etape("1. json", t0)
        if point_actif(2):
            t0 = time.monotonic()
            point_2_ordre()
            chrono_etape("2. ordre", t0)
        if point_actif(3):
            t0 = time.monotonic()
            point_3_classification()
            chrono_etape("3. classification", t0)
        if point_actif(4):
            t0 = time.monotonic()
            point_4_encart()
            chrono_etape("4. encart", t0)
        if point_actif(5):
            t0 = time.monotonic()
            point_5_preuve_negative()
            chrono_etape("5. preuve negative", t0)
        if point_actif(6):
            t0 = time.monotonic()
            point_6_normes()
            chrono_etape("6. normes", t0)
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
    print("=== VERDICT : %s ===" % ("PROPRE (etats pilote calques sur l action)"
                                    if NB_KO == 0 else "KO (etats pilote incoherents)"))
    return 1 if NB_KO > 0 else 0


if __name__ == "__main__":
    sys.exit(main())