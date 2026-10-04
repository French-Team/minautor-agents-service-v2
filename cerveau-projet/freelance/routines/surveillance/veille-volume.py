# -*- coding: ascii -*-
"""routine : veille-volume -- surveille le volume des files JSONL JARVIS
(inbox/outbox/files) et alerte [EDITH-REVEIL] quand un fichier grossit
au-dela des seuils (volume des messages, pas des octets lus par l'LLM).

Contexte 2026-08-29 : l'audit de non-corruption des inbox/outbox v1 + v2
a revele des fichiers v2 volumineux (inbox/stark.jsonl ~2,2 Mo ~2676
messages, inbox/jarvis.jsonl ~1,6 Mo ~2230 messages) - cumuls LEGITIMES
de chaque tic de routine, mais sans borne. Cette routine surveille la
croissance et reveille EDITH quand un fichier depasse les seuils, pour
qu'une rotation/purge soit decidee avant tout probleme de place.

LECTURE SEULE : ne modifie JAMAIS les files surveillees - elle les
mesure et alerte. Anti-spam : un fichier en alerte ne reveille qu une
fois (etat persistant), re-arme quand il repasse sous le seuil.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# P10 : racine DETECTEE en remontant jusqu'a AGENTS.md (jamais compte)
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)

JARVIS_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "jarvis"
OBS_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
    / "routines-server" / "observations"

# Seuils (octets et messages) -- ajustables sans toucher au code
SEUIL_OCTETS = 1_500_000      # 1,5 Mo par fichier JSONL
SEUIL_MESSAGES = 2500         # 2500 messages par fichier JSONL

# Fichier d etat persistant (anti-spam : un fichier en alerte ne
# reveille qu une fois, re-arme quand il repasse sous le seuil)
_ETAT = Path(__file__).parent / ".veille-volume-etat.json"


def _charger_etat():
    if not _ETAT.exists():
        return {}
    try:
        return json.loads(_ETAT.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _sauver_etat(etat):
    _ETAT.write_text(json.dumps(etat, ensure_ascii=False), encoding="utf-8")


def _mesurer(fichier):
    """Retourne (octets, nb_messages). Lecture seule."""
    octets = fichier.stat().st_size
    nb = 0
    try:
        with open(fichier, "r", encoding="utf-8") as fh:
            for ligne in fh:
                if ligne.strip():
                    nb += 1
    except (OSError, UnicodeDecodeError):
        pass
    return octets, nb


def _alerter(details):
    """Deposer un message P1 [EDITH-REVEIL] dans le hub (inbox/jarvis.jsonl)
    + trace outbox/edith (protocole 18 : EDITH incarnee rapporte les 4 W)."""
    import uuid
    base = {
        "de": "edith", "priorite": 1,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[EDITH-REVEIL] volume file JARVIS depasse le seuil",
        "corps": ("DEMANDE D'ACTIVATION EDITH (protocole 18). EDITH doit "
                  "etre activee pour analyser les 4 W.\n" + details),
        "lu": False, "accuse": False, "type": "reveil",
    }
    for destinataire in ("jarvis",):
        msg = dict(base)
        msg["id"] = str(uuid.uuid4())[:8]
        msg["vers"] = destinataire
        msg_out = dict(msg)
        msg_out["lu"] = True
        msg_out["accuse"] = True
        for cible in (JARVIS_DIR / "inbox" / ("%s.jsonl" % destinataire),
                      JARVIS_DIR / "outbox" / "edith.jsonl"):
            cible.parent.mkdir(parents=True, exist_ok=True)
            ecrit = msg if "inbox" in str(cible) else msg_out
            with open(cible, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(ecrit, ensure_ascii=False) + "\n")
    # Trace dans l activite recente v2 (sous le nom de la routine)
    try:
        _fo = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
            / "os_path" / "fonctions"
        _fj = JARVIS_DIR / "fonctions"
        for p in (_fo, _fj):
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
        from historique import historiser
        historiser("veille-volume", "Volume file JARVIS depasse le seuil",
                   "R", session="session-freelance")
    except Exception:
        pass


def main():
    zones = [
        ("inbox", JARVIS_DIR / "inbox"),
        ("outbox", JARVIS_DIR / "outbox"),
        ("files", JARVIS_DIR / "files"),
    ]
    etat = _charger_etat()
    nouvelles_alertes = []

    for nom_zone, dossier in zones:
        if not dossier.exists():
            continue
        for fichier in sorted(dossier.glob("*.jsonl")):
            octets, nb = _mesurer(fichier)
            cle = "%s/%s" % (nom_zone, fichier.name)
            depasse = octets > SEUIL_OCTETS or nb > SEUIL_MESSAGES
            deja_alerte = etat.get(cle, False)
            if depasse and not deja_alerte:
                nouvelles_alertes.append(cle)
                rel_ws = str(fichier).replace(str(RACINE) + os.sep, "")\
                    .replace("\\", "/")
                details = (
                    "QUI: veille-volume | QUOI: %s a depasse le seuil | "
                    "COMMENT: %d octets (%d messages), seuils %d octets / "
                    "%d messages | QUAND: %s" % (
                        rel_ws, octets, nb, SEUIL_OCTETS, SEUIL_MESSAGES,
                        datetime.now(timezone.utc).isoformat()))
                # Observation ecrite (trace, lecture seule sur les files)
                try:
                    OBS_DIR.mkdir(exist_ok=True)
                    obs = OBS_DIR / ("observation-volume-%s.md"
                                     % datetime.now().strftime("%Y%m%d-%H%M%S"))
                    obs.write_text("# Observation - volume file depasse\n\n"
                                   + details + "\n", encoding="utf-8")
                except OSError:
                    pass
                _alerter(details)
                print("[VEILLE-VOLUME] ALERTE : %s (%d octets, %d messages)"
                      % (cle, octets, nb))
            elif not depasse and deja_alerte:
                print("[VEILLE-VOLUME] %s repasse sous le seuil (re-armement)"
                      % cle)
            etat[cle] = depasse

    _sauver_etat(etat)
    if nouvelles_alertes:
        print("[VEILLE-VOLUME] %d nouvelle(s) alerte(s) : %s"
              % (len(nouvelles_alertes), ", ".join(nouvelles_alertes)))
    else:
        print("[VEILLE-VOLUME] Aucun fichier au-dela des seuils")
    return 0


if __name__ == "__main__":
    sys.exit(main())
