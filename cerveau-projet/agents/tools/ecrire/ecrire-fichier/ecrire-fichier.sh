#!/bin/bash
# ecrire-fichier.sh
# Ecrire/echraser le contenu d'un fichier
# Version : 0.3.0
# Statut : prepare

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.3.2"
STATUT="prepare"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== ecrire-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier> [contenu]"
    echo ""
    echo "Options :"
    echo "  --backup         Creer une sauvegarde .bak avant"
    echo "  --dry-run        Simuler sans ecrire"
    echo "  --verbose        Afficher les details"
    echo "  --help           Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md \"# Nouveau contenu\""
    echo "  echo \"texte\" | $0 fichier.md -"
    echo ""
}

# Main
main() {
    local fichier=""
    local contenu=""
    local backup="false"
    local dry_run="false"
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --backup) backup="true"; shift ;;
            --dry-run) dry_run="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$fichier" ]; then
                    fichier="$1"
                elif [ "$contenu" = "" ] && [ "$1" != "-" ]; then
                    contenu="$1"
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
        echo -e "${RED}[ERREUR] Aucun fichier specifie${NC}"
        afficher_aide
        exit 1
    fi
    
    # Lire le contenu depuis stdin si "-"
    if [ "$contenu" = "-" ] || { [ -z "$contenu" ] && [ ! -t 0 ]; }; then
        contenu=$(cat)
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] Ecriture dans: $fichier${NC}"
        exit 0
    fi
    
    # Sauvegarde si demande
    if [ "$backup" = "true" ] && [ -f "$fichier" ]; then
        cp "$fichier" "${fichier}.bak"
        if [ "$verbose" = "true" ]; then
            echo -e "${BLUE}[INFO] Sauvegarde creee: ${fichier}.bak${NC}"
        fi
    fi
    
    # Ecrire. Contenu vide = fichier tronque a zero octet (jamais de no-op
    # silencieux : vider un fichier est une action explicite et le message
    # le confirme). Le .py fait la meme chose.
    if [ -n "$contenu" ]; then
        echo "$contenu" > "$fichier"
        if [ "$verbose" = "true" ]; then
            echo -e "${GREEN}[OK] Fichier ecrit: $fichier${NC}"
        fi
    else
        : > "$fichier"
        echo -e "${YELLOW}[INFO] Contenu vide : fichier tronque a zero octet: $fichier${NC}"
    fi
    
    exit 0
}

main "$@"