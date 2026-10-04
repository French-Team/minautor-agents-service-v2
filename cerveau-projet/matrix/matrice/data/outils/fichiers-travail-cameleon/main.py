"""Point d entree global de l outil fichiers-travail-cameleon (MO-378).

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

LA PORTE JUMELLE DU FLUX CAMELEON : le meme besoin que la porte d Optimus
(nommer, lister, montrer, vider, journaliser les fichiers de travail d une
mission), dans SON domicile. Elle CONSOMME les memes declarations partagees
(data/commun/zone_tmp.py : nom et chemin de la zone), elle ne copie AUCUN code
du jumeau : sa forme de nom est M- (celle de son pilote), pas MO-.

Usage (par le lanceur, jamais par un chemin de brique recopie) :
  python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon nommer --mission M-378 --libelle bilan
  python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon lister [--mission M-378] [--strict] [--json]
  python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon montrer m-378-bilan.txt
  python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon vider [--mission M-378] [--par <qui>]
  python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon journal [--n 20]
  python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon --auto-test

CODES DE SORTIE : 0 ok ; 1 ecart (purge partielle, ou --strict devant un residu) ;
2 refus.
"""
import sys

from journal.entry import executer as journal_executer
from lister.entry import executer as lister_executer
from montrer.entry import executer as montrer_executer
from nommer.entry import executer as nommer_executer
from vider.entry import executer as vider_executer


def lancer_auto_test(arguments):
    """Verbe de service : rejoue le cobaye de la porte (dossier jetable).

    Il est declare COMME VERBE pour que l option EN TETE --auto-test ne soit pas
    refusee par le garde de service (options.refuser_option_en_tete) : un outil
    qui declare ses verbes refuse toute option a leur place, SAUF celles qu il
    declare aussi.
    """
    from autotest import auto_test
    return auto_test()


COMMANDES = {
    "nommer": nommer_executer,
    "lister": lister_executer,
    "montrer": montrer_executer,
    "vider": vider_executer,
    "journal": journal_executer,
    "--auto-test": lancer_auto_test,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
