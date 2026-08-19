#!/usr/bin/env bash
# valider-tableaux.sh
# Verifie la coherence des tableaux des fiches agents :
#   1. Nombres d'etapes annonces vs lignes reelles (tableau des missions)
#   2. Numerotation continue des tableaux numerotes (etapes, points de controle)
#   3. Completude des listes d'agents (Agents disponibles vs fiches existantes)
# Wrapper pur : transmet les arguments au .py (parite garantie par construction).
# (L'ancien heredoc python3 - cassait l'interpretation sous stdin Windows,
#  bug preexistant 0.2.0 -> remplace par le wrapper en 0.2.1.)
# Version : 0.2.1
# Statut : prepare
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/valider-tableaux.py"

if [ ! -f "$PY_SCRIPT" ]; then
    echo "ERREUR: $PY_SCRIPT introuvable" >&2
    exit 1
fi

exec python3 "$PY_SCRIPT" "$@"
