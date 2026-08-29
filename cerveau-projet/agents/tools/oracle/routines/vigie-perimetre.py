#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine vigie-perimetre -- Guetteuse des modifications du perimetre
Oracle (v1, session-admin).

Transposee de la routine v2 vigie (ex-surveiller-modifications,
surveillance/vigie.py + detection.py) pour l univers v1 (decision
utilisateur 2026-08-29 : creer les routines v1 inspirees des v2, sans
recuperer leur code - 2 univers distincts).

Surveille le perimetre Oracle (le dossier routines/ et les serveurs) par
empreintes SHA-256, compare a un etat persistant (etat-empreintes.json),
et alerte Cerberus au format 4W quand un fichier surveille change.

Perimetre : manifest.json, section perimetre_surveille (editable sans
toucher au code). Exclusions par defaut : etat-executions.json (reecrit
par le daemon a chaque tic), les fichiers d etat des routines
(.flux_derniere.txt, .notation_derniere.txt, etat-empreintes.json) et
les dossiers volatils (data/, observations/, __pycache__).

LECTURE SEULE + alerte : ne corrige jamais, elle signale.

Usage:
    python3 vigie-perimetre.py [--dry-run] [--no-chrono]

Retour: 0 si succes (rien de modifie ou alerte envoyee), 1 si erreur.
"""

import hashlib
import io
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = Path(_DOSSIER).parent
INBOX_DIR = ORACLE_DIR / "inbox"
MANIFEST = ORACLE_DIR / "routines" / "manifest.json"
ETAT_EMPREINTES = Path(_DOSSIER) / "etat-empreintes.json"

# Dossiers/fichiers volatils jamais surveillables (reecrits en continu).
DOSSIERS_EXCLUS = {"__pycache__", "data", "observations", "inbox", "outbox",
                   "files", "etat-cartes", "historique"}
FICHIERS_EXCLUS = {"etat-executions.json", "etat-vigie.json",
                   "etat-empreintes.json", ".flux_derniere.txt",
                   ".notation_derniere.txt"}


def _racine_projet():
    racine = Path(_DOSSIER)
    while not (racine / "AGENTS-historique.md").is_file():
        if racine.parent == racine:
            return Path.cwd()
        racine = racine.parent
    return racine


def _historiser_agent(agent, raison, type_action="R"):
    """Helper d historisation (meme que flux.py)."""
    import importlib.util
    import os as _os
    aap_path = ORACLE_DIR.parent / "activer" / "activer-agent-principal" / \
        "activer-agent-principal.py"
    if not aap_path.exists():
        return False
    racine = _racine_projet()
    _os.environ["AGENTS_HISTORIQUE"] = str(racine / "AGENTS-historique.md")
    _os.environ["AGENTS_ACTIVITE_RECENTE"] = str(
        racine / "AGENTS-activite-recente.md")
    _os.environ["AGENTS_FILE"] = str(racine / "AGENTS.md")
    _os.environ["CLASSEUR_STOCKAGE"] = str(
        racine / "cerveau-projet" / "agents" / "classeur-variables" /
        "stockage" / "variables-actuelles.md")
    _os.environ["GRADES_V1"] = str(
        racine / "cerveau-projet" / "agents" / "tools" / "oracle" /
        "grades-v1.json")
    _bdd_dir = (racine / "cerveau-projet" / "freelance" / "tools-commun" /
                "jarvis" / "fonctions")
    if str(_bdd_dir) not in sys.path:
        sys.path.insert(0, str(_bdd_dir))
    spec = importlib.util.spec_from_file_location("aap_v1", str(aap_path))
    aap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aap)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    rc = aap.ajouter_historique(ts, "session-admin", agent, raison,
                                type_action)
    return rc == 0


def _ecrire_alerte(details, motif):
    """Alerte Cerberus au format 4W (canal inbox Oracle, type vigie-perimetre)."""
    maintenant = datetime.now()
    message = {
        "id": "vigie-perimetre-%s" % uuid.uuid4().hex[:8],
        "de": "vigie-perimetre",
        "vers": "cerberus",
        "priorite": 1,
        "date": maintenant.strftime("%Y-%m-%dT%H:%M:%S"),
        "objet": "[VIGIE-PERIMETRE] perimetre modifie : " + motif[:40],
        "corps": details,
        "lu": False,
        "accuse": False,
        "type": "vigie-perimetre",
    }
    try:
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        with open(INBOX_DIR / "cerberus.jsonl", "a",
                  encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")
        return message
    except OSError as exc:
        print("[VIGIE-PERIMETRE] ERREUR ecriture alerte : %s" % exc)
        return None


def _empreinte(fichier):
    """Empreinte SHA-256 du fichier."""
    h = hashlib.sha256()
    with open(fichier, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def _perimetre():
    """Liste des chemins a surveiller (manifest, section perimetre_surveille)."""
    if not MANIFEST.is_file():
        return []
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        return data.get("perimetre_surveille", [])
    except (ValueError, OSError):
        return []


def _survoler(racine_projet):
    """Enumere les fichiers surveilles : (chemin_absolu, cle_relat).

    Pour chaque entree du perimetre :
      - un dossier : walk recursif (exclusions volatiles) ;
      - un fichier : surveille directement.
    cle_relat = chemin relatif a la racine du projet (stable dans l etat).
    """
    fichiers = []
    for relatif in _perimetre():
        base = Path(racine_projet) / relatif
        if base.is_dir():
            for courant, dossiers, noms in os.walk(str(base)):
                dossiers[:] = [d for d in dossiers
                               if d not in DOSSIERS_EXCLUS]
                for nom in noms:
                    if nom in FICHIERS_EXCLUS:
                        continue
                    reel = os.path.join(courant, nom)
                    fichiers.append((reel, os.path.relpath(reel,
                                                           racine_projet)))
        elif base.is_file():
            fichiers.append((str(base), relatif))
    return fichiers


def _qui_par_git(rel_ws, racine_projet):
    """Dernier auteur ayant commite le fichier (inconnu sinon)."""
    try:
        flags = 0
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            flags = subprocess.CREATE_NO_WINDOW
        p = subprocess.run(
            ["git", "log", "-1", "--format=%an %ad", "--", rel_ws],
            capture_output=True, text=True, cwd=str(racine_projet),
            timeout=10, creationflags=flags)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "inconnu (modification non commitee)"


def main():
    dry_run = "--dry-run" in sys.argv
    chrono_actif = "--no-chrono" not in sys.argv
    t_debut = time.monotonic()
    if chrono_actif:
        print("[CHRONO] vigie-perimetre (debut)")

    racine = _racine_projet()
    etat = {}
    if ETAT_EMPREINTES.is_file():
        try:
            etat = json.loads(ETAT_EMPREINTES.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            etat = {}
    # Hygiene : purger les empreintes de fichiers qui n existent plus.
    etat = {k: v for k, v in etat.items()
            if os.path.exists(os.path.join(str(racine), k))}

    fichiers = _survoler(racine)
    modifications = []
    for reel, cle in fichiers:
        empreinte_actuelle = _empreinte(reel)
        if etat.get(cle) and etat[cle] != empreinte_actuelle:
            rel_ws = cle.replace("\\", "/")
            qui = _qui_par_git(rel_ws, racine)
            modifications.append(
                "[perimetre-modifie] QUI: %s - QUOI: %s modifie - "
                "QUAND: %s - OU: empreinte SHA-256 changee "
                "(etat-empreintes.json)" % (
                    qui, rel_ws,
                    datetime.now().strftime("%Y-%m-%dT%H:%M:%S")))
        etat[cle] = empreinte_actuelle

    if not modifications:
        print("[VIGIE-PERIMETRE] Aucune modification du perimetre.")
        if not dry_run:
            _sauver_etat(etat)
        if chrono_actif:
            print("[CHRONO] vigie-perimetre (fin, %.1fs)"
                  % (time.monotonic() - t_debut))
        return 0

    print("[VIGIE-PERIMETRE] %d modification(s) du perimetre :"
          % len(modifications))
    for m in modifications:
        print("  - %s" % m)
    if dry_run:
        print("[VIGIE-PERIMETRE] --dry-run : alerte NON envoyee, "
              "etat non sauve.")
        if chrono_actif:
            print("[CHRONO] vigie-perimetre (fin, %.1fs)"
                  % (time.monotonic() - t_debut))
        return 1
    corps = "\n".join("- %s" % m for m in modifications)
    msg = _ecrire_alerte(corps, modifications[0].split("QUOI: ")[1][:60]
                         if "QUOI: " in modifications[0] else "perimetre")
    _sauver_etat(etat)
    _historiser_agent("vigie-perimetre",
                      "%d modification(s) perimetre: %s" % (
                          len(modifications),
                          "; ".join(m.split("QUOI: ")[1].split(" - QUAND:")[0]
                                    for m in modifications[:2])), "R")
    if msg:
        print("[VIGIE-PERIMETRE] Alerte envoyee a Cerberus (%s)" % msg["id"])
    if chrono_actif:
        print("[CHRONO] vigie-perimetre (fin, %.1fs)"
              % (time.monotonic() - t_debut))
    return 0 if msg else 1


def _sauver_etat(etat):
    """Sauvegarder l etat des empreintes (LF, trie)."""
    try:
        with io.open(ETAT_EMPREINTES, "w", encoding="utf-8",
                     newline="\n") as fh:
            fh.write(json.dumps(etat, ensure_ascii=True,
                                indent=1, sort_keys=True))
    except OSError:
        pass


if __name__ == "__main__":
    sys.exit(main())