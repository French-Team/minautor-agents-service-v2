#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
generateurs-squelette-spec.py
Genere le squelette d'une spec conforme au spec-template et a la
convention-renommage.

Usage:
  generateurs-squelette-spec.py --theme <theme> [--id <id>] [--class <class>]
      [--statut <statut>] [--dossier <dossier>] [--parent <lien>]
      [--dry-run]

Options:
  --theme <theme>     Theme de la spec (obligatoire, sans accents ni espaces)
  --id <id>           Identifiant numerique (defaut: 001)
  --class <class>     Classe numerique (defaut: 01)
  --statut <statut>   Statut (defaut: ebauche)
  --dossier <dossier> Dossier de destination (defaut: spec/)
  --parent <lien>     Lien vers le pense-bete source
  --dry-run           Afficher le squelette sans creer le fichier
  --version           Afficher la version
  --aide, -h          Afficher cette aide

Retour: 0 si succes, 1 si erreur.

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : beta
"""

import argparse
import datetime
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "beta"

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color

# Theme valide : minuscules, chiffres, tirets (pas d'accents ni espaces)
THEME_VALIDE = re.compile(r"^[a-z0-9-]+$")

PARENT_DEFAUT = "[lien vers le pense-bete parent]"


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "generateurs-squelette-spec.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def generer_squelette(theme, id_elt, class_elt, statut, parent):
    """Genere le squelette de la spec (markdown)."""
    date = datetime.date.today().isoformat()
    parent_aff = parent if parent else PARENT_DEFAUT
    return f"""# Gabarit -- Specification

> **Specification technique de {theme}.**

---

## Header

**Statut :** {statut}
**ID :** {id_elt}
**Class :** {class_elt}
**Cree :** {date}
**Theme :** {theme}
**Pense-bete source :** {parent_aff}

---

## 1. Objectif

[Quel est l'objectif precis de cette spec ? Qu'est-ce qu'elle doit permettre d'atteindre ?]

## 2. Contexte

### 2.1 Origine

[D'ou vient ce besoin ? Quel probleme ou opportunite a declenche cette spec ?]

### 2.2 Perimetre

[Que couvre cette spec ? Qu'est-ce qui est hors perimetre ?]

### 2.3 Public cible

[Qui utilise ou sera impacte par cette spec ?]

---

## 3. Exigences Fonctionnelles

### 3.1 Exigence [ID] -- [Titre]

| Champ | Description |
|---|---|
| **Priorite** | Haute / Moyenne / Basse |
| **Description** | [Description detaillee] |
| **Critere d'acceptation** | [Comment valider que l'exigence est remplie] |
| **Dependances** | [Liens vers d'autres exigences ou specs] |

*(Repeter pour chaque exigence)*

---

## 4. Exigences Non-Fonctionnelles

| Categorie | Exigence | Critere de mesure |
|---|---|---|
| **Performance** | [ex: temps de reponse < 200ms] | [methode de test] |
| **Securite** | [ex: authentification requise] | [critere de validation] |
| **Maintenabilite** | [ex: code testable a 80%] | [couverture de tests] |
| **Accessibilite** | [ex: WCAG 2.1 AA] | [outil de verification] |

---

## 5. Architecture / Structure Technique

### 5.1 Vue d'ensemble

[Description de l'architecture cible]

### 5.2 Composants

| Composant | Role | Dependances |
|---|---|---|
| [Nom] | [Description] | [Liens] |

### 5.3 Modele de donnees

[Si applicable - schema, entites, relations]

### 5.4 Interfaces / API

[Si applicable - points d'entree, contrats, formats]

### 5.5 Flux / Workflows

[Si applicable - sequences d'actions, etats, transitions]

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| [Description] | [Impact] | [Solution] |

### 6.2 Risques

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| [Description] | Elevee / Moyenne / Faible | Eleve / Moyen / Faible | [Solution] |

---

## 7. Livrables attendus

| Livrable | Format | Destination |
|---|---|---|
| [Ex: Code source] | [Repertoire, langage] | [Depot] |
| [Ex: Documentation] | [Markdown, PDF] | [Emplacement] |
| [Ex: Tests] | [Type de tests] | [Repertoire] |

---

## 8. Plan de validation

### 8.1 Criteres de succes globaux

- [ ] [Critere 1]
- [ ] [Critere 2]
- [ ] [Critere 3]

### 8.2 Methode de validation

[Ex: revue par les pairs, tests d'integration, demo fonctionnelle]

### 8.3 Responsables

| Role | Responsable |
|---|---|
| Redaction | [Nom / Role] |
| Validation technique | [Nom / Role] |
| Validation metier | [Nom / Role] |

---

## 9. Liens et References

### 9.1 Pense-bete source

- {parent_aff}

### 9.2 Specs connexes

- [Lien vers autres specs liees]

### 9.3 Conventions applicables

- [Lien vers conventions utilisees]

### 9.4 Regles immuables

- [Lien vers regles respectees]

### 9.5 References externes

- [Liens vers documentation, standards, etc.]

---

## 10. RVAV de la spec

- [rechercher] -- toutes les references, dependances externes rassemblees
- [verifier] -- la structure est complete (toutes les sections remplies)
- [analyser] -- la spec est coherente avec le cerveau existant et le pense-bete source
- [valider] -- pret pour le statut suivant (prepare)

---

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| {date} | v0.1 | [Nom] | [Description du changement] |
"""


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="generateurs-squelette-spec.py",
        description="Genere le squelette d'une spec conforme au spec-template.",
        add_help=False,
    )
    parser.add_argument("--theme", default="",
                        help="Theme de la spec (obligatoire, sans accents ni espaces)")
    parser.add_argument("--id", dest="id_elt", default="001",
                        help="Identifiant numerique (defaut: 001)")
    parser.add_argument("--class", dest="class_elt", default="01",
                        help="Classe numerique (defaut: 01)")
    parser.add_argument("--statut", default="ebauche",
                        help="Statut (defaut: ebauche)")
    parser.add_argument("--dossier", default="spec",
                        help="Dossier de destination (defaut: spec/)")
    parser.add_argument("--parent", default="",
                        help="Lien vers le pense-bete source")
    parser.add_argument("--dry-run", action="store_true",
                        help="Afficher le squelette sans creer le fichier")
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
        print("generateurs-squelette-spec.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if not args.theme:
        print(RED + "[ERREUR] Le theme est obligatoire (--theme)" + NC)
        construire_parser().print_help()
        return 1

    if not THEME_VALIDE.match(args.theme):
        print(RED + "[ERREUR] Le theme doit etre en minuscules sans accents ni espaces : " +
              args.theme + NC)
        return 1

    nom_fichier = "spec-" + args.theme + "." + args.id_elt + "." + \
        args.class_elt + "." + args.statut + ".md"
    chemin_fichier = os.path.join(args.dossier, nom_fichier)
    squelette = generer_squelette(args.theme, args.id_elt, args.class_elt,
                                  args.statut, args.parent)

    if args.dry_run:
        print(YELLOW + "[DRY-RUN]" + NC + " Squelette de : " + nom_fichier)
        print("")
        print(squelette)
        return 0

    if os.path.isfile(chemin_fichier):
        print(RED + "[ERREUR] Le fichier existe deja : " + chemin_fichier + NC)
        return 1

    try:
        os.makedirs(args.dossier, exist_ok=True)
        # FIGER LF : newline='' evite la traduction CRLF Windows
        with open(chemin_fichier, "w", encoding="utf-8", newline="") as f:
            f.write(squelette)
    except OSError as e:
        print(RED + "[ERREUR] Impossible de creer le fichier : " + str(e) + NC)
        return 1

    print(GREEN + "[OK]" + NC + " Squelette cree : " + chemin_fichier)
    return 0


if __name__ == "__main__":
    sys.exit(main())
