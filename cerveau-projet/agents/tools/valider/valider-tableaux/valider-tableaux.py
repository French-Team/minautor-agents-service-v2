#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-tableaux.py

Verifie la coherence des tableaux des fiches agents :
  1. Nombres d'etapes annonces vs lignes reelles (tableau des missions)
  2. Numerotation continue des tableaux numerotes (etapes, points de controle)
  3. Completude des listes d'agents (Agents disponibles vs fiches existantes)

Utilisation:
  valider-tableaux.py [OPTIONS] [FICHIER|DOSSIER]

Arguments :
  [FICHIER]  Verifier un fichier fiche agent (ex: buffy.md)
  [DOSSIER]  Verifier toutes les fiches d'un dossier (defaut: agents/)

Options :
  --agent <nom>       Verifier la fiche d'un agent precis
  --detail            Afficher le detail complet des verifications
  --help              Afficher cette aide

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

# Racine du projet : 5 niveaux au-dessus de ce script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(SCRIPT_DIR, "../../../../.."))

DOSSIER_DEFAUT = os.path.join(RACINE, "cerveau-projet", "agents")


def afficher_aide():
    print("=== valider-tableaux v%s ===" % VERSION)
    print("")
    print("Verifie la coherence des tableaux des fiches agents :")
    print("  1. Nombres d'etapes annonces vs lignes reelles (missions)")
    print("  2. Numerotation continue des tableaux numerotes")
    print("  3. Completude des listes d'agents")
    print("")
    print("Usage: valider-tableaux.py [OPTIONS] [FICHIER|DOSSIER]")
    print("")
    print("Arguments :")
    print("  [FICHIER]  Verifier un fichier fiche agent (ex: buffy.md)")
    print("  [DOSSIER]  Verifier toutes les fiches d'un dossier (defaut: agents/)")
    print("")
    print("Options :")
    print("  --agent <nom>       Verifier la fiche d'un agent precis")
    print("  --detail            Afficher le detail complet des verifications")
    print("  --help              Afficher cette aide")


# --- 1. Verification: nombres annonces vs lignes reelles ---
def verifier_nombres_annonces(fichier):
    c = io.open(fichier, encoding="utf-8").read()
    lignes = c.split("\n")
    annonces = []   # (mission, nombre annonce)
    details = {}    # mission -> lignes d'etapes
    in_tab = False
    for l in lignes:
        if re.match(r"^#{2,3} .*[Mm]issions [Dd]isponibles", l):
            in_tab = True
            continue
        if in_tab:
            if re.match(r"^#{2,3} ", l):
                in_tab = False
            else:
                m = re.match(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(\d+)\s*etapes?\s*\|", l)
                if m:
                    annonces.append((m.group(1).strip(), int(m.group(2))))
    in_sec = False
    nom = None
    for l in lignes:
        m = re.match(r"^### Mission : (.+)$", l)
        if m:
            nom = m.group(1).strip()
            details.setdefault(nom, 0)
            in_sec = True
            continue
        if in_sec:
            if re.match(r"^#{2,3} ", l):
                in_sec = False
                continue
            if re.match(r"^\|\s*(\*{0,2}\d+\*{0,2}|\*{0,2}FIN\*{0,2})\s*\|", l):
                details[nom] += 1
    erreurs = []
    for nom_annonce, nb in annonces:
        candidats = [d for d in details if d == nom_annonce or d.startswith(nom_annonce + " (")]
        if candidats:
            reel = details[candidats[0]]
            if reel != nb:
                erreurs.append('  [NOMBRES] %s : "%s" annonce %d etapes, section en contient %d' % (
                    os.path.basename(fichier), nom_annonce, nb, reel))
        else:
            erreurs.append('  [NOMBRES] %s : "%s" annonce %d etapes mais AUCUNE section trouvee' % (
                os.path.basename(fichier), nom_annonce, nb))
    return erreurs


# --- 2. Verification: numerotation continue (doublons + trous) ---
def analyser_numeros(section, numeros, fichier):
    erreurs = []
    vus = {}
    for n in numeros:
        vus[n] = vus.get(n, 0) + 1
    for n, count in vus.items():
        if count > 1:
            erreurs.append('  [NUMEROTATION] %s : section "%s" -- numero %d en double (x%d)' % (
                os.path.basename(fichier), section, n, count))
    uniq = sorted(vus.keys())
    if uniq and uniq[0] in (0, 1):
        debut = uniq[0]
        attendu = list(range(debut, max(uniq) + 1))
        manquants = [x for x in attendu if x not in vus]
        if manquants:
            erreurs.append('  [NUMEROTATION] %s : section "%s" -- numeros manquants : %s' % (
                os.path.basename(fichier), section, manquants))
    return erreurs


def verifier_numerotation(fichier):
    c = io.open(fichier, encoding="utf-8").read()
    lignes = c.split("\n")
    erreurs = []
    section = "(debut)"
    numeros = []
    in_table = False
    for l in lignes:
        m = re.match(r"^(#{1,3}) (.+)$", l)
        if m:
            if in_table and numeros:
                erreurs.extend(analyser_numeros(section, numeros, fichier))
                numeros = []
                in_table = False
            section = m.group(2).strip()
            continue
        if l.strip().startswith("|"):
            m2 = re.match(r"^\|\s*(\*{0,2}\d+\*{0,2})\s*\|", l.strip())
            if m2:
                if not in_table:
                    in_table = True
                    numeros = []
                numeros.append(int(m2.group(1).replace("*", "")))
            elif in_table:
                erreurs.extend(analyser_numeros(section, numeros, fichier))
                numeros = []
                in_table = False
        else:
            if in_table and numeros:
                erreurs.extend(analyser_numeros(section, numeros, fichier))
                numeros = []
                in_table = False
    if in_table and numeros:
        erreurs.extend(analyser_numeros(section, numeros, fichier))
    return erreurs


# --- 3. Verification: completude des listes d'agents ---
def analyser_liste(listes, agents_dossiers, fichier):
    erreurs = []
    attends = [a for a in agents_dossiers if a.lower() != "cerberus"]
    manquants = [a for a in attends if a.lower() not in [x.lower() for x in listes]]
    if manquants:
        erreurs.append('  [COMPLETUDE] %s : agents absents de la liste : %s' % (
            os.path.basename(fichier), ", ".join(manquants)))
    fantomes = [x for x in listes if x.lower() not in agents_dossiers]
    if fantomes:
        erreurs.append('  [COMPLETUDE] %s : agents listes mais inexistants : %s' % (
            os.path.basename(fichier), ", ".join(fantomes)))
    return erreurs


def verifier_liste_agents(fichier_cerberus):
    erreurs = []
    agents_dossiers = []
    agents_dir = os.path.join(RACINE, "cerveau-projet", "agents")
    if os.path.isdir(agents_dir):
        for d in sorted(os.listdir(agents_dir)):
            if os.path.isdir(os.path.join(agents_dir, d)) and os.path.exists(
                    os.path.join(agents_dir, d, d + ".md")):
                agents_dossiers.append(d)
    if not os.path.exists(fichier_cerberus):
        return erreurs
    c = io.open(fichier_cerberus, encoding="utf-8").read()
    lignes = c.split("\n")
    in_tab = False
    listes = []
    for l in lignes:
        if re.match(r"^#{2,3} .*[Aa]gents [Dd]isponibles", l):
            in_tab = True
            listes = []
            continue
        if in_tab:
            if re.match(r"^#{2,3} ", l):
                if listes:
                    erreurs.extend(analyser_liste(listes, agents_dossiers, fichier_cerberus))
                    listes = []
                in_tab = False
                continue
            m = re.match(r"^\|\s*\*\*(.+?)\*\*\s*\|", l)
            if m:
                listes.append(m.group(1).strip())
    if listes:
        erreurs.extend(analyser_liste(listes, agents_dossiers, fichier_cerberus))
    return erreurs


def main(argv):
    cible = ""
    agent = ""
    detail = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--help", "-h"):
            afficher_aide()
            return 0
        if arg == "--version":
            print("valider-tableaux v%s (%s)" % (VERSION, STATUT))
            return 0
        elif arg == "--agent":
            if i + 1 < len(argv):
                agent = argv[i + 1]
                i += 1
        elif arg == "--detail":
            detail = True
        elif arg.startswith("-"):
            print("ERREUR: option inconnue: %s" % arg)
            afficher_aide()
            return 1
        else:
            cible = arg
        i += 1

    if agent:
        cible = os.path.join(DOSSIER_DEFAUT, agent, agent + ".md")
    elif not cible:
        cible = DOSSIER_DEFAUT

    erreurs = []
    fichiers = []
    if os.path.isfile(cible):
        fichiers = [cible]
    elif os.path.isdir(cible):
        # 1) fiches .md directes dans le dossier (chemins complets, comme le .sh)
        for f in sorted(os.listdir(cible)):
            if f.endswith(".md"):
                chemin = os.path.join(cible, f)
                if os.path.isfile(chemin):
                    fichiers.append(chemin)
        # 2) fiches dans les sous-dossiers (pattern agent/agent.md)
        for a in sorted(os.listdir(cible)):
            f = os.path.join(cible, a, a + ".md")
            if os.path.exists(f) and f not in fichiers:
                fichiers.append(f)
    else:
        print("ERREUR: cible introuvable: %s" % cible)
        return 1

    fichiers_ok = 0
    for f in fichiers:
        err_f = []
        err_f += verifier_nombres_annonces(f)
        err_f += verifier_numerotation(f)
        if os.path.basename(f) == "cerberus.md":
            err_f += verifier_liste_agents(f)
        if err_f:
            erreurs.extend(err_f)
        else:
            fichiers_ok += 1

    print("=== valider-tableaux : rapport ===")
    print("Fichiers analyses : %d | Conformes : %d | Problemes : %d" % (
        len(fichiers), fichiers_ok, len(erreurs)))
    print("")
    if erreurs:
        for e in erreurs:
            print(e)
        print("")
        print("=== Resultat : NON CONFORME (%d probleme(s)) ===" % len(erreurs))
        return 1
    print("=== Resultat : CONFORME ===")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
