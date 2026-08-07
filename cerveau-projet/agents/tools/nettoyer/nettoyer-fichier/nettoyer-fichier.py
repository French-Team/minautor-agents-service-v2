#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
nettoyer-fichier.py

Outil pour purifier un fichier markdown en supprimant le contenu
non essentiel : lignes vides consecutives, notes de rappel,
commentaires YAML inutiles.

Options:
  --dry-run     Afficher les changements SANS les appliquer
  --verbose     Afficher les details
  --backup      Creer une copie de sauvegarde (fichier.backup)
  --aide        Afficher cette aide

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

VERBOSE = False
DRY_RUN = False
BACKUP = False


def afficher_aide():
    print("Usage: nettoyer-fichier.py <fichier> [options]")
    print("")
    print("Options:")
    print("  --dry-run     Afficher les changements SANS les appliquer")
    print("  --verbose     Afficher les details")
    print("  --backup      Creer une copie de sauvegarde")
    print("  --aide        Afficher cette aide")
    print("")
    print("Exemples:")
    print("  nettoyer-fichier.py --dry-run cerveau-projet/agents/buffy/buffy.md")
    print("  nettoyer-fichier.py --verbose cerveau-projet/agents/buffy/buffy.md")
    print("  nettoyer-fichier.py cerveau-projet/agents/buffy/buffy.md")


def afficher_changement(type_chg, description, lignes):
    """Afficher un changement si verbose ou dry-run."""
    if VERBOSE or DRY_RUN:
        print("[%s] %s (%d lignes)" % (type_chg, description, lignes))


def purifier_fichier(fichier):
    """Purifier un fichier markdown."""
    if not os.path.isfile(fichier):
        print("ERREUR: Le fichier %s n'existe pas" % fichier)
        return 1

    backup = fichier + ".backup"
    temp = fichier + ".tmp"

    # TOUJOURS creer une sauvegarde avant modification
    shutil.copyfile(fichier, backup)

    if VERBOSE:
        print("=== Purification de %s ===" % os.path.basename(fichier))
        print("")

    shutil.copyfile(fichier, temp)

    lignes_supprimees = 0

    # Lire le fichier temporaire
    with io.open(temp, "r", encoding="utf-8", errors="replace") as fh:
        lignes = fh.readlines()

    # 1. Les blockquotes sont conserves par defaut pour preserver le contenu

    # 2. Supprimer les lignes vides consecutives (max une ligne vide)
    avant = len(lignes)
    propres = []
    vide_precedent = False
    for ligne in lignes:
        est_vide = ligne.strip() == ""
        if est_vide and vide_precedent:
            continue
        propres.append(ligne)
        vide_precedent = est_vide
    lignes = propres
    diff = avant - len(lignes)
    if diff > 0:
        lignes_supprimees += diff
        afficher_changement("SUPPRIME", "Lignes vides consecutives", diff)

    # 3. Supprimer les notes de rappel
    avant = len(lignes)
    notes = ("> Note:", "> Important:", "> Rappel:")
    lignes = [l for l in lignes if not any(l.startswith(prefixe) for prefixe in notes)]
    diff = avant - len(lignes)
    if diff > 0:
        lignes_supprimees += diff
        afficher_changement("SUPPRIME", "Notes de rappel", diff)

    # 4. Supprimer les commentaires YAML inutiles
    avant = len(lignes)
    commentaires = ("# Type:", "# Convention:", "# Comment devenir")
    lignes = [l for l in lignes if not any(l.startswith(prefixe) for prefixe in commentaires)]
    diff = avant - len(lignes)
    if diff > 0:
        lignes_supprimees += diff
        afficher_changement("SUPPRIME", "Commentaires YAML inutiles", diff)

    # 5. Condenser le frontmatter YAML (garder l'essentiel)
    #    NE PAS supprimer les commentaires YAML - ils peuvent etre importants
    #    (aucune suppression effective, conserve la logique du .sh)

    # 6. Reduire les blocs de code vides ou simples
    avant = len(lignes)
    resultat = []
    dans_bloc = False
    for ligne in lignes:
        if ligne.rstrip("\n").strip() == "```":
            if not dans_bloc:
                # Ouverture de bloc
                dans_bloc = True
                resultat.append(ligne)
            else:
                # Fermeture de bloc : ne garder que si le bloc n'etait pas vide
                # (vide = pas de ligne de commentaire entre les ```)
                dans_bloc = False
                resultat.append(ligne)
        elif dans_bloc:
            # Ligne de commentaire seule dans un bloc -> supprimee
            if ligne.strip().startswith("#") and ligne.strip().lstrip("#").strip() == "":
                continue
            resultat.append(ligne)
        else:
            resultat.append(ligne)
    lignes = resultat
    diff = avant - len(lignes)
    if diff > 0:
        lignes_supprimees += diff
        afficher_changement("REDUIT", "Blocs de code vides", diff)

    # 7. Les separateurs sont conserves pour preserver la structure

    lignes_avant = len(io.open(fichier, "r", encoding="utf-8", errors="replace").readlines())
    lignes_apres = len(lignes)
    total_supprime = lignes_avant - lignes_apres

    print("")
    print("=== Resume ===")
    print("Lignes avant  : %d" % lignes_avant)
    print("Lignes apres  : %d" % lignes_apres)
    print("Supprimees   : %d" % total_supprime)

    if DRY_RUN:
        print("")
        print("[DRY-RUN] Aucun changement applique")
        os.remove(temp)
    else:
        with io.open(temp, "w", encoding="utf-8", newline="\n") as fh:
            fh.writelines(lignes)
        os.remove(fichier)
        os.rename(temp, fichier)
        print("")
        print("[APPLIQUE] Fichier mis a jour")

    # Nettoyage de la sauvegarde si l'option --backup n'est pas demandee
    if not BACKUP and os.path.exists(backup):
        os.remove(backup)

    return 0


def main(argv):
    global VERBOSE, DRY_RUN, BACKUP

    if not argv:
        afficher_aide()
        return 0

    fichier = ""
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--aide", "--help", "-h"):
            afficher_aide()
            return 0
        if arg == "--version":
            print("nettoyer-fichier v%s (%s)" % (VERSION, STATUT))
            return 0
        if arg == "--dry-run":
            DRY_RUN = True
        elif arg == "--verbose":
            VERBOSE = True
        elif arg == "--backup":
            BACKUP = True
        else:
            fichier = arg
        i += 1

    if not fichier:
        print("ERREUR: Fichier non specifie")
        afficher_aide()
        return 1

    return purifier_fichier(fichier)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
