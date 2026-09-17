"""La ZONE JETABLE d'un agent : la vider, et RENDRE ce qui a ete supprime.

Moteur PARTAGE (un seul domicile -- L-029/L-102) : les DEUX pilotes purgent leur
zone par ce code, Optimus (Flux 2, `tmp-optimus`) et le cameleon (Flux 1,
`tmp-cameleon`). Deux copies de cette logique divergeraient : l'une viderait,
l'autre oublierait -- et personne ne verrait la difference.

Regle immuable `perimetre-tmp`, point 4 : en fin de mission, le CONTENU de la
zone est VIDE (fichiers ET dossiers de cobaye), le README seul demeure. La preuve
d'un cobaye est son RESULTAT, lu a l'execution : le fichier qui dort n'est plus
une preuve. Sa suppression se TRACE (marbre ou journal), jamais silencieuse --
une preuve citee puis supprimee sans trace laisserait une citation vers du vide.

Ce que ce module NE fait PAS : la TRACE. Il ne sait pas ou chaque flux
journalise (le marbre d'Optimus, le journal du cameleon) : il REND la liste,
l'appelant l'ecrit avec ses mots.
"""

import shutil
from pathlib import Path

# Une zone jetable s'appelle `tmp-*` : le moteur REFUSE toute autre cible
# (L-006 : jamais un chemin devine, la cible est verifiee avant d'agir).
PREFIXE_ZONE = "tmp-"
NOM_README = "README.md"


def contenu(zone, nom_readme=NOM_README):
    """Les elements de la zone a vider (le README excepte), tries.

    Trie pour que la trace soit stable d'une execution a l'autre : une liste
    dans l'ordre du disque produirait un detail different a chaque passage.
    """
    zone = Path(zone)
    if not zone.is_dir():
        return []
    return sorted(p for p in zone.iterdir() if p.name != nom_readme)


def vider(zone, nom_readme=NOM_README):
    """Vide le contenu d'une zone `tmp-*` et rend (supprimes, echecs).

    Le README reste : la zone est PERMANENTE, c'est le chemin sur lequel
    s'appuient les cobayes et les outils (point 3 de la regle).

    Un element qui resiste (fichier verrouille) n'interrompt pas les autres : il
    est NOMME dans `echecs`. Une purge partielle qui se tairait serait une purge
    menteuse -- le garde dirait "sain" sur une zone encore pleine.

    Leve ValueError si la zone ne s'appelle pas `tmp-*` : c'est un refus, pas
    une erreur de parcours ; l'appelant l'annonce.
    """
    zone = Path(zone)
    if not zone.name.startswith(PREFIXE_ZONE):
        raise ValueError("Refus : " + str(zone) + " n'est pas une zone " + PREFIXE_ZONE + "*")
    supprimes = []
    echecs = []
    for element in contenu(zone, nom_readme):
        try:
            if element.is_dir():
                shutil.rmtree(str(element))
            else:
                element.unlink()
            supprimes.append(element.name)
        except OSError:
            echecs.append(element.name)
    return supprimes, echecs
