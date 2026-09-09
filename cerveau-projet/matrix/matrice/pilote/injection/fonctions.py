"""Fonctions simples de la categorie injection : une seule tache chacune."""
import json

from commun import (
    annoncer,
    annoncer_debut,
    armer_lot,
    bilan_consolide,
    defcon_bloque_theme,
    deposer_message,
    enregistrer_file,
    horodater,
    ids_en_lot,
    mission_en_cours,
    prochaine_du_lot,
    prochaine_en_attente,
    puiser_tresse,
    session_en_pause,
    journaliser_mission,
)
from checklist.stockage import fabrique_checklist
from constants import (
    BOITE_PILOTE_OUT,
    CHEMIN_THEMES,
    ENCODAGE,
    REPERTOIRE_DATA,
    STATUT_EN_ATTENTE,
    STATUT_EN_COURS,
)


def afficher_statut(file_missions):
    """Affiche l'etat de la mission en cours (ou l'absence de mission en cours)."""
    mission = mission_en_cours(file_missions)
    if mission is None:
        en_attente = sum(1 for m in file_missions.get("missions", []) if m.get("statut") == STATUT_EN_ATTENTE)
        print("Aucune mission en cours. File : " + str(en_attente) + " en attente.")
        return 0
    print("Mission en cours : " + mission["id"] + " (theme : " + mission["theme"] + ") -- " + mission["objectif"])
    return 0


def preparer_injection(charger_file):
    """Prepare et depose l'injection ordonnee de la mission suivante.

    Serie stricte : REFUS si une mission est deja en cours.
    Protocole de pause (M-080) : REFUS si la session-matrix est EN PAUSE.
    Priorite au createur : 1) le lot arme, 2) la file des missions chargees,
    3) la TRESSE (puisage automatique : tisser si besoin, puis tete du brin).
    """
    if session_en_pause():
        print("REFUS : session-matrix EN PAUSE (protocole M-080) -- aucune injection pendant la maintenance.")
        print("(reprise par l'outil pause-session, verbe reprendre, apres maintenance user + optimus)")
        return 1
    file_missions = charger_file()
    if mission_en_cours(file_missions) is not None:
        print("REFUS : une mission est deja en cours (serie stricte). Termine-la d'abord : python main.py fin --bilan ...")
        return 1
    mission = prochaine_du_lot(file_missions) or prochaine_en_attente(file_missions)
    if mission is None:
        mission = puiser_tresse(file_missions)
    if mission is None:
        print("Aucune mission en attente (lot, file et tresse vides).")
        return 0
    code, message = defcon_bloque_theme(mission.get("theme", ""))
    if code != 0:
        print(message)
        print("(mission " + mission["id"] + " laissee en attente pendant la mise en securite)")
        return code

    checklist = mission.get("checklist") or fabrique_checklist(mission.get("type") or mission.get("theme", ""))
    injection = {
        "type": "injection",
        "date": horodater(),
        "mission": mission["id"],
        "theme": mission["theme"],
        "objectif": mission["objectif"],
        "checklist": checklist,
        "lecons_utiles": charger_lecons_utiles(),
        "themes_utiles": charger_themes_utiles(),
    }
    deposer_message(BOITE_PILOTE_OUT, injection)

    mission["statut"] = STATUT_EN_COURS
    mission["injectee_le"] = horodater()
    mission["checklist"] = checklist
    enregistrer_file(file_missions)
    annoncer_debut(file_missions, mission)
    print("Injection deposee pour " + mission["id"] + " -> " + str(BOITE_PILOTE_OUT))
    return 0


def enchainer(charger_file):
    """Arme le round multiple : la premiere mission du lot passe en cours.

    Ensuite, chaque `fin` declenche automatiquement la mission suivante du lot
    (annonce FIN puis DEBUT), jusqu'au RETOUR consolide a la Matrice quand
    toutes les missions du lot sont terminees.
    Protocole de pause (M-080) : REFUS si la session-matrix est EN PAUSE.
    """
    if session_en_pause():
        print("REFUS : session-matrix EN PAUSE (protocole M-080) -- aucun enchainement pendant la maintenance.")
        return 1
    file_missions = charger_file()
    if mission_en_cours(file_missions) is not None:
        print("REFUS : une mission est deja en cours (serie stricte).")
        return 1
    if not ids_en_lot(file_missions):
        print('Aucun lot arme. Chargez-en un : python main.py lot --lot "nom" --theme "t1,t2" --objectif "o1|o2"')
        return 1
    mission = prochaine_du_lot(file_missions)
    if mission is None:
        print("Le lot est deja termine (aucune mission en attente dans le lot).")
        return 0

    checklist = mission.get("checklist") or fabrique_checklist(mission.get("type") or mission.get("theme", ""))
    injection = {
        "type": "injection",
        "date": horodater(),
        "mission": mission["id"],
        "theme": mission["theme"],
        "objectif": mission["objectif"],
        "lot": True,
        "checklist": checklist,
        "lecons_utiles": charger_lecons_utiles(),
        "themes_utiles": charger_themes_utiles(),
    }
    deposer_message(BOITE_PILOTE_OUT, injection)

    mission["statut"] = STATUT_EN_COURS
    mission["checklist"] = checklist
    mission["injectee_le"] = horodater()
    enregistrer_file(file_missions)
    annoncer_debut(file_missions, mission)
    print("Chaine armee : chaque 'fin' enchainra la mission suivante du lot.")
    return 0


def charger_lecons_utiles():
    """Charge les lecons de la BDD lecons.json (liste vide si absente ou illisible).

    BDD en cours de construction : jamais de faux blocage, jamais de type surprenant.
    Format prevu (contrat data) : {"lecons": [{...tags...}, ...]}.
    """
    chemin_lecons = REPERTOIRE_DATA / "lecons.json"
    if not chemin_lecons.exists():
        return []
    try:
        with open(chemin_lecons, "r", encoding=ENCODAGE) as flux:
            donnees = json.load(flux)
        return donnees.get("lecons", []) if isinstance(donnees, dict) else []
    except (OSError, ValueError):
        return []


def charger_themes_utiles():
    """Charge les themes du registre vivier-themes.json (liste vide si absent).

    Meme doctrine que lecons_utiles : garde jamais bloquant, type toujours sur.
    Format (moule theme-bdd) : {"themes": [{"id", "nom", "but", ...}, ...]}.
    """
    if not CHEMIN_THEMES.exists():
        return []
    try:
        with open(CHEMIN_THEMES, "r", encoding=ENCODAGE) as flux:
            donnees = json.load(flux)
        return donnees.get("themes", []) if isinstance(donnees, dict) else []
    except (OSError, ValueError):
        return []
