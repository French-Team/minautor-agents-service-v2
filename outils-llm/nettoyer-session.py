#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reset one LLM session without deleting required project files."""

import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.2.2"
RACINE = Path(__file__).resolve().parent.parent
ORACLE_DIR = RACINE / "cerveau-projet/agents/tools/oracle"
CLASSEUR_DIR = RACINE / "cerveau-projet/agents/classeur-variables"
ACTIVER_PRINCIPAL = RACINE / "cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py"

FILES = {
    "session-admin": {
        "encart": RACINE / "AGENTS-activite-recente.md",
        "corps": RACINE / "AGENTS-historique.md",
        "encoding": "ascii",
        "newline": "\n",
    },
    "session-freelance": {
        "encart": RACINE / "AGENTS-activite-recente-v2.md",
        "corps": RACINE / "AGENTS-historique-v2.md",
        "encoding": "utf-8",
        "newline": "\r\n",
    },
}
AGENT_OUVERTURE = {"session-admin": "cerberus", "session-freelance": "stark"}


def _write(path, text, encoding="utf-8", newline="\n", dry_run=False):
    if dry_run:
        print("  [DRY-RUN] recreerait %s" % path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    text = text.replace("\r\n", "\n").replace("\n", newline)
    with open(path, "w", encoding=encoding, newline="") as fh:
        fh.write(text)


def _reset_activity_files(session, dry_run=False):
    cfg = FILES[session]
    if session == "session-admin":
        encart = (
            "---\nidentite:\n  nom: Activites recentes\n  type: tableau\n"
            "  description: Vue des activites recentes de la session-admin v1\n"
            "  appartient_a: commun\n  commun: true\n---\n\n"
            "## Activites recentes -- session-admin\n\n"
            "| Grade | Agent | Defcon | Executeur | Etat | Secteur | Raison | Heure | id | Type |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n"
        )
        corps = (
            "---\nidentite:\n  nom: Historique session-admin\n  type: historique\n"
            "  appartient_a: commun\n  commun: true\n---\n"
        )
    else:
        encart = (
            "---\nidentite:\n  nom: Activites recentes freelance\n  type: tableau\n"
            "  appartient_a: commun\n  commun: true\n---\n"
        )
        corps = (
            "---\nidentite:\n  nom: Historique session-freelance\n  type: historique\n"
            "  appartient_a: commun\n  commun: true\n---\n"
        )
    _write(cfg["encart"], encart, cfg["encoding"], cfg["newline"], dry_run)
    _write(cfg["corps"], corps, cfg["encoding"], cfg["newline"], dry_run)


def _clear_dir(path, dry_run=False):
    if not path.exists():
        if not dry_run:
            path.mkdir(parents=True, exist_ok=True)
        return 0
    children = list(path.iterdir())
    if dry_run:
        for child in children:
            print("  [DRY-RUN] supprimerait %s" % child)
        return len(children)
    for child in children:
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    return len(children)


def _remove_file(path, dry_run=False):
    if not path.exists():
        return 0
    if dry_run:
        print("  [DRY-RUN] supprimerait %s" % path)
        return 1
    path.unlink()
    return 1


def _backup_path(session):
    """Return a unique, session-scoped backup directory."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return RACINE / ("backup-%s-%s" % (stamp, session))


def _backup_file(source, backup_root, dry_run=False):
    if not source.exists() or not source.is_file():
        return 0
    destination = backup_root / source.relative_to(RACINE)
    if dry_run:
        print("  [DRY-RUN] sauvegarderait %s -> %s" % (source, destination))
        return 1
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return 1


def _backup_runtime_admin(backup_root, dry_run=False):
    """Backup all resettable admin state before it is cleared."""
    count = 0
    paths = [
        RACINE / "AGENTS-activite-recente.md",
        RACINE / "AGENTS-historique.md",
        ORACLE_DIR / "files/asap.jsonl",
        ORACLE_DIR / "files/normale.jsonl",
        ORACLE_DIR / "files/plus-tard.jsonl",
        CLASSEUR_DIR / "stockage/variables-actuelles.md",
        CLASSEUR_DIR / "historique/historique-modifications.md",
    ]
    for path in paths:
        count += _backup_file(path, backup_root, dry_run)
    for directory in (ORACLE_DIR / "inbox", ORACLE_DIR / "outbox",
                      ORACLE_DIR / "etat-cartes", ORACLE_DIR / "routines/data"):
        if directory.exists():
            for path in directory.rglob("*"):
                if path.is_file():
                    count += _backup_file(path, backup_root, dry_run)
    if dry_run:
        print("  [DRY-RUN] creerait le manifeste %s/manifest.json" % backup_root)
    else:
        backup_root.mkdir(parents=True, exist_ok=True)
        manifest = {
            "session": "session-admin",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "purpose": "zero-total backup before reset",
            "files": count,
        }
        (backup_root / "manifest.json").write_text(
            __import__("json").dumps(manifest, indent=2), encoding="utf-8")
    return count


def _reset_queue_files(dry_run=False):
    """Recreate all standard queues as valid empty JSONL files."""
    count = 0
    for name in ("asap.jsonl", "normale.jsonl", "plus-tard.jsonl"):
        path = ORACLE_DIR / "files" / name
        _write(path, "", dry_run=dry_run)
        count += 1
    return count


def _zero_total_admin(dry_run=False):
    backup_root = _backup_path("session-admin")
    print("  sauvegarde: %s" % backup_root)
    backed_up = _backup_runtime_admin(backup_root, dry_run)
    total = 0
    for relative in ("inbox", "outbox", "etat-cartes", "routines/data"):
        total += _clear_dir(ORACLE_DIR / relative, dry_run)
    total += _reset_queue_files(dry_run)
    for relative in (
        "routines/etat-executions.json",
        "oracle-server.pid",
        "routines-server.pid",
        "super-combos/super-pilote.pid",
        "session-admin-inactivite.json",
    ):
        total += _remove_file(ORACLE_DIR / relative, dry_run)
    _reset_activity_files("session-admin", dry_run)
    _write(
        CLASSEUR_DIR / "stockage/variables-actuelles.md",
        "---\nidentite:\n  type: classeur\n  appartient_a: commun\n  commun: true\n---\n"
        "# Stockage -- Variables Actuelles\n---\n\n## Variables\n"
        "| Variable | Valeur | Source | Date | Statut |\n"
        "|---|---|---|---|---|\n",
        dry_run=dry_run,
    )
    _write(
        CLASSEUR_DIR / "historique/historique-modifications.md",
        "# Historique des modifications du classeur\n",
        dry_run=dry_run,
    )
    print("  fichiers sauvegardes: %d" % backed_up)
    return total


def _reset_agent(session, dry_run=False):
    if dry_run or not ACTIVER_PRINCIPAL.is_file():
        return dry_run
    try:
        result = subprocess.run(
            [sys.executable, str(ACTIVER_PRINCIPAL), "activer", session,
             AGENT_OUVERTURE[session], "ZERO TOTAL: etat neuf de session"],
            capture_output=True, text=True, timeout=60,
        )
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def nettoyer(llm_id, session, zero_total=False, dry_run=False):
    print("=== NETTOYAGE SESSION v%s ===" % VERSION)
    print("  id: %s\n  session: %s" % (llm_id, session))
    if zero_total:
        if session != "session-admin":
            print("ERREUR: --zero-total est reserve a session-admin")
            return 1
        print("  mode: ZERO TOTAL%s" % (" (simulation)" if dry_run else ""))
        total = _zero_total_admin(dry_run)
        print("  elements runtime concernes: %d" % total)
    else:
        _reset_activity_files(session, dry_run)
        if session == "session-freelance":
            _clear_dir(RACINE / "cerveau-projet/freelance/tools-commun/jarvis/inbox", dry_run)
            _clear_dir(RACINE / "cerveau-projet/freelance/tools-commun/jarvis/outbox", dry_run)
    if not dry_run and not _reset_agent(session):
        print("  agent d ouverture: activation indisponible")
    elif dry_run:
        print("  [DRY-RUN] activation de %s differee" % AGENT_OUVERTURE[session])
    else:
        print("  agent d ouverture: %s" % AGENT_OUVERTURE[session])
    print("=== %s TERMINE ===" % ("ZERO TOTAL" if zero_total else "NETTOYAGE"))
    return 0


def afficher_aide():
    print("usage: nettoyer-session.py <id> <session> [--zero-total] [--dry-run]")
    print("  --zero-total  purge les historiques, messages et etats runtime admin")
    print("  --dry-run     affiche les operations sans modifier de fichier")


def main(argv):
    if "--help" in argv or "-h" in argv or "aide" in argv:
        afficher_aide()
        return 0
    zero_total = "--zero-total" in argv
    dry_run = "--dry-run" in argv
    args = [arg for arg in argv if arg not in ("--zero-total", "--dry-run")]
    if len(args) < 2:
        afficher_aide()
        return 1
    session = "session-" + args[1] if args[1] in ("admin", "freelance") else args[1]
    if session not in FILES:
        print("ERREUR: session invalide")
        return 1
    return nettoyer(args[0], session, zero_total, dry_run)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
