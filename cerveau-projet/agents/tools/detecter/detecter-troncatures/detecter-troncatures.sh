#!/usr/bin/env bash
# detecter-troncatures.sh
# Detecte les elements tronques donc illisibles (fichiers trop longs,
# blocs non fermes, marqueurs de troncature).
#
# Usage :
#   detecter-troncatures.sh [OPTIONS] <fichier|dossier> [autres...]
#   detecter-troncatures.sh --tous
#
# Version : 0.2.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# Detection de la racine projet (la ou se trouve AGENTS.md)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RACINE="$SCRIPT_DIR"
while [ ! -f "$RACINE/AGENTS.md" ] && [ "$RACINE" != "/" ]; do
    RACINE="$(dirname "$RACINE")"
done

PYTHON="python3"
OUTIL_PY="$SCRIPT_DIR/detecter-troncatures.py"

if [ ! -f "$OUTIL_PY" ]; then
    echo "[ERREUR] Version Python introuvable: $OUTIL_PY" >&2
    exit 2
fi

cd "$RACINE" || exit 2
exec "$PYTHON" "$OUTIL_PY" "$@"
