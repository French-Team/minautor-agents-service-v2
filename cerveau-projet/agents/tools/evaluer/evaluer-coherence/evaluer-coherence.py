#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
evaluer-coherence.py
Evalue la coherence inter-fichiers : liens, references croisees.

Produit un rapport markdown sur stdout avec un score /100.

Usage:
  evaluer-coherence.py [DOSSIER] [--rapport FICHIER] [--verbose]

Options :
  --rapport <fichier> : ecrit le rapport markdown (sans couleurs)
  --verbose           : detail des fichiers analyses

Retour: 0 toujours (outil d'evaluation, rapport sur stdout).

Proprietaire : Themis (outil partage)
Version : 0.2.5-py
Statut : beta
"""

import argparse
import io
import os
import re
import sys

VERSION = "0.2.5-py"
STATUT = "beta"

# Couleurs ANSI : desactivees si la sortie n'est pas un terminal (capture,
# redirection, combo audit) pour garder des rapports propres.
_ANSI = sys.stdout.isatty()
RED = "\033[0;31m" if _ANSI else ""
GREEN = "\033[0;32m" if _ANSI else ""
YELLOW = "\033[1;33m" if _ANSI else ""
NC = "\033[0m" if _ANSI else ""

# Motifs generiques : exemples de documentation, pas des liens reels
MOTIFS_GENERIQUES = ('texte', 'chemin', 'ancien.md', 'nouveau.md', 'perdu.md',
                     'exemple.md', '.*', 'fichier.md', 'dossier.md', 'cible.md',
                     'source.md', 'destination.md', 'fichier-exemple', 'index.md',
                     'frere-a', 'frere-b', 'sous-dossier', 'parent.md', 'racine/',
                     'protocole-X')

PATTERN_LIEN = re.compile(r"\[[^]]+\]\(([^)]+)\)")

AGENTS_ATTENDUS = ["argus", "cerberus", "buffy", "athena", "atlas", "clio",
                   "janus", "minerve", "morpheus", "promethee", "vulcain",
                   "themis", "hygie", "hermes", "gardien"]

# Prefixes qui vivent dans agents/conventions/ et agents/regles-immuables/ et ne sont pas des outils
PREFIXES_NON_OUTILS = ("convention-", "protocole-", "regles-", "rvav-",
                       "sous-protocole-")

# Commandes systeme et outils d'environnement citees en exemple dans les
# regles interdites (ex: athena liste `cat`, `grep`, `sed` entre backticks)
# mais qui ne sont PAS des outils du cerveau -- a exclure du scan.
COMMANDES_SYSTEME = ("cat", "grep", "sed", "basher", "read_files",
                     "write_file", "basher", "python", "ruby", "perl",
                     "node", "awk", "sort", "find", "xargs", "chmod",
                     "chown", "rm", "mv", "cp", "touch", "wc", "head",
                     "tail", "cut", "tr", "uniq", "diff", "ls", "man",
                     "echo", "printf", "sudo", "apt", "brew", "pip")


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "evaluer-coherence.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="evaluer-coherence.py",
        description="Evalue la coherence inter-fichiers.",
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


def lister_liens_casses(racine, racine_projet=None):
    """Retourne la liste des (fichier, chemin) des liens internes casses.

    racine : dossier a scanner (cerveau-projet/).
    racine_projet : racine du projet (dossier) pour resoudre les liens
                     ../ qui remontent au-dessus de cerveau-projet/.
    """
    if racine_projet is None:
        racine_projet = racine
    resultats = []
    for base, dossiers, fichiers in os.walk(racine):
        base_norm = base.replace("\\", "/")
        if "/exemples/" in base_norm + "/":
            continue
        for nom_fichier in fichiers:
            if not nom_fichier.endswith(".md"):
                continue
            fichier = os.path.join(base, nom_fichier).replace("\\", "/")
            try:
                contenu = io.open(fichier, encoding="utf-8",
                                  errors="replace").read()
                contenu = contenu.replace("\r\n", "\n").replace("\r", "\n")
            except IOError:
                continue
            dans_bloc = False
            for ligne in contenu.split("\n"):
                if ligne.strip().startswith("```") or ligne.strip().startswith("~~~"):
                    dans_bloc = not dans_bloc
                    continue
                if dans_bloc:
                    continue
                for m in PATTERN_LIEN.finditer(ligne):
                    chemin = m.group(1).strip()
                    if not chemin:
                        continue
                    if chemin.startswith("http://") or chemin.startswith("https://"):
                        continue
                    if chemin.startswith("#"):
                        continue
                    if any(motif in chemin for motif in MOTIFS_GENERIQUES):
                        continue
                    cible_fichier = os.path.normpath(
                        os.path.join(os.path.dirname(fichier), chemin))
                    cible_racine = os.path.normpath(
                        os.path.join(racine, chemin))
                    cible_projet = os.path.normpath(
                        os.path.join(racine_projet, chemin))
                    if not os.path.exists(cible_fichier) and not os.path.exists(cible_racine) and not os.path.exists(cible_projet):
                        resultats.append((fichier, chemin))
    return resultats


def lister_dossiers_vides(racine):
    """Retourne la liste des dossiers vides (hors exclusions).

    Fidele au .sh original : le pattern */spec/* n'exclut que le CONTENU
    d'un dossier spec/ ou todo/ (ex: spec/todo), pas le dossier spec/ ou
    todo/ lui-meme. Un dossier spec/ vide est donc signale.
    """
    exclusions = ("spec", "todo", "exemples", ".git", "rapports")
    vides = []
    for base, dossiers, fichiers in os.walk(racine):
        if not fichiers and not dossiers:
            base_norm = base.replace("\\", "/")
            parent = os.path.dirname(base_norm).replace("\\", "/")
            if any(("/" + d + "/") in parent + "/" for d in exclusions):
                continue
            vides.append(base_norm)
    return vides


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("evaluer-coherence.py v" + VERSION + " (" + STATUT + ")")
        return 0

    dossier = args.dossier
    print("=== evaluer-coherence v" + VERSION + " ===")
    print("Cible : " + dossier)
    print("")

    if not os.path.isdir(dossier):
        print(RED + "[ERREUR] Le dossier n'existe pas : " + dossier + NC)
        return 1

    total = 0
    ok = 0
    erreurs = 0
    avertissements = 0

    print("# Rapport evaluer-coherence")
    print("")

    cerveau = os.path.join(dossier, "cerveau-projet")

    # 1. Liens internes casses
    print("## Liens internes casses")
    total += 1
    liens_casses = lister_liens_casses(cerveau, dossier)
    for i, (fichier, chemin) in enumerate(liens_casses[:5], 1):
        print("  - `" + chemin + "` dans `" + fichier + "`")
    if not liens_casses:
        print("| OK | Liens internes | Aucun lien casse detecte |")
        ok += 1
    else:
        print("| ERREUR | Liens internes | " + str(len(liens_casses)) +
              " lien(s) casse(s) (max 5 affiches) |")
        erreurs += 1

    # 2. Dossiers vides (hors exemples)
    print("")
    print("## Dossiers vides")
    total += 1
    dossiers_vides = lister_dossiers_vides(cerveau)
    for d in dossiers_vides[:3]:
        print("  - `" + d + "`")
    if not dossiers_vides:
        print("| OK | Dossiers vides | Aucun dossier vide suspect |")
        ok += 1
    else:
        print("| AVERTISSEMENT | Dossiers vides | " + str(len(dossiers_vides)) +
              " dossier(s) vide(s) |")
        avertissements += 1

    # 3. Agents references dans AGENTS.md
    print("")
    print("## Agents dans AGENTS.md")
    total += 1
    contenu_agents_md = ""
    agants_md = os.path.join(dossier, "AGENTS.md")
    if os.path.isfile(agants_md):
        with open(agants_md, encoding="utf-8", errors="replace") as f:
            contenu_agents_md = f.read()
    agents_ref = 0
    agents_manquants = []
    for agent in AGENTS_ATTENDUS:
        if agent in contenu_agents_md:
            agents_ref += 1
        else:
            agents_manquants.append(agent)
    if not agents_manquants:
        print("| OK | References agents | " + str(agents_ref) +
              " agent(s) reference(s) dans AGENTS.md |")
        ok += 1
    else:
        print("| ERREUR | References agents | Agents non references :" +
              " ".join(agents_manquants) + " |")
        erreurs += 1

    # 4. Outils references par les agents
    print("")
    print("## Outils references par les agents")
    total += 1
    outils_casses = []
    agents_dir = os.path.join(cerveau, "agents")
    tools_dir = os.path.join(agents_dir, "tools")
    noms_outils = set()
    if os.path.isdir(tools_dir):
        # Fidele au .sh original (find -name sur tout tools/) : couvre
        # aussi les protections (tools/tester/protections/) au niveau 3
        for base, dossiers, fichiers in os.walk(tools_dir):
            for d in dossiers:
                if re.match(r"^[a-z-]+$", d):
                    noms_outils.add(d)
            for f in fichiers:
                if f.endswith(".sh"):
                    noms_outils.add(f[:-3])
    if os.path.isdir(agents_dir):
        # Scan limite aux 11 agents officiels (AGENTS_ATTENDUS) : les autres
        # dossiers de agents/ (classeur-variables, conventions, regles-immuables,
        # philosophie, tools) ne sont pas des fiches d agent - leurs variables
        # ou references ne doivent PAS etre interpretees comme des outils.
        for nom in AGENTS_ATTENDUS:
            agent_dir = os.path.join(agents_dir, nom)
            agent_md = os.path.join(agent_dir, nom + ".md")
            if not os.path.isfile(agent_md):
                continue
            with open(agent_md, encoding="utf-8", errors="replace") as f:
                contenu = f.read()
            for outil in re.findall(r"`[a-z-]+`", contenu):
                outil = outil.strip("`")
                if not outil:
                    continue
                # Les options de ligne de commande (--parallele, --serial,
                # --etat-tests...) sont des OPTIONS, pas des outils : elles
                # sont exclues du scan (lecon Janus 2026-08-15, doc janus.md).
                if outil.startswith("--"):
                    continue
                if outil.startswith(PREFIXES_NON_OUTILS):
                    continue
                if outil in COMMANDES_SYSTEME:
                    continue
                if outil.endswith("-template") or outil.startswith("template-"):
                    continue
                if outil.startswith("combos-combos-"):
                    continue
                # Un nom d outil du cerveau contient un tiret (action-outil) ou
                # est connu des dossiers reels. Un mot francais simple entre
                # backticks (conforme, success, probleme...) n est PAS un outil
                # (lecon Janus 2026-08-15 : faux positifs des fiches).
                if "-" not in outil and outil not in noms_outils:
                    continue
                if outil not in noms_outils:
                    if outil not in outils_casses:
                        outils_casses.append((outil, nom))
    for outil, agent in outils_casses[:3]:
        print("  - `" + outil + "` reference par `" + agent +
              "` mais introuvable")
    if not outils_casses:
        print("| OK | Outils references | Tous les outils references existent |")
        ok += 1
    else:
        print("| ERREUR | Outils references | " + str(len(outils_casses)) +
              " outil(s) reference(s) mais introuvable(s) |")
        erreurs += 1

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
    print("Score coherence : " + str(score) + "/100")

    # Rapport fichier (sans codes de couleur)
    if args.rapport:
        try:
            with io.open(args.rapport, "w", encoding="utf-8",
                         newline="\n") as fh:
                fh.write("# Rapport evaluer-coherence\n\n")
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
