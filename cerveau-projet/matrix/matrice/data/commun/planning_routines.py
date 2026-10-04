'''PLANNING DES ROUTINES -- lecture du planning, en UN SEUL DOMICILE (M-076).

Decision du createur D1 (2026-09-26, MO-429) : le PLANNING est la SOURCE des
cadences et de la mecanique d allumage ; chaque routine LE LIT, jamais l inverse.
Ce module est le motif partage : les 7 routines (leurs constantes), le SERVICE du
serveur de vie, la porte vie etat et les gardes passent par ICI.

Ce que le planning DETIENT (et rien d autre) : cadence, mode (passe | boucle),
decalage initial (la rotation d allumage), priorite, tolerance et la commande de
passe. Ce qui est declare AILLEURS (PID, drapeaux, temoin de cadence chez la
routine) reste ou il vit : UNE SEULE verite par chose.

Refus : un planning absent, illisible ou incomplet est REFUSE EN NOMMANT le
fichier et le champ faillant (L-055) -- jamais de defaut silencieux.
'''
import json
from pathlib import Path

ENCODAGE = 'utf-8'

# Ou vit le planning, RELATIF au dossier racine (le dossier qui CONTIENT matrice/).
# Le planning N EST PAS une routine : il vit CHEZ LE SERVICE (vie/, la famille
# qui gere la vie des routines) -- un dossier neuf sous routines/ nait du
# moule routine (EO-389), et le planning n est pas un squelette de routine.
CHEMIN_RELATIF = Path('matrice') / 'routines' / 'vie' / 'planning.json'

MODES = ('passe', 'boucle')
CHAMPS = (
    'nom',
    'cadence_secondes',
    'mode',
    'decalage_initial_secondes',
    'priorite',
    'tolerance_cadences',
    'commande_passe',
)

# Cache par processus, invalide des que le fichier bouge : le service vit des
# heures, il doit VOIR une decision posee pendant son tour, sans redemarrage.
_cache = {}


class PlanningIllisible(RuntimeError):
    '''Refus NOMME : le planning est absent, illisible ou incomplet.'''


def racine_du_planning(depuis=None):
    '''Le dossier qui CONTIENT matrice/ (le cobaye passe le sien).

    Par defaut : on REMONTE depuis ce module jusqu au dossier matrix par
    MARQUEUR (MO-088 : aucun parents[N] nu), et on REFUSE si le marqueur manque
    -- on ne devine jamais un chemin (garde-foi L-006).
    '''
    if depuis is not None:
        return Path(depuis)
    dossier = Path(__file__).resolve().parent
    while dossier.name != 'matrix':
        if dossier.parent == dossier:
            raise PlanningIllisible(
                'dossier matrix introuvable en remontant depuis ' + str(__file__)
            )
        dossier = dossier.parent
    return dossier


def chemin_planning(racine=None):
    '''Le chemin du fichier de planning (jamais devine : lu a sa source).'''
    return racine_du_planning(racine) / CHEMIN_RELATIF


def _valider(donnees, chemin):
    '''Valide la structure COMPLETE du planning, un champ par refus.

    Rend la liste des routines telles que lues. Une anomalie leve
    PlanningIllisible avec le nom du fichier ET du champ : un refus qui ne nomme
    pas son sujet oblige a relire le code (L-055).
    '''
    if not isinstance(donnees, dict):
        raise PlanningIllisible('planning illisible (objet attendu) : ' + str(chemin))
    routines = donnees.get('routines')
    if not isinstance(routines, list) or not routines:
        raise PlanningIllisible('champ routines absent ou vide : ' + str(chemin))
    vus = set()
    for index, entree in enumerate(routines):
        if not isinstance(entree, dict):
            raise PlanningIllisible('entree ' + str(index) + ' illisible : ' + str(chemin))
        for champ in CHAMPS:
            if champ not in entree:
                raise PlanningIllisible(
                    'champ ' + champ + ' absent de l entree ' + str(index)
                    + ' : ' + str(chemin)
                )
        nom = entree['nom']
        if not isinstance(nom, str) or not nom:
            raise PlanningIllisible('nom vide en entree ' + str(index) + ' : ' + str(chemin))
        if nom in vus:
            raise PlanningIllisible('routine ' + nom + ' en double : ' + str(chemin))
        vus.add(nom)
        if entree['mode'] not in MODES:
            raise PlanningIllisible(
                'mode ' + str(entree['mode']) + ' de ' + nom
                + ' attendu parmi ' + ' | '.join(MODES) + ' : ' + str(chemin)
            )
        for champ_nombre in (
            'cadence_secondes', 'decalage_initial_secondes', 'priorite', 'tolerance_cadences'
        ):
            valeur = entree[champ_nombre]
            if not isinstance(valeur, int) or isinstance(valeur, bool) or valeur < 0:
                raise PlanningIllisible(
                    'champ ' + champ_nombre + ' de ' + nom
                    + ' doit etre un entier positif : ' + str(chemin)
                )
        if entree['cadence_secondes'] <= 0:
            raise PlanningIllisible(
                'cadence de ' + nom + ' doit etre superieure a zero : ' + str(chemin)
            )
        commande = entree['commande_passe']
        if (not isinstance(commande, list) or not commande
                or not all(isinstance(morceau, str) for morceau in commande)):
            raise PlanningIllisible(
                'commande_passe de ' + nom + ' doit etre une liste de chaines : '
                + str(chemin)
            )
    return routines


def charger(racine=None):
    '''Le planning complet (dict), relu a chaque changement de fichier.'''
    chemin = chemin_planning(racine)
    try:
        marque = chemin.stat().st_mtime_ns
    except OSError:
        raise PlanningIllisible('planning introuvable : ' + str(chemin))
    en_cache = _cache.get(str(chemin))
    if en_cache is not None and en_cache[0] == marque:
        return en_cache[1]
    try:
        donnees = json.loads(chemin.read_text(encoding=ENCODAGE))
    except ValueError as erreur:
        raise PlanningIllisible('planning JSON illisible : ' + str(chemin) + ' (' + str(erreur) + ')')
    except OSError as erreur:
        raise PlanningIllisible('planning illisible : ' + str(chemin) + ' (' + str(erreur) + ')')
    routines = _valider(donnees, chemin)
    donnees['routines'] = routines
    _cache[str(chemin)] = (marque, donnees)
    return donnees


def entrees(racine=None):
    '''Les entrees du planning, en ORDRE DE SERVICE : priorite DECROISSANTE,
    puis decalage initial croissant, puis nom -- la rotation d allumage.'''
    routines = charger(racine)['routines']
    return sorted(
        routines,
        key=lambda entree: (-entree['priorite'], entree['decalage_initial_secondes'], entree['nom']),
    )


def noms(racine=None):
    return [entree['nom'] for entree in charger(racine)['routines']]


def entree(nom, racine=None):
    '''L entree d une routine, ou un refus NOMMANT ce qui manque.'''
    donnees = charger(racine)
    for entree_ in donnees['routines']:
        if entree_['nom'] == nom:
            return entree_
    raise PlanningIllisible(
        'routine ' + nom + ' absente du planning ' + str(chemin_planning(racine))
        + ' (presentes : ' + ', '.join(noms(racine)) + ')'
    )


def cadence_planning(nom, racine=None):
    '''La cadence de la routine -- LA source, celle que la routine LIT.

    C est la seule fonction que les constantes d une routine appellent : elles
    n exportent plus de valeur, elles exportent le RENVOI.
    '''
    return entree(nom, racine)['cadence_secondes']


# Raccourci pour le service et les gardes (une seule implementation, deux noms).
cadence = cadence_planning


def mode(nom, racine=None):
    return entree(nom, racine)['mode']


def mode_est_passe(nom, racine=None):
    return mode(nom, racine) == 'passe'


def tolerance(nom, racine=None):
    return entree(nom, racine)['tolerance_cadences']


def decalage(nom, racine=None):
    return entree(nom, racine)['decalage_initial_secondes']


def commande_passe(nom, racine=None):
    '''(script, arguments) de la PASSE de la routine -- la commande d allumage.'''
    commande = entree(nom, racine)['commande_passe']
    return commande[0], tuple(commande[1:])
