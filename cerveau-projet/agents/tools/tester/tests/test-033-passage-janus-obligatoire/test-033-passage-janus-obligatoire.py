#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-033-passage-janus-obligatoire.py
GARDE-FOU ANTI-RECURRENCE : la fin de mission de Morpheus passe OBLIGATOIREMENT
par Janus (lecon 2026-08-13, demande utilisateur).

Contexte (2026-08-13) :
  - L utilisateur a demande pourquoi Morpheus ne lancait plus Janus en fin de
    mission. Janus (controle croise) a identifie la cause racine : la carte de
    Morpheus etait CORRECTE (c10/c14 = FIN - Activer Janus, commande exacte
    activer session-llm-1 janus) mais les consignes des 3 missions recentes
    (chrono, pool workers, goulot test-028) portaient reactiver Cerberus au
    lieu de activer JANUS - Morpheus a suivi la consigne au lieu de SA carte
    (derive analogue au template : la carte est la reference, jamais la
    consigne). De plus la REGLE DELEGATION de la fiche portait la clause
    erronee Je ne reactive CERBERUS que si j ai ete active directement par
    Cerberus, qui contredisait la carte c14 (meme active directement, je passe
    par Janus).
  - Corrections : REGLE ABSOLUE -- PASSAGE PAR JANUS ajoutee a la fiche
    morpheus.md + clause erronee retiree de la REGLE DELEGATION.

Invariants verifies :
  1. Carte morpheus : la fin de mission est FIN - Activer Janus (c14 apres
     la refonte v0.5.8 ; c10 a ete fusionnee dans la chaine c14)
  2. Carte morpheus : c14 est une fin FIN - Activer Janus avec la commande
     exacte activer session-llm-1 janus et PAS reactiver dans le message
  3. Fiche morpheus : contient la REGLE ABSOLUE -- PASSAGE PAR JANUS
  4. Fiche morpheus : contient JAMAIS reactiver Cerberus directement
  5. Fiche morpheus : la REGLE DELEGATION ne porte plus la clause erronee
     Je ne reactive CERBERUS que si j ai ete active directement par Cerberus
  6. Normes : ASCII strict + LF pur (carte + fiche + test)
Tags: agents, janus, garde-fou, anti-recurrence
"""
import importlib.util
import io
import json
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

PARCOURS_MORPHEUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                 "morpheus", "parcours", "arbre-morpheus.json")
FICHE_MORPHEUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                              "morpheus", "morpheus.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


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


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-033 : passage obligatoire par Janus (Morpheus) ===")
    try:
        with io.open(PARCOURS_MORPHEUS, encoding="utf-8") as fh:
            arbre = json.load(fh)
        dossier = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                               "morpheus", "parcours")
        # Modele aero v2 : les fins sont centralisees dans fins.json et vont
        # vers ORACLE (l aeroport) - jamais Cerberus, jamais un autre agent.
        fichier_fins = arbre.get("fins", {}).get("fichier", "fins.json")
        chemin_fins = os.path.join(dossier, fichier_fins)
        with io.open(chemin_fins, encoding="utf-8") as fh:
            donnees_fins = json.load(fh)
        fins = donnees_fins.get("fins", {})

        # 1. Au moins une fin reactiver vers ORACLE existe (fin de mission)
        fins_oracle = [nom for nom, f in fins.items()
                       if f.get("action") == "reactiver"
                       and f.get("cible") == "oracle"]
        verifier("1. fins.json a au moins une fin reactiver vers ORACLE",
                 len(fins_oracle) >= 1, "fins=%s" % fins_oracle)

        # 2-3. Chaque fin reactiver porte reactiver-fin <agent> --cible oracle
        msg_ok = True
        msg_ko = []
        for nom, f in fins.items():
            if f.get("action") != "reactiver":
                continue
            cmd = f.get("commande", "")
            if "reactiver-fin morpheus" not in cmd or "--cible oracle" not in cmd:
                msg_ok = False
                msg_ko.append(nom)
        verifier("2. fins reactiver portent reactiver-fin morpheus --cible oracle",
                 msg_ok, "ko=%s" % msg_ko)

        # 4. Aucune fin ne reactiver Cerberus ni n active un agent directement
        commande_reactiver = False
        for nom, f in fins.items():
            cmd = f.get("commande", "") + " " + f.get("description", "")
            if "reactiver cerberus" in cmd.lower() \
                    or "--cible cerberus" in cmd.lower() \
                    or "reactiver <session>" in cmd:
                commande_reactiver = True
        verifier("4. aucune fin ne reactiver Cerberus directement (modele aero)",
                 not commande_reactiver, "")

        with io.open(FICHE_MORPHEUS, encoding="utf-8", errors="replace") as fh:
            fiche = fh.read()

        # 5. REGLE ABSOLUE -- PASSAGE PAR JANUS presente
        verifier("5. fiche : REGLE ABSOLUE -- PASSAGE PAR JANUS presente",
                 "REGLE ABSOLUE -- PASSAGE PAR JANUS" in fiche, "")

        # 6. la regle interdit reactiver Cerberus directement
        verifier("6. fiche : JAMAIS reactiver Cerberus directement",
                 "JAMAIS reactiver Cerberus directement" in fiche, "")

        # 7. la clause erronee est retiree de la REGLE DELEGATION
        clause_erronee = ("Je ne reactive CERBERUS que si j ai ete active "
                          "directement par Cerberus")
        verifier("7. REGLE DELEGATION sans la clause erronee (reactiver direct)",
                 clause_erronee not in fiche, "")
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    # 8-9. Normes ASCII strict + LF pur (fins.json + fiche + test)
    fichiers = [os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                             "morpheus", "parcours", "fins.json"),
                FICHE_MORPHEUS, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("8. ASCII strict : 0 non-ASCII (carte + fiche + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("9. LF pur : 0 CRLF (carte + fiche + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
