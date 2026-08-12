#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-liens.py

Valide les liens dans un fichier Markdown : liens internes (existence
du fichier/dossier cible) et liens externes (http/https, non verifies).

Utilisation:
  valider-liens.py [OPTIONS] FICHIER

Options:
  --aide, -h          Afficher l'aide
  --verbose, -v       Afficher les details
  --version           Afficher la version
  --racine RACINE     Racine du projet (defaut: .)

Proprietaire : Vulcain (outil partage)
Version : 0.4.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.4.0-py"
STATUT = "prepare"

PATTERN_LIEN = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


def afficher_aide():
    print("==========================================")
    print("  valider-liens v%s" % VERSION)
    print("  Valide les liens dans un fichier Markdown")
    print("==========================================")
    print("")
    print("Usage: valider-liens.py [OPTIONS] FICHIER")
    print("")
    print("Options:")
    print("  --aide, -h          Afficher cette aide")
    print("  --verbose, -v       Afficher les details")
    print("  --version           Afficher la version")
    print("  --racine RACINE     Racine du projet (defaut: .)")
    print("")
    print("Arguments:")
    print("  FICHIER             Fichier Markdown a valider")
    print("")
    print("Exemples:")
    print("  valider-liens.py fichier.md")
    print("  valider-liens.py --verbose --racine /chemin/projet autre-fichier.md")


def normaliser_chemin(dossier_fichier, chemin):
    """Normaliser un chemin relatif depuis le dossier du fichier."""
    chemin_propre = chemin.split("#")[0]
    if not chemin_propre.strip():
        return ""
    # Repertoire absolu du dossier du fichier
    base = os.path.abspath(dossier_fichier)
    chemin_abs = os.path.normpath(os.path.join(base, chemin_propre))
    return chemin_abs


def valider_liens(fichier, verbose, racine):
    liens_valides = 0
    liens_invalides = 0
    liens_externes = 0

    dossier_fichier = os.path.dirname(os.path.abspath(fichier))

    print("[LIEN] Validation des liens dans : %s" % fichier)
    print("[DOSSIER] Repertoire du fichier : %s" % dossier_fichier)
    print("")

    try:
        with io.open(fichier, encoding="utf-8") as fh:
            contenu = fh.read()
    except Exception:
        print("[ERREUR] Impossible de lire le fichier : %s" % fichier)
        return 1

    liens = PATTERN_LIEN.findall(contenu)

    if not liens:
        print("Aucun lien Markdown trouve.")
        return 0

    total = len(liens)
    print("Trouve %d lien(s) Markdown" % total)
    print("")

    for texte, chemin in liens:
        texte = texte.strip()
        chemin = chemin.strip()

        if re.match(r"^https?://", chemin):
            liens_externes += 1
            if verbose:
                print("[LIEN] %s -> %s (externe)" % (texte, chemin))
            continue

        if not chemin:
            # Lien vide (ex: image placeholder) - ignore
            continue

        chemin_complet = normaliser_chemin(dossier_fichier, chemin)

        if os.path.exists(chemin_complet):
            liens_valides += 1
            if verbose:
                print("[OK] %s -> %s" % (texte, chemin))
        else:
            liens_invalides += 1
            print("[ERREUR] %s -> %s" % (texte, chemin))
            if verbose:
                print("   Chemin verifie : %s" % chemin_complet)

    print("")
    print("Resume :")
    print("[OK] Liens valides : %d" % liens_valides)
    print("[ERREUR] Liens invalides : %d" % liens_invalides)
    print("[LIEN] Liens externes : %d" % liens_externes)

    return 1 if liens_invalides > 0 else 0


def main(argv):
    fichier = ""
    verbose = False
    racine = "."

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--aide", "-h"):
            afficher_aide()
            return 0
        if arg in ("--verbose", "-v"):
            verbose = True
        elif arg == "--version":
            print("valider-liens v%s" % VERSION)
            return 0
        elif arg == "--racine":
            if i + 1 < len(argv):
                racine = argv[i + 1]
                i += 1
        elif arg.startswith("-"):
            print("Option inconnue: %s" % arg)
            print("Utilisez --aide pour l'aide")
            return 1
        else:
            fichier = arg
        i += 1

    if not fichier:
        print("Erreur: Aucun fichier specifie")
        print("Utilisez --aide pour l'aide")
        return 1

    if not os.path.isfile(fichier):
        print("Erreur: Le fichier '%s' n'existe pas" % fichier)
        return 1

    return valider_liens(fichier, verbose, racine)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
