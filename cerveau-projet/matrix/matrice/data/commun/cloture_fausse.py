"""LE JUGEMENT D UNE CLOTURE FAUSSE (EO-356) : une regle, UN domicile (M-076).

POURQUOI UN DOMICILE (MO-426) : la panne payee en MO-387 -- un round ouvre une
mission par une CHARGE INDIVIDUELLE tracee, et la premiere cloture qui suit nomme
une AUTRE mission (la tete du lot) -- est lue par DEUX consommateurs :
  - le SUIVI DU PILOTE (super-combo suivi-pilote.py, maillon 37) : il DIAGNOSTIQUE ;
  - la CLOTURE du pilote (fin/fonctions.py, MO-426) : elle REFUSE.
Deux copies de cette regle divergeraient en silence (L-029) : elle vit donc ici,
et les deux la CONSOMMENT au lieu de la recopier.

LA REGLE
Une CHARGE individuelle (hors lot) dont la PREMIERE issue est une `fin` qui nomme
une AUTRE mission est une CLOTURE FAUSSE. Ce qui ARRETE la lecture est la PREMIERE
des deux issues : un `report` de la MEME mission (parquee : sortie de round SANS
cloture), ou une `fin` (de n importe qui). Sans trace de charge, RIEN n est accuse :
les charges anterieures au 2026-09-22 sont muettes, la porte ne devine pas.

LES DEUX EXEMPTIONS, EXIGEES ENSEMBLE (et c est ce qui les rend etroites)
  - la mission CLOSE a ete PARQUEE (`report`) AVANT la charge ;
  - ET elle a ete REPRISE (`prise`) APRES la charge.
Le cas paye en MO-387 (la tete du lot close sous le nom d une charge) n a AUCUNE
des deux -- la tete du lot n avait jamais ete parquee. Une `prise` seule ne suffit
pas : la machine la pose au geste de reception, elle excuserait MO-387.

LA DEUXIEME FAMILLE (EO-455 / MO-480, mesure du 2026-09-27) : le TITRE DU BILAN.
La premiere famille lit le JOURNAL et suppose que la cloture nomme la mission close.
Le cas REEL paye en MO-440 est d une AUTRE famille : la fin a bien nomme la mission
close (MO-440), mais le BILAN attache declarait < BILAN MO-463 > -- le round avait
clos la mauvaise mission, et journal, file et controle de coherence disaient tous
D ACCORD. Le seul endroit ou la faute se lit est le TITRE du bilan : c est lui que
juge `bilan_etranger`, et c est MESURE (deux accusations vraies sur 327 bilans,
aucune accusation fausse -- le critere large < premier identifiant mentionne >
ayant ete mesure puis REFUSE : 11 accusations dont 9 legitimes).
"""

import re

# Le TITRE d un bilan : la PREMIERE ligne non vide, et la seule forme jugee --
# `BILAN <id>`. Une premiere ligne qui ne declare aucun identifiant n est PAS jugee
# (la regle dit ce qu elle sait lire, elle ne devine pas), et le CORPS du recit reste
# libre : un bilan CITE legitimement d autres missions plus loin (mesure du 2026-09-27).
MOTIF_TITRE_BILAN = re.compile(r"^BILAN\s+((?:MO|M)-[0-9]+)\b")


def clotures_fausses(evenements, ids_du_lot):
    """Les couples (mission_chargee, mission_closee) des clotures FAUSSES.

    `evenements` : les evenements du journal (dicts portant `action` et `mission`).
    `ids_du_lot` : les ids des missions chargees AVEC un lot -- elles ATTENDENT
    leur tour, leur cloture par la chaine est LEGITIME et n est jamais accusee.
    Rend la LISTE des couples, dans l ordre du journal (vide si aucune).
    """
    journal = [(e.get("action"), e.get("mission")) for e in evenements]
    fausses = []
    for rang, (action, mission_id) in enumerate(journal):
        if action != "charge" or not mission_id or mission_id in ids_du_lot:
            continue
        suivante = None
        reprises = set()
        for a, m in journal[rang + 1:]:
            if a == "report" and m == mission_id:
                suivante = None  # parquee : sortie de round sans cloture
                break
            if a == "prise" and m:
                reprises.add(m)
            if a == "fin":
                suivante = (a, m)
                break
        if suivante is None:
            continue  # jamais close : c est < chargee sans conduite > qui la juge
        _, cloturee = suivante
        if cloturee == mission_id:
            continue
        parquee_avant = any(a == "report" and m == cloturee
                            for a, m in journal[:rang])
        if parquee_avant and cloturee in reprises:
            continue
        fausses.append((mission_id, cloturee))
    return fausses


def normaliser_id(identifiant):
    """La forme COMPARABLE d un identifiant : sa famille (M ou MO) et son numero.

    La famille COMPTE : `M-076` est une mission du cameleon, `MO-076` une mission
    d Optimus -- les confondre ferait taire une vraie faute ou crier une fausse.
    Les zeros de tete, eux, ne comptent pas (M-076 : deux ecritures d un meme id ne
    doivent pas fabriquer deux verdicts).
    """
    texte = str(identifiant or "").strip().upper()
    trouve = re.match(r"^(MO|M)-0*([0-9]+)$", texte)
    if not trouve:
        return texte
    return trouve.group(1) + "-" + trouve.group(2)


def mission_declaree_par_le_titre(bilan):
    """L identifiant DECLARE par le TITRE du bilan, ou "" (aucun).

    Le TITRE = la PREMIERE ligne non vide ; la forme reconnue = `BILAN <id>`. Toute
    autre forme rend "" : la regle ne devine pas ce qu elle ne sait pas lire (mesure
    du 2026-09-27 : 283 des 327 bilans de l historique ne portent pas ce titre).
    """
    if not bilan:
        return ""
    for ligne in str(bilan).splitlines():
        propre = ligne.strip()
        if not propre:
            continue
        trouve = MOTIF_TITRE_BILAN.match(propre)
        return trouve.group(1) if trouve else ""
    return ""


def bilan_etranger(id_close, bilan):
    """Le couple (mission_close, mission_declaree) si le TITRE du bilan en declare UNE AUTRE.

    MESURE DU 2026-09-27 (EO-455, pendant MO-441) sur les 327 bilans de
    `matrice/data/historiques-missions-optimus.jsonl` : ce critere accuse EXACTEMENT
    DEUX enregistrements -- MO-407 (< BILAN MO-412 >) et MO-440 (< BILAN MO-463 >) --
    les DEUX clotures fausses connues, et AUCUN autre. Le critere plus large < premier
    identifiant mentionne > a ete mesure AUSSI et REFUSE : il accuse 11 enregistrements,
    dont 9 bilans legitimes qui CITENT une autre mission des leur premiere ligne.

    Rend None quand il n y a rien a dire -- titre sans identifiant, identifiant
    identique a la mission close, ou entree muette.
    """
    declaree = mission_declaree_par_le_titre(bilan)
    if not declaree or not id_close:
        return None
    if normaliser_id(declaree) == normaliser_id(id_close):
        return None
    return (id_close, declaree)
