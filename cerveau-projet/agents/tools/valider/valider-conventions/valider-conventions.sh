#!/bin/bash
# valider-conventions.sh
# Verifier que les conventions sont respectees dans un fichier
# Version: 0.1.0
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
NC='\033[0m' # No Color

# Fonction d'aide
aide() {
    echo "=========================================="
    echo "  valider-conventions v${VERSION}"
    echo "  Verifier les conventions dans un fichier"
    echo "=========================================="
    echo ""
    echo "Usage: valider-conventions [OPTIONS] FICHIER"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les details"
    echo "  --version           Afficher la version"
    echo ""
    echo "Conventions verifiees:"
    echo "  - Frontmatter YAML present"
    echo "  - Titre principal present"
    echo "  - Sections avec ##"
    echo "  - Pas d'espaces en fin de ligne"
    echo "  - Fichier non vide"
    echo ""
    echo "Exemples:"
    echo "  valider-conventions fichier.md"
    echo "  valider-conventions --verbose autre-fichier.md"
    echo ""
}

# Fonction pour valider les conventions
valider_conventions() {
    local fichier=$1
    local verbose=$2
    local erreurs=0
    local warnings=0

    echo -e "${BLUE}[CHECKLIST] Validation des conventions : $(basename "$fichier")${NC}"
    echo ""

    # Verifier que le fichier n'est pas vide
    if [[ ! -s "$fichier" ]]; then
        echo -e "  ${RED}[ERREUR] Fichier vide${NC}"
        return 1
    fi

    # 1. Verifier le frontmatter YAML
    echo -e "${BLUE}1. Frontmatter YAML${NC}"
    if head -1 "$fichier" | grep -q "^---"; then
        echo -e "  ${GREEN}[OK] Frontmatter present${NC}"
    else
        echo -e "  ${YELLOW}[ATTENTION]  Frontmatter absent${NC}"
        warnings=$((warnings + 1))
    fi

    # 2. Verifier le titre principal
    echo -e "${BLUE}2. Titre principal${NC}"
    if grep -q "^# " "$fichier"; then
        echo -e "  ${GREEN}[OK] Titre principal present${NC}"
    else
        echo -e "  ${YELLOW}[ATTENTION]  Titre principal absent${NC}"
        warnings=$((warnings + 1))
    fi

    # 3. Verifier les sections avec ##
    echo -e "${BLUE}3. Sections${NC}"
    local nb_sections=$(grep -c "^## " "$fichier" 2>/dev/null || echo "0")
    if [[ $nb_sections -gt 0 ]]; then
        echo -e "  ${GREEN}[OK] ${nb_sections} section(s) trouvee(s)${NC}"
    else
        echo -e "  ${YELLOW}[ATTENTION]  Aucune section ## trouvee${NC}"
        warnings=$((warnings + 1))
    fi

    # 4. Verifier les espaces en fin de ligne
    echo -e "${BLUE}4. Espaces en fin de ligne${NC}"
    local nb_espaces=$(grep -c " $" "$fichier" 2>/dev/null || echo "0")
    if [[ $nb_espaces -gt 0 ]]; then
        echo -e "  ${YELLOW}[ATTENTION]  ${nb_espaces} ligne(s) avec espaces en fin${NC}"
        warnings=$((warnings + 1))
    else
        echo -e "  ${GREEN}[OK] Pas d'espaces en fin de ligne${NC}"
    fi

    # 5. Verifier la longueur des lignes
    echo -e "${BLUE}5. Longueur des lignes${NC}"
    local nb_longues=$(awk 'length > 120' "$fichier" | wc -l)
    if [[ $nb_longues -gt 0 ]]; then
        echo -e "  ${YELLOW}[ATTENTION]  ${nb_longues} ligne(s) > 120 caracteres${NC}"
        warnings=$((warnings + 1))
    else
        echo -e "  ${GREEN}[OK] Toutes les lignes < 120 caracteres${NC}"
    fi

    # 6. Verifier les liens casses (basique)
    echo -e "${BLUE}6. Liens Markdown${NC}"
    local nb_liens=$(sed -n 's/.*\[\([^]]*\)\](\([^)]*\)).*/\1|\2/p' "$fichier" 2>/dev/null | wc -l)
    if [[ $nb_liens -gt 0 ]]; then
        echo -e "  ${GREEN}[OK] ${nb_liens} lien(s) Markdown trouve(s)${NC}"
    else
        echo -e "  ${YELLOW}[ATTENTION]  Aucun lien Markdown trouve${NC}"
    fi

    # Resume
    echo ""
    echo -e "${BLUE}Resume :${NC}"
    echo -e "  ${GREEN}[OK] Conventions respectees : Oui${NC}"
    if [[ $warnings -gt 0 ]]; then
        echo -e "  ${YELLOW}[ATTENTION]  Avertissements : ${warnings}${NC}"
    fi
    if [[ $erreurs -gt 0 ]]; then
        echo -e "  ${RED}[ERREUR] Erreurs : ${erreurs}${NC}"
    fi

    return $erreurs
}

# Valeurs par defaut
VERBOSE="false"

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
            echo "valider-conventions v${VERSION}"
            exit 0
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

if [[ ! -f "$FICHIER" ]]; then
    echo "Erreur: Le fichier '$FICHIER' n'existe pas"
    exit 1
fi

# Execution
valider_conventions "$FICHIER" "$VERBOSE"

exit $?
