# -*- coding: utf-8 -*-
"""fonctions/routines.py - UNE tache : executer les routines dont
l'intervalle est ecoule, a CHAQUE invocation de jarvis (protocole 16,
decision utilisateur : plus de processus d'arriere-plan a faire vivre -
jarvis est appele en permanence donc les routines tournent naturellement).

Reference de temps : tools-commun/horloge (decision utilisateur).
Tolerance EDITH : pas a la minute pres - l'interval elargira plus tard.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "horloge", "fonctions")
sys.path.insert(0, _sys_dir)
# P10 : le module racine vit dans os_path - le chemin s'insere ICI,
# avant l'import (sinon dependance cachee a l'ordre des imports).
_sys_dir_racine = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir_racine)
from horloge import maintenant  # noqa: E402
from racine import trouver_racine

RACINE = Path(trouver_racine(__file__))
FREELANCE = RACINE / "cerveau-projet" / "freelance"
MANIFEST = FREELANCE / "routines" / "manifest.json"
ETAT = FREELANCE / "routines" / "etat-executions.json"


def charger_etat():
    if ETAT.exists():
        try:
            return json.loads(ETAT.read_text(encoding="utf-8"))
        except ValueError:
            return {}
    return {}


def sauver_etat(etat):
    ETAT.parent.mkdir(parents=True, exist_ok=True)
    ETAT.write_text(json.dumps(etat, ensure_ascii=False), encoding="utf-8")


def secondes_ecoulee(iso_derniere):
    """Secondes ecoulees depuis un horodatage horloge (ISO UTC).
    Tolerance EDITH : si illisible, on considere 'longtemps'."""
    try:
        derniere = datetime.strptime(iso_derniere, "%Y-%m-%dT%H:%M:%S")
        return (datetime.utcnow() - derniere).total_seconds()
    except (ValueError, TypeError):
        return 10**9


def infos_routines():
    """Lister les routines du manifest :
    [(nom, script_path, intervalle_secondes, actif), ...]"""
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    resultat = []
    for routine in manifest.get("routines_surveillance", []):
        intervalle = routine.get(
            "intervalles_secondes",
            manifest.get("intervalle_boucle_secondes", 600))
        resultat.append((routine.get("nom"),
                         FREELANCE / "routines" / routine.get("script", ""),
                         int(intervalle),
                         routine.get("actif", True)))
    return resultat


def executer_routine(nom):
    """Executer UNE routine par son nom (pour un tic dedie).
    Retourne True si l'execution a reussi."""
    flags_no_window = 0
    if hasattr(subprocess, "CREATE_NO_WINDOW"):
        flags_no_window = subprocess.CREATE_NO_WINDOW
    for nom_routine, script, _, actif in infos_routines():
        if nom_routine != nom:
            continue
        if not actif or not script.exists():
            return False
        etat = charger_etat()
        etat[nom] = {"derniere": maintenant()}
        sauver_etat(etat)
        try:
            p = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=120,
                creationflags=flags_no_window)
            if p.returncode != 0:
                print(f"[ROUTINES] {nom}: rc={p.returncode}")
            return p.returncode == 0
        except Exception as e:
            print(f"[ROUTINES] ERREUR {nom}: {e}")
            return False
    return False


def executer_routines():
    """Executer les routines du manifest dont l'intervalle est ecoule.
    Silencieux sauf erreur : jarvis reste fluide. Aucune fenetre :
    CREATE_NO_WINDOW + sortie capturee."""
    import subprocess
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    etat = charger_etat()
    flags_no_window = 0
    try:
        import subprocess as _s
        if hasattr(_s, "CREATE_NO_WINDOW"):
            flags_no_window = _s.CREATE_NO_WINDOW
    except Exception:
        pass
    for routine in manifest.get("routines_surveillance", []):
        if not routine.get("actif", True):
            continue
        nom = routine.get("nom")
        script = FREELANCE / "routines" / routine.get("script", "")
        intervalle = routine.get("intervalles_secondes",
                                 manifest.get("intervalle_boucle_secondes",
                                              600))
        dernier_iso = etat.get(nom, {}).get("derniere", "")
        ecoulé = secondes_ecoulee(dernier_iso)
        if ecoulé < intervalle:
            continue
        if not script.exists():
            continue
        etat[nom] = {"derniere": maintenant()}
        sauver_etat(etat)  # sauver AVANT : jamais deux fois par tour
        try:
            p = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=120,
                creationflags=flags_no_window)
            if p.returncode != 0:
                print(f"[ROUTINES] {nom}: rc={p.returncode}")
        except Exception as e:
            print(f"[ROUTINES] ERREUR {nom}: {e}")


def cmd_routines_etat(args=None):
    """Afficher l'etat des routines (derniere execution / intervalle)."""
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        print("[ROUTINES] manifest introuvable")
        return
    etat = charger_etat()
    print("[ROUTINES] Etat (intervalle ecoule = sera executee au prochain "
          "appel de jarvis) :")
    for routine in manifest.get("routines_surveillance", []):
        nom = routine.get("nom")
        intervalle = routine.get("intervalles_secondes",
                                 manifest.get("intervalle_boucle_secondes",
                                              600))
        dernier_iso = etat.get(nom, {}).get("derniere", "")
        ecoulé = secondes_ecoulee(dernier_iso)
        quand = f"il y a {int(ecoulé)}s" if ecoulé < 10**9 else "jamais"
        due = "A EXECUTER" if ecoulé >= intervalle else ""
        print(f"  {nom} [{intervalle}s] derniere: {quand} {due}")
