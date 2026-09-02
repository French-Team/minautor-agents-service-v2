#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-120-consommateur-notation-garde-fou.py
GARDE-FOU : le consommateur [NOTATION] d oracle.py v0.5.9 convertit les
demandes d evaluation croisee de la routine notation en mission Themis
(decision utilisateur 2026-09-02, mission eaa954a0 + f141af1d).

Contexte (2026-09-02) :
  - La routine notation (routines/notation.py) depose toutes les 960s une
    demande [NOTATION] dans l inbox d Oracle (inbox/oracle.jsonl) demandant
    l activation de l evaluation croisee par Themis.
  - Auparavant AUCUN code ne convertissait cette demande en mission : Oracle
    acquittait par habitude et la rotation MAX_MESSAGES=5 purgeait sans
    traitement ('Personne ne les lisait et personne n en tenait compte').
  - Fix (oracle.py v0.5.9) : _consommer_notation() parcourt l inbox d Oracle,
    convertit chaque message [NOTATION] non-acquitte en mission Themis via
    files.ajouter(mission, file=asap, agent=themis), marque le message
    accuse+consomme+consomme_date. Hooks : cmd_lire et cmd_acquitter
    (agent oracle). Anti-inondation : pas de depot si une mission Themis
    d evaluation est deja EN_ATTENTE OU si un depot a eu lieu il y a moins
    de 60 min (.notation_consommation.txt).

Invariants verifies (sur repertoires TEMPORAIRES, jamais les vrais) :
  1. _consommer_notation() convertit un message [NOTATION] non-acquitte en
     mission Themis (EVALUATION CROISEE) dans la file asap
  2. Les marqueurs du message : accuse=True + consomme=True + consomme_date
  3. Anti-inondation mission : 2e message [NOTATION] avec mission Themis
     deja EN_ATTENTE -> aucun nouveau depot (1 seule mission)
  4. Anti-inondation temporel : .notation_consommation.txt recent (< 60 min)
     -> aucun depot
  5. Preuve negative : un message NON-[NOTATION] ne declenche aucun depot
  6. Hooks : cmd_lire(agent=oracle) avec un [NOTATION] non lu declenche le
     consommateur
  7-8. Normes : ASCII strict + LF pur + purge

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: consommateur, notation, themis, evaluation, garde-fou
"""
import importlib.util
import io
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
ORACLE_PY = os.path.join(TOOLS_DIR, "oracle", "oracle.py")
FILES_PY = os.path.join(TOOLS_DIR, "oracle", "fonctions", "files.py")

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
    print("=== CHRONO test-120 (total %.1fs) ===" % total)
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


def charger_oracle(tmp_dir):
    """Charger oracle.py avec INBOX_DIR/FILES_DIR/fichier-anti-inondation
    rediriges vers tmp_dir (jamais les vrais repertoires)."""
    spec = importlib.util.spec_from_file_location("oracle_mod", ORACLE_PY)
    o = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(o)
    tmp = Path(tmp_dir)
    (tmp / "inbox").mkdir(parents=True, exist_ok=True)
    (tmp / "files").mkdir(parents=True, exist_ok=True)
    (tmp / "routines").mkdir(parents=True, exist_ok=True)
    o.INBOX_DIR = tmp / "inbox"
    o.FILES_DIR = tmp / "files"
    o._FICHIER_CONSOM_NOTATION = tmp / "routines" / ".notation_consommation.txt"
    # files.py importe par oracle.py : rediriger aussi son FILES_DIR
    o._files.FILES_DIR = tmp / "files"
    return o


def message_notation(mid, lu=False):
    return {
        "id": mid,
        "de": "notation",
        "vers": "oracle",
        "priorite": 2,
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[NOTATION] demande activation de l evaluation periodique "
                 "des agents",
        "corps": "DEMANDE D EVALUATION CROISEE (test) : Themis doit etre "
                 "activee pour poser le questionnaire d evaluation croisee.",
        "lu": lu,
        "accuse": False,
        "type": "notation",
    }


def ecrire_inbox(o, messages):
    lignes = [json.dumps(m, ensure_ascii=False) for m in messages]
    (o.INBOX_DIR / "oracle.jsonl").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8")


def lire_inbox(o):
    p = o.INBOX_DIR / "oracle.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()
            if l.strip()]


def missions_themis(o):
    result = []
    p = o.FILES_DIR / "asap.jsonl"
    if not p.exists():
        return result
    for l in p.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        try:
            e = json.loads(l)
        except ValueError:
            continue
        if (e.get("agent", "").strip().casefold() == "themis"
                and "EVALUATION" in str(e.get("mission", "")).upper()):
            result.append(e)
    return result


def point_1_conversion(o):
    ecrire_inbox(o, [message_notation("n1")])
    o._consommer_notation()
    ms = missions_themis(o)
    ok_mission = len(ms) == 1 and ms[0].get("statut") == "EN_ATTENTE"
    ok_agent = ms[0].get("agent") == "themis" if ms else False
    ok_texte = "EVALUATION CROISEE" in str(ms[0].get("mission", "")) if ms else False
    verifier("1. _consommer_notation() : [NOTATION] -> mission Themis asap",
             ok_mission and ok_agent and ok_texte,
             "missions=%d" % len(ms))


def point_2_marqueurs(o):
    ecrire_inbox(o, [message_notation("n2")])
    o._consommer_notation()
    msgs = lire_inbox(o)
    m = msgs[0] if msgs else {}
    verifier("2. Marqueurs : accuse + consomme + consomme_date poses",
             m.get("accuse") is True and m.get("consomme") is True
             and bool(m.get("consomme_date")),
             "accuse=%s consomme=%s date=%s"
             % (m.get("accuse"), m.get("consomme"), m.get("consomme_date")))


def point_3_anti_inondation_mission(o):
    # 1re demande -> mission deposee
    ecrire_inbox(o, [message_notation("n3a")])
    o._consommer_notation()
    # 2e demande (mission Themis deja EN_ATTENTE) -> aucun nouveau depot
    ecrire_inbox(o, [message_notation("n3b")])
    o._consommer_notation()
    ms = missions_themis(o)
    verifier("3. Anti-inondation : mission Themis deja EN_ATTENTE -> 1 seule",
             len(ms) == 1, "missions=%d" % len(ms))


def point_4_anti_inondation_temporel(o):
    # Poser un fichier .notation_consommation recent (< 60 min)
    o._FICHIER_CONSOM_NOTATION.write_text(str(time.time()))
    ecrire_inbox(o, [message_notation("n4")])
    o._consommer_notation()
    ms = missions_themis(o)
    verifier("4. Anti-inondation : depot recent (< 60 min) -> aucun depot",
             len(ms) == 0, "missions=%d" % len(ms))
    o._FICHIER_CONSOM_NOTATION.unlink(missing_ok=True)


def point_5_preuve_negative(o):
    ecrire_inbox(o, [{
        "id": "autre-1",
        "de": "vigie-perimetre",
        "vers": "oracle",
        "priorite": 2,
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[VIGIE-PERIMETRE] perimetre modifie",
        "corps": "Un fichier du perimetre a change.",
        "lu": False,
        "accuse": False,
        "type": "vigie-perimetre",
    }])
    o._consommer_notation()
    ms = missions_themis(o)
    verifier("5. Preuve negative : NON-[NOTATION] -> aucun depot",
             len(ms) == 0, "missions=%d" % len(ms))


def point_6_hook_cmd_lire(o):
    ecrire_inbox(o, [message_notation("n6", lu=False)])
    o.cmd_lire(type("A", (), {"agent": "oracle"})())
    ms = missions_themis(o)
    verifier("6. Hook cmd_lire(agent=oracle) : [NOTATION] lu -> mission deposee",
             len(ms) == 1, "missions=%d" % len(ms))


def point_7_normes():
    fichiers = [os.path.abspath(__file__), ORACLE_PY]
    total_na = sum(max(ascii_count(f), 0) for f in fichiers)
    total_crlf = sum(max(crlf_count(f), 0) for f in fichiers)
    verifier("7. ASCII strict : 0 non-ASCII (oracle.py + test)",
             total_na == 0, "nb=%d" % total_na)
    verifier("8. LF pur : 0 CRLF (oracle.py + test)",
             total_crlf == 0, "nb=%d" % total_crlf)


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-120 : consommateur [NOTATION] -> mission Themis ===")
    tmp_base = os.path.join(PROJECT_ROOT, "tmp-test120")
    try:
        # Chaque point a SON sous-repertoire isole (lecon test-118) : les
        # files/inbox se polluent sinon (mission du point 1 en attente ->
        # fausse les anti-inondation des points suivants).
        if point_actif(1):
            t0 = time.monotonic()
            point_1_conversion(charger_oracle(os.path.join(tmp_base, "p1")))
            chrono_etape("1. conversion", t0)
        if point_actif(2):
            t0 = time.monotonic()
            point_2_marqueurs(charger_oracle(os.path.join(tmp_base, "p2")))
            chrono_etape("2. marqueurs", t0)
        if point_actif(3):
            t0 = time.monotonic()
            point_3_anti_inondation_mission(
                charger_oracle(os.path.join(tmp_base, "p3")))
            chrono_etape("3. anti-inondation mission", t0)
        if point_actif(4):
            t0 = time.monotonic()
            point_4_anti_inondation_temporel(
                charger_oracle(os.path.join(tmp_base, "p4")))
            chrono_etape("4. anti-inondation temporel", t0)
        if point_actif(5):
            t0 = time.monotonic()
            point_5_preuve_negative(
                charger_oracle(os.path.join(tmp_base, "p5")))
            chrono_etape("5. preuve negative", t0)
        if point_actif(6):
            t0 = time.monotonic()
            point_6_hook_cmd_lire(charger_oracle(os.path.join(tmp_base, "p6")))
            chrono_etape("6. hook cmd_lire", t0)
        if point_actif(7):
            t0 = time.monotonic()
            point_7_normes()
            chrono_etape("7-8. normes", t0)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1
    except Exception as e:
        print("  [KO] EXCEPTION : %s" % e)
        NB_KO += 1
    finally:
        if os.path.isdir(tmp_base):
            shutil.rmtree(tmp_base, ignore_errors=True)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % ("PROPRE (consommateur [NOTATION] actif)"
                                    if NB_KO == 0 else "KO (consommateur casse)"))
    return 1 if NB_KO > 0 else 0


if __name__ == "__main__":
    sys.exit(main())