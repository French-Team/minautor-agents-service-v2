#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
detecter-local-hors-fonction.py
Detecte les declarations 'local' utilisees hors d'une fonction dans les
scripts bash.

Parseur brace-tracking : suit la profondeur d'accolades, detecte le debut
des fonctions ("name() {" ou "function name {") et signale tout mot cle
'local' hors de toute fonction.

Usage:
  detecter-local-hors-fonction.py [CHEMIN] [options]

Options:
  --recursive, -r     Recursif (scan de toute une arborescence)
  --verbose, -v       Afficher les details
  --version           Afficher la version
  --aide, -h          Afficher cette aide

Retour: 0 si aucun 'local' hors fonction, 1 sinon, 2 si erreur.

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : beta
"""

import argparse
import io
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "beta"

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


def analyser(chemin):
    """Retourne la liste des (numero_ligne, contenu) avec 'local' hors fonction."""
    try:
        c = io.open(chemin, encoding="utf-8").read()
    except Exception as e:
        return None, str(e)
    lignes = c.split("\n")
    resultats = []
    prof = 0
    dans_fonction = False
    niveau_fonction = -1

    for i, ligne in enumerate(lignes, 1):
        l = ligne.strip()
        if not l or l.startswith("#"):
            continue
        # Detection debut de fonction: "name() {" ou "function name {"
        m_func = (re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*\(\s*\)\s*\{", l)
                  or re.match(r"^function\s+[A-Za-z_][A-Za-z0-9_]*\s*(\(\s*\))?\s*\{", l))
        if m_func and not dans_fonction:
            dans_fonction = True
            niveau_fonction = prof
            prof += 1
            continue
        ouvr = l.count("{")
        ferm = l.count("}")
        prof += ouvr - ferm
        if ferm > 0 and dans_fonction and prof <= niveau_fonction:
            dans_fonction = False
            niveau_fonction = -1
        if prof < 0:
            prof = 0
        if re.match(r"^\s*local\b", l) and not dans_fonction:
            resultats.append((i, l))
    return resultats, None


def analyser_fichier(chemin, verbose):
    """Analyse un fichier .sh. Retourne (nb_local_hors_fonction, lignes)."""
    res, erreur = analyser(chemin)
    if erreur:
        print(RED + "[ERREUR] Lecture impossible de " + chemin +
              " : " + erreur + NC)
        return None
    return res


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="detecter-local-hors-fonction.py",
        description="Detecte les declarations 'local' utilisees hors d'une fonction dans les scripts bash.",
        add_help=False,
    )
    parser.add_argument("chemin", nargs="?",
                        default="cerveau-projet/agents/tools",
                        help="Fichier .sh ou dossier a analyser (defaut: outils/)")
    parser.add_argument("--recursive", "-r", action="store_true",
                        help="Recursif (scan de toute une arborescence)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Afficher les details")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def main(argv=None):
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("detecter-local-hors-fonction.py v" + VERSION + " (" + STATUT + ")")
        return 0

    cible = args.chemin
    total_fichiers = 0
    fichiers_ok = 0
    fichiers_problemes = 0

    print(BLUE + "=== Detection des 'local' hors fonction ===" + NC)
    print(BLUE + "Version : " + VERSION + NC)
    print(BLUE + "Cible : " + cible + NC)
    print("")

    if os.path.isfile(cible):
        # Mode fichier unique
        total_fichiers = 1
        nom = os.path.basename(cible)
        print(BLUE + "[FICHIER] Analyse de : " + cible + NC)
        res = analyser_fichier(cible, args.verbose)
        if res is None:
            return 2
        if not res:
            print(GREEN + "[OK] " + nom +
                  " : aucun 'local' hors fonction" + NC)
            fichiers_ok = 1
        else:
            print(RED + "[PROBLEME] " + nom + " : " + str(len(res)) +
                  " 'local' hors fonction" + NC)
            for num, contenu in res:
                print("  L" + str(num) + ": " + contenu.strip()[:100])
            fichiers_problemes = 1
    elif os.path.isdir(cible):
        # Mode dossier
        for racine, _, fichiers in os.walk(cible):
            if not args.recursive and racine != cible:
                continue
            for nom_f in sorted(fichiers):
                if not nom_f.endswith(".sh"):
                    continue
                chemin = os.path.join(racine, nom_f)
                total_fichiers += 1
                res = analyser_fichier(chemin, args.verbose)
                if res is None:
                    return 2
                if not res:
                    fichiers_ok += 1
                else:
                    fichiers_problemes += 1
                    print(RED + "[PROBLEME] " + chemin + " : " +
                          str(len(res)) + " 'local' hors fonction" + NC)
                    for num, contenu in res:
                        print("  L" + str(num) + ": " + contenu.strip()[:100])
                if args.verbose:
                    print("  [scanne] " + chemin)
    else:
        print(RED + "[ERREUR] '" + cible + "' n'existe pas" + NC)
        return 2

    print("")
    print(BLUE + "=== Resume ===" + NC)
    print("  Total : " + str(total_fichiers))
    print("  OK : " + str(fichiers_ok))
    print("  Fichiers avec 'local' hors fonction : " + str(fichiers_problemes))

    if fichiers_problemes > 0:
        print(RED + "[KO] Des 'local' hors fonction ont ete detectes" + NC)
        return 1
    else:
        print(GREEN + "[OK] Aucun 'local' hors fonction" + NC)
        return 0


if __name__ == "__main__":
    sys.exit(main())
