"""Fonctions communes du pilote : file de missions, intercom, historique, chaine (lot).

Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import json
import os
import subprocess
import sys
from datetime import datetime

from constants import (
    BOITE_MATRICE_IN,
    BOITE_PILOTE_OUT,
    CHEMIN_CLASSEUR_VARIABLES,
    CHEMIN_ENTONNOIR,
    CHEMIN_ETAT_PAUSE,
    CHEMIN_FILE,
    CHEMIN_HISTORIQUE,
    CHEMIN_THEMES,
    CLE_DEFCON,
    ENCODAGE,
    INDENTATION_JSON,
    NIVEAU_DEFCON_MAX,
    NOM_ENTONNOIR,
    NOM_FILE,
    STATUT_EN_ATTENTE,
    STATUT_EN_COURS,
    THEME_DEFCON,
)


def horodater():
    """Retourne la date-heure locale au format des journaux."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def charger_themes_autorises():
    """Retourne les noms de themes du vivier (liste vide si absent ou illisible).

    Doctrine lecons_utiles : jamais bloquant. La fermeture du champ ne
    s'applique que si le registre est lisible ET non vide (degradation
    signalee sinon : le theme passe mais l'ECART est crie).
    """
    if not CHEMIN_THEMES.exists():
        return []
    try:
        with open(CHEMIN_THEMES, "r", encoding=ENCODAGE) as flux:
            donnees = json.load(flux)
    except (json.JSONDecodeError, OSError):
        return []
    themes = donnees.get("themes", []) if isinstance(donnees, dict) else []
    return [t.get("nom", "") for t in themes if t.get("nom", "")]


def valider_theme(theme):
    """Porte du champ theme FERME : refuse un theme hors vivier (code 2 + liste).

    Correspondance casse-ignoree sur la forme canonique du vivier ; le theme
    reconnu est renvoye sous SA forme canonique (canonisation a la porte).
    Vivier absent/illisible/vide -> degradation : accepte mais ECART affiche
    (la fermeture ne doit jamais bloquer une reparation du vivier lui-meme).
    Retourne (code, theme_renvoye).
    """
    theme = " ".join(theme.split())
    themes_autorises = charger_themes_autorises()
    if not themes_autorises:
        print("ECART : vivier-themes.json absent, illisible ou vide -- theme accepte SANS verification (a reparer).")
        return 0, theme
    for nom in themes_autorises:
        if nom.lower() == theme.lower():
            return 0, nom
    print("REFUS : theme " + repr(theme) + " hors vivier (champ ferme).")
    print("Themes disponibles : " + ", ".join(themes_autorises))
    print("(pour l'ajouter au vivier d'abord : outil theme-vivier, verbe ajouter)")
    return 2, theme


def defcon_bloque_theme(theme):
    """Garde mise en securite : a defcon 5, seul le theme DEFCON reste injectable.

    Lecture seule du classeur-variables (variable tenue par machine-defcon),
    JAMAIS bloquant si illisible ou absente (une panne de lecture n'est pas
    une mise en securite ; l'espion attrapera la panne). Retourne (code, message).
    """
    if not CHEMIN_CLASSEUR_VARIABLES.exists():
        return 0, ""
    try:
        with open(CHEMIN_CLASSEUR_VARIABLES, "r", encoding=ENCODAGE) as flux:
            donnees = json.load(flux)
    except (json.JSONDecodeError, OSError):
        return 0, ""
    for variable in donnees.get("variables", ()):
        if variable.get("cle") != CLE_DEFCON:
            continue
        try:
            niveau = int(variable.get("valeur"))
        except (TypeError, ValueError):
            return 0, ""
        if niveau == NIVEAU_DEFCON_MAX and theme != THEME_DEFCON:
            return 1, (
                "REFUS defcon 5 : mise en securite totale -- seules les missions "
                "themees DEFCON restent injectables (optimus-prime reveille)."
            )
        return 0, ""
    return 0, ""


def session_en_pause():
    """Garde protocole de pause (M-080) : True si l'etat serialise existe.

    L'etat est pose par l'outil pause-session (data/session-matrix-etat.json)
    au moment de la pause, supprime a la reprise. Lecture seule, jamais
    bloquante : fichier absent = session active.
    """
    return CHEMIN_ETAT_PAUSE.exists()


def charger_file():
    """Retourne la file des missions, ou une file vide si elle n'existe pas."""
    if not CHEMIN_FILE.exists():
        return {"missions": [], "compteur": 0, "lot": None}
    with open(CHEMIN_FILE, "r", encoding=ENCODAGE) as flux:
        return json.load(flux)


def enregistrer_file(file_missions):
    """Ecrit la file de facon atomique (tmp + remplacement, LF forces)."""
    chemin_tmp = CHEMIN_FILE.with_name(NOM_FILE + ".tmp")
    with open(chemin_tmp, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(file_missions, flux, indent=INDENTATION_JSON, ensure_ascii=True)
        flux.write("\n")
    os.replace(chemin_tmp, CHEMIN_FILE)


def ids_en_lot(file_missions):
    """Retourne la liste des ids du lot actif (liste vide si pas de lot)."""
    lot = file_missions.get("lot")
    if not lot:
        return []
    return list(lot.get("ids", []))


def portee_lot(file_missions):
    """Retourne (ids_du_lot, position_k, total_n) pour la mission EN COURS.

    Serie stricte : au maximum une mission en cours ; si elle fait partie du
    lot actif, sa position est k dans le lot (k commence a 1).
    Retourne (None, 0, 0) si pas de lot ou mission hors lot.
    """
    ids = ids_en_lot(file_missions)
    if not ids:
        return (None, 0, 0)
    en_cours = mission_en_cours(file_missions)
    if en_cours is None or en_cours["id"] not in ids:
        return (None, 0, 0)
    return (ids, ids.index(en_cours["id"]) + 1, len(ids))


def prochaine_en_attente(file_missions):
    """Retourne la premiere mission en attente (ordre de chargement), ou None."""
    for mission in file_missions.get("missions", []):
        if mission.get("statut") == STATUT_EN_ATTENTE:
            return mission
    return None


def prochaine_du_lot(file_missions):
    """Retourne la premiere mission du lot encore en attente, ou None."""
    ids = ids_en_lot(file_missions)
    for mission in file_missions.get("missions", []):
        if mission.get("id") in ids and mission.get("statut") == STATUT_EN_ATTENTE:
            return mission
    return None


def mission_en_cours(file_missions):
    """Retourne la mission en cours, ou None (serie stricte : au maximum une)."""
    for mission in file_missions.get("missions", []):
        if mission.get("statut") == STATUT_EN_COURS:
            return mission
    return None


def prochain_id(file_missions):
    """Calcule l'identifiant de la prochaine mission (compteur incremente)."""
    file_missions["compteur"] = file_missions["compteur"] + 1
    return "M-" + str(file_missions["compteur"]).zfill(3)


def annoncer(type_message, mission, extra=None):
    """Depose l'annonce DEBUT/FIN d'une mission dans la boite du pilote."""
    message = {"type": type_message, "date": horodater(), "mission": mission["id"], "theme": mission["theme"]}
    if extra:
        message.update(extra)
    deposer_message(BOITE_PILOTE_OUT, message)


def annoncer_debut(file_missions, mission):
    """Annonce le DEBUT d'une mission, avec sa position dans le lot si place."""
    ids, k, total = portee_lot(file_missions)
    extra = {"position": str(k) + "/" + str(total)} if ids else None
    annoncer("debut-mission", mission, extra)
    suffixe = " (round " + str(k) + "/" + str(total) + ")" if ids else ""
    print("DEBUT mission " + mission["id"] + " -- " + mission["theme"] + suffixe)


def annoncer_fin(file_missions, mission):
    """Annonce la FIN d'une mission, avec sa position dans le lot si place."""
    ids, k, total = portee_lot(file_missions)
    extra = {"position": str(k) + "/" + str(total)} if ids else None
    annoncer("fin-mission", mission, extra)
    suffixe = " (round " + str(k) + "/" + str(total) + ")" if ids else ""
    print("FIN mission " + mission["id"] + " -- " + mission["theme"] + suffixe)


def armer_lot(file_missions, ids):
    """Arme le lot : la chaine d'enchainement ne couvrira que ces ids (ordre du lot)."""
    file_missions["lot"] = {"ids": ids, "position": 0}


def lot_termine(file_missions):
    """Retourne True si le lot est arme et qu'aucune de ses missions n'est en attente."""
    ids = ids_en_lot(file_missions)
    return bool(ids) and prochaine_du_lot(file_missions) is None


def bilan_consolide(file_missions):
    """Assemble le bilan consolide du lot depuis l'historique des missions."""
    ids = ids_en_lot(file_missions)
    morceaux = []
    for mission in file_missions.get("missions", []):
        if mission.get("id") in ids:
            morceaux.append(mission["id"] + " [" + mission["theme"] + "] " + mission.get("bilan", "(sans bilan)"))
    return " | ".join(morceaux)


def deposer_message(chemin_boite, message):
    """Depose UN message dans une boite intercom (jsonl en ajout seul)."""
    chemin_boite.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin_boite, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(message, ensure_ascii=True) + "\n")


def journaliser_mission(entree):
    """Ajoute UNE ligne a l'historique des missions (jsonl en ajout seul)."""
    CHEMIN_HISTORIQUE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHEMIN_HISTORIQUE, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")


def charger_entonnoir_pilote():
    """Retourne l'etat de l'entonnoir (echelon 4 : le brin), ou l'etat initial."""
    if not CHEMIN_ENTONNOIR.exists():
        return {"vrac": [], "files": {}, "compteur": 0}
    with open(CHEMIN_ENTONNOIR, "r", encoding=ENCODAGE) as flux:
        return json.load(flux)


def enregistrer_entonnoir_pilote(etat):
    """Ecrit l'etat de l'entonnoir de facon atomique (tmp + remplacement, LF forces)."""
    chemin_tmp = CHEMIN_ENTONNOIR.with_name(NOM_ENTONNOIR + ".tmp")
    with open(chemin_tmp, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(etat, flux, indent=INDENTATION_JSON, ensure_ascii=True)
        flux.write("\n")
    os.replace(chemin_tmp, CHEMIN_ENTONNOIR)


def consommer_tete_tresse(file_missions):
    """Verse la TETE du brin dans la file du pilote (echelon 4 -> serie stricte).

    La mission sort du brin ET de SA file-type (sinon le prochain tisser
    la re-tisserait). REFUS si le pilote a deja une mission en cours.
    Retourne (code, message).
    """
    if mission_en_cours(file_missions) is not None:
        return 1, "REFUS : une mission est deja en cours (serie stricte). Termine-la d'abord."
    etat = charger_entonnoir_pilote()
    brin = etat.get("brin", [])
    if not brin:
        return 0, "Brin vide : rien a verser au pilote (python entonnoir/main.py tresse tisser pour recomposer)."
    tete = brin.pop(0)
    mission = {
        "id": prochain_id(file_missions),
        "theme": tete.get("theme", ""),
        "objectif": tete.get("objectif", ""),
        "type": tete.get("type", ""),
        "statut": STATUT_EN_ATTENTE,
        "chargee_le": horodater(),
        "source": "entonnoir:" + tete.get("id", "E-???") + ":" + tete.get("type", "?") + "/" + tete.get("categorie", "?") + ":" + tete.get("urgence", "?"),
    }
    file_missions.setdefault("missions", []).append(mission)
    for missions_du_type in etat.get("files", {}).values():
        for rang, m in enumerate(missions_du_type):
            if m.get("id") == tete.get("id"):
                del missions_du_type[rang]
                break
    enregistrer_file(file_missions)
    enregistrer_entonnoir_pilote(etat)
    return 0, (
        "Tete du brin verse au pilote : " + mission["id"] + " <- " + tete.get("id", "E-???")
        + " (" + mission["source"] + "). Reste au brin : " + str(len(brin)) + "."
    )


def tisser_tresse():
    """Recompose le brin via la porte officielle de l'entonnoir (sous-processus).

    Un import croise est interdit (modules homonymes, lecon L-009) : le pilote
    orchestre, l'entonnoir reste l'unique source de verite du tressage.
    """
    resultat = subprocess.run(
        [sys.executable, str(CHEMIN_ENTONNOIR.parent / "entonnoir" / "main.py"), "tresse", "tisser"],
        capture_output=True,
        text=True,
        check=False,
    )
    if resultat.returncode != 0:
        print("ALERTE tresse : le tisser a echoue (code " + str(resultat.returncode) + ")")
        if resultat.stderr:
            print(resultat.stderr.strip())


def puiser_tresse(file_missions):
    """    Verse la tete du brin dans la file du pilote (tisser d'abord : brin frais).

    Priorite createur conservee : cette fonction n'est appelee que si ni le lot
    ni la file n'offrent de mission. Retourne la mission venue de la tresse, ou None.
    """
    tisser_tresse()
    code, message = consommer_tete_tresse(file_missions)
    print(message)
    if code != 0:
        return None
    return prochaine_en_attente(file_missions)


def extraire_options(arguments, noms_connus):
    """Extrait les options --nom valeur d'une liste d'arguments (forme seulement)."""
    options = {}
    index = 0
    while index < len(arguments):
        morceau = arguments[index]
        if morceau.startswith("--") and morceau[2:] in noms_connus:
            if index + 1 < len(arguments):
                options[morceau[2:]] = arguments[index + 1]
            index += 2
        else:
            index += 1
    return options
