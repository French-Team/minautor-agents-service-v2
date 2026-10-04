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
    controler_archives_conservation,
    controler_borne_conservation,
    controler_plafond_conservation,
    controler_raisonnement_mission,
    crier_controle_conservation,
    crier_mission_muette,
    derniere_injection,
    deposer_message,
    deposer_segments_raisonnement,
    declarer_borne_marbre,
    declarer_disparitions_conservation,
    enregistrer_file,
    entretenir_suivi,
    fichiers_de_la_mission,
    horodater,
    ids_en_lot,
    journaliser_mission,
    lot_termine,
    mission_en_cours,
    portee_lot,
    promouvoir_les_suivants,
    nettoyer_intercom,
    noter_prise_round,
    noter_session,
    purger_archives_conservation,
    purger_archives_journaux,
    purger_zone_temporaire,
    rappel_round_servi_non_conduit,
    rattraper_fichiers_non_traces,
    refus_bilan_etranger,
    refus_cloture_fausse,
    rotation_boites_intercom,
    resume_mission,
    session_en_pause,
    verification_post_fin,
    verifier_serie_stricte,
)
from constants import (
    BOITE_MATRICE_IN,
    BOITE_PILOTE_OUT,
    CHAMP_AUTO_VALIDATION,
    CHAMP_DEFAUTS_MISSION,
    STATUT_DEFAUT_REPARE,
    STATUT_TERMINEE,
)

# --- LE PROCESSUS [question] FINIT PAR UNE MISSION (MO-553) ---------------------
# Le crochet `[question]` route vers le verbe `lot` avec le type `question`
# (filtrer/entry.py). Les 4 parts de la convention des crochets sont 4 missions
# (ANALYSTEUR, RECHERCHEUR, CONTRE-ANALYSE, RAPPORTEUR). Apres la derniere, la
# chaine n emporte rien : le mis en cause que la contre-analyse a designe ne
# donne jamais lieu a une mission. Les themes `AUTO-CORRECTION` et
# `AUTO-EVOLUTION` existent, ils ne sont pas branches.
#
# Le mis en cause n est pas DEVINE : il est NOMME par le bilan, qui porte une
# ligne `MIS EN CAUSE : <texte>`. Decision du createur : la mission nait
# TOUJOURS (meme si le verdict est "rien"), et UNE SEULE mission porte a la fois
# la correction et l evolution.
MARQUEUR_MIS_EN_CAUSE = "MIS EN CAUSE"
TYPE_QUESTION = "question"
TYPE_ITEM_CORRECTION = "reparation"
SOURCE_ITEM_CORRECTION = "audit-nemesis"


def mis_en_cause_du_bilan(bilan):
    """Le texte du `MIS EN CAUSE` d un bilan, ou None s il n y en a pas.

    Fonction PURE : elle lit un texte et rend une reponse, elle ne touche ni au
    disque ni a l horloge. Une regle qu on ne peut pas appeler ne peut pas etre
    eprouvee par le jeu.

    La lecture est TOLERANTE sur la forme (marqueur seul, deux-points espace ou
    non) et STRICTE sur le fond : un marqueur vide ne vaut pas un mis en cause,
    il rend None comme s il n y en avait pas.

    Le decoupage se fait au PREMIER deux-points, pas par prefixe : c est la meme
    grammaire et cela evite la FORME `splitlines()` + `startswith(...)`, que le
    garde `verifier-extraction-ecarts` lit comme une extraction de sortie
    (accusation du 2026-10-03). Ici on ne filtre aucune ligne IMPRIMEE : on
    cherche un libelle dans un texte, la distinction n est pas cosmetique.
    """
    for ligne in str(bilan or "").splitlines():
        libelle, sep, suite = ligne.partition(":")
        if not sep:
            continue
        if libelle.strip().upper() != MARQUEUR_MIS_EN_CAUSE:
            continue
        suite = suite.strip()
        if suite:
            return suite
    return None


def fin_du_processus_question(file_missions, mission):
    """Vrai si cette mission TERMINE un processus [question].

    Le processus, c'est la QUESTION -- pas le lot. Une question chargee
    individuellement est donc sa propre fin. Dans un lot, c'est la DERNIERE part
    de la liste : les parts deja terminees restent dans le lot, seule compte
    celle qui vient APRES (mesure du cobaye du 2026-10-03 : la premiere version
    comparait la liste entiere, donc les trois premieres parts se croyaient
    chacune en fin de processus, et le processus aurait produit quatre
    missions au lieu d une).
    """
    if str(mission.get("type", "")).strip().lower() != TYPE_QUESTION:
        return False
    identifiant = str(mission.get("id", ""))
    ids = [str(i) for i in ids_en_lot(file_missions)]
    if identifiant not in ids:
        return True
    return not ids[ids.index(identifiant) + 1:]


def afficher_champ(nom, valeur):
    """Affiche UN champ de l injection, quel que soit son TYPE (MO-394, EO-381).

    Un champ ABSENT se DIT (L-055) ; une liste se lit en puces ; un objet se lit en
    cles et valeurs ; un texte se lit tel quel. C est la FORME qui s adapte au champ,
    jamais le champ qui disparait par accident de forme.
    """
    etiquette = str(nom).upper()
    if valeur is None or valeur == "" or valeur == [] or valeur == {}:
        print(etiquette + " : ABSENT (la porte ne l a pas depose -- le DIT, L-055)")
        return
    if isinstance(valeur, dict):
        print(etiquette + " (" + str(len(valeur)) + " cle(s))")
        for cle in valeur:
            print("  " + str(cle) + " : " + str(valeur[cle]))
        return
    if isinstance(valeur, (list, tuple)):
        print(etiquette + " (" + str(len(valeur)) + ")")
        for element in valeur:
            print("  - " + str(element))
        return
    print(etiquette)
    print("  " + str(valeur).strip())


def remettre_les_ordres(charger_file, complet=False):
    """IMPRIME les ordres du round servi (EO-370) : ils etaient dans un FICHIER.

    OU CA MERDAIT (mesure du 2026-09-22, demande du createur : < tu dois comprendre ou
    ca merde >). `injection.preparer_injection` DEPOSE l'injection complete (objectif,
    checklist, role, lecons, rappel) dans la boite de sortie et n'imprime sur la
    console que le CHEMIN du fichier. Entre deux rounds, l'agent recevait donc un
    IDENTIFIANT, pas une CONSIGNE -- et le seul geste qui LISAIT une injection etait
    l ORDRE 2, un ordre de DEMARRAGE. Pour savoir quoi faire, il fallait ouvrir la
    boite a la main : c'est LA que le round s'arrete. Un agent sans ordres en main
    raconte ou il demande, il ne continue pas.

    Ici, ce qui a ete DEPOSE est AUSSI IMPRIME : un seul contenu, deux lecteurs.

    MO-394 (EO-381, mesure de l audit MO-365) : cette porte imprimait QUATRE champs sur
    les NEUF peses -- recherche, modes_emploi, role, profil, themes_utiles, lecons_utiles
    et auto_validation etaient fabriques, peses et JAMAIS remis (mesure : 30 injections
    sur 30 portaient recherche et modes_emploi, aucune ne les remettait). Elle remet
    desormais TOUS les CHAMPS_PESES, et la remise a UN SEUL chemin d APPEL : la porte
    preparer_injection -- donc la cloture, les verbes `injecter` et `conduire`. La cloture
    n a plus d appel propre : deux appels imprimeraient DEUX FOIS les memes ordres.

    MO-471 (decisions D2/D3, 2026-09-26) : la remise par DEFAUT est desormais la FICHE
    TECHNIQUE DE TRAVAIL -- BORNEE (noyau dit EN ENTIER, ajustables resumes). MO-394
    avait lui-meme DIT la limite : < la remise deverse l injection ENTIERE, 41 K
    caracteres ; une remise plus etroite est une DECISION >. Le chemin LONG reste
    disponible (complet=True) et l injection ENTIERE reste joignable a sa porte
    (`pilote ordres --id <id> --complet`) : la fiche RESUME, elle ne REMPLACE pas.
    """
    mission = mission_en_cours(charger_file() or {})
    if not mission:
        return
    # MO-451 (retour createur 2026-09-24) : LE RAPPEL IMMEDIAT du round SERVI et
    # JAMAIS CONDUIT. Le FAIT n attend AUCUN seuil : des que la prise est le dernier
    # acte du round, il est connu (domicile partage data/commun/round_servi.py). Le
    # suivi du pilote le crie APRES son seuil ; ici on le DIT tout de suite, dans la
    # remise des ordres -- au demarrage, c est ce que l agent lit en premier.
    rappel = rappel_round_servi_non_conduit(charger_file)
    if rappel:
        print("=" * 60)
        print(rappel)
        print("=" * 60)
    identifiant = str(mission.get("id", ""))
    injection = derniere_injection(identifiant)
    if not injection:
        print("TES ORDRES : injection INTROUVABLE pour " + identifiant + " -- la porte ne"
              " l'a pas retrouvee dans " + str(BOITE_PILOTE_OUT) + " (le DIT, jamais le taire).")
        return
    print("=" * 60)
    print("TES ORDRES POUR CE ROUND : " + identifiant
          + " (" + str(injection.get("theme", "")) + ")")
    print("=" * 60)
    # MO-471 (D2/D3) : par DEFAUT, la remise est la FICHE TECHNIQUE DE TRAVAIL -- bornee,
    # noyau dit EN ENTIER, ajustables resumes. Le chemin LONG (complet=True) imprime TOUS
    # les CHAMPS_PESES (contrat MO-394) et reste joignable par `pilote ordres --complet`.
    from injection.fonctions import (fiche_technique, poids_fiche, CHAMPS_PESES,
                                     PLAFOND_LEGONS_TOKENS, PLAFOND_REMISE_TOKENS)
    if complet:
        print("OBJECTIF")
        print("  " + str(injection.get("objectif", "") or "").strip())
        for champ in CHAMPS_PESES:
            if champ != "objectif":
                afficher_champ(champ, injection.get(champ))
        afficher_champ(CHAMP_AUTO_VALIDATION, injection.get(CHAMP_AUTO_VALIDATION))
        poids = injection.get("poids_tokens")
        if poids:
            print("POIDS DE L INJECTION : " + str(poids) + " tokens declares"
                  " (plafond des lecons : " + str(PLAFOND_LEGONS_TOKENS) + ")")
    else:
        for ligne in fiche_technique(injection):
            print(ligne)
        # MO-473 : le PLAFOND DE REMISE est DECLARE et RESPECTE. Un depassement se DIT
        # (jamais un tronquage muet : le NOYAU est ce qui DECIDE, on ne le coupe pas en
        # silence) et nomme le chemin LONG.
        mesure = poids_fiche(injection)
        if mesure > PLAFOND_REMISE_TOKENS:
            print("REMISE : fiche de " + str(mesure) + " tokens, AU-DELA du plafond de"
                  " remise " + str(PLAFOND_REMISE_TOKENS) + " -- lis l injection ENTIERE :"
                  " pilote ordres --id " + identifiant + " --complet")
    print("=" * 60)


def enchainer_et_prendre(charger_file):
    """SERT la suite de la chaine, PUIS PREND le round servi (EO-367, 2026-09-22).

    DEMANDE DU CREATEUR : < c est le PILOTE qui doit te faire continuer les rounds >.
    POURQUOI ICI, ET PAS DANS LA DOCTRINE : la doctrine ECRIT la boucle, elle ne
    l EXECUTE pas. Le seul endroit qui SAIT qu un round vient d etre servi est la
    CLOTURE elle-meme : c est donc elle qui PREND. La prise cesse d etre un geste de
    l agent -- un geste qu on n a pas a faire ne s oublie pas.

    La prise n est notee QUE si un round a REELLEMENT ete servi : la chaine peut
    S ARRETER (mission suivante non auto-validee, lot termine sans tete de brin,
    session en pause) -- on ne prend pas un round qui n existe pas, et on ne prend
    pas celui qu on vient de CLORE.
    """
    from injection.fonctions import preparer_injection

    preparer_injection(charger_file, enchainer=True)
    if not mission_en_cours(charger_file() or {}):
        return
    noter_prise_round(charger_file, par_la_cloture=True)
    # EO-370 + MO-394 (EO-381) : le round arrive SERVI, PRIS, ET AVEC TOUS SES ORDRES
    # IMPRIMES. La remise n est plus appelee ici : elle a UN domicile et elle est
    # desormais declenchee par preparer_injection, donc l appeler aussi ici
    # imprimerait DEUX FOIS les memes ordres.


def args_item_correction(mission, mis_en_cause):
    """Les arguments du depot de l entonnoir, pour le mis en cause d une [question].

    Fonction PURE : elle rend la liste d arguments, elle n ecrit rien. La forme
    du depot est donc eprouvable par le jeu, et la cloture n a plus qu a la
   .play() -- un seul chemin d ecriture, celui de la porte.
    """
    identifiant = str(mission.get("id", ""))
    theme = ("Correction et evolution -- mis en cause : " + str(mis_en_cause))[:180]
    objectif = (
        "Mission de CORRECTION et d EVOLUTION, issue du processus [question] "
        "cloture en " + identifiant + " (theme " + str(mission.get("theme", "")) + ").\n"
        "MIS EN CAUSE : " + str(mis_en_cause) + "\n\n"
        "Une seule mission porte les deux volets, comme decide : le CORRIGER d abord "
        "(le defaut nomme ci-dessus), puis faire EVOLUER le processus pour qu il ne se "
        "reproduise pas. Le bilan complet de la question est dans la mission citee "
        "ci-dessus.")
    return [
        "--theme", theme,
        "--objectif", objectif,
        "--type", TYPE_ITEM_CORRECTION,
        "--source", SOURCE_ITEM_CORRECTION,
        "--urgence", "normale",
        "--trace", ("Processus [question] cloture en " + identifiant
                    + " : fin de processus, mission de correction et d evolution "
                    "deposee automatiquement (MO-553)."),
    ]


def decision_fin_question(file_missions, mission, bilan):
    """(code, message, args) : ce que la FIN d une [question] doit faire.

    DECISION PURE : elle lit la file et le bilan, elle n ecrit rien et ne lit
    aucun disque. C est elle qui est eprouvee par le jeu ; la cloture ne fait
    qu appliquer son verdict.

      (0, "", None)      la regle ne parle pas a cette mission ;
      (1, REFUS, None)   la [question] se termine sans avoir dit son mis en cause ;
      (0, "", args)      il faut deposer la mission de correction et d evolution.
    """
    if not fin_du_processus_question(file_missions, mission):
        return 0, "", None
    mis_en_cause = mis_en_cause_du_bilan(bilan)
    if not mis_en_cause:
        return 1, ("REFUS : cette mission TERMINE un processus [question] et son bilan\n"
                   "  ne nomme pas le mis en cause. Une question qui ne dit pas ce qu elle\n"
                   "  a mis en cause ne peut pas se cloturer (MO-553).\n"
                   "  Remede : ajouter au bilan une ligne\n"
                   "    " + MARQUEUR_MIS_EN_CAUSE + " : <ce que l analyse et la contre-analyse ont mis en cause>\n"
                   "  Le verdict peut etre 'rien' : la mission nait quand meme et le dit."), None
    return 0, "", args_item_correction(mission, mis_en_cause)


def cloturer_mission(charger_file, bilan, defauts=None, segments=None):
    """CLOTURE la mission en cours, puis, si un lot est arme :
    - annonce la FIN (k/n),
    - enchaine AUTOMATIQUEMENT la mission suivante du lot (DEBUT k+1/n),
    - au terme du lot : RETOUR consolide a la Matrice (bilan du lot entier).
    Les DEFAUTS d'outil rencontres en travaillant (R5, audit MO-174) VOYAGENT
    avec la mission -- fichier, journal, retour Matrice. Un defaut NON REPARE est
    un POINT OUVERT : il est CRIE, jamais une note de bas de page.
    LES SEGMENTS DE RAISONNEMENT (MO-500, option C de l audit MO-499) : la cloture
    DEMANDE si ce round en a produit un -- elle le DEPOSE (source = cette mission),
    ou elle le DIT (le constat part au marbre, jamais un silence).
    """
    defauts = defauts or []
    segments = segments or []
    file_missions = charger_file()
    mission = mission_en_cours(file_missions)
    if mission is None:
        print("REFUS : aucune mission en cours a cloturer.")
        return 1

    # CLOTURE FAUSSE (MO-426) : refus NOMME quand cette cloture nommerait une AUTRE
    # mission que celle reellement ouverte (charge INDIVIDUELLE jamais conduite).
    # Le jugement vit au domicile PARTAGE (data/commun/cloture_fausse.py) : le suivi
    # du pilote diagnostique avec la MEME regle. Pose AVANT toute mutation de la file.
    refus_marbre = refus_cloture_fausse(file_missions, mission)
    if refus_marbre:
        print(refus_marbre)
        return 1

    # CLOTURE FAUSSE DE ROUND (EO-455, MO-480) : deuxieme famille -- le TITRE du bilan
    # declare la mission close. Le JOURNAL ne peut pas la voir (la fin nomme bien la
    # mission close) : mesure du 2026-09-27, MO-440 close avec le bilan de MO-463.
    # Meme domicile partage (data/commun/cloture_fausse.py, M-076). Pose AVANT toute
    # mutation de la file, comme le refus de cloture fausse.
    refus_bilan = refus_bilan_etranger(mission, bilan)
    if refus_bilan:
        print(refus_bilan)
        return 1

    # LA DEMANDE DE SEGMENT DE RAISONNEMENT (MO-500, option C de l audit MO-499 /
    # EO-477) : la cloture DEMANDE si ce round a produit un segment. OUI -> elle le
    # DEPOSE (par la porte de l outil, source = CETTE mission) ; NON -> elle le DIT.
    # Le DEPOT est place AVANT toute mutation, comme les deux refus ci-dessus : un
    # segment declare qui ne rentre pas REFUSE la cloture, donc il ne peut pas se
    # perdre dans un round clos. La MESURE suit immediatement, et le constat part AU
    # MARBRE (controler_raisonnement_mission) : le silence est impossible -- c est CE
    # fait qui rend l option C mesurable (compter les rounds qui deposent et ceux qui
    # declarent n avoir rien produit).
    code_depot, message_depot = deposer_segments_raisonnement(mission, segments)
    if code_depot != 0:
        print("REFUS : " + message_depot)
        return 1
    if message_depot:
        print(message_depot)
    _code_raisonnement, message_raisonnement = controler_raisonnement_mission(mission)
    if message_raisonnement:
        print(message_raisonnement)

    # LA FIN D UN PROCESSUS [question] (MO-553) : une question qui ne dit pas ce
    # qu elle a mis en cause ne peut pas se terminer -- et une question qui le
    # dit NE PEUT PAS finir sans avoir depose la mission de correction et
    # d evolution. Posee AVANT toute mutation de la file, comme les refus
    # ci-dessus : une regle qui s applique apres l ecriture constate l ecart trop
    # tard. Le depot passe par `vrac/entry.py::executer`, la fonction que la
    # PORTE appelle : un seul chemin d ecriture, pas une deuxieme main.
    if fin_du_processus_question(file_missions, mission):
        from entonnoir.vrac import entry as vrac_entry
        code_question, message_question, args_question = decision_fin_question(
            file_missions, mission, bilan)
        if code_question != 0:
            print(message_question)
            return code_question
        code_item = vrac_entry.executer(args_question)
        if code_item != 0:
            print("REFUS : la mission de correction n a pas pu etre deposee (code "
                  + str(code_item) + ") -- la cloture de " + str(mission.get("id", ""))
                  + " est suspendue plutot que d etre muette.")
            return code_item
        print("PROCESSUS [question] TERMINE : la mission de correction et d evolution")
        print("  du mis en cause est deposee dans l entonnoir (voir l item cree ci-dessus).")

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
    # L ACTE de PURGE de la MEME famille (P3, MO-308) : la rotation vient de
    # deposer les points ages dans l archive ; sans ce geste l archive regrossirait
    # sans fin et le cycle repartirait -- le defaut que V2 de la revision nomme
    # ("un mecanisme dont l acte est manuel n est pas une politique"). La porte TRI :
    # elle ne supprime que ce qu elle peut PROUVER recouvrable, et refuse le reste.
    _code_purge_archives, message_purge_archives = purger_archives_conservation(mission)
    if message_purge_archives:
        print(message_purge_archives)
    # LES ARCHIVES DATEES DES JOURNAUX ET DES BOITES (regle createur, 2026-09-20) :
    # la purge ci-dessus ne traite QUE la famille du registre -- les archives de la
    # rotation des journaux n avaient AUCUNE porte, et 116 Mo vivaient sans duree de
    # vie (dont 90,6 Mo pour la seule archive de l espion-integrite). Meme doctrine,
    # meme porte de preuve : le balayage reconnait la CONVENTION de nom de la
    # rotation et ne supprime QUE ce dont le contenu VIT dans un blob engage. Ce qui
    # n est pas engage RESTE (et c est heureux : l archive que la rotation vient
    # d ecrire porte la memoire de dedoublonnage de son propre lot).
    _code_purge_journaux, message_purge_journaux = purger_archives_journaux(mission)
    if message_purge_journaux:
        print(crier_controle_conservation(mission, _code_purge_journaux,
                                          message_purge_journaux))
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
        print(crier_controle_conservation(mission, _code_borne, message_borne))
    # LE PLAFOND des ACTES EN ATTENTE (P4, MO-309) : la masse se borne, elle ne se
    # raconte pas. Meme doctrine que la borne -- le controle est lance a CHAQUE
    # cloture, APRES l acte qui doit vider l attente, et son echec part au marbre
    # par le meme canal (une alerte qui ne vit que sur la console se perd).
    _code_plafond, message_plafond = controler_plafond_conservation(mission)
    if message_plafond:
        print(crier_controle_conservation(mission, _code_plafond, message_plafond))
    # Zone jetable (MO-136) : la mission est close, le PILOTE vide la zone et le
    # NOTE au marbre -- le point 4 de perimetre-tmp etait une discipline d'agent,
    # et une discipline qu'aucun instrument ne mesure depend de la memoire.
    _code_purge, message_purge = purger_zone_temporaire(mission)
    print("[PURGE] " + message_purge)
    # LES DISPARITIONS QUE LA PURGE VIENT DE CAUSER (V5, MO-304) : la purge
    # ci-dessus retire des fichiers dont certains portaient un point de
    # restauration ENREGISTRE (tout ce qu'une mission a ecrit dans la zone
    # jetable en a cree un). Le registre les gardait non-archives et
    # `controler-archives` les comptait en ECART, sans que rien ne les solde :
    # mesure du 2026-09-20, 7 points et 8 ecarts, alors que 17 du meme genre
    # avaient deja ete declares A LA MAIN a EO-276 -- le stock se reconstituait
    # tout seul a chaque round. Le pilote DECLARE donc ce qu'il vient de faire,
    # par la PORTE qui existe pour cela, et APRES la purge : une declaration
    # porte sur un FAIT (la porte refuse un point encore PRESENT sur le disque).
    _code_disparition, message_disparition = declarer_disparitions_conservation(mission)
    if message_disparition:
        print(crier_controle_conservation(mission, _code_disparition, message_disparition))
    # LE GARDE DE LA PERTE (case 8, MO-304) : la borne mesure l'EXCES et le plafond
    # la MASSE ; celui-ci mesure la PERTE (`archive + actif + disparu + purge =
    # origine`). PERSONNE ne le jouait -- la cloture lancait les deux autres,
    # jamais lui -- donc 8 ecarts vivaient sans qu'aucun instrument ne les voie.
    # Meme doctrine que la borne (MO-165) et le plafond (MO-309) : lance a CHAQUE
    # cloture, APRES les gestes qui doivent le satisfaire, et son echec part AU
    # MARBRE par le meme canal.
    _code_perte, message_perte = controler_archives_conservation(mission)
    if message_perte:
        print(crier_controle_conservation(mission, _code_perte, message_perte))
    # Verification post-fin : py_compile + benchmark auto
    code_verif, msgs_verif = verification_post_fin(mission, bilan)
    for msg in msgs_verif:
        print(msg)
    # Nettoyage intercom : purge messages traites
    nettoyer_intercom()
    # LES BOITES INTERCOM SE BORNENT (demande createur, 2026-09-20) : une boite est
    # en AJOUT SEUL, donc elle ne grandit que par ABSENCE d acte -- mesure du jour :
    # l outbox du pilote portait 17,5 Mo et 708 messages (24,7 Ko par message) pour
    # un plafond de 5 Mo, et RIEN ne mesurait sa TAILLE (le cockpit n en comptait que
    # les lignes). Le pilote la borne ici, par le MOTEUR PARTAGE des journaux, et il
    # MESURE ce qu il fait (l acte est note au marbre). Place APRES l entretien de la
    # boite (les messages traites sont partis) et AVANT le depot de la fin de mission :
    # la ligne qu on vient d ecrire n est jamais la premiere candidate au depart.
    _code_boites, message_boites = rotation_boites_intercom(mission)
    if message_boites:
        print(crier_controle_conservation(mission, _code_boites, message_boites))
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

    # PROMOTION AUTOMATIQUE (EO-457, decision du createur) : la mission vient d etre
    # CLOSE -- c est la < position suivant la mission en cours >. Les items du brin
    # STRICTEMENT plus importants qu elle, et les suivants a reclasser, sont
    # ordonnes MAINTENANT, AVANT de servir le round suivant. La mission close n est
    # jamais rouverte : seule la SUITE change d ordre (serie stricte respectee).
    promouvoir_les_suivants(file_missions, mission)

    # Chaine du lot : la suivante, ou le RETOUR consolide.
    # Garde 1 : seule une mission DU LOT declenche la logique de lot
    # (la fin d'une mission hors lot ne rejoue jamais un RETOUR passe).
    ids_lot = ids_en_lot(file_missions)
    if mission["id"] not in ids_lot:
        # E-008 : fin HORS lot -> la boucle ne meurt jamais. La mission
        # suivante (file ou tresse) est relancee automatiquement.
        # M-080 : JAMAIS pendant une pause (gardes dans preparer_injection).
        if not session_en_pause():
            # MO-175 (3e jambe) : c est ICI que la CHAINE s enchaine -- et qu elle
            # S ARRETE si la mission suivante n est pas auto-validee.
            # EO-367 : enchainer, c est aussi PRENDRE (le pilote fait la boucle).
            enchainer_et_prendre(charger_file)
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
            print("Fin de lot : la chaine reouvre sur la tete auto-validee du brin...")
            enchainer_et_prendre(charger_file)
        else:
            print("SESSION EN PAUSE (M-080) : aucune relance automatique pendant la maintenance.")
    else:
        print("Enchainement automatique de la mission suivante du lot...")
        enchainer_et_prendre(charger_file)
    return 0
