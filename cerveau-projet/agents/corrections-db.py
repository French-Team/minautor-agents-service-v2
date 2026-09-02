#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared corrections importer and short-memory migrator for v1 agents."""
import argparse
import hashlib
import re
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
DB_PATH = AGENTS_DIR / "corrections.db"
SCHEMA = """
CREATE TABLE IF NOT EXISTS corrections (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 agent TEXT NOT NULL,
 section TEXT NOT NULL,
 key TEXT NOT NULL,
 value TEXT NOT NULL,
 source_path TEXT NOT NULL,
 source_hash TEXT NOT NULL,
 imported_at TEXT NOT NULL,
 UNIQUE(agent, section, key, value, source_hash)
);
CREATE INDEX IF NOT EXISTS idx_corrections_agent ON corrections(agent);
"""


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as db:
        db.executescript(SCHEMA)


def parse_rows(text):
    section = "general"
    ignored = {"regle", "philosophie", "date", "outil", "fichier", "champ"}
    for line in text.splitlines():
        heading = re.match(r"^##\s+([^#]+)", line)
        if heading:
            section = heading.group(1).strip()
            continue
        if not line.startswith("|") or re.match(r"^\|\s*:?-+", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() in ignored:
            continue
        yield section, cells[0], " | ".join(cells[1:])


def import_all():
    init_db()
    now = datetime.now().isoformat(timespec="milliseconds")
    total = 0
    files = sorted(AGENTS_DIR.glob("*/corrections.md"))
    with sqlite3.connect(DB_PATH) as db:
        for path in files:
            text = path.read_text(encoding="utf-8")
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            agent = path.parent.name
            for section, key, value in parse_rows(text):
                cur = db.execute(
                    "INSERT OR IGNORE INTO corrections "
                    "(agent,section,key,value,source_path,source_hash,imported_at) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (agent, section, key, value,
                     str(path.relative_to(ROOT)), digest, now),
                )
                total += cur.rowcount
        db.commit()
    return total, len(files)


def _explicit_blocks(text):
    lines = text.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines)
              if re.match(r"^##\s+\[LECON\]\s+", line)]
    return ["".join(lines[start:(starts[pos + 1] if pos + 1 < len(starts) else len(lines))]).rstrip() + "\n"
            for pos, start in enumerate(starts)]


def _legacy_rows(text):
    """Extract dated Markdown table rows as self-contained lesson blocks."""
    rows = []
    for line in text.splitlines():
        if re.match(r"^\|\s*20\d\d-\d\d-\d\d\s*\|", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2:
                title = cells[1][:80]
                rows.append((cells[0], "## [LECON] %s -- %s\n\n%s\n" %
                             (cells[0], title, line)))
    return rows


def trim_lessons(limit=10):
    """Keep the ten newest lessons, supporting explicit blocks and legacy rows."""
    changed = 0
    for path in sorted(AGENTS_DIR.glob("*/corrections.md")):
        text = path.read_text(encoding="utf-8")
        explicit = _explicit_blocks(text)
        legacy = _legacy_rows(text)
        if len(explicit) > limit:
            first = re.search(r"^##\s+\[LECON\]\s+", text, re.M)
            header = text[:first.start()]
            text = header + "\n".join(b.rstrip() for b in explicit[-limit:]) + "\n"
            path.write_text(text, encoding="utf-8", newline="\n")
            changed += 1
        elif not explicit and len(legacy) > limit:
            # Preserve everything before the first dated lesson table row and
            # rebuild the table with its newest ten rows.
            first = re.search(r"^\|\s*20\d\d-\d\d-\d\d\s*\|", text, re.M)
            if first:
                header = text[:first.start()]
                rows = [block for _, block in legacy[-limit:]]
                path.write_text(header + "\n".join(r.rstrip() for r in rows) + "\n",
                                encoding="utf-8", newline="\n")
                changed += 1
    return changed


def list_corrections(agent=None):
    init_db()
    query = "SELECT agent, section, key, value FROM corrections"
    args = ()
    if agent:
        query += " WHERE agent=?"
        args = (agent,)
    query += " ORDER BY agent, id"
    with sqlite3.connect(DB_PATH) as db:
        return db.execute(query, args).fetchall()


def main():
    parser = argparse.ArgumentParser(prog="agents-corrections-db")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    imp = sub.add_parser("import")
    imp.add_argument("--trim", action="store_true",
                     help="archive all lessons, then keep 10 newest per file")
    show = sub.add_parser("list")
    show.add_argument("--agent")
    args = parser.parse_args()
    if args.command == "init":
        init_db()
        print(DB_PATH)
    elif args.command == "import":
        count, agents = import_all()
        trimmed = trim_lessons() if args.trim else 0
        print("%d correction(s) imported from %d agent(s); %d file(s) trimmed" %
              (count, agents, trimmed))
    else:
        for agent, section, key, value in list_corrections(args.agent):
            print("[%s][%s] %s: %s" % (agent, section, key, value))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
