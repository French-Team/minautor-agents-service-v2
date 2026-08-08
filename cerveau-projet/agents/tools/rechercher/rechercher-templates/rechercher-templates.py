#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
rechercher-templates.py

Rechercher les fichiers template dans le projet.

Options:
  --mode nom          Rechercher par nom (contient 'template') - defaut
  --mode frontmatter  Rechercher les fichiers avec un frontmatter de template
  --mode contenu      Rechercher les fichiers contenant 'template' dans le contenu
  --tous              Combiner tous les modes
  --extensions        Extensions a chercher (defaut: md)
  --exclure           Dossiers a exclure (defaut: .git,node_modules,.agents)
  --verbose           Afficher les details
  --help              Afficher cette aide

Proprietaire : Buffy (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"

MARQUEURS = ("template", "modele", "placeholder")


def afficher_aide():
    print("=== rechercher-templates v%s ===" % VERSION)
    print("")
    print("Usage: rechercher-templates.py [OPTIONS] [DOSSIER]")
    print("")
    print("Options :")
    print("  --mode nom          Rechercher par nom (contient 'template') - defaut")
    print("  --mode frontmatter  Rechercher les fichiers avec un frontmatter de template")
    print("  --mode contenu      Rechercher les fichiers contenant 'template' dans le contenu")
    print("  --tous              Combiner tous les modes")
    print("  --extensions        Extensions a chercher (defaut: md)")
    print("  --exclure           Dossiers a exclure (defaut: .git,node_modules,.agents)")
    print("  --verbose           Afficher les details")
    print("  --help              Afficher cette aide")


def est_template_nom(fichier):
    """Verifier si un fichier est un template (par nom)."""
    return "template" in os.path.basename(fichier).lower()


def est_template_frontmatter(fichier):
    """Verifier si un fichier a un frontmatter de template."""
    try:
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            lignes = [fh.readline().rstrip("\r\n")]
            if lignes[0] != "---":
                return False
            for _ in range(14):
                ligne = fh.readline().rstrip("\r\n")
                if ligne == "":
                    break
                lignes.append(ligne)
    except IOError:
        return False
    contenu = "\n".join(lignes).lower()
    return any(m in contenu for m in MARQUEURS)


def est_template_contenu(fichier):
    """Verifier si un fichier mentionne 'template' dans son contenu."""
    try:
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            contenu = fh.read(200000).lower()
    except IOError:
        return False
    return any(m in contenu for m in MARQUEURS)


def main(argv):
    dossier = "."
    extensions = "md"
    exclure = ".git,node_modules,.agents"
    verbose = False
    help_demande = False
    mode = "nom"
    tous = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--mode" and i + 1 < len(argv):
            mode = argv[i + 1]
            i += 2
            continue
        if arg == "--extensions" and i + 1 < len(argv):
            extensions = argv[i + 1]
            i += 2
            continue
        if arg == "--exclure" and i + 1 < len(argv):
            exclure = argv[i + 1]
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
            print("rechercher-templates v%s (%s)" % (VERSION, STATUT))
            return 0
        dossier = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    if not os.path.isdir(dossier):
        print("[ERREUR] Le dossier n'existe pas : %s" % dossier)
        return 1

    print("=== Recherche de templates ===")
    print("Dossier : %s" % dossier)
    if tous:
        print("Mode : tous (nom + frontmatter + contenu)")
    else:
        print("Mode : %s" % mode)
    print("Extensions : %s" % extensions)
    print("")

    ext_liste = [e.strip() for e in extensions.split(",") if e.strip()]
    excl_dirs = [d for d in exclure.split(",") if d]

    total_fichiers = 0
    templates_trouves = 0
    fichiers_ok = 0

    for racine, dossiers, fichiers in os.walk(dossier):
        dossiers[:] = [d for d in dossiers if d not in excl_dirs and not d.startswith(".")]
        for nom in fichiers:
            if not any(nom.endswith("." + ext) for ext in ext_liste):
                continue
            chemin = os.path.join(racine, nom)
            if not os.path.isfile(chemin):
                continue
            total_fichiers += 1
            est_template = False
            raisons = []

            if (mode == "nom" or tous) and est_template_nom(chemin):
                est_template = True
                raisons.append("nom")
            if (mode == "frontmatter" or tous) and not est_template and est_template_frontmatter(chemin):
                est_template = True
                raisons.append("frontmatter")
            if (mode == "contenu" or tous) and not est_template and est_template_contenu(chemin):
                est_template = True
                raisons.append("contenu")

            if est_template:
                templates_trouves += 1
                print("  [TEMPLATE] %s" % chemin)
                if verbose:
                    print("        -> detecte par : %s" % "|".join(raisons))
            else:
                fichiers_ok += 1

    print("")
    print("=== Resume ===")
    print("Fichiers trouves : %d" % total_fichiers)
    print("Templates detectes : %d" % templates_trouves)
    print("Fichiers non-templates : %d" % fichiers_ok)

    if templates_trouves == 0:
        print("")
        print("[ATTENTION] Aucun template trouve")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
