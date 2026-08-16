#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-078-amelioration-checklist-obligatoire.py
GARDE-FOU : TOUTE activation d amelioration (mission dont la raison
contient un motif d amelioration) DOIT etre precedee d un passage par
generateurs-amelioration (Pattern 17, cases c19c/c1b de la carte
cerberus : GENERATEUR D ABORD - la checklist AVANT d activer l agent).

Contexte (2026-08-16, controle Cerberus) :
  - Le round d amelioration de detecter-troncatures a active Vulcain a
    15:03 SANS generateurs-amelioration : le registre ne contenait aucune
    entree de l outil, la declaration n a ete faite qu a 15:22 (APRES
    l activation, a posteriori). C est la derive que ce garde-fou doit
    empecher de revenir.
  - test-008 couvre l OUTIL (version, parite, structure, themes) mais PAS
    la regle de PROCESSUS : une activation d amelioration doit etre
    precedee d un usage generateurs-amelioration declare au registre.

Regle verifiee (croisement AGENTS-historique.md x registre-usages-outils) :
  - Pour chaque ligne d AGENTS-historique dont la raison contient un motif
    d amelioration (ROUND D AMELIORATION, AMELIORER, AMELIORATION,
    ameliorer, round amelioration), il DOIT exister une entree
    generateurs-amelioration au registre avec un timestamp <= celui de
    l activation (comparaison MINUTE-LEVEL : une declaration faite a
    posteriori le meme jour ne compte pas).
  - Le passe AVANT la creation du garde-fou (avant 2026-08-17) est
    documente comme ECART HISTORIQUE (liste), pas KO bloquant : seule la
    derive FUTURE (a partir de 2026-08-17) est KO.
  - PREUVE NEGATIVE : injecter une ligne d activation fictive (veille de
    la premiere declaration) sans declaration registre -> l ecart est
    detecte.

Invariants verifies :
  1. Le registre contient au moins une entree generateurs-amelioration.
  2. Les activations d amelioration FUTURES (date >= reference) ont toutes
     une declaration generateurs-amelioration <= date d activation.
  3. Les activations d amelioration PASSEES sont listees comme ecarts
     historiques documentes (le round detecter-troncatures 15:03 y figure,
     la declaration 15:22 etant posterieure).
  4. PREUVE NEGATIVE : une activation fictive sans declaration registre
     avant elle est detectee comme ecart (KO si elle n etait pas detectee).
  5. Normes : ASCII strict + LF pur (test + sources).
"""
import datetime
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

HISTORIQUE = os.path.join(PROJECT_ROOT, "AGENTS-historique.md")
REGISTRE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces",
                        "registre-usages-outils.jsonl")

# Motifs d amelioration dans la raison d une activation
MOTIFS_AMELIORATION = (
    "ROUND D AMELIORATION", "AMELIORER", "AMELIORATION",
    "ameliorer", "round amelioration",
)

# Date de reference : lendemain de la creation du garde-fou (2026-08-16).
# Les activations AVANT cette date (dont le round detecter-troncatures
# 15:03, sans checklist) sont des ecarts HISTORIQUES documentes (pas KO
# bloquant). Seule la derive FUTURE (a partir du 2026-08-17) est KO.
DATE_REFERENCE = "2026-08-17"

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 7


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-078 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, str(detail)[-100:]))


def charger_protections():
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                          "tester", "tester-protections", "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def lire(chemin):
    if not os.path.exists(chemin):
        return ""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def dates_generateurs_amelioration(registre):
    """Dates des entrees generateurs-amelioration au registre (listes de
    'YYYY-MM-DD HH:MM:SS' triees)."""
    dates = []
    if not os.path.exists(registre):
        return dates
    for ligne in io.open(registre, encoding="utf-8", errors="replace"):
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            e = json.loads(ligne)
        except ValueError:
            continue
        if e.get("outil") == "generateurs-amelioration":
            d = e.get("date", "")
            if d:
                dates.append(d)
    return sorted(dates)


def activations_amelioration(texte_historique):
    """Lignes d AGENTS-historique dont la raison contient un motif
    d amelioration. Retourne [(date, agent, raison_complete)].
    Le parametre est le TEXTE (deja lu), pas le chemin."""
    resultats = []
    for ligne in texte_historique.splitlines():
        if not any(m in ligne.upper() for m in
                   ("ROUND D AMELIORATION", "AMELIORER", "AMELIORATION",
                    "ROUND AMELIORATION")):
            continue
        m = re.match(r"\|\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s+[0-9:]+\s*\|"
                     r"\s*[^|]+\|\s*([a-zA-Z-]+)\s*\|", ligne)
        if not m:
            continue
        date = m.group(1)
        agent = m.group(2).strip()
        # l agent Cerberus (bilan/reactivation) n est pas une activation
        # de mission d amelioration : ignorer les lignes Cerberus/BILAN.
        if agent.lower() == "cerberus" and ("BILAN" in ligne or "TERMINE" in ligne):
            continue
        resultats.append((date, agent, ligne.strip()))
    return resultats


def decl_avant(date_activation, dates_decl):
    """True si une declaration generateurs-amelioration existe AVANT (ou a
    la meme minute) que l activation. Comparaison du TIMESTAMP COMPLET
    (minute pres), pas seulement du jour : sinon une declaration faite
    a posteriori le meme jour (ex 15:22 pour une activation 15:03)
    masquerait l ecart."""
    act = date_activation[:16]
    return any(d[:16] <= act for d in dates_decl)


def main():
    print("=== Garde-fou : generateurs-amelioration avant chaque activation d amelioration ===")

    # 1. Le registre contient au moins une entree generateurs-amelioration
    t0 = time.monotonic()
    dates = dates_generateurs_amelioration(REGISTRE)
    verifier("1. registre : au moins une entree generateurs-amelioration",
             len(dates) > 0, "nb=%d" % len(dates))
    chrono_etape("1. registre", t0)

    # 2. Liste des activations d amelioration (toutes, passees + futures)
    t0 = time.monotonic()
    activations = activations_amelioration(lire(HISTORIQUE))
    verifier("2. activations d amelioration trouv\u00e9es dans l historique (>= 1)",
             len(activations) >= 1, "nb=%d" % len(activations))
    chrono_etape("2. historique", t0)

    # 3. FUTUR : chaque activation >= DATE_REFERENCE a une declaration <= date
    t0 = time.monotonic()
    ecarts_futurs = []
    for date, agent, ligne in activations:
        if date < DATE_REFERENCE:
            continue
        if not decl_avant(date, dates):
            ecarts_futurs.append("%s %s %s" % (date, agent, ligne[:60]))
    verifier("3. activations d amelioration FUTURES precedees de generateurs-amelioration",
             not ecarts_futurs, "ecarts=%s" % ecarts_futurs[:3])
    chrono_etape("3. futur", t0)

    # 4. PASSE : les activations < DATE_REFERENCE sans declaration sont des
    #    ecarts HISTORIQUES documentes (le round detecter-troncatures 15:03
    #    doit y figurer) - liste attendue, pas KO bloquant.
    t0 = time.monotonic()
    ecarts_historiques = []
    for date, agent, ligne in activations:
        if date >= DATE_REFERENCE:
            continue
        if not decl_avant(date, dates):
            ecarts_historiques.append("%s %s" % (date, agent))
    verifier("4. ecart historique documente : activation detecter-troncatures 15:03 sans checklist",
             any("2026-08-16" in e and "vulcain" in e for e in ecarts_historiques),
             "historiques=%s" % ecarts_historiques[:5])
    chrono_etape("4. passe", t0)

    # 5. PREUVE NEGATIVE : injecter une activation fictive SANS declaration
    #    registre avant elle -> elle doit etre detectee comme ecart. La date
    #    fictive est la VEILLE de la premiere declaration generateurs-
    #    amelioration (aucune declaration ne peut exister avant) : le
    #    croisement decl_avant doit etre False -> l ecart est detecte.
    t0 = time.monotonic()
    tmp = tempfile.mkdtemp(prefix="tmp-test078-")
    try:
        hist_fictif = os.path.join(tmp, "historique.md")
        premiere = datetime.datetime.strptime(min(dates)[:10], "%Y-%m-%d")
        date_fictive = (premiere - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        ligne_fictive = ("| %s 12:00 | session-llm-1 | vulcain | "
                         "MISSION TEST-078 FICTIVE : ROUND D AMELIORATION "
                         "d un outil fictif sans checklist |" % date_fictive)
        with io.open(hist_fictif, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(hist_fictif_reel(hist_fictif, ligne_fictive))
        act_fictives = activations_amelioration(lire(hist_fictif))
        detectee = any(a[0] == date_fictive and "TEST-078" in a[2]
                       for a in act_fictives)
        # croisement registre : aucune declaration le jour de la veille
        # -> si l activation a ete extraite, elle est un ecart (KO si non).
        verifier("5. preuve negative : activation fictive detectee comme ecart",
                 detectee and not decl_avant(date_fictive, dates),
                 "detectee=%s decl=%s" % (detectee, decl_avant(date_fictive, dates)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    chrono_etape("5. preuve negative", t0)

    # 6. Normes ASCII + LF (test + historique + registre)
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    for f in [os.path.abspath(__file__), HISTORIQUE, REGISTRE]:
        if not os.path.exists(f):
            continue
        d = io.open(f, encoding="utf-8", errors="replace").read()
        na_total += sum(1 for ch in d if ord(ch) > 127)
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("6. normes : 0 non-ASCII (test + sources)",
             na_total == 0, "non-ascii=%d" % na_total)
    verifier("6b. normes : 0 CRLF (test + sources)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("6. normes", t0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % (
        "PROPRE (checklist amelioration verrouillee)" if NB_KO == 0 else "KO A CORRIGER"))
    return 0 if NB_KO == 0 else 1


def hist_fictif_reel(chemin, ligne_fictive):
    """Historique fictif minimal (la ligne fictive suffit)."""
    return ligne_fictive + "\n"


if __name__ == "__main__":
    sys.exit(main())
