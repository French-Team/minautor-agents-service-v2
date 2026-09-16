"""Point d'entree principal de l'outil executer.

Sac a dos : guide l'outil dans tous les cas d'usage.
Dispatch : executer | --help | sans arg.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def afficher_aide():
    """Affiche l'aide de l'outil."""
    print("Outil EXECUTER -- Execution Python seule (pas de shell)")
    print("")
    print("Verbes :")
    print("  executer  --cmd <commande> [--timeout N] [--contenu-chemin @file] [--json]")
    print("")
    print("Regles absolues :")
    print("  - Python seul (pas de bash/sh/cmd/powershell)")
    print("  - Pas de pipe (|)")
    print("  - Pas de redirection (>, 2>/dev/null)")
    print("  - Pas de heredoc (<<)")
    print("  - Pas de curl/wget")
    print("")
    print("Codes retour : 0=succes, 1=echec commande, 2=refus/erreur")
    print("")
    print("Exemples :")
    print('  executer --cmd "python3 -m py_compile foo.py"')
    print('  executer --cmd "python3 -m json.tool data.json" --json')
    print('  executer --contenu-chemin @commande.txt --timeout 120')


def main():
    """Point d'entree : sac a dos + dispatch."""
    arguments = sys.argv[1:]

    if not arguments:
        afficher_aide()
        return 0

    premier = arguments[0]

    if premier in ("--help", "-h", "help"):
        afficher_aide()
        return 0

    if premier == "executer":
        from executer.entry import executer
        return executer(arguments[1:])

    # Si premier arg ressemble a --cmd, c'est executer implicite
    if premier.startswith("--"):
        from executer.entry import executer
        return executer(arguments)

    print(f"ERREUR : verbe inconnu '{premier}'. Verbs : executer")
    print("Usage : python3 main.py executer --cmd <commande>")
    return 2


if __name__ == "__main__":
    sys.exit(main())
