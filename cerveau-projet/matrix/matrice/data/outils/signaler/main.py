"""Point d'entree principal de l'outil signaler.

Le cameleon signale un probleme outil a la Matrice.
La Matrice route vers intercom maintenance (Optimus).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def afficher_aide():
    """Affiche l'aide de l'outil."""
    print("Outil SIGNALER -- Signaler un probleme outil a la Matrice")
    print("")
    print("Verbes :")
    print("  signal  --outil <nom> --niveau <niveau> --description <texte>")
    print("          [--mission <id>] [--erreur <texte>] [--json]")
    print("")
    print("Niveaux :")
    print("  critique  Outil en panne totale, mission impossible")
    print("  haute     Bug bloquant, mission ralentie")
    print("  moyenne   Amelioration manquante, mission defaillante")
    print("  basse     Souhait d'amelioration, pas bloquant")
    print("")
    print("Codes retour : 0=depot OK, 2=erreur")
    print("")
    print("Exemple :")
    print('  signal --outil "lire" --niveau critique')
    print('         --description "Le fichier de 5000 lignes est tronque a 2000"')
    print('         --mission "M-042" --erreur "troncature silencieuse"')


def principal(arguments):
    """Point d'entree notable : le sac a dos NOTE l'usage (bdd-usages), puis dispatch."""

    if not arguments:
        afficher_aide()
        return 0

    premier = arguments[0]

    if premier in ("--help", "-h", "help"):
        afficher_aide()
        return 0

    if premier == "signaler":
        from signaler.entry import signaler
        return signaler(arguments[1:])

    if premier.startswith("--"):
        from signaler.entry import signaler
        return signaler(arguments)

    print(f"ERREUR : verbe inconnu '{premier}'. Verbs : signal")
    return 2


if __name__ == "__main__":
    import constants  # noqa: F401  -- pose le pont vers data/commun (le pont vit dans constants.py)
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
