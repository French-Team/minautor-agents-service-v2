#!/bin/bash
# analyser-noms-maj.sh
# Analyser la casse et la forme des noms references (orphelins, min/MAJ)
# Version : 0.1.0
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.1.0"

# Repertoire de l'outil
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Delegue au .py (parite garantie)
exec python3 "$SCRIPT_DIR/analyser-noms-maj.py" "$@"
