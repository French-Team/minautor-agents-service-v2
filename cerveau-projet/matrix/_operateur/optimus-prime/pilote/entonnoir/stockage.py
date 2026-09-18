"""Stockage de l'entonnoir : charger, enregistrer, horodater.

NOMMAGE : ce module s'appelle stockage.py (PAS commun.py) pour ne pas entrer
en collision avec les modules du pilote (le script importe depuis son dossier).
Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import json
import os
from datetime import datetime
from pathlib import Path

REPERTOIRE_ENTONNOIR = Path(__file__).resolve().parent
REPERTOIRE_PILOTE = REPERTOIRE_ENTONNOIR.parent
if REPERTOIRE_PILOTE.name != "pilote":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_ENTONNOIR) + " n'est pas dans pilote/"
    )

try:
    from listes import NOM_ENTONNOIR, PREFIXE_ITEM
except ImportError:  # importe comme paquet (depuis le pilote) : chemin complet
    from entonnoir.listes import NOM_ENTONNOIR, PREFIXE_ITEM

CHEMIN_ENTONNOIR = REPERTOIRE_PILOTE / NOM_ENTONNOIR

ENCODAGE = "utf-8"
INDENTATION_JSON = 2


def verifier_famille(identifiant):
    """Refuse un id qui n'appartient PAS a la famille de CET entonnoir (CV-009).

    Pourquoi une garde ici : les deux entonnoirs (Optimus / cameleon) sont deux
    copies du meme outil, donc un id de l'autre flux ne se distingue de rien --
    il repondait simplement "Mission inconnue", ce qui ressemble a un oubli de
    saisie au lieu d'un id etranger. Un id hors famille est un ECART, pas une
    absence : on le dit (code 2, aucune ecriture).
    """
    if identifiant.startswith(PREFIXE_ITEM):
        return 0, ""
    return 2, (
        "Identifiant hors famille : " + repr(identifiant) + " (attendu "
        + PREFIXE_ITEM + "NNN pour cet entonnoir) -- un item de l'autre "
        "entonnoir ne se manipule pas ici."
    )


def normaliser_chargement(etat):
    """AUTO-SOIN a la lecture : l auto-validation est un INDEX d ids, pas une COPIE.

    Une mission presente dans deux listes = DEUX verites, et le brin se BLOQUE
    dessus (mesure MO-175 : tresser ne rend jamais la main quand un id vit dans
    deux files). Une file legacy est donc CONVERTIE en index et RETIREE des files :
    la mission ne vit plus qu a UN domicile.
    """
    try:
        from listes import (CHAMP_AUTO_VALIDATION, CLE_AUTO_VALIDEES,
                            CLE_LEGACY_AUTO_VALIDEE, VERDICT_AUTO)
    except ImportError:
        from entonnoir.listes import (CHAMP_AUTO_VALIDATION, CLE_AUTO_VALIDEES,
                                      CLE_LEGACY_AUTO_VALIDEE, VERDICT_AUTO)
    files = etat.get("files")
    index = list(etat.get(CLE_AUTO_VALIDEES) or [])
    if isinstance(files, dict):
        legacy = files.pop(CLE_LEGACY_AUTO_VALIDEE, None) or []
        for missions in list(files.values()) + [legacy]:
            for mission in missions or []:
                if not isinstance(mission, dict):
                    continue
                if mission.get(CHAMP_AUTO_VALIDATION) != VERDICT_AUTO:
                    continue
                if mission.get("id") and mission["id"] not in index:
                    index.append(mission["id"])
    etat.setdefault("files", {})
    if index:
        etat[CLE_AUTO_VALIDEES] = index
    return etat


def charger_entonnoir():
    """Retourne l'etat de l'entonnoir, ou l'etat initial si le fichier n'existe pas.

    Echelon 0 : le vrac. Echelons 1-2 : une file PAR TYPE, rangee par categorie.
    """
    if not CHEMIN_ENTONNOIR.exists():
        return {"vrac": [], "files": {}, "compteur": 0}
    with open(CHEMIN_ENTONNOIR, "r", encoding=ENCODAGE) as flux:
        return normaliser_chargement(json.load(flux))


def enregistrer_entonnoir(etat):
    """Ecrit l'etat de l'entonnoir de facon atomique (tmp + REMPLACEMENT, LF forces)."""
    chemin_tmp = CHEMIN_ENTONNOIR.with_name(NOM_ENTONNOIR + ".tmp")
    with open(chemin_tmp, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(etat, flux, indent=INDENTATION_JSON, ensure_ascii=True)
        flux.write("\n")
    os.replace(chemin_tmp, CHEMIN_ENTONNOIR)


def horodater():
    """Retourne la date-heure locale au format des journaux."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
