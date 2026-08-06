#!/bin/bash
# analyser-dependances.sh
# Analyser les dépendances entre fichiers
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
    echo "  analyser-dependances v${VERSION}"
    echo "  Analyser les dépendances entre fichiers"
    echo "=========================================="
    echo ""
    echo "Usage: analyser-dependances [OPTIONS] FICHIER"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les détails"
    echo "  --version           Afficher la version"
    echo "  --inverse, -i       Afficher les fichiers qui dépendent de celui-ci"
    echo ""
    echo "Exemples:"
    echo "  analyser-dependances fichier.md"
    echo "  analyser-dependances --inverse fichier.md"
    echo ""
}

# Fonction pour analyser les dépendances
analyser_dependances() {
    local fichier=$1
    local verbose=$2
    local inverse=$3

    echo -e "${BLUE}[LIEN] Analyse des dépendances : $(basename "$fichier")${NC}"
    echo ""

    # Vérifier que le fichier existe
    if [[ ! -f "$fichier" ]]; then
        echo -e "${RED}Erreur: Le fichier '${fichier}' n'existe pas${NC}"
        return 1
    fi

    local dossier_fichier=$(dirname "$fichier")

    if [[ "$inverse" == "true" ]]; then
        # Mode inverse : trouver les fichiers qui dépendent de celui-ci
        echo -e "${CYAN}----------------------------------------${NC}"
        echo -e "${GREEN}[TELECHARGER] Fichiers qui dépendent de $(basename "$fichier")${NC}"
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
        echo -e "${BLUE}Terminé.${NC}"
    else
        # Mode normal : analyser les dépendances de ce fichier
        echo -e "${CYAN}----------------------------------------${NC}"
        echo -e "${GREEN}[ENVOYER] Dépendances de $(basename "$fichier")${NC}"
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
                
                # Vérifier si c'est un lien interne
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
            echo -e "  ${YELLOW}Aucun lien Markdown trouvé${NC}"
        fi
        echo ""

        # 2. Imports/Inclusions (pour les fichiers de code)
        echo -e "${BLUE}2. Imports/Inclusions${NC}"
        local extension="${fichier##*.}"
        
        case $extension in
            sh|bash)
                # Scripts Bash - chercher les sources
                local sources=$(grep -E '^\s*source\s+|^\s*\.\s+' "$fichier" 2>/dev/null | wc -l)
                echo -e "  [PAQUET] Sources Bash : ${sources}"
                ;;
            py)
                # Scripts Python - chercher les imports
                local imports=$(grep -E '^\s*import\s+|^\s*from\s+' "$fichier" 2>/dev/null | wc -l)
                echo -e "  [PAQUET] Imports Python : ${imports}"
                ;;
            js|ts)
                # Scripts JavaScript - chercher les imports
                local imports=$(grep -E '^\s*import\s+|^\s*require\s*\(' "$fichier" 2>/dev/null | wc -l)
                echo -e "  [PAQUET] Imports JavaScript : ${imports}"
                ;;
            *)
                echo -e "  ${YELLOW}Type de fichier non analysé pour les imports${NC}"
                ;;
        esac
        echo ""

        # 3. Fichiers référencés
        echo -e "${BLUE}3. Fichiers référencés${NC}"
        local refs=$(grep -oE '[a-zA-Z0-9_./-]+\.(md|sh|py|js|ts|json)' "$fichier" 2>/dev/null | sort -u | wc -l)
        echo -e "  [FICHIER] ${refs} fichier(s) référencé(s)"
        echo ""

        echo -e "${BLUE}Terminé.${NC}"
    fi
}

# Valeurs par défaut
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

# Vérification du fichier
if [[ -z "$FICHIER" ]]; then
    echo "Erreur: Aucun fichier spécifié"
    echo "Utilisez --aide pour l'aide"
    exit 1
fi

# Exécution
analyser_dependances "$FICHIER" "$VERBOSE" "$INVERSE"

exit $?
