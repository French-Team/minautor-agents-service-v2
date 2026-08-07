#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
supprimer-ligne.py

Supprimer une ligne (ou une plage) par numero dans un fichier.

Arguments:
  <fichier>       Fichier a modifier
  <ligne>         Numero de la ligne a supprimer (1 = premiere)
  [ligne-fin]     Derniere ligne de la plage a supprimer (defaut = ligne)

Options:
  --dry-run       Simuler sans modifier
  --verbose       Afficher les details
  --help          Afficher cette aide

Proprietaire : Buffy (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"


def afficher_aide():
    print("=== supprimer-ligne v%s ===" % VERSION)
    print("")
    print("Usage: supprimer-ligne.py [OPTIONS] <fichier> <ligne> [ligne-fin]")
    print("")
    print("Arguments :")
    print("  <fichier>       Fichier a modifier")
    print("  <ligne>         Numero de la ligne a supprimer (1 = premiere)")
    print("  [ligne-fin]     Derniere ligne de la plage a supprimer (defaut = ligne)")
    print("")
    print("Options :")
    print("  --dry-run       Simuler sans modifier")
    print("  --verbose       Afficher les details")
    print("  --help          Afficher cette aide")


def main(argv):
    fichier = ""
    ligne = ""
    ligne_fin = ""
    dry_run = False
    verbose = False
    help_demande = False

    for arg in argv:
        if arg == "--dry-run":
            dry_run = True
        elif arg in ("--verbose", "-v"):
            verbose = True
        elif arg in ("--help", "--aide", "-h"):
            help_demande = True
        elif arg == "--version":
            print("supprimer-ligne v%s (%s)" % (VERSION, STATUT))
            return 0
        else:
            if not fichier:
                fichier = arg
            elif not ligne:
                ligne = arg
            elif not ligne_fin:
                ligne_fin = arg
            else:
                print("[ERREUR] Trop d'arguments: %s" % arg)
                afficher_aide()
                return 1

    if help_demande:
        afficher_aide()
        return 0

    if not fichier or not ligne:
        print("[ERREUR] Fichier et numero de ligne obligatoires")
        afficher_aide()
        return 1

    if not os.path.isfile(fichier):
        print("[ERREUR] Fichier non trouve: %s" % fichier)
        return 1

    if not ligne.isdigit():
        print("[ERREUR] Le numero de ligne doit etre un nombre: %s" % ligne)
        return 1

    if not ligne_fin:
        ligne_fin = ligne

    if not ligne_fin.isdigit():
        print("[ERREUR] La ligne de fin doit etre un nombre: %s" % ligne_fin)
        return 1

    debut = int(ligne)
    fin = int(ligne_fin)

    if debut < 1:
        print("[ERREUR] Le numero de ligne doit etre >= 1")
        return 1

    if fin < debut:
        print("[ERREUR] La ligne de fin (%d) doit etre >= a la ligne (%d)" % (fin, debut))
        return 1

    try:
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            toutes = fh.readlines()
    except IOError:
        print("[ERREUR] Impossible de lire le fichier: %s" % fichier)
        return 1

    total_lignes = len(toutes)

    if debut > total_lignes:
        print("[INFO] Le fichier n'a que %d lignes, ligne %d inexistante" % (total_lignes, debut))
        return 0

    if fin > total_lignes:
        fin = total_lignes

    nb_supprimes = fin - debut + 1

    if verbose:
        print("[INFO] Fichier: %s (%d lignes)" % (fichier, total_lignes))
        print("[INFO] Suppression des lignes %d a %d (%d ligne(s))" % (debut, fin, nb_supprimes))
        print("---")

    if dry_run:
        print("[DRY-RUN] Aucune modification appliquee")
        print("Lignes qui seraient supprimees :")
        for i in range(debut - 1, fin):
            print(toutes[i].rstrip("\r\n"))
        return 0

    # Supprimer les lignes (fichier temporaire puis remplacement)
    resultat = toutes[:debut - 1] + toutes[fin:]
    try:
        with io.open(fichier + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
            fh.writelines(resultat)
        os.remove(fichier)
        os.rename(fichier + ".tmp", fichier)
    except (IOError, OSError):
        print("[ERREUR] Echec de la suppression des lignes")
        return 1

    if verbose:
        print("[OK] %d ligne(s) supprimee(s) de %s" % (nb_supprimes, fichier))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
