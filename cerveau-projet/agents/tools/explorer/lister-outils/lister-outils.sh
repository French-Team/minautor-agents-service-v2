#!/bin/bash
# lister-outils.sh
# Lister les outils partagés du cerveau-projet
# Version: 0.1.0
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
VERSION="0.1.0"
DATE="2026-08-05"
TOOLS_DIR="cerveau-projet/agents/tools"

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
    echo "  lister-outils v${VERSION}"
    echo "  Lister les outils partagés"
    echo "=========================================="
    echo ""
    echo "Usage: lister-outils [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les détails"
    echo "  --version           Afficher la version"
    echo "  --detail, -d        Afficher les détails complets"
    echo "  --categorie, -c     Filtrer par catégorie"
    echo ""
    echo "Exemples:"
    echo "  lister-outils"
    echo "  lister-outils --detail"
    echo "  lister-outils --categorie explorer"
    echo ""
}

# Fonction pour lister les outils
lister_outils() {
    local verbose=$1
    local detail=$2
    local categorie=$3

    echo -e "${BLUE}🔧 Liste des outils partagés${NC}"
    echo ""

    # Vérifier si le dossier tools existe
    if [[ ! -d "$TOOLS_DIR" ]]; then
        echo -e "${RED}Erreur: Le dossier ${TOOLS_DIR} n'existe pas${NC}"
        return 1
    fi

    local total=0
    local avec_script=0
    local sans_script=0

    # Définir les catégories
    local categories=("explorer" "valider" "analyser" "corriger")

    for cat in "${categories[@]}"; do
        # Si une catégorie est spécifiée, ne traiter que celle-ci
        if [[ -n "$categorie" && "$cat" != "$categorie" ]]; then
            continue
        fi

        local cat_dir="${TOOLS_DIR}/${cat}"
        
        if [[ -d "$cat_dir" ]]; then
            echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${GREEN}📂 Catégorie : ${cat}${NC}"
            echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            
            for tool_dir in "$cat_dir"/*/; do
                if [[ -d "$tool_dir" ]]; then
                    local tool_name=$(basename "$tool_dir")
                    local tool_md="${tool_dir}${tool_name}.md"
                    local tool_sh="${tool_dir}${tool_name}.sh"
                    
                    echo -e "  🔧 ${tool_name}"
                    
                    # Vérifier si le script existe
                    if [[ -f "$tool_sh" ]]; then
                        echo -e "    ✅ Script : Présent"
                        avec_script=$((avec_script + 1))
                        
                        if [[ "$detail" == "true" ]]; then
                            # Extraire la version
                            local version=$(grep "VERSION=" "$tool_sh" 2>/dev/null | head -1 | sed 's/VERSION="//' | sed 's/"//')
                            if [[ -n "$version" ]]; then
                                echo -e "    📦 Version : ${version}"
                            fi
                            
                            # Vérifier si le script est exécutable
                            if [[ -x "$tool_sh" ]]; then
                                echo -e "    🚀 Exécutable : Oui"
                            else
                                echo -e "    ⚠️  Exécutable : Non"
                            fi
                        fi
                    else
                        echo -e "    ❌ Script : Absent"
                        sans_script=$((sans_script + 1))
                    fi
                    
                    # Vérifier la documentation
                    if [[ -f "$tool_md" ]]; then
                        echo -e "    📄 Documentation : Présente"
                    else
                        echo -e "    ⚠️  Documentation : Absente"
                    fi
                    
                    total=$((total + 1))
                    echo ""
                fi
            done
        fi
    done

    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Résumé :${NC}"
    echo -e "  📊 Total outils : ${total}"
    echo -e "  ✅ Avec script : ${avec_script}"
    echo -e "  ❌ Sans script : ${sans_script}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Valeurs par défaut
VERBOSE="false"
DETAIL="false"
CATEGORIE=""

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
            echo "lister-outils v${VERSION}"
            exit 0
            ;;
        --detail|-d)
            DETAIL="true"
            shift
            ;;
        --categorie|-c)
            CATEGORIE="$2"
            shift 2
            ;;
        -*)
            echo "Option inconnue: $1"
            echo "Utilisez --aide pour l'aide"
            exit 1
            ;;
        *)
            shift
            ;;
    esac
done

# Exécution
lister_outils "$VERBOSE" "$DETAIL" "$CATEGORIE"

exit $?
