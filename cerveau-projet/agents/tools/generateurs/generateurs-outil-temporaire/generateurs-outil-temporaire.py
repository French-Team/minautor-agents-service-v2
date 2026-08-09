#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
generateurs-outil-temporaire.py

Genere un outil TEMPORAIRE (script Python jetable) dans le workspace pour
repondre a un besoin ponctuel d'une mission. L'outil temporaire est cree
DANS le workspace uniquement (jamais hors workspace, jamais dans tools/),
porte un en-tete standard (identite type: outil-temporaire, ASCII strict,
LF, 100% stdlib) et se termine par la question de PROMOTION : si le besoin
se reproduit (2e utilisation), l'agent ACTIVE VULCAIN pour creer l'outil
durable (protocole 5 fichiers) ; Vulcain reactive ensuite l'agent precedent.

Usage:
  generateurs-outil-temporaire.py --nom <besoin> [--description <texte>]
      [--dossier <chemin>] [--force] [--version]

Options:
  --nom <besoin>       Nom du besoin (obligatoire, sans accents ni espaces,
                       prefixe tmp- ajoute automatiquement)
  --description <texte> Description courte de ce que fait l'outil temporaire
  --dossier <chemin>   Dossier de destination DANS le workspace (defaut:
                       racine du workspace)
  --force              Ecrire reellement le fichier (sans --force : dry-run)
  --version            Afficher la version
  --aide, -h           Afficher cette aide

Retour: 0 si succes, 1 si erreur.

Proprietaire : Vulcain (outil partage)
Version : 0.1.0
Statut : beta
"""

import argparse
import datetime
import os
import re
import sys

VERSION = "0.1.0"
STATUT = "beta"

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color

# Nom du besoin valide : minuscules, chiffres, tirets (pas d'accents ni espaces)
NOM_VALIDE = re.compile(r"^[a-z0-9-]+$")

# Le workspace racine est detecte en remontant depuis ce script jusqu'au
# dossier contenant AGENTS.md (present a la racine du projet).
WORKSPACE_MARQUEUR = "AGENTS.md"


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "generateurs-outil-temporaire.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def resoudre_workspace():
    """Remonte depuis le script jusqu'au dossier contenant AGENTS.md."""
    courant = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(courant, WORKSPACE_MARQUEUR)):
            return courant
        parent = os.path.dirname(courant)
        if parent == courant:
            return None
        courant = parent


def verifier_dans_workspace(chemin_abs, workspace):
    """Verifie que le chemin absolu est bien DANS le workspace."""
    if not workspace:
        print(RED + "[ERREUR] Workspace introuvable (marqueur AGENTS.md absent)" + NC)
        return False
    # Normaliser les separateurs pour la comparaison
    chem = os.path.normcase(os.path.abspath(chemin_abs))
    base = os.path.normcase(os.path.abspath(workspace))
    if chem == base or chem.startswith(base + os.sep):
        return True
    print(RED + "[ERREUR] Chemin hors workspace : " + chemin_abs + NC)
    print(YELLOW + "  REGLE WORKSPACE : ecriture = workspace seul, jamais hors workspace." + NC)
    return False


def generer_script(nom, description, date):
    """Genere le contenu du script temporaire.

    nom est le nom AVEC le prefixe tmp- (ex: tmp-mesurer-taille) :
    le template utilise nom tel quel, sans re-ajouter le prefixe.
    """
    # Nom sans le prefixe tmp- pour la description par defaut
    nom_simple = nom[4:] if nom.startswith("tmp-") else nom
    if not description:
        description = "Outil temporaire pour le besoin " + nom_simple
    contenu = """#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil-temporaire
#   appartient_a: commun
#   commun: false
\"\"\"
%(nom)s.py
%(description)s

Usage:
  python3 %(nom)s.py [arguments]

REGLE WORKSPACE : outil TEMPORAIRE - cree dans le workspace uniquement.
JAMAIS dans tools/ (outil durable = role Vulcain, protocole 5 fichiers).
Supprime en fin de mission (0 residu) OU promu en outil durable si le
besoin se reproduit (2e utilisation -> activer Vulcain).

Version : 0.1.0-tmp
Statut : temporaire
Cree : %(date)s
\"\"\"

import sys

VERSION = "0.1.0-tmp"


def main():
    # A COMPLETER : logique du besoin
    print("%(nom)s : logique a completer")


if __name__ == "__main__":
    main()
""" % {"nom": nom, "description": description, "date": date}
    return contenu


def question_promotion(nom):
    """Affiche la question de promotion (mode non-bloquant, destinee a l'agent)."""
    print()
    print(YELLOW + "=== QUESTION (destinee a l'agent, reponse selon la carte) ===" + NC)
    print(YELLOW + "Ce besoin est-il deja apparu auparavant (2e utilisation) ?" + NC)
    print()
    print(GREEN + "[NON] - Usage ponctuel :" + NC)
    print("  L'outil temporaire tmp-" + nom + ".py est utilisable pour la mission.")
    print("  Il sera SUPPRIME en fin de mission (0 residu, regle workspace).")
    print()
    print(GREEN + "[OUI] - Besoin recurrent (PROMOTION) :" + NC)
    print("  1) ACTIVER VULCAIN directement (maillon de chaine, pas Cerberus) :")
    print("     activer-agent-principal.py activer <session> vulcain <raison>")
    print("  2) Vulcain cree l'outil DURABLE (protocole 5 fichiers : py+sh+md+spec+index)")
    print("  3) Vulcain termine puis REACTIVE L'AGENT PRECEDENT :")
    print("     activer-agent-principal.py reactiver <session> <raison> <agent_precedent>")
    print("  4) L'agent precedent reprend SA mission avec l'outil durable.")
    print()
    print("La promotion systhematique : un besoin utilise 2x n'a pas le droit")
    print("de rester temporaire (lecon : script temporaire -> outil durable).")


def main():
    verifier_nommage(os.path.basename(sys.argv[0]))

    parser = argparse.ArgumentParser(
        prog="generateurs-outil-temporaire.py",
        description="Generer un outil temporaire (script Python jetable) dans le workspace.",
        add_help=False,
    )
    parser.add_argument("--nom", dest="nom", default="")
    parser.add_argument("--description", dest="description", default="")
    parser.add_argument("--dossier", dest="dossier", default="")
    parser.add_argument("--force", dest="force", action="store_true")
    parser.add_argument("--version", dest="version", action="store_true")
    parser.add_argument("--aide", "-h", dest="aide", action="store_true")
    args = parser.parse_args()

    if args.version:
        print("generateurs-outil-temporaire.py " + VERSION + " (" + STATUT + ")")
        return 0
    if args.aide:
        parser.print_help()
        return 0

    # --- Nom obligatoire
    if not args.nom:
        print(RED + "[ERREUR] Parametre --nom obligatoire" + NC)
        print("  Usage : generateurs-outil-temporaire.py --nom <besoin> [--description <texte>]")
        return 1

    # --- Validation du nom : minuscules, chiffres, tirets, pas d'accents
    nom_corrige = args.nom.strip().lower().replace(" ", "-")
    if not NOM_VALIDE.match(nom_corrige):
        print(RED + "[ERREUR] Nom invalide : " + args.nom + NC)
        print(YELLOW + "  Le nom doit contenir uniquement des minuscules, chiffres et tirets" + NC)
        print(YELLOW + "  (pas d'accents, pas d'espaces, pas de caracteres speciaux)." + NC)
        return 1

    # --- Prefixe tmp- automatique
    if not nom_corrige.startswith("tmp-"):
        nom_corrige = "tmp-" + nom_corrige

    # --- Dossier de destination (par defaut : racine du workspace)
    workspace = resoudre_workspace()
    if args.dossier:
        dossier = args.dossier
    else:
        dossier = workspace

    dossier_abs = os.path.abspath(dossier)
    if not verifier_dans_workspace(dossier_abs, workspace):
        return 1

    chemin = os.path.join(dossier_abs, nom_corrige + ".py")
    date = datetime.date.today().isoformat()

    contenu = generer_script(nom_corrige, args.description.strip(), date)

    # --- Mode dry-run par defaut ; --force pour ecrire reellement
    if not args.force:
        print(YELLOW + "=== DRY-RUN (aucun fichier cree) : contenu de " + chemin + " ===" + NC)
        print(contenu)
        print(GREEN + "[OK] Re-lancer avec --force pour ecrire reellement le fichier." + NC)
        question_promotion(nom_corrige)
        return 0

    # --- Ecriture reelle
    if os.path.exists(chemin):
        print(RED + "[ERREUR] Le fichier existe deja : " + chemin + NC)
        print(YELLOW + "  Supprimer d'abord le fichier existant (supprimer-fichier) ou" + NC)
        print(YELLOW + "  choisir un autre nom de besoin." + NC)
        return 1

    try:
        with open(chemin, "w", encoding="ascii", newline="\n") as fh:
            fh.write(contenu)
    except Exception as exc:
        print(RED + "[ERREUR] Impossible d'ecrire " + chemin + " : " + str(exc) + NC)
        return 1

    print(GREEN + "[OK] Outil temporaire cree : " + chemin + NC)
    print(GREEN + "[OK] ASCII strict + LF pur appliques." + NC)
    print(GREEN + "[OK] Lire le .md d'usage avant utilisation (Pattern 9)." + NC)
    question_promotion(nom_corrige)
    return 0


if __name__ == "__main__":
    sys.exit(main())
