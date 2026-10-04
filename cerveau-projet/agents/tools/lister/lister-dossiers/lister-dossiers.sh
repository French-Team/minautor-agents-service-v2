#!/bin/bash
# lister-dossiers.sh
# Liste les dossiers d'un chemin donne
# Version: 0.1.0
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
DATE="2026-08-05"

# Couleurs pour la sortie
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'aide
aide() {
    echo "=========================================="
    echo "  lister-dossiers v${VERSION}"
    echo "  Liste les dossiers d'un chemin"
    echo "=========================================="
    echo ""
    echo "Usage: lister-dossiers [OPTIONS] [CHEMIN]"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --recursif, -r      Explorer les sous-dossiers"
    echo "  --version           Afficher la version"
    echo ""
    echo "Arguments:"
    echo "  CHEMIN              Chemin du dossier (defaut: .)"
    echo ""
    echo "Exemples:"
    echo "  lister-dossiers"
    echo "  lister-dossiers /chemin/vers/dossier"
    echo "  lister-dossiers --recursif"
    echo "  lister-dossiers -r cerveau-projet"
    echo ""
}

# Fonction pour lister les dossiers
lister_dossiers() {
    local chemin=$1
    local recursif=$2
    
    if [[ "$recursif" == "true" ]]; then
        # Mode recursif
        find "$chemin" -type d 2>/dev/null | sort
    else
        # Mode non recursif
        if [[ -d "$chemin" ]]; then
            ls -d "$chemin"/*/ 2>/dev/null | sed "s|^\./||" | sed "s|/$||" | sort
        else
            echo "Erreur: Le chemin '$chemin' n'existe pas ou n'est pas un dossier"
            exit 1
        fi
    fi
}

# Valeurs par defaut
CHEMIN="."
RECURSIF="false"

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --aide|-h)
            aide
            exit 0
            ;;
        --recursif|-r)
            RECURSIF="true"
            shift
            ;;
        --version)
            echo "lister-dossiers v${VERSION}"
            exit 0
            ;;
        -*)
            echo "Option inconnue: $1"
            echo "Utilisez --aide pour l'aide"
            exit 1
            ;;
        *)
            CHEMIN="$1"
            shift
            ;;
    esac
done

# Verification que le chemin existe
if [[ ! -e "$CHEMIN" ]]; then
    echo "Erreur: Le chemin '$CHEMIN' n'existe pas"
    exit 1
fi

# Execution
echo -e "${BLUE}[DOSSIER] Dossiers dans : ${CHEMIN}${NC}"
echo ""

lister_dossiers "$CHEMIN" "$RECURSIF"

exit 0
