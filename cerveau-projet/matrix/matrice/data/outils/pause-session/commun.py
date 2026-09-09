"""Fonctions communes de pause-session : defcon, file pilote, etat, journal.

Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import hashlib
import json
import os
from datetime import datetime

from constants import (
    CHEMIN_CLASSEUR,
    CHEMIN_EMPREINTE_CLASSEUR,
    CHEMIN_ETAT,
    CHEMIN_FILE_PILOTE,
    CHEMIN_JOURNAL,
    CHEMINS_MAINTENANCE,
    CLE_DEFCON,
    CLE_PERIMETRE,
    ENCODAGE,
    INDENTATION_JSON,
    NIVEAU_PAUSE_AUTO,
    NOM_CLASSEUR_TMP,
    NOM_ETAT_TMP,
    STATUT_EN_COURS,
    TAILLE_BLOC_LECTURE,
    ZONE_MAINTENANCE,
)


def horodater():
    """Retourne la date-heure locale au format des journaux Matrice."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def lire_niveau_defcon():
    """Retourne (niveau_courant, message_absence). Lecture seule, jamais bloquant."""
    if not CHEMIN_CLASSEUR.exists():
        return None, "Variable 'defcon' absente : classeur-variables.json introuvable."
    try:
        with open(CHEMIN_CLASSEUR, "r", encoding=ENCODAGE) as flux:
            donnees = json.load(flux)
    except (json.JSONDecodeError, OSError):
        return None, "Classeur-variables illisible (espion alerte)."
    for variable in donnees.get("variables", ()):
        if variable.get("cle") == CLE_DEFCON:
            try:
                return int(variable.get("valeur")), ""
            except (TypeError, ValueError):
                return None, "Variable 'defcon' illisible dans le classeur."
    return None, "Variable 'defcon' absente du classeur : la definir via bdd-variables."


def charger_file():
    """Retourne la file du pilote (source de verite de la mission en cours)."""
    with open(CHEMIN_FILE_PILOTE, "r", encoding=ENCODAGE) as flux:
        return json.load(flux)


def enregistrer_file(file_missions):
    """Ecrit la file du pilote de facon atomique (tmp + remplacement, LF forces)."""
    chemin_tmp = CHEMIN_FILE_PILOTE.with_name(CHEMIN_FILE_PILOTE.name + ".tmp")
    with open(chemin_tmp, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(file_missions, flux, indent=INDENTATION_JSON, ensure_ascii=True)
        flux.write("\n")
    os.replace(chemin_tmp, CHEMIN_FILE_PILOTE)


def mission_en_cours(file_missions):
    """Retourne la mission en cours, ou None (serie stricte du pilote)."""
    for mission in file_missions.get("missions", []):
        if mission.get("statut") == STATUT_EN_COURS:
            return mission
    return None


def etat_existe():
    """True si un etat de pause est deja pose (garde : pas de pause double)."""
    return CHEMIN_ETAT.exists()


def serialiser_etat(file_missions):
    """Construit l'etat de pause : mission EN COURS retiree de la file.

    Sauvegarde SEULEMENT a la pause (decision createur) : ce JSON est la
    reprise a l'identique (mission + position chronologique dans la file).
    Retourne (etat, mission) ou (None, None) si aucune mission en cours.
    """
    mission = mission_en_cours(file_missions)
    if mission is None:
        return None, None
    missions_restantes = [
        m for m in file_missions.get("missions", []) if m.get("id") != mission["id"]
    ]
    etat = {
        "mission": mission,
        "position": file_missions.get("missions", []).index(mission),
        "file_restante": missions_restantes,
        "pause_le": horodater(),
    }
    return etat, mission


def poser_etat(etat):
    """Pose l'etat serialise (atomique : tmp + remplacement, LF forces)."""
    chemin_tmp = CHEMIN_ETAT.with_name(NOM_ETAT_TMP)
    with open(chemin_tmp, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(etat, flux, indent=INDENTATION_JSON, ensure_ascii=True)
        flux.write("\n")
    os.replace(chemin_tmp, CHEMIN_ETAT)


def lire_etat():
    """Retourne l'etat de pause pose, ou None."""
    if not CHEMIN_ETAT.exists():
        return None
    with open(CHEMIN_ETAT, "r", encoding=ENCODAGE) as flux:
        return json.load(flux)


def retirer_etat():
    """Supprime l'etat de pause apres reprise reussie."""
    os.remove(CHEMIN_ETAT)


def journaliser(type_evenement, details):
    """Append UNE ligne JSON au journal des pauses (jamais bloquant)."""
    ligne = {"type": type_evenement, "date": horodater()}
    ligne.update(details)
    with open(CHEMIN_JOURNAL, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(ligne, ensure_ascii=True) + "\n")


def lire_journal(n=5):
    """Retourne les n derniers evenements (les plus recents d'abord)."""
    if not CHEMIN_JOURNAL.exists():
        return []
    evenements = []
    for ligne in CHEMIN_JOURNAL.read_text(encoding=ENCODAGE).splitlines():
        try:
            evenements.append(json.loads(ligne))
        except json.JSONDecodeError:
            continue
    return list(reversed(evenements))[:n]


def extraire_options(arguments, noms_connus):
    """Extrait les options --nom valeur d'une liste d'arguments (forme seulement)."""
    options = {}
    index = 0
    while index < len(arguments):
        nom = arguments[index]
        if nom.startswith("--") and nom[2:] in noms_connus:
            if index + 1 < len(arguments):
                options[nom[2:]] = arguments[index + 1]
            index += 2
        else:
            index += 1
    return options


def lire_perimetre():
    """Retourne (niveau_defcon, liste_zones_exclues, message_absence).

    Les zones exclues vivent dans le classeur-variables (cle CLE_PERIMETRE) :
    UNE source de verite, tenue par l'outil pause-session lui-meme (porte
    bdd-variables, motif atomique + empreinte repris de machine-defcon).

    Etancheite (decision createur, audit protections 2026-09-09) : la zone
    neutre ZONE_MAINTENANCE est RESOLUE vers ses chemins reels ici, afin
    que le classeur ne revele jamais le nom de l'entite interne.
    """
    niveau, message = lire_niveau_defcon()
    zones = []
    if CHEMIN_CLASSEUR.exists():
        try:
            with open(CHEMIN_CLASSEUR, "r", encoding=ENCODAGE) as flux:
                donnees = json.load(flux)
            for variable in donnees.get("variables", ()):
                if variable.get("cle") == CLE_PERIMETRE:
                    brut = variable.get("valeur", "")
                    zones = [z.strip() for z in str(brut).split(",") if z.strip()]
        except (json.JSONDecodeError, OSError):
            zones = []
    if ZONE_MAINTENANCE in zones:
        zones.remove(ZONE_MAINTENANCE)
        zones.extend(list(CHEMINS_MAINTENANCE))
    return niveau, zones, message
