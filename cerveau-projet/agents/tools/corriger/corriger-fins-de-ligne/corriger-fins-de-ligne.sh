#!/bin/bash
# corriger-fins-de-ligne.sh
# Convertit les fins de ligne CRLF vers LF sur un fichier ou un dossier (--recursive)
# Version : 0.1.0
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.1.1"

set -e

# Wrapper pur : toute la logique vit dans le .py (parite garantie par construction)
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$DIR/corriger-fins-de-ligne.py" "$@"
