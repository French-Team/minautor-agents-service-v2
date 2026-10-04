#!/bin/bash
# verifier-conformite-fiche.sh
# Verifie la conformite des fiches agents au template fiche-agent-template.md
# Proprietaire : Vulcain (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.1"

# Transmission de tous les arguments au script Python
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/verifier-conformite-fiche.py" "$@"
