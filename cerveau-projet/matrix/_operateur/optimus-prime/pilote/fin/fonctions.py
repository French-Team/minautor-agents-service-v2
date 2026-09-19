"""Fonctions simples de la categorie fin : une seule tache chacune.

Garde M-080 : la relance automatique est suspendue pendant une pause
session-matrix (protocole de pause, outil pause-session).
"""
from commun import (
    annoncer_fin,
    balayer_famille_conservation,
    archiver_anciennes_missions,
    archiver_famille_conservation,
    bilan_consolide,
    controler_borne_conservation,
    crier_borne_rompue,
    crier_mission_muette,
    deposer_message,
    declarer_borne_marbre,
    enregistrer_file,
    entretenir_suivi,
    fichiers_de_la_mission,
    horodater,
    ids_en_lot,
    journaliser_mission,
    lot_termine,
    mission_en_cours,
    portee_lot,
    nettoyer_intercom,
    noter_session,
    purger_zone_temporaire,
    rattraper_fichiers_non_traces,
    resume_mission,
    session_en_pause,
    verification_post_fin,
    verifier_serie_stricte,
)
from constants import (
    BOITE_MATRICE_IN,
    CHAMP_DEFAUTS_MISSION,
    STATUT_DEFAUT_REPARE,
    STATUT_TERMINEE,
)


def cloturer_mission(charger_file, bilan, defauts=None):
    """CLOTURE la mission en cours, puis, si un lot est arme :
    - annonce la FIN (k/n),
    - enchaine AUTOMATIQUEMENT la mission suivante du lot (DEBUT k+1/n),
    - au terme du lot : RETOUR consolide a la Matrice (bilan du lot entier).
    Les DEFAUTS d'outil rencontres en travaillant (R5, audit MO-174) VOYAGENT
    avec la mission -- fichier, journal, retour Matrice. Un defaut NON REPARE est
    un POINT OUVERT : il est CRIE, jamais une note de bas de page.
    """
    defauts = defauts or []
    file_missions = charger_file()
    mission = mission_en_cours(file_missions)
    if mission is None:
        print("REFUS : aucune mission en cours a cloturer.")
        return 1

    # Position dans le lot AVANT la bascule de statut (MO-102) : apres, la
    # mission n'est plus `en-cours` et la position ne serait plus calculable.
    portee = portee_lot(file_missions)
    mission["statut"] = STATUT_TERMINEE
    mission["terminee_le"] = horodater()
    mission["bilan"] = bilan
    # DEFAUTS STRUCTURES (R5) : attaches a la MISSION, pas seulement au recit du
    # bilan. Le fichier les porte (ils survivent a la session), le journal les
    # historise, le retour Matrice les remonte. Un defaut lisible par un
    # instrument est un defaut qu'on peut SUIVRE ; un defaut qui ne vit que dans
    # une phrase se perd au premier changement de session.
    if defauts:
        mission[CHAMP_DEFAUTS_MISSION] = defauts
        non_repares = [d for d in defauts if d.get("statut") != STATUT_DEFAUT_REPARE]
        print("DEFAUTS DECLARES : " + str(len(defauts)) + " (dont "
              + str(len(non_repares)) + " non repare(s)).")
        for defaut in non_repares:
            # Le cri porte l'OUTIL et son ETAT : la Matrice voit ce qui reste
            # ouvert sans relire le recit (lecon de la friction 68 -- une alerte
            # qui ne vit que dans un tuyau se perd).
            print("  [A SUIVRE] [" + (defaut.get("statut") or "sans statut") + "] "
                  + defaut["outil"] + " : " + defaut["defaut"])
    enregistrer_file(file_missions)

    # Archivage automatique si plafond depasse (50 missions terminees max en actif)
    nb_archived = archiver_anciennes_missions(file_missions)
    if nb_archived > 0:
        print(f"ARCHIVAGE : {nb_archived} ancienne(s) mission(s) deplacee(s) dans l'archive.")

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
            CHAMP_DEFAUTS_MISSION: defauts,
        }
    )
    # Suivi-optimus : marbre L-020 (2026-09-11) -- "Le pilote ne note RIEN" :
    # c'est OPTIMUS qui declare sa fin via la porte noter. L'appel automatique
    # a `noter` ici creait un 2e fin (doublon MO-030, attrape par verifier le 2026-09-13).
    # En revanche la VUE derivee est bien rafraichie par le pilote : FIN.
    # BDD sessions (MO-092) : la trace persistante entre sessions LLM.
    # Un fait = mission finie + theme : la reprise de la PROCHAINE session
    # relit cette entree au lieu de deviner ce qui a ete fait. Non bloquant.
    code_session, sortie_session = noter_session(
        "travail",
        "Mission " + mission["id"] + " terminee (theme " + mission["theme"] + ") : " + bilan,
        mission=mission["id"],
    )
    if code_session != 0:
        print("ALERTE BDD sessions : fait non trace (" + sortie_session[:120] + ").")

    # Marbre (MO-108) : le pilote declare la borne de FIN, en mode
    # `--si-absent oui` (si l'agent l'a deja declaree, rien n'est double).
    # Motif mesure le 2026-09-15 : MO-105/MO-106 terminees sans fin au marbre.
    # MO-139 : la borne est declaree AVANT la vue, parce que la vue PROJETTE le
    # journal. Regeneree d'abord, elle montrait la mission encore "en cours"
    # alors que le pilote venait de la clore -- et rien ne la rafraichissait plus
    # avant la mission suivante (l'ordre etait une cecite d'une mission).
    fichiers_mission = fichiers_de_la_mission(mission["id"])
    declarer_borne_marbre(
        mission,
        "fin",
        "fin declaree par le pilote (cloture) : " + resume_mission(mission),
        fichiers=fichiers_mission,
        portes=["pilote:fin"],
    )
    # Trace MUETTE (EO-130, friction 69) : la mission est close -- ses fichiers
    # sont-ils DITS ? Une colonne vide se lit "aucun fichier touche". Le constat
    # part au marbre, jamais seulement sur la console (lecon de la friction 68,
    # apprise le meme jour : une alerte qui ne vit que dans un tuyau se perd).
    _code_muet, message_muet = crier_mission_muette(mission, fichiers_mission)
    if message_muet:
        print(message_muet)
    # Rattrapage des fichiers NON TRACES (EO-133, voie b) : la vue ne lit QUE le
    # journal -- tout ce que le DOMICILE porte et que le journal ignore est
    # INVISIBLE (mesure du 2026-09-16 : 12 fichiers pour MO-132 et MO-136, et 576
    # sur le passe, invisibles depuis la naissance de la derivation). Le pilote
    # comble le trou a CHAQUE cloture, et l'appel est place AVANT l'entretien :
    # la vue est regeneree juste apres (entretenir_suivi), donc elle montre le
    # rattrapage qu'elle vient de rendre lisible -- l'ordre inverse aurait laisse
    # un tour de retard, la cecite d'une mission que MO-139 avait deja corrigee.
    _nb_rattrapes, _nb_fichiers_rattrapes, message_rattrapage = rattraper_fichiers_non_traces()
    if message_rattrapage:
        print(message_rattrapage)
    # Entretien de la trace (MO-139) : le super-combo sc-003 fait travailler la
    # coherence file<->journal PUIS regenere la vue, par les portes officielles.
    entretenir_suivi()
    # Famille de CONSERVATION (EO-147, MO-163) : le balayage CLASSE par la regle
    # les points de restauration nes des ecritures de la mission. Place APRES
    # l'entretien de la trace (la vue est deja a jour quand les decisions
    # s'ecrivent) et AVANT la purge, qui est le dernier geste de la cloture.
    _code_balayage, message_balayage = balayer_famille_conservation(mission)
    if message_balayage:
        print(message_balayage)
    # ACTE de la famille (EO-147) : le balayage vient d'ecrire les DECISIONS,
    # le pilote execute donc la ROTATION dans la foulee. Sans ce geste, une
    # famille classee attendrait un `archiver --lot oui` manuel a CHAQUE mission :
    # exactement la discipline d'agent qu'EO-147 ferme (mesure : 88 elements
    # decidas `archiver` en attente). L'ORDRE est celui de la doctrine -- le
    # verdict est trace AVANT que quoi que ce soit bouge (plan-conservation, 5) --
    # et c'est la porte de rotation qui agit, avec ses refus et son manifeste.
    _code_rotation, message_rotation = archiver_famille_conservation(mission)
    if message_rotation:
        print(message_rotation)
    # CONTROLE de la MEME famille (EO-152, MO-165) : les deux gestes ci-dessus
    # MAINTIENNENT la borne N=1 ; ce controle la MESURE. Mesure MO-164 : la case 8
    # (`controler-archives`) reste verte TOUT LE TEMPS -- elle mesure la PERTE,
    # jamais la BORNE -- et 16 points STRUCTUREL en trop dans 10 familles sur 88
    # n'etaient vus par AUCUN instrument. Un controle que personne ne lance ne
    # protege rien : le pilote le lance donc a CHAQUE cloture, APRES l'acte qui
    # doit l'etablir (l'ordre inverse mesurerait un etat que l'acte n'a pas encore
    # produit).
    # L'ECHEC, lui, part AU MARBRE : une alerte rendue seulement sur la console se
    # perd dans le tuyau (lecon de la friction 68, deja appliquee a la trace muette
    # vingt lignes plus haut) et la vue ne lit QUE le journal. Le cri porte la
    # MESURE de la porte, familles en exces comprises.
    _code_borne, message_borne = controler_borne_conservation(mission)
    if message_borne:
        print(crier_borne_rompue(mission, _code_borne, message_borne))
    # Zone jetable (MO-136) : la mission est close, le PILOTE vide la zone et le
    # NOTE au marbre -- le point 4 de perimetre-tmp etait une discipline d'agent,
    # et une discipline qu'aucun instrument ne mesure depend de la memoire.
    _code_purge, message_purge = purger_zone_temporaire(mission)
    print("[PURGE] " + message_purge)
    # Verification post-fin : py_compile + benchmark auto
    code_verif, msgs_verif = verification_post_fin(mission, bilan)
    for msg in msgs_verif:
        print(msg)
    # Nettoyage intercom : purge messages traites
    nettoyer_intercom()
    annoncer_fin(file_missions, mission, portee)
    deposer_message(
        BOITE_MATRICE_IN,
        {
            "type": "fin-mission",
            "date": horodater(),
            "mission": mission["id"],
            "bilan": bilan,
            CHAMP_DEFAUTS_MISSION: defauts,
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

            # MO-175 (3e jambe) : c est ICI que la CHAINE s enchaine -- et qu elle
            # S ARRETE si la mission suivante n est pas auto-validee.
            preparer_injection(charger_file, enchainer=True)
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
        # F3 (2026-09-19, decision createur) : un lot desarme ne doit pas TUER la
        # chaine. Avant, la fin d un lot rendait la main a la Matrice et ne
        # regardait JAMAIS l entonnoir : une tete de brin auto-validee ne pouvait
        # donc etre reprise qu apres une mission HORS lot (chemin rare, verbe
        # `conduire`). Le lot est desormais desarme (ci-dessus) et la chaine
        # REOUVRE sur l entonnoir. Si la tete n est PAS auto-validee, le STOP
        # reste et RIEN n est consomme -- on ne force pas la main, on la donne.
        if not session_en_pause():
            from injection.fonctions import preparer_injection

            print("Fin de lot : la chaine reouvre sur la tete auto-validee du brin...")
            preparer_injection(charger_file, enchainer=True)
        else:
            print("SESSION EN PAUSE (M-080) : aucune relance automatique pendant la maintenance.")
    else:
        from injection.fonctions import preparer_injection

        print("Enchainement automatique de la mission suivante du lot...")
        preparer_injection(charger_file, enchainer=True)
    return 0
