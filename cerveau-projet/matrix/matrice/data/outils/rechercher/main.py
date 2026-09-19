"""Point d'entree principal de l'outil rechercher.

Sac a dos : guide l'outil dans tous les cas d'usage.
Dispatch : rechercher | indexer | schema | --help | sans arg.
"""
import sys
import os

# Ajoute le repertoire parent au path pour les imports constants/commun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import REPERTOIRE_OUTIL
from commun import extraire_options


def afficher_aide():
    """Affiche l'aide de l'outil."""
    print("Outil RECHERCHER -- Moteur de recherche unifie (fichiers + BDD)")
    print("")
    print("Verbes :")
    print("  rechercher   --requete <texte> [--dans fichiers|bdd|tous]")
    print("               [--tag <tag>] [--mot-cle <texte>] [--source <nom>]")
    print("               [--periode 7j] [--json] [--limite N]")
    print("  indexer      (rebuild index, palier 2 futur)")
    print("  schema       (affiche les options)")
    print("")
    print("Codes retour : 0=succes, 1=aucun resultat, 2=refus/erreur")
    print("")
    print("Exemples :")
    print('  rechercher --requete "defcon" --dans tous')
    print('  rechercher --requete "L-016" --dans bdd --tag GOUVERNANCE')
    print('  rechercher --requete "moteur" --dans fichiers --json')
    print('  rechercher --requete "auto-evolution" --dans bdd --source lecons --periode 30j')


def afficher_schema():
    """Affiche le schema des options."""
    print("Schema RECHERCHER :")
    print("  --requete <texte>    (requis) Texte a rechercher (regex supportee)")
    print("  --dans <fichiers|bdd|tous>  Scope (defaut: tous)")
    print("  --tag <tag>          FILTRE par tag BDD (liste des tags de l'entree)")
    print("  --mot-cle <texte>    FILTRE par mot-cle (contenu de l'entree)")
    print("  --source <nom>       FILTRE de source BDD (source inconnue = refus 2)")
    print("  --periode <7j|30j|3m|1a>  FILTRE temporel (ecarte ce qui n'a pas de date)")
    print("  --json               Sortie machine JSON (ASCII pur)")
    print("  --limite <N>         Nombre max de resultats (defaut: 50)")
    print("")
    print("Un filtre RETIRE : il ne peut pas ajouter de resultat.")


def principal(arguments):
    """Point d'entree notable : le sac a dos NOTE l'usage (bdd-usages), puis dispatch."""
    # Garde d'encodage (EO-105) : une console cp1252 ne doit JAMAIS faire echouer
    # la porte. La sortie machine est deja en ASCII pur ; ce garde couvre la
    # sortie humaine (un extrait de fichier peut porter un caractere exotique).
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass

    # Sans argument : aide
    if not arguments:
        afficher_aide()
        return 0

    premier = arguments[0]

    # --help ou aide
    if premier in ("--help", "-h", "help"):
        afficher_aide()
        return 0

    # schema
    if premier == "schema":
        afficher_schema()
        return 0

    # Dispatch verbes
    if premier == "rechercher":
        from rechercher.entry import rechercher
        return rechercher(arguments[1:])

    if premier == "indexer":
        from indexer.entry import indexer
        return indexer(arguments[1:])

    # Si premier arg ressemble a une option, c'est rechercher implicite
    if premier.startswith("--"):
        from rechercher.entry import rechercher
        return rechercher(arguments)

    print(f"ERREUR : verbe inconnu '{premier}'. Verbs : rechercher, indexer, schema")
    print("Usage : python3 main.py rechercher --requete <texte> [--dans ...]")
    return 2


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
