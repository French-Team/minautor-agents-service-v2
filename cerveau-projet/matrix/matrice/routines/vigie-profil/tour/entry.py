"""Categorie tour : orchestre UNE passe de vigie du profil utilisateur.

Interface entre main.py et les fonctions simples (tour/fonctions.py).
Retourne 0 si rien a signaler, 1 si une alerte a ete posee (ou si la fiche
est absente).

REGLE ANTI-BRUIT (correction MO-070, 2026-09-13) : le depot est borne par
MISSION, pas par champ rempli. Tant qu'une alerte est OUVERTE pour une fiche
incomplete, aucune nouvelle alerte n'est posee, meme si des champs se remplissent
entre-temps. L'ancienne regle re-alertait des que la SIGNATURE d'etat changeait
-- or la fiche du createur se remplit un champ a la fois, donc chaque champ
rempli changeait la signature : 4 depots en 3 minutes mesures dans l'inbox.

Seule la fiche COMPLETE ferme l'episode : la memoire est remise a zero et un
futur retour a l'incompletude ouvre un nouvel episode, sous reserve du plancher
de temps `ANTI_SPAM_SECONDES` (anti-clignotement).

La decision elle-meme vit dans `tour/fonctions.py` (decision_depot) : elle est
PURE, donc testable sans disque ni horloge reelle.

MO-082 -- ETAT ET HISTOIRE. La passe journalisait la MEME ligne `passe` a chaque
tour, meme quand rien n'avait bouge : mesure du 2026-09-14, 194 lignes identiques
sur 330 (58,8 %), une par tour de 900 s. Or le remplissage de la fiche est un
ETAT : il ne change pas entre deux passes. L'ETAT court (`vigie-profil-etat-passes.json`)
le porte donc a CHAQUE passe, ecrase ; l'HISTOIRE ne recoit la passe que si ce
qu'elle a VU a change -- et ce changement EST le fait. Le MOTIF de la decision
anti-spam vit dans l'etat court lui aussi : aucune decision n'est supprimee en
silence (seule la REPETITION l'est, et elle est comptee -- `passes_absorbes`).
"""
from datetime import datetime

from battement import ajouter_passe
from commun import (
    ecrire_etat_passes,
    ecrire_json_atomique,
    horodater,
    journaliser,
    lire_etat_passes,
    lire_json,
)
from constants import CHEMIN_ETAT, CLE_ANNEAU_PASSES, PASSES_GARDEES_ETAT
from etat_histoire import decision_fait, signature_fait
from tour.fonctions import alerter, decision_depot, etat_profil

ETAT_PAR_DEFAUT = {"signature": "", "alerte_le": "", "etat": "jamais-verifie"}


def journaliser_passe(etat, deposer, motif):
    """ETAT et HISTOIRE d'une passe : le journal ne recoit la passe que si elle CHANGE.

    MO-082 -- mesure du 2026-09-14 : 194 lignes identiques sur 330 (58,8 %), une
    par tour de 900 s. Une passe est un ETAT (le remplissage de la fiche) : il part
    dans l'etat court, ecrit a CHAQUE passe et ECRASE. L'HISTOIRE ne recoit la
    passe que si ce qu'elle a VU a change -- et ce changement EST le fait.

    Le MOTIF de la decision anti-spam vit dans l'etat court lui aussi : aucune
    decision ne disparait en silence (seule la REPETITION l'est, et elle est
    comptee -- `passes_absorbes`).

    Rend (notable, mode) : la decision elle-meme, pour que le cobaye du garde
    permanent l'eprouve sans disque de service.
    """
    vu = {
        "present": etat["present"],
        "pourcentage": etat["pourcentage"],
        "attendus_vides": etat["attendus_vides"],
        "optionnels_vides": etat["optionnels_vides"],
    }
    passe_avant = lire_etat_passes()
    signature = signature_fait(vu)
    notable, mode = decision_fait(signature, passe_avant.get("signature"))
    absorbes = int(passe_avant.get("passes_absorbes") or 0)

    if notable:
        # Un FAIT : la fiche a change (un champ s'est rempli, un autre s'est vide).
        journaliser({
            "type": "passe", **vu,
            "depot": deposer, "motif": motif, "mode": mode,
            "passes_absorbes": absorbes,
        })

    # L'ETAT court : ecrit a CHAQUE passe, ECRASE. Il porte ce que la passe a vu,
    # ce qu'elle a decide, et le compte des passes absorbees depuis la derniere
    # ligne d'histoire -- la redondance supprimee est TRACEE, jamais silencieuse.
    maintenant = horodater()
    ecrire_etat_passes({
        **vu,
        # LA DATE DE LA PASSE : sans elle, le battement REEL d'une routine
        # absorbante n'est mesurable nulle part (friction 28 : rien ne comparait
        # le battement reel a la cadence declaree).
        "date": maintenant,
        "motif": motif,
        "mode": mode,
        "signature": signature if notable else (passe_avant.get("signature") or ""),
        "passes_absorbes": 0 if notable else absorbes + 1,
        "derniere_ecriture": maintenant if notable else (passe_avant.get("derniere_ecriture") or ""),
        # L'ANNEAU DES PASSES : c'est LUI qui rend le battement mesurable en
        # MEDIANE. `passes_absorbes` / `derniere_ecriture` disent COMBIEN de
        # passes ont ete absorbees ; ils ne disent pas QUAND -- une moyenne sur
        # ces deux nombres est fausse des qu'une passe n'est pas a l'heure.
        CLE_ANNEAU_PASSES: ajouter_passe(
            passe_avant.get(CLE_ANNEAU_PASSES), maintenant, PASSES_GARDEES_ETAT
        ),
    })
    return notable, mode


def executer(arguments):
    etat = etat_profil()
    memoire = lire_json(CHEMIN_ETAT, dict(ETAT_PAR_DEFAUT))
    deposer, motif = decision_depot(etat, memoire, datetime.now())

    # --- ETAT et HISTOIRE (MO-082) : la passe est un ETAT, son CHANGEMENT un fait
    journaliser_passe(etat, deposer, motif)

    if not etat["attendus_vides"]:
        if memoire.get("signature"):
            # La fiche vient d'etre completee : on remet la memoire a zero.
            ecrire_json_atomique(
                CHEMIN_ETAT,
                {"signature": "", "alerte_le": memoire.get("alerte_le", ""), "etat": "complete",
                 "complete_le": horodater()},
            )
            journaliser({"type": "profil-complet", "pourcentage": etat["pourcentage"]})
            print("Fiche profil COMPLETE : alerte close, memoire remise a zero.")
            return 0
        print("Fiche profil complete (" + str(etat["pourcentage"]) + "%).")
        return 0

    if not deposer:
        print(
            "Fiche profil incomplete (" + str(etat["pourcentage"]) + "%) : pas de nouveau "
            "signal (" + motif + ")."
        )
        return 0

    code, sortie = alerter(etat)
    if code != 0:
        journaliser({"type": "alerte-echec", "code": code, "detail": sortie[:300]})
        print("ALERTE NON POSEE : " + sortie[:200])
        return 1

    ecrire_json_atomique(
        CHEMIN_ETAT,
        {
            "signature": etat["cle"],
            "alerte_le": horodater(),
            "etat": "incomplete",
            "pourcentage": etat["pourcentage"],
            "attendus_vides": etat["attendus_vides"],
        },
    )
    journaliser({"type": "alerte-posee", "pourcentage": etat["pourcentage"],
                 "attendus_vides": etat["attendus_vides"]})
    print("ALERTE POSEE dans l'inbox de la Matrice :")
    print("  " + etat["description"])
    return 1
