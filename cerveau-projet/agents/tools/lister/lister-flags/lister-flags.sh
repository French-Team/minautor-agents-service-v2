#!/usr/bin/env bash
# lister-flags.sh
# Wrapper Bash : delegue a lister-flags.py.
# Version : 0.1.1
# Statut : prepare
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

VERSION="0.1.1"
STATUT="prepare"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/lister-flags.py" "$@"
