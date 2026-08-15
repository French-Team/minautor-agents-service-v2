#!/bin/bash
# creer-fichier.sh
# Creer un nouveau fichier avec verification
# Version : 0.3.1
# Statut : prepare

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
    echo "=== creer-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier> [contenu]"
    echo ""
    echo "Options :"
    echo "  --forcer         Ecraser si le fichier existe deja"
    echo "  --backup         Sauvegarder le fichier existant en .bak avant ecrasement"
    echo "  --dry-run        Simuler sans creer"
    echo "  --verbose        Afficher les details"
    echo "  --help           Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 nouveau-fichier.md"
    echo "  $0 nouveau-fichier.md \"# Titre\""
    echo "  $0 --forcer fichier.md"
    echo ""
}

# Main
main() {
    local fichier=""
    local contenu=""
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
                if [ -z "$fichier" ]; then
                    fichier="$1"
                elif [ -z "$contenu" ]; then
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
    
    # Verifier si le fichier existe deja
    if [ -f "$fichier" ] && [ "$forcer" = "false" ]; then
        echo -e "${RED}[ERREUR] Le fichier existe deja: $fichier${NC}"
        echo -e "${YELLOW}[INFO] Utiliser --forcer pour ecraser${NC}"
        exit 1
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] Creation de: $fichier${NC}"
        if [ -n "$contenu" ]; then
            echo -e "${YELLOW}[DRY-RUN] Contenu: $contenu${NC}"
        fi
        exit 0
    fi
    
    # Sauvegarde avant ecrasement (--forcer + --backup)
    if [ -f "$fichier" ] && [ "$forcer" = "true" ] && [ "$backup" = "true" ]; then
        cp "$fichier" "${fichier}.bak"
        if [ "$verbose" = "true" ]; then
            echo -e "${BLUE}[INFO] Sauvegarde: ${fichier}.bak${NC}"
        fi
    fi
    
    # Creer le repertoire parent si necessaire
    local dossier=$(dirname "$fichier")
    if [ ! -d "$dossier" ]; then
        mkdir -p "$dossier"
        if [ "$verbose" = "true" ]; then
            echo -e "${BLUE}[INFO] Repertoire cree: $dossier${NC}"
        fi
    fi
    
    # Creer le fichier
    if [ -n "$contenu" ]; then
        echo "$contenu" > "$fichier"
    else
        touch "$fichier"
    fi
    
    if [ "$verbose" = "true" ]; then
        echo -e "${GREEN}[OK] Fichier cree: $fichier${NC}"
    fi
    
    exit 0
}

main "$@"