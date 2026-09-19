"""Point d'entree global de l'outil chaine-pense-bete -> spec -> todo-list (EO-215, MO-224).

LA CHAINE : un seul document a NOM STABLE (arbitrage B), trois etapes, trois
familles d'ids (PB- / SP- / TD-, arbitrage C), et un avancement pose par la
PORTE des que les conditions tiennent (arbitrage D) -- la trace NEMESIS est
une CONDITION LUE, jamais une promesse. Domicile : l'espace preparation
(arbitrage A1).

Role : DIRIGER (router le verbe vers la categorie). Aucune logique metier ici.
"""
import sys

from etape.entry import executer as etape_executer

COMMANDES = {
    "naitre": etape_executer,
    "avancer": etape_executer,
    "etat": etape_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        print("Usage : naitre --titre \"...\" [--objectif \"...\"] | avancer --id PB-001 | etat [--id PB-001]")
        return 2
    return COMMANDES[arguments[0]](arguments)


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
