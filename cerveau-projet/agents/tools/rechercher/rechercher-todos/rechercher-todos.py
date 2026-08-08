#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
rechercher-todos.py

Rechercher les todos existants et eviter les doublons.

Options:
  --theme <motif>   Rechercher les todos dont le theme est identique ou proche
  --tous            Lister tous les todos existants (inventaire complet)
  --dossier <chemin> Dossier de recherche (defaut: racine du projet)
  --verbose         Afficher les details de correspondance
  --help            Afficher cette aide

Proprietaire : Minerve (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"

PREFIX = "todo"
LABEL = "todos"


def afficher_aide():
    print("=== rechercher-todos v%s ===" % VERSION)
    print("")
    print("Usage: rechercher-todos.py [OPTIONS]")
    print("")
    print("Options :")
    print("  --theme <motif>   Rechercher les todos dont le theme est identique ou proche")
    print("  --tous            Lister tous les todos existants (inventaire complet)")
    print("  --dossier <chemin> Dossier de recherche (defaut: racine du projet)")
    print("  --verbose         Afficher les details de correspondance")
    print("  --help            Afficher cette aide")


def extraire_theme(fichier):
    """Extraire le theme d'un fichier (la partie apres le prefixe, avant le premier point)."""
    nom_base = os.path.basename(fichier)
    nom = nom_base[len(PREFIX) + 1:] if nom_base.startswith(PREFIX + "-") else nom_base
    return nom.split(".")[0]


def extraire_statut(fichier):
    """Extraire le statut d'un fichier (la partie avant .md)."""
    m = re.search(r"\.([a-z-]+)\.md$", os.path.basename(fichier))
    return m.group(1) if m else ""


def normaliser(texte):
    """Normaliser un theme pour la comparaison (minuscules, _ et espaces -> -)."""
    return re.sub(r"-+", "-", texte.lower().replace("_", "-").replace(" ", "-"))


def correspond(motif, theme):
    """Verifier si un theme correspond au motif (exact, partiel, ou mots-cles partages)."""
    if motif == theme:
        return "EXACT"
    if motif in theme or theme in motif:
        return "PROCHE"
    for mot in motif.split("-"):
        if len(mot) >= 4 and mot in theme.split("-"):
            return "PARTIEL"
    return "AUCUN"


def recueillir_fichiers(dossier):
    """Recueillir tous les fichiers <prefixe>-*.md (hors templates et index)."""
    fichiers = []
    for racine, dossiers, fichiers_local in os.walk(dossier):
        dossiers[:] = [d for d in dossiers if d != ".git" and d != "node_modules"]
        for nom in fichiers_local:
            if not nom.startswith(PREFIX + "-") or not nom.endswith(".md"):
                continue
            if nom.endswith("-template.md") or nom.startswith("index-"):
                continue
            fichiers.append(os.path.join(racine, nom))
    return fichiers


def main(argv):
    motif = ""
    tous = False
    dossier = "."
    verbose = False
    help_demande = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--theme" and i + 1 < len(argv):
            motif = argv[i + 1]
            i += 2
            continue
        if arg == "--dossier" and i + 1 < len(argv):
            dossier = argv[i + 1]
            i += 2
            continue
        if arg == "--tous":
            tous = True
            i += 1
            continue
        if arg in ("--verbose", "-v"):
            verbose = True
            i += 1
            continue
        if arg in ("--help", "--aide", "-h"):
            help_demande = True
            i += 1
            continue
        if arg == "--version":
            print("rechercher-todos v%s (%s)" % (VERSION, STATUT))
            return 0
        print("[ERREUR] Option inconnue : %s" % arg)
        afficher_aide()
        return 1

    if help_demande:
        afficher_aide()
        return 0

    if not os.path.isdir(dossier):
        print("[ERREUR] Le dossier n'existe pas : %s" % dossier)
        return 1

    fichiers = recueillir_fichiers(dossier)

    if not fichiers:
        print("[ATTENTION] Aucun %s trouve" % LABEL)
        return 0

    # Mode inventaire complet
    if tous or not motif:
        print("=== Inventaire des %s ===" % LABEL)
        print("Dossier : %s" % dossier)
        print("")
        print("  %-40s %-30s %s" % ("THEME", "FICHIER", "STATUT"))
        print("  " + "-" * 70)
        for f in fichiers:
            theme = extraire_theme(f)
            statut = extraire_statut(f)
            print("  %-40s %-30s %s" % (theme, os.path.basename(f), statut))
        print("")
        print("Total : %d %s" % (len(fichiers), LABEL))
        return 0

    # Mode anti-doublon (avec motif)
    motif_norm = normaliser(motif)
    print("=== Recherche anti-doublon : theme '%s' ===" % motif)
    print("")
    trouves = 0
    for f in fichiers:
        theme = extraire_theme(f)
        theme_norm = normaliser(theme)
        resultat = correspond(motif_norm, theme_norm)
        if resultat != "AUCUN":
            trouves += 1
            print("  [%s] %s -> %s" % (resultat, theme, os.path.basename(f)))
            if verbose:
                print("        motif: '%s' | theme: '%s' | score: %s" % (motif, theme, resultat))

    print("")
    if trouves == 0:
        print("[OK] Aucun doublon trouve pour le theme '%s'. Vous pouvez creer le fichier." % motif)
        return 0
    else:
        print("[ATTENTION] %d correspondance(s) trouvee(s). Verifiez avant de creer." % trouves)
        print("-> Ne pas creer si un [EXACT] ou [PROCHE] existe deja.")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
