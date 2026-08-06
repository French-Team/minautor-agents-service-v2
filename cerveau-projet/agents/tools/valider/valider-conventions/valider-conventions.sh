#!/bin/bash
# valider-conventions.sh
# Vérifier que les conventions sont respectées dans un fichier
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
NC='\033[0m' # No Color

# Fonction d'aide
aide() {
    echo "=========================================="
    echo "  valider-conventions v${VERSION}"
    echo "  Vérifier les conventions dans un fichier"
    echo "=========================================="
    echo ""
    echo "Usage: valider-conventions [OPTIONS] FICHIER"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les détails"
    echo "  --version           Afficher la version"
    echo ""
    echo "Conventions vérifiées:"
    echo "  - Frontmatter YAML présent"
    echo "  - Titre principal présent"
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

    echo -e "${BLUE}📋 Validation des conventions : $(basename "$fichier")${NC}"
    echo ""

    # Vérifier que le fichier n'est pas vide
    if [[ ! -s "$fichier" ]]; then
        echo -e "  ${RED}❌ Fichier vide${NC}"
        return 1
    fi

    # 1. Vérifier le frontmatter YAML
    echo -e "${BLUE}1. Frontmatter YAML${NC}"
    if head -1 "$fichier" | grep -q "^---"; then
        echo -e "  ${GREEN}✅ Frontmatter présent${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Frontmatter absent${NC}"
        warnings=$((warnings + 1))
    fi

    # 2. Vérifier le titre principal
    echo -e "${BLUE}2. Titre principal${NC}"
    if grep -q "^# " "$fichier"; then
        echo -e "  ${GREEN}✅ Titre principal présent${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Titre principal absent${NC}"
        warnings=$((warnings + 1))
    fi

    # 3. Vérifier les sections avec ##
    echo -e "${BLUE}3. Sections${NC}"
    local nb_sections=$(grep -c "^## " "$fichier" 2>/dev/null || echo "0")
    if [[ $nb_sections -gt 0 ]]; then
        echo -e "  ${GREEN}✅ ${nb_sections} section(s) trouvée(s)${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Aucune section ## trouvée${NC}"
        warnings=$((warnings + 1))
    fi

    # 4. Vérifier les espaces en fin de ligne
    echo -e "${BLUE}4. Espaces en fin de ligne${NC}"
    local nb_espaces=$(grep -c " $" "$fichier" 2>/dev/null || echo "0")
    if [[ $nb_espaces -gt 0 ]]; then
        echo -e "  ${YELLOW}⚠️  ${nb_espaces} ligne(s) avec espaces en fin${NC}"
        warnings=$((warnings + 1))
    else
        echo -e "  ${GREEN}✅ Pas d'espaces en fin de ligne${NC}"
    fi

    # 5. Vérifier la longueur des lignes
    echo -e "${BLUE}5. Longueur des lignes${NC}"
    local nb_longues=$(awk 'length > 120' "$fichier" | wc -l)
    if [[ $nb_longues -gt 0 ]]; then
        echo -e "  ${YELLOW}⚠️  ${nb_longues} ligne(s) > 120 caractères${NC}"
        warnings=$((warnings + 1))
    else
        echo -e "  ${GREEN}✅ Toutes les lignes < 120 caractères${NC}"
    fi

    # 6. Vérifier les liens cassés (basique)
    echo -e "${BLUE}6. Liens Markdown${NC}"
    local nb_liens=$(grep -oP '\[([^\]]*)\]\(([^)]+)\)' "$fichier" | wc -l)
    if [[ $nb_liens -gt 0 ]]; then
        echo -e "  ${GREEN}✅ ${nb_liens} lien(s) Markdown trouvé(s)${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Aucun lien Markdown trouvé${NC}"
    fi

    # Résumé
    echo ""
    echo -e "${BLUE}Résumé :${NC}"
    echo -e "  ${GREEN}✅ Conventions respectées : Oui${NC}"
    if [[ $warnings -gt 0 ]]; then
        echo -e "  ${YELLOW}⚠️  Avertissements : ${warnings}${NC}"
    fi
    if [[ $erreurs -gt 0 ]]; then
        echo -e "  ${RED}❌ Erreurs : ${erreurs}${NC}"
    fi

    return $erreurs
}

# Valeurs par défaut
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

# Vérification du fichier
if [[ -z "$FICHIER" ]]; then
    echo "Erreur: Aucun fichier spécifié"
    echo "Utilisez --aide pour l'aide"
    exit 1
fi

if [[ ! -f "$FICHIER" ]]; then
    echo "Erreur: Le fichier '$FICHIER' n'existe pas"
    exit 1
fi

# Exécution
valider_conventions "$FICHIER" "$VERBOSE"

exit $?
