#!/usr/bin/env bash
# detecter-fins-passives.sh
# Wrapper bash : delegue au detecter-fins-passives.py (Parite py/sh).
# Version : 0.1.0
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.1.0"
STATUT="prepare"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Chercher le projet a la racine (AGENTS.md)
racine="$SCRIPT_DIR"
while [ ! -f "$racine/AGENTS.md" ] && [ "$racine" != "/" ]; do
    racine="$(dirname "$racine")"
done

exec python3 "$SCRIPT_DIR/detecter-fins-passives.py" "$@"