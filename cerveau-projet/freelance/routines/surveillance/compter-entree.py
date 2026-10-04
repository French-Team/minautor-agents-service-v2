# -*- coding: ascii -*-
# routine : compter-entree -- mesure les tokens ENTREE periodiquement,
# journalise dans data/journal-entree.jsonl et ecrit dans tokens-historique.md.
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
_TOOLS_ENTREE = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "compter-entree" / "fonctions"
sys.path.insert(0, str(_TOOLS_ENTREE))
from mesurer import mesurer_fichiers, calculer_tokens, comparer_snapshots, charger_patterns

# Import historique
sys.path.insert(0, str(Path(__file__).parent))
from ecrire_historique import (
    trouver_fichier_historique, lire_etat_actuel,
    mettre_a_jour_etat, ajouter_ligne_historique
)

DATA_DIR = RACINE / "cerveau-projet" / "freelance" / "routines" / "data"
JOURNAL = DATA_DIR / "journal-entree.jsonl"
SNAPSHOT_FILE = DATA_DIR / "snapshot-entree.json"


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


def _journaliser(secteur, tokens, delta):
    """Ajoute une entree au journal JSONL."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    entree = {
        "date": datetime.now().isoformat(),
        "tokens": tokens["total_tokens"],
        "octets": tokens["total_octets"],
        "fichiers": tokens["nb_fichiers"],
        "delta": delta.get("delta_tokens", 0),
    }
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    patterns_fichier = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / "compter-entree" / "data" / "patterns.json"
    patterns = charger_patterns(str(patterns_fichier))
    fichiers = mesurer_fichiers(str(RACINE), patterns)
    tokens = calculer_tokens(fichiers, patterns.get("chars_par_token", 4.0))

    precedent = _lire_dernier_snapshot()
    delta = comparer_snapshots(precedent, tokens)

    _journaliser("entree", tokens, delta)
    _ecrire_snapshot(tokens)

    # Ecrire dans tokens-historique.md
    fichier_hist = trouver_fichier_historique(str(RACINE))
    etat = lire_etat_actuel(fichier_hist)
    delta_entree = tokens["total_tokens"] - etat.get("entree", 0)
    mettre_a_jour_etat(fichier_hist, tokens["total_tokens"], etat.get("sortie", 0))
    ajouter_ligne_historique(fichier_hist, tokens["total_tokens"],
                             etat.get("sortie", 0), delta_entree, 0, "entree")

    if delta["delta_tokens"] > 0:
        print("[COMPTER-ENTREE] +%d tokens (%d -> %d)" % (
            delta["delta_tokens"],
            delta.get("precedent_tokens", 0),
            tokens["total_tokens"]))
    elif delta["delta_tokens"] < 0:
        print("[COMPTER-ENTREE] %d tokens (%d -> %d)" % (
            delta["delta_tokens"],
            delta.get("precedent_tokens", 0),
            tokens["total_tokens"]))
    else:
        print("[COMPTER-ENTREE] Stable : %d tokens" % tokens["total_tokens"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
