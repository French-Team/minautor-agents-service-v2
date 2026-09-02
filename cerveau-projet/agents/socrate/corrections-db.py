#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SQLite knowledge base for Socrate corrections.

The Markdown corrections file remains the human-readable source document;
this tool imports its structured rules and lessons into a queryable database.
"""
import argparse
import hashlib
import re
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENT_DIR = ROOT / "agents" / "socrate"
CORRECTIONS = AGENT_DIR / "corrections.md"
DB_PATH = AGENT_DIR / "corrections.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS corrections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    source_hash TEXT NOT NULL,
    imported_at TEXT NOT NULL,
    UNIQUE(section, key, value)
);
CREATE INDEX IF NOT EXISTS idx_corrections_section ON corrections(section);
"""


def _rows(text):
    section = "general"
    for line in text.splitlines():
        heading = re.match(r"^##\s+([^#]+)", line)
        if heading:
            section = heading.group(1).strip()
            continue
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() in {"regle", "philosophie", "date", "outil", "fichier"}:
            continue
        yield section, cells[0], " | ".join(cells[1:])


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as db:
        db.executescript(SCHEMA)


def import_corrections(path=CORRECTIONS):
    text = path.read_text(encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    now = datetime.now().isoformat(timespec="milliseconds")
    init_db()
    count = 0
    with sqlite3.connect(DB_PATH) as db:
        for section, key, value in _rows(text):
            db.execute(
                "INSERT OR IGNORE INTO corrections "
                "(section,key,value,source_hash,imported_at) VALUES (?,?,?,?,?)",
                (section, key, value, digest, now),
            )
            count += db.execute("SELECT changes()").fetchone()[0]
        db.commit()
    return count


def list_corrections(section=None):
    init_db()
    query = "SELECT section,key,value FROM corrections"
    args = ()
    if section:
        query += " WHERE section=?"
        args = (section,)
    query += " ORDER BY id"
    with sqlite3.connect(DB_PATH) as db:
        return db.execute(query, args).fetchall()


def main():
    parser = argparse.ArgumentParser(prog="socrate-corrections-db")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("import")
    show = sub.add_parser("list")
    show.add_argument("--section")
    args = parser.parse_args()
    if args.command == "init":
        init_db()
        print(DB_PATH)
    elif args.command == "import":
        print("%d correction(s) imported" % import_corrections())
    else:
        for section, key, value in list_corrections(args.section):
            print("[%s] %s: %s" % (section, key, value))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
