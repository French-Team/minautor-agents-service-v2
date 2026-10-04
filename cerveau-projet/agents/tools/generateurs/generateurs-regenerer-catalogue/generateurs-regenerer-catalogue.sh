#!/usr/bin/env bash
# =============================================================================
# generateurs-regenerer-catalogue.sh
# Wrapper bash de generateurs-regenerer-catalogue.py (parite py/sh).
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
set -euo pipefail

REPERTOIRE_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec python3 "$REPERTOIRE_SCRIPT/generateurs-regenerer-catalogue.py" "$@"
