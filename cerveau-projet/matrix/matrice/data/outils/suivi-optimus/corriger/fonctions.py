"""Fonctions simples de la categorie corriger : une seule tache chacune.

POURQUOI CE VERBE (EO-269, decision de l operateur du 2026-09-19) : le pilote a
declare `duree_s = 0` a CHAQUE cloture pendant des mois -- un PLACEHOLDER pris
pour une mesure (L-055 : une valeur qui ment se lit comme un fait). EO-267 a
repare la SOURCE (la vue CALCULE desormais la duree des deux bornes) ; il restait
l HISTOIRE : des centaines de lignes declarant `0`, et AUCUNE porte pour les
corriger EN PLACE. Le journal est en AJOUT SEUL : on ne supprime pas une ligne, on
la CORRIGE, et l ancienne valeur SURVIT dans l entree.

CE QUE LA PORTE CORRIGE, ET RIEN D AUTRE : un evenement qui DECLARE une `duree_s`
NON VIDE differente de la duree MESUREE par les bornes de sa mission. C est
exactement la population du garde `verifier-placeholders`, qui reste TEL QUEL
(decision de l operateur) : il est la MESURE DE L AVANCEMENT, et c est lui qui
valide la porte -- apres le nettoyage il doit rendre 0 ecart.

UNE DECLARATION EGALE A LA MESURE EST UN FAIT : un vrai zero (les bornes donnent
0 s -- mesure du 2026-09-20 : 45 missions) ou une vraie duree n est JAMAIS touchee.
Un SILENCE (valeur vide) n est pas une declaration : il n est ni accuse, ni corrige.

LA VALEUR HONNETE EST VIDE, PAS LA MESURE : le pilote n a jamais mesure, et
recopier la duree des bornes remplacerait un mensonge par une valeur que PERSONNE
n a declaree. C est la VUE qui calcule (vue/fonctions.py), et elle le faisait deja.

L ANCIENNE VALEUR RESTE RELISIBLE : elle voyage dans `corrections` (date, motif,
duree_s_avant, duree_s_apres, mesure des bornes), portee par l entree -- meme
patron que `bdd-modifications corriger` (EO-155), qui declare son champ de la
meme facon.

LA REGLE DE DUREE N EST PAS RECOPIEE (L-032) : elle vient du DOMICILE
(`vue.fonctions.calculer_duree`), celui-la meme que le garde consomme.
"""
from datetime import datetime

from constants import ENCODAGE
from vue.fonctions import calculer_duree

# Champs du journal consommes ici : le nom est une valeur, elle vit donc a UN
# domicile (convention zero-valeur-en-dur), et ce domicile est le proprietaire du
# champ -- le meme choix que `corriger` de bdd-modifications (EO-155).
CHAMP_DUREE = "duree_s"
CHAMP_CORRECTIONS = "corrections"


def declaree(evenement):
    """La valeur DECLAREE du champ, ou "" -- un silence n est pas une declaration."""
    return str(evenement.get(CHAMP_DUREE, "") or "").strip()


def nombre(valeur):
    """La valeur declaree en entier, ou None quand ce n est PAS un nombre."""
    try:
        return int(float(valeur))
    except (TypeError, ValueError):
        return None


def mesure_des_bornes(agregat):
    """La duree MESUREE des bornes de la mission, ou None (aucune mesure possible).

    Une mesure absente n est pas un zero : sans les deux bornes, RIEN ne permet de
    dire si la declaration est vraie, donc la porte ne la corrige pas -- et le garde
    ne l accuse pas non plus. MEME CRITERE des deux cotes : c est ce qui rend les
    deux mesurables ensemble (le garde valide la porte).
    """
    if not agregat:
        return None
    debut = str(agregat.get("debut", "") or "")
    fin = str(agregat.get("fin", "") or "")
    if not debut or not fin:
        return None
    return calculer_duree(debut, fin)


def population(evenements, agregats, mission=""):
    """Separe les evenements a corriger des declarations qui sont des FAITS.

    Rend (cibles, egales, sans_mesure, inconnue) :
      cibles      : [(index, mission, valeur_avant, mesure)] -- la declaration
                    contredit la mesure, la porte la corrige ;
      egales      : [mission] dont la declaration EGALE la mesure (jamais touchee) ;
      sans_mesure : [mission] sans les deux bornes (aucune correction possible) ;
      inconnue    : True quand la mission demandee n existe PAS dans le journal --
                    une correction ne devine jamais sa cible.
    """
    vues = set()
    for evenement in evenements:
        nom = str(evenement.get("mission", "") or "")
        if nom:
            vues.add(nom)
    inconnue = bool(mission) and mission not in vues
    cibles = []
    egales = set()
    sans_mesure = set()
    for index, evenement in enumerate(evenements):
        nom = str(evenement.get("mission", "") or "")
        if mission and nom != mission:
            continue
        avant = declaree(evenement)
        if not avant:
            continue
        mesure = mesure_des_bornes(agregats.get(nom))
        if mesure is None:
            sans_mesure.add(nom)
            continue
        if nombre(avant) == mesure:
            egales.add(nom)
            continue
        cibles.append((index, nom, avant, mesure))
    return cibles, sorted(egales), sorted(sans_mesure), inconnue


def corriger_evenement(evenement, mesure, motif):
    """Corrige UNE entree EN PLACE et rend la ligne du rapport.

    DATE, ACTION ET DETAIL SONT CONSERVES : seuls `duree_s` change (vide = la
    valeur honnete) et `corrections` s enrichit -- l ancienne valeur reste donc
    RELISIBLE, avec la date, le motif et la mesure qui l a condamnee.
    """
    avant = declaree(evenement)
    evenement[CHAMP_DUREE] = ""
    evenement.setdefault(CHAMP_CORRECTIONS, []).append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "motif": motif,
        "duree_s_avant": avant,
        "duree_s_apres": "",
        "mesure_des_bornes_s": mesure,
    })
    return ("  " + str(evenement.get("mission", "")) + "  " + str(evenement.get("date", ""))
            + "  " + str(evenement.get("action", "")) + " : duree_s " + repr(avant)
            + " -> vide (mesure des bornes " + str(mesure) + " s)")


def corriger_cibles(evenements, cibles, motif):
    """Corrige les cibles, dans l ORDRE du journal. Rend (nombre, lignes)."""
    lignes = []
    for index, _nom, _avant, mesure in cibles:
        lignes.append(corriger_evenement(evenements[index], mesure, motif))
    return len(cibles), lignes


def compter_lignes(chemin):
    """Le nombre de LIGNES NON VIDES du journal, lu BRUT (jamais par le parseur).

    POURQUOI : `lire_evenements` SAUTE une ligne illisible, et la reecriture
    ecrirait alors un journal PLUS COURT -- une suppression SILENCIEUSE de donnees.
    La porte compare les deux comptes AVANT d ecrire et REFUSE s ils different :
    une correction ne supprime JAMAIS une ligne.
    """
    try:
        contenu = chemin.read_text(encoding=ENCODAGE)
    except OSError:
        return None
    return sum(1 for ligne in contenu.splitlines() if ligne.strip())
