#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
evaluer-agents.py
Evalue le comportement des agents : respect des protocoles, outils, fiches.

Produit un rapport markdown sur stdout avec un score /100.

Usage:
  evaluer-agents.py [DOSSIER] [--rapport FICHIER] [--verbose]

Options :
  --rapport <fichier> : ecrit le rapport markdown (sans couleurs)
  --verbose           : detail des fichiers analyses

Retour: 0 toujours (outil d'evaluation, rapport sur stdout).

Proprietaire : Themis (outil partage)
Version : 0.2.3-py
Statut : beta
"""

import argparse
import io
import os
import sys

VERSION = "0.2.3-py"
STATUT = "beta"

# Couleurs ANSI : desactivees si la sortie n'est pas un terminal (capture,
# redirection, combo audit) pour garder des rapports propres.
_ANSI = sys.stdout.isatty()
RED = "\033[0;31m" if _ANSI else ""
GREEN = "\033[0;32m" if _ANSI else ""
YELLOW = "\033[1;33m" if _ANSI else ""
NC = "\033[0m" if _ANSI else ""

# Dossiers non-agents a ignorer dans agents/
DOSSIERS_NON_AGENTS = {"tools", "examples", "exemples"}


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "evaluer-agents.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="evaluer-agents.py",
        description="Evalue le comportement des agents.",
        add_help=False,
    )
    parser.add_argument("dossier", nargs="?", default=".",
                        help="Racine du projet (defaut: .)")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    parser.add_argument("--rapport", default="",
                        help="Ecrire le rapport markdown dans ce fichier")
    parser.add_argument("--verbose", action="store_true",
                        help="Detail des fichiers analyses")
    return parser


def lister_agents(agents_dir):
    """Retourne la liste des dossiers d'agents (hors non-agents)."""
    agents = []
    if not os.path.isdir(agents_dir):
        return agents
    for nom in sorted(os.listdir(agents_dir)):
        chemin = os.path.join(agents_dir, nom)
        if os.path.isdir(chemin) and nom not in DOSSIERS_NON_AGENTS:
            agents.append(nom)
    return agents


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("evaluer-agents.py v" + VERSION + " (" + STATUT + ")")
        return 0

    dossier = args.dossier
    print("=== evaluer-agents v" + VERSION + " ===")
    print("Cible : " + dossier)
    print("")

    if not os.path.isdir(dossier):
        print(RED + "[ERREUR] Le dossier n'existe pas : " + dossier + NC)
        return 1

    total = 0
    ok = 0
    erreurs = 0
    avertissements = 0

    print("# Rapport evaluer-agents")
    print("")

    agents_dir = os.path.join(dossier, "cerveau-projet", "agents")
    agents = lister_agents(agents_dir)

    # 1. Chaque agent a une fiche
    print("## Fiches agents")
    for agent in agents:
        total += 1
        fiche = os.path.join(agents_dir, agent, agent + ".md")
        if os.path.isfile(fiche):
            print("| OK | Fiche " + agent + " | `" + agent + "/" + agent + ".md` |")
            ok += 1
        else:
            print("| ERREUR | Fiche " + agent + " | `" + agent +
                  "/" + agent + ".md` MANQUANT |")
            erreurs += 1

    # 2. Chaque agent a corrections.md
    print("")
    print("## Fichiers corrections")
    for agent in agents:
        total += 1
        corrections = os.path.join(agents_dir, agent, "corrections.md")
        if os.path.isfile(corrections):
            print("| OK | Corrections " + agent + " | `" + agent +
                  "/corrections.md` |")
            ok += 1
        else:
            print("| AVERTISSEMENT | Corrections " + agent + " | `" + agent +
                  "/corrections.md` MANQUANT |")
            avertissements += 1

    # 3. Chaque outil a un .sh et un .md
    print("")
    print("## Outils complets (sh + md)")
    tools_dir = os.path.join(agents_dir, "tools")
    sous_dossiers_a_ignorer = {"spec", "todo", "rapports", "protections", "test", "__pycache__"}
    if os.path.isdir(tools_dir):
        for categorie in sorted(os.listdir(tools_dir)):
            cat_path = os.path.join(tools_dir, categorie)
            if not os.path.isdir(cat_path):
                continue
            for outil in sorted(os.listdir(cat_path)):
                outil_dir = os.path.join(cat_path, outil)
                if not os.path.isdir(outil_dir):
                    continue
                if outil in sous_dossiers_a_ignorer:
                    continue
                total += 1
                has_sh = os.path.isfile(os.path.join(outil_dir, outil + ".sh"))
                has_md = os.path.isfile(os.path.join(outil_dir, outil + ".md"))
                if has_sh and has_md:
                    print("| OK | Outil " + outil + " | .sh + .md presents |")
                    ok += 1
                elif has_sh:
                    print("| AVERTISSEMENT | Outil " + outil +
                          " | .sh present, .md MANQUANT |")
                    avertissements += 1
                elif has_md:
                    print("| AVERTISSEMENT | Outil " + outil +
                          " | .md present, .sh MANQUANT |")
                    avertissements += 1
                else:
                    print("| ERREUR | Outil " + outil +
                          " | .sh ET .md MANQUANTS |")
                    erreurs += 1

    # 4. Agents declares dans AGENTS.md
    print("")
    print("## Declaration dans AGENTS.md")
    total += 1
    agents_declares = 0
    agants_md = os.path.join(dossier, "AGENTS.md")
    contenu_agents_md = ""
    if os.path.isfile(agants_md):
        with open(agants_md, encoding="utf-8", errors="replace") as f:
            contenu_agents_md = f.read()
    for agent in agents:
        if agent in contenu_agents_md:
            agents_declares += 1
        else:
            print("| ERREUR | Agent " + agent +
                  " | Non declare dans AGENTS.md |")
            erreurs += 1
    if erreurs == 0:
        print("| OK | Declaration agents | " + str(agents_declares) +
              " agent(s) declare(s) dans AGENTS.md |")
        ok += 1

    # 5. Agent actif = Cerberus (verification)
    print("")
    print("## Agent actif")
    total += 1
    # Convention v0.5.0 : champ **Nom Agent** (ancien **Nom** accepte en repli)
    agent_actif = ""
    for ligne in contenu_agents_md.splitlines():
        if ("**Nom Agent**" in ligne or "**Nom**" in ligne) and "|" in ligne:
            agent_actif = ligne.split("|")[2].strip()
            break
    if agent_actif == "Cerberus":
        print("| OK | Agent actif | Cerberus (attendu) |")
        ok += 1
    else:
        print("| AVERTISSEMENT | Agent actif | '" + agent_actif +
              "' au lieu de Cerberus |")
        avertissements += 1

    # Resume
    print("")
    print("## Resume")
    print("")
    print("- Total elements verifies : " + str(total))
    print("- OK : " + str(ok))
    print("- Erreurs : " + str(erreurs))
    print("- Avertissements : " + str(avertissements))
    print("")
    score = (ok * 100 // total) if total > 0 else 0
    print("Score agents : " + str(score) + "/100")

    # Rapport fichier (sans codes de couleur)
    if args.rapport:
        try:
            with io.open(args.rapport, "w", encoding="utf-8",
                         newline="\n") as fh:
                fh.write("# Rapport evaluer-agents\n\n")
                fh.write("**Date** : %s | **Score** : %d/100 | "
                         "**Erreurs** : %d | **Avertissements** : %d\n\n" % (
                             __import__("datetime").datetime.now()
                             .strftime("%Y-%m-%d %H:%M"),
                             score, erreurs, avertissements))
                fh.write("Voir le rapport complet sur stdout (rapport "
                         "markdown avec le detail par element).\n")
            print("Rapport ecrit : %s" % os.path.abspath(args.rapport))
        except (IOError, OSError) as e:
            print("[ERREUR] Impossible d'ecrire le rapport : %s" % e)

    return 0


if __name__ == "__main__":
    sys.exit(main())
