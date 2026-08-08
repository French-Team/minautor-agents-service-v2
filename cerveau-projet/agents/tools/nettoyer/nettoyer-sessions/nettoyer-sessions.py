#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
nettoyer-sessions.py

Supprime TOUTES les sessions LLM existantes (etats actifs uniquement) :
  - AGENTS.md          : blocs '### Session : session-llm-N' + section '## Sessions connues'
  - classeur-variables : lignes 'profil-session-*'
Le frontmatter, l'entete et le reste de chaque fichier sont PRESERVES.
AGENTS-historique.md (le journal) n'est JAMAIS modifie : c'est un temoignage.

Actions:
  nettoyer-sessions.py [options]

Options:
  --dry-run   Afficher ce qui serait supprime sans ecrire
  --verbose   Afficher les details
  --version   Afficher la version

Variables d'environnement (tests sur copies) :
  AGENTS_FILE          - surcharger le chemin de AGENTS.md
  CLASSEUR_STOCKAGE    - surcharger le chemin du classeur-variables

Proprietaire : Vulcain
Version : 0.1.0
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.1.0"
STATUT = "prepare"

AGENTS_FILE = os.environ.get("AGENTS_FILE", "AGENTS.md")
CLASSEUR_STOCKAGE = os.environ.get(
    "CLASSEUR_STOCKAGE", "cerveau-projet/agents/classeur-variables/stockage/variables-actuelles.md"
)

# Section dont on supprime TOUT le contenu dans AGENTS.md (jusqu'a la section suivante)
SECTIONS_A_SUPPRIMER = ("## Sessions LLM", "## Sessions connues")


def verifier_ascii(chaine):
    """Retourner True si la chaine est 100% ASCII."""
    return all(ord(c) < 128 for c in chaine)


def nettoyer_agents(dry_run=False, verbose=False):
    """Supprimer les blocs session + la table Sessions connues d'AGENTS.md.
    Retourne le nombre de lignes supprimees, ou 0 si le fichier est absent."""
    if not os.path.isfile(AGENTS_FILE):
        print("WARNING: %s introuvable - rien a nettoyer" % AGENTS_FILE)
        return 0
    with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
        lignes = fh.readlines()

    sortie = []
    dans_section = False
    section_courante = ""
    nb_supprime = 0
    for ligne in lignes:
        entete = ligne.strip()
        if re.match(r"^## ", entete):
            dans_section = entete in SECTIONS_A_SUPPRIMER
            section_courante = entete
            if dans_section:
                nb_supprime += 1
                continue
        elif re.match(r"^### Session : session-llm-", ligne) or entete.startswith("## Sessions"):
            if not dans_section:
                dans_section = True
                section_courante = "## Sessions LLM"
            nb_supprime += 1
            continue
        if dans_section:
            nb_supprime += 1
            continue
        sortie.append(ligne)

    # Nettoyer les lignes vides multiples creees par la suppression
    sortie_finale = []
    vide_precedent = False
    for ligne in sortie:
        est_vide = ligne.strip() == ""
        if est_vide and vide_precedent:
            continue
        sortie_finale.append(ligne)
        vide_precedent = est_vide

    if dry_run:
        print("[DRY-RUN] AGENTS.md : %d lignes supprimees (blocs session + Sessions connues)" % nb_supprime)
        return nb_supprime

    with io.open(AGENTS_FILE, "w", encoding="utf-8", newline="\n") as fh:
        fh.writelines(sortie_finale)
    print("AGENTS.md : %d lignes supprimees (blocs session + Sessions connues)" % nb_supprime)
    return nb_supprime


def nettoyer_classeur(dry_run=False, verbose=False):
    """Supprimer les lignes profil-session-* du classeur-variables.
    Retourne le nombre de lignes supprimees, ou 0 si le fichier est absent."""
    if not os.path.isfile(CLASSEUR_STOCKAGE):
        print("WARNING: %s introuvable - rien a nettoyer" % CLASSEUR_STOCKAGE)
        return 0
    with io.open(CLASSEUR_STOCKAGE, "r", encoding="utf-8", errors="replace") as fh:
        lignes = fh.readlines()

    sortie = []
    nb_supprime = 0
    for ligne in lignes:
        if "profil-session-" in ligne:
            nb_supprime += 1
            continue
        sortie.append(ligne)

    if dry_run:
        print("[DRY-RUN] Classeur : %d lignes profil-session supprimees" % nb_supprime)
        return nb_supprime

    with io.open(CLASSEUR_STOCKAGE, "w", encoding="utf-8", newline="\n") as fh:
        fh.writelines(sortie)
    print("Classeur : %d lignes profil-session supprimees" % nb_supprime)
    return nb_supprime


def afficher_aide():
    print("Usage: nettoyer-sessions.py [options]")
    print("")
    print("Supprime TOUTES les sessions LLM (etats actifs uniquement) :")
    print("  - AGENTS.md          : blocs ### Session : session-llm-N + section ## Sessions connues")
    print("  - classeur-variables : lignes profil-session-*")
    print("")
    print("Options:")
    print("  --dry-run   Afficher ce qui serait supprime sans ecrire")
    print("  --verbose   Afficher les details")
    print("  --version   Afficher la version")
    print("")
    print("AGENTS-historique.md (le journal) n'est JAMAIS modifie : c'est un temoignage.")
    print("Variables d'environnement: AGENTS_FILE, CLASSEUR_STOCKAGE (tests sur copies)")


def main(argv):
    if "--version" in argv:
        print("nettoyer-sessions v%s (%s)" % (VERSION, STATUT))
        return 0
    if "--aide" in argv or "-h" in argv:
        afficher_aide()
        return 0

    dry_run = "--dry-run" in argv
    verbose = "--verbose" in argv

    total = 0
    total += nettoyer_agents(dry_run=dry_run, verbose=verbose)
    total += nettoyer_classeur(dry_run=dry_run, verbose=verbose)

    if dry_run:
        print("[DRY-RUN] Total : %d lignes a supprimer (aucune modification reelle)" % total)
    else:
        print("Nettoyage termine : %d lignes supprimees" % total)

    # Verification ASCII des fichiers modifies (ne doit jamais bloquer l'ecriture)
    for chemin in (AGENTS_FILE, CLASSEUR_STOCKAGE):
        if os.path.isfile(chemin):
            with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
                contenu = fh.read()
            if not verifier_ascii(contenu):
                print("WARNING: Caracteres non-ASCII presents dans %s" % chemin)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
