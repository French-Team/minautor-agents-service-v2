#!/bin/bash
# analyser-structure.sh
# Analyser la structure du projet
# Version: 0.2.0
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
VERSION="0.2.0"
DATE="2026-08-05"

# Couleurs pour la sortie
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction d'aide
aide() {
    echo "=========================================="
    echo "  analyser-structure v${VERSION}"
    echo "  Analyser la structure du projet"
    echo "=========================================="
    echo ""
    echo "Usage: analyser-structure [OPTIONS] [CHEMIN]"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les details"
    echo "  --version           Afficher la version"
    echo "  --profondeur, -p    Profondeur d'analyse (defaut: 2)"
    echo ""
    echo "Exemples:"
    echo "  analyser-structure"
    echo "  analyser-structure --profondeur 3 cerveau-projet"
    echo ""
}

# Fonction pour analyser la structure
analyser_structure() {
    local chemin=$1
    local verbose=$2
    local profondeur=$3

    echo -e "${BLUE}[ANALYSE] Structure de : ${chemin:-.}${NC}"
    echo ""

    # Chemin par defaut
    if [[ -z "$chemin" ]]; then
        chemin="."
    fi

    # Verifier que le chemin existe
    if [[ ! -e "$chemin" ]]; then
        echo -e "${RED}Erreur: Le chemin '${chemin}' n'existe pas${NC}"
        return 1
    fi

    # 1. Statistiques generales
    echo -e "${CYAN}----------------------------------------${NC}"
    echo -e "${GREEN}[STATS] Statistiques generales${NC}"
    echo -e "${CYAN}----------------------------------------${NC}"
    
    local nb_dossiers=$(find "$chemin" -type d -maxdepth "$profondeur" 2>/dev/null | wc -l)
    local nb_fichiers=$(find "$chemin" -type f -maxdepth "$profondeur" 2>/dev/null | wc -l)
    local nb_md=$(find "$chemin" -name "*.md" -type f -maxdepth "$profondeur" 2>/dev/null | wc -l)
    local nb_sh=$(find "$chemin" -name "*.sh" -type f -maxdepth "$profondeur" 2>/dev/null | wc -l)
    local nb_py=$(find "$chemin" -name "*.py" -type f -maxdepth "$profondeur" 2>/dev/null | wc -l)
    local nb_js=$(find "$chemin" -name "*.js" -type f -maxdepth "$profondeur" 2>/dev/null | wc -l)

    echo -e "  [DOSSIERS] ${nb_dossiers}"
    echo -e "  [FICHIERS] ${nb_fichiers}"
    echo -e "  [MD] ${nb_md}"
    echo -e "  [SH] ${nb_sh}"
    echo -e "  [PY] ${nb_py}"
    echo -e "  [JS] ${nb_js}"
    echo ""

    # 2. Taille totale
    echo -e "${CYAN}----------------------------------------${NC}"
    echo -e "${GREEN}[TAILLE]${NC}"
    echo -e "${CYAN}----------------------------------------${NC}"
    
    local taille=$(du -sh "$chemin" 2>/dev/null | cut -f1)
    echo -e "  [TAILLE] Taille totale : ${taille}"
    echo ""

    # 3. Extensions
    echo -e "${CYAN}----------------------------------------${NC}"
    echo -e "${GREEN}[EXTENSIONS]${NC}"
    echo -e "${CYAN}----------------------------------------${NC}"
    
    find "$chemin" -type f -maxdepth "$profondeur" 2>/dev/null | \
        sed 's/.*\.//' | \
        sort | uniq -c | sort -rn | head -10 | \
        while read -r count ext; do
            echo -e "  .${ext} : ${count} fichier(s)"
        done
    echo ""

    # 4. Structure arborescente (limitee)
    echo -e "${CYAN}----------------------------------------${NC}"
    echo -e "${GREEN}[STRUCTURE]${NC}"
    echo -e "${CYAN}----------------------------------------${NC}"
    
    if [[ "$verbose" == "true" ]]; then
        tree -L "$profondeur" "$chemin" 2>/dev/null || \
            find "$chemin" -maxdepth "$profondeur" -type d | head -30
    else
        find "$chemin" -maxdepth "$profondeur" -type d | head -20
    fi
    echo ""

    # 5. Fichiers recents
    echo -e "${CYAN}----------------------------------------${NC}"
    echo -e "${GREEN}[RECENTS] Fichiers recents (7 jours)${NC}"
    echo -e "${CYAN}----------------------------------------${NC}"
    
    local nb_recents=$(find "$chemin" -type f -mtime -7 -maxdepth "$profondeur" 2>/dev/null | wc -l)
    echo -e "  [RECENTS] ${nb_recents} fichier(s) recent(s)"
    echo ""

    echo -e "${BLUE}Analyse terminee.${NC}"
}

# Valeurs par defaut
VERBOSE="false"
PROFONDEUR=2

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --aide|-h)
            aide
            exit 0
            ;;
        --verbose|-v)
            VERBOSE="true"
            shift
            ;;
        --version)
            echo "analyser-structure v${VERSION}"
            exit 0
            ;;
        --profondeur|-p)
            PROFONDEUR="$2"
            shift 2
            ;;
        -*)
            echo "Option inconnue: $1"
            echo "Utilisez --aide pour l'aide"
            exit 1
            ;;
        *)
            CHEMIN="$1"
            shift
            ;;
    esac
done

# Execution
analyser_structure "$CHEMIN" "$VERBOSE" "$PROFONDEUR"

exit $?
