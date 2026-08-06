#!/bin/bash
# lister-appels.sh
# Lister les appels de fonctions dans un fichier
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
    echo "  lister-appels v${VERSION}"
    echo "  Lister les appels de fonctions"
    echo "=========================================="
    echo ""
    echo "Usage: lister-appels [OPTIONS] FICHIER"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les détails"
    echo "  --version           Afficher la version"
    echo "  --unique, -u        Afficher uniquement les appels uniques"
    echo ""
    echo "Arguments:"
    echo "  FICHIER             Fichier à analyser"
    echo ""
    echo "Exemples:"
    echo "  lister-appels script.sh"
    echo "  lister-appels --unique script.py"
    echo ""
}

# Fonction pour lister les appels de fonctions
lister_appels() {
    local fichier=$1
    local verbose=$2
    local unique=$3

    echo -e "${BLUE}[RECHERCHE] Appels de fonctions dans : ${fichier}${NC}"
    echo ""

    # Détecter le type de fichier
    local extension="${fichier##*.}"

    case $extension in
        sh|bash)
            # Scripts Bash - chercher les appels de fonctions
            echo -e "${BLUE}Type : Script Bash${NC}"
            echo ""
            
            if [[ "$unique" == "true" ]]; then
                # Extraire les noms de fonctions appelées (uniquement les uniques)
                grep -oE '[a-zA-Z_][a-zA-Z0-9_]*\(\)' "$fichier" 2>/dev/null | \
                    sed 's/()//' | \
                    sort -u | \
                    while read -r func; do
                        echo -e "${GREEN}[TELEPHONE] ${func}${NC}"
                    done
            else
                # Extraire tous les appels de fonctions
                grep -nE '[a-zA-Z_][a-zA-Z0-9_]*\(\)' "$fichier" 2>/dev/null | \
                    while IFS=: read -r num ligne; do
                        echo -e "${YELLOW}Ligne ${num}:${NC} $(echo "$ligne" | xargs)"
                    done
            fi
            ;;
        py)
            # Scripts Python - chercher les appels de fonctions
            echo -e "${BLUE}Type : Script Python${NC}"
            echo ""
            
            if [[ "$unique" == "true" ]]; then
                # Extraire les noms de fonctions appelées (uniquement les uniques)
                grep -oE '[a-zA-Z_][a-zA-Z0-9_]*\(' "$fichier" 2>/dev/null | \
                    sed 's/($//' | \
                    sort -u | \
                    while read -r func; do
                        echo -e "${GREEN}[TELEPHONE] ${func}${NC}"
                    done
            else
                # Extraire tous les appels de fonctions
                grep -nE '[a-zA-Z_][a-zA-Z0-9_]*\(' "$fichier" 2>/dev/null | \
                    while IFS=: read -r num ligne; do
                        echo -e "${YELLOW}Ligne ${num}:${NC} $(echo "$ligne" | xargs)"
                    done
            fi
            ;;
        js|ts)
            # Scripts JavaScript/TypeScript - chercher les appels de fonctions
            echo -e "${BLUE}Type : Script JavaScript/TypeScript${NC}"
            echo ""
            
            if [[ "$unique" == "true" ]]; then
                # Extraire les noms de fonctions appelées (uniquement les uniques)
                grep -oE '[a-zA-Z_][a-zA-Z0-9_]*\(' "$fichier" 2>/dev/null | \
                    sed 's/($//' | \
                    sort -u | \
                    while read -r func; do
                        echo -e "${GREEN}[TELEPHONE] ${func}${NC}"
                    done
            else
                # Extraire tous les appels de fonctions
                grep -nE '[a-zA-Z_][a-zA-Z0-9_]*\(' "$fichier" 2>/dev/null | \
                    while IFS=: read -r num ligne; do
                        echo -e "${YELLOW}Ligne ${num}:${NC} $(echo "$ligne" | xargs)"
                    done
            fi
            ;;
        *)
            echo -e "${YELLOW}Type de fichier non pris en charge : ${extension}${NC}"
            echo "Formats supportés : sh, bash, py, js, ts"
            return 1
            ;;
    esac

    echo ""
    echo -e "${BLUE}Terminé.${NC}"
}

# Valeurs par défaut
VERBOSE="false"
UNIQUE="false"

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --aide|-h)
            aide
            exit 0
            ;;
        --verbose|-v)
            VERBOSE="true"
            shift
            ;;
        --version)
            echo "lister-appels v${VERSION}"
            exit 0
            ;;
        --unique|-u)
            UNIQUE="true"
            shift
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

# Exécution
lister_appels "$FICHIER" "$VERBOSE" "$UNIQUE"

exit $?
