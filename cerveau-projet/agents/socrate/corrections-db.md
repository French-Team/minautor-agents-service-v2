# Socrate - base de corrections

`corrections-db.py` stocke dans SQLite (`corrections.db`) les regles et lecons structurees issues de `corrections.md`.

Le fichier Markdown reste la source lisible ; l'import est idempotent et utilise un hash de contenu, donc les imports repetes n'ajoutent pas de doublons.

```bash
python3 cerveau-projet/agents/socrate/corrections-db.py init
python3 cerveau-projet/agents/socrate/corrections-db.py import
python3 cerveau-projet/agents/socrate/corrections-db.py list
python3 cerveau-projet/agents/socrate/corrections-db.py list --section REGLES -- Regles specifiques
```

Sections, clefs, valeurs, hash source et horodatage d import sont exploitables depuis la table `corrections`.

