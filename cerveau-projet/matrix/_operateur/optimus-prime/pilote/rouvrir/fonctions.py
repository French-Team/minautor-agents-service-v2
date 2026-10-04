"""Fonctions de la categorie rouvrir : RENDRE A FAIRE une mission close par erreur.

MO-548 / EO-553. Le manque mesure : `fin` clos la mission EN COURS, le bilan est
ecrit, et plus AUCUNE porte ne rend la main. Mesure du 2026-10-02 (MO-547) : la
porte `fin` a clos MO-534 avec le bilan de MO-547. Le bilan faux a ete corrige par
un evenement de suivi, mais le STATUT est reste `terminee` -- donc le controle de
coherence, qui lit la file ET le journal, ne peut pas voir la difference, et une
mission du createur passe pour faite.

CE QUE CE VERBE FAIT, ET CE QU IL NE FAIT PAS. Il remet la mission en
`en-attente` avec son motif, sa date de rouverture et son compteur. Il NE
REECRIT PAS le bilan : le texte fautif est CONSERVE sous `bilan_retire`, avec la
raison du retrait -- la trace porte le retrait, elle n efface rien (lecon L-176).
Il ne touche ni au journal des evenements de fin deja poses, ni au marbre : une
fin honnete reste une fin honnete meme si le bilan, lui, etait faux.

LA DECISION EST PURE (`diagnostiquer`), comme chez `regulariser` : tout lui est
rendu en argument, elle ne lit aucun disque. C est ce qui permet a la non-regression
de la rejouer sur des cas FABRIQUES, sans toucher a une seule trace.

LES REFUS SONT NOMMES ET DIRECTIONNELS : le message dit le remede, rien n est ecrit.

SUR LA QUATRIEME REGLE DE L OBJECTIF. L objectif disait : refuser si un travail
reel existe sur le disque que le motif ne nomme pas. La mission NE PORTE aucun
champ de livrables (les `--fichiers` partent au suivi, pas dans la file), donc une
verification de ce genre ne pourrait rien voir -- un garde qui regarde un champ
inexistant est vert par construction (lecon L-032). Elle est donc remplacee par ce
qui se PEUT verifier : le motif doit NOMMER ce qu il retire, c est a dire l id de
la mission ou l id que le bilan annonce. Un motif qui ne dit pas ce qu il annule
n est pas une trace, c est un geste. Et la porte IMPRIME le bilan et sa date avant
d ecrire, pour que le motif soit ecrit contre des faits et non contre un souvenir.
"""
from commun import (
    charger_file,
    declarer_borne_marbre,
    enregistrer_file,
    horodater,
    journaliser_mission,
)
from constants import STATUT_EN_ATTENTE, STATUT_EN_COURS, STATUT_TERMINEE

# Verdicts de la decision (vocabulaire ferme rendu par `diagnostiquer`).
VERDICT_ROUVERTURE = "ouverture"
VERDICT_MOTIF_MANQUANT = "motif-manquant"
VERDICT_INCONNUE = "inconnue"
VERDICT_DEJA_EN_ATTENTE = "deja-en-attente"
VERDICT_EN_COURS = "en-cours"
VERDICT_DEJA_RETIREE = "bilan-deja-retire"
VERDICT_TRAVAIL_NON_NOMME = "travail-non-nomme"

# Action du MARBRE qui dit l ACTE -- elle doit figurer dans le vocabulaire ferme de
# l outil suivi-optimus (constants.ACTIONS), sinon la porte `noter` REFUSE. Elle a
# SON nom (MO-548) : le premier jet reprenait `intervention`, qui designe
# l intervention du CREATEUR sur la mission EN COURS -- un acte TENU pendant un
# round, pas un changement de statut d une mission CLOSE. Le mot etait faux, la
# trace le repetait, et apres elle ne pouvait plus dire CE QUI avait rouvre la
# mission. Meme lecon, meme forme que `regularisation` (MO-461) : un verbe porte
# le sien.
ACTION_ROUVERTURE = "rouverture"

# Porte citee dans la trace, pour que la vue dise QUEL verbe a agi.
PORTE_ROUVRIR = "pilote:rouvrir"


def _ids_dans(texte):
    """Les identifiants de mission APPARUSENT dans un texte.

    Un id du projet se reconnait a sa FORME : deux lettres, un tiret, des chiffres.
    C est une forme, pas une liste recopiee -- une liste d ids nommerait ceux
    d aujourd hui et tairait ceux de demain (M-076).
    """
    trouves = set()
    for bout in str(texte or "").replace(",", " ").replace(":", " ").split():
        net = bout.strip(".;()[]\"'-!?")
        if (len(net) >= 4 and net[:2].isalpha() and net[2] == "-"
                and net[3:].isdigit()):
            trouves.add(net.upper())
    return trouves


def diagnostiquer(motif, mission):
    """Decision PURE de rouvrir : (code, verdict), sans aucun acces disque.

    (2, motif-manquant)    -- une rouverture sans motif ne se trace pas ;
    (1, inconnue)          -- aucun id de la FILE ACTIVE ne porte ce nom ;
    (1, bilan-deja-retire) -- le bilan a deja ete retire : rien a retirer deux fois ;
    (1, deja-en-attente)   -- elle ne l est plus : rien a rouvrir ;
    (1, en-cours)          -- c est `fin` qui la clos, donc `fin` peut la reprendre ;
    (2, travail-non-nomme) -- le motif ne nomme NI la mission NI l id que le bilan
                             announce : il dit quoi faire, pas ce qu il retire ;
    (0, ouverture)         -- elle est close, son bilan existe et le motif le nomme.

    L ORDRE DE `bilan-deja-retire` EST CELUI DE LA MESURE (MO-548). Il etait
    juge APRES le statut, donc il n etait pas ATTEIGNABLE : une mission rouverte
    porte TOUJOURS `statut = en-attente`, donc `deja-en-attente` parlait avant lui
    et la branche promettait une reponse (nommer le retrait precedent et son
    motif) qu elle ne donnait jamais. La lecon de L-032 a un versant symetrique :
    un garde qui ne peut pas dire NON ne garde rien, et une branche qui ne peut
    pas parler ne protege rien. Elle se juge donc en PREMIER, parce qu elle est la
    plus PRECISE des trois.
    """
    if not str(motif or "").strip():
        return 2, VERDICT_MOTIF_MANQUANT
    if mission is None:
        return 1, VERDICT_INCONNUE
    if mission.get("bilan_retire"):
        return 1, VERDICT_DEJA_RETIREE
    statut = mission.get("statut")
    if statut == STATUT_EN_ATTENTE:
        return 1, VERDICT_DEJA_EN_ATTENTE
    if statut == STATUT_EN_COURS:
        return 1, VERDICT_EN_COURS
    # Le motif doit nommer ce qu il RETIRE : au moins un id presente SOI-meme ou
    # dans son bilan (mesure du 2026-10-02 : le bilan de MO-534 annoncait MO-547).
    # Premier jet de cette regle : les ids du bilan etaient comptes comme NOMMES,
    # donc la branche de refus n etait ATTEIGNABLE PAR AUCUN MOTIF -- un garde qui
    # ne peut pas dire NON ne garde rien (lecon L-032). Ici les deux ensembles
    # restent SEPARES, et l intersection doit etre non vide.
    nommes = _ids_dans(motif)
    disponibles = _ids_dans(mission.get("bilan") or "") | _ids_dans(mission.get("id"))
    if not (nommes & disponibles):
        return 2, VERDICT_TRAVAIL_NON_NOMME
    return 0, VERDICT_ROUVERTURE


def mission_par_id(file_missions, identifiant):
    """La mission de la file ACTIVE portant cet id, ou None (jamais d exception)."""
    for mission in (file_missions or {}).get("missions", []):
        if mission.get("id") == identifiant:
            return mission
    return None


def poser_la_rouverture(mission, motif, date):
    """La mission redevient A FAIRE ; le bilan faux est RETIRE, pas efface.

    PURE au sens de l ecriture : elle rend la mission MUTEE, elle n enregistre
    RIEN (c est `rouvrir_mission` qui enregistre).
    """
    mission["statut"] = STATUT_EN_ATTENTE
    mission["rouverte_le"] = date
    mission["motif_rouverture"] = motif
    mission["compteur_rouvertures"] = int(mission.get("compteur_rouvertures") or 0) + 1
    bilan = mission.get("bilan")
    if bilan:
        # LE RETRAIT EST DIT DANS LE BILAN LUI-MEME : une mission rendue A FAIRE
        # avec un bilan d autrui sous les yeux se ferait relire comme sien.
        mission["bilan_retire"] = {
            "date": date,
            "motif": motif,
            "texte": bilan,
        }
        mission["bilan"] = (
            "BILAN " + str(mission.get("id", "")) + " -- RETIRE LE " + date + "\n\n"
            + "Ce bilan ne vaut pas pour cette mission ; il a ete retire par la porte"
            " `rouvrir`.\nMotif du retrait : " + motif
            + "\nTexte retire, conserve :\n" + bilan
        )
        mission["bilan_retire_le"] = date
    return mission


def rouvrir_mission(charger_file, identifiant, motif):
    """PORTE : rendre A FAIRE une mission close dont le bilan ne vaut pas pour elle.

    Les refus sont NOMMES et DIRECTIONNELS. L ACTE ecrit la FILE, note l ACTE sous
    l action qui lui appartient et journalise une ligne dediee.
    """
    file_missions = charger_file()
    mission = mission_par_id(file_missions, identifiant)
    code, verdict = diagnostiquer(motif, mission)

    if verdict == VERDICT_MOTIF_MANQUANT:
        print('REFUS : le motif est OBLIGATOIRE (--motif "...") -- une rouverture'
              " se TRACE, jamais muette.")
        return code
    if verdict == VERDICT_INCONNUE:
        print("REFUS : " + identifiant + " est INCONNUE de la file ACTIVE -- une"
              " rouverture rend A FAIRE une mission EXISTANTE, elle n en invente pas.")
        print("  Remede : une mission CLOSE puis sortie de la file est dans"
              " l archive ; celle-ci ne se rouvre pas (une archive est une archive).")
        return code
    if verdict == VERDICT_DEJA_EN_ATTENTE:
        print("REFUS : " + identifiant + " est deja en-attente dans la file -- rien a"
              " rouvrir, rien n est ecrit.")
        return code
    if verdict == VERDICT_EN_COURS:
        print("REFUS : " + identifiant + " est la mission EN COURS -- c est `fin` qui"
              " la clos, et elle sera conduite jusqu au bout.")
        return code
    if verdict == VERDICT_DEJA_RETIREE:
        print("REFUS : le bilan de " + identifiant + " a DEJA ete retire le "
              + str(mission.get("bilan_retire_le")) + " -- on ne retire pas deux fois.")
        print("  Motif du retrait precedent : " + str((mission.get("bilan_retire")
                                                        or {}).get("motif", ""))[:120])
        return code
    if verdict == VERDICT_TRAVAIL_NON_NOMME:
        print("REFUS : le motif ne nomme NI " + identifiant + " NI l id que son bilan"
              " annonce -- un motif doit dire CE QU IL RETIRE, pas seulement qu il"
              " agit.")
        return code

    # Les faits, AVANT l ecriture : une trace ecrite contre un souvenir n est pas
    # une trace, c est une intention. La porte DIT donc ce qu elle va retirer.
    print("Ce que la trace va retirer :")
    print("  mission : " + identifiant + " (" + str(mission.get("theme", "")) + ")")
    print("  terminee_le : " + str(mission.get("terminee_le", "inconnu")))
    print("  premiere ligne du bilan : "
          + (str(mission.get("bilan", "")).splitlines() or ["(vide)"])[0][:160])

    date = horodater()
    poser_la_rouverture(mission, motif, date)
    enregistrer_file(file_missions)
    # L ACTE : une action a LUI, jamais une seconde `fin` -- la fin honnete au
    # journal reste vraie, c est le BILAN qui ne valait pas.
    declarer_borne_marbre(
        mission,
        ACTION_ROUVERTURE,
        "mission rouverte : " + motif,
        portes=[PORTE_ROUVRIR],
    )
    journaliser_mission(
        {
            "type": "mission-rouverte",
            "date": date,
            "id": identifiant,
            "theme": mission.get("theme", ""),
            "motif": motif,
            "detail": ("mission " + identifiant + " ROUVRTE (rendue A FAIRE) : "
                       + motif + " -- le bilan fautif est RETIRE et conserve, jamais"
                       " efface"),
        }
    )
    print("Mission " + identifiant + " ROUVRTE : rendue A FAIRE, motif trace.")
    print("  Le bilan fautif est RETIRE et CONSERVE dans la mission (bilan_retire) :"
          " la trace porte le retrait, elle n efface rien.")
    return 0
