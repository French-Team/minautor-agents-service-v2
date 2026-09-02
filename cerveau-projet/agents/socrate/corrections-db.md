# Socrate corrections database

`corrections-db.py` stores the structured rules and lessons from `corrections.md`
in SQLite at `corrections.db`.

The Markdown file remains the readable source; importing is idempotent and
uses a content hash, so repeated imports do not create duplicate rows.

```bash
python3 cerveau-projet/agents/socrate/corrections-db.py init
python3 cerveau-projet/agents/socrate/corrections-db.py import
python3 cerveau-projet/agents/socrate/corrections-db.py list
python3 cerveau-projet/agents/socrate/corrections-db.py list --section REGLES -- Regles specifiques
```

Sections, keys, values, source hash, and import timestamp are queryable from
the `corrections` table.
