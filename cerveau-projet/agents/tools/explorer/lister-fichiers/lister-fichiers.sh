#!/bin/bash
# lister-fichiers.sh
# Liste les fichiers d'un chemin donné
# Version: 0.1.0
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
VERSION="0.1.0"
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
    echo "  lister-fichiers v${VERSION}"
    echo "  Liste les fichiers d'un chemin"
    echo "=========================================="
    echo ""
    echo "Usage: lister-fichiers [OPTIONS] [CHEMIN]"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --recursif, -r      Explorer les sous-dossiers"
    echo "  --extension EXT     Filtrer par extension"
    echo "  --version           Afficher la version"
    echo ""
    echo "Arguments:"
    echo "  CHEMIN              Chemin du dossier (défaut: .)"
    echo ""
    echo "Exemples:"
    echo "  lister-fichiers"
    echo "  lister-fichiers /chemin/vers/dossier"
    echo "  lister-fichiers --recursif --extension md"
    echo ""
}

# Fonction pour lister les fichiers
lister_fichiers() {
    local chemin=$1
    local recursif=$2
    local extension=$3
    
    if [[ "$recursif" == "true" ]]; then
        # Mode récursif
        if [[ -n "$extension" ]]; then
            find "$chemin" -type f -name "*.$extension" 2>/dev/null | sort
        else
            find "$chemin" -type f 2>/dev/null | sort
        fi
    else
        # Mode non récursif
        if [[ -d "$chemin" ]]; then
            if [[ -n "$extension" ]]; then
                ls -1 "$chemin"/*."$extension" 2>/dev/null | sed "s|^\./||" | sort
            else
                ls -1 "$chemin" 2>/dev/null | sed "s|^\./||" | sort
            fi
        else
            echo "Erreur: Le chemin '$chemin' n'existe pas ou n'est pas un dossier"
            exit 1
        fi
    fi
}

# Valeurs par défaut
CHEMIN="."
RECURSIF="false"
EXTENSION=""

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
        --extension)
            EXTENSION="$2"
            shift 2
            ;;
        --version)
            echo "lister-fichiers v${VERSION}"
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

# Vérification que le chemin existe
if [[ ! -e "$CHEMIN" ]]; then
    echo "Erreur: Le chemin '$CHEMIN' n'existe pas"
    exit 1
fi

# Exécution
echo -e "${BLUE}📄 Fichiers dans : ${CHEMIN}${NC}"
echo ""

lister_fichiers "$CHEMIN" "$RECURSIF" "$EXTENSION"

exit 0
