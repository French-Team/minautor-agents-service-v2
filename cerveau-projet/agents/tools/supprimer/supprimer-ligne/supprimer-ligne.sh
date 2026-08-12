#!/bin/bash
# supprimer-ligne.sh
# Supprimer une ligne (ou une plage) par numero dans un fichier
# Version : 0.3.0

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
    echo "=== supprimer-ligne v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier> <ligne> [ligne-fin]"
    echo ""
    echo "Arguments :"
    echo "  <fichier>       Fichier a modifier"
    echo "  <ligne>         Numero de la ligne a supprimer (1 = premiere)"
    echo "  [ligne-fin]     Derniere ligne de la plage a supprimer (defaut = ligne)"
    echo ""
    echo "Options :"
    echo "  --backup        Creer une sauvegarde .bak avant"
    echo "  --dry-run       Simuler sans modifier"
    echo "  --verbose       Afficher les details"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md 42        # Supprimer la ligne 42"
    echo "  $0 fichier.md 10 15     # Supprimer les lignes 10 a 15"
    echo "  $0 --dry-run fichier.md 42"
    echo ""
}

main() {
    local fichier=""
    local ligne=""
    local ligne_fin=""
    local backup="false"
    local dry_run="false"
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run) dry_run="true"; shift ;;
            --backup) backup="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *)
                if [ -z "$fichier" ]; then
                    fichier="$1"
                elif [ -z "$ligne" ]; then
                    ligne="$1"
                elif [ -z "$ligne_fin" ]; then
                    ligne_fin="$1"
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
    
    if [ -z "$fichier" ] || [ -z "$ligne" ]; then
        echo -e "${RED}[ERREUR] Fichier et numero de ligne obligatoires${NC}"
        afficher_aide
        exit 1
    fi
    
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve: $fichier${NC}"
        exit 1
    fi
    
    if ! [[ "$ligne" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}[ERREUR] Le numero de ligne doit etre un nombre: $ligne${NC}"
        exit 1
    fi
    
    if [ -z "$ligne_fin" ]; then
        ligne_fin="$ligne"
    fi
    
    if ! [[ "$ligne_fin" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}[ERREUR] La ligne de fin doit etre un nombre: $ligne_fin${NC}"
        exit 1
    fi
    
    if [ "$ligne" -lt 1 ]; then
        echo -e "${RED}[ERREUR] Le numero de ligne doit etre >= 1${NC}"
        exit 1
    fi
    
    if [ "$ligne_fin" -lt "$ligne" ]; then
        echo -e "${RED}[ERREUR] La ligne de fin ($ligne_fin) doit etre >= a la ligne ($ligne)${NC}"
        exit 1
    fi
    
    local total_lignes=$(wc -l < "$fichier")
    
    if [ "$ligne" -gt "$total_lignes" ]; then
        # Robustesse (round 4) : pluriel correct ("1 ligne" vs "N lignes")
        local mot="lignes"
        if [ "$total_lignes" -eq 1 ]; then
            mot="ligne"
        fi
        echo -e "${RED}[ERREUR] Le fichier n'a que $total_lignes $mot, ligne $ligne inexistante${NC}"
        exit 1
    fi
    
    if [ "$ligne_fin" -gt "$total_lignes" ]; then
        ligne_fin="$total_lignes"
    fi
    
    local nb_supprimes=$(( ligne_fin - ligne + 1 ))
    
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}[INFO] Fichier: $fichier ($total_lignes lignes)${NC}"
        echo -e "${BLUE}[INFO] Suppression des lignes $ligne a $ligne_fin ($nb_supprimes ligne(s))${NC}"
        echo "---"
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN] Aucune modification appliquee${NC}"
        echo "Lignes qui seraient supprimees :"
        sed -n "${ligne},${ligne_fin}p" "$fichier"
        exit 0
    fi
    
    # Sauvegarde
    if [ "$backup" = "true" ]; then
        cp "$fichier" "${fichier}.bak"
        if [ "$verbose" = "true" ]; then
            echo -e "${BLUE}[INFO] Sauvegarde: ${fichier}.bak${NC}"
        fi
    fi
    
    # Supprimer les lignes avec sed (fichier temporaire puis remplacement)
    sed "${ligne},${ligne_fin}d" "$fichier" > "${fichier}.tmp"
    mv "${fichier}.tmp" "$fichier"
    
    if [ "$verbose" = "true" ]; then
        echo -e "${GREEN}[OK] $nb_supprimes ligne(s) supprimee(s) de $fichier${NC}"
    fi
    
    exit 0
}

main "$@"
