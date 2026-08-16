#!/usr/bin/env python3
# -*- coding: ascii -*-
# combos-analyse-projet.py
# Combo analyse-projet : analyser la structure reelle du projet et produire le
# rapport des ecarts README vs realite (compteurs, categories, agents, outils)
# Proprietaire : Clio (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
combos-analyse-projet.py
combos-analyse-projet

Usage:
  combos-analyse-projet.py [OPTIONS]
"""

VERSION = "0.1.3"
STATUT = "prepare"

import datetime
import json
import os
import re
import sys
from pathlib import Path

if sys.stdout.isatty():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"
else:
    RED = GREEN = YELLOW = BLUE = NC = ""


def verifier_nommage():
    """Regle immuable : le nom du fichier doit commencer par le prefixe du dossier de categorie."""
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        sys.exit(2)


def compter_outils(racine):
    """Compter les outils reels par categorie (sous-dossiers de agents/tools/).
    Aligne sur mettre-a-jour-readme (source de verite) : chaque sous-dossier d'une
    categorie = 1 outil (pas de filtre .py/.sh)."""
    tools = Path(racine) / "cerveau-projet" / "agents" / "tools"
    if not tools.is_dir():
        print(RED + "[ERREUR] Dossier tools introuvable : " + str(tools) + NC)
        return {}
    categories = {}
    for cat in sorted(p for p in tools.iterdir() if p.is_dir() and not p.name.startswith('__')):
        # Cas special tester : compter les protections (sous-dossiers de protections/) - meme
        # logique que mettre-a-jour-readme (source de verite)
        if cat.name == "tester":
            prot = cat / "protections"
            if prot.is_dir():
                nb = sum(1 for d in prot.iterdir() if d.is_dir() and not d.name.startswith('__'))
            else:
                nb = 0
        else:
            nb = sum(1 for d in cat.iterdir() if d.is_dir() and not d.name.startswith('__'))
        if nb > 0:
            categories[cat.name] = nb
    # Cas special templates : categorie virtuelle (outil-template.md a la racine de tools/) -
    # meme logique que mettre-a-jour-readme (source de verite)
    if (tools / "outil-template.md").is_file():
        categories["templates"] = 1
    return categories


def compter_agents(racine):
    """Compter les agents reels (dossiers de agents/ hors tools).
    Aligne sur mettre-a-jour-readme (source de verite) : tout dossier != tools."""
    agents_dir = Path(racine) / "cerveau-projet" / "agents"
    if not agents_dir.is_dir():
        return 0
    # Un agent d action a un parcours JSON : agents/<nom>/parcours/parcours-<nom>.json
    nb = 0
    for d in agents_dir.iterdir():
        if not (d.is_dir() and d.name != "tools"):
            continue
        if (d / "parcours" / ("parcours-" + d.name + ".json")).is_file():
            nb += 1
    return nb


def lire_README(racine):
    p = Path(racine) / "README.md"
    if not p.is_file():
        return None
    return p.read_text(encoding="utf-8", errors="replace")


def lire_README_dev(racine):
    """Lire readme-dev.md (documentation developpeur). Depuis la refonte grand
    public du README (2026-08-14), la table des categories d outils vit dans
    readme-dev.md section 6, plus dans le README public (par design)."""
    p = Path(racine) / "cerveau-projet" / "readme-dev.md"
    if not p.is_file():
        return None
    return p.read_text(encoding="utf-8", errors="replace")


def extraire_compteur_readme(readme, pattern):
    """Extraire le 1er nombre capture par pattern dans le README, None si absent."""
    m = re.search(pattern, readme, re.M)
    return int(m.group(1)) if m else None


def capitaliser(nom):
    """Capitaliser un nom (cerberus -> Cerberus) - meme logique que mettre-a-jour-readme."""
    return nom[:1].upper() + nom[1:] if nom else nom


def nom_categorie_affichable(cle):
    """Nom de categorie affichable (capitalise + 'Mettre a jour') - meme logique que
    mettre-a-jour-readme (source de verite)."""
    cat = capitaliser(cle)
    cat = cat.replace("Mettre-a-jour", "Mettre a jour")
    return cat


def main():
    verifier_nommage()
    import argparse

    parser = argparse.ArgumentParser(
        prog="combos-analyse-projet",
        description="Combo analyse-projet : structure reelle du projet et ecarts README vs realite.",
    )
    parser.add_argument("racine", nargs="?", default=".", help="Racine du projet (defaut: .)")
    parser.add_argument("--rapport", action="store_true",
                        help="Sauvegarder le rapport dans clio/rapports/")
    parser.add_argument("--version", action="version",
                        version="combos-analyse-projet " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    racine = Path(args.racine)
    print(BLUE + "=== combos-analyse-projet v" + VERSION + " ===" + NC)
    print("Racine : " + str(racine.resolve()))
    print("Date : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("")

    readme = lire_README(racine)
    if readme is None:
        print(RED + "[ERREUR] README.md introuvable a la racine" + NC)
        return 1

    # 1. Etat reel
    categories = compter_outils(racine)
    nb_agents = compter_agents(racine)
    nb_outils = sum(categories.values())

    print(BLUE + "=== ETAT REEL ===  " + NC)
    print("Agents reels : " + str(nb_agents))
    print("Outils reels : " + str(nb_outils))
    print("Outils par categorie :")
    for cat, n in sorted(categories.items()):
        print("  %-20s : %d" % (cat, n))
    print("")

    # 2. Ecarts README vs realite
    print(BLUE + "=== ECARTS README vs REALITE ===" + NC)
    ecarts = []

    # badge Outils-XX du header
    badge = extraire_compteur_readme(readme, r"badge/Outils-(\d+)-")
    if badge is not None and badge != nb_outils:
        ecarts.append("BADGE Outils : README dit %d, realite %d" % (badge, nb_outils))
        print(YELLOW + "  [ECART] Badge Outils-<n> : README=%d realite=%d" % (badge, nb_outils) + NC)
    elif badge is not None:
        print(GREEN + "  [OK] Badge Outils : %d == %d" % (badge, nb_outils) + NC)

    # compteur agents
    cpt_agents = extraire_compteur_readme(readme, r"(?:Agents? reel(?:s)?\s*[:|]\s*)(\d+)")
    # chercher aussi la table des agents
    if cpt_agents is not None and cpt_agents != nb_agents:
        ecarts.append("Compteur agents : README dit %d, realite %d" % (cpt_agents, nb_agents))
        print(YELLOW + "  [ECART] Compteur agents : README=%d realite=%d" % (cpt_agents, nb_agents) + NC)

    # categories manquantes dans readme-dev.md (table boite a outils) : la table
    # a quitte le README public (refonte grand public) pour readme-dev.md section 6.
    readme_dev = lire_README_dev(racine)
    for cat in sorted(categories):
        # chercher la ligne "| <Cat> | <n> |" dans readme-dev (nom capitalise,
        # meme logique que mettre-a-jour-readme) ; repli sur README.md si absent
        cat_aff = nom_categorie_affichable(cat)
        if readme_dev is not None:
            m = re.search(r"^\| " + re.escape(cat_aff) + r" \| (\d+) \|", readme_dev, re.M)
        else:
            m = re.search(r"\*\*" + re.escape(cat_aff) + r"\s*\((\d+)\)\*\*", readme)
        if m is None:
            ecarts.append("Categorie %s absente de la table readme-dev (realite %d)" % (cat, categories[cat]))
            print(YELLOW + "  [MANQUANT] Categorie '%s' absente de la table readme-dev" % cat + NC)
        elif int(m.group(1)) != categories[cat]:
            ecarts.append("Categorie %s : readme-dev dit %d, realite %d" % (cat, int(m.group(1)), categories[cat]))
            print(YELLOW + "  [ECART] Categorie %s : readme-dev=%d realite=%d" % (cat, int(m.group(1)), categories[cat]) + NC)

    # 3. Synthese
    print("")
    print(BLUE + "=== SYNTHESE ===" + NC)
    if ecarts:
        print("Ecarts detectes : " + str(len(ecarts)))
        print("Verdict : A CORRIGER (lancer combos-maj-readme-massive pour une grosse MAJ, "
              "ou combo-maj-readme pour une petite)")
        for e in ecarts:
            print("  - " + e)
    else:
        print("Ecarts detectes : 0")
        print("Verdict : README A JOUR (aucune correction necessaire)")

    # 4. Rapport
    if args.rapport:
        rapport_dir = Path(racine) / "cerveau-projet" / "agents" / "clio" / "rapports"
        rapport_dir.mkdir(parents=True, exist_ok=True)
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        rapport_file = rapport_dir / ("analyse-projet-" + date + ".md")
        lignes = [
            "# Rapport d'analyse du projet -- " + date,
            "",
            "## Contexte",
            "- Combo utilise : combos-analyse-projet v" + VERSION,
            "- Racine : " + str(racine.resolve()),
            "",
            "## Etat reel",
            "- Agents : " + str(nb_agents),
            "- Outils : " + str(nb_outils),
            "",
            "| Categorie | Nombre |",
            "|---|---|",
        ]
        for cat, n in sorted(categories.items()):
            lignes.append("| " + cat + " | " + str(n) + " |")
        lignes.append("")
        lignes.append("## Ecarts README vs realite")
        if ecarts:
            for e in ecarts:
                lignes.append("- " + e)
        else:
            lignes.append("Aucun ecart detecte - README a jour.")
        lignes.append("")
        lignes.append("## Verdict")
        lignes.append("A CORRIGER (" + str(len(ecarts)) + " ecart(s))" if ecarts else "A JOUR")
        rapport_file.write_text("\n".join(lignes) + "\n", encoding="utf-8", newline="")
        print("")
        print(GREEN + "Rapport sauvegarde : " + str(rapport_file) + NC)

    return 0


if __name__ == "__main__":
    sys.exit(main())
