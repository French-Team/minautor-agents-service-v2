#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine encart -- Verification de l integrite de l encart v1
(session-admin, AGENTS-activite-recente.md).

Transposee de la routine v2 encart (surveillance/encart.py). Le format v1
est un tableau markdown simple (sans emoji grade) :
  | Grade | Agent | Executeur | Etat | Secteur | Raison | Heure | id | Type |

La colonne Etat porte l etat de l activite (decision utilisateur
2026-08-29) : DEBUT, FIN, ATTENTE, URGENT, BUG, ACTIF.

Verifie la presence de l en-tete de colonnes, l integrite structurelle,
que les valeurs de la colonne Etat sont parmi les valeurs connues, et que
la colonne EXECUTEUR n est pas vide (lecon 2026-08-30 : des entrees a
Executeur vide etaient historisees par activer-agent-principal au lieu
d Oracle, et AUCUNE routine ne le signalait). Depuis v0.3.1 (decision
utilisateur 2026-09-02, URGENT) : detecte aussi les valeurs 'Inconnu' en
colonnes Grade et Agent - un grade 'Inconnu' ou un agent absent du mapping
grades-v1.json (agents/routines declares) signale un ACTEUR NON DECLARE
dans l encart (ex: le pilote avant sa declaration SP) et est historise en
anomalie comme les etats inconnus. Historise UNIQUEMENT en cas d anomalie
(evenementiel).

Usage:
    python3 encart.py [--dry-run]

Retour: 0 si OK, 1 si anomalie(s).
"""

import io
import json
import os
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.3.1"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = Path(_DOSSIER).parent

ENTETE_V1 = "| Grade | Agent | Defcon | Executeur | Etat | Secteur | Raison |"

# Etats connus de la colonne Etat (decision utilisateur 2026-08-29) :
# charges DYNAMIQUEMENT depuis etats-actions.json (v0.2.0) pour ne plus
# editer le code quand on ajoute un etat. Repli : ensemble v0.1.0.
ETATS_CONNUS_DEFAUT = {"DEBUT", "FIN", "ATTENTE", "URGENT", "BUG",
                       "ACTIF", "DEV", "AUTO", "ACTION"}

GRADES_V1 = os.environ.get("GRADES_V1",
                            "cerveau-projet/agents/tools/oracle/grades-v1.json")


def _chemin_grades_v1():
    """Chemin absolu vers grades-v1.json (declare les agents/routines v1)."""
    p = Path(GRADES_V1)
    if p.is_absolute():
        return p
    return _racine_projet() / GRADES_V1


def _charger_grades_v1():
    """Lire grades-v1.json (agents + routines declares pour la session v1).
    Repli : dict vide si fichier absent/invalide."""
    try:
        with io.open(str(_chemin_grades_v1()), "r", encoding="utf-8",
                     errors="replace") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            return data
    except (OSError, ValueError):
        pass
    return {}


def _agents_connus():
    """Ensemble des agents + routines declares dans grades-v1.json (minuscules).
    Exclut les pseudonymes de grade qui ne sont pas des acteurs (ex: defaut)."""
    data = _charger_grades_v1()
    connus = set()
    for cle in ("agents", "routines"):
        m = data.get(cle)
        if isinstance(m, dict):
            connus.update(k.lower() for k in m.keys())
    return connus


def _charger_etats_connus():
    """Lire la liste des etats depuis etats-actions.json (cles de 'etats')."""
    try:
        with io.open(str(ORACLE_DIR / "etats-actions.json"), "r",
                     encoding="utf-8", errors="replace") as fh:
            data = json.load(fh)
        etats = data.get("etats")
        if isinstance(etats, dict) and etats:
            return set(etats.keys())
    except (OSError, ValueError):
        pass
    return ETATS_CONNUS_DEFAUT


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


def main():
    dry_run = "--dry-run" in sys.argv
    racine = _racine_projet()
    encart = racine / "AGENTS-activite-recente.md"
    anomalies = []

    if not encart.is_file():
        anomalies.append("Fichier AGENTS-activite-recente.md absent")
    else:
        contenu = encart.read_text(encoding="utf-8", errors="replace")
        if ENTETE_V1 not in contenu:
            anomalies.append("En-tete de colonnes v1 absent : %s" % ENTETE_V1)
        # Verifier les valeurs de la colonne Etat + la colonne Executeur.
        # Colonnes: '' | Grade | Agent | Defcon | Executeur | Etat | Secteur |
        for ligne in contenu.splitlines():
            if not ligne.strip().startswith("| ") or "| Grade |" in ligne:
                continue
            cols = [c.strip() for c in ligne.split("|")]
            if len(cols) < 6:
                continue
            # Sauver l ID d historique (colonne 9) pour le signaler.
            ident = cols[9] if len(cols) > 9 else "?"
            etat = cols[5]
            if etat and etat not in _charger_etats_connus():
                anomalies.append("Etat inconnu '%s' (colonne Etat)" % etat)
            # Executeur vide (colonne 4) : signale une historisation hors
            # Oracle (seul Oracle doit historiser). Les lignes de donnees ont
            # toujours un Executeur (Oracle pour un historique utilisateur,
            # RT(<s>) pour les routines, demarrer-llm pour le demarrage).
            executeur = cols[4]
            if not executeur:
                anomalies.append(
                    "Executeur vide (ligne id=%s, agent=%s)" %
                    (ident, cols[2]))
            # Decision utilisateur 2026-09-02 (URGENT) : detecter les cases
            # 'Inconnu' dans les colonnes Grade ET Agent. Un grade 'Inconnu'
            # ou un agent absent du mapping grades-v1.json (agents/routines)
            # signale un acteur NON DECLARE dans l encart (ex: le pilote
            # avant sa declaration SP). Colonnes: '' | Grade | Agent | ...
            # => cols[1]=Grade, cols[2]=Agent.
            agent_c = (cols[2] or "").strip().lower()
            grade = cols[1] if len(cols) > 1 else ""
            if grade and grade == "Inconnu":
                anomalies.append(
                    "Grade 'Inconnu' pour l agent '%s' (non declare dans "
                    "grades-v1.json agents/routines)" % cols[2])
            if agent_c and agent_c not in _agents_connus():
                anomalies.append(
                    "Agent '%s' absent du mapping grades-v1.json "
                    "(agents/routines non declares)" % cols[2])

    if not anomalies:
        print("[ENCART] OK (encart v1 coherent)")
        return 0

    print("[ENCART] %d anomalie(s) :" % len(anomalies))
    for a in anomalies:
        print("  ! %s" % a)
    if dry_run:
        print("[ENCART] --dry-run : anomalie non historisee")
        return 1
    _historiser_agent("encart", "%d anomalie(s): %s" %
                      (len(anomalies), "; ".join(anomalies[:3])), "R")
    return 1


if __name__ == "__main__":
    sys.exit(main())