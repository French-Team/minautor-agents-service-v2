#!/bin/bash
# lire-lignes.sh
# Lire des lignes specifiques d'un fichier (par numero ou plage)
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
    echo "=== lire-lignes v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier> <debut> [fin]"
    echo ""
    echo "Arguments :"
    echo "  <fichier>       Fichier a lire"
    echo "  <debut>         Numero de la premiere ligne (1 = debut)"
    echo "  [fin]           Numero de la derniere ligne (defaut = debut)"
    echo ""
    echo "Options :"
    echo "  --verbose       Afficher les details"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md 5        # Lire la ligne 5"
    echo "  $0 fichier.md 5 15     # Lire les lignes 5 a 15"
    echo "  $0 --verbose fichier.md 10 20"
    echo ""
}

main() {
    local fichier=""
    local debut=""
    local fin=""
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$fichier" ]; then
                    fichier="$1"
                elif [ -z "$debut" ]; then
                    debut="$1"
                elif [ -z "$fin" ]; then
                    fin="$1"
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
    
    if [ -z "$fichier" ] || [ -z "$debut" ]; then
        echo -e "${RED}[ERREUR] Fichier et numero de ligne obligatoires${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve: $fichier${NC}"
        exit 1
    fi
    
    if ! [[ "$debut" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}[ERREUR] Le debut doit etre un nombre: $debut${NC}"
        exit 1
    fi
    
    if [ -z "$fin" ]; then
        fin="$debut"
    fi
    
    if ! [[ "$fin" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}[ERREUR] La fin doit etre un nombre: $fin${NC}"
        exit 1
    fi
    
    if [ "$debut" -lt 1 ]; then
        echo -e "${RED}[ERREUR] Le debut doit etre >= 1${NC}"
        exit 1
    fi
    
    if [ "$fin" -lt "$debut" ]; then
        echo -e "${RED}[ERREUR] La fin ($fin) doit etre >= au debut ($debut)${NC}"
        exit 1
    fi
    
    local total_lignes=$(wc -l < "$fichier")
    
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}[INFO] Fichier: $fichier ($total_lignes lignes)${NC}"
        echo -e "${BLUE}[INFO] Lecture des lignes $debut a $fin${NC}"
        echo "---"
    fi
    
    if [ "$debut" -gt "$total_lignes" ]; then
        echo -e "${YELLOW}[INFO] Le fichier n'a que $total_lignes lignes, rien a afficher${NC}"
        exit 0
    fi
    
    sed -n "${debut},${fin}p" "$fichier"
}

main "$@"
