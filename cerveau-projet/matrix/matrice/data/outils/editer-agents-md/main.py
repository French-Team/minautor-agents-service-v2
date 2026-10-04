"""Point d'entree global de l'outil editer-agents-md.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

L'outil de la session-matrix (v3) : comme la v1 (activer-agent-principal) et
la v2 (jarvis) ont leurs outils pour modifier AGENTS.md dans leur encart, la
Matrice a le sien. Il ne touche JAMAIS au reste du fichier (encarts v1/v2,
marbre constitution) : uniquement le bloc delimite session-matrix.

Usage :
    python main.py etat
    python main.py definir --nom-llm <id> --agent <nom> --raison "..."
    python main.py verifier
"""
import sys

from definir.entry import executer as definir_executer
from etat.entry import executer as etat_executer
from verifier.entry import executer as verifier_executer

COMMANDES = {
    "etat": etat_executer,
    "definir": definir_executer,
    "verifier": verifier_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
