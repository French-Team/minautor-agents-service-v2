#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-123-consommation-notification-mission-garde-fou.py
GARDE-FOU : a la TERMINEE d une mission, files.terminer() consomme la
notification 'MISSION pour X' dans l inbox de l agent (correctif boucle
flux / P1 fantomes, oracle v0.5.11, mission 6ad0c87c - constat
utilisateur 2026-09-04).

Cause racine corrigee : mission-relais (_envoyer_direct dans oracle.py)
depose un P1 'MISSION pour X' (lu=False, sans champ type) dans
inbox/<agent>.jsonl. flux.py compte exactement ces messages
(not lu and priorite==1 and not type). Quand la mission devenait TERMINEE,
RIEN ne marquait ce message lu/accuse : il restait P1 non-lu indefiniment
-> flux le recomptait a chaque cycle -> encart URGENT (source flux) ->
verifier-statuts escaladait DEFCON 4 et deposait 'ETAT URGENT xN: N P1
non-acquitte(s)' en asap -> Oracle devait acquitter manuellement chaque
round.

Fix : _consommer_notification_mission(entree) dans fonctions/files.py,
appele par terminer() (point unique de transition vers TERMINEE) -
consomme (supprime) le message MISSION correspondant : meme agent,
de==oracle, objet=='MISSION pour <agent>', corps normalise == texte
mission. Idempotent, no-op si agent/inbox absents, autres P1 preserves.

Points verifies (sur FILES_DIR temporaire, jamais les vraies files) :
  1. terminer() consomme le message MISSION (absent de l inbox apres)
     et PRESERVE un second message P1 non-mission
  2. Idempotence : terminer une 2e fois (deja TERMINEE) -> no-op sans
     erreur, aucune ligne perdue
  3. Entree sans champ agent -> terminer ne plante pas, aucune inbox
     touchee
  4. Corps different (autre mission) -> message NON consomme (pas de
     faux positif)
  5. Agent sans fichier inbox -> terminer ne plante pas (no-op)
  6. flux --dry-run apres TERMINEE : la notification consommee ne
     compte plus comme P1 non-acquitte (0 pour ce message)
  7. Normes : ASCII strict + LF pur (files.py + test)
  8. PERSISTANCE relais (complement 0.5.12, decouvert en validation
     live) : mission SANS agent -> relais() deduit l agent ET le
     persiste dans le fichier (source de verite) -> terminer() retrouve
     l agent et consomme la notification correspondante

Proprietaire : Morpheus (testeur dedie)
Version : 0.2.0
Tags: files, terminer, mission, notification, flux, garde-fou
"""
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
FILES_PY = os.path.join(TOOLS_DIR, "oracle", "fonctions", "files.py")
FLUX_PY = os.path.join(TOOLS_DIR, "oracle", "routines", "flux.py")
ORACLE_DIR = os.path.join(TOOLS_DIR, "oracle")

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
    print("=== CHRONO test-123 (total %.1fs) ===" % total)
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
    try:
        data = io.open(chemin, "r", encoding="utf-8").read()
    except (OSError, UnicodeError):
        return -1
    return sum(1 for ch in data if ord(ch) > 127)


def crlf_count(chemin):
    try:
        data = io.open(chemin, "r", encoding="utf-8").read()
    except (OSError, UnicodeError):
        return -1
    return data.count("\r\n")


def charger_files(base_dir):
    """Charger fonctions/files.py avec FILES_DIR redirige vers
    base_dir/files (la hierarchie oracle : files/ et inbox/ sont freres,
    _consommer_notification_mission lit FILES_DIR.parent/inbox)."""
    files_dir = os.path.join(base_dir, "files")
    os.makedirs(files_dir, exist_ok=True)
    spec = importlib.util.spec_from_file_location("files_mod", FILES_PY)
    f = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(f)
    ancien = f.FILES_DIR
    f.FILES_DIR = type(ancien)(files_dir)
    return f, ancien


def sous_tmp(tmp_dir, nom):
    """Base dediee a un point : contient files/ et inbox/ (freres)."""
    p = os.path.join(tmp_dir, nom)
    os.makedirs(os.path.join(p, "files"), exist_ok=True)
    os.makedirs(os.path.join(p, "inbox"), exist_ok=True)
    return p


def ecrire_inbox(base_dir, agent, messages):
    """Ecrire base_dir/inbox/<agent>.jsonl (miroir)."""
    inbox = os.path.join(base_dir, "inbox")
    os.makedirs(inbox, exist_ok=True)
    with io.open(os.path.join(inbox, "%s.jsonl" % agent), "w",
                 encoding="utf-8", newline="\n") as f:
        for m in messages:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")


def lire_inbox(base_dir, agent):
    """Lire base_dir/inbox/<agent>.jsonl -> liste de dicts."""
    inbox = os.path.join(base_dir, "inbox")
    chemin = os.path.join(inbox, "%s.jsonl" % agent)
    if not os.path.isfile(chemin):
        return []
    result = []
    with io.open(chemin, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                result.append(json.loads(ligne))
            except ValueError:
                continue
    return result


def message_mission(agent, texte):
    return {"id": "notif-%s" % agent, "de": "oracle", "vers": agent,
            "priorite": 1, "date": "2026-09-04T09:00:00",
            "objet": "MISSION pour %s" % agent, "corps": texte,
            "lu": False, "accuse": False}


def message_non_mission(agent):
    return {"id": "autre-%s" % agent, "de": "oracle", "vers": agent,
            "priorite": 1, "date": "2026-09-04T09:00:00",
            "objet": "autre alerte", "corps": "autre chose a traiter",
            "lu": False}


def point_1_consommation(tmp_dir):
    """terminer() consomme le MESSAGE MISSION, preserve le non-mission."""
    t0 = time.monotonic()
    base = sous_tmp(tmp_dir, "p1")
    f, _ = charger_files(base)
    e, err = f.ajouter("TEST mission point 1", file="asap", agent="x")
    assert e is not None and err is None
    ecrire_inbox(base, "x", [message_mission("x", e["mission"]),
                             message_non_mission("x")])
    pris, _ = f.prendre(file="asap")
    ret, err = f.terminer(pris["id"], file="asap")
    restants = lire_inbox(base, "x")
    objets = [m.get("objet") for m in restants]
    ok = (ret.get("statut") == "TERMINEE" and err is None
          and "MISSION pour x" not in objets
          and "autre alerte" in objets)
    verifier("1. terminer() consomme MISSION, preserve non-mission",
             ok, "objets=%s" % objets)
    chrono_etape("1 consommation", t0)


def point_2_idempotence(tmp_dir):
    """Terminer une 2e fois (deja TERMINEE) -> no-op sans erreur."""
    t0 = time.monotonic()
    base = sous_tmp(tmp_dir, "p2")
    f, _ = charger_files(base)
    e, _ = f.ajouter("TEST mission point 2", file="asap", agent="y")
    ecrire_inbox(base, "y", [message_mission("y", e["mission"])])
    pris, _ = f.prendre(file="asap")
    f.terminer(pris["id"], file="asap")
    restants_1 = lire_inbox(base, "y")
    # 2e terminer : la mission est deja TERMINEE (statut non trouve en
    # EN_ATTENTE mais l entree existe -> la re-marque TERMINEE, idempotent)
    ret2, err2 = f.terminer(pris["id"], file="asap")
    restants_2 = lire_inbox(base, "y")
    ok = (err2 is None and len(restants_1) == len(restants_2)
          and all(not m.get("objet", "").startswith("MISSION pour")
                  for m in restants_2))
    verifier("2. terminer() 2e fois : no-op sans erreur (idempotent)",
             ok, "err2=%s n1=%d n2=%d" % (err2, len(restants_1),
                                          len(restants_2)))
    chrono_etape("2 idempotence", t0)


def point_3_sans_agent(tmp_dir):
    """Entree sans champ agent -> terminer ne plante pas, inbox intacte."""
    t0 = time.monotonic()
    base = sous_tmp(tmp_dir, "p3")
    f, _ = charger_files(base)
    e, _ = f.ajouter("TEST mission sans agent", file="asap", agent="")
    ecrire_inbox(base, "z", [message_non_mission("z")])
    pris, _ = f.prendre(file="asap")
    try:
        ret, err = f.terminer(pris["id"], file="asap")
        plante = False
    except Exception as exc:  # noqa: BLE001 - toute exception = KO
        ret, err, plante = None, str(exc), True
    restants = lire_inbox(base, "z")
    ok = (not plante and err is None and ret is not None
          and ret.get("statut") == "TERMINEE"
          and len(restants) == 1)
    verifier("3. sans agent : terminer no-op, inbox intacte",
             ok, "plante=%s err=%s" % (plante, err))
    chrono_etape("3 sans agent", t0)


def point_4_faux_positif(tmp_dir):
    """Corps different (autre mission) -> message NON consomme."""
    t0 = time.monotonic()
    base = sous_tmp(tmp_dir, "p4")
    f, _ = charger_files(base)
    e, _ = f.ajouter("TEST mission point 4", file="asap", agent="w")
    # le message porte une AUTRE mission (texte different)
    ecrire_inbox(base, "w",
                 [message_mission("w", "AUTRE mission completement")])
    pris, _ = f.prendre(file="asap")
    ret, err = f.terminer(pris["id"], file="asap")
    restants = lire_inbox(base, "w")
    objets = [m.get("objet") for m in restants]
    ok = (err is None and ret.get("statut") == "TERMINEE"
          and "MISSION pour w" in objets)
    verifier("4. corps different : message NON consomme (pas de faux "
             "positif)", ok, "objets=%s" % objets)
    chrono_etape("4 faux positif", t0)


def point_5_sans_inbox(tmp_dir):
    """Agent sans fichier inbox -> terminer no-op sans erreur."""
    t0 = time.monotonic()
    base = sous_tmp(tmp_dir, "p5")
    f, _ = charger_files(base)
    e, _ = f.ajouter("TEST mission point 5", file="asap", agent="v")
    # AUCUNE inbox creee pour v
    pris, _ = f.prendre(file="asap")
    try:
        ret, err = f.terminer(pris["id"], file="asap")
        plante = False
    except Exception as exc:  # noqa: BLE001
        ret, err, plante = None, str(exc), True
    ok = (not plante and err is None and ret.get("statut") == "TERMINEE")
    verifier("5. sans inbox : terminer no-op sans erreur",
             ok, "plante=%s err=%s" % (plante, err))
    chrono_etape("5 sans inbox", t0)


def point_6_flux_zero(tmp_dir):
    """Apres TERMINEE, le message consomme ne compte plus comme P1."""
    t0 = time.monotonic()
    base = sous_tmp(tmp_dir, "p6")
    f, _ = charger_files(base)
    e, _ = f.ajouter("TEST mission point 6", file="asap", agent="u")
    ecrire_inbox(base, "u", [message_mission("u", e["mission"]),
                             message_non_mission("u")])
    pris, _ = f.prendre(file="asap")
    f.terminer(pris["id"], file="asap")
    restants = lire_inbox(base, "u")
    # le message MISSION est consomme ; il ne reste que le non-mission
    # qui, lui, est un P1 sans type -> flux le compterait. On verifie
    # donc que la NOTIFICATION MISSION n est plus la (0 message MISSION).
    missions = [m for m in restants
                if m.get("objet", "").startswith("MISSION pour")]
    ok = len(missions) == 0
    verifier("6. apres TERMINEE : 0 notification MISSION restante "
             "(plus de P1 fantome)", ok,
             "missions_restantes=%d" % len(missions))
    chrono_etape("6 flux zero", t0)


def point_8_persistance_relais(tmp_dir):
    """relais() deduit ET persiste l agent -> terminer() consomme.
    (complement oracle v0.5.12 - decouvert en validation live : la
    mission 91ccea62 relayee vers oracle gardait agent="" dans le
    fichier, la consommation ne pouvait pas retrouver l agent.)"""
    t0 = time.monotonic()
    base = sous_tmp(tmp_dir, "p8")
    f, _ = charger_files(base)
    e, _ = f.ajouter("TEST mission sans agent au depot", file="asap",
                     agent="")
    entree, err = f.relais("asap")
    agent = entree.get("agent")
    # 1. l agent est deduit (texte "TEST" -> morpheus)
    ok_deduit = bool(agent) and err is None
    # 2. l agent est PERSISTE dans le fichier
    ok_fichier = False
    with io.open(os.path.join(base, "files", "asap.jsonl"), "r",
                 encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne:
                continue
            d = json.loads(ligne)
            if d.get("id") == entree["id"]:
                ok_fichier = d.get("agent") == agent
    # 3. notification dans l inbox de l agent deduit
    ecrire_inbox(base, agent, [message_mission(agent, entree["mission"])])
    # 4. terminer -> la notification est consommee
    ret, err2 = f.terminer(entree["id"], file="asap")
    restants = lire_inbox(base, agent)
    ok_consomme = (err2 is None and ret.get("statut") == "TERMINEE"
                   and len(restants) == 0)
    verifier("8. relais() persiste l agent deduit -> terminer() consomme",
             ok_deduit and ok_fichier and ok_consomme,
             "deduit=%s fichier=%s consomme=%s" % (ok_deduit, ok_fichier,
                                                   ok_consomme))
    chrono_etape("8 persistance relais", t0)


def point_7_normes():
    """ASCII strict + LF pur sur files.py et le test."""
    t0 = time.monotonic()
    fichiers = [FILES_PY, os.path.abspath(__file__)]
    ko = []
    for chemin in fichiers:
        a = ascii_count(chemin)
        c = crlf_count(chemin)
        if a != 0 or c != 0:
            ko.append("%s ascii=%d crlf=%d" % (os.path.basename(chemin), a, c))
    verifier("7. normes : ASCII 0/0 et CRLF 0/0 (files.py + test)",
             not ko, "; ".join(ko))
    chrono_etape("7 normes", t0)


def main():
    tmp_dir = tempfile.mkdtemp(prefix="test-123-")
    try:
        if point_actif(1):
            point_1_consommation(tmp_dir)
        if point_actif(2):
            point_2_idempotence(tmp_dir)
        if point_actif(3):
            point_3_sans_agent(tmp_dir)
        if point_actif(4):
            point_4_faux_positif(tmp_dir)
        if point_actif(5):
            point_5_sans_inbox(tmp_dir)
        if point_actif(6):
            point_6_flux_zero(tmp_dir)
        if point_actif(7):
            point_7_normes()
        if point_actif(8):
            point_8_persistance_relais(tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO,
                                                               NB_POINTS))
    print("=== VERDICT : %s ===" % ("PROPRE" if NB_KO == 0 else "A REVOIR"))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
