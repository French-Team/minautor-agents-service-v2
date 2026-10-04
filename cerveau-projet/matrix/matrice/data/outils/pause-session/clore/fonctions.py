"""Fonctions simples de la categorie clore : decision et trace PURES.

Regularisation (EO-357) : le journal append-only garde une pause SANS reprise
alors que le etat de pause a disparu. Le verbe reprendre REFUSE dans ce cas
(serie stricte : une mission est en cours). Ici, une reprise de REGULARISATION
est journalisee -- tracee et motivee -- sans jamais toucher la file du pilote.

La DECISION et la TRACE sont des fonctions PURES (tout leur est rendu en
arguments) : la garde PERMANENTE (verifier-contrats-outils.py, maillon 30 de la
non-regression) les eprouve sans toucher au journal reel.
"""
from commun import journaliser

# Verdicts de la decision (vocabulaire ferme rendu par diagnostiquer).
VERDICT_REGULARISATION = "regularisation"
VERDICT_MOTIF_MANQUANT = "motif-manquant"
VERDICT_ETAT_PRESENT = "etat-present"
VERDICT_RIEN_A_REGULARISER = "rien-a-regulariser"

# Vocabulaire de la trace (le lecteur `journal` lit la cle regularisation).
TYPE_REPRISE = "reprise"
CLE_REGULARISATION = "regularisation"


def diagnostiquer(motif, etat_present, dernier_evenement):
    """Decision PURE de clore : (code, verdict), sans aucun acces disque.

    (2, motif-manquant)     -- une regularisation sans motif ne se trace pas ;
    (1, etat-present)       -- la pause est LEGITIME : c est reprendre qui agit ;
    (1, rien-a-regulariser) -- le journal et le etat sont deja coherents ;
    (0, regularisation)     -- pause OUVERTE (dernier evenement = pause) et etat
                               ABSENT : la contradiction est regularisable.
    """
    if not (motif or "").strip():
        return 2, VERDICT_MOTIF_MANQUANT
    if etat_present:
        return 1, VERDICT_ETAT_PRESENT
    if not dernier_evenement or dernier_evenement.get("type") != "pause":
        return 1, VERDICT_RIEN_A_REGULARISER
    return 0, VERDICT_REGULARISATION


def evenement_regularisation(id_mission, motif):
    """(type, details) de la ligne de journal d une reprise de REGULARISATION.

    PURE : la garde permanente eprouve CETTE fonction, donc la trace (type +
    motif) est couverte sans ecrire dans le journal reel.
    """
    return TYPE_REPRISE, {"mission": id_mission, CLE_REGULARISATION: motif}


def journaliser_regularisation(id_mission, motif):
    """Journalise une reprise de REGULARISATION : close une pause orpheline.

    La file du pilote n est jamais touchee (aucun etat a lever, aucune mission a
    restaurer) : seul le journal append-only recoit la ligne.
    """
    type_evenement, details = evenement_regularisation(id_mission, motif)
    journaliser(type_evenement, details)
