"""Point d'entree global de l'outil domicilier (RE-CONDUITE de MO-171).

Role : DIRIGER (router la commande). Aucune logique metier ici.

Une CLASSE est un motif RECOPIE : une meme fonction vivant dans plusieurs
fichiers. Mesure MO-169/MO-171 : 40 copies VIVANTES du meme parseur d options, en
22 textes DIFFERENTS -- elles avaient diverge en silence, sans qu'aucun controle
ne le voie. Le DOMICILE est le module qui porte le CONTRAT (data/commun/options.py).
Cette remorque aligne une CLASSE sur son DOMICILE, et elle est CONDUITE par un
PLAN qui declare tout -- la fonction, le marqueur, le remplacement, les EXTRAS
et surtout les EXCLUSIONS. Un plan incomplet est REFUSE : aligner a l'aveugle
ecrirait dans des fichiers dont personne n'a verifie le role.

Usage :
    python main.py auditer [--plan <chemin>] [--perimetre <dossier>] [--json]
    python main.py aligner [--plan <chemin>] [--perimetre <dossier>] [--simuler|--publier]

--simuler est le DEFAUT : sans --publier, la remorque DIT ce qu'elle ferait et
n'ecrit rien. Toute ecriture passe par la PORTE ecrire, fragments compris :
la remorque n'a AUCUN privilege d'ecriture.
"""
import sys

from aligner.entry import executer_verbe as aligner_executer
from auditer.entry import executer_verbe as auditer_executer

COMMANDES = {
    "auditer": auditer_executer,
    "aligner": aligner_executer,
}
CODE_SANS_COMMANDE = 2


def principal(arguments):
    """Route vers la categorie du verbe, ou rend l'aide (code 2)."""
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return CODE_SANS_COMMANDE
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper

    sys.exit(envelopper(principal, sys.argv[1:]))
