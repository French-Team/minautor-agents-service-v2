#!/usr/bin/env python3
# creer-remplir-spec.py
# Remplit une section d'une spec sans ouvrir le fichier
# Version : 0.2.0-py
# Statut : beta

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION = "0.2.0-py"
STATUT = "beta"

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

# Marqueurs de sections (section -> regex du marqueur)
MARQUEURS = {
    "titre": r"^# Gabarit -- Specification",
    "parent": r"^\*\*Pense-bete source :",
    "objectif": r"^## 1\. Objectif",
    "contexte": r"^## 2\. Contexte",
    "exigences": r"^## 3\. Exigences Fonctionnelles",
    "architecture": r"^## 5\. Architecture / Structure Technique",
    "risques": r"^## 6\. Contraintes et Risques",
    "livrables": r"^## 7\. Livrables attendus",
    "validation": r"^## 8\. Plan de validation",
    "liens": r"^## 9\. Liens et References",
    "rvav": r"^## 10\. RVAV de la spec",
}
TITRE_SECTIONS = ("titre",)
HEADER_SECTIONS = ("parent",)


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
        print(RED + "[ERREUR] Lecture impossible : " + str(e) + NC)
        return None
    return contenu.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def interpreter_echappements(contenu):
    """Interpreter les sequences d'echappement (\\n -> retour a la ligne, comme printf %b)."""
    return contenu.replace("\\n", "\n").replace("\\t", "\t")


def trouver_ligne_section(lignes, marqueur):
    """Trouver la premiere ligne (index) qui matche le marqueur de section."""
    pattern = re.compile(marqueur)
    for i, ligne in enumerate(lignes):
        if pattern.match(ligne):
            return i
    return None


def trouver_ligne_fin(lignes, depart):
    """Trouver la prochaine ligne '## ' a partir de depart (index de debut de section)."""
    for i in range(depart + 1, len(lignes)):
        if lignes[i].startswith("## "):
            return i
    return None


def remplir_section(fichier, section, contenu, dry_run):
    if section not in MARQUEURS:
        print(RED + "[ERREUR] Section inconnue : " + section + NC)
        print("Sections disponibles : " + ", ".join(sorted(MARQUEURS.keys())))
        return 1

    if not Path(fichier).is_file():
        print(RED + "[ERREUR] Fichier non trouve : " + fichier + NC)
        return 1

    lignes = lire_lignes(fichier)
    if lignes is None:
        return 1

    marqueur = MARQUEURS[section]
    ligne_section = trouver_ligne_section(lignes, marqueur)
    if ligne_section is None:
        print(RED + "[ERREUR] Section '" + section + "' non trouvee dans " + fichier + NC)
        return 1

    if dry_run:
        print(YELLOW + "[DRY-RUN]" + NC + " Section '" + section + "' de " + fichier)
        print("  Contenu a inserer :")
        print("  -----------------")
        print(contenu)
        print("  -----------------")
        return 0

    if section in TITRE_SECTIONS:
        lignes[ligne_section] = "# Spec -- " + contenu
    elif section in HEADER_SECTIONS:
        lignes[ligne_section] = "**Pense-bete source :** " + contenu
    else:
        contenu_interprete = interpreter_echappements(contenu)
        ligne_fin = trouver_ligne_fin(lignes, ligne_section)
        if ligne_fin is not None:
            nouvelle = lignes[:ligne_section + 1]
            nouvelle.append("")
            nouvelle.extend(contenu_interprete.split("\n"))
            nouvelle.append("")
            nouvelle.extend(lignes[ligne_fin:])
        else:
            nouvelle = lignes[:ligne_section + 1]
            nouvelle.append("")
            nouvelle.extend(contenu_interprete.split("\n"))
            nouvelle.append("")

        lignes = nouvelle

    try:
        Path(fichier).write_text("\n".join(lignes) + "\n", encoding="utf-8")
    except OSError as e:
        print(RED + "[ERREUR] Ecriture impossible : " + str(e) + NC)
        return 1

    print(GREEN + "[OK]" + NC + " Section '" + section + "' remplie dans " + fichier)
    return 0


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="creer-remplir-spec",
        description="Remplir une section d'une spec sans ouvrir le fichier.",
    )
    parser.add_argument("fichier", help="Chemin de la spec a remplir")
    parser.add_argument("section", help="Section a remplir (titre, parent, objectif, contexte, exigences, architecture, risques, livrables, validation, liens, rvav)")
    parser.add_argument("contenu", help="Contenu a inserer")
    parser.add_argument("--dry-run", action="store_true", help="Afficher ce qui serait fait sans modifier")
    parser.add_argument("--version", action="version", version="creer-remplir-spec " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    return remplir_section(args.fichier, args.section, args.contenu, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
