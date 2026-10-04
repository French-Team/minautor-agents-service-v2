"""DOMICILE du ROUND SERVI ET JAMAIS CONDUIT : la REGLE, une seule fois (M-076).

CE QUE CE FICHIER JUGE. Le DERNIER acte d un round (le marbre) est une PRISE --
le geste de RECEPTION que le pilote trace -- et AUCUN acte de l AGENT (le
sac-a-dos des usages, tag `auto` EXCLU) ne la suit : le round a ete SERVI et
PRIS par la machine, et l agent a rendu la main sans le CONDUIT. C est le fait
paye par le createur (retour du 2026-09-24 : < quand un round est servi -> tu dois
le faire et ne pas stopper pour faire ton bilan >).

POURQUOI UN DOMICILE, ET PAS UN SEUIL DE PLUS. Les pannes declarees
(round-arme-jamais-pris, round-pris-jamais-conduit) et la plus fine
(bilan-rapport-entre-deux-rounds) se declenchent sur un SEUIL mesure : un arret
IMMEDIAT n est vu par AUCUN garde. Or le FAIT est connu DES L INSTANT ou la prise
est le dernier acte. Ce module rend ce fait NU (aucun seuil) ; c est l APPELANT
qui decide de le DIRE tout de suite (le pilote, au demarrage et dans la remise),
de servir un rappel, ou d attendre son seuil pour parler de panne (le suivi).

DEUX CONSOMMATEURS, UNE REGLE (L-029) : le suivi du pilote (qui crie avec son
seuil declare) et le pilote lui-meme (qui le DIT sans seuil). En recopier une
deuxieme version aurait fait deux verites, donc deux frontieres.

LES DEUX SOURCES sont nommees ICI (relatives a la RACINE de la Matrice ; l
appelant ancre, ce module ne devine aucune racine) :
  - le MARBRE (suivi-optimus.jsonl) : le dernier acte de chaque mission ;
  - le SAC-A-DOS (usages-outils-combos.jsonl) : l ACTIVITE REELLE de l agent.
    Les ROUTINES y marquent leurs passes `auto` : elles sont EXCLUES -- une
    routine n a pas de LLM, elle ne conduit aucun round et ferait taire le fait.
"""

import json
from datetime import datetime
from pathlib import Path

CHEMIN_MARBRE = ("matrice", "data", "suivi-optimus.jsonl")
CHEMIN_SAC_A_DOS = ("matrice", "data", "usages-outils-combos.jsonl")
ACTION_PRISE = "prise"
TAG_ROUTINE = "auto"
FORMATS_HORODATAGE = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M")


def horodate(texte):
    """Le moment d un horodatage, ou None (jamais devine)."""
    for forme in FORMATS_HORODATAGE:
        try:
            return datetime.strptime(str(texte)[:19], forme)
        except (ValueError, TypeError):
            continue
    return None


def lire_evenements(chemin):
    """Les evenements LISIBLES d un journal JSONL, dans l ordre du fichier.

    Une ligne illisible est IGNOREE, le reste est lu (lecture TOLERANTE). Un
    fichier ABSENT rend une liste vide : la question porte sur ce qui est ECRIT.
    """
    chemin = Path(chemin)
    try:
        lignes = chemin.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    evenements = []
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            evenements.append(json.loads(ligne))
        except ValueError:
            continue
    return evenements


def dernier_acte_par_mission(evenements):
    """{id_mission: (moment, date, action)} -- le DERNIER acte de chaque mission."""
    derniers = {}
    for evenement in evenements:
        mission = evenement.get("mission")
        action = evenement.get("action")
        date = evenement.get("date")
        moment = horodate(date)
        if not mission or not action or moment is None:
            continue
        if mission not in derniers or moment > derniers[mission][0]:
            derniers[mission] = (moment, date, action)
    return derniers


def lire_acte_agent(chemin):
    """Le moment du DERNIER acte de l AGENT (sac-a-dos, tag `auto` EXCLU), ou None.

    `None` DIT une mesure impossible (sac-a-dos absent ou illisible) : un fait non
    mesurable ne se conclut pas (L-055).
    """
    chemin = Path(chemin)
    if not chemin.is_file():
        return None
    dernier = None
    try:
        lignes = chemin.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            evenement = json.loads(ligne)
        except ValueError:
            continue
        if TAG_ROUTINE in (evenement.get("tags") or []):
            continue
        moment = horodate(evenement.get("date"))
        if moment and (dernier is None or moment > dernier):
            dernier = moment
    return dernier


def servi_non_conduit(action_dernier_acte, moment_dernier_acte, acte_agent):
    """Le FAIT NU (aucun seuil) : le round est PRIS et l agent ne l a pas CONDUIT.

    Rend :
      - True  : le dernier acte est une PRISE et AUCUN acte de l agent ne la suit ;
      - False : le dernier acte n est PAS une prise, ou un acte de l agent la SUIT ;
      - None  : la mesure est IMPOSSIBLE (moment ou acte agent absents) -- on ne
                conclut pas, et c est l appelant qui le DIT (L-055).

    Frontiere : un acte de l agent STRICTEMENT posterieur dit < conduit >. Un acte
    EGAL (granularite de la seconde) ne blanchit PAS la prise -- c est la MEME
    frontiere que le detecteur du suivi, et c est voulu : une seule regle.
    """
    if str(action_dernier_acte) != ACTION_PRISE:
        return False
    if moment_dernier_acte is None or acte_agent is None:
        return None
    return not (acte_agent > moment_dernier_acte)


def message_rappel(identifiant, date_prise):
    """Le RAPPEL IMMEDIAT du round servi et jamais conduit (ASCII, nomme le round).

    Il se LIT : il nomme le round et sa prise, et il DIT la route (conduire dans le
    meme tour). Le texte vit ICI, avec la regle -- deux copies divergeraient.
    """
    return ("ROUND SERVI ET JAMAIS CONDUIT : " + str(identifiant)
            + " a ete SERVI et PRIS le " + str(date_prise)
            + ", et AUCUN outil n a ete invoque depuis. Tu as rendu la main apres la"
            " cloture : CONDUIS CE ROUND MAINTENANT (ORDRE 4.2). Un round servi se"
            " conduit DANS LE MEME TOUR -- ne t arrete qu a la fin du LOT, sur un"
            " CRITIQUE (createur), ou sur une QUESTION du createur (ORDRE 4.7).")
