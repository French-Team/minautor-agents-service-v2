#!/bin/bash
# detecter-divergences-version.sh
# Detecte les spec/ dont la version diverge de celle du .py associe
# (regle des 5 fichiers). Wrapper bash du .py (parite).
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

VERSION="0.1.0"
STATUT="ebauche"

if [ "$1" = "--version" ]; then
    echo "detecter-divergences-version v${VERSION}"
    exit 0
fi

python3 "$(dirname "$0")/detecter-divergences-version.py" "$@"
exit $?
