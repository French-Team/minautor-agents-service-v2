#!/bin/bash
# ajouter-contenu-fichier.sh
# Ajouter du contenu a la fin d'un fichier (append)
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
    echo "=== ajouter-contenu-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier-cible> [contenu]"
    echo ""
    echo "Arguments :"
    echo "  <fichier-cible> Fichier a completer"
    echo "  [contenu]       Chaine a ajouter (ou --fichier source)"
    echo ""
    echo "Options :"
    echo "  --fichier <src> Ajouter le contenu d'un fichier source"
    echo "  --dry-run       Simuler sans modifier"
    echo "  --verbose       Afficher les details"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md \"Nouvelle ligne\""
    echo "  $0 fichier.md --fichier source.md"
    echo "  $0 --dry-run fichier.md \"contenu\""
    echo ""
}

main() {
    local cible=""
    local contenu=""
    local source=""
    local dry_run="false"
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --fichier) source="$2"; shift 2 ;;
            --dry-run) dry_run="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$cible" ]; then
                    cible="$1"
                elif [ -z "$contenu" ]; then
                    contenu="$1"
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
    
    if [ -z "$cible" ]; then
        echo -e "${RED}[ERREUR] Fichier cible obligatoire${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ ! -f "$cible" ]; then
        echo -e "${RED}[ERREUR] Fichier cible non trouve: $cible${NC}"
        exit 1
    fi
    
    if [ -n "$source" ]; then
        if [ ! -f "$source" ]; then
            echo -e "${RED}[ERREUR] Fichier source non trouve: $source${NC}"
            exit 1
        fi
        local nb_lignes=$(wc -l < "$source")
    elif [ -n "$contenu" ]; then
        local nb_lignes=$(echo "$contenu" | wc -l)
        if [ "$nb_lignes" -eq 0 ]; then
            nb_lignes=1
        fi
    else
        echo -e "${RED}[ERREUR] Aucun contenu a ajouter (chaine ou --fichier)${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}[INFO] Fichier cible: $cible${NC}"
        echo -e "${BLUE}[INFO] $nb_lignes ligne(s) a ajouter${NC}"
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] $nb_lignes ligne(s) seraient ajoutees a $cible${NC}"
        exit 0
    fi
    
    # S'assurer que le fichier se termine par un retour a la ligne
    if [ -s "$cible" ]; then
        local derniere=$(tail -c 1 "$cible")
        if [ -n "$derniere" ]; then
            printf '\n' >> "$cible"
        fi
    fi
    
    if [ -n "$source" ]; then
        cat "$source" >> "$cible"
    else
        printf '%s\n' "$contenu" >> "$cible"
    fi
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERREUR] L'ajout a echoue${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[OK] $nb_lignes ligne(s) ajoutee(s) a la fin de $cible${NC}"
}

main "$@"
