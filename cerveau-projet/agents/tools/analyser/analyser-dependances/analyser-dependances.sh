#!/bin/bash
# analyser-dependances.sh
# Analyser les dependances entre fichiers
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
    echo "  analyser-dependances v${VERSION}"
    echo "  Analyser les dependances entre fichiers"
    echo "=========================================="
    echo ""
    echo "Usage: analyser-dependances [OPTIONS] FICHIER"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les details"
    echo "  --version           Afficher la version"
    echo "  --inverse, -i       Afficher les fichiers qui dependent de celui-ci"
    echo ""
    echo "Exemples:"
    echo "  analyser-dependances fichier.md"
    echo "  analyser-dependances --inverse fichier.md"
    echo ""
}

# Fonction pour analyser les dependances
analyser_dependances() {
    local fichier=$1
    local verbose=$2
    local inverse=$3

    echo -e "${BLUE}[ANALYSE] Dependances de : $(basename "$fichier")${NC}"
    echo ""

    # Verifier que le fichier existe
    if [[ ! -f "$fichier" ]]; then
        echo -e "${RED}Erreur: Le fichier '${fichier}' n'existe pas${NC}"
        return 1
    fi

    local dossier_fichier=$(dirname "$fichier")

    if [[ "$inverse" == "true" ]]; then
        # Mode inverse : trouver les fichiers qui dependent de celui-ci
        echo -e "${CYAN}----------------------------------------${NC}"
        echo -e "${GREEN}[DEPENDANTS] Fichiers qui dependent de $(basename "$fichier")${NC}"
        echo -e "${CYAN}----------------------------------------${NC}"
        
        local dependants=0
        
        # Chercher dans tous les fichiers .md
        find . -name "*.md" -type f | while read -r autrefichier; do
            if [[ "$autrefichier" != "$fichier" ]]; then
                if grep -q "$(basename "$fichier")" "$autrefichier" 2>/dev/null; then
                    echo -e "  [FICHIER] ${autrefichier}"
                    dependants=$((dependants + 1))
                fi
            fi
        done
        
        echo ""
        echo -e "${BLUE}Termine.${NC}"
    else
        # Mode normal : analyser les dependances de ce fichier
        echo -e "${CYAN}----------------------------------------${NC}"
        echo -e "${GREEN}[DEPENDANCES] Dependances de $(basename "$fichier")${NC}"
        echo -e "${CYAN}----------------------------------------${NC}"
        
        # 1. Liens Markdown
        echo -e "${BLUE}1. Liens Markdown${NC}"
        local liens=$(sed -n 's/.*\[\([^]]*\)\](\([^)]*\)).*/\1|\2/p' "$fichier" 2>/dev/null)
        
        if [[ -n "$liens" ]]; then
            local nb_valides=0
            local nb_invalides=0
            
            while IFS= read -r lien; do
                local texte=$(echo "$lien" | cut -d'|' -f1)
                local chemin=$(echo "$lien" | cut -d'|' -f2)
                
                # Verifier si c'est un lien interne
                if ! echo "$chemin" | grep -qE '^https?://'; then
                    local chemin_complet="${dossier_fichier}/${chemin}"
                    if [[ -f "$chemin_complet" ]] || [[ -d "$chemin_complet" ]]; then
                        nb_valides=$((nb_valides + 1))
                        if [[ "$verbose" == "true" ]]; then
                            echo -e "  ${GREEN}[OK] ${texte} -> ${chemin}${NC}"
                        fi
                    else
                        nb_invalides=$((nb_invalides + 1))
                        echo -e "  ${RED}[ERREUR] ${texte} -> ${chemin}${NC}"
                    fi
                fi
            done <<< "$liens"
            
            echo -e "  ${GREEN}Valides : ${nb_valides}${NC}"
            echo -e "  ${RED}Invalides : ${nb_invalides}${NC}"
        else
            echo -e "  ${YELLOW}Aucun lien Markdown trouve${NC}"
        fi
        echo ""

        # 2. Imports/Inclusions (pour les fichiers de code)
        echo -e "${BLUE}2. Imports/Inclusions${NC}"
        local extension="${fichier##*.}"
        
        case $extension in
            sh|bash)
                # Scripts Bash - chercher les sources
                local sources=$(grep -E '^\s*source\s+|^\s*\.\s+' "$fichier" 2>/dev/null | wc -l)
                echo -e "  [SOURCES] Sources Bash : ${sources}"
                ;;
            py)
                # Scripts Python - chercher les imports
                local imports=$(grep -E '^\s*import\s+|^\s*from\s+' "$fichier" 2>/dev/null | wc -l)
                echo -e "  [IMPORTS] Imports Python : ${imports}"
                ;;
            js|ts)
                # Scripts JavaScript - chercher les imports
                local imports=$(grep -E '^\s*import\s+|^\s*require\s*\(' "$fichier" 2>/dev/null | wc -l)
                echo -e "  [IMPORTS] Imports JavaScript : ${imports}"
                ;;
            *)
                echo -e "  ${YELLOW}Type de fichier non analyse pour les imports${NC}"
                ;;
        esac
        echo ""

        # 3. Fichiers references
        echo -e "${BLUE}3. Fichiers references${NC}"
        local refs=$(grep -oE '[a-zA-Z0-9_./-]+\.(md|sh|py|js|ts|json)' "$fichier" 2>/dev/null | sort -u | wc -l)
        echo -e "  [REFERENCES] ${refs} fichier(s) reference(s)"
        echo ""

        echo -e "${BLUE}Termine.${NC}"
    fi
}

# Valeurs par defaut
VERBOSE="false"
INVERSE="false"

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
            echo "analyser-dependances v${VERSION}"
            exit 0
            ;;
        --inverse|-i)
            INVERSE="true"
            shift
            ;;
        -*)
            echo "Option inconnue: $1"
            echo "Utilisez --aide pour l'aide"
            exit 1
            ;;
        *)
            FICHIER="$1"
            shift
            ;;
    esac
done

# Verification du fichier
if [[ -z "$FICHIER" ]]; then
    echo "Erreur: Aucun fichier specifie"
    echo "Utilisez --aide pour l'aide"
    exit 1
fi

# Execution
analyser_dependances "$FICHIER" "$VERBOSE" "$INVERSE"

exit $?
