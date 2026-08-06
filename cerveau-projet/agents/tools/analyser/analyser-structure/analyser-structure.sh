#!/bin/bash
# analyser-structure.sh
# Analyser la structure du projet
# Version: 0.1.0
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
VERSION="0.1.0"
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
    echo "  --verbose, -v       Afficher les détails"
    echo "  --version           Afficher la version"
    echo "  --profondeur, -p    Profondeur d'analyse (défaut: 2)"
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

    echo -e "${BLUE}📊 Analyse de la structure : ${chemin:-.}${NC}"
    echo ""

    # Chemin par défaut
    if [[ -z "$chemin" ]]; then
        chemin="."
    fi

    # Vérifier que le chemin existe
    if [[ ! -e "$chemin" ]]; then
        echo -e "${RED}Erreur: Le chemin '${chemin}' n'existe pas${NC}"
        return 1
    fi

    # 1. Statistiques générales
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}📁 Statistiques générales${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    local nb_dossiers=$(find "$chemin" -type d -maxdepth "$profondeur" 2>/dev/null | wc -l)
    local nb_fichiers=$(find "$chemin" -type f -maxdepth "$profondeur" 2>/dev/null | wc -l)
    local nb_md=$(find "$chemin" -name "*.md" -type f -maxdepth "$profondeur" 2>/dev/null | wc -l)
    local nb_sh=$(find "$chemin" -name "*.sh" -type f -maxdepth "$profondeur" 2>/dev/null | wc -l)
    local nb_py=$(find "$chemin" -name "*.py" -type f -maxdepth "$profondeur" 2>/dev/null | wc -l)
    local nb_js=$(find "$chemin" -name "*.js" -type f -maxdepth "$profondeur" 2>/dev/null | wc -l)

    echo -e "  📂 Dossiers : ${nb_dossiers}"
    echo -e "  📄 Fichiers : ${nb_fichiers}"
    echo -e "  📝 Markdown : ${nb_md}"
    echo -e "  🐚 Scripts Bash : ${nb_sh}"
    echo -e "  🐍 Scripts Python : ${nb_py}"
    echo -e "  📜 Scripts JavaScript : ${nb_js}"
    echo ""

    # 2. Taille totale
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}💾 Taille${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    local taille=$(du -sh "$chemin" 2>/dev/null | cut -f1)
    echo -e "  📦 Taille totale : ${taille}"
    echo ""

    # 3. Extensions
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}📎 Extensions${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    find "$chemin" -type f -maxdepth "$profondeur" 2>/dev/null | \
        sed 's/.*\.//' | \
        sort | uniq -c | sort -rn | head -10 | \
        while read -r count ext; do
            echo -e "  .${ext} : ${count} fichier(s)"
        done
    echo ""

    # 4. Structure arborescente (limitée)
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🌳 Structure${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if [[ "$verbose" == "true" ]]; then
        tree -L "$profondeur" "$chemin" 2>/dev/null || \
            find "$chemin" -maxdepth "$profondeur" -type d | head -30
    else
        find "$chemin" -maxdepth "$profondeur" -type d | head -20
    fi
    echo ""

    # 5. Fichiers récents
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🕐 Fichiers récents (modifiés dans les 7 derniers jours)${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    local nb_recents=$(find "$chemin" -type f -mtime -7 -maxdepth "$profondeur" 2>/dev/null | wc -l)
    echo -e "  📄 ${nb_recents} fichier(s) récent(s)"
    echo ""

    echo -e "${BLUE}Analyse terminée.${NC}"
}

# Valeurs par défaut
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

# Exécution
analyser_structure "$CHEMIN" "$VERBOSE" "$PROFONDEUR"

exit $?
