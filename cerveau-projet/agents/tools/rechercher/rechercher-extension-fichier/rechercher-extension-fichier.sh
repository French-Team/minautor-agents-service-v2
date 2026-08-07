#!/bin/bash
# rechercher-extension-fichier.sh
# Extraire l'extension d'un fichier (ou verifier une extension)
# Version : 0.2.0

VERSION="0.2.0"
STATUT="ebauche"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== rechercher-extension-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier>"
    echo ""
    echo "Arguments :"
    echo "  <fichier>       Fichier dont on veut l'extension"
    echo ""
    echo "Options :"
    echo "  --verifier <ext>  Verifier si le fichier a cette extension (retourne 0 si oui, 1 si non)"
    echo "  --verbose       Afficher les details"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md           # Affiche: md"
    echo "  $0 fichier.tar.gz       # Affiche: gz"
    echo "  $0 --verifier sh script.sh   # 0 si .sh, 1 sinon"
    echo "  $0 --verbose fichier.md"
    echo ""
}

main() {
    local fichier=""
    local verifier=""
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verifier) verifier="$2"; shift 2 ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$fichier" ]; then
                    fichier="$1"
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
    
    if [ -z "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier obligatoire${NC}"
        afficher_aide
        exit 1
    fi
    
    # Extraire l'extension (apres le dernier point, sans le point)
    local extension="${fichier##*.}"
    
    # Si pas de point, pas d'extension
    if [ "$extension" = "$fichier" ]; then
        extension=""
    fi
    
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}[INFO] Fichier: $fichier${NC}"
        echo -e "${BLUE}[INFO] Extension: ${extension:-aucune}${NC}"
        echo "---"
    fi
    
    if [ -n "$verifier" ]; then
        if [ "$extension" = "$verifier" ]; then
            if [ "$verbose" = "true" ]; then
                echo -e "${GREEN}[OK] Le fichier a bien l'extension .$verifier${NC}"
            fi
            exit 0
        else
            if [ "$verbose" = "true" ]; then
                echo -e "${YELLOW}[NON] Extension trouvee: ${extension:-aucune} (attendu: $verifier)${NC}"
            fi
            exit 1
        fi
    fi
    
    echo "$extension"
}

main "$@"
