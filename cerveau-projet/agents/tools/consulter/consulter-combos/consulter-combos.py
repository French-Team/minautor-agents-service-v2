#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
consulter-combos.py

Consulte le catalogue central des combos (catalogue-combos.json, source de
verite creee 2026-08-19) : il repond a la question "ou est utilise l outil X
et par qui ?" en croisant le catalogue (combos -> membres) et les fiches
outils (champ 'combos' du frontmatter).

La lecture est JOURNALISEE (registre-usages-outils) : qui a consulte quoi.

Usage:
  python3 consulter-combos.py --outil <nom-outil>
  python3 consulter-combos.py --combo <nom-combo>
  python3 consulter-combos.py --tous [--rapport <fichier>]

Options:
  --outil <nom>      Afficher les combos qui utilisent cet outil (+ proprietaire)
  --combo <nom>      Afficher les membres d un combo (+ proprietaire)
  --tous             Afficher tout le catalogue
  --agent <nom>      Agent qui consulte (pour la trace)
  --rapport <f>      Ecrire le rapport markdown dans ce fichier
  --version          Affiche la version
  --aide             Affiche cette aide

Version : 0.1.0
"""
import argparse
import io
import json
import os
import sys

VERSION = "0.1.0"
STATUT = "prepare"

GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def chemin_catalogue(racine):
    return os.path.join(racine, "cerveau-projet", "agents", "tools",
                        "combos", "catalogue-combos.json")


def charger_catalogue(racine):
    chemin = chemin_catalogue(racine)
    if not os.path.isfile(chemin):
        print("[ERREUR] catalogue-combos.json introuvable : %s" % chemin)
        sys.exit(2)
    with io.open(chemin, encoding="utf-8") as fh:
        return json.load(fh)


def index_outil_vers_combos(catalogue):
    """outil -> [(combo, proprietaire)]"""
    resultat = {}
    for combo in catalogue.get("combos", []):
        nom = combo.get("nom", "")
        proprio = combo.get("proprietaire", "?")
        for m in combo.get("membres", []):
            resultat.setdefault(m, []).append((nom, proprio))
    return resultat


def index_combo(catalogue):
    """combo -> {proprietaire, membres}"""
    return {c.get("nom", ""): c for c in catalogue.get("combos", [])}


def journaliser(agent, outil_consulte):
    """Ecrit une entree de consultation dans le registre des usages."""
    registre = os.path.join(racine_projet(), "cerveau-projet", "agents",
                            "traces", "registre-usages-outils.jsonl")
    import datetime
    entree = {
        "agent": agent or "inconnu",
        "outil": "consulter-combos",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "verrou-auto",
        "contexte": "consultation: %s" % outil_consulte,
    }
    try:
        with io.open(registre, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entree, ensure_ascii=False) + "\n")
    except (IOError, OSError):
        pass


def afficher_outil(catalogue, nom_outil):
    index = index_outil_vers_combos(catalogue)
    combos = index.get(nom_outil, [])
    if not combos:
        print("%s[INFO] L outil '%s' n est membre d aucun combo du catalogue.%s"
              % (YELLOW, nom_outil, NC))
        return
    print("=== Outil : %s ===" % nom_outil)
    print("Utilise par %d combo(s) :" % len(combos))
    for combo, proprio in combos:
        print("  - %s (proprietaire : %s)" % (combo, proprio))


def afficher_combo(catalogue, nom_combo):
    combos = index_combo(catalogue)
    combo = combos.get(nom_combo)
    if not combo:
        print("%s[INFO] Combo '%s' introuvable dans le catalogue.%s"
              % (YELLOW, nom_combo, NC))
        return
    membres = combo.get("membres", [])
    print("=== Combo : %s ===" % nom_combo)
    print("Proprietaire : %s" % combo.get("proprietaire", "?"))
    print("Type : %s" % combo.get("type", "?"))
    if membres:
        print("Outils membres (%d) :" % len(membres))
        for m in membres:
            print("  - %s" % m)
    else:
        print("Outils membres : aucun (combo d analyse ou de chainage interne)")


def afficher_tout(catalogue):
    print("=== Catalogue des combos (v%s) ===" % catalogue.get("version", "?"))
    print("")
    for combo in catalogue.get("combos", []):
        print("- %s (proprietaire : %s, %s)" %
              (combo.get("nom", "?"), combo.get("proprietaire", "?"),
               combo.get("type", "?")))


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="consulter-combos.py",
        description="Consulte le catalogue des combos (source de verite).",
        add_help=False,
    )
    parser.add_argument("--outil", default="", help="Nom de l outil a interroger")
    parser.add_argument("--combo", default="", help="Nom du combo a afficher")
    parser.add_argument("--tous", action="store_true",
                        help="Afficher tout le catalogue")
    parser.add_argument("--agent", default="",
                        help="Agent qui consulte (pour la trace)")
    parser.add_argument("--rapport", default="",
                        help="Ecrire le rapport markdown dans ce fichier")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def ecrire_rapport(catalogue, nom, contenu, chemin):
    with io.open(chemin, "w", encoding="utf-8", newline="") as fh:
        fh.write("---\n")
        fh.write("type: rapport-consultation-combos\n")
        fh.write("date: 2026-08-19\n")
        fh.write("cible: %s\n" % nom)
        fh.write("---\n\n")
        fh.write("# Consultation combos : %s\n\n" % nom)
        fh.write("```\n%s\n```\n" % contenu)
    print("Rapport ecrit : %s" % chemin)


def main():
    args = construire_parser().parse_args()
    if args.version:
        print("consulter-combos.py v%s (%s)" % (VERSION, STATUT))
        return 0
    if args.aide:
        print(__doc__)
        return 0
    if not (args.outil or args.combo or args.tous):
        print("[ERREUR] Fournir --outil, --combo ou --tous (--aide pour l aide)")
        return 2

    racine = racine_projet()
    catalogue = charger_catalogue(racine)

    if args.outil:
        afficher_outil(catalogue, args.outil)
        journaliser(args.agent, args.outil)
    elif args.combo:
        afficher_combo(catalogue, args.combo)
        journaliser(args.agent, args.combo)
    elif args.tous:
        afficher_tout(catalogue)
        journaliser(args.agent, "--tous")
    return 0


if __name__ == "__main__":
    sys.exit(main())
