#!/bin/bash
# valider-ebauche.sh
# Verifie si un fichier ebauche respecte les exigences minimales
# Proprietaire : Vulcain (outil partage)

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VERBOSE=false
FICHIER=""

# Fonction pour afficher l'aide
afficher_aide() {
    echo "Usage: $0 <fichier> [options]"
    echo ""
    echo "Verifie si un fichier ebauche respecte les exigences minimales."
    echo ""
    echo "Options:"
    echo "  --verbose     Afficher les details"
    echo "  --aide        Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 protocole-xxx.001.01.ebauche.md"
    echo "  $0 --verbose protocole-xxx.001.01.ebauche.md"
}

# Fonction pour verifier si le fichier est un ebauche
verifier_statut() {
    local fichier=$1
    local basename=$(basename "$fichier")
    
    if echo "$basename" | grep -qE '\.ebauche\.md$'; then
        return 0
    else
        echo -e "${RED}[ERREUR] Le fichier n'est pas un ebauche : $basename${NC}"
        return 1
    fi
}

# Fonction pour verifier la structure du nom
verifier_nommage() {
    local fichier=$1
    local basename=$(basename "$fichier")
    
    # Format attendu: [type]-[theme].[id].[class].ebauche.md
    # ou [theme].[id].[class].ebauche.md (pour les fichiers plateforme)
    
    if echo "$basename" | grep -qE '^([a-zA-Z0-9_-]+-)?[a-zA-Z0-9_-]+\.[0-9]{3}\.[0-9]{2}\.ebauche\.md$'; then
        return 0
    else
        echo -e "${YELLOW}[ATTENTION]  Le nom ne respecte pas la convention : $basename${NC}"
        echo "  Format attendu: [type]-[theme].[id].[class].ebauche.md"
        return 1
    fi
}

# Fonction pour verifier la presence de sections minimales
verifier_sections() {
    local fichier=$1
    local erreurs=0
    
    # Verifier la presence d'un titre
    if ! grep -q "^#" "$fichier"; then
        echo -e "${RED}[ERREUR] Pas de titre principal (h1)${NC}"
        erreurs=$((erreurs + 1))
    fi
    
    return $erreurs
}

# Fonction pour verifier la presence de contenu minimal
verifier_contenu() {
    local fichier=$1
    local lignes=$(wc -l < "$fichier")
    local erreurs=0
    
    # Verifier le nombre de lignes minimal
    if [ "$lignes" -lt 5 ]; then
        echo -e "${RED}[ERREUR] Trop peu de contenu : $lignes lignes (minimum 5)${NC}"
        erreurs=$((erreurs + 1))
    fi
    
    return $erreurs
}

# Fonction pour verifier si le fichier est TROP complet pour un ebauche
verifier_pas_trop_complet() {
    local fichier=$1
    local warnings=0
    
    # Verifier la presence de frontmatter
    if head -n 1 "$fichier" | grep -q "^---"; then
        echo -e "${YELLOW}[ATTENTION]  Frontmatter present (inutile pour un ebauche)${NC}"
        warnings=$((warnings + 1))
    fi
    
    # Verifier la presence de tableaux
    if grep -qE "^\|.*\|" "$fichier"; then
        echo -e "${YELLOW}[ATTENTION]  Tableaux presents (peut-etre trop structure pour un ebauche)${NC}"
        warnings=$((warnings + 1))
    fi
    
    # Verifier la presence de many sections
    local nb_sections=$(grep -c "^## " "$fichier" 2>/dev/null || echo 0)
    if [ "$nb_sections" -gt 3 ]; then
        echo -e "${YELLOW}[ATTENTION]  $nb_sections sections (peut-etre trop structure pour un ebauche)${NC}"
        warnings=$((warnings + 1))
    fi
    
    return $warnings
}

# Fonction principale de validation
valider_ebauche() {
    local fichier=$1
    local erreurs_totales=0
    local avertissements=0
    
    echo -e "${BLUE}=== Validation du fichier ebauche ===${NC}"
    echo "Fichier : $fichier"
    echo ""
    
    # Verifier que le fichier existe
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve : $fichier${NC}"
        exit 1
    fi
    
    # Verifier le statut
    verifier_statut "$fichier"
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    # Verifier le nommage
    echo -e "${BLUE}--- Verification du nommage ---${NC}"
    verifier_nommage "$fichier"
    if [ $? -ne 0 ]; then
        avertissements=$((avertissements + 1))
    fi
    
    # Verifier la structure
    echo ""
    echo -e "${BLUE}--- Verification de la structure minimale ---${NC}"
    verifier_sections "$fichier"
    if [ $? -ne 0 ]; then
        erreurs_totales=$((erreurs_totales + 1))
    fi
    
    # Verifier le contenu
    echo ""
    echo -e "${BLUE}--- Verification du contenu minimal ---${NC}"
    verifier_contenu "$fichier"
    if [ $? -ne 0 ]; then
        erreurs_totales=$((erreurs_totales + 1))
    fi
    
    # Verifier si le fichier est trop complet
    echo ""
    echo -e "${BLUE}--- Verification : pas trop complet pour un ebauche ---${NC}"
    verifier_pas_trop_complet "$fichier"
    if [ $? -ne 0 ]; then
        avertissements=$((avertissements + 1))
    fi
    
    # Resume
    echo ""
    echo -e "${BLUE}=== Resume ===${NC}"
    echo "Erreurs : $erreurs_totales"
    echo "Avertissements : $avertissements"
    
    if [ "$erreurs_totales" -eq 0 ]; then
        echo ""
        echo -e "${GREEN}[OK] Le fichier ebauche respecte les exigences minimales${NC}"
        if [ "$avertissements" -gt 0 ]; then
            echo -e "${YELLOW}[ATTENTION]  Cependant, il semble trop structure pour un ebauche${NC}"
            echo -e "${YELLOW}    Considerez passer au statut 'prepare'${NC}"
        fi
        exit 0
    else
        echo ""
        echo -e "${RED}[ERREUR] Le fichier ebauche ne respecte pas les exigences minimales${NC}"
        exit 1
    fi
}

# Parser les arguments
while [ $# -gt 0 ]; do
    case $1 in
        "--aide"|"--help"|"-h")
            afficher_aide
            exit 0
            ;;
        "--verbose")
            VERBOSE=true
            shift
            ;;
        *)
            FICHIER="$1"
            shift
            ;;
    esac
done

# Verifier qu'un fichier a ete specifie
if [ -z "$FICHIER" ]; then
    echo -e "${RED}[ERREUR] Aucun fichier specifie${NC}"
    afficher_aide
    exit 1
fi

# Valider le fichier
valider_ebauche "$FICHIER"
