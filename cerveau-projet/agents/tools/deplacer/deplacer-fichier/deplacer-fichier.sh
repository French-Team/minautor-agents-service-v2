#!/bin/bash
# deplacer-fichier.sh
# Deplacer ou renommer un fichier vers une nouvelle destination
# Version : 0.3.0

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.3.1"
STATUT="prepare"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== deplacer-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <source> <destination>"
    echo ""
    echo "Arguments :"
    echo "  <source>        Fichier a deplacer ou renommer"
    echo "  <destination>   Nouveau chemin du fichier"
    echo ""
    echo "Options :"
    echo "  --forcer        Ecraser la destination si elle existe deja"
    echo "  --backup        Sauvegarder la destination en .bak avant ecrasement"
    echo "  --dry-run       Simuler sans deplacer"
    echo "  --verbose       Afficher les details"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 ancien.md nouveau.md"
    echo "  $0 src/x.md dst/x.md"
    echo "  $0 --dry-run source.md destination.md"
    echo ""
}

main() {
    local source=""
    local destination=""
    local forcer="false"
    local backup="false"
    local dry_run="false"
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --forcer) forcer="true"; shift ;;
            --backup) backup="true"; shift ;;
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
    
    if [ ! -f "$source" ]; then
        echo -e "${RED}[ERREUR] Source non trouvee ou pas un fichier: $source${NC}"
        exit 1
    fi
    
    if [ "$source" = "$destination" ]; then
        echo -e "${YELLOW}[INFO] Source et destination identiques, rien a faire${NC}"
        exit 0
    fi
    
    if [ -e "$destination" ]; then
        if [ "$forcer" != "true" ]; then
            echo -e "${RED}[ERREUR] La destination existe deja: $destination${NC}"
            echo -e "${YELLOW}[INFO] Utiliser --forcer pour ecraser, ou --backup pour sauvegarder avant${NC}"
            exit 1
        fi
        if [ "$backup" = "true" ]; then
            cp "$destination" "${destination}.bak"
            if [ "$verbose" = "true" ]; then
                echo -e "${BLUE}[INFO] Sauvegarde: ${destination}.bak${NC}"
            fi
        fi
    fi
    
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}[INFO] Source: $source${NC}"
        echo -e "${BLUE}[INFO] Destination: $destination${NC}"
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] Deplacement simule : $source -> $destination${NC}"
        exit 0
    fi
    
    # Creer le dossier parent de destination si besoin
    local dossier_dest=$(dirname "$destination")
    if [ "$dossier_dest" != "." ] && [ ! -d "$dossier_dest" ]; then
        mkdir -p "$dossier_dest"
        if [ $? -ne 0 ]; then
            echo -e "${RED}[ERREUR] Impossible de creer le dossier: $dossier_dest${NC}"
            exit 1
        fi
    fi
    
    mv "$source" "$destination"
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERREUR] Le deplacement a echoue${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[OK] Fichier deplace : $source -> $destination${NC}"
}

main "$@"
