"""Point d'entree global de l'outil suivi-optimus.

Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py noter --mission MO-XXX --theme SUIVI --action <action> --detail "..."  (Optimus : MO- ; M- = cameleon)
                        [--fichiers "a,b"] [--portes "a,b"] [--duree-s N]
    python main.py lire [--mission M] [--action <action>] [--n N]
    python main.py verifier
    python main.py coherence [--racine <matrix>]  (croise la file du pilote et le journal)
    python main.py archiver [--racine <matrix>] [--doublons]
                                       (sort du journal, en les ARCHIVANT : par defaut
                                       les evenements HORS PERIMETRE OPTIMUS ; avec
                                       --doublons, les 2e debut / 2e fin d une meme
                                       mission -- l ECART que `verifier` remonte, le
                                       PREMIER evenement fait foi ; archive dediee
                                       suivi-optimus-doublons.jsonl)
    python main.py corriger [--mission MO-XXX] --motif "..." [--simuler oui]
                                       (corrige EN PLACE une duree_s DECLAREE qui
                                       contredit la mesure des bornes : la valeur
                                       honnete est VIDE, l ancienne valeur reste
                                       relisible dans `corrections`)
    python main.py vue   (genere la vue markdown dediee _operateur/optimus-prime/suivi-optimus.md)
"""
import sys

from archiver.entry import executer as archiver_executer
from coherence.entry import executer as coherence_executer
from corriger.entry import executer as corriger_executer
from lire.entry import executer as lire_executer
from noter.entry import executer as noter_executer
from verifier.entry import executer as verifier_executer
from vue.entry import executer as vue_executer

COMMANDES = {
    "noter": noter_executer,
    "lire": lire_executer,
    "verifier": verifier_executer,
    "coherence": coherence_executer,
    "corriger": corriger_executer,
    "archiver": archiver_executer,
    "vue": vue_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    return COMMANDES[arguments[0]](arguments[1:])


if __name__ == "__main__":
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))