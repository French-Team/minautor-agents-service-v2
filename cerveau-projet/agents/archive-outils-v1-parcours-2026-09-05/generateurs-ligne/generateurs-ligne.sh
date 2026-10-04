#!/usr/bin/env bash
# -*- coding: ascii -*-
# generateurs-ligne.sh -- wrapper pur exec python3 (parite avec le .py)
# Ajoute une LIGNE (chemin de bout en bout) a une carte de decision via des
# gabarits de groupes de cases (configs), apres verification de la carte
# cartographique d'Atlas. Dry/wet pour valider. Les configs sont
# externalisees dans gabarits-ligne.json et extensibles via ajouter-config.
# Version : 0.3.0
# Statut : ebauche

set -euo pipefail

# Repertoire de ce script (quelles que soient les symlinks)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/generateurs-ligne.py"

# Parite --version : le .sh retourne exactement la version du .py
if [ "${1:-}" = "--version" ]; then
    exec python3 "$PYTHON_SCRIPT" --version
fi

exec python3 "$PYTHON_SCRIPT" "$@"
