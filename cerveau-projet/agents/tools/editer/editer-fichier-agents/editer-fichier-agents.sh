#!/usr/bin/env bash
# -*- coding: ascii -*-
# editer-fichier-agents.sh -- wrapper pur exec python3 (parite avec le .py)
# Edite les fiches des agents (.md) : ligne ou bloc (titre markdown),
# supprimer/remplacer/ajouter, avec correcteur ASCII integre (--ascii).
# Dry-run + backup pour securiser les modifications.
# Version : 0.1.0-beta
# Statut : beta

set -euo pipefail

# Repertoire de ce script (quelles que soient les symlinks)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/editer-fichier-agents.py"

# Parite --version : le .sh retourne exactement la version du .py
if [ "${1:-}" = "--version" ]; then
    exec python3 "$PYTHON_SCRIPT" --version
fi

exec python3 "$PYTHON_SCRIPT" "$@"
