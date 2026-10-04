#!/usr/bin/env python3
# -*- coding: ascii -*-
# ajouter-contenu-fichier.py
# Ajouter du contenu a la fin d'un fichier (append)
# Version : 0.3.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# OUTIL PYTHON - VERSION DE ajouter-contenu-fichier.sh
# ============================================================
# Meme logique que la version bash, traduite en Python.
# 100% stdlib, ASCII strict, compatible Windows/Git Bash.
# ============================================================

"""
ajouter-contenu-fichier.py
ajouter-contenu-fichier

Usage:
  ajouter-contenu-fichier.py [OPTIONS]
"""

import argparse
import os
import sys
from pathlib import Path

VERSION = "0.3.0"
STATUT = "prepare"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    """Retourne le texte colore si le terminal le supporte, sinon le texte brut."""
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def verifier_nommage(script_path):
    """VERIFIE que le nom du fichier commence par le prefixe du dossier de categorie.

    Exemple : agents/tools/ajouter/ajouter-contenu-fichier/ajouter-contenu-fichier.py
    -> dossier parent = 'ajouter-contenu-fichier', prefixe attendu = 'ajouter-'
    """
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(
            _couleur(
                "ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
                % (nom_fichier, prefixe),
                "rouge",
            ),
            file=sys.stderr,
        )
        sys.exit(1)


def afficher_aide(parser):
    """Affiche l'aide de l'outil."""
    print("=== ajouter-contenu-fichier v%s ===" % VERSION)
    print("")
    parser.print_help()


def construire_parser():
    """Construit le parseur d'arguments."""
    parser = argparse.ArgumentParser(
        prog="ajouter-contenu-fichier",
        description="Ajouter du contenu a la fin d'un fichier (append)",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("cible", nargs="?", type=str, help="Fichier a completer")
    parser.add_argument("contenu", nargs="?", type=str, help="Chaine a ajouter")
    parser.add_argument("--fichier", type=str, dest="source", help="Ajouter le contenu d'un fichier source")
    parser.add_argument("--backup", action="store_true", help="Creer une sauvegarde .bak avant")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans modifier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="ajouter-contenu-fichier v%s" % VERSION)
    return parser


def main():
    """Point d'entree principal de l'outil."""
    verifier_nommage(sys.argv[0])

    parser = construire_parser()
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    cible = args.cible
    contenu = args.contenu
    source = args.source
    backup = args.backup
    dry_run = args.dry_run
    verbose = args.verbose

    if not cible:
        print(_couleur("[ERREUR] Fichier cible obligatoire", "rouge"), file=sys.stderr)
        afficher_aide(parser)
        return 1

    if not Path(cible).is_file():
        print(_couleur("[ERREUR] Fichier cible non trouve: %s" % cible, "rouge"), file=sys.stderr)
        return 1

    # Determiner le contenu a ajouter et le nombre de lignes
    nb_lignes = 0
    contenu_a_ajouter = ""

    if source:
        if not Path(source).is_file():
            print(_couleur("[ERREUR] Fichier source non trouve: %s" % source, "rouge"), file=sys.stderr)
            return 1
        with open(source, "r", encoding="utf-8") as f:
            contenu_a_ajouter = f.read()
        nb_lignes = contenu_a_ajouter.count("\n")
        if contenu_a_ajouter and not contenu_a_ajouter.endswith("\n"):
            nb_lignes += 1
    elif contenu is not None:
        contenu_a_ajouter = contenu + "\n"
        nb_lignes = contenu.count("\n") + 1
    else:
        print(_couleur("[ERREUR] Aucun contenu a ajouter (chaine ou --fichier)", "rouge"), file=sys.stderr)
        afficher_aide(parser)
        return 1

    if verbose:
        print(_couleur("[INFO] Fichier cible: %s" % cible, "bleu"))
        print(_couleur("[INFO] %d ligne(s) a ajouter" % nb_lignes, "bleu"))

    if dry_run:
        print(_couleur("[DRY-RUN] %d ligne(s) seraient ajoutees a %s" % (nb_lignes, cible), "jaune"))
        return 0

    try:
        if backup:
            import shutil
            shutil.copy2(cible, cible + ".bak")
            if verbose:
                print(_couleur("[INFO] Sauvegarde: %s.bak" % cible, "bleu"))
        # S'assurer que le fichier se termine par un retour a la ligne
        with open(cible, "r", encoding="utf-8") as f:
            contenu_cible = f.read()
        if contenu_cible and not contenu_cible.endswith("\n"):
            contenu_a_ajouter = "\n" + contenu_a_ajouter

        # FIGER LF : newline='' evite la traduction CRLF Windows
        with open(cible, "a", encoding="utf-8", newline="") as f:
            f.write(contenu_a_ajouter)
    except OSError as e:
        print(_couleur("[ERREUR] L'ajout a echoue: %s" % e, "rouge"), file=sys.stderr)
        return 1

    print(_couleur("[OK] %d ligne(s) ajoutee(s) a la fin de %s" % (nb_lignes, cible), "vert"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
