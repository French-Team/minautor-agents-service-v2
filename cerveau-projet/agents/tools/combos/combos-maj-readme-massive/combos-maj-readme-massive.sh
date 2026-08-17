#!/bin/bash
# combos-maj-readme-massive.sh
# Combo maj-readme-massive : GROSSE mise a jour conservative du README
# (analyse -> verifier -> maj -> correctifs -> ASCII -> rapport)
# Proprietaire : Clio (outil partage)
# Version : 0.1.6

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.1.6"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== combos-maj-readme-massive v${VERSION} ==="
    echo ""
    echo "Usage: $0 [RACINE] [OPTIONS]"
    echo ""
    echo "Combo maj-readme-massive : grosse mise a jour conservative du README."
    echo ""
    echo "Options:"
    echo "  --rapport   Sauvegarder le rapport dans clio/rapports/"
    echo "  --help      Afficher cette aide"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RACINE="${1:-.}"
SAUVEGARDER=false

while [ $# -gt 0 ]; do
    case $1 in
        --rapport) SAUVEGARDER=true; shift ;;
        --help|-h) afficher_aide; exit 0 ;;
        *) RACINE="$1"; shift ;;
    esac
done

echo -e "${BLUE}=== combos-maj-readme-massive v${VERSION} ===${NC}"
echo "Racine : $RACINE"
echo "Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

if [ ! -f "$RACINE/README.md" ]; then
    echo -e "${RED}[ERREUR] README.md introuvable a la racine${NC}"
    exit 1
fi

# Delegation : la logique Python est la source de verite (parite py/sh)
PY="$SCRIPT_DIR/combos-maj-readme-massive.py"
if [ -f "$PY" ]; then
    python3 "$PY" "$RACINE" ${SAUVEGARDER:+--rapport}
    exit $?
fi

echo -e "${RED}[ERREUR] combos-maj-readme-massive.py introuvable - impossible de poursuivre${NC}"
exit 1
