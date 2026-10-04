#!/usr/bin/env bash
# executer-script-temporaire.sh
# ENTONNOIR (parite bash) : normalise puis execute un script temporaire.
# Usage : bash executer-script-temporaire.sh <script.py> [args...]
# Version : 0.1.3
# Statut : ebauche

set -u

# Detection racine projet (AGENTS.md)
RACINE=""
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
while [ -n "$DIR" ]; do
  if [ -f "$DIR/AGENTS.md" ]; then
    RACINE="$DIR"
    break
  fi
  DIR="${DIR%/*}"
done
if [ -z "$RACINE" ]; then
  echo "[ERREUR] Racine projet non trouvee (AGENTS.md introuvable)" >&2
  exit 2
fi

OUTIL="$RACINE/cerveau-projet/agents/tools/executer/executer-script-temporaire/executer-script-temporaire.py"

if [ "${1:-}" = "--version" ] || [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  python3 "$OUTIL" "$@"
  exit $?
fi

exec python3 "$OUTIL" "$@"
