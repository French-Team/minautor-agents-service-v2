#!/bin/bash
# detecter-residus.sh
# Wrapper bash de detecter-residus.py (detection des residus par zone)
# Proprietaire : Hygie (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.1.3"

DIR="$(cd "$(dirname "$0")" && pwd)"

# Aide courte
if [ "$1" = "--aide" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: detecter-residus.sh [--zone <cerveau-projet|workspace|tous>] [--detail] [--rapport <fichier>] [--verbose] [--version]"
    echo ""
    echo "Detecte les residus du workspace, compartimente par zone :"
    echo "  TEMP        : scripts/dossiers temporaires (tmp-*/.zz-*/.tmp-*)"
    echo "  VERSION     : fichiers de version semver a la racine"
    echo "  SAUVEGARDE  : fichiers de sauvegarde (*.bak, *~, *.orig)"
    echo "  RAPPORT_EGARE : rapports/audits egare hors des dossiers de rapport"
    echo "  CACHE       : dossiers __pycache__ et fichiers .pyc"
    exit 0
fi

python3 "$DIR/detecter-residus.py" "$@"
