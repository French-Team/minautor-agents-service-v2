#!/bin/bash
# supprimer-fichier.sh
# Supprimer un fichier avec verification
# Version : 0.1.0-beta
# Statut : ebauche

VERSION="0.2.0"
STATUT="prepare"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== supprimer-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier>"
    echo ""
    echo "Options :"
    echo "  --forcer         Supprimer sans confirmer"
    echo "  --dry-run        Simuler sans supprimer"
    echo "  --verbose        Afficher les details"
    echo "  --help           Afficher cette aide"
    echo ""
}

# Main
main() {
    local fichier=""
    local forcer="false"
    local dry_run="false"
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --forcer) forcer="true"; shift ;;
            --dry-run) dry_run="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *) fichier="$1"; shift ;;
        esac
    done
    
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    if [ -z "$fichier" ]; then
        echo -e "${RED}[ERREUR] Aucun fichier specifie${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ ! -f "$fichier" ]; then
        echo -e "${YELLOW}[INFO] Fichier inexistant: $fichier${NC}"
        exit 0
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] Suppression: $fichier${NC}"
        exit 0
    fi
    
    rm "$fichier"
    
    if [ "$verbose" = "true" ]; then
        echo -e "${GREEN}[OK] Supprime: $fichier${NC}"
    fi
    
    exit 0
}

main "$@"