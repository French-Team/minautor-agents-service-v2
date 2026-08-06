#!/bin/bash
# supprimer-dossier.sh
# Supprimer un dossier recursivement (avec protections)
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
    echo "=== supprimer-dossier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <dossier>"
    echo ""
    echo "Arguments :"
    echo "  <dossier>       Dossier a supprimer (recursif)"
    echo ""
    echo "Options :"
    echo "  --force         Executer la suppression (sans : dry-run)"
    echo "  --verbose       Afficher les details"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 dossier-temporaire          # Dry-run"
    echo "  $0 --force dossier-temporaire  # Suppression reelle"
    echo "  $0 --force --verbose dossier/"
    echo ""
}

main() {
    local dossier=""
    local force="false"
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force) force="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$dossier" ]; then
                    dossier="$1"
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
    
    if [ -z "$dossier" ]; then
        echo -e "${RED}[ERREUR] Aucun dossier specifie${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ ! -d "$dossier" ]; then
        echo -e "${RED}[ERREUR] Dossier non trouve ou pas un dossier: $dossier${NC}"
        exit 1
    fi
    
    # Normaliser le chemin (supprimer les / finaux)
    dossier=$(echo "$dossier" | sed 's:/*$::')
    
    # PROTECTION : chemins sensibles absolument interdits
    case "$dossier" in
        ""|"/"|"."|".."|"./"|"../")
            echo -e "${RED}[ERREUR] Suppression interdite de ce chemin sensible: $dossier${NC}"
            exit 1
            ;;
    esac
    
    # PROTECTION : ne pas supprimer la racine du projet ni le dossier des outils
    local racine_abs=$(cd "$(dirname "$0")/../../../.." 2>/dev/null && pwd)
    local cible_abs=$(cd "$dossier" 2>/dev/null && pwd)
    if [ "$cible_abs" = "$racine_abs" ]; then
        echo -e "${RED}[ERREUR] Refus : ce dossier est la racine du projet${NC}"
        exit 1
    fi
    case "$dossier" in
        "cerveau-projet/agents/tools")
            echo -e "${RED}[ERREUR] Refus : ce dossier contient les outils partages${NC}"
            exit 1
            ;;
    esac
    
    local nb_fichiers=$(find "$dossier" -type f 2>/dev/null | wc -l)
    local nb_dossiers=$(find "$dossier" -type d 2>/dev/null | wc -l)
    nb_dossiers=$((nb_dossiers - 1))  # exclure le dossier racine lui-meme
    
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}[INFO] Dossier cible: $dossier${NC}"
        echo -e "${BLUE}[INFO] Contenu: $nb_fichiers fichiers, $nb_dossiers sous-dossiers${NC}"
    fi
    
    if [ "$force" != "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] Aucune suppression effectuee (utiliser --force pour executer)${NC}"
        echo -e "${YELLOW}[INFO] $nb_fichiers fichiers et $nb_dossiers dossiers seraient supprimes${NC}"
        exit 0
    fi
    
    rm -rf "$dossier"
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERREUR] La suppression a echoue${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[OK] Dossier supprime : $dossier ($nb_fichiers fichiers, $nb_dossiers dossiers)${NC}"
}

main "$@"
