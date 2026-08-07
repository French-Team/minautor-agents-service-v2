#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
editer-fichier.py

Remplace une chaine par une autre dans un fichier.
Premiere occurrence par defaut, toutes avec --global.

Utilisation:
  editer-fichier.py [OPTIONS] <fichier> <ancien> <nouveau>

Options :
  --global         Remplacer toutes les occurrences
  --backup         Creer une sauvegarde .bak avant
  --dry-run        Simuler sans modifier
  --verbose        Afficher les details
  --help           Afficher cette aide

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import shutil
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("=== editer-fichier v%s ===" % VERSION)
    print("")
    print("Usage: editer-fichier.py [OPTIONS] <fichier> <ancien> <nouveau>")
    print("")
    print("Options :")
    print("  --global         Remplacer toutes les occurrences")
    print("  --backup         Creer une sauvegarde .bak avant")
    print("  --dry-run        Simuler sans modifier")
    print("  --verbose        Afficher les details")
    print("  --help           Afficher cette aide")
    print("")
    print("Exemples :")
    print("  editer-fichier.py fichier.md \"ancien\" \"nouveau\"")
    print("  editer-fichier.py --global fichier.md \"texte\" \"remplacement\"")


def main(argv):
    fichier = ""
    ancien = ""
    nouveau = ""
    global_remplacement = False
    backup = False
    dry_run = False
    verbose = False
    help_demande = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--global":
            global_remplacement = True
        elif arg == "--backup":
            backup = True
        elif arg == "--dry-run":
            dry_run = True
        elif arg == "--verbose":
            verbose = True
        elif arg in ("--help", "-h"):
            help_demande = True
        elif arg == "--version":
            print("editer-fichier v%s (%s)" % (VERSION, STATUT))
            return 0
        elif arg.startswith("-"):
            print("[ERREUR] Option inconnue : %s" % arg)
            afficher_aide()
            return 1
        else:
            if not fichier:
                fichier = arg
            elif not ancien:
                ancien = arg
            elif not nouveau:
                nouveau = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    if not fichier or not ancien:
        print("[ERREUR] Arguments manquants")
        afficher_aide()
        return 1

    if not os.path.isfile(fichier):
        print("[ERREUR] Fichier non trouve: %s" % fichier)
        return 1

    try:
        with io.open(fichier, encoding="utf-8") as fh:
            contenu = fh.read()
    except Exception:
        print("[ERREUR] Impossible de lire le fichier : %s" % fichier)
        return 1

    nb = contenu.count(ancien)

    if nb == 0:
        print("[INFO] Aucune occurrence de '%s' dans %s" % (ancien, fichier))
        return 0

    if dry_run:
        print("[DRY-RUN] %d occurrence(s) trouvee(s)" % nb)
        for num, ligne in enumerate(contenu.split("\n"), 1):
            if ancien in ligne:
                print("  %d: %s" % (num, ligne.strip()))
        return 0

    if backup:
        shutil.copy2(fichier, fichier + ".bak")
        if verbose:
            print("[INFO] Sauvegarde: %s.bak" % fichier)

    if global_remplacement:
        nouveau_contenu = contenu.replace(ancien, nouveau)
    else:
        nouveau_contenu = contenu.replace(ancien, nouveau, 1)

    with io.open(fichier, "w", encoding="utf-8", newline="") as fh:
        fh.write(nouveau_contenu)

    if verbose:
        print("[OK] Remplacement effectue dans %s" % fichier)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
