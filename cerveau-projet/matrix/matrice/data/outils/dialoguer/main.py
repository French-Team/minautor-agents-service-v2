"""Point d'entree principal de l'outil dialoguer.

Sac a dos : guide l'outil dans tous les cas d'usage.
Dispatch : dialoguer | plan | --help | sans arg.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def afficher_aide():
    """Affiche l'aide de l'outil."""
    print("Outil DIALOGUER -- Interaction createur (Flux 2 seul)")
    print("")
    print("Verbes :")
    print("  dialoguer  --question <texte> [--choix a,b,c] [--timeout N] [--json]")
    print("  plan       --todos <json_list> [--json]")
    print("")
    print("Codes retour : 0=reponse/succes, 1=timeout, 2=erreur")
    print("")
    print("Exemples :")
    print('  dialoguer --question "Quel theme prioritaire ?" --choix "A,B,C"')
    print('  dialoguer --question "Valider ?" --timeout 30')
    print('  plan --todos \'[{"task":"MO-001","completed":true}]\' --json')


def principal(arguments):
    """Point d'entree notable : le sac a dos NOTE l'usage (bdd-usages), puis dispatch."""

    if not arguments:
        afficher_aide()
        return 0

    premier = arguments[0]

    if premier in ("--help", "-h", "help"):
        afficher_aide()
        return 0

    if premier == "dialoguer":
        from dialoguer.entry import dialoguer
        return dialoguer(arguments[1:])

    if premier == "plan":
        from plan.entry import plan
        return plan(arguments[1:])

    if premier.startswith("--"):
        from dialoguer.entry import dialoguer
        return dialoguer(arguments)

    print(f"ERREUR : verbe inconnu '{premier}'. Verbs : dialoguer, plan")
    print("Usage : python3 main.py dialoguer --question <texte>")
    return 2


if __name__ == "__main__":
    import constants  # noqa: F401  -- pose le pont vers data/commun (le pont vit dans constants.py)
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
