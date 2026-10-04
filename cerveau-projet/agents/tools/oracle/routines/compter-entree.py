#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
routine compter-entree -- Mesure des tokens ENTREE (v1, session-admin).

Transposee des routines v2 compter-entree (surveillance/) pour l univers
v1 : reutilise le module partage de comptage v2 (compteur.mesurer_entree)
pour la MESURE reelle (les fichiers lus par l LLM), mais journalise dans
le dossier v1 (oracle/routines/data/) - 2 univers distincts.

Le principe D15 est respecte : la routine = collecteur (elle tourne),
l outil fait le calcul ; ici on reuse le compteur partage et on cree un
journal v1 + un fichier tokens-historique-v1.md.

Usage:
    python3 compter-entree.py

Retour: 0 si succes, 1 si erreur.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
ORACLE_DIR = Path(_DOSSIER).parent
DATA_DIR = Path(_DOSSIER) / "data"
JOURNAL = DATA_DIR / "journal-entree.jsonl"

# Racine du projet
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)


def _journaliser(tokens, delta, octets, fichiers):
    """Ajoute une entree au journal JSONL v1."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    entree = {
        "date": datetime.now().isoformat(),
        "tokens": tokens,
        "octets": octets,
        "fichiers": fichiers,
        "delta": delta,
    }
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")


def _mettre_a_jour_historique(tokens, delta):
    """Ecrit/ajoute dans tokens-historique-v1.md (ligne par tick)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    hist = DATA_DIR / "tokens-historique-v1.md"
    ligne = "| %s | %d | %+d | entree |" % (
        datetime.now().strftime("%H:%M"), tokens, delta)
    if not hist.exists():
        hist.write_text(
            "# Tokens ENTREE v1 (session-admin)\n\n"
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
        from compteur import mesurer_entree, mesurer_fichiers
        import json as _json
        # Reutiliser le calcul detaille pour avoir octets + nb fichiers.
        data_dir = RACINE / "cerveau-projet" / "freelance" / \
            "tools-commun" / "compter-entree" / "data" / "patterns.json"
        patterns = {}
        if data_dir.exists():
            try:
                patterns = _json.loads(data_dir.read_text(encoding="utf-8"))
            except ValueError:
                patterns = {}
        fichiers = mesurer_fichiers(str(RACINE), patterns)
        total_octets = sum(r["taille_octets"] for r in fichiers)
        chars = patterns.get("chars_par_token", 4.0)
        tokens = int(total_octets / chars)
        precedent = _lire_dernier_tokens()
        delta = tokens - precedent
        _journaliser(tokens, delta, total_octets, len(fichiers))
        _mettre_a_jour_historique(tokens, delta)
        print("[COMPTER-ENTREE] %d tokens (%d->%d, %d fichiers)" %
              (tokens, precedent, tokens, len(fichiers)))
    except Exception as exc:
        print("[COMPTER-ENTREE] ERREUR : %s" % exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())