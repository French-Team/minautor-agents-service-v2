#!/bin/bash
# rechercher-dossier.sh
# Verifier si un dossier existe
# Version : 0.2.0

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
STATUT="ebauche"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== rechercher-dossier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <chemin>"
    echo ""
    echo "Arguments :"
    echo "  <chemin>        Chemin du dossier a verifier"
    echo ""
    echo "Options :"
    echo "  --verbose       Afficher les details"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Code de sortie :"
    echo "  0 = le dossier existe"
    echo "  1 = le dossier n'existe pas"
    echo ""
    echo "Exemples :"
    echo "  $0 cerveau-projet/agents/tools"
    echo "  $0 --verbose chemin/dossier"
    echo ""
}

main() {
    local chemin=""
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$chemin" ]; then
                    chemin="$1"
                else
                    echo -e "${RED}[ERREUR] Trop d'arguments: $1${NC}"
                    afficher_aide
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    if [ -z "$chemin" ]; then
        echo -e "${RED}[ERREUR] Aucun chemin specifie${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ -d "$chemin" ]; then
        if [ "$verbose" = "true" ]; then
            echo -e "${BLUE}[INFO] Chemin verifie: $chemin${NC}"
        fi
        echo -e "${GREEN}[OK] Le dossier existe : $chemin${NC}"
        exit 0
    else
        if [ "$verbose" = "true" ]; then
            if [ -e "$chemin" ]; then
                echo -e "${YELLOW}[INFO] Le chemin existe mais n'est pas un dossier${NC}"
            else
                echo -e "${YELLOW}[INFO] Le chemin n'existe pas du tout${NC}"
            fi
        fi
        echo -e "${RED}[ERREUR] Le dossier n'existe pas : $chemin${NC}"
        exit 1
    fi
}

main "$@"
