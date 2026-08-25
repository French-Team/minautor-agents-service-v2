#!/bin/bash
# editer-fichier.sh
# Remplacer une chaine par une autre dans un fichier
# Version : 0.5.0
# Statut : prepare

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.5.0"
STATUT="prepare"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== editer-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier> <ancien> <nouveau>"
    echo ""
    echo "Options :"
    echo "  --global         Remplacer toutes les occurrences"
    echo "  --backup         Creer une sauvegarde .bak avant"
    echo "  --dry-run        Simuler sans modifier"
    echo "  --verbose        Afficher les details"
    echo "  --help           Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md \"ancien\" \"nouveau\""
    echo "  $0 --global fichier.md \"texte\" \"remplacement\""
    echo ""
}

# Main
main() {
    local fichier=""
    local ancien=""
    local nouveau=""
    local global="false"
    local backup="false"
    local dry_run="false"
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --global) global="true"; shift ;;
            --backup) backup="true"; shift ;;
            --dry-run) dry_run="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$fichier" ]; then
                    fichier="$1"
                elif [ -z "$ancien" ]; then
                    ancien="$1"
                elif [ -z "$nouveau" ]; then
                    nouveau="$1"
                fi
                shift
                ;;
        esac
    done
    
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    if [ -z "$fichier" ] || [ -z "$ancien" ]; then
        echo -e "${RED}[ERREUR] Arguments manquants${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve: $fichier${NC}"
        exit 1
    fi
    
    # Compter les occurrences
    local nb=$(grep -c "$ancien" "$fichier" 2>/dev/null || echo "0")
    
    if [ "$nb" = "0" ]; then
        echo -e "${RED}[ERREUR] Aucune occurrence de '$ancien' dans $fichier${NC}"
        echo -e "${YELLOW}  (verifiez l'indentation exacte et le contenu de la chaine)${NC}"
        exit 1
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] $nb occurrence(s) trouvee(s)${NC}"
        grep -n "$ancien" "$fichier" | head -5
        exit 0
    fi
    
    # Sauvegarde
    if [ "$backup" = "true" ]; then
        cp "$fichier" "${fichier}.bak"
        if [ "$verbose" = "true" ]; then
            echo -e "${BLUE}[INFO] Sauvegarde: ${fichier}.bak${NC}"
        fi
    fi
    
    # Remplacer
    if [ "$global" = "true" ]; then
        sed -i "s|$ancien|$nouveau|g" "$fichier"
    else
        sed -i "0,/$ancien/{
            s|$ancien|$nouveau|
        }" "$fichier"
    fi
    
    if [ "$verbose" = "true" ]; then
        echo -e "${GREEN}[OK] Remplacement effectue dans $fichier${NC}"
    fi
    
    exit 0
}

main "$@"