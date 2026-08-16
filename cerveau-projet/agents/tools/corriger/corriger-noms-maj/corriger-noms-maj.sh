#!/bin/bash
# corriger-noms-maj.sh
# Corriger la casse et la forme des noms references (champ outil du registre)
# Version : 0.1.1
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.1.1"

# Repertoire de l'outil
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Delegue au .py (parite garantie)
exec python3 "$SCRIPT_DIR/corriger-noms-maj.py" "$@"
