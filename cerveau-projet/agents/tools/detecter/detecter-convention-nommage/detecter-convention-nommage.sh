#!/usr/bin/env bash
# detecter-convention-nommage.sh
# Wrapper pur : execute la version Python (parite py/sh).
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$DIR/detecter-convention-nommage.py" "$@"
