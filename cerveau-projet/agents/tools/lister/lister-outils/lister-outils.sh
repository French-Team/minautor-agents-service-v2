#!/bin/bash
# lister-outils.sh
# Lister les outils partages du cerveau-projet
# Version: 0.3.0
# Date: 2026-08-08
# Auteur: Vulcain

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.3.0"
DATE="2026-08-08"
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
    echo "  Lister les outils partages"
    echo "=========================================="
    echo ""
    echo "Usage: lister-outils [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les details"
    echo "  --version           Afficher la version"
    echo "  --detail, -d        Afficher les details complets"
    echo "  --categorie, -c     Filtrer par categorie"
    echo "  --tag TAG           Filtrer par tag (convention-tags)"
    echo ""
    echo "Exemples:"
    echo "  lister-outils"
    echo "  lister-outils --detail"
    echo "  lister-outils --categorie rechercher"
    echo "  lister-outils --tag validation"
    echo ""
}

# Fonction pour lister les outils
# Lire les tags d'un fichier (frontmatter identite, format convention-tags)
# Arg1: chemin du fichier -> stdout: liste des tags separes par des espaces
lire_tags() {
    local fichier=$1
    [[ -f "$fichier" ]] || return 0
    local dans_identite=0
    while IFS= read -r ligne; do
        if [[ "$ligne" == *"identite:"* ]]; then
            dans_identite=1
            continue
        fi
        if [[ $dans_identite -eq 1 ]]; then
            if [[ "$ligne" =~ ^[[:space:]]*(#)?[[:space:]]*tags:[[:space:]]*(.*)$ ]]; then
                echo "${BASH_REMATCH[2]}"
                return 0
            fi
        fi
    done < "$fichier"
    return 0
}

lister_outils() {
    local verbose=$1
    local detail=$2
    local categorie=$3
    local tag=$4

    echo -e "${BLUE}[LISTE] Liste des outils partages${NC}"
    if [[ -n "$tag" ]]; then
        echo -e "${YELLOW}[FILTRE] Tag : ${tag}${NC}"
    fi
    echo ""

    # Verifier si le dossier tools existe
    if [[ ! -d "$TOOLS_DIR" ]]; then
        echo -e "${RED}Erreur: Le dossier ${TOOLS_DIR} n'existe pas${NC}"
        return 1
    fi

    local total=0
    local avec_script=0
    local sans_script=0

    # Definir les categories dynamiquement (chaque sous-dossier = une categorie)
    local categories=()
    for d in "$TOOLS_DIR"/*/; do
        if [[ -d "$d" ]] && [[ "$(basename "$d")" != "combos" ]] && [[ "$(basename "$d")" != "tester" ]]; then
            categories+=("$(basename "$d")")
        fi
    done

    for cat in "${categories[@]}"; do
        # Si une categorie est specifiee, ne traiter que celle-ci
        if [[ -n "$categorie" && "$cat" != "$categorie" ]]; then
            continue
        fi

        local cat_dir="${TOOLS_DIR}/${cat}"
        
        if [[ -d "$cat_dir" ]]; then
            echo -e "${CYAN}----------------------------------------${NC}"
            echo -e "${GREEN}[CATEGORIE] ${cat}${NC}"
            echo -e "${CYAN}----------------------------------------${NC}"
            
            for tool_dir in "$cat_dir"/*/; do
                if [[ -d "$tool_dir" ]]; then
                    local tool_name=$(basename "$tool_dir")
                    local tool_md="${tool_dir}${tool_name}.md"
                    local tool_sh="${tool_dir}${tool_name}.sh"
                    
                    # Filtre par tag (convention-tags)
                    if [[ -n "$tag" ]]; then
                        local tags_md=$(lire_tags "$tool_md")
                        local tags_sh=$(lire_tags "$tool_sh")
                        local tags_norm=$(echo "$tags_md $tags_sh" | tr ',' ' ')
                        if [[ " $tags_norm " != *" $tag "* ]]; then
                            continue
                        fi
                    fi
                    
                    echo -e "  [OUTIL] ${tool_name}"
                    
                    # Verifier si le script existe
                    if [[ -f "$tool_sh" ]]; then
                        echo -e "    [OK] Script : Present"
                        avec_script=$((avec_script + 1))
                        
                        if [[ "$detail" == "true" ]]; then
                            # Extraire la version
                            local version=$(grep "VERSION="0.2.0"$tool_sh" 2>/dev/null | head -1 | sed 's/VERSION="0.2.0"//')
                            if [[ -n "$version" ]]; then
                                echo -e "    [VERSION] ${version}"
                            fi
                            
                            # Verifier si le script est executable
                            if [[ -x "$tool_sh" ]]; then
                                echo -e "    [EXECUTABLE] Oui"
                            else
                                echo -e "    [ATTENTION]  Executable : Non"
                            fi
                        fi
                    else
                        echo -e "    [ERREUR] Script : Absent"
                        sans_script=$((sans_script + 1))
                    fi
                    
                    # Verifier la documentation
                    if [[ -f "$tool_md" ]]; then
                        echo -e "    [DOCUMENTATION] Presente"
                    else
                        echo -e "    [ATTENTION]  Documentation : Absente"
                    fi
                    
                    total=$((total + 1))
                    echo ""
                fi
            done
        fi
    done

    echo -e "${CYAN}----------------------------------------${NC}"
    echo -e "${BLUE}Resume :${NC}"
    echo -e "  [TOTAL] Outils : ${total}"
    echo -e "  [OK] Avec script : ${avec_script}"
    echo -e "  [ERREUR] Sans script : ${sans_script}"
    echo -e "${CYAN}----------------------------------------${NC}"
}

# Valeurs par defaut
VERBOSE="false"
DETAIL="false"
CATEGORIE=""
TAG=""

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
        --tag)
            TAG="$2"
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

# Execution
lister_outils "$VERBOSE" "$DETAIL" "$CATEGORIE" "$TAG"

exit $?
