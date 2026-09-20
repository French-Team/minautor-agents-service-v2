"""Fonctions simples de la categorie coherence : une seule tache chacune.

Croise les DEUX traces d'optimus : la FILE DU PILOTE (ce qu'il a charge) et le
JOURNAL suivi-optimus (ce qui a ete declare). Les deux vivent separement -- le
pilote ecrit la file, c'est l'AGENT qui declare au journal (marbre L-020 : le
pilote ne note RIEN) -- donc rien ne les compare. C'est exactement le trou par
lequel MO-043 est restee 'en-cours' dans la file alors que le journal la disait
finie depuis 40 minutes.

Regle de lecture : un ECART est une divergence A REPARER (la suite bascule en
KO), une DETTE est un etat TRANSITOIRE legitime ou un residu hors perimetre
(signale, jamais bloquant : on ne bloque pas un flux parce qu'un agent est en
train de declarer sa mission).
"""
import json

from constants import (
    ACTION_DEBUT,
    ACTION_FIN,
    CHEMIN_RELATIF_ARCHIVE_PILOTE,
    CHEMIN_RELATIF_BDD,
    CHEMIN_RELATIF_FILE_PILOTE,
    ENCODAGE,
    LONGUEUR_NUMERO,
    PREFIXE_MISSION,
    STATUT_EN_ATTENTE,
    STATUT_EN_COURS,
    STATUT_TERMINEE,
)


def lire_json(chemin):
    """Charge un JSON, ou None si absent/illisible (jamais d'exception)."""
    try:
        with open(str(chemin), "r", encoding=ENCODAGE) as flux:
            return json.load(flux)
    except (OSError, ValueError):
        return None


def lire_evenements(chemin):
    """Charge un journal jsonl ligne a ligne (une ligne cassee est ignoree)."""
    evenements = []
    try:
        with open(str(chemin), "r", encoding=ENCODAGE) as flux:
            for ligne in flux:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    evenements.append(json.loads(ligne))
                except ValueError:
                    continue
    except OSError:
        return []
    return evenements


def numero_mission(identifiant):
    """Numero d'un identifiant MO-NNN, ou None (tout autre prefixe est hors perimetre)."""
    if not isinstance(identifiant, str) or not identifiant.startswith(PREFIXE_MISSION):
        return None
    reste = identifiant[len(PREFIXE_MISSION):]
    return int(reste) if reste.isdigit() else None


def indexer_journal(evenements):
    """Retourne (debuts, fins, hors_perimetre) : ids declares a chaque action.

    hors_perimetre = identifiants NON MO- presents au journal (residus du
    cameleon qui ne concernent pas la file d'optimus) : signales, pas juges.
    """
    debuts, fins, hors_perimetre = set(), set(), set()
    for evenement in evenements:
        mission = evenement.get("mission")
        if not mission:
            continue
        if numero_mission(mission) is None:
            hors_perimetre.add(mission)
            continue
        if evenement.get("action") == ACTION_DEBUT:
            debuts.add(mission)
        elif evenement.get("action") == ACTION_FIN:
            fins.add(mission)
    return debuts, fins, hors_perimetre


def croiser(missions, archivees, debuts, fins):
    """Croise la file (active + archivee) et le journal. Retourne (ecarts, dettes).

    Sept fautes detectees :
      (1) terminee dans la file SANS fin au journal ;
      (2) fin au journal alors que la file n'est PAS terminee ;
      (3) declaree commencee au journal alors que la file la dit en-attente ;
      (4) declaree au journal mais INCONNUE de la file (ni active, ni archivee) ;
      (5) plus d'une mission en cours (la serie stricte est violee) ;
      (6) compteur du pilote en retard sur le plus grand id utilise (un id
          DEJA PRIS serait reattribue a la prochaine charge) ;
      (7) fiche du pilote illisible.
    Et deux dettes (non bloquantes) :
      (a) en cours dans la file sans debut au journal (fenetre d'injection, ou
          declaration oubliee) ;
      (b) identifiants hors perimetre presents au journal.
    """
    ecarts, dettes = [], []

    en_cours = [m for m in missions if m.get("statut") == STATUT_EN_COURS]
    for mission in missions:
        identifiant = mission.get("id")
        if not identifiant or numero_mission(identifiant) is None:
            continue
        statut = mission.get("statut")
        if statut == STATUT_TERMINEE and identifiant not in fins:
            ecarts.append(
                identifiant + " : terminee dans la file, SANS fin au journal"
                + " (la trace ne sait pas que c'est fini)"
            )
        if statut != STATUT_TERMINEE and identifiant in fins:
            ecarts.append(
                identifiant + " : fin au journal, mais encore '" + str(statut)
                + "' dans la file"
            )
        if statut == STATUT_EN_ATTENTE and identifiant in debuts:
            ecarts.append(
                identifiant + " : declaree commencee au journal, mais toujours"
                + " en-attente dans la file (le pilote ne l'a pas chargee)"
            )
        if statut == STATUT_EN_COURS and identifiant not in debuts:
            dettes.append(
                identifiant + " : en cours dans la file, sans debut au journal"
                + " (fenetre d'injection, ou declaration oubliee)"
            )

    connus = {m.get("id") for m in (missions + archivees) if m.get("id")}
    for identifiant in sorted(debuts | fins, key=lambda i: numero_mission(i) or 0):
        if identifiant not in connus:
            ecarts.append(
                identifiant + " : declaree au journal, INCONNUE de la file"
                + " (ni active, ni archivee)"
            )

    if len(en_cours) > 1:
        ecarts.append(
            "serie stricte violee : " + str(len(en_cours)) + " missions en cours"
            + " dans la file (" + ", ".join(m.get("id", "?") for m in en_cours) + ")"
        )
    return ecarts, dettes, connus


def controler_compteur(compteur, connus, debuts, fins):
    """Ecarts du compteur : il doit avoir depasse TOUT id deja utilise.

    C'est le garde-fou de l'id reutilise : le pilote attribue par compteur + 1,
    donc un compteur en retard reattribue un identifiant DEJA PRIS (cas reel
    MO-045 / MO-046, 2026-09-13).
    """
    numeros = [n for n in (numero_mission(i) for i in (connus | debuts | fins)) if n]
    if not numeros:
        return []
    plus_grand = max(numeros)
    if compteur >= plus_grand:
        return []
    prochain = PREFIXE_MISSION + str(compteur + 1).zfill(LONGUEUR_NUMERO)
    return [
        "compteur " + str(compteur) + " < plus grand id deja utilise (" + str(plus_grand)
        + ") : la prochaine charge reattribuerait " + prochain + " (id deja pris)"
    ]


def controler(matrice):
    """Croise la file du pilote et le journal. Retourne (ecarts, dettes, resume)."""
    chemin_file = matrice / CHEMIN_RELATIF_FILE_PILOTE
    chemin_archive = matrice / CHEMIN_RELATIF_ARCHIVE_PILOTE
    chemin_journal = matrice / CHEMIN_RELATIF_BDD

    file_pilote = lire_json(chemin_file)
    if file_pilote is None:
        return ["fiche du pilote illisible ou absente : " + str(chemin_file)], [], ""
    evenements = lire_evenements(chemin_journal)
    if not evenements:
        return ["journal illisible ou vide : " + str(chemin_journal)], [], ""

    missions = [m for m in (file_pilote.get("missions") or []) if m.get("id")]
    archive = lire_json(chemin_archive) or {}
    archivees = [m for m in (archive.get("missions") or []) if m.get("id")]
    debuts, fins, hors_perimetre = indexer_journal(evenements)

    ecarts, dettes, connus = croiser(missions, archivees, debuts, fins)
    ecarts += controler_compteur(int(file_pilote.get("compteur") or 0), connus, debuts, fins)
    if hors_perimetre:
        dettes.append(
            str(len(hors_perimetre)) + " identifiant(s) hors perimetre au journal"
            + " (prefixe autre que " + PREFIXE_MISSION + ", residus du cameleon) :"
            + " " + ", ".join(sorted(hors_perimetre)[:5])
        )

    resume = (
        "file : " + str(len(missions)) + " active(s) + " + str(len(archivees))
        + " archivee(s), compteur " + str(file_pilote.get("compteur"))
        + " | journal : " + str(len(evenements)) + " evenement(s), "
        + str(len(debuts)) + " debut(s), " + str(len(fins)) + " fin(s)"
    )
    return ecarts, dettes, resume
