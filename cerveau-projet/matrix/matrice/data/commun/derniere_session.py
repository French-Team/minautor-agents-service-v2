"""Moteur partage : la DERNIERE session d'une BDD sessions (M-076, MO-092).

Un moteur se PARTAGE, il ne se recopie pas (lecon L-029) : le pilote
(injection/cycle.py, reprise de session) et l'outil bdd-sessions (lire
--derniere) lisent la meme fonction, jamais deux copies.

Le contrat de ce moteur est le FORMAT des entrees de data/sessions.json
(id, date, session, tags, source), pas son chemin : chaque lecteur charge
son propre fichier et passe la liste des entrees.

MO-125 -- L'ORDRE DES ENTREES EST DEPARTAGE : la cle de recence est
(horodatage, rang d'append). Le rang vient de la POSITION dans le fichier --
la BDD est en ajout seul, donc l'entree ECRITE APRES est la plus recente. Sans
ce departage, deux entrees a la MEME SECONDE s'inversaient selon l'ordre de
lecture : l'accident S-052/S-053 de MO-119 (une cloture et une ouverture a la
meme seconde) faisait trancher la reprise pour la CLOTURE, et la seule
reparation possible etait de RE-NOTER l'entree. Chaque lecteur passe donc la
liste DANS L'ORDRE DU FICHIER.
"""
from datetime import datetime

# Le FORMAT de l'horodatage appartient au contrat de trace (MO-121/MO-124) :
# celui qui ECRIT, celui qui RE-DATE et celui qui LIT partagent la MEME
# constante (data/commun/trace_session.py) -- deux formats qui divergent,
# c'est le trou que MO-121 a ferme (L-029 : un contrat se declare a UN domicile).
from trace_session import FORMAT_HORODATAGE  # noqa: E402

FORMAT_DATE = FORMAT_HORODATAGE
TAG_OUVERTURE = "session-ouverte"
TAG_FERMETURE = "session-fermee"


def _parse_date(valeur):
    """Retourne la date exploitable d'une entree, ou None (jamais d'exception).

    Une donnee corrompue ne doit pas tuer la reprise : l'entree est ignoree.
    """
    if not isinstance(valeur, str):
        return None
    try:
        return datetime.strptime(valeur, FORMAT_DATE)
    except ValueError:
        return None


def _cle_recence(entree, rang):
    """La cle d'ORDRE d'une entree : (horodatage, rang d'append), ou None.

    Le rang est la POSITION dans la liste -- et les lecteurs passent la liste
    dans l'ordre du fichier, en ajout seul. A la MEME SECONDE, l'entree ecrite
    APRES est donc la plus recente : sans ce departage, l'ordre depend de la
    lecture et la reprise peut annoncer l'INVERSE de la verite (MO-125,
    accident S-052/S-053 de MO-119). Une entree sans date exploitable rend
    None : elle est ignoree, jamais une exception.
    """
    date = _parse_date(entree.get("date"))
    if date is None:
        return None
    return (date, rang)


def _rang_de(entrees, entree):
    """La position de `entree` dans la liste, sinon -1 (jamais d'exception).

    L'identite d'abord (le cas normal : le lecteur a pris l'entree DANS cette
    liste), puis l'id (une copie de la meme entree) : un appelant qui recopie
    l'entree ne perd pas son rang.
    """
    identifiant = (entree or {}).get("id")
    for rang, candidate in enumerate(entrees):
        if candidate is entree:
            return rang
    if identifiant is not None:
        for rang, candidate in enumerate(entrees):
            if candidate.get("id") == identifiant:
                return rang
    return -1


def derniere_session(entrees):
    """Fonction PURE : la derniere session fermee, sinon la derniere ouverte.

    Retourne (entree, etat) avec etat in {"fermee", "ouverte", "aucune"} :
      - "fermee" : la derniere session a avoir ete cloturee proprement ;
      - "ouverte" : aucune cloture, ou une ouverture PLUS RECENTE que la
        derniere cloture (session precedente jamais fermee -- le cas de la
        session interrompue, a annoncer BIEN VISIBLE a la reprise).
    La recence est (horodatage, rang d'append) : deux entrees a la meme
    seconde sont departagees par l'ORDRE D'ECRITURE, jamais par l'ordre de
    lecture (MO-125). Une entree sans date exploitable est ignoree, pas une
    exception.
    """
    fermee = None
    ouverte = None
    for rang, entree in enumerate(entrees):
        tags = entree.get("tags", [])
        cle = _cle_recence(entree, rang)
        if cle is None:
            continue
        if TAG_FERMETURE in tags:
            if fermee is None or cle > fermee[0]:
                fermee = (cle, entree)
        elif TAG_OUVERTURE in tags:
            if ouverte is None or cle > ouverte[0]:
                ouverte = (cle, entree)
    if fermee is not None:
        if ouverte is not None and ouverte[0] > fermee[0]:
            return ouverte[1], "ouverte"
        return fermee[1], "fermee"
    if ouverte is not None:
        return ouverte[1], "ouverte"
    return None, "aucune"

def entrees_apres(entrees, entree):
    """Les entrees PLUS RECENTES que `entree` (la trace a-t-elle avance ?).

    Retourne (nombre, derniere) : le nombre d'entrees posterieures et la
    derniere d'entre elles, ou (0, None). Une entree sans date exploitable
    est ignoree, jamais une exception.

    "Plus recente" se mesure sur la MEME cle que la reprise -- (horodatage,
    rang d'append) : une entree ecrite apres, a la MEME seconde, compte comme
    posterieure (sinon le garde de retard serait aveugle exactement dans le
    cas ou l'ordre est le plus douteux, MO-125).
    """
    date_reference = _parse_date((entree or {}).get("date"))
    if date_reference is None:
        return 0, None
    cle_reference = (date_reference, _rang_de(entrees, entree))
    posterieures = []
    for rang, candidate in enumerate(entrees):
        cle = _cle_recence(candidate, rang)
        if cle is not None and cle > cle_reference:
            posterieures.append((cle, candidate))
    if not posterieures:
        return 0, None
    derniere = max(posterieures, key=lambda element: element[0])
    return len(posterieures), derniere[1]
