#!/bin/bash
# lire-frontmatter.sh
# Extraire le frontmatter YAML en tete d'un fichier markdown
# Version : 0.2.0

VERSION="0.2.0"
STATUT="ebauche"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== lire-frontmatter v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier>"
    echo ""
    echo "Arguments :"
    echo "  <fichier>       Fichier markdown a analyser"
    echo ""
    echo "Options :"
    echo "  --champ <nom>   Afficher uniquement la valeur d'un champ (ex: statut)"
    echo "  --verbose       Afficher les details (presence/absence)"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md              # Afficher tout le frontmatter"
    echo "  $0 --champ statut fichier.md  # Afficher la valeur du champ statut"
    echo "  $0 --verbose fichier.md    # Detail avec presence/absence"
    echo ""
}

main() {
    local fichier=""
    local champ=""
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --champ) champ="$2"; shift 2 ;;
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
    
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve: $fichier${NC}"
        exit 1
    fi
    
    # Extraire le frontmatter : bloc delimite par --- en premiere et 3e ligne
    local contenu=""
    if [ "$verbose" = "true" ]; then
        contenu=$(awk 'NR==1 && /^---$/ {print; in_fm=1; next} in_fm && /^---$/ {print; exit} in_fm {print}' "$fichier")
    else
        contenu=$(awk 'NR==1 && /^---$/ {in_fm=1; next} in_fm && /^---$/ {exit} in_fm {print}' "$fichier")
    fi
    
    if [ -z "$contenu" ]; then
        if [ "$verbose" = "true" ]; then
            echo -e "${YELLOW}[INFO] Pas de frontmatter detecte en tete de $fichier${NC}"
        fi
        exit 0
    fi
    
    if [ -n "$champ" ]; then
        # Afficher uniquement la valeur du champ demande
        local valeur=$(echo "$contenu" | awk -v c="$champ" 'index($0, c ":") == 1 {sub(/^[^:]+:[[:space:]]*/, ""); print; exit}')
        if [ -z "$valeur" ]; then
            if [ "$verbose" = "true" ]; then
                echo -e "${YELLOW}[ERREUR] Champ '$champ' absent du frontmatter${NC}"
            fi
            exit 1
        fi
        echo "$valeur"
        exit 0
    fi
    
    echo "$contenu"
}

main "$@"
