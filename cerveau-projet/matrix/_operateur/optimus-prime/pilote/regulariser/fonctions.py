"""Fonctions simples de la categorie regulariser : une seule tache chacune.

MO-461 / EO-433. Une FIN declaree au JOURNAL pour une mission que la FILE dit
encore < en-attente > ne pouvait etre fermee par AUCUNE porte du pilote :
`enregistrer` REFUSE un id deja present dans la file (mesure : < REFUS : MO-412
est deja dans la file (statut : en-attente) >) et `fin` ne close que la mission
EN COURS. Le controle de coherence (suivi-optimus coherence) rendait donc DEUX
ecarts que RIEN ne pouvait faire tomber : la file et le journal restaient
divergents POUR TOUJOURS (mesure du 2026-09-25 : MO-412 close au journal a
08:53:31 par une note de regularisation, restee < en-attente > dans la file).

LA REGLE : une REGULARISATION n est PAS une cloture. Elle ne FAIT pas la fin --
elle la CONSTATE. La fin doit DEJA vivre au journal ; sans elle, la porte REFUSE.
C est ce qui laisse le controle MORDRE : une mission < terminee > dans la file
SANS fin au journal reste accusee, et cette porte n a pas le pouvoir de l excuser
en inventant une borne (c est le contre-temoin de l epreuve).

CE QUI EST ECRIT, ET CE QUI NE L EST PAS :
  - la FILE : statut terminee + terminee_le + regularisee_le + le motif ;
  - le MARBRE : la borne de fin est declaree IDEMPOTENTE (si_absent) -- une fin
    deja posee n est JAMAIS doublee (meme garde que la cloture, MO-108) ; l ACTE
    y est note sous une action a LUI (`regularisation`), jamais un second `fin` ;
  - le JOURNAL DES MISSIONS : une ligne `mission-regularisee` (meme pratique que
    le verbe `reporter`, qui y depose `mission-reportee`).
Un motif est OBLIGATOIRE : une regularisation se TRACE, jamais muette.

Le vocabulaire d ACTION appartient a suivi-optimus (constants.ACTIONS, qui REFUSE
une action inconnue) : comme `reporter` le fait deja pour `report`, on passe ici
le LITTERAL plutot que d ouvrir un 2e domicile de constantes.
"""
from commun import (
    declarer_borne_marbre,
    enregistrer_file,
    horodater,
    journaliser_mission,
    lire_evenements_marbre,
)
from constants import STATUT_EN_COURS, STATUT_TERMINEE

# Verdicts de la decision (vocabulaire ferme rendu par `diagnostiquer`).
VERDICT_REGULARISATION = "regularisation"
VERDICT_MOTIF_MANQUANT = "motif-manquant"
VERDICT_INCONNUE = "inconnue"
VERDICT_DEJA_TERMINEE = "deja-terminee"
VERDICT_EN_COURS = "en-cours"
VERDICT_SANS_FIN = "sans-fin-au-journal"

# Action du MARBRE qui dit l ACTE -- elle doit figurer dans le vocabulaire ferme
# de l outil suivi-optimus (constants.ACTIONS), sinon la porte `noter` REFUSE.
ACTION_REGULARISATION = "regularisation"

# Porte citee dans la trace, pour que la vue dise QUEL verbe a agi.
PORTE_REGULARISER = "pilote:regulariser"


def diagnostiquer(motif, mission, fin_au_journal):
    """Decision PURE de regulariser : (code, verdict), sans aucun acces disque.

    (2, motif-manquant)      -- une regularisation sans motif ne se trace pas ;
    (1, inconnue)            -- aucun id de la FILE ACTIVE ne porte ce nom ;
    (1, deja-terminee)       -- la file dit DEJA terminee : rien a regulariser ;
    (1, en-cours)            -- c est `fin` qui clore le round OUVERT, pas ici ;
    (1, sans-fin-au-journal) -- la fin N EXISTE PAS : la porte ne l INVENTE pas
                                (l ecart doit RESTER accuse, contre-temoin) ;
    (0, regularisation)      -- la fin VIT au journal, la file ne la dit pas.

    La DECISION est PURE (tout lui est rendu en arguments) : l epreuve permanente
    (maillon 57 de la non-regression) la rejoue sans toucher a aucune trace.
    """
    if not (motif or "").strip():
        return 2, VERDICT_MOTIF_MANQUANT
    if mission is None:
        return 1, VERDICT_INCONNUE
    statut = mission.get("statut")
    if statut == STATUT_TERMINEE:
        return 1, VERDICT_DEJA_TERMINEE
    if statut == STATUT_EN_COURS:
        return 1, VERDICT_EN_COURS
    if not fin_au_journal:
        return 1, VERDICT_SANS_FIN
    return 0, VERDICT_REGULARISATION


def mission_par_id(file_missions, identifiant):
    """La mission de la file ACTIVE portant cet id, ou None (jamais d exception)."""
    for mission in (file_missions or {}).get("missions", []):
        if mission.get("id") == identifiant:
            return mission
    return None


def porte_la_fin(evenements, identifiant):
    """Vrai si le JOURNAL porte DEJA une fin pour cette mission -- la SEULE preuve.

    Un journal ILLISIBLE (None) ne prouve RIEN : la porte refuse alors de
    regulariser, elle ne devine pas ce qu elle ne peut pas lire (L-055).
    """
    if evenements is None:
        return False
    return any(evenement.get("action") == "fin"
               and evenement.get("mission") == identifiant
               for evenement in evenements)


def poser_la_regularisation(mission, motif, date, identifiant):
    """La FILE dit desormais ce que le JOURNAL savait deja -- sans rien inventer.

    PURE au sens de l ecriture : elle rend la mission MUTEE, elle n enregistre
    RIEN (c est `regulariser_mission` qui enregistre). C est ce qui rend l ACTE
    eprouvable en memoire (L-032), comme le saut de lot du maillon 46.
    Le `bilan` n est pose QUE s il MANQUE : une regularisation ne REEcrit pas un
    recit deja ecrit. Son titre suit la forme que le refus de bilan etranger sait
    lire (`BILAN <id>`, data/commun/cloture_fausse.py).
    """
    mission["statut"] = STATUT_TERMINEE
    mission["terminee_le"] = date
    mission["regularisee_le"] = date
    mission["motif_regularisation"] = motif
    if not mission.get("bilan"):
        mission["bilan"] = (
            "BILAN " + identifiant + " -- REGULARISATION DE LA FILE" + "\n" + "\n"
            + "La fin de cette mission vivait DEJA au journal (declaree hors file) :"
            + " le pilote ne l a pas FAITE, il l a CONSTATEE." + "\n"
            + "Motif de la regularisation : " + motif
        )
    return mission


def regulariser_mission(charger_file, identifiant, motif):
    """PORTE : la file ACTIVE dit terminee une mission dont le journal porte la fin.

    Les refus sont NOMMES et DIRECTIONNELS (le message dit le remede, aucune
    ecriture). L ACTE ecrit la FILE, declare la fin au MARBRE en mode IDEMPOTENT
    (jamais deux bornes) et note l ACTE sous l action `regularisation`.
    """
    file_missions = charger_file()
    mission = mission_par_id(file_missions, identifiant)
    evenements = lire_evenements_marbre()
    code, verdict = diagnostiquer(motif, mission, porte_la_fin(evenements, identifiant))

    if verdict == VERDICT_MOTIF_MANQUANT:
        print('REFUS : le motif est OBLIGATOIRE (--motif "...") -- une regularisation'
              " se TRACE, jamais muette.")
        return code
    if verdict == VERDICT_INCONNUE:
        print("REFUS : " + identifiant + " est INCONNUE de la file ACTIVE -- une"
              " regularisation FERME une ligne de la file, elle n en CREE aucune.")
        print("  Remede : une mission menee HORS file s enregistre par"
              " `python main.py enregistrer --id ... `.")
        return code
    if verdict == VERDICT_DEJA_TERMINEE:
        print("REFUS : " + identifiant + " est DEJA terminee dans la file -- rien a"
              " regulariser (rien n est ecrit, rien n est double).")
        print("  Si le journal ne porte AUCUNE fin, l ecart doit RESTER accuse :"
              " c est `fin` ou `enregistrer` qui fait la fin, pas cette porte.")
        return code
    if verdict == VERDICT_EN_COURS:
        print("REFUS : " + identifiant + " est la mission EN COURS -- c est `fin` qui"
              " la close, pas une regularisation.")
        return code
    if verdict == VERDICT_SANS_FIN:
        print("REFUS : le journal NE PORTE PAS de fin pour " + identifiant + " -- une"
              " regularisation CONSTATE une fin, elle ne l INVENTE pas.")
        print("  L ecart < fin au journal, mais encore " + str(mission.get("statut"))
              + " dans la file > ne s applique donc pas : rien n est ecrit.")
        return code

    date = horodater()
    poser_la_regularisation(mission, motif, date, identifiant)
    enregistrer_file(file_missions)
    # La BORNE de fin est declaree IDEMPOTENTE : la fin est DEJA au journal (c est
    # la condition d entree), donc l appel ne double RIEN -- et si elle manquait,
    # le pilote COMBLERAIT le trou au lieu de laisser un ecart (meme garde que la
    # cloture, MO-108).
    declarer_borne_marbre(
        mission,
        "fin",
        "fin CONSTATEE par le pilote (regularisation) : " + motif,
        portes=[PORTE_REGULARISER],
    )
    # L ACTE lui-meme : une action a LUI, jamais un second `fin` -- la vue s en
    # fait une section, et le controle de coherence ne compte que les bornes.
    declarer_borne_marbre(
        mission,
        ACTION_REGULARISATION,
        "regularisation de la file : " + motif,
        portes=[PORTE_REGULARISER],
    )
    journaliser_mission(
        {
            "type": "mission-regularisee",
            "date": date,
            "id": identifiant,
            "theme": mission.get("theme", ""),
            "motif": motif,
            "detail": ("mission " + identifiant + " REGULARISEE (la fin vivait deja"
                       " au journal) : " + motif),
        }
    )
    print("Mission " + identifiant + " REGULARISEE : la file dit desormais terminee ce"
          " que le journal portait deja.")
    print("  Motif de la regularisation : " + motif)
    print("  La borne de fin n a PAS ete doublee (declaration idempotente au marbre).")
    return 0
