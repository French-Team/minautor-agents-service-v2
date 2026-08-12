#!/usr/bin/env bash
# -*- coding: ascii -*-
# generateurs-amelioration.sh
# Wrapper pur : transmet les arguments au .py (parite garantie par construction).
# Version : 2.1.0
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/generateurs-amelioration.py"

if [ ! -f "$PY_SCRIPT" ]; then
    echo "ERREUR: $PY_SCRIPT introuvable" >&2
    exit 1
fi

exec python3 "$PY_SCRIPT" "$@"
