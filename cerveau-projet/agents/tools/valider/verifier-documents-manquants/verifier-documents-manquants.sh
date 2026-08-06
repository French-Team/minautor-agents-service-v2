#!/bin/bash
# verifier-documents-manquants.sh
# Verifier que chaque script .sh a sa documentation .md et inversement
# Version : 0.2.0-beta
# Statut : ebauche

# Configuration
VERSION="0.2.0-beta"
STATUT="ebauche"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== verifier-documents-manquants v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] [DOSSIER]"
    echo ""
    echo "Options :"
    echo "  --sh-sans-md       Verifier les .sh sans .md correspondant (defaut: on)"
    echo "  --md-sans-sh       Verifier les .md sans .sh correspondant (defaut: on)"
    echo "  --inclure-speciaux Inclure les fichiers speciaux (spec/, test-*, index-*, *template*)"
    echo "  --dry-run          Simuler sans rien modifier"
    echo "  --verbose          Afficher les details"
    echo "  --help             Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0                                    # Verifier dans le dossier courant"
    echo "  $0 cerveau-projet/agents/tools/      # Verifier les outils"
    echo "  $0 --sh-sans-md outils/              # Verifier seulement les .sh sans .md"
    echo "  $0 --inclure-speciaux outils/        # Inclure aussi spec/, test-*, index-*, templates"
    echo ""
}

# Verifier si un fichier est un faux positif (document de support sans script)
est_faux_positif() {
    local fichier="$1"
    local nom_base=$(basename "$fichier")
    local dossier_fichier=$(dirname "$fichier")
    
    # Dossier spec/ : specifications, pas besoin de script
    if [[ "$dossier_fichier" == */spec* ]]; then
        return 0
    fi
    
    # Fichiers de test : test-*.md / test_*.md
    if [[ "$nom_base" == test-* ]] || [[ "$nom_base" == test_* ]]; then
        return 0
    fi
    
    # Index : index-*.md / index_*.md
    if [[ "$nom_base" == index-* ]] || [[ "$nom_base" == index_* ]]; then
        return 0
    fi
    
    # Templates : *template*.md
    if [[ "$nom_base" == *template* ]]; then
        return 0
    fi
    
    return 1
}

# Verifier les .sh sans .md correspondant
verifier_sh_sans_md() {
    local dossier="$1"
    local count=0
    
    while IFS= read -r sh_file; do
        local base="${sh_file%.sh}"
        local md_file="${base}.md"
        
        if [ ! -f "$md_file" ]; then
            count=$((count + 1))
            echo -e "  ${RED}[MANQUANT]${NC} $sh_file"
            if [ "$verbose" = "true" ]; then
                echo -e "        ${YELLOW}-> Documentation manquante : ${md_file}${NC}"
            fi
        fi
    done < <(find "$dossier" -name "*.sh" -type f 2>/dev/null)
    
    return $count
}

# Verifier les .md sans .sh correspondant
verifier_md_sans_sh() {
    local dossier="$1"
    local count=0
    
    while IFS= read -r md_file; do
        local base="${md_file%.md}"
        local sh_file="${base}.sh"
        
        if [ ! -f "$sh_file" ]; then
            count=$((count + 1))
            echo -e "  ${YELLOW}[SANS-SCRIPT]${NC} $md_file"
            if [ "$verbose" = "true" ]; then
                echo -e "        ${YELLOW}-> Script correspondant manquant : ${sh_file}${NC}"
            fi
        fi
    done < <(find "$dossier" -name "*.md" -type f 2>/dev/null)
    
    return $count
}

# Main
main() {
    local dossier="."
    local check_sh=true
    local check_md=true
    local dry_run="false"
    local verbose="false"
    local help="false"
    local inclure_speciaux="false"
    
    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --sh-sans-md)
                check_sh=true
                check_md=false
                shift
                ;;
            --md-sans-sh)
                check_md=true
                check_sh=false
                shift
                ;;
            --inclure-speciaux)
                inclure_speciaux="true"
                shift
                ;;
            --dry-run)
                dry_run="true"
                shift
                ;;
            --verbose)
                verbose="true"
                shift
                ;;
            --help)
                help="true"
                shift
                ;;
            *)
                dossier="$1"
                shift
                ;;
        esac
    done
    
    # Afficher l'aide
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    # Verifier que le dossier existe
    if [ ! -d "$dossier" ]; then
        echo -e "${RED}[ERREUR] Le dossier n'existe pas : $dossier${NC}"
        exit 1
    fi
    
    echo "=== Verification des documents manquants ==="
    echo "Dossier : ${dossier}"
    echo ""
    
    local total_manquants=0
    local total_sh=0
    local total_md=0
    
    # Compter les fichiers
    total_sh=$(find "$dossier" -name "*.sh" -type f 2>/dev/null | wc -l)
    total_md=$(find "$dossier" -name "*.md" -type f 2>/dev/null | wc -l)        # Verifier les .sh sans .md
        if [ "$check_sh" = "true" ]; then
            echo "--- Scripts .sh sans documentation .md ---"
            local count=0
            while IFS= read -r sh_file; do
                # Ignorer les faux positifs (script de spec, de test, etc.)
                if [ "$inclure_speciaux" = "false" ] && est_faux_positif "$sh_file"; then
                    continue
                fi
                
                local base="${sh_file%.sh}"
                local md_file="${base}.md"
                
                if [ ! -f "$md_file" ]; then
                    count=$((count + 1))
                    echo -e "  ${RED}[MANQUANT]${NC} $sh_file"
                fi
            done < <(find "$dossier" -name "*.sh" -type f 2>/dev/null)
            
            total_manquants=$((total_manquants + count))
            echo -e "  ${YELLOW}-> ${count} script(s) sans documentation${NC}"
            echo ""
        fi
        
        # Verifier les .md sans .sh
        if [ "$check_md" = "true" ]; then
            echo "--- Documentation .md sans script .sh ---"
            local count=0
            while IFS= read -r md_file; do
                # Ignorer les documents de support (spec/, test-*, index-*, templates)
                if [ "$inclure_speciaux" = "false" ] && est_faux_positif "$md_file"; then
                    continue
                fi
                
                local base="${md_file%.md}"
                local sh_file="${base}.sh"
                
                if [ ! -f "$sh_file" ]; then
                    count=$((count + 1))
                    echo -e "  ${YELLOW}[SANS-SCRIPT]${NC} $md_file"
                fi
            done < <(find "$dossier" -name "*.md" -type f 2>/dev/null)
            
            total_manquants=$((total_manquants + count))
            echo -e "  ${YELLOW}-> ${count} documentation(s) sans script${NC}"
            echo ""
        fi
    
    # Resume
    echo "=== Resume ==="
    echo "Scripts .sh : ${total_sh}"
    echo "Documentations .md : ${total_md}"
    echo -e "Documents manquants : ${RED}${total_manquants}${NC}"
    
    # Code de sortie
    if [ "$total_manquants" -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}[ATTENTION] Des documents manquants ont ete detectes${NC}"
        exit 1
    fi
    
    exit 0
}

# Executer
main "$@"
