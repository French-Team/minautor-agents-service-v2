"""Point d'entree global de l'outil chaine-pense-bete -> spec -> todo-list (EO-215, MO-224).

LA CHAINE : un seul document a NOM STABLE (arbitrage B), quatre etapes, quatre
familles d'ids (PB- / SP- / TD- / EX- ; l etat d EXECUTION est ajoute en MO-577
sur decision createur), et un avancement pose par la
PORTE des que les conditions tiennent (arbitrage D) -- la trace NEMESIS est
une CONDITION LUE, jamais une promesse. Domicile : l'espace preparation
(arbitrage A1).

Role : DIRIGER (router le verbe vers la categorie). Aucune logique metier ici.

Usage :
    naitre    --titre "..." [--objectif "..."]
    avancer   --id PB-001                    (s arrete a todo : l execution a son verbe)
    executer  --id PB-001 --preuve <chemin>  (constate la preuve SUR LE DISQUE, puis execute)
    revenir   --id PB-001                    (le sens inverse : execute se REFait)
    etat      [--id PB-001]
"""
import sys

from etape.entry import executer as etape_executer

COMMANDES = {
    "naitre": etape_executer,
    "avancer": etape_executer,
    "executer": etape_executer,
    "revenir": etape_executer,
    "etat": etape_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        # L USAGE EST DANS LE DOCSTRING, affiche juste au-dessus : ce module le
        # REECRIVAIT aussi, et une copie diverge des que l outil gagne un
        # verbe -- les deux verbes de MO-577 n y etaient pas.

        return 2
    return COMMANDES[arguments[0]](arguments)


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
