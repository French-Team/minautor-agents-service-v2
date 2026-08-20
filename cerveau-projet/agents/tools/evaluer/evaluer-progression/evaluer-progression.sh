#!/usr/bin/env bash
# evaluer-progression.sh
# Evalue la progression du cerveau-projet en temps reel (criteres
# definissables jusqu a 100%) et l auto-amelioration (score % non plafonne,
# croissance exponentielle permise).
# Wrapper pur : transmet les arguments au .py (parite garantie par
# construction).
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/evaluer-progression.py"

if [ ! -f "$PY_SCRIPT" ]; then
    echo "ERREUR: $PY_SCRIPT introuvable" >&2
    exit 1
fi

exec python3 "$PY_SCRIPT" "$@"