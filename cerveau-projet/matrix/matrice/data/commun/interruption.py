"""LE JUGEMENT D UNE INTERRUPTION DE ROUND (EO-436) : une regle, UN domicile (M-076).

POURQUOI UN DOMICILE (MO-464) : la panne nommee en EO-436 -- le pilote PARQUE sa
mission (report) et CHARGE la suivante dans le MEME geste -- est lue par DEUX
consommateurs, tous deux dans le chargement du pilote :
  - la mission simple (file/fonctions.py, `charger_mission`) ;
  - le LOT (file/fonctions.py, `charger_lot`).
Deux copies de cette regle divergeraient en silence (L-029) : elle vit donc ici, et
les deux la CONSOMMENT au lieu de la recopier.

LA MESURE (2026-09-25, rapportee par MO-416) : `report` de MO-409 a 09:54:00, puis
`charge` de MO-416 a 09:54:01 -- dans la meme seconde, la file porte DEUX missions
OUVERTES : la parquee (qui reprendra son round) et la forgee (que personne ne sert
avant 21:29). Le round courant n a pas ete ferme : la file ne dit plus QUELLE
mission le round reprend, et le suivi du pilote a accuse une CLOTURE FAUSSE qui
n avait pas eu lieu (l exemption du meme jour l excuse, elle ne le repare pas).

LA REGLE (option a, tranchee en MO-464) : une interruption PARQUE, elle ne CHARGE
pas. Forger une mission pendant qu un round parque attend sa reprise laisserait
DEUX missions ouvertes, et une mission forgee sans round est INDISCERNABLE d une
mission qui attend son tour (L-207 : la forme d un artefact a UN domicile, et tous
ses consommateurs le LISENT).
Le remede est le GESTE, pas une exception : `charger --conduire` forge ET sert dans
le meme geste -- la mission nait AVEC son round, donc il n existe jamais de mission
forgee sans round a cote d un round parque.

CE QUE CE MODULE NE JUGE PAS : il ne juge pas le DROIT d interrompre (le geste reste
permis, et `reporter` reste sa porte) ; il juge l ETAT de la file au moment ou une
mission NOUVELLE y entre.
"""

# Les champs juges sont ceux de la FILE : c est elle qui les ECRIT
# (pilote/file/fonctions.py pour `chargee_le` et `statut`,
# pilote/reporter/fonctions.py pour `reporte_le` et `raison_report`).
# Ce module les LIT, et il ne les invente pas.
CHAMP_STATUT = "statut"
VALEUR_EN_ATTENTE = "en-attente"
VALEUR_EN_COURS = "en-cours"
CHAMP_REPORTE_LE = "reporte_le"
CHAMP_RAISON_REPORT = "raison_report"


def mission_en_cours(file_missions):
    """La mission EN COURS, ou None (serie stricte : au maximum une)."""
    for mission in (file_missions or {}).get("missions", []) or []:
        if mission.get(CHAMP_STATUT) == VALEUR_EN_COURS:
            return mission
    return None


def mission_parquee(file_missions):
    """La mission PARQUEE, ou None -- celle qui ATTEND sa reprise.

    PARQUEE veut dire DEUX choses, et les deux sont exigees : son statut est
    `en-attente` ET elle porte la trace de son report (`reporte_le`, ecrit par le
    verbe `reporter`). Une mission `en-attente` SANS `reporte_le` n a JAMAIS ete
    parquee : elle ATTEND son tour (lot ou file) et n a rien d une interruption --
    c est l exemption qui interdit a cette regle de crier sur la file ordinaire.
    """
    for mission in (file_missions or {}).get("missions", []) or []:
        if mission.get(CHAMP_STATUT) != VALEUR_EN_ATTENTE:
            continue
        if mission.get(CHAMP_REPORTE_LE):
            return mission
    return None


def round_parque_en_attente(file_missions):
    """La mission parquee qui attend sa reprise, ou None -- et None si un round EST en cours.

    Un round EN COURS tient le creneau : il n y a alors plus rien a reprendre, et le
    refus de la serie stricte parle a sa place (une seule forme par regle). Ce
    jugement ne juge donc QUE l etat ou la file n a plus AUCUN round ouvert mais
    porte encore une mission parquee : c est exactement l entre-deux du geste
    mesure (parquer puis charger dans la meme seconde).
    """
    if mission_en_cours(file_missions) is not None:
        return None
    return mission_parquee(file_missions)
