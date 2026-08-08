#!/bin/bash
# copier-fichier.sh
# Copier un fichier vers une destination
# Version : 0.1.0-beta
# Statut : ebauche

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
STATUT="prepare"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== copier-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <source> <destination>"
    echo ""
    echo "Options :"
    echo "  --forcer         Ecraser si la destination existe"
    echo "  --dry-run        Simuler sans copier"
    echo "  --verbose        Afficher les details"
    echo "  --help           Afficher cette aide"
    echo ""
}

# Main
main() {
    local source=""
    local destination=""
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
            *)
                if [ -z "$source" ]; then
                    source="$1"
                elif [ -z "$destination" ]; then
                    destination="$1"
                fi
                shift
                ;;
        esac
    done
    
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    if [ -z "$source" ] || [ -z "$destination" ]; then
        echo -e "${RED}[ERREUR] Source et destination requises${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ ! -f "$source" ]; then
        echo -e "${RED}[ERREUR] Source non trouvee: $source${NC}"
        exit 1
    fi
    
    if [ -f "$destination" ] && [ "$forcer" = "false" ]; then
        echo -e "${RED}[ERREUR] Destination existe deja: $destination${NC}"
        echo -e "${YELLOW}[INFO] Utiliser --forcer pour ecraser${NC}"
        exit 1
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] Copie: $source -> $destination${NC}"
        exit 0
    fi
    
    # Creer le repertoire parent si necessaire
    local dossier=$(dirname "$destination")
    if [ ! -d "$dossier" ]; then
        mkdir -p "$dossier"
    fi
    
    cp "$source" "$destination"
    
    if [ "$verbose" = "true" ]; then
        echo -e "${GREEN}[OK] Copie: $source -> $destination${NC}"
    fi
    
    exit 0
}

main "$@"