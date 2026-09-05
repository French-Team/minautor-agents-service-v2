#!/usr/bin/env bash
# -*- coding: ascii -*-
# valider-case.sh
# Wrapper pur : transmet les arguments au .py (parite garantie par construction).
# Version : 1.1.1
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/valider-case.py"

if [ ! -f "$PY_SCRIPT" ]; then
    echo "ERREUR: $PY_SCRIPT introuvable" >&2
    exit 1
fi

exec python3 "$PY_SCRIPT" "$@"
