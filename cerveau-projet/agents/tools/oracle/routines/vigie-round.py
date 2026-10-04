#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine vigie-round -- Detection des rounds casses (v1, session-admin).

Decision utilisateur 2026-08-28 : LES DEUX EN CASCADE - detection
(routine vigie) + prevention (blocages mecaniques). Cette routine est la
partie DETECTION : elle surveille en continu et ALERTE Cerberus quand un
round semble casse, en LECTURE SEULE (jamais de correction automatique).

Elle detecte :
  1. SESSION ORPHELINE : un agent actif (non cerberus) sans activite
     historisee depuis X minutes alors qu il a une mission en cours
     (source : classeur profil-session-admin + tableau Activites recentes).
  2. CHAINE EN ATTENTE : un agent actif dont l etat de carte (etat-cartes)
     indique etape=fin depuis X minutes sans que le round n avance
     (personne n a reactive Cerberus).

Alerte : ecrit dans l inbox Oracle de Cerberus (format 4W : qui, quoi,
quand, ou), meme canal que le harnais Oracle (harnais_oracle.py).

Usage:
    python3 vigie-round.py [--seuil-minutes N] [--dry-run] [--no-chrono]

Retour: 0 si succes (alerte envoyee ou rien a signaler), 1 si erreur.
"""

import io
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

VERSION = "0.1.0"

# Dossier de cette routine : oracle/routines/
_DOSSIER = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = Path(_DOSSIER).parent
INBOX_DIR = ORACLE_DIR / "inbox"
def _rotation_ajouter(agent, message):
    """Rotation inbox : garder les 5 messages les plus recents (decision
    utilisateur 2026-08-29 : les inbox s accumulaient, personne ne les
    lisait). Reutilise le module central oracle/fonctions/rotation.py."""
    try:
        import importlib.util
        _f = Path(_DOSSIER).parent / "fonctions" / "rotation.py"
        _spec = importlib.util.spec_from_file_location("rotation", str(_f))
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        return _mod.ajouter_message(INBOX_DIR, agent, message)
    except Exception:
        return False

ETAT_CARTES_DIR = ORACLE_DIR / "etat-cartes"

SEUIL_MINUTES_DEFAUT = 10
# Anti-spam : ne pas re-alerter le meme cas avant ce delai (minutes)
ALERTE_REPETITION_MINUTES = 30
_ETAT_VIGIE = Path(_DOSSIER) / "etat-vigie.json"


def _racine_projet():
    """Racine du projet (la ou vivent AGENTS-historique.md et
    AGENTS-activite-recente.md). Remonte depuis routines/ jusqu a trouver
    le fichier historique. Independante du cwd (le daemon lance ce script
    avec cwd=routines/)."""
    racine = Path(_DOSSIER)
    while not (racine / "AGENTS-historique.md").is_file():
        if racine.parent == racine:
            return Path.cwd()
        racine = racine.parent
    return racine


def _lire_fichier(chemin):
    """Lire un fichier texte (retourne '' si absent/illisible)."""
    try:
        return Path(chemin).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _lire_classeur_agent_actif():
    """Lire l agent actif depuis le classeur (profil-session-admin).
    Retourne (agent, date) ou (None, None) si introuvable."""
    racine = _racine_projet()
    classeur = racine / "cerveau-projet" / "agents" / "classeur-variables" / \
        "stockage" / "variables-actuelles.md"
    contenu = _lire_fichier(classeur)
    for ligne in contenu.split("\n"):
        if "profil-session-admin" not in ligne:
            continue
        # ligne : | `profil-session-admin` | session: session-admin / id: glm5 / agent: vulcain / date: ... |
        agent = None
        date = None
        for partie in ligne.split("/"):
            p = partie.strip()
            if p.startswith("agent:"):
                agent = p.split(":", 1)[1].strip()
            elif p.startswith("date:"):
                date = p.split(":", 1)[1].strip()
        return agent, date
    return None, None


def _derniere_activite(agent):
    """Heure de la derniere entree de l agent dans le tableau
    Activites recentes (aujourd hui). Retourne un datetime ou None."""
    racine = _racine_projet()
    activite = racine / "AGENTS-activite-recente.md"
    contenu = _lire_fichier(activite)
    dernier_heure = None
    for ligne in contenu.split("\n"):
        if not ligne.startswith("| "):
            continue
        cellules = [c.strip() for c in ligne.split("|")]
        # | Grade | Agent | Defcon | Executeur | Etat | Secteur | Raison | Heure | id | Type |
        # Le prefixe vide du tableau fait decaler les colonnes d un rang :
        # Agent=[2], Raison=[7], Heure=[8]. <8 -> <9 pour pouvoir lire [8].
        if len(cellules) < 9:
            continue
        nom_agent = cellules[2]
        if nom_agent.lower() != agent.lower():
            continue
        heure = cellules[8]
        try:
            h = datetime.strptime(heure[:8], "%H:%M:%S")
        except ValueError:
            continue
        if dernier_heure is None or h > dernier_heure:
            dernier_heure = h
    if dernier_heure is None:
        return None
    maintenant = datetime.now()
    return maintenant.replace(hour=dernier_heure.hour,
                              minute=dernier_heure.minute,
                              second=dernier_heure.second,
                              microsecond=0)


def _etat_carte(agent):
    """Lire l etat de carte de l agent (dict vide si absent)."""
    chemin = ETAT_CARTES_DIR / ("%s.json" % agent)
    if not chemin.is_file():
        return {}
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def _ecrire_alerte(ecarts):
    """Ecrire une alerte dans l inbox d Oracle (coordinateur, qui avise
    ensuite) - decision utilisateur 2026-08-30 : les routines previennent
    Oracle et pas Cerberus (modele aero : Oracle coordonne)."""
    if not ecarts:
        return None
    maintenant = datetime.now()
    message = {
        "id": "vigie-%s" % maintenant.strftime("%H%M%S"),
        "de": "vigie-round",
        "vers": "oracle",
        "priorite": 1,
        "date": maintenant.strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[VIGIE-ROUND] %d round(s) casse(s) detecte(s)" % len(ecarts),
        "corps": "\n".join("- %s" % e for e in ecarts),
        "lu": False,
        "accuse": False,
        "type": "vigie-round",
    }
    try:
        _rotation_ajouter("oracle", message)
    except OSError as exc:
        print("[VIGIE-ROUND] ERREUR ecriture alerte : %s" % exc)
        return None
    return message


def _charger_etat_vigie():
    """Charger l etat des alertes deja envoyees (anti-spam)."""
    if not _ETAT_VIGIE.is_file():
        return {}
    try:
        return json.loads(_ETAT_VIGIE.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def _sauver_etat_vigie(etat):
    """Sauvegarder l etat des alertes envoyees."""
    try:
        with io.open(_ETAT_VIGIE, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(etat, ensure_ascii=True, indent=1))
    except OSError:
        pass


def detecter(seuil_minutes=SEUIL_MINUTES_DEFAUT):
    """Scan complet : retourne la liste des ecarts (messages 4W)."""
    ecarts = []
    agent, date = _lire_classeur_agent_actif()
    if not agent:
        return ecarts

    # CAS NORMAL : Cerberus actif en accueil (attente utilisateur) -> jamais d alerte
    if agent.lower() == "cerberus":
        return ecarts

    maintenant = datetime.now()
    # 1. SESSION ORPHELINE : agent actif (non cerberus) sans activite
    #    depuis seuil_minutes.
    dernier = _derniere_activite(agent)
    age_minutes = None
    if dernier is not None:
        age_minutes = (maintenant - dernier).total_seconds() / 60.0
    if age_minutes is None or age_minutes >= seuil_minutes:
        duree = "aucune activite aujourd hui" if age_minutes is None else \
            "%.0f minutes" % age_minutes
        ecarts.append(
            "[session-orpheline] QUI: %s - QUOI: agent actif sans activite "
            "depuis %s - QUAND: derniere trace %s - OU: session-admin "
            "(mission en cours non executee)" % (
                agent, duree, (dernier.strftime("%H:%M:%S") if dernier else "inconnue")))

    # 2. CHAINE EN ATTENTE : etat de carte a etape=fin (le round est
    #    termine mais personne n a reactive Cerberus).
    etat = _etat_carte(agent)
    if etat.get("etape") == "fin" and age_minutes is not None and \
            age_minutes >= seuil_minutes:
        ecarts.append(
            "[chaine-en-attente] QUI: %s - QUOI: etat de carte a etape=fin "
            "depuis %.0f minutes, Cerberus non reactive - QUAND: %s - OU: "
            "etat-cartes/%s.json (fin de chaine Pattern 13 non executee)" % (
                agent, age_minutes, maintenant.strftime("%H:%M:%S"), agent))
    return ecarts


def main():
    # --- OPTIONS (triplet : protections + options on/off + chrono) ---
    seuil = SEUIL_MINUTES_DEFAUT
    dry_run = False
    chrono_actif = "--no-chrono" not in sys.argv
    t_debut = time.monotonic()
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--seuil-minutes" and i + 1 < len(args):
            try:
                seuil = int(args[i + 1])
            except ValueError:
                pass
        if arg == "--dry-run":
            dry_run = True
    if seuil < 1:
        seuil = SEUIL_MINUTES_DEFAUT

    if chrono_actif:
        print("[CHRONO] vigie-round (debut)")
    ecarts = detecter(seuil_minutes=seuil)

    if not ecarts:
        print("[VIGIE-ROUND] Aucun round casse - la v1 se comporte bien.")
        return 0

    print("[VIGIE-ROUND] %d round(s) casse(s) detecte(s) :" % len(ecarts))
    for e in ecarts:
        print("  - %s" % e)
    # Anti-spam : ne pas re-alerter le meme cas (memes cles) avant
    # ALERTE_REPETITION_MINUTES (sinon la vigie spammerait l inbox de
    # Cerberus toutes les 60 s tant que le cas n est pas resolu).
    cles = sorted(e.split("]")[0].strip("[") for e in ecarts)
    etat = _charger_etat_vigie()
    repetition = False
    if cles == etat.get("cles", []) and etat.get("date"):
        try:
            d = datetime.strptime(str(etat["date"])[:19], "%Y-%m-%dT%H:%M:%S")
            age = (datetime.now() - d).total_seconds() / 60.0
            repetition = age < ALERTE_REPETITION_MINUTES
        except ValueError:
            repetition = False
    if repetition:
        print("[VIGIE-ROUND] Meme cas deja alerte il y a moins de %d min "
              "- pas de nouvelle alerte anti-spam." % ALERTE_REPETITION_MINUTES)
        return 0
    if dry_run:
        print("[VIGIE-ROUND] --dry-run : alerte NON envoyee a Oracle.")
    else:
        msg = _ecrire_alerte(ecarts)
        if msg:
            print("[VIGIE-ROUND] Alerte envoyee a Oracle (%s)" % msg["id"])
            _sauver_etat_vigie({"cles": cles, "date":
                                datetime.now().strftime("%Y-%m-%dT%H:%M:%S")})
        else:
            print("[VIGIE-ROUND] ERREUR : alerte non envoyee.")
            return 1
    if chrono_actif:
        print("[CHRONO] vigie-round (fin, %.1fs)" % (time.monotonic() - t_debut))
    return 0


if __name__ == "__main__":
    sys.exit(main())
