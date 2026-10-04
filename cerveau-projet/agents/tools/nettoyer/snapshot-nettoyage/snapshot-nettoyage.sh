#!/bin/bash
# snapshot-nettoyage.sh
# Wrapper bash de snapshot-nettoyage.py (snapshot du workspace avant nettoyage)
# Proprietaire : Hygie (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.1.0"

DIR="$(cd "$(dirname "$0")" && pwd)"

# Aide courte
if [ "$1" = "--aide" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: snapshot-nettoyage.sh <creer|consulter|rotation|liste> [--version]"
    echo ""
    echo "Snapshot de l etat du workspace avant nettoyage (agent Hygie) :"
    echo "  creer     : prend un snapshot de l etat actuel (dossier hygie/snapshots/)"
    echo "  consulter : affiche le snapshot precedent"
    echo "  rotation  : supprime les snapshots de plus de 7 jours"
    echo "  liste     : liste les snapshots existants"
    exit 0
fi

python3 "$DIR/snapshot-nettoyage.py" "$@"
