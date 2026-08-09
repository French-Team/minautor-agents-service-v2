#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
generateurs-squelette-todo.py
Genere le squelette d'un todo conforme au todo-template et a la
convention-renommage.

Usage:
  generateurs-squelette-todo.py --theme <theme> [--id <id>] [--class <class>]
      [--statut <statut>] [--dossier <dossier>] [--dry-run]

Options:
  --theme <theme>     Theme du todo (obligatoire, sans accents ni espaces)
  --id <id>           Identifiant numerique (defaut: 001)
  --class <class>     Classe numerique (defaut: 01)
  --statut <statut>   Statut (defaut: ebauche)
  --dossier <dossier> Dossier de destination (defaut: spec/todo)
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


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "generateurs-squelette-todo.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def generer_squelette(theme, id_elt, class_elt, statut):
    """Genere le squelette du todo (markdown)."""
    date = datetime.date.today().isoformat()
    return f"""# Todo -- [Titre de la mission]

> **Taches a realiser pour implementer et maintenir le concept de {theme}.**

---

## Phase 0 -- Activation de l'agent

> **Regle OBLIGATOIRE** : La premiere action de tout todo est d'activer l'agent adapte.

1. Identifier l'agent adapte
2. Mettre a jour AGENTS.md
3. Lire la fiche et corrections de l'agent
4. Agent active et pret

---

## Header

```yaml
mission:
  id: "[MISSION-XXX]"
  titre: "[Titre de la mission]"
  statut: "en-attente"
  date_debut: "[YYYY-MM-DD]"
  date_fin: "[YYYY-MM-DD]"
  agent: "[nom-agent]"
  pense_bete: "[lien]"
  spec: "[lien]"
```

---

## Statut de l'intervention

| Element | Statut | Lien |
|---|---|---|
| **Pense-bete** | [en-attente/cree/valide] | [lien] |
| **Spec** | [en-attente/cree/valide] | [lien] |
| **Todo** | [en-attente/en-cours/terminee] | [lien] |

---

## Phase 1 -- Analyse de la demande

1. **Comprendre le besoin** : Qu'est-ce que l'utilisateur demande vraiment ?
2. **Tours de question** : Si ambiguites, poser des questions
3. **Classifier** : Nouveau projet, composant, bug fix, etc.

---

## Phase 2 -- Verification du cerveau

1. **Conventions** : renommage, structures, liens, protocoles
2. **Regles immuables** : validation, emojis, hierarchie
3. **Protocoles** : demarrer, reprendre, installer regles
4. **Recherches-web** : recherches similaires existantes

---

## Phase 3 -- Recherches

1. **Recherches-web** : documenter les sources
2. **Documentation technique** : versions et liens
3. **Comparaison** : code vs recherches
4. **Mise a jour cerveau** : sauvegarder les trouvailles

---

## Phase 4 -- Preparation des outils

1. **Outils disponibles** : lister ceux qui existent
2. **Outils a creer** : identifier les manquants
3. **Protocole** : suivre protocole-outils pour creation

---

## Phase 5 -- Developpement

1. **Taches** : lister avec dependances
2. **Verifications** : conventions, regles, liens

---

## Phase 6 -- Tests et validation

1. **Tests unitaires** : chaque fonction
2. **Tests d'integration** : ensemble
3. **Validation manuelle** : execution reelle
4. **Checklist** : tous les points coches

---

## Phase 7 -- Controle secondaire

1. **Preparer** : fichiers modifies, recherches, tests
2. **Executer** : verifier chaque critere
3. **Decider** : valide, non valide, partiel

---

## Phase 8 -- Finalisation

1. **Statut** : mettre a jour dans le cerveau
2. **Documentation** : historique, recherches
3. **Declaration** : mission terminee

---

## Phase 9 -- Reactivation de Cerberus

> **Regle OBLIGATOIRE** : La derniere action de tout todo suit SA carte (Pattern 8) : reactiver Cerberus si active directement par Cerberus, sinon activer le maillon suivant de la chaine ; seul le dernier maillon reactiver Cerberus avec le bilan consolide.

1. Verifier que tout est termine
2. Mettre a jour AGENTS.md (Cerberus agent principal)
3. Documenter la raison du retour

---

## Historique

| Date | Etape | Action | Resultat |
|---|---|---|---|
| {date} | [Etape] | [Action] | [Resultat] |

---

## Notes

[Notes supplementaires sur la mission]

---

## Liens

- **Pense-bete** : [lien]
- **Spec** : [lien]
- **Recherches-web** : [lien]
- **Cerveau** : [lien]
"""


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="generateurs-squelette-todo.py",
        description="Genere le squelette d'un todo conforme au todo-template.",
        add_help=False,
    )
    parser.add_argument("--theme", default="",
                        help="Theme du todo (obligatoire, sans accents ni espaces)")
    parser.add_argument("--id", dest="id_elt", default="001",
                        help="Identifiant numerique (defaut: 001)")
    parser.add_argument("--class", dest="class_elt", default="01",
                        help="Classe numerique (defaut: 01)")
    parser.add_argument("--statut", default="ebauche",
                        help="Statut (defaut: ebauche)")
    parser.add_argument("--dossier", default="spec/todo",
                        help="Dossier de destination (defaut: spec/todo)")
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
        print("generateurs-squelette-todo.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if not args.theme:
        print(RED + "[ERREUR] Le theme est obligatoire (--theme)" + NC)
        construire_parser().print_help()
        return 1

    if not THEME_VALIDE.match(args.theme):
        print(RED + "[ERREUR] Le theme doit etre en minuscules sans accents ni espaces : " +
              args.theme + NC)
        return 1

    nom_fichier = "todo-" + args.theme + "." + args.id_elt + "." + \
        args.class_elt + "." + args.statut + ".md"
    chemin_fichier = os.path.join(args.dossier, nom_fichier)
    squelette = generer_squelette(args.theme, args.id_elt, args.class_elt,
                                  args.statut)

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
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            f.write(squelette)
    except OSError as e:
        print(RED + "[ERREUR] Impossible de creer le fichier : " + str(e) + NC)
        return 1

    print(GREEN + "[OK]" + NC + " Squelette cree : " + chemin_fichier)
    return 0


if __name__ == "__main__":
    sys.exit(main())
