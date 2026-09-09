"""Point d'entree global de l'outil pause-session.

Protocole de pause session-matrix (M-080) : la Matrice utilise le cameleon
(jamais l'inverse). Une pause = cameleon arrete, mission sauvegardee A LA
PAUSE SEULEMENT, session-matrix en pause (jamais cassee), notification
"maintenance" sans raison. La reprise restore a l'identique.

Usage :
    python main.py pause    [--raison "..."]      (manuel ou defcon 5)
    python main.py reprendre                     (apres maintenance user + optimus)
    python main.py etat                          (montre l'etat de pause s'il existe)
    python main.py perimetre --zones "a,b"       (reduit le perimetre de lecture cameleon)
    python main.py journal                       (derniers evenements pause/reprise)
"""
import sys

from etat.entry import executer as etat_executer
from journal.entry import executer as journal_executer
from pause.entry import executer as pause_executer
from perimetre.entry import executer as perimetre_executer
from reprendre.entry import executer as reprendre_executer

COMMANDES = {
    "pause": pause_executer,
    "reprendre": reprendre_executer,
    "etat": etat_executer,
    "perimetre": perimetre_executer,
    "journal": journal_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
