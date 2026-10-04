#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
ecrire-fichier.py
Ecrire ou ecraser le contenu d'un fichier. Supporte l'ecriture depuis un
argument ou depuis stdin.

Usage:
  ecrire-fichier.py [OPTIONS] <fichier> [contenu]

Options:
  --backup            Creer une sauvegarde .bak avant
  --dry-run           Simuler sans ecrire
  --verbose           Afficher les details
  --version           Afficher la version
  --aide, -h          Afficher cette aide

Exemples:
  ecrire-fichier.py fichier.md "# Nouveau contenu"
  echo "texte" | ecrire-fichier.py fichier.md -

Retour: 0 si succes, 1 si erreur.

Proprietaire : Vulcain (outil partage)
Version : 0.3.3
Statut : prepare
"""

import argparse
import io
import os
import shutil
import sys

VERSION = "0.3.3"
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
    attendu = "ecrire-fichier.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="ecrire-fichier.py",
        description="Ecrire ou ecraser le contenu d'un fichier.",
        add_help=False,
    )
    parser.add_argument("fichier", nargs="?", default=None,
                        help="Chemin du fichier a ecrire")
    parser.add_argument("contenu", nargs="?", default="",
                        help="Contenu a ecrire (ou '-' pour lire depuis stdin)")
    parser.add_argument("--contenu-chemin", dest="contenu_chemin", default=None,
                        help="Mode ANTI-HEREDOC : lire le contenu depuis un fichier source au lieu d un argument bash (contenus longs acceptes sans troncature)")
    parser.add_argument("--backup", action="store_true",
                        help="Creer une sauvegarde .bak avant")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans ecrire")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    parser.add_argument("--agent", type=str, default=None,
                        help="Agent appelant (perimetre)")
    return parser


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("ecrire-fichier.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.fichier is None:
        print(RED + "[ERREUR] Aucun fichier specifie" + NC)
        construire_parser().print_help()
        return 1

    fichier = args.fichier

    # PERIMETRE PAR AGENT (v0.5.0-pilote, decision utilisateur 2026-08-22) :
    # si cerveau-projet/agents/<agent>/perimetre.json existe (--agent fourni),
    # la cible doit matcher un motif sinon BLOQUE.
    _ag = ""
    for _i, _a in enumerate(sys.argv):
        if _a == "--agent" and _i + 1 < len(sys.argv):
            _ag = sys.argv[_i + 1]
    if _ag:
        import json as _json
        import io as _io
        import fnmatch as _fn
        _pf = os.path.join("cerveau-projet", "agents", _ag, "perimetre.json")
        if os.path.isfile(_pf):
            _d = _json.load(_io.open(_pf, encoding="utf-8"))
            _n = os.path.normpath(os.path.abspath(fichier)).replace("\\", "/")
            _r = os.path.normpath(os.getcwd()).replace("\\", "/")
            _rel = _n[len(_r) + 1:] if _n.startswith(_r + "/") else _n
            _ok = any(
                _rel == m.replace("\\", "/")
                or _fn.fnmatch(_rel, m.replace("\\", "/"))
                for m in _d.get("fichiers", []))
            if not _ok:
                print(RED + "[BLOQUE] %s hors du PERIMETRE de %s (voir "
                      "cerveau-projet/agents/%s/perimetre.json)"
                      % (os.path.basename(fichier), _ag, _ag) + NC)
                return 1

    # Securite (round 3) : octet nul dans le chemin -> refus explicite
    if "\x00" in fichier:
        print(RED + "[ERREUR] Chemin non sur (octet nul present)" + NC)
        return 1

    # Securite (round 3) : refus d'ecrire a travers un lien symbolique
    # (l'ecriture suivrait le lien vers la cible a l'insu de l'agent)
    if os.path.islink(fichier):
        print(RED + "[ERREUR] Chemin est un lien symbolique (refus securite): " +
              fichier + NC)
        return 1

    contenu = args.contenu

    # Mode ANTI-HEREDOC : lire le contenu depuis un fichier source (jamais
    # de ligne de commande geante). Pattern identique a creer-fichier
    # --contenu-chemin et ajouter-contenu-fichier --fichier SOURCE.
    if args.contenu_chemin:
        try:
            if not os.path.isfile(args.contenu_chemin):
                print(RED + "[ERREUR] Fichier source introuvable: " +
                      args.contenu_chemin + NC)
                return 1
            with io.open(args.contenu_chemin, "r", encoding="utf-8") as fh:
                contenu = fh.read().rstrip("\n")
        except OSError as e:
            print(RED + "[ERREUR] Lecture du fichier source impossible: " +
                  str(e) + NC)
            return 1

    # Lire le contenu depuis stdin si "-" ou si stdin est un pipe
    if contenu == "-" or (not contenu and not sys.stdin.isatty()):
        contenu = sys.stdin.read()

    if args.dry_run:
        print(YELLOW + "[DRY-RUN] Ecriture dans: " + fichier + NC)
        return 0

    # Sauvegarde si demandee et le fichier existe. Copie BINAIRE (shutil) :
    # une copie texte pourrait corrompre un fichier non-UTF-8 (latin-1).
    if args.backup and os.path.isfile(fichier):
        backup_path = fichier + ".bak"
        shutil.copy2(fichier, backup_path)
        if args.verbose:
            print(BLUE + "[INFO] Sauvegarde creee: " + backup_path + NC)

    # Ecrire. Contenu vide = fichier TRONQUE a zero octet (jamais de no-op
    # silencieux : vider un fichier est une action explicite et le message
    # le confirme). L'ecriture d'un contenu vide cree le fichier s'il
    # n'existe pas (comportement naturel d'un ecrire).
    try:
        if contenu:
            # FIGER LF : newline='' evite la traduction CRLF Windows
            with open(fichier, "w", encoding="utf-8", newline="") as f:
                f.write(contenu)
            if args.verbose:
                print(GREEN + "[OK] Fichier ecrit: " + fichier + NC)
        else:
            # Troncature explicite (le .sh fait la meme chose avec > fichier)
            with open(fichier, "w", encoding="utf-8", newline="") as f:
                pass
            print(YELLOW + "[INFO] Contenu vide : fichier tronque a zero octet: " +
                  fichier + NC)
    except OSError as e:
        print(RED + "[ERREUR] Impossible d'ecrire " + fichier +
              " : " + str(e) + NC)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
