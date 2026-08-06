#!/bin/bash
# copier-dossier.sh
# Copier un dossier recursivement vers une destination
# Version : 0.1.0-beta
# Statut : ebauche

VERSION="0.1.0-beta"
STATUT="ebauche"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== copier-dossier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <source> <destination>"
    echo ""
    echo "Arguments :"
    echo "  <source>        Dossier a copier (recursif)"
    echo "  <destination>   Dossier de destination"
    echo ""
    echo "Options :"
    echo "  --dry-run       Simuler sans copier"
    echo "  --verbose       Afficher les details"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 dossiers-src dossiers-dst"
    echo "  $0 --dry-run dossiers-src dossiers-dst"
    echo ""
}

main() {
    local source=""
    local destination=""
    local dry_run="false"
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run) dry_run="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$source" ]; then
                    source="$1"
                elif [ -z "$destination" ]; then
                    destination="$1"
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
    
    if [ -z "$source" ] || [ -z "$destination" ]; then
        echo -e "${RED}[ERREUR] Source et destination obligatoires${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ ! -d "$source" ]; then
        echo -e "${RED}[ERREUR] Source non trouvee ou pas un dossier: $source${NC}"
        exit 1
    fi
    
    # Anti-boucle : la destination ne doit pas etre dans la source
    case "$destination" in
        "$source"/*)
            echo -e "${RED}[ERREUR] La destination ($destination) est dans la source ($source)${NC}"
            exit 1
            ;;
    esac
    
    if [ -e "$destination" ]; then
        echo -e "${YELLOW}[INFO] La destination existe deja: $destination${NC}"
        echo -e "${YELLOW}[INFO] Le contenu sera fusionne/ecrase par cp -r${NC}"
    fi
    
    local nb_fichiers=$(find "$source" -type f 2>/dev/null | wc -l)
    
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}[INFO] Source: $source ($nb_fichiers fichiers)${NC}"
        echo -e "${BLUE}[INFO] Destination: $destination${NC}"
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] Copie simulee : $source -> $destination ($nb_fichiers fichiers)${NC}"
        exit 0
    fi
    
    cp -r "$source" "$destination"
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERREUR] La copie a echoue${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[OK] Copie terminee : $source -> $destination${NC}"
    echo -e "${GREEN}[INFO] $nb_fichiers fichiers copies${NC}"
}

main "$@"
