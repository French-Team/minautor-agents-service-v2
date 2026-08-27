# -*- coding: ascii -*-
# routine : compter-sortie -- mesure les tokens SORTIE periodiquement,
# journalise dans data/journal-sortie.jsonl et ecrit dans tokens-historique.md.
# D15 : routine = collecteur, l'outil fait le calcul.
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# P10 : racine DETECTEE
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)

# Import de l'outil (tools-commun)
_TOOLS_SORTIE = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "compter-sortie" / "fonctions"
sys.path.insert(0, str(_TOOLS_SORTIE))
from mesurer import mesurer_toutes_sources, calculer_tokens_sortie, \
    comparer_snapshots_sortie, charger_sources

# Import historique
sys.path.insert(0, str(Path(__file__).parent))
from ecrire_historique import (
    trouver_fichier_historique, lire_etat_actuel,
    mettre_a_jour_etat, ajouter_ligne_historique
)

DATA_DIR = RACINE / "cerveau-projet" / "freelance" / "routines" / "data"
JOURNAL = DATA_DIR / "journal-sortie.jsonl"
SNAPSHOT_FILE = DATA_DIR / "snapshot-sortie.json"


def _lire_dernier_snapshot():
    """Lit le dernier snapshot ou retourne dict vide."""
    if not SNAPSHOT_FILE.exists():
        return {}
    try:
        return json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def _ecrire_snapshot(tokens):
    """Ecrit le snapshot actuel."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(
        json.dumps(tokens, ensure_ascii=False), encoding="utf-8")


def _journaliser(tokens, delta):
    """Ajoute une entree au journal JSONL."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    entree = {
        "date": datetime.now().isoformat(),
        "tokens": tokens["total_tokens"],
        "octets": tokens["total_octets"],
        "sources": tokens["nb_sources"],
        "delta": delta.get("delta_tokens", 0),
    }
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    sources_fichier = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "compter-sortie" / "data" / "sources.json"
    sources_config = charger_sources(str(sources_fichier))
    resultats = mesurer_toutes_sources(str(RACINE), sources_config)
    tokens = calculer_tokens_sortie(
        resultats, sources_config.get("chars_par_token", 4.0))

    precedent = _lire_dernier_snapshot()
    delta = comparer_snapshots_sortie(precedent, tokens)

    _journaliser(tokens, delta)
    _ecrire_snapshot(tokens)

    # Ecrire dans tokens-historique.md
    fichier_hist = trouver_fichier_historique(str(RACINE))
    etat = lire_etat_actuel(fichier_hist)
    delta_sortie = tokens["total_tokens"] - etat.get("sortie", 0)
    mettre_a_jour_etat(fichier_hist, etat.get("entree", 0), tokens["total_tokens"])
    ajouter_ligne_historique(fichier_hist, etat.get("entree", 0),
                             tokens["total_tokens"], 0, delta_sortie, "sortie")

    if delta["delta_tokens"] > 0:
        print("[COMPTER-SORTIE] +%d tokens (%d -> %d)" % (
            delta["delta_tokens"],
            delta.get("precedent_tokens", 0),
            tokens["total_tokens"]))
    elif delta["delta_tokens"] < 0:
        print("[COMPTER-SORTIE] %d tokens (%d -> %d)" % (
            delta["delta_tokens"],
            delta.get("precedent_tokens", 0),
            tokens["total_tokens"]))
    else:
        print("[COMPTER-SORTIE] Stable : %d tokens" % tokens["total_tokens"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
