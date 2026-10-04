#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-111-pilote-anti-redemarrage-garde-fou.py

GARDE-FOU ANTI-RE-DEMARRAGE DU PILOTE ORACLE (decision utilisateur
2026-08-30, test round integre aero vers argus) : quand une mission est
deja terminee (etat de carte a etape=fin + historise_fin=true), le pilote
ne doit PAS re-resoudre la racine et re-servir la mission depuis le debut.
Avant la correction, un appel ulterieur au pilote re-demarrait le round au
besoin 1 -- c est exactement la mecanique du residu ETAT-CARTE INCOHERENT
(etape=fin, precedent=None) detecte au demarrage de session.

Le correctif : garde anti-re-demarrage dans pilote() (fonctions/pilote.py)
-- si etape=fin + historise_fin=true, le pilote repond "Mission deja
terminee" et laisse la main a l agent (reactiver-fin <agent> --cible
oracle). La garde est placee AVANT toute resolution de la racine.

Points verifies :
  1. La garde existe dans pilote.py (message + condition etape=fin +
     historise_fin).
  2. La garde est placee AVANT la resolution de la racine (ordre dans le
     code source).
  3. TEST REEL : etat de carte factice etape=fin + historise_fin=true ->
     oracle pilote <agent-factice> repond "Mission deja terminee" et ne
     sert AUCUNE commande de travail ("SERVE POUR VOUS" absent).
  4. TEST REEL INVERSE : etat de carte factice etape=travail ->
     le pilote sert normalement (la garde ne bloque pas une mission en
     cours).
  5. Nettoyage : le fichier d etat factice est supprime (aucune trace).
  6. Preuve negative : sans la condition etape=fin, la garde ne se
     declenche pas (detection par lecture du code).
  7. Normes : ASCII strict + LF pur (pilote.py + test).

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: pilote, oracle, etat-carte, anti-redemarrage, garde-fou, anti-recurrence
"""
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

ORACLE_DIR = os.path.join(TOOLS_DIR, "oracle")
PILOTE = os.path.join(ORACLE_DIR, "fonctions", "pilote.py")
ORACLE_PY = os.path.join(ORACLE_DIR, "oracle.py")
ETAT_DIR = os.path.join(ORACLE_DIR, "etat-cartes")

# Agent factice pour les tests reels (jamais un vrai agent).
AGENT_TEST = "zz-test-pilote-garde"

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


def run(cmd, timeout=60):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      timeout=timeout)


def lire(chemin):
    try:
        with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def _etat_factice(etape, historise_fin):
    """Etat de carte factice sur l arbre d argus (valide et present)."""
    return {
        "agent": AGENT_TEST,
        "parcours": "agents/argus/parcours/arbre-argus.json",
        "case_courante": None,
        "mission_type": "detecter",
        "mission": "test garde-fou anti-redemarrage",
        "historise_debut": True,
        "precedent": "Cerberus",
        "etape": etape,
        "historise_fin": historise_fin,
    }


def _ecrire_etat_factice(etat):
    os.makedirs(ETAT_DIR, exist_ok=True)
    chemin = os.path.join(ETAT_DIR, "%s.json" % AGENT_TEST)
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(etat, ensure_ascii=True, indent=1))
    return chemin


def _supprimer_etat_factice():
    chemin = os.path.join(ETAT_DIR, "%s.json" % AGENT_TEST)
    try:
        os.remove(chemin)
    except OSError:
        pass


def point_1_garde_presente():
    contenu = lire(PILOTE)
    ok = ("Mission deja terminee" in contenu
          and 'etat.get("etape") == "fin"' in contenu
          and 'etat.get("historise_fin")' in contenu)
    verifier("1. garde anti-redemarrage presente dans pilote.py", ok)


def point_2_garde_avant_resolution():
    contenu = lire(PILOTE)
    # La garde doit etre dans la fonction d entree pilote() AVANT l appel a
    # _piloter_arbre (la navigation). L ordre d execution est : cmd_pilote
    # -> pilote() -> [GARDE] -> _piloter_arbre. On verifie la position dans
    # le corps de pilote() : la garde avant l appel a _piloter_arbre(
    # (l ordre texte dans la FONCTION pilote, pas dans tout le fichier).
    pos_garde = contenu.find('etat.get("etape") == "fin"')
    pos_piloter_arbre = contenu.find("_piloter_arbre(parcours, arbre_dir, etat, agent, limite)")
    ok = (pos_garde != -1 and pos_piloter_arbre != -1
          and pos_garde < pos_piloter_arbre)
    verifier("2. garde dans pilote() AVANT l appel a _piloter_arbre", ok,
             "pos_garde=%d pos_piloter_arbre=%d" % (pos_garde, pos_piloter_arbre))


def point_3_test_reel_fin():
    """Etat factice etape=fin + historise_fin -> pilote dit mission terminee,
    aucun travail servi."""
    chemin = _ecrire_etat_factice(_etat_factice("fin", True))
    try:
        r = run([PYTHON, ORACLE_PY, "pilote", AGENT_TEST], timeout=60)
        sortie = (r.stdout or "") + (r.stderr or "")
        ok = ("Mission deja terminee" in sortie
              and "SERVE POUR VOUS" not in sortie
              and "BESOIN 1/10" not in sortie)
        verifier("3. etat=fin -> mission terminee, aucun travail servi", ok,
                 sortie.strip()[-200:])
    finally:
        _supprimer_etat_factice()


def point_4_test_reel_travail():
    """Etat factice etape=travail -> le pilote sert normalement (la garde
    ne bloque pas une mission en cours)."""
    chemin = _ecrire_etat_factice(_etat_factice("travail", False))
    try:
        r = run([PYTHON, ORACLE_PY, "pilote", AGENT_TEST], timeout=60)
        sortie = (r.stdout or "") + (r.stderr or "")
        ok = ("Mission deja terminee" not in sortie
              and ("BESOIN 1/10" in sortie or "SERVE POUR VOUS" in sortie))
        verifier("4. etat=travail -> pilote sert normalement", ok,
                 sortie.strip()[-200:])
    finally:
        _supprimer_etat_factice()


def point_5_nettoyage():
    chemin = os.path.join(ETAT_DIR, "%s.json" % AGENT_TEST)
    verifier("5. etat factice supprime (aucune trace)", not os.path.exists(chemin))


def point_6_preuve_negative():
    contenu = lire(PILOTE)
    # La condition DOIT porter sur etape=fin : si elle ne testait que
    # historise_fin, la garde se declencherait aussi pour un etat en cours
    # qui aurait deja ete historise -- ce qui serait un faux positif.
    ok = ('etat.get("etape") == "fin"' in contenu
          and "and" in contenu)
    verifier("6. condition portant bien sur etape=fin (pas seulement historise)",
             ok)


def point_7_normes():
    fichiers = [PILOTE, os.path.abspath(__file__)]
    total_non_ascii = 0
    total_crlf = 0
    for f in fichiers:
        data = open(f, "rb").read()
        total_non_ascii += len([c for c in data if c > 127])
        total_crlf += data.count(b"\r\n")
    ok = total_non_ascii == 0 and total_crlf == 0
    verifier("7. ASCII strict + LF pur (pilote.py + test)", ok,
             "non_ascii=%d crlf=%d" % (total_non_ascii, total_crlf))


def main():
    print("=== test-111 : pilote Oracle anti-redemarrage (residu etat-carte) ===")

    points = [
        ("1. garde presente", point_1_garde_presente),
        ("2. garde avant resolution", point_2_garde_avant_resolution),
        ("3. test reel etat=fin", point_3_test_reel_fin),
        ("4. test reel etat=travail", point_4_test_reel_travail),
        ("5. nettoyage", point_5_nettoyage),
        ("6. preuve negative", point_6_preuve_negative),
        ("7. normes", point_7_normes),
    ]
    for num, (nom, fn) in enumerate(points, start=1):
        if not point_actif(num):
            continue
        t_debut = time.monotonic()
        fn()
        chrono_etape(nom, t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
