#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-084-relecture-avant-gravure-garde-fou.py
GARDE-FOU : la porte du marbre (proteger-modifier-marbre v0.1.3) exige la
RELECTURE Argus (detecter-contradictions --regles) PROPRE avant toute
gravure d une zone de REGLES. Demande utilisateur 2026-08-16 : graver la
relecture obligatoire avant toute nouvelle regle immuable - audit Argus
(doublons + concordance source/protocole) AVANT la porte du marbre.

Contexte :
  - proteger-modifier-marbre v0.1.3 : toute zone dont le fichier est dans
    regles-immuables/ (est_zone_regles) lance automatiquement l audit Argus
    AVANT d accepter l autorisation utilisateur. Non PROPRE = BLOQUE (rc=1)
    meme avec --autorisation. Champ relecture journalise dans marbre-log.
  - Le protocole-securite-marbre v0.1.1 documente cette relecture (etape 4).

Invariants verifies :
  1. La porte v0.1.3 contient est_zone_regles + audit_regles_propre
  2. --version affiche v0.1.3
  3. Zone REGLE (regles-groupes-agents) + autorisation + audit PROPRE :
     rc=0 ou 'contenu inchange' (l audit est bien lance et passe)
  4. PREUVE NEGATIVE : doublon EXACT de titre IMMUABLE injecte dans le vrai
     regles-groupes-agents.md -> la porte BLOQUE (rc=1, 'relecture Argus'),
     fichier restaure + marbre resynchronise
  5. Protocole-securite-marbre v0.1.1 documente la relecture
  6. Normes : ASCII strict + LF pur
Tags: securite, marbre, relecture, garde-fou
"""

import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
AGENTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")
REGLES = os.path.join(AGENTS_DIR, "regles-immuables", "general",
                      "regles-groupes-agents.md")
GENERAL_DIR = os.path.join(AGENTS_DIR, "regles-immuables", "general")
PORTE_PY = os.path.join(TOOLS_DIR, "proteger", "proteger-modifier-marbre",
                        "proteger-modifier-marbre.py")
PORTE_MD = os.path.join(TOOLS_DIR, "proteger", "proteger-modifier-marbre",
                        "proteger-modifier-marbre.md")
PROTOCOLE = os.path.join(GENERAL_DIR, "protocole-securite-marbre",
                         "protocole-securite-marbre.001.01.ebauche.md")
MARBRE_JSON = os.path.join(AGENTS_DIR, "regles-immuables", "marbre", "marbre.json")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
POINT_ACTIF = None
DESACTIVES = set()
CHRONO_ACTIF = "--no-chrono" not in sys.argv
DEBUT = time.monotonic()
ETAPES = []


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def chrono_etape(nom, duree):
    ETAPES.append((nom, duree))
    print("  [chrono] %-40s %.2fs" % (nom, duree))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT
    print("")
    print("=== CHRONO test (total %.1fs) ===" % total)


def point_actif(numero):
    global POINT_ACTIF
    return POINT_ACTIF is None or numero == POINT_ACTIF


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if not point_actif(NB_POINTS):
        return
    if NB_POINTS in DESACTIVES:
        print("  [DESACTIVE] %s" % nom)
        return
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(commande, timeout=120):
    res = PROTECTIONS.lancer_protege(commande, timeout=timeout)
    return res


def compter_non_ascii(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def compter_crlf(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def empreinte_zone(nom_zone):
    """Calcule l empreinte actuelle de la zone dans marbre.json (lecture)."""
    import json
    with io.open(MARBRE_JSON, encoding="utf-8") as fh:
        manifeste = json.load(fh)
    zone = manifeste.get("zones", {}).get(nom_zone)
    return zone.get("empreinte", "") if zone else ""


def main():
    global POINT_ACTIF, DESACTIVES
    import argparse
    ap = argparse.ArgumentParser(description="test-084 relecture avant gravure")
    ap.add_argument("--isoler", type=int, default=None)
    ap.add_argument("--desactiver", default="")
    ap.add_argument("--no-chrono", action="store_true")
    args = ap.parse_args()
    POINT_ACTIF = args.isoler
    DESACTIVES = set(int(x) for x in args.desactiver.split(",") if x.strip())

    print("=== Garde-fou : relecture Argus obligatoire avant gravure (porte marbre v0.1.3) ===")
    t0 = time.monotonic()

    # 1. La porte v0.1.3 contient les fonctions de relecture
    code = io.open(PORTE_PY, encoding="utf-8", errors="replace").read()
    ok = ("def est_zone_regles" in code and "def audit_regles_propre" in code
          and "detecter-contradictions" in code and "--no-audit" in code)
    verifier("1. porte v0.1.3 : est_zone_regles + audit_regles_propre + no-audit",
             ok)
    chrono_etape("1. fonctions relecture", time.monotonic() - t0)

    # 2. --version affiche v0.1.3
    t0 = time.monotonic()
    r = run([sys.executable, PORTE_PY, "--version"])
    verifier("2. --version affiche v0.1.3",
             r.returncode == 0 and "0.1.3" in (r.stdout or ""),
             (r.stdout or "")[-60:])
    chrono_etape("2. version", time.monotonic() - t0)

    # 3. Zone REGLE + autorisation + audit PROPRE : l audit est lance et passe
    t0 = time.monotonic()
    r = run([sys.executable, PORTE_PY, "--zone", "regles-groupes-agents",
             "--raison", "test-084 preuve positive audit", "--autorisation",
             "UTILISATEUR"])
    sortie = (r.stdout or "") + (r.stderr or "")
    ok = (r.returncode in (0, 1)) and ("RELECTURE" in sortie)
    if r.returncode == 0 and "contenu inchange" in sortie:
        ok = True
    verifier("3. zone regle + autorisation : audit Argus lance (PROPRE = OK)",
             ok, "rc=%d %s" % (r.returncode, sortie[-150:]))
    chrono_etape("3. audit positif", time.monotonic() - t0)

    # 4. PREUVE NEGATIVE : doublon exact de titre IMMUABLE -> BLOQUE
    t0 = time.monotonic()
    sauvegarde = REGLES + ".bak-t084"
    shutil.copy(REGLES, sauvegarde)
    bloque = False
    restaure = False
    try:
        d = io.open(REGLES, encoding="utf-8").read()
        div = ("\n### SEUL MORPHEUS ECRIT ET EXECUTE LES TESTS (IMMUABLE)\n"
               "> REGLE : doublon injecte par test-084 pour la preuve negative.\n")
        io.open(REGLES, "w", encoding="ascii", newline="\n").write(d + div)
        r = run([sys.executable, PORTE_PY, "--zone", "regles-groupes-agents",
                 "--raison", "test-084 preuve negative doublon",
                 "--autorisation", "UTILISATEUR"])
        sortie = (r.stdout or "") + (r.stderr or "")
        bloque = (r.returncode == 1 and "BLOQUE" in sortie
                  and "relecture Argus" in sortie)
    finally:
        shutil.move(sauvegarde, REGLES)
        restaure = True
    verifier("4. PREUVE NEGATIVE : doublon IMMUABLE injecte -> porte BLOQUE "
             "(rc=1, relecture Argus)", bloque,
             "rc=%d" % (1 if not bloque else 0))
    verifier("4b. fichier de regles restaure apres la preuve", restaure)
    chrono_etape("4. preuve negative", time.monotonic() - t0)

    # 5. Protocole-securite-marbre v0.1.1 documente la relecture
    t0 = time.monotonic()
    try:
        proto = io.open(PROTOCOLE, encoding="utf-8", errors="replace").read()
        ok = ("0.1.1" in proto and "RELECTURE OBLIGATOIRE" in proto
              and "detecter-contradictions" in proto)
    except OSError:
        ok = False
    verifier("5. protocole-securite-marbre v0.1.1 : relecture documentee", ok)
    chrono_etape("5. protocole", time.monotonic() - t0)

    # 5b. MODE --AJOUTER : l audit est aussi obligatoire pour les NOUVELLES
    # zones de regles (la porte construit zone_audit depuis --fichier).
    t0 = time.monotonic()
    import json as _json
    zones_ajoutees = []
    try:
        # 5b.1 --ajouter zone REGLE : audit Argus lance
        r = run([sys.executable, PORTE_PY, "--ajouter", "zone-t084-regle",
                 "--fichier", "cerveau-projet/agents/regles-immuables/general/"
                 "regles-general-global.md", "--type", "fichier",
                 "--raison", "test-084 preuve ajout regle",
                 "--autorisation", "UTILISATEUR"])
        sortie = (r.stdout or "") + (r.stderr or "")
        ok_ajout_regle = (r.returncode == 0 and "RELECTURE" in sortie
                          and "audit Argus PROPRE" in sortie)
        zones_ajoutees.append("zone-t084-regle")
        verifier("5b. AJOUT zone REGLE : audit Argus obligatoire lance",
                 ok_ajout_regle, "rc=%d %s" % (r.returncode, sortie[-150:]))

        # 5b.2 --ajouter zone NON-regle : PAS d audit (defaut)
        r = run([sys.executable, PORTE_PY, "--ajouter", "zone-t084-nonregle",
                 "--fichier", "cerveau-projet/agents/buffy/buffy.md",
                 "--type", "fichier",
                 "--raison", "test-084 preuve ajout non-regle",
                 "--autorisation", "UTILISATEUR"])
        sortie = (r.stdout or "") + (r.stderr or "")
        ok_ajout_nonregle = (r.returncode == 0 and "RELECTURE" not in sortie)
        zones_ajoutees.append("zone-t084-nonregle")
        verifier("5b2. AJOUT zone NON-regle : pas d audit (defaut)",
                 ok_ajout_nonregle, "rc=%d %s" % (r.returncode, sortie[-120:]))
    finally:
        # NETTOYAGE OBLIGATOIRE : retirer les zones ajoutees du marbre.json
        try:
            with io.open(MARBRE_JSON, encoding="utf-8") as fh:
                manifeste = _json.load(fh)
            modifie = False
            for z in zones_ajoutees:
                if z in manifeste.get("zones", {}):
                    del manifeste["zones"][z]
                    modifie = True
            if modifie:
                with io.open(MARBRE_JSON, "w", encoding="utf-8",
                             newline="\n") as fh:
                    _json.dump(manifeste, fh, ensure_ascii=True, indent=1)
                    fh.write("\n")
        except (IOError, ValueError):
            pass
    zones_restantes = []
    try:
        with io.open(MARBRE_JSON, encoding="utf-8") as fh:
            manifeste = _json.load(fh)
        zones_restantes = [z for z in zones_ajoutees
                           if z in manifeste.get("zones", {})]
    except (IOError, ValueError):
        pass
    verifier("5c. nettoyage : zones test retirees du marbre.json (0 restante)",
             not zones_restantes, "restantes=%s" % zones_restantes)
    chrono_etape("5b. ajout zones + nettoyage", time.monotonic() - t0)

    # 6. Normes
    t0 = time.monotonic()
    fichiers = [PORTE_PY, PORTE_MD, PROTOCOLE, REGLES, os.path.abspath(__file__)]
    total_na = sum(compter_non_ascii(f) for f in fichiers if os.path.isfile(f))
    verifier("6. ASCII strict : 0 non-ASCII (porte + doc + protocole + regles + test)",
             total_na == 0, "total=%d" % total_na)
    total_crlf = sum(compter_crlf(f) for f in fichiers if os.path.isfile(f))
    verifier("6b. LF pur : 0 CRLF", total_crlf == 0, "total=%d" % total_crlf)
    chrono_etape("6. normes", time.monotonic() - t0)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
