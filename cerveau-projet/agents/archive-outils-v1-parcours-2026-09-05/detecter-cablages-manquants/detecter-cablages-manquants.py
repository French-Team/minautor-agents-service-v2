#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-cablages-manquants.py
#
# Verifie le cablage d'une carte de decision (parcours JSON) : detecte les
# cablages manquants qui echappent a valider-case (qui ne verifie QUE les fins
# non joignables). Cet outil detecte :
#
#   1. CASE_DEPART        : manquante ou inexistante dans les cases
#   2. FINS NON JOIGNABLES: une case de type 'fin' jamais atteignable depuis
#                           la case de depart (BFS anti-boucle)
#   3. CASES ORPHELINES    : TOUTE case (pas seulement les fins) jamais
#                           atteignable depuis la case de depart - le maillon
#                           manquant du bug des questions Ameliorations
#                           orphelines (vulcain c9b/c15b)
#   4. BOUCLES INDIRECTES : cycle entre 2+ cases (ex c22 -> c9b -> c22).
#                           Les boucles directes de re-essai (controle NON ->
#                           soi-meme) sont voulues et NON signalees.
#   5. REFERENCES MORTES   : champ 'suivant' ou branche 'vers' pointant vers
#                           une case inexistante
#
# Usage :
#   python3 detecter-cablages-manquants.py <chemin-parcours.json> [autres...]
#   python3 detecter-cablages-manquants.py --tous
#   python3 detecter-cablages-manquants.py --tous --rapport rapport.md --verbose
#
# Options :
#   --tous              : scanne tous les parcours de cerveau-projet/agents/*/parcours/
#   --rapport <fichier> : ecrit le rapport markdown
#   --verbose           : detail des graphes (depart, cases atteignables)
#   --version
#
# Version : 0.1.2
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (detecter-).
# =============================================================================
"""
detecter-cablages-manquants.py
detecter-cablages-manquants

Usage:
  detecter-cablages-manquants.py [OPTIONS]
"""

import argparse
import glob
import io
import json
import os
import subprocess
import sys
from datetime import datetime

VERSION = "0.1.2"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[0;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte, _COULEURS["neutre"])


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def verrouiller_habilitation(agent, outil):
    """Verrou d habilitation + auto-journalisation : appele
    proteger-verrou-habilitation et retourne (code, message).
    Code 0 = habilite (usage journalise en mode verrou-auto), 1 = bloque,
    2 = erreur. L outil signale LUI-MEME son usage (espionnage)."""
    racine = racine_projet()
    verrou = os.path.join(
        racine, "cerveau-projet", "agents", "tools", "proteger",
        "proteger-verrou-habilitation", "proteger-verrou-habilitation.py")
    if not os.path.isfile(verrou):
        return (2, "[ERREUR] Verrou introuvable : %s" % verrou)
    r = subprocess.run(
        [sys.executable, verrou, "--agent", agent, "--outil", outil],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    message = (r.stdout + r.stderr).strip()
    return (r.returncode, message)


def charger_parcours(chemin):
    """Charge un parcours JSON et retourne (parcours, nom, erreur)."""
    try:
        with io.open(chemin, encoding="utf-8", newline="") as fh:
            data = json.load(fh)
    except Exception as e:
        return None, os.path.basename(chemin), "JSON invalide : %s" % e
    nom = data.get("parcours", {}).get("nom", os.path.basename(chemin))
    return data, nom, None


def cases_atteignables(cases, depart):
    """BFS anti-boucle : ids de cases atteignables depuis depart."""
    if not depart or depart not in cases:
        return set()
    atteintes = set()
    file = [depart]
    while file:
        cid = file.pop(0)
        if cid in atteintes:
            continue
        atteintes.add(cid)
        case = cases[cid]
        suivant = case.get("suivant")
        if suivant and suivant in cases:
            file.append(suivant)
        for b in case.get("branches", []):
            vers = b.get("vers")
            if vers and vers in cases:
                file.append(vers)
    return atteintes


def successeurs(cases, cid):
    """Ids des cases cibles atteintes depuis cid (suivant + branches)."""
    c = cases.get(cid, {})
    res = []
    if c.get("suivant") and c["suivant"] in cases:
        res.append(c["suivant"])
    for b in c.get("branches", []):
        if b.get("vers") and b["vers"] in cases:
            res.append(b["vers"])
    return res


def trouver_cycles(cases, depart):
    """DFS : cycles impliquant 2+ cases distinctes (exclut les boucles
    directes de re-essai NON -> soi-meme qui sont voulues).
    Retourne une liste de cycles (liste de ids)."""
    cycles = []

    def dfs(noeud, pile, vu):
        if noeud not in cases:
            return
        if noeud in pile:
            idx = pile.index(noeud)
            cycle = pile[idx:]
            if len(set(cycle)) >= 2:
                sig = tuple(sorted(set(cycle)))
                if sig not in vu:
                    vu.add(sig)
                    cycles.append(cycle[:])
            return
        pile.append(noeud)
        for s in successeurs(cases, noeud):
            dfs(s, pile, vu)
        pile.pop()

    vu = set()
    if depart and depart in cases:
        dfs(depart, [], vu)
    return cycles


def cycle_a_sortie(cases, cycle):
    """Un cycle a-t-il une sortie ? Vrai si une case du cycle pointe vers
    une case hors du cycle (boucle de re-travail legitime : NON -> recommencer
    puis sortie par OUI). Faux = boucle bloquante sans issue."""
    ensemble = set(cycle)
    for cid in ensemble:
        for s in successeurs(cases, cid):
            if s not in ensemble:
                return True
    return False


def verifier_parcours(chemin, verbose=False):
    """Verifie un parcours : retourne (nom, problemes, avertissements, info)."""
    data, nom, err = charger_parcours(chemin)
    if err:
        return nom, [("CHARGEMENT", err)], [], {}
    cases = data.get("cases", {})
    depart = data.get("parcours", {}).get("case_depart")
    problemes = []
    avertissements = []

    # 1. case_depart
    if not depart:
        problemes.append(("CASE_DEPART", "case_depart manquante dans le parcours"))
    elif depart not in cases:
        problemes.append(("CASE_DEPART", "case_depart '%s' inexistante" % depart))

    atteignables = cases_atteignables(cases, depart)
    total = len(cases)

    # 2. fins non joignables
    for cid, case in cases.items():
        if case.get("type") == "fin" and cid not in atteignables:
            problemes.append(("FIN_NON_JOIGNABLE",
                              "fin '%s' non joignable depuis la case de depart" % cid))

    # 3. cases orphelines (toute case, pas seulement les fins)
    for cid in sorted(cases):
        if cid not in atteignables:
            problemes.append(("CAS_ORPHELINE",
                              "case '%s' jamais atteignable depuis la case de depart" % cid))

    # 4. boucles indirectes (2+ cases)
    for cycle in trouver_cycles(cases, depart):
        if cycle_a_sortie(cases, cycle):
            avertissements.append(("BOUCLE_RE_TRAVAIL",
                                   "cycle de re-travail (sortie existante) : %s" % " -> ".join(cycle)))
        else:
            problemes.append(("BOUCLE_BLOQUANTE",
                              "cycle SANS sortie : %s" % " -> ".join(cycle)))

    # 4b. boucle directe via 'suivant' vers soi-meme (toujours bloquante :
    #     pas de re-essai possible, contrairement a une branche NON -> soi-meme)
    for cid, case in cases.items():
        if case.get("suivant") == cid:
            problemes.append(("BOUCLE_BLOQUANTE",
                              "case '%s' : suivant pointe vers elle-meme (aucune sortie possible)" % cid))

    # 5. references mortes (suivant / branches.vers)
    for cid, case in cases.items():
        suivant = case.get("suivant")
        if suivant and suivant not in cases:
            problemes.append(("REF_MORTE",
                              "case '%s' : suivant '%s' inexistant" % (cid, suivant)))
        for b in case.get("branches", []):
            vers = b.get("vers")
            if vers and vers not in cases:
                problemes.append(("REF_MORTE",
                                  "case '%s' : branche '%s' -> '%s' inexistant" % (cid, b.get("reponse", "?"), vers)))

    info = {"total": total, "atteignables": len(atteignables), "depart": depart or "ABSENT"}
    return nom, problemes, avertissements, info


def main():
    parser = argparse.ArgumentParser(
        description="Verifie le cablage des cartes de decision (cases orphelines, boucles indirectes, references mortes, fins non joignables)")
    parser.add_argument("parcours", nargs="*", help="Chemins des parcours JSON a verifier (ou rien avec --tous)")
    parser.add_argument("--agent", type=str, required=True, help="Agent appelant (obligatoire pour le verrou)")
    parser.add_argument("--tous", action="store_true", help="Scanne tous les parcours de cerveau-projet/agents/*/parcours/")
    parser.add_argument("--rapport", type=str, default="", help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--verbose", action="store_true", help="Detail des graphes")
    parser.add_argument("--version", action="version",
                        version="detecter-cablages-manquants v%s" % VERSION)
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    # VERROU AUTO-JOURNALISATION (v0.1.2) : l outil signale LUI-MEME son usage
    # (autorise -> registre mode verrou-auto ; non autorise -> bloque).
    code_verrou, msg_verrou = verrouiller_habilitation(args.agent, "detecter-cablages-manquants")
    if code_verrou != 0:
        print(_couleur(msg_verrou, "rouge"))
        return code_verrou

    racine = racine_projet()
    chemins = list(args.parcours)
    if args.tous:
        pattern = os.path.join(racine, "cerveau-projet", "agents", "*", "parcours", "parcours-*.json")
        chemins = sorted(glob.glob(pattern))
    if not chemins:
        parser.print_help()
        return 2

    print(_couleur("=== Detecter les cablages manquants des parcours ===", "bleu"))
    print("  %d parcours a verifier" % len(chemins))
    print("")

    tous_problemes = []
    tous_avertissements = []
    lignes_rapport = []
    for chemin in chemins:
        nom, problemes, avertissements, info = verifier_parcours(chemin, verbose=args.verbose)
        print(_couleur("--- %s ---" % nom, "jaune"))
        if args.verbose:
            print("  depart: %s | cases: %d | atteignables: %d" % (
                info["depart"], info["total"], info["atteignables"]))
        if not problemes and not avertissements:
            print(_couleur("  OK : cablage correct (%d cases, %d atteignables)" % (
                info["total"], info["atteignables"]), "vert"))
        else:
            for typ, msg in problemes:
                print("  [%s] %s" % (_couleur(typ, "rouge"), msg))
            for typ, msg in avertissements:
                print("  [%s] %s" % (_couleur(typ, "jaune"), msg))
            if problemes:
                print(_couleur("  KO : %d probleme(s) bloquant(s) + %d avertissement(s)" % (len(problemes), len(avertissements)), "rouge"))
            else:
                print(_couleur("  AVERTISSEMENT : %d boucle(s) de re-travail (verifier si voulu)" % len(avertissements), "jaune"))
        tous_problemes.append((nom, problemes))
        tous_avertissements.append((nom, avertissements))
        lignes_rapport.append((nom, problemes, avertissements, info))

    total_global = sum(len(p) for _, p in tous_problemes)
    total_av = sum(len(a) for _, a in tous_avertissements)
    print("")
    verdict = "PROPRE" if total_global == 0 else "%d PROBLEME(S) BLOQUANT(S) DETECTE(S)" % total_global
    suffixe = " (%d boucle(s) de re-travail a verifier)" % total_av if total_av else ""
    print(_couleur("  Verdict global : %s sur %d parcours%s" % (verdict, len(chemins), suffixe),
                   "vert" if total_global == 0 else "rouge"))

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Rapport : cablages manquants des parcours\n\n")
            fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fh.write("Parcours verifies : %d\n" % len(chemins))
            fh.write("Problemes bloquants : %d\n" % total_global)
            fh.write("Boucles de re-travail : %d\n\n" % total_av)
            for nom, problemes, avertissements, info in lignes_rapport:
                fh.write("## %s (cases %d, atteignables %d)\n\n" % (nom, info["total"], info["atteignables"]))
                if problemes:
                    for typ, msg in problemes:
                        fh.write("- **[%s]** %s\n" % (typ, msg))
                if avertissements:
                    for typ, msg in avertissements:
                        fh.write("- _[%s]_ %s\n" % (typ, msg))
                if not problemes and not avertissements:
                    fh.write("- OK : cablage correct\n")
                fh.write("\n")
            fh.write("Verdict : %s\n" % verdict)
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))

    return 1 if total_global else 0


if __name__ == "__main__":
    sys.exit(main())
