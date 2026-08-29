#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine compter-sortie -- Mesure des tokens SORTIE (v1, session-admin).

Transposee de la routine v2 compter-sortie (surveillance/) pour l univers
v1 : reutilise le module partage de comptage v2 (compteur.mesurer_sortie)
pour la MESURE reelle des sources de sortie, mais journalise dans le
dossier v1 (oracle/routines/data/) - 2 univers distincts.

Usage:
    python3 compter-sortie.py

Retour: 0 si succes, 1 si erreur.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = Path(_DOSSIER) / "data"
JOURNAL = DATA_DIR / "journal-sortie.jsonl"

# Racine du projet
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)


def _journaliser(tokens, delta, octets, sources):
    """Ajoute une entree au journal JSONL v1."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    entree = {
        "date": datetime.now().isoformat(),
        "tokens": tokens,
        "octets": octets,
        "sources": sources,
        "delta": delta,
    }
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")


def _mettre_a_jour_historique(tokens, delta):
    """Ecrit/ajoute dans tokens-historique-v1.md (ligne par tick)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    hist = DATA_DIR / "tokens-historique-v1.md"
    ligne = "| %s | %d | %+d | sortie |" % (
        datetime.now().strftime("%H:%M"), tokens, delta)
    if not hist.exists():
        hist.write_text(
            "# Tokens SORTIE v1 (session-admin)\n\n"
            "| Heure | tokens | delta | type |\n"
            "|-------|--------|-------|------|\n", encoding="utf-8")
    with open(hist, "a", encoding="utf-8") as f:
        f.write(ligne + "\n")


def _lire_dernier_tokens():
    """Dernier total de tokens connu dans le journal."""
    if not JOURNAL.exists():
        return 0
    dernier = 0
    try:
        for ligne in JOURNAL.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            m = json.loads(ligne)
            dernier = int(m.get("tokens", 0))
    except (ValueError, OSError):
        pass
    return dernier


def main():
    try:
        sys.path.insert(0, str(RACINE / "cerveau-projet" / "freelance" /
                               "tools-commun" / "compter" / "fonctions"))
        from compteur import mesurer_sources
        import json as _json
        sources_file = RACINE / "cerveau-projet" / "freelance" / \
            "tools-commun" / "compter-sortie" / "data" / "sources.json"
        config = {}
        if sources_file.exists():
            try:
                config = _json.loads(sources_file.read_text(encoding="utf-8"))
            except ValueError:
                config = {}
        resultats = mesurer_sources(str(RACINE), config)
        total_octets = sum(r["taille_octets"] for r in resultats)
        chars = config.get("chars_par_token", 4.0)
        tokens = int(total_octets / chars)
        precedent = _lire_dernier_tokens()
        delta = tokens - precedent
        _journaliser(tokens, delta, total_octets, len(resultats))
        _mettre_a_jour_historique(tokens, delta)
        print("[COMPTER-SORTIE] %d tokens (%d->%d, %d sources)" %
              (tokens, precedent, tokens, len(resultats)))
    except Exception as exc:
        print("[COMPTER-SORTIE] ERREUR : %s" % exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())