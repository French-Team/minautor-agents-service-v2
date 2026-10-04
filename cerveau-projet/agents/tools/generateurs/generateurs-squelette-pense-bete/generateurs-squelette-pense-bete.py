#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
generateurs-squelette-pense-bete.py
Genere le squelette d'un pense-bete conforme au pense-bete-template.

Usage:
  generateurs-squelette-pense-bete.py --theme <theme> [--id <id>]
      [--class <class>] [--statut <statut>] [--dossier <dossier>]
      [--dry-run]

Options:
  --theme <theme>     Theme du pense-bete (obligatoire, sans accents ni espaces)
  --id <id>           Identifiant numerique (defaut: 001)
  --class <class>     Classe numerique (defaut: 01)
  --statut <statut>   Statut (defaut: ebauche)
  --dossier <dossier> Dossier de destination (defaut: .)
  --dry-run           Afficher le squelette sans creer le fichier
  --version           Afficher la version
  --aide, -h          Afficher cette aide

Retour: 0 si succes, 1 si erreur.

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : beta
"""

import argparse
import datetime
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "beta"

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color

# Theme valide : minuscules, chiffres, tirets (pas d'accents ni espaces)
THEME_VALIDE = re.compile(r"^[a-z0-9-]+$")


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "generateurs-squelette-pense-bete.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def generer_squelette(theme, id_elt, class_elt, statut):
    """Genere le squelette du pense-bete (markdown)."""
    date = datetime.date.today().isoformat()
    return f"""# Gabarit -- Pense-bete

**Statut :** {statut}
**ID :** {id_elt}
**Class :** {class_elt}
**Cree :** {date}
**Theme :** {theme}

---

## 1. Idee (1-2 phrases)

[L'essence du concept - ce que ce pense-bete apporte de nouveau ou resout]

## 2. Probleme / Question

[Quel probleme ou question ce pense-bete adresse-t-il ?]

## 3. Contexte

[Comment s'inscrit ce pense-bete dans le projet ou le cerveau ?]

## 4. Liens

- Pense-betes connexes : [a completer]
- Conventions applicables : [a completer]
- Regles immuables : [a completer]

## 5. Structure prevue (RVAV par sous-partie)

| Sous-partie | Fichier cible | Statut | RVAV |
|---|---|---|---|
| Idee | `pense-bete-{theme}.{id_elt}.{class_elt}.{statut}.md` | {statut} | a valider |
| Spec | `spec/spec-{theme}.{id_elt}.{class_elt}.{statut}.md` | - | a creer |
| Todo | `spec/todo/todo-{theme}.{id_elt}.{class_elt}.{statut}.md` | - | a creer |
| Liens | `liens/liens-{theme}.{id_elt}.{class_elt}.{statut}.md` | - | a creer |

## 6. RVAV du pense-bete

- [rechercher] -- toutes les references/liens externes sont rassembles
- [verifier] -- la structure (idee + probleme + contexte + liens) est complete
- [analyser] -- l'idee est coherente avec le cerveau existant (pas de doublon)
- [valider] -- pret pour le statut suivant (prepare)
"""


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="generateurs-squelette-pense-bete.py",
        description="Genere le squelette d'un pense-bete conforme au pense-bete-template.",
        add_help=False,
    )
    parser.add_argument("--theme", default="",
                        help="Theme du pense-bete (obligatoire, sans accents ni espaces)")
    parser.add_argument("--id", dest="id_elt", default="001",
                        help="Identifiant numerique (defaut: 001)")
    parser.add_argument("--class", dest="class_elt", default="01",
                        help="Classe numerique (defaut: 01)")
    parser.add_argument("--statut", default="ebauche",
                        help="Statut (defaut: ebauche)")
    parser.add_argument("--dossier", default=".",
                        help="Dossier de destination (defaut: .)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Afficher le squelette sans creer le fichier")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("generateurs-squelette-pense-bete.py v" + VERSION +
              " (" + STATUT + ")")
        return 0

    if not args.theme:
        print(RED + "[ERREUR] Le theme est obligatoire (--theme)" + NC)
        construire_parser().print_help()
        return 1

    if not THEME_VALIDE.match(args.theme):
        print(RED + "[ERREUR] Le theme doit etre en minuscules sans accents ni espaces : " +
              args.theme + NC)
        return 1

    nom_fichier = "pense-bete-" + args.theme + "." + args.id_elt + "." + \
        args.class_elt + "." + args.statut + ".md"
    chemin_fichier = os.path.join(args.dossier, nom_fichier)
    squelette = generer_squelette(args.theme, args.id_elt, args.class_elt,
                                  args.statut)

    if args.dry_run:
        print(YELLOW + "[DRY-RUN]" + NC + " Squelette de : " + nom_fichier)
        print("")
        print(squelette)
        return 0

    if os.path.isfile(chemin_fichier):
        print(RED + "[ERREUR] Le fichier existe deja : " + chemin_fichier + NC)
        return 1

    try:
        # FIGER LF : newline='' evite la traduction CRLF Windows
        with open(chemin_fichier, "w", encoding="utf-8", newline="") as f:
            f.write(squelette)
    except OSError as e:
        print(RED + "[ERREUR] Impossible de creer le fichier : " + str(e) + NC)
        return 1

    print(GREEN + "[OK]" + NC + " Squelette cree : " + chemin_fichier)
    return 0


if __name__ == "__main__":
    sys.exit(main())
