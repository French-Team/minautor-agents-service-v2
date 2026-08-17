#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-043-generateurs-quoter.py
GARDE-FOU ANTI-RECURRENCE : generateurs-commande doit quoter les parametres
declares `quoter: true` dans le catalogue (guillemets doubles + echappement),
sinon une valeur avec apostrophe/espaces casse la commande composee.

Contexte (2026-08-13) :
  - La regle anti-echappement des combos (combos-moteur.md v0.3.3) documente
    que {var} doit etre quote. La preuve reelle (mission apostrophe) a montre
    que generateurs-commande quote via composer_valeur (quoter:true ou espace
    -> guillemets doubles + echappement des \\ et ").
  - 5 parametres quoter:true dans le catalogue : activer-activer/raison,
    activer-reactiver/raison, remplacer-texte/paire1+paire2,
    remplir-pense-bete/contenu.
  - Demande utilisateur : un garde-fou verifie en permanence que
    generateurs-commande quote bien ces parametres - si le champ quoter est
    retire du catalogue ou si composer_valeur cesse de quoter, la
    non-regression le signale immediatement.

REGLE D AJOUT : tout NOUVEAU parametre declare `quoter: true` dans le
catalogue est verifie automatiquement (composer_valeur doit le quoter).

Invariants verifies :
  1. Les parametres quoter:true attendus sont presents dans le catalogue
  2. composer_valeur quote (guillemets doubles) quand quoter:true
  3. La valeur quotee resiste a shlex.split (1 argument intact, apostrophe
     comprise)
  4. composer_commande produit une commande shlex.split-able avec une raison
     a apostrophe (argument intact)
  5. Normes : ASCII strict + LF pur (catalogue + generateurs-commande + test)
Tags: outils, catalogue, generateurs, garde-fou
"""
import importlib.util
import io
import json
import os
import shlex
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
GENERATEUR = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                          "generateurs-commande.py")

# Parametres quoter:true attendus (regle d ajout : en ajouter ici)
PARAMS_QUOTER = [
    ("activer-activer", "raison"),
    ("activer-reactiver", "raison"),
    ("remplacer-texte", "paire1"),
    ("remplacer-texte", "paire2"),
    ("remplir-pense-bete", "contenu"),
]

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
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


def charger_generateur():
    """Importe generateurs-commande.py (garde __main__ present, sans effet)."""
    spec = importlib.util.spec_from_file_location("generateurs_commande", GENERATEUR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Test formel generateurs-quoter ===")
    try:
        catalogue = json.load(io.open(CATALOGUE, encoding="utf-8"))
        commandes = {c.get("nom"): c for c in catalogue.get("commandes", [])}
        gen = charger_generateur()

        # 1. Les parametres quoter:true attendus sont presents
        for nom, cle in PARAMS_QUOTER:
            cmd = commandes.get(nom)
            present = False
            if cmd:
                present = any(p.get("cle") == cle and p.get("quoter")
                              for p in cmd.get("parametres", []))
            verifier("1. %s/%s : quoter:true present" % (nom, cle), present)

        # 2. composer_valeur quote quand quoter:true (valeur avec apostrophe)
        RAISON = "reprise d'activation de la mission"
        param_quoter = {"cle": "raison", "quoter": True}
        valeur_quote = gen.composer_valeur(param_quoter, RAISON)
        verifier("2. composer_valeur quote (guillemets doubles)",
                 valeur_quote.startswith('"') and valeur_quote.endswith('"'),
                 "valeur=%s" % valeur_quote)

        # 3. La valeur quotee resiste a shlex.split (1 argument intact)
        try:
            args = shlex.split(valeur_quote)
            ok3 = len(args) == 1 and args[0] == RAISON
        except ValueError:
            ok3 = False
        verifier("3. shlex.split : raison intacte en 1 argument", ok3,
                 "args=%s" % (args if 'args' in dir() else "?"))

        # 4. composer_commande : commande complete avec raison a apostrophe
        cmd_reactiver = commandes.get("activer-reactiver")
        if cmd_reactiver:
            commande = gen.composer_commande(cmd_reactiver, {
                "session": "session-llm-1",
                "raison": RAISON,
                "agent": "Cerberus",
            })
            try:
                args_cmd = shlex.split(commande)
                raisons = [a for a in args_cmd if "activation" in a]
                ok4 = len(raisons) == 1 and raisons[0] == RAISON
            except ValueError:
                ok4 = False
            verifier("4. composer_commande : commande shlex.split-able, raison intacte",
                     ok4, "cmd=%s" % commande[:100])
        else:
            verifier("4. composer_commande : commande activer-reactiver", False,
                     "introuvable")

        # 5. Normes : ASCII strict + LF pur (catalogue + generateur + test)
        fichiers = [CATALOGUE, GENERATEUR, os.path.abspath(__file__)]
        total_non_ascii = sum(ascii_count(f) for f in fichiers if os.path.isfile(f))
        verifier("5. ASCII strict : 0 non-ASCII (catalogue + generateur + test)",
                 total_non_ascii == 0, "total=%d" % total_non_ascii)
        total_crlf = sum(crlf_count(f) for f in fichiers if os.path.isfile(f))
        verifier("6. LF pur : 0 CRLF (catalogue + generateur + test)",
                 total_crlf == 0, "total=%d" % total_crlf)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
