#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
inserer-contenu-fichier.py
Inserer du contenu a une position precise dans un fichier (apres un numero
de ligne OU apres une ligne contenant un motif).

Usage:
  inserer-contenu-fichier.py [OPTIONS] <fichier> <position|--apres MOTIF> [contenu]

Arguments:
  <fichier>       Fichier a modifier
  <position>      Inserer APRES cette ligne (0 = au debut)
  [contenu]       Chaine a inserer (ou --fichier source)

Options:
  --apres <motif> Inserer apres la PREMIERE ligne contenant le motif
                  (ciblage par contenu : l'agent n'a pas a compter les lignes)
  --indent        Aligner le bloc insere sur l'indentation de la ligne cible
                  (detection automatique du contexte, pas de calcul manuel)
  --fichier <src> Inserer le contenu d'un fichier source
  --backup        Creer une sauvegarde .bak avant
  --dry-run       Simuler sans modifier
  --verbose       Afficher les details
  --version       Afficher la version
  --aide, -h      Afficher cette aide

Retour: 0 si succes, 1 si erreur (motif introuvable = echec explicite).

Proprietaire : Buffy (outil partage)
Version : 0.3.1
Statut : prepare
"""

import argparse
import os
import re
import shutil
import sys

VERSION = "0.3.1"
STATUT = "prepare"

# Securite (round 3) : force la sortie en UTF-8 pour ne jamais crasher sur
# l'encodage de la console (cp1252 sous Windows avec des caracteres non-ASCII).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass  # Python < 3.7 : la console gere l'encodage comme elle peut

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "inserer-contenu-fichier.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="inserer-contenu-fichier.py",
        description="Inserer du contenu a une position precise dans un fichier.",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Fichier a modifier")
    parser.add_argument("position", nargs="?", default=None,
                        help="Inserer APRES cette ligne (0 = au debut)")
    parser.add_argument("contenu", nargs="?", default="",
                        help="Chaine a inserer (ou --fichier source)")
    parser.add_argument("--apres", dest="motif", default="",
                        help="Inserer apres la premiere ligne contenant le motif")
    parser.add_argument("--indent", action="store_true",
                        help="Aligner le bloc sur l'indentation de la ligne cible")
    parser.add_argument("--fichier", dest="source", default="",
                        help="Inserer le contenu d'un fichier source")
    parser.add_argument("--backup", action="store_true",
                        help="Creer une sauvegarde .bak avant")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans modifier")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details")
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
        print("inserer-contenu-fichier.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.fichier is None:
        print(RED + "[ERREUR] Fichier obligatoire" + NC)
        construire_parser().print_help()
        return 1

    # Ergonomie --apres : avec ce mode l'agent fournit <fichier> <contenu>
    # (2 positionnels) au lieu de <fichier> <position> <contenu> (3).
    # Si la position n'est pas un nombre, c'est en realite le contenu.
    if args.motif and args.position is not None and not args.position.isdigit():
        if not args.contenu:
            args.contenu = args.position
        args.position = None

    if args.position is None and not args.motif:
        print(RED + "[ERREUR] Position ou --apres <motif> obligatoire" + NC)
        construire_parser().print_help()
        return 1

    fichier = args.fichier
    position = args.position

    # Securite (round 3) : octet nul dans le chemin -> refus explicite
    if "\x00" in fichier or (args.source and "\x00" in args.source):
        print(RED + "[ERREUR] Chemin non sur (octet nul present)" + NC)
        return 1

    # Securite (round 3) : refus de modifier a travers un lien symbolique
    if os.path.islink(fichier) or (args.source and os.path.islink(args.source)):
        print(RED + "[ERREUR] Chemin est un lien symbolique (refus securite): " +
              fichier + NC)
        return 1

    if not os.path.isfile(fichier):
        print(RED + "[ERREUR] Fichier non trouve: " + fichier + NC)
        return 1

    # Lecture robuste (round 3) : UTF-8-sig puis fallback latin-1, jamais de crash
    def lire_robuste(chemin):
        try:
            with open(chemin, encoding="utf-8-sig") as f:
                return f.read().split("\n")
        except (UnicodeDecodeError, OSError):
            with open(chemin, encoding="latin-1") as f:
                return f.read().split("\n")

    if args.motif:
        if position is not None:
            print(YELLOW + "[INFO] --apres fourni : le numero de ligne est ignore" + NC)
        # Ciblage par contenu : trouver la premiere ligne contenant le motif
        try:
            lignes = lire_robuste(fichier)
        except OSError as e:
            print(RED + "[ERREUR] Lecture impossible: " + str(e) + NC)
            return 1
        indice_motif = None
        for i, ligne in enumerate(lignes):
            if args.motif in ligne:
                indice_motif = i
                break
        if indice_motif is None:
            print(RED + "[ERREUR] Motif introuvable dans " + fichier +
                  " : " + args.motif + NC)
            return 1
        position = indice_motif + 1  # inserer APRES la ligne du motif
        indentation_cible = re.match(r"\s*", lignes[indice_motif]).group(0)
        if args.verbose:
            print(BLUE + "[INFO] Motif trouve ligne " + str(position) + NC)
            print(BLUE + "[INFO] Indentation de la ligne cible : '" +
                  indentation_cible + "'" + NC)
    else:
        if not position.isdigit():
            print(RED + "[ERREUR] La position doit etre un nombre: " + position + NC)
            return 1
        position = int(position)
        indentation_cible = ""

    if args.source:
        if not os.path.isfile(args.source):
            print(RED + "[ERREUR] Fichier source non trouve: " + args.source + NC)
            return 1
    elif not args.contenu:
        print(RED + "[ERREUR] Aucun contenu a inserer (chaine ou --fichier)" + NC)
        construire_parser().print_help()
        return 1

    try:
        lignes = lire_robuste(fichier)
    except OSError as e:
        print(RED + "[ERREUR] Lecture impossible: " + str(e) + NC)
        return 1

    total_lignes = len(lignes)

    if position > total_lignes:
        print(YELLOW + "[INFO] La position (" + str(position) +
              ") depasse le nombre de lignes (" + str(total_lignes) + ")" + NC)
        print(YELLOW + "[INFO] Le contenu sera ajoute a la fin" + NC)
        position = total_lignes

    if args.verbose:
        print(BLUE + "[INFO] Fichier: " + fichier +
              " (" + str(total_lignes) + " lignes)" + NC)
        print(BLUE + "[INFO] Insertion apres la ligne " + str(position) + NC)

    if args.dry_run:
        print(YELLOW + "[DRY-RUN] Insertion simulee apres la ligne " +
              str(position) + " dans " + fichier + NC)
        return 0

    # Construire le contenu a inserer
    if args.source:
        try:
            bloc = "\n".join(lire_robuste(args.source)).rstrip("\n")
        except OSError as e:
            print(RED + "[ERREUR] Lecture source impossible: " + str(e) + NC)
            return 1
    else:
        bloc = args.contenu

    # Indentation automatique : aligner chaque ligne du bloc sur la cible
    if args.indent and indentation_cible:
        lignes_bloc = bloc.split("\n")
        bloc = "\n".join(indentation_cible + l for l in lignes_bloc)
        if args.verbose:
            print(BLUE + "[INFO] Indentation appliquee au bloc insere" + NC)

    # Inserer : avant = lignes 0..position ; bloc ; apres = position+1..fin
    avant = lignes[:position]
    apres = lignes[position:]
    nouvelles = avant + [bloc] + apres
    resultat = "\n".join(nouvelles)

    try:
        if args.backup:
            shutil.copy2(fichier, fichier + ".bak")
            if args.verbose:
                print(BLUE + "[INFO] Sauvegarde: " + fichier + ".bak" + NC)
        # FIGER LF : newline='' evite la traduction CRLF Windows
        with open(fichier, "w", encoding="utf-8", newline="") as f:
            f.write(resultat)
    except OSError as e:
        print(RED + "[ERREUR] L'insertion a echoue: " + str(e) + NC)
        return 1

    print(GREEN + "[OK] Contenu insere apres la ligne " + str(position) +
          " dans " + fichier + NC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
