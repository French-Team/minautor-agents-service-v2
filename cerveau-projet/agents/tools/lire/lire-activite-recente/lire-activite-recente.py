#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lire-activite-recente.py
Lire les N dernieres interventions des agents depuis l'historique
(AGENTS-historique.md) au format condense : date | session | agent | action.

Usage:
  lire-activite-recente.py [OPTIONS] [fichier]

Arguments:
  [fichier]       Fichier historique a lire (defaut: env AGENTS_HISTORIQUE,
                  sinon AGENTS-historique.md)

Options:
  --nombre N      Nombre d'entrees a afficher (defaut: 15)
  --longueur L    Longueur max de l'action en caracteres (defaut: 100)
  --verbose       Afficher les details
  --version       Afficher la version
  --aide, -h      Afficher cette aide

Retour: 0 si succes, 1 si erreur.

Proprietaire : Vulcain (outil partage)
Version : 0.1.1
Statut : prepare
"""

import argparse
import os
import re
import sys

VERSION = "0.1.1"
STATUT = "prepare"
FICHIER_DEFAUT = "AGENTS-historique.md"

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "lire-activite-recente.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lire-activite-recente.py",
        description="Lire les N dernieres interventions des agents (format condense).",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Fichier historique (defaut: env AGENTS_HISTORIQUE ou AGENTS-historique.md)")
    parser.add_argument("--nombre", default=None,
                        help="Nombre d'entrees a afficher (defaut: 15)")
    parser.add_argument("--longueur", default=None,
                        help="Longueur max de l'action en caracteres (defaut: 100)")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


VERSION = "0.1.1"

RE_BALISES = re.compile(r"<[^>]+>")


def nettoyer_balises(texte):
    """Retire les balises HTML (spans de couleur) d une cellule."""
    return RE_BALISES.sub("", texte).strip()


def extraire_entrees(fichier, nombre, longueur):
    """Extraire les N dernieres interventions (les plus recentes en premier).
    Format v0.1.1 : | agent | heure | date | session | raison | (la 1re
    cellule est un span colore ; la raison peut continuer en lignes '###>').
    Retourne la liste de tuples (date, session, agent, action) avec
    date = 'AAAA-MM-JJ HH:MM' (reconstituee) et action = raison complete."""
    entrees = []
    try:
        with open(fichier, encoding="utf-8", errors="replace") as f:
            lignes = [ligne.strip() for ligne in f]
        i = 0
        while i < len(lignes) and len(entrees) < nombre:
            l = lignes[i]
            if not l.startswith("| <span"):
                i += 1
                continue
            parties = l.split("|")
            if len(parties) < 6:
                i += 1
                continue
            agent = nettoyer_balises(parties[1])
            heure = parties[2].strip()
            date = parties[3].strip()
            session = parties[4].strip()
            raison = "|".join(parties[5:-1]).strip()
            # continuations '###>' : suite de la raison (meme entree)
            i += 1
            while i < len(lignes) and lignes[i].startswith("###>"):
                suite = lignes[i][4:].strip()
                if suite:
                    raison += " " + suite
                i += 1
            date_heure = (date + " " + heure).strip()
            action = raison if len(raison) <= longueur else raison[:longueur] + "..."
            entrees.append((date_heure, session, agent, action))
    except OSError as e:
        print(RED + "[ERREUR] Lecture impossible: " + str(e) + NC)
        return None
    return entrees


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("lire-activite-recente.py v" + VERSION + " (" + STATUT + ")")
        return 0

    nombre = 15
    if args.nombre is not None:
        if not args.nombre.isdigit() or int(args.nombre) < 1:
            print(RED + "[ERREUR] --nombre doit etre un entier >= 1: " + args.nombre + NC)
            return 1
        nombre = int(args.nombre)

    longueur = 100
    if args.longueur is not None:
        if not args.longueur.isdigit() or int(args.longueur) < 1:
            print(RED + "[ERREUR] --longueur doit etre un entier >= 1: " + args.longueur + NC)
            return 1
        longueur = int(args.longueur)

    fichier = args.fichier or os.environ.get("AGENTS_HISTORIQUE") or FICHIER_DEFAUT
    if not os.path.isfile(fichier):
        print(RED + "[ERREUR] Fichier historique non trouve: " + fichier + NC)
        print(YELLOW + "  Defaut: env AGENTS_HISTORIQUE ou " + FICHIER_DEFAUT + NC)
        return 1

    if args.verbose:
        print(BLUE + "[INFO] Fichier: " + fichier + NC)
        print(BLUE + "[INFO] " + str(nombre) + " entrees (action max " + str(longueur) + " caracteres)" + NC)
        print("---")

    entrees = extraire_entrees(fichier, nombre, longueur)
    if entrees is None:
        return 1

    if not entrees:
        print(YELLOW + "[INFO] Aucune intervention trouvee dans " + fichier + NC)
        return 0

    for date, session, agent, action in entrees:
        print("%s | %s | %s | %s" % (date, session, agent, action))

    return 0


if __name__ == "__main__":
    sys.exit(main())
