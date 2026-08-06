#!/bin/bash
# lister-fonctions.sh
# Liste les fonctions d'un fichier
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
    echo "  lister-fonctions v${VERSION}"
    echo "  Liste les fonctions d'un fichier"
    echo "=========================================="
    echo ""
    echo "Usage: lister-fonctions [OPTIONS] FICHIER"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --type TYPE         Type de fichier: bash, python, js (défaut: auto)"
    echo "  --version           Afficher la version"
    echo ""
    echo "Arguments:"
    echo "  FICHIER             Fichier à analyser"
    echo ""
    echo "Exemples:"
    echo "  lister-fonctions script.sh"
    echo "  lister-fonctions --type python module.py"
    echo ""
}

# Fonction pour lister les fonctions bash
lister_fonctions_bash() {
    local fichier=$1
    grep -n "^[a-zA-Z_][a-zA-Z0-9_]*() {" "$fichier" 2>/dev/null | sed 's/() {//' | sed 's/^[[:space:]]*//'
}

# Fonction pour lister les fonctions Python
lister_fonctions_python() {
    local fichier=$1
    grep -n "^def " "$fichier" 2>/dev/null | sed 's/^def //' | sed 's/://' | sed 's/^[[:space:]]*//'
}

# Fonction pour lister les fonctions JavaScript
lister_fonctions_js() {
    local fichier=$1
    grep -n "function " "$fichier" 2>/dev/null | sed 's/function //' | sed 's/ {//' | sed 's/^[[:space:]]*//'
}

# Fonction pour détecter le type de fichier
detecter_type() {
    local fichier=$1
    local extension="${fichier##*.}"
    
    case $extension in
        sh|bash)
            echo "bash"
            ;;
        py)
            echo "python"
            ;;
        js|jsx|ts|tsx)
            echo "js"
            ;;
        *)
            echo "bash"  # Par défaut
            ;;
    esac
}

# Valeurs par défaut
TYPE="auto"

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --aide|-h)
            aide
            exit 0
            ;;
        --type)
            TYPE="$2"
            shift 2
            ;;
        --version)
            echo "lister-fonctions v${VERSION}"
            exit 0
            ;;
        -*)
            echo "Option inconnue: $1"
            echo "Utilisez --aide pour l'aide"
            exit 1
            ;;
        *)
            FICHIER="$1"
            shift
            ;;
    esac
done

# Vérification du fichier
if [[ -z "$FICHIER" ]]; then
    echo "Erreur: Aucun fichier spécifié"
    echo "Utilisez --aide pour l'aide"
    exit 1
fi

if [[ ! -f "$FICHIER" ]]; then
    echo "Erreur: Le fichier '$FICHIER' n'existe pas"
    exit 1
fi

# Détection du type si nécessaire
if [[ "$TYPE" == "auto" ]]; then
    TYPE=$(detecter_type "$FICHIER")
fi

# Exécution
echo -e "${BLUE}🔍 Fonctions dans : ${FICHIER}${NC}"
echo ""

case $TYPE in
    bash)
        lister_fonctions_bash "$FICHIER"
        ;;
    python)
        lister_fonctions_python "$FICHIER"
        ;;
    js)
        lister_fonctions_js "$FICHIER"
        ;;
    *)
        echo "Type non supporté: $TYPE"
        exit 1
        ;;
esac

exit 0
