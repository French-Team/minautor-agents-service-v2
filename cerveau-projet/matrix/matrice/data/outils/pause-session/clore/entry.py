"""Categorie clore : regularise une pause dont le etat a disparu.

EO-357 : le journal append-only garde une pause SANS reprise alors que le etat de
pause est ABSENT (contradiction des deux traces). Le verbe reprendre REFUSE dans
ce cas (serie stricte : une mission est en cours dans la file). Le verbe clore
JOURNALISE une reprise de REGULARISATION -- tracee par son motif -- sans toucher
la file du pilote ni le etat (il n y en a pas).

La DECISION vit dans clore.fonctions.diagnostiquer (fonction PURE) : cette
categorie ne fait que LIRE le disque, lui passer les faits et IMPRIMER le verdict.
"""
from commun import etat_existe, extraire_options, lire_journal
from constants import NOM_ETAT
from clore.fonctions import (
    VERDICT_ETAT_PRESENT,
    VERDICT_MOTIF_MANQUANT,
    VERDICT_RIEN_A_REGULARISER,
    diagnostiquer,
    journaliser_regularisation,
)

NOMS_OPTIONS = ("motif",)


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    motif = (options.get("motif") or "").strip()
    evenements = lire_journal(1)
    dernier = evenements[0] if evenements else None
    code, verdict = diagnostiquer(motif, etat_existe(), dernier)

    if verdict == VERDICT_MOTIF_MANQUANT:
        print("REFUS : le motif est OBLIGATOIRE (--motif \"...\") -- une regularisation se TRACE, jamais muette.")
        return code
    if verdict == VERDICT_ETAT_PRESENT:
        print("REFUS : un etat de pause EXISTE (" + NOM_ETAT + ") : cette pause est LEGITIME.")
        print("  Remede : python3 cerveau-projet/matrix/lancer.py pause-session reprendre (leve le etat ET journalise la reprise).")
        return code
    if verdict == VERDICT_RIEN_A_REGULARISER:
        print("REFUS : aucune pause ouverte a regulariser (journal et etat sont deja COHERENTS).")
        return code

    id_mission = dernier.get("mission", "?")
    journaliser_regularisation(id_mission, motif)
    print("PAUSE REGULARISEE : la ligne de pause du " + str(dernier.get("date", "?")) + " (mission " + id_mission + ") est CLOSE par une reprise tracee.")
    print("  Motif de regularisation : " + motif)
    print("  La file du pilote n a PAS ete touchee (aucun etat a lever, aucune mission a restaurer).")
    return 0
