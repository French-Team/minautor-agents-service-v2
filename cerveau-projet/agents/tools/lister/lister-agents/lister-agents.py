#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lister-agents.py
Lister les agents du cerveau-projet avec leurs informations (role, statut,
version, principal). Option --detail pour verifier corrections.md,
carte de decision et boucles de retro-action.

Usage:
  lister-agents.py [OPTIONS]

Options:
  --detail, -d    Afficher les details complets
  --tag TAGS      Filtrer par tag (convention-tags, cle tags: dans identite)
  --verbose, -v   Afficher les details
  --version       Afficher la version
  --aide, -h      Afficher cette aide

Retour: 0 si succes, 1 si erreur.

Proprietaire : Vulcain (outil partage)
Version : 0.4.0-py
Statut : beta
"""

import argparse
import os
import re
import sys

VERSION = "0.4.0-py"
STATUT = "beta"

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
NC = "\033[0m"  # No Color

AGENTS_DIR = "cerveau-projet/agents"


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "lister-agents.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def extraire_champ(contenu, champ):
    """Extrait la valeur d'un champ simple (role-agent:, statut-<agent>:...)."""
    for ligne in contenu.split("\n"):
        m = re.match(r"^\s*" + re.escape(champ) + r"\s*:\s*(.*)$", ligne)
        if m:
            return m.group(1).strip().strip("\"")
    return ""


def lire_tags_contenu(contenu):
    """Lit la cle tags: du frontmatter identite. Retourne la liste des tags."""
    dans_identite = False
    for ligne in contenu.split("\n"):
        if "identite:" in ligne:
            dans_identite = True
            continue
        if dans_identite:
            m = re.match(r"^\s*tags:\s*(.*)$", ligne)
            if m:
                return [t.strip() for t in m.group(1).split(",")
                        if t.strip()]
    return []


def extraire_champ_avec_repli(contenu, nouveau, ancien):
    """Extraire la valeur d'un champ avec repli : le nouveau nom (convention
    v0.3.0 : role-agent, statut-<agent>) est cherche en premier, l'ancien nom
    (role:, statut:) sert de repli pendant la transition."""
    val = extraire_champ(contenu, nouveau)
    if val:
        return val
    return extraire_champ(contenu, ancien)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lister-agents.py",
        description="Lister les agents du cerveau-projet avec leurs informations.",
        add_help=False,
    )
    parser.add_argument("--detail", "-d", action="store_true",
                        help="Afficher les details complets")
    parser.add_argument("--tag", default="",
                        help="Filtrer par tag (convention-tags)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Afficher les details")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("lister-agents.py v" + VERSION + " (" + STATUT + ")")
        return 0

    print(BLUE + "[LISTE] Liste des agents du cerveau-projet" + NC)
    if args.tag:
        print(YELLOW + "[FILTRE] Tag : " + args.tag + NC)
    print("")

    if not os.path.isdir(AGENTS_DIR):
        print(RED + "Erreur: Le dossier " + AGENTS_DIR + " n'existe pas" + NC)
        return 1

    total = 0
    actifs = 0
    en_attente = 0

    for nom in sorted(os.listdir(AGENTS_DIR)):
        agent_dir = os.path.join(AGENTS_DIR, nom)
        if not os.path.isdir(agent_dir) or nom == "tools":
            continue

        agent_file = os.path.join(agent_dir, nom + ".md")
        corrections_file = os.path.join(agent_dir, "corrections.md")

        if os.path.isfile(agent_file):
            with open(agent_file, encoding="utf-8", errors="replace") as f:
                contenu = f.read()

            # Filtre par tag (convention-tags : cle tags: dans identite)
            if args.tag:
                tags_agent = lire_tags_contenu(contenu)
                if args.tag not in tags_agent:
                    continue

            print(CYAN + "----------------------------------------" + NC)
            print(GREEN + "[AGENT] Agent : " + nom + NC)
            print(CYAN + "----------------------------------------" + NC)

            role = extraire_champ_avec_repli(contenu, "role-agent", "role")
            if role:
                print("  [ROLE] " + role)
            statut = extraire_champ_avec_repli(contenu, "statut-" + nom, "statut")
            if statut:
                print("  [STATUT] " + statut)
            principal = extraire_champ(contenu, "role_principal")
            if principal == "true":
                print("  [PRINCIPAL] Oui")
                actifs += 1
            else:
                en_attente += 1
            version = extraire_champ(contenu, "version")
            if version:
                print("  [VERSION] " + version)

            if args.detail:
                print("")
                print(YELLOW + "Details :" + NC)
                if os.path.isfile(corrections_file):
                    print("    [OK] Fichier corrections : Present")
                else:
                    print("    [ERREUR] Fichier corrections : Absent")
                if "CARTE DE DECISION" in contenu:
                    print("    [OK] Carte de decision : Presente")
                else:
                    print("    [ERREUR] Carte de decision : Absente")
                retro_dir = os.path.join(agent_dir, "retro-actions")
                if os.path.isdir(retro_dir):
                    nb = len([x for x in os.listdir(retro_dir)
                              if x.endswith(".md")])
                    print("    [BOUCLES] Boucles de retro-action : " + str(nb))
                else:
                    print("    [BOUCLES] Boucles de retro-action : Aucune")

            total += 1
            print("")
        else:
            print(YELLOW + "  [ATTENTION]  Fiche d'agent non trouvee" + NC)
            print("")

    print(CYAN + "----------------------------------------" + NC)
    print(BLUE + "Resume :" + NC)
    print("  [TOTAL] Agents : " + str(total))
    print("  [PRINCIPAUX] " + str(actifs))
    print("  [ATTENTE] " + str(en_attente))
    print(CYAN + "----------------------------------------" + NC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
