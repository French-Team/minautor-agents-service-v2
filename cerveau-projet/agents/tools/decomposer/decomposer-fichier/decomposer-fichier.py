#!/usr/bin/env python3
# decomposer-fichier.py
# Outil de decomposition des fichiers markdown
# Permet de voir uniquement ce dont on a besoin
# Proprietaire : Atlas (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION = "0.2.0-py"
STATUT = "beta"

import json
import re
import sys
from pathlib import Path

# Couleurs ANSI (desactivees si la sortie n'est pas un terminal)
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
        print("  Nom actuel : " + nom)
        sys.exit(2)


def lire_lignes(fichier):
    """Lire un fichier en normalisant CRLF/LF."""
    try:
        contenu = Path(fichier).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print("ERREUR: Impossible de lire " + str(fichier) + " : " + str(e))
        return None
    return contenu.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def lister_sections(lignes, nom):
    """Lister les sections avec numerotation."""
    print("=== Sections de " + nom + " ===")
    print("")
    num = 0
    sous_num = 0
    for ligne in lignes:
        num += 1
        if re.match(r"^## [^#]", ligne):
            sous_num = 0
            print(str(num) + ". " + ligne)
        elif re.match(r"^### [^#]", ligne):
            sous_num += 1
            print("   " + str(num) + "." + str(sous_num) + " " + ligne)
        elif re.match(r"^#### [^#]", ligne):
            print("      " + str(num) + "." + str(sous_num) + ".1 " + ligne)


def extraire_section(lignes, section, nom):
    """Extraire une section par nom."""
    print("=== Section: " + section + " ===")
    print("")
    dans_section = False
    niveau = 0
    for ligne in lignes:
        # Detecter le debut de la section
        if re.search(section, ligne, re.IGNORECASE):
            dans_section = True
            m = re.match(r"^(#{1,4})", ligne)
            niveau = len(m.group(1)) if m else 0
            print(ligne)
            continue
        if dans_section:
            # Fin de la section : nouveau titre de meme niveau ou superieur
            if niveau > 0 and re.match(r"^#{1," + str(niveau) + r"} [^#]", ligne):
                break
            print(ligne)


def filtrer_type(lignes, type_filtre):
    """Filtrer les lignes par type de contenu."""
    motifs = {
        "titres": re.compile(r"^#{1,4} "),
        "regles": re.compile(r"REGLE|JAMAIS|TOUJOURS|OBLIGATOIRE|INTERDIT"),
        "tableaux": re.compile(r"^\|.*\|"),
        "code": re.compile(r"^```"),
        "liens": re.compile(r"\[.*\]\(.*\)"),
    }
    if type_filtre not in motifs:
        print("Type inconnu: " + type_filtre)
        print("Types disponibles: titres, regles, tableaux, code, liens")
        return 1
    pattern = motifs[type_filtre]
    for num, ligne in enumerate(lignes, start=1):
        if pattern.search(ligne):
            print(str(num) + ": " + ligne)
    return 0


def afficher_resume(lignes, nom):
    """Afficher le resume du fichier."""
    lignes_count = len(lignes)
    sections = sum(1 for l in lignes if re.match(r"^## [^#]", l))
    sous_sections = sum(1 for l in lignes if re.match(r"^### [^#]", l))
    tableaux = sum(1 for l in lignes if re.match(r"^\|.*\|", l))
    blocs_code = sum(1 for l in lignes if l.startswith("```"))

    print("=== Resume de " + nom + " ===")
    print("")
    print("Lignes       : " + str(lignes_count))
    print("Sections     : " + str(sections))
    print("Sous-sections: " + str(sous_sections))
    print("Tableaux     : " + str(tableaux))
    print("Blocs de code: " + str(blocs_code))


def compter_contenu(lignes, nom):
    """Compter lignes, mots, caracteres."""
    print("=== Comptage de " + nom + " ===")
    print("")
    print("Lignes      : " + str(len(lignes)))
    mots = sum(len(l.split()) for l in lignes)
    print("Mots        : " + str(mots))
    caracteres = sum(len(l) for l in lignes)
    print("Caracteres  : " + str(caracteres))


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="decomposer-fichier",
        description="Decomposer les fichiers markdown pour voir uniquement ce dont on a besoin.",
    )
    parser.add_argument("fichier", help="Fichier markdown a decomposer")
    parser.add_argument("--lister", action="store_true", help="Lister les sections")
    parser.add_argument("--extraire", metavar="SECTION", help="Extraire une section")
    parser.add_argument("--filtrer", metavar="TYPE", help="Filtrer par type (titres|regles|tableaux|code|liens)")
    parser.add_argument("--resume", action="store_true", help="Afficher le resume")
    parser.add_argument("--compter", action="store_true", help="Compter le contenu")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    parser.add_argument("--verbose", action="store_true", help="Details supplementaires")
    parser.add_argument("--version", action="version", version="decomposer-fichier " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    fichier = Path(args.fichier)
    if not fichier.is_file():
        print("ERREUR: Le fichier " + args.fichier + " n'existe pas")
        return 1

    lignes = lire_lignes(fichier)
    if lignes is None:
        return 1

    nom = fichier.name

    if args.lister:
        lister_sections(lignes, nom)
    elif args.extraire:
        extraire_section(lignes, args.extraire, nom)
    elif args.filtrer:
        return filtrer_type(lignes, args.filtrer)
    elif args.resume:
        afficher_resume(lignes, nom)
    elif args.compter:
        compter_contenu(lignes, nom)
    else:
        # Par defaut : afficher le resume
        afficher_resume(lignes, nom)

    return 0


if __name__ == "__main__":
    sys.exit(main())
