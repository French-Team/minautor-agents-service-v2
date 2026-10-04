#!/bin/bash
# lire-fichier.sh
# Lire le contenu complet d'un fichier
# Version : 0.4.2
# Statut : prepare

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.4.2"
STATUT="prepare"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== lire-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier>"
    echo ""
    echo "Options :"
    echo "  --debut N       Lire a partir de la ligne N"
    echo "  --fin N         Lire jusqu'a la ligne N"
    echo "  --lignes N      Lire les N premieres lignes"
    echo "  --verbose       Afficher les details"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md"
    echo "  $0 --lignes 10 fichier.md"
    echo "  $0 --debut 5 --fin 15 fichier.md"
    echo ""
}

# Main
main() {
    local fichier=""
    local debut=""
    local fin=""
    local lignes=""
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --debut) debut="$2"; shift 2 ;;
            --fin) fin="$2"; shift 2 ;;
            --lignes) lignes="$2"; shift 2 ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *) fichier="$1"; shift ;;
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
    
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve: $fichier${NC}"
        exit 1
    fi
    
    # Robustesse (round 4) : validation de la plage AVANT toute lecture.
    # Une plage invalide est refusee avec un message explicite : jamais de
    # 0 silencieux avec une sortie vide. (parite avec le .py)
    if [ -n "$lignes" ] && [ "$lignes" -lt 1 ]; then
        echo -e "${RED}[ERREUR] Plage invalide : --lignes doit etre >= 1 (recu: $lignes)${NC}"
        exit 1
    fi
    if [ -n "$debut" ] && [ "$debut" -lt 1 ]; then
        echo -e "${RED}[ERREUR] Plage invalide : --debut doit etre >= 1 (recu: $debut)${NC}"
        exit 1
    fi
    if [ -n "$fin" ] && [ "$fin" -lt 1 ]; then
        echo -e "${RED}[ERREUR] Plage invalide : --fin doit etre >= 1 (recu: $fin)${NC}"
        exit 1
    fi
    if [ -n "$debut" ] && [ -n "$fin" ] && [ "$debut" -gt "$fin" ]; then
        echo -e "${RED}[ERREUR] Plage invalide : --debut ($debut) > --fin ($fin)${NC}"
        exit 1
    fi
    
    if [ "$verbose" = "true" ]; then
        local total_lignes=$(wc -l < "$fichier")
        echo -e "${BLUE}[INFO] Fichier: $fichier ($total_lignes lignes)${NC}"
    fi
    
    # Construire la commande sed
    local cmd="cat"
    
    if [ -n "$lignes" ]; then
        cmd="head -n $lignes"
    elif [ -n "$debut" ] && [ -n "$fin" ]; then
        cmd="sed -n '${debut},${fin}p'"
    elif [ -n "$debut" ]; then
        cmd="sed -n '${debut},\$p'"
    elif [ -n "$fin" ]; then
        cmd="head -n $fin"
    fi
    
    # Executer
    eval "$cmd" "$fichier"
}

main "$@"