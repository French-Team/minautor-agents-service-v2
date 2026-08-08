#!/bin/bash
# rechercher-texte.sh
# Rechercher un pattern dans un fichier
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
    echo "=== rechercher-texte v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <pattern> <fichier>"
    echo ""
    echo "Options :"
    echo "  --insensible     Ignorer la casse"
    echo "  --numeros        Afficher les numeros de ligne"
    echo "  --inverser       Afficher les lignes qui ne matchent pas"
    echo "  --compter        Compter les occurrences"
    echo "  --verbose        Afficher les details"
    echo "  --help           Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 \"mot\" fichier.md"
    echo "  $0 --insensible --numeros \"texte\" fichier.md"
    echo ""
}

# Main
main() {
    local pattern=""
    local fichier=""
    local insensible="false"
    local numeros="false"
    local inverser="false"
    local compter="false"
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --insensible) insensible="true"; shift ;;
            --numeros) numeros="true"; shift ;;
            --inverser) inverser="true"; shift ;;
            --compter) compter="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$pattern" ]; then
                    pattern="$1"
                elif [ -z "$fichier" ]; then
                    fichier="$1"
                fi
                shift
                ;;
        esac
    done
    
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    if [ -z "$pattern" ] || [ -z "$fichier" ]; then
        echo -e "${RED}[ERREUR] Pattern et fichier requis${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve: $fichier${NC}"
        exit 1
    fi
    
    # Construire les options grep
    local opts=""
    if [ "$insensible" = "true" ]; then
        opts="$opts -i"
    fi
    if [ "$numeros" = "true" ]; then
        opts="$opts -n"
    fi
    if [ "$inverser" = "true" ]; then
        opts="$opts -v"
    fi
    
    # Executer
    if [ "$compter" = "true" ]; then
        local nb=$(grep $opts -c "$pattern" "$fichier" 2>/dev/null || echo "0")
        if [ "$verbose" = "true" ]; then
            echo -e "${BLUE}$nb occurrences dans $fichier${NC}"
        else
            echo "$nb"
        fi
    else
        grep $opts "$pattern" "$fichier"
    fi
    
    exit $?
}

main "$@"