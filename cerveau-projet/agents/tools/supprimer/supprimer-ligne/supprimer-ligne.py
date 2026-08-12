#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
supprimer-ligne.py

Supprimer une ligne (ou une plage) par numero dans un fichier.

Arguments:
  <fichier>       Fichier a modifier
  <ligne>         Numero de la ligne a supprimer (1 = premiere)
  [ligne-fin]     Derniere ligne de la plage a supprimer (defaut = ligne)

Options:
  --backup        Creer une sauvegarde .bak avant
  --dry-run       Simuler sans modifier
  --verbose       Afficher les details
  --help          Afficher cette aide
  --version       Afficher la version

Retour : 0 si succes, 1 si erreur ou si la ligne demandee n'existe pas
         (echec explicite : jamais 0 silencieux).

Proprietaire : Buffy (outil partage)
Version : 0.3.1
Statut : prepare
"""

import io
import os
import shutil
import sys

VERSION = "0.3.2"
STATUT = "prepare"

NOM_ATTENDU = "supprimer-ligne.py"

# Securite (round 3) : force la sortie en UTF-8 pour ne jamais crasher sur
# l'encodage de la console (cp1252 sous Windows avec des caracteres non-ASCII).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass  # Python < 3.7 : la console gere l'encodage comme elle peut


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    if nom_script != NOM_ATTENDU:
        print("[ERREUR] Nom de fichier invalide : %s" % nom_script)
        print("  Attendu : %s" % NOM_ATTENDU)
        sys.exit(2)


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
    print("  --backup        Creer une sauvegarde .bak avant")
    print("  --dry-run       Simuler sans modifier")
    print("  --verbose       Afficher les details")
    print("  --help          Afficher cette aide")
    print("  --version       Afficher la version")
    print("")
    print("Retour : 0 si succes, 1 si erreur ou si la ligne n'existe pas.")


def main(argv):
    verifier_nommage(os.path.basename(sys.argv[0]))

    fichier = ""
    ligne = ""
    ligne_fin = ""
    backup = False
    dry_run = False
    verbose = False
    help_demande = False

    for arg in argv:
        if arg == "--dry-run":
            dry_run = True
        elif arg == "--backup":
            backup = True
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

    # Securite (round 3) : octet nul dans le chemin -> refus explicite
    if "\x00" in fichier:
        print("[ERREUR] Chemin non sur (octet nul present)")
        return 1

    # Securite (round 3) : refus de modifier a travers un lien symbolique
    # (l'ecriture suivrait le lien vers la cible a l'insu de l'agent)
    if os.path.islink(fichier):
        print("[ERREUR] Chemin est un lien symbolique (refus securite): %s" % fichier)
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

    # Lecture robuste (round 3) : UTF-8-sig puis fallback latin-1, jamais de crash
    try:
        with io.open(fichier, "r", encoding="utf-8-sig") as fh:
            toutes = fh.readlines()
    except (UnicodeDecodeError, IOError):
        try:
            with io.open(fichier, "r", encoding="latin-1") as fh:
                toutes = fh.readlines()
        except IOError:
            print("[ERREUR] Impossible de lire le fichier: %s" % fichier)
            return 1

    total_lignes = len(toutes)

    if debut > total_lignes:
        # Robustesse (round 4) : pluriel correct ("1 ligne" vs "N lignes")
        mot = "ligne" if total_lignes == 1 else "lignes"
        print("[ERREUR] Le fichier n'a que %d %s, ligne %d inexistante"
              % (total_lignes, mot, debut))
        return 1

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

    if backup:
        shutil.copy2(fichier, fichier + ".bak")
        if verbose:
            print("[INFO] Sauvegarde: %s.bak" % fichier)

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
