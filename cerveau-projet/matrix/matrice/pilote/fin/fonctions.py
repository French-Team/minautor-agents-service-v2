"""Fonctions simples de la categorie fin : une seule tache chacune.

Garde M-080 : la relance automatique est suspendue pendant une pause
session-matrix (protocole de pause, outil pause-session).
"""
from commun import (
    annoncer_fin,
    bilan_consolide,
    deposer_message,
    enregistrer_file,
    horodater,
    ids_en_lot,
    journaliser_mission,
    lot_termine,
    mission_en_cours,
    purger_zone_temporaire,
    rafraichir_vue_journal,
    session_en_pause,
)
from constants import (
    BOITE_MATRICE_IN,
    STATUT_TERMINEE,
)


def cloturer_mission(charger_file, bilan):
    """CLOTURE la mission en cours, puis, si un lot est arme :
    - annonce la FIN (k/n),
    - enchaine AUTOMATIQUEMENT la mission suivante du lot (DEBUT k+1/n),
    - au terme du lot : RETOUR consolide a la Matrice (bilan du lot entier).
    """
    file_missions = charger_file()
    mission = mission_en_cours(file_missions)
    if mission is None:
        print("REFUS : aucune mission en cours a cloturer.")
        return 1

    mission["statut"] = STATUT_TERMINEE
    mission["terminee_le"] = horodater()
    mission["bilan"] = bilan
    enregistrer_file(file_missions)

    journaliser_mission(
        {
            "type": "mission-terminee",
            "date": horodater(),
            "id": mission["id"],
            "theme": mission["theme"],
            "objectif": mission["objectif"],
            "chargee_le": mission["chargee_le"],
            "injectee_le": mission.get("injectee_le", ""),
            "terminee_le": mission["terminee_le"],
            "bilan": bilan,
        }
    )
    # VUE du journal du cameleon (MO-136, miroir de `suivi-optimus.md` cote
    # Optimus) : la vue derivee est regeneree par le PILOTE a la cloture, juste
    # apres la ligne de journal que l'on vient d'ecrire -- sans cet appel elle
    # restait figee sur la derniere construction manuelle (mesure du 2026-09-16 :
    # aucun appelant de `construire` du cote du flux 1).
    _code_vue, message_vue = rafraichir_vue_journal()
    if _code_vue != 0:
        print("ALERTE vue : " + message_vue)
    # Zone jetable (MO-136) : la mission est close, le PILOTE vide la zone et le
    # TRACE dans SON journal -- le point 4 de perimetre-tmp etait une discipline
    # d'agent, et une discipline qu'aucun instrument ne mesure depend de la
    # memoire.
    _code_purge, message_purge = purger_zone_temporaire(mission)
    print("[PURGE] " + message_purge)
    annoncer_fin(file_missions, mission)
    deposer_message(
        BOITE_MATRICE_IN,
        {
            "type": "fin-mission",
            "date": horodater(),
            "mission": mission["id"],
            "bilan": bilan,
        },
    )

    # Chaine du lot : la suivante, ou le RETOUR consolide.
    # Garde 1 : seule une mission DU LOT declenche la logique de lot
    # (la fin d'une mission hors lot ne rejoue jamais un RETOUR passe).
    ids_lot = ids_en_lot(file_missions)
    if mission["id"] not in ids_lot:
        # E-008 : fin HORS lot -> la boucle ne meurt jamais. La mission
        # suivante (file ou tresse) est relancee automatiquement.
        # M-080 : JAMAIS pendant une pause (gardes dans preparer_injection).
        if not session_en_pause():
            from injection.fonctions import preparer_injection

            preparer_injection(charger_file)
        else:
            print("SESSION EN PAUSE (M-080) : aucune relance automatique pendant la maintenance.")
        return 0
    if lot_termine(file_missions):
        retour = {
            "type": "retour-lot",
            "date": horodater(),
            "lot": file_missions.get("lot", {}).get("ids", []),
            "bilan_consolide": bilan_consolide(file_missions),
        }
        deposer_message(BOITE_MATRICE_IN, retour)
        # Garde 2 : le lot est DESAMORCE apres son RETOUR (il ne se rejoue pas).
        file_missions["lot"] = None
        enregistrer_file(file_missions)
        print("RETOUR : toutes les missions du lot sont terminees. Bilan consolide -> Matrice.")
        print("  " + retour["bilan_consolide"])
    else:
        from injection.fonctions import preparer_injection

        print("Enchainement automatique de la mission suivante du lot...")
        preparer_injection(charger_file)
    return 0
