#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
super-pilote.py - SUPER-PILOTE cote Oracle (agent + serveur) v1.

Un SUPER-COMBO est un enchainement planifie d AGENTS (pas d outils) pour
une mission complexe qui traverse plusieurs agents. Chaque super-combo a
SON arbre de decision (super-combos/arbre-super-combo-<nom>.json) AU-DESSUS
des arbres des agents.

Le SUPER-PILOTE conduit le super-combo. Il orchestre le FLUX inter-agents :
pour chaque case (agent + mission) de l arbre du super-combo, il
1) poste la mission pour l agent cible (file asap, champ agent explicite),
2) declenche oracle (mission-relais) : historise le DEBUT, envoie le message,
   initialise l etat de carte,
3) declare le pilote qui dirige l agent (couche inferieure deja en place),
4) passe a la case suivante.

PRINCIPE (decision utilisateur) : on ne cherche PAS a tout controler.
oracle / pilote / agents gerent deja les details de chaque mission et les
inter-round. Le super-pilote ne fait que conduire la sequence des agents
definie par l arbre du super-combo.

Usage:
    python3 super-pilote.py lister
    python3 super-pilote.py etapes <nom-super-combo>
    python3 super-pilote.py lancer <nom-super-combo>
    python3 super-pilote.py --boucle [--intervalle N]        # daemon resident

Statut : prototype (ebauche)

REGLE IMMUABLE : ASCII strict / LF pur / 100% stdlib Python.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"
STATUT = "ebauche"

ORACLE_DIR = Path(__file__).parent.parent
SUPER_COMBOS_DIR = Path(__file__).parent

# Injection du chemin pour reutiliser les fonctions oracle (files, pilote)
sys.path.insert(0, str(ORACLE_DIR))


# --- Lecture de l arbre d un super-combo ---

def _chemin_arbre(nom):
    return SUPER_COMBOS_DIR / f"arbre-super-combo-{nom}.json"


def charger_super_combo(nom):
    """Charger un super-combo par son nom. Retourne (arbre, erreur)."""
    chemin = _chemin_arbre(nom)
    if not chemin.exists():
        return None, f"super-combo introuvable: {nom}"
    try:
        return json.loads(chemin.read_text(encoding="utf-8")), None
    except ValueError as exc:
        return None, f"JSON invalide pour {nom}: {exc}"


def lister_super_combos():
    """Lister les super-combos disponibles."""
    resultats = []
    if SUPER_COMBOS_DIR.exists():
        for chemin in sorted(SUPER_COMBOS_DIR.glob("arbre-super-combo-*.json")):
            nom = chemin.stem.replace("arbre-super-combo-", "", 1)
            try:
                d = json.loads(chemin.read_text(encoding="utf-8"))
                resultats.append((nom, d.get("identite", {}).get("description", "")))
            except ValueError:
                resultats.append((nom, "JSON invalide"))
    return resultats


# --- Pilotage d un super-combo ---

def _poster_mission(agent, mission, file="asap"):
    """Poster la mission pour l agent cible (via files.ajouter, champ agent)."""
    try:
        from fonctions import files as _files
    except (ImportError, SystemExit):
        from fichiers import files as _files  # repli (chemin local)
    entree, erreur = _files.ajouter(mission, file=file, agent=agent)
    if erreur:
        return False, erreur
    return True, entree.get("id", "?")


def _relayer(agent, mission):
    """Declencher oracle mission-relais pour un agent et une mission donnes.

    Simule le flux normal (historise DEBUT, envoie le message, initialise
    l etat de carte) en appelant orchestralement oracle.py mission-relais
    sur la file asap, puis le pilote pour diriger l agent.
    """
    from subprocess import run as _run
    import sys as _sys
    base = [_sys.executable, str(ORACLE_DIR / "oracle.py")]
    # Note : la mission a ete postee avec champ agent explicite -> relais la deduit.
    r = _run(base + ["mission-relais", "--file", "asap"],
             capture_output=True, text=True, cwd=str(ORACLE_DIR))
    return r.stdout + r.stderr


def lancer(nom, verbose=True):
    """Executer un super-combo case par case."""
    arbre, erreur = charger_super_combo(nom)
    if erreur:
        print(f"[SUPER-PILOTE] ERREUR: {erreur}")
        return 1
    sc = arbre.get("super-combo", {})
    cases = arbre.get("cases", {})
    courant = sc.get("case_depart", "c1")
    gen = 0
    max_gen = len(cases) * 2 + 2  # garde-fou anti-boucle
    while courant and courant != "fin" and gen < max_gen:
        gen += 1
        case = cases.get(courant)
        if not case:
            print(f"[SUPER-PILOTE] Case inconnue: {courant}")
            return 1
        agent = case.get("agent")
        mission = case.get("mission", "")
        ftype = case.get("type", "agent")
        print("=" * 60)
        print(f"[SUPER-PILOTE] Etape {courant}: {case.get('titre', '')}")
        print(f"  Agent   : {agent}")
        print(f"  Mission : {mission[:80]}")
        # Poste + relais + pilote pour l agent (couche inferieure)
        ok, ref = _poster_mission(agent, mission, file=case.get("file", "asap"))
        if not ok:
            print(f"[SUPER-PILOTE] ERREUR poste: {ref}")
            return 1
        print(f"  Mission postee (id={ref}) -> relai oracle + pilote.")
        _relayer(agent, mission)
        courant = case.get("suivant", "fin")
    # Fin consolidee
    fin = arbre.get("fins", {}).get("fin-super-combo", {})
    print("=" * 60)
    print(f"[SUPER-PILOTE] {fin.get('titre', 'SUPER-COMBO TERMINE')}")
    print(f"  {fin.get('description', '')}")
    return 0


# --- Mode daemon (--boucle) ---

def boucle(intervalle=120):
    """Daemon resident : surveille et consomme les super-combos declares."""
    print(f"[SUPER-PILOTE] Daemon lance (intervalle {intervalle}s). "
          f"Ctrl+C pour arreter.")
    deja = set()
    try:
        while True:
            for nom, _desc in lister_super_combos():
                if nom in deja:
                    continue
                print(f"[SUPER-PILOTE] Lancement du super-combo '{nom}'...")
                lancer(nom)
                deja.add(nom)
            time.sleep(intervalle)
    except KeyboardInterrupt:
        print("\n[SUPER-PILOTE] Arret du daemon.")


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="SUPER-PILOTE v%s -- orchestre les super-combos cote Oracle" % VERSION
    )
    parser.add_argument("--boucle", action="store_true",
                        help="Daemon resident")
    parser.add_argument("--intervalle", type=int, default=120,
                        help="Intervalle du daemon (secondes)")
    parser.add_argument("sous_commande", nargs="?", help="lister|etapes|lancer")
    parser.add_argument("nom", nargs="?", help="Nom du super-combo")
    args = parser.parse_args()

    # Mode daemon
    if args.boucle:
        boucle(args.intervalle)
        return 0

    # Mode ponctuel
    if not args.sous_commande:
        parser.print_help()
        return 0
    if args.sous_commande == "lister":
        combos = lister_super_combos()
        if not combos:
            print("[SUPER-PILOTE] Aucun super-combo defini.")
            return 0
        print(f"[SUPER-PILOTE] {len(combos)} super-combo(s) :")
        for nom, desc in combos:
            print(f"  - {nom}: {desc}")
        return 0
    if args.sous_commande == "etapes":
        arbre, erreur = charger_super_combo(args.nom)
        if erreur:
            print(f"[SUPER-PILOTE] ERREUR: {erreur}")
            return 1
        cases = arbre.get("cases", {})
        courant = arbre.get("super-combo", {}).get("case_depart", "c1")
        print(f"[SUPER-PILOTE] Super-combo '{args.nom}' - etapes :")
        while courant and courant != "fin":
            case = cases.get(courant)
            if not case:
                break
            print(f"  - [{courant}] {case.get('titre', '')} -> agent {case.get('agent')}")
            courant = case.get("suivant", "fin")
        print("  - [fin] SUPER-COMBO TERMINE")
        return 0
    if args.sous_commande == "lancer":
        if not args.nom:
            print("[SUPER-PILOTE] Nom du super-combo requis: lancer <nom>")
            return 1
        return lancer(args.nom)
    print(f"[SUPER-PILOTE] Sous-commande inconnue: {args.sous_commande}")
    return 1


if __name__ == "__main__":
    sys.exit(main())