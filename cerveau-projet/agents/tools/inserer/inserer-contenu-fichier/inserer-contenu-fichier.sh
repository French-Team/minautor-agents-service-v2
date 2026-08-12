#!/bin/bash
# inserer-contenu-fichier.sh
# Inserer du contenu a une position precise dans un fichier
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
    echo "=== inserer-contenu-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier> <position|--apres MOTIF> [contenu]"
    echo ""
    echo "Arguments :"
    echo "  <fichier>       Fichier a modifier"
    echo "  <position>      Inserer APRES cette ligne (0 = au debut)"
    echo "  [contenu]       Chaine a inserer (ou --fichier source)"
    echo ""
    echo "Options :"
    echo "  --apres <motif> Inserer apres la premiere ligne contenant le motif"
    echo "  --fichier <src> Inserer le contenu d'un fichier source"
    echo "  --backup        Creer une sauvegarde .bak avant"
    echo "  --dry-run       Simuler sans modifier"
    echo "  --verbose       Afficher les details"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md 5 \"Contenu a inserer\""
    echo "  $0 fichier.md 0 \"Ligne en debut de fichier\""
    echo "  $0 --dry-run fichier.md 5 \"contenu\""
    echo ""
}

main() {
    local fichier=""
    local position=""
    local contenu=""
    local source=""
    local motif=""
    local backup="false"
    local dry_run="false"
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --apres) motif="$2"; shift 2 ;;
            --fichier) source="$2"; shift 2 ;;
            --backup) backup="true"; shift ;;
            --dry-run) dry_run="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$fichier" ]; then
                    fichier="$1"
                elif [ -z "$position" ]; then
                    position="$1"
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
    
    if [ -z "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier obligatoire${NC}"
        afficher_aide
        exit 1
    fi

    # Ciblage par contenu : --apres <motif> remplace la position numerique
    if [ -n "$motif" ]; then
        position=$(grep -n -- "$motif" "$fichier" 2>/dev/null | head -1 | cut -d: -f1)
        if [ -z "$position" ]; then
            echo -e "${RED}[ERREUR] Motif introuvable dans $fichier : $motif${NC}"
            exit 1
        fi
        if [ "$verbose" = "true" ]; then
            echo -e "${BLUE}[INFO] Motif trouve ligne $position${NC}"
        fi
    fi

    if [ -z "$position" ]; then
        echo -e "${RED}[ERREUR] Position ou --apres <motif> obligatoire${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve: $fichier${NC}"
        exit 1
    fi
    
    if ! [[ "$position" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}[ERREUR] La position doit etre un nombre: $position${NC}"
        exit 1
    fi
    
    if [ -n "$source" ]; then
        if [ ! -f "$source" ]; then
            echo -e "${RED}[ERREUR] Fichier source non trouve: $source${NC}"
            exit 1
        fi
    elif [ -z "$contenu" ]; then
        echo -e "${RED}[ERREUR] Aucun contenu a inserer (chaine ou --fichier)${NC}"
        afficher_aide
        exit 1
    fi
    
    local total_lignes=$(wc -l < "$fichier")
    
    if [ "$position" -gt "$total_lignes" ]; then
        echo -e "${YELLOW}[INFO] La position ($position) depasse le nombre de lignes ($total_lignes)${NC}"
        echo -e "${YELLOW}[INFO] Le contenu sera ajoute a la fin${NC}"
        position="$total_lignes"
    fi
    
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}[INFO] Fichier: $fichier ($total_lignes lignes)${NC}"
        echo -e "${BLUE}[INFO] Insertion apres la ligne $position${NC}"
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] Insertion simulee apres la ligne $position dans $fichier${NC}"
        exit 0
    fi

    # Sauvegarde
    if [ "$backup" = "true" ]; then
        cp "$fichier" "${fichier}.bak"
        if [ "$verbose" = "true" ]; then
            echo -e "${BLUE}[INFO] Sauvegarde: ${fichier}.bak${NC}"
        fi
    fi
    
    # Construire le contenu a inserer dans un fichier temporaire
    local tmp=$(mktemp)
    if [ -n "$source" ]; then
        cat "$source" > "$tmp"
    else
        printf '%s\n' "$contenu" > "$tmp"
    fi
    
    # Inserer : avant = lignes 1..position ; bloc ; apres = position+1..fin
    if [ "$position" -eq 0 ]; then
        cat "$tmp" "$fichier" > "$fichier.tmp-inserer"
    else
        head -n "$position" "$fichier" > "$fichier.tmp-inserer"
        cat "$tmp" >> "$fichier.tmp-inserer"
        tail -n +$((position + 1)) "$fichier" >> "$fichier.tmp-inserer"
    fi
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERREUR] L'insertion a echoue${NC}"
        rm -f "$tmp" "$fichier.tmp-inserer"
        exit 1
    fi
    
    mv "$fichier.tmp-inserer" "$fichier"
    rm -f "$tmp"
    
    echo -e "${GREEN}[OK] Contenu insere apres la ligne $position dans $fichier${NC}"
}

main "$@"
