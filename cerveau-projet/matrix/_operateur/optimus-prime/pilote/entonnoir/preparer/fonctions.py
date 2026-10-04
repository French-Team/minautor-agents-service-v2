"""Fonctions simples de la categorie preparer : une seule tache chacune.

POURQUOI CETTE PORTE (EO-313, demande createur du 2026-09-20)
Les outils qu une mission allait appeler etaient une FONCTION DE SON TYPE
(checklist/listes.py OUTILS_PAR_TYPE) : deux missions dev recevaient les MEMES
outils, et un outil qu UNE mission precise appelait ne pouvait pas lui etre livre.
Le createur le dit : "si la mission d apres est differente, elle va surement
utiliser des outils differents" -- donc la liste se PREPARE EN AMONT, au moment ou
l on prepare la mission, et elle est FOURNIE DANS LA MISSION.

POURQUOI SUR L ITEM (et pas sur la mission) : l item est la MEMOIRE DURABLE. Il
survit au redemarrage et il existe AVANT la mission ; la mission nait au chargement,
et c est le pont item -> mission qui RECOPIE la liste. Choix tranche par le createur
le 2026-09-20.

SOUVERAINETE : la liste est DECLAREE ici, jamais devinee. Ce verbe ne propose RIEN
(ni mot-cle, ni table) : la proposition viendra du REGISTRE DES OUTILS (EO-314), qui
la soumettra a validation -- une proposition n ouvre rien.

LA PORTE VALIDE CONTRE LE CONSOMMATEUR : chaque nom est resolu par le catalogue des
briques QUE L INJECTION SAIT SERVIR (injection/modes_emploi.py, trouver_brique), et
c est SON refus qui parle (refus_nom). Une porte qui accepterait un nom non servable
ferait ACCUSER par le garde une mission qu elle a prise elle-meme. Le PLAFOND de
l injection est IMPORTE de son domicile (pilote/constants.py) : une liste plus longue
est REFUSEE, jamais servie en partie en silence.

ATOMICITE ET TRACE : TOUS les noms sont valides AVANT la premiere ecriture (un seul
nom non servable et l item garde sa liste d avant) ; la liste d avant est conservee
dans outils_avant, comme role_avant et categorie_avant -- on ne reecrit jamais une
identite en silence.
"""
import importlib.util
import sys
from pathlib import Path

# Le PILOTE est installe dans sys.path pour lire le PLAFOND a SON domicile (meme
# geste que roles.py) : une seule source pour la valeur, jamais une copie.
REPERTOIRE_PILOTE = Path(__file__).resolve().parent.parent.parent
if str(REPERTOIRE_PILOTE) not in sys.path:
    sys.path.append(str(REPERTOIRE_PILOTE))

from constants import PLAFOND_OUTILS_MODE_EMPLOI  # noqa: E402  (apres le sys.path)
from listes import CHAMP_OUTILS, CHAMP_OUTILS_AVANT, CHAMP_OUTILS_LE  # noqa: E402
from stockage import horodater, trouver_item, verifier_famille  # noqa: E402
from transport_listes import decouper_liste  # noqa: E402  (domicile partage, M-076)

# L EXTRACTEUR DE BRIQUES : charge par CHEMIN, jamais un import croise -- l entonnoir
# est appele en SOUS-PROCESSUS par le pilote (doctrine de la zone, indices.md : deux
# copies du meme outil, donc des modules homonymes).
CHEMIN_EXTRACTEUR = REPERTOIRE_PILOTE / "injection" / "modes_emploi.py"


def charger_extracteur():
    """L extracteur de briques de SON domicile -- ou un refus NOMME.

    Aucune resolution n est recopiee ici : la porte interroge la MEME fonction que
    l injection (trouver_brique) et le MEME refus (refus_nom). C est ce qui garantit
    qu un nom accepte par la porte est un nom que l injection sait servir.
    """
    if not CHEMIN_EXTRACTEUR.is_file():
        raise RuntimeError("extracteur de briques ABSENT : " + str(CHEMIN_EXTRACTEUR))
    specification = importlib.util.spec_from_file_location(
        "modes_emploi_entonnoir", str(CHEMIN_EXTRACTEUR))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _noms_uniques(outils_texte):
    """Les noms declares, dans l ORDRE dit, sans doublon -- et les doublons ecartes.

    Un doublon n est jamais avale en silence : un outil cite deux fois ne se sert
    qu une fois, et l agent doit le savoir (le message le DIT).
    """
    noms = [nom.strip() for nom in decouper_liste(outils_texte) if nom.strip()]
    uniques = []
    doublons = []
    for nom in noms:
        if nom in uniques:
            if nom not in doublons:
                doublons.append(nom)
            continue
        uniques.append(nom)
    return uniques, doublons


def preparer_outils(etat, identifiant, outils_texte):
    """Pose la LISTE DES OUTILS d un item (n importe quel echelon). Rend (code, message).

    Trois refus NOMMES, aucune ecriture dans les trois cas :
      - un nom non servable : le refus de l extracteur (nom fautif, proches, remede) ;
      - une liste plus longue que le PLAFOND de l injection : les noms EN TROP ;
      - un item inconnu, ou un id hors famille.
    La chaine vide VIDE la liste (geste explicite, trace) ; la MEME liste rend code 1
    (rien a faire) : une porte qui reecrit ce qui est deja en place fabrique du bruit.
    """
    code, message = verifier_famille(identifiant)
    if code != 0:
        return code, message
    item, _type_file = trouver_item(etat, identifiant)
    if item is None:
        return 1, "Mission inconnue dans l entonnoir : " + identifiant
    avant = list(item.get(CHAMP_OUTILS) or [])
    noms, doublons = _noms_uniques(outils_texte)
    note_doublons = (" (doublon(s) ecarte(s) : " + ", ".join(doublons) + ")") if doublons else ""
    if not noms:
        if not avant:
            return 1, ("Mission " + identifiant + " : aucune liste a poser ni a retirer"
                       " -- l item n en portait aucune, donc le repli par TYPE s appliquera"
                       " a l injection.")
        item[CHAMP_OUTILS] = []
        item[CHAMP_OUTILS_LE] = horodater()
        item[CHAMP_OUTILS_AVANT] = avant
        return 0, ("Mission " + identifiant + " : liste d outils VIDEE (avant : "
                   + ", ".join(avant) + ") -- le repli par TYPE s appliquera a l injection.")
    if len(noms) > PLAFOND_OUTILS_MODE_EMPLOI:
        return 2, ("REFUS : " + str(len(noms)) + " outil(s) prepare(s) pour un PLAFOND de "
                   + str(PLAFOND_OUTILS_MODE_EMPLOI) + " a l injection -- la porte ne pose pas"
                   " une liste que le consommateur servirait en PARTIE en silence.\n"
                   "  en trop : " + ", ".join(noms[PLAFOND_OUTILS_MODE_EMPLOI:]) + "\n"
                   "  (garde les " + str(PLAFOND_OUTILS_MODE_EMPLOI)
                   + " outils que la mission va VRAIMENT appeler.)")
    module = charger_extracteur()
    inconnus = [nom for nom in noms if module.trouver_brique(nom) is None]
    if inconnus:
        lignes = ["REFUS : " + str(len(inconnus)) + " nom(s) non servable(s) -- AUCUNE ecriture"
                  " (l item garde sa liste)."]
        for nom in inconnus:
            lignes.append("  " + module.refus_nom(nom))
        return 2, "\n".join(lignes)
    if noms == avant:
        return 1, ("Mission " + identifiant + " : liste d outils deja en place ("
                   + ", ".join(noms) + ") -- rien a faire.")
    item[CHAMP_OUTILS] = noms
    item[CHAMP_OUTILS_LE] = horodater()
    if avant:
        item[CHAMP_OUTILS_AVANT] = avant
    return 0, ("Mission " + identifiant + " : " + str(len(noms)) + " outil(s) prepare(s) : "
               + ", ".join(noms) + note_doublons
               + (" (avant : " + ", ".join(avant) + ")" if avant else ""))
