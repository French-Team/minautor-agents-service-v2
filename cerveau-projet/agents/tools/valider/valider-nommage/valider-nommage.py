#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
valider-nommage.py

Verifie que le nommage est correct selon les conventions :
protocole (nom.XX.XX.statut.md), agent (nom-agent.md),
outil (nom-outil.sh/py/md avec prefixe du dossier),
convention (convention-nom.md). Mode recursif pour valider
tous les outils d'un dossier.

Utilisation:
  valider-nommage.py [OPTIONS] CHEMIN

Options:
  --aide, -h          Afficher l'aide
  --verbose, -v       Afficher les details
  --version           Afficher la version
  --type TYPE         Type de fichier (protocole, convention, agent, outil)
  --recursive, -r     Valider tous les outils d'un dossier

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"

STATUTS_VALIDES = ("ebauche", "prepare", "dev", "test", "valide")

PATTERN_PROTOCOLE = re.compile(r"^([a-zA-Z0-9_-]+)\.(\d+)\.(\d+)\.([a-zA-Z]+)\.md$")
PATTERN_AGENT = re.compile(r"^[a-z]+\.md$")
PATTERN_OUTIL = re.compile(r"^[a-z-]+\.(sh|py|md)$")
PATTERN_CONVENTION = re.compile(r"^convention-[a-z-]+\.md$")


def afficher_aide():
    print("==========================================")
    print("  valider-nommage v%s" % VERSION)
    print("  Verifier le nommage selon les conventions")
    print("==========================================")
    print("")
    print("Usage: valider-nommage.py [OPTIONS] CHEMIN")
    print("")
    print("Options:")
    print("  --aide, -h          Afficher cette aide")
    print("  --verbose, -v       Afficher les details")
    print("  --version           Afficher la version")
    print("  --type TYPE         Type de fichier (protocole, convention, agent, outil)")
    print("  --recursive, -r     Valider tous les outils d'un dossier (ignore --type)")
    print("")
    print("Types de fichiers:")
    print("  protocole     nom-protocole.XX.XX.statut.md")
    print("  agent         nom-agent.md")
    print("  outil         nom-outil.sh, nom-outil.py ou nom-outil.md")
    print("  convention    convention-nom.md")
    print("")
    print("Statuts valides (protocoles):")
    print("  ebauche, prepare, dev, test, valide")
    print("")
    print("Exemples:")
    print("  valider-nommage.py --type protocole chemin/vers/protocole.md")
    print("  valider-nommage.py --type agent chemin/vers/agent.md")
    print("  valider-nommage.py --recursive cerveau-projet/agents/tools/")


def valider_protocole(fichier, verbose):
    basename = os.path.basename(fichier)
    erreurs = 0

    print("[CHECKLIST] Validation du nommage : %s" % basename)
    print("")

    m = PATTERN_PROTOCOLE.match(basename)
    if not m:
        print("  [ERREUR] Format invalide : %s" % basename)
        print("    Attendu : nom-protocole.XX.XX.statut.md")
        return 1

    nom_part, major_part, minor_part, statut_part = m.groups()

    statut = statut_part
    if statut not in STATUTS_VALIDES:
        print("  [ERREUR] Statut invalide : %s" % statut)
        print("    Statuts valides : ebauche, prepare, dev, test, valide")
        return 1

    print("  [OK] Format valide : %s" % basename)
    if verbose:
        print("    Nom : %s" % nom_part)
        print("    Version : %s.%s" % (major_part, minor_part))
        print("    Statut : %s" % statut)
    return 0


def valider_agent(fichier, verbose):
    basename = os.path.basename(fichier)

    print("[CHECKLIST] Validation du nommage : %s" % basename)
    print("")

    if PATTERN_AGENT.match(basename):
        print("  [OK] Format valide : %s" % basename)
        return 0
    print("  [ERREUR] Format invalide : %s" % basename)
    print("    Attendu : nom-agent.md")
    return 1


def valider_convention(fichier, verbose):
    basename = os.path.basename(fichier)

    print("[CHECKLIST] Validation du nommage : %s" % basename)
    print("")

    if PATTERN_CONVENTION.match(basename):
        print("  [OK] Format valide : %s" % basename)
        return 0
    print("  [ERREUR] Format invalide : %s" % basename)
    print("    Attendu : convention-nom.md")
    return 1


def valider_outil(fichier, verbose, categorie=None):
    basename = os.path.basename(fichier)
    erreurs = 0

    print("[CHECKLIST] Validation du nommage : %s" % basename)
    print("")

    if not PATTERN_OUTIL.match(basename):
        print("  [ERREUR] Format invalide : %s" % basename)
        print("    Attendu : nom-outil.sh, nom-outil.py ou nom-outil.md")
        erreurs += 1

    nom = re.sub(r"\.(sh|py|md)$", "", basename)

    if not categorie:
        dossier_outil = os.path.dirname(os.path.abspath(fichier))
        categorie = os.path.basename(os.path.dirname(dossier_outil))

    if categorie and (nom == categorie or nom.startswith(categorie + "-")):
        if verbose:
            print("  [OK] Prefixe dossier respecte : %s/" % categorie)
    else:
        print("  [ERREUR] Prefixe dossier manquant : %s" % basename)
        print("    Le nom doit commencer par '%s-' (dossier: %s/)" % (categorie, categorie))
        erreurs += 1

    return erreurs


def valider_recursif(dossier, verbose):
    total = 0
    ok = 0
    ko = 0

    print("=== Validation recursive des outils dans : %s ===" % dossier)
    print("")

    # Structure: tools/categorie/outil/
    if not os.path.isdir(dossier):
        print("Erreur: '%s' n'est pas un dossier" % dossier)
        return 1

    try:
        entrees = sorted(os.listdir(dossier))
    except OSError:
        print("Erreur: Impossible de lire le dossier '%s'" % dossier)
        return 1

    for categorie_nom in entrees:
        chemin_cat = os.path.join(dossier, categorie_nom)
        if not os.path.isdir(chemin_cat):
            continue
        try:
            sous = sorted(os.listdir(chemin_cat))
        except OSError:
            continue
        for outil_nom in sous:
            chemin_outil = os.path.join(chemin_cat, outil_nom)
            if not os.path.isdir(chemin_outil):
                continue
            for f in sorted(os.listdir(chemin_outil)):
                if f.endswith((".sh", ".py", ".md")):
                    total += 1
                    code = valider_outil(os.path.join(chemin_outil, f), verbose, categorie_nom)
                    if code == 0:
                        ok += 1
                    else:
                        ko += 1
                    print("")

    print("=== Resume ===")
    print("  Total : %d" % total)
    print("  OK : %d" % ok)
    if ko > 0:
        print("  Erreurs : %d" % ko)
    else:
        print("  Erreurs : 0")
    return ko


def main(argv):
    verbose = False
    type_fichier = ""
    fichier = ""
    recursif = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--aide", "-h"):
            afficher_aide()
            return 0
        if arg in ("--verbose", "-v"):
            verbose = True
        elif arg == "--version":
            print("valider-nommage v%s" % VERSION)
            return 0
        elif arg == "--type":
            if i + 1 < len(argv):
                type_fichier = argv[i + 1]
                i += 1
        elif arg in ("--recursive", "-r"):
            recursif = True
        elif arg.startswith("-"):
            print("Option inconnue: %s" % arg)
            print("Utilisez --aide pour l'aide")
            return 1
        else:
            fichier = arg
        i += 1

    if recursif:
        if not fichier:
            print("Erreur: Aucun dossier specifie pour --recursive")
            return 1
        return valider_recursif(fichier, verbose)

    if not fichier:
        print("Erreur: Aucun fichier specifie")
        print("Utilisez --aide pour l'aide")
        return 1

    if not os.path.isfile(fichier):
        print("Erreur: Le fichier '%s' n'existe pas" % fichier)
        return 1

    if not type_fichier:
        print("Erreur: Type non specifie")
        print("Utilisez --type pour specifier le type")
        return 1

    if type_fichier == "protocole":
        return valider_protocole(fichier, verbose)
    if type_fichier == "agent":
        return valider_agent(fichier, verbose)
    if type_fichier == "outil":
        return valider_outil(fichier, verbose)
    if type_fichier == "convention":
        return valider_convention(fichier, verbose)

    print("Erreur: Type inconnu '%s'" % type_fichier)
    print("Types disponibles : protocole, agent, outil, convention")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
