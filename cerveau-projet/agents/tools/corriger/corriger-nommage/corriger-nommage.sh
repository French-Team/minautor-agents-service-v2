#!/bin/bash
# corriger-nommage.sh
# Corriger le nommage des fichiers selon les conventions
# Version : 0.2.0
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
    echo "  corriger-nommage v${VERSION}"
    echo "  Corriger le nommage des fichiers"
    echo "=========================================="
    echo ""
    echo "Usage: corriger-nommage [OPTIONS] FICHIER"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --dry-run           Simuler sans modifier"
    echo "  --verbose, -v       Afficher les details"
    echo "  --version           Afficher la version"
    echo "  --type TYPE         Type de fichier (protocole, convention, agent, outil)"
    echo ""
    echo "Exemples:"
    echo "  corriger-nommage --type protocole chemin/vers/protocole.md"
    echo "  corriger-nommage --dry-run --type agent chemin/vers/agent.md"
    echo ""
}

# Fonction pour corriger le nommage d'un protocole
corriger_protocole() {
    local fichier=$1
    local dry_run=$2
    local verbose=$3

    local basename=$(basename "$fichier")
    local dossier=$(dirname "$fichier")

    echo -e "${BLUE}[OUTIL] Correction du nommage : ${basename}${NC}"
    echo ""

    # Extraire les parties du nom
    local nom_part=$(echo "$basename" | cut -d'.' -f1)
    local major_part=$(echo "$basename" | cut -d'.' -f2)
    local minor_part=$(echo "$basename" | cut -d'.' -f3)
    local statut_part=$(echo "$basename" | cut -d'.' -f4)

    # Verifier si le format est correct
    if [[ -z "$nom_part" || -z "$major_part" || -z "$minor_part" || -z "$statut_part" ]]; then
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Impossible de corriger automatiquement"
        return 1
    fi

    # Construire le nouveau nom
    local nouveau_nom="${nom_part}.${major_part}.${minor_part}.${statut_part}.md"

    # Verifier si une correction est necessaire
    if [[ "$basename" == "$nouveau_nom" ]]; then
        echo -e "  ${GREEN}[OK] Aucune correction necessaire${NC}"
        return 0
    fi

    echo -e "  ${YELLOW}[ATTENTION]  Correction necessaire :${NC}"
    echo -e "    Actuel : ${basename}"
    echo -e "    Nouveau : ${nouveau_nom}"

    if [[ "$dry_run" == "true" ]]; then
        echo -e "  ${YELLOW}Mode dry-run : aucun fichier modifie${NC}"
    else
        local chemin_complet="${dossier}/${nouveau_nom}"
        if [[ -f "$chemin_complet" ]]; then
            echo -e "  ${RED}[ERREUR] Le fichier destination existe deja${NC}"
            return 1
        fi
        
        mv "$fichier" "$chemin_complet"
        echo -e "  ${GREEN}[OK] Fichier renomme${NC}"
    fi

    return 0
}

# Fonction pour corriger le nommage d'un agent
corriger_agent() {
    local fichier=$1
    local dry_run=$2
    local verbose=$3

    local basename=$(basename "$fichier")
    local dossier=$(dirname "$fichier")

    echo -e "${BLUE}[OUTIL] Correction du nommage : ${basename}${NC}"
    echo ""

    # Verifier le format : nom-agent.md
    if [[ "$basename" =~ ^[a-z]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Aucune correction necessaire${NC}"
        return 0
    fi

    # Extraire le nom sans extension
    local nom=$(echo "$basename" | sed 's/\.md$//')
    local nouveau_nom="${nom}.md"

    echo -e "  ${YELLOW}[ATTENTION]  Correction necessaire :${NC}"
    echo -e "    Actuel : ${basename}"
    echo -e "    Nouveau : ${nouveau_nom}"

    if [[ "$dry_run" == "true" ]]; then
        echo -e "  ${YELLOW}Mode dry-run : aucun fichier modifie${NC}"
    else
        local chemin_complet="${dossier}/${nouveau_nom}"
        if [[ -f "$chemin_complet" ]]; then
            echo -e "  ${RED}[ERREUR] Le fichier destination existe deja${NC}"
            return 1
        fi
        
        mv "$fichier" "$chemin_complet"
        echo -e "  ${GREEN}[OK] Fichier renomme${NC}"
    fi

    return 0
}

# Fonction pour corriger le nommage d'un outil
corriger_outil() {
    local fichier=$1
    local dry_run=$2
    local verbose=$3

    local basename=$(basename "$fichier")
    local dossier=$(dirname "$fichier")

    echo -e "${BLUE}[OUTIL] Correction du nommage : ${basename}${NC}"
    echo ""

    # Verifier le format : nom-outil.sh ou nom-outil.md
    if [[ "$basename" =~ ^[a-z-]+\.sh$ ]] || [[ "$basename" =~ ^[a-z-]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Aucune correction necessaire${NC}"
        return 0
    fi

    # Extraire le nom et l'extension
    local nom=$(echo "$basename" | sed 's/\.[^.]*$//')
    local extension="${basename##*.}"
    local nouveau_nom="${nom}.${extension}"

    echo -e "  ${YELLOW}[ATTENTION]  Correction necessaire :${NC}"
    echo -e "    Actuel : ${basename}"
    echo -e "    Nouveau : ${nouveau_nom}"

    if [[ "$dry_run" == "true" ]]; then
        echo -e "  ${YELLOW}Mode dry-run : aucun fichier modifie${NC}"
    else
        local chemin_complet="${dossier}/${nouveau_nom}"
        if [[ -f "$chemin_complet" ]]; then
            echo -e "  ${RED}[ERREUR] Le fichier destination existe deja${NC}"
            return 1
        fi
        
        mv "$fichier" "$chemin_complet"
        echo -e "  ${GREEN}[OK] Fichier renomme${NC}"
    fi

    return 0
}

# Fonction pour corriger le nommage d'une convention
corriger_convention() {
    local fichier=$1
    local dry_run=$2
    local verbose=$3

    local basename=$(basename "$fichier")
    local dossier=$(dirname "$fichier")

    echo -e "${BLUE}[OUTIL] Correction du nommage : ${basename}${NC}"
    echo ""

    # Verifier le format : convention-nom.md
    if [[ "$basename" =~ ^convention-[a-z-]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Aucune correction necessaire${NC}"
        return 0
    fi

    # Extraire le nom
    local nom=$(echo "$basename" | sed 's/\.md$//' | sed 's/^convention-//')
    local nouveau_nom="convention-${nom}.md"

    echo -e "  ${YELLOW}[ATTENTION]  Correction necessaire :${NC}"
    echo -e "    Actuel : ${basename}"
    echo -e "    Nouveau : ${nouveau_nom}"

    if [[ "$dry_run" == "true" ]]; then
        echo -e "  ${YELLOW}Mode dry-run : aucun fichier modifie${NC}"
    else
        local chemin_complet="${dossier}/${nouveau_nom}"
        if [[ -f "$chemin_complet" ]]; then
            echo -e "  ${RED}[ERREUR] Le fichier destination existe deja${NC}"
            return 1
        fi
        
        mv "$fichier" "$chemin_complet"
        echo -e "  ${GREEN}[OK] Fichier renomme${NC}"
    fi

    return 0
}

# Valeurs par defaut
VERBOSE="false"
DRY_RUN="false"
TYPE=""
FICHIER=""

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --aide|-h)
            aide
            exit 0
            ;;
        --dry-run)
            DRY_RUN="true"
            shift
            ;;
        --verbose|-v)
            VERBOSE="true"
            shift
            ;;
        --version)
            echo "corriger-nommage v${VERSION}"
            exit 0
            ;;
        --type)
            TYPE="$2"
            shift 2
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

# Verifier le type
if [[ -z "$TYPE" ]]; then
    echo "Erreur: Type non specifie"
    echo "Utilisez --type pour specifier le type"
    exit 1
fi

# Execution selon le type
case $TYPE in
    protocole)
        corriger_protocole "$FICHIER" "$DRY_RUN" "$VERBOSE"
        ;;
    agent)
        corriger_agent "$FICHIER" "$DRY_RUN" "$VERBOSE"
        ;;
    outil)
        corriger_outil "$FICHIER" "$DRY_RUN" "$VERBOSE"
        ;;
    convention)
        corriger_convention "$FICHIER" "$DRY_RUN" "$VERBOSE"
        ;;
    *)
        echo "Erreur: Type inconnu '$TYPE'"
        echo "Types disponibles : protocole, agent, outil, convention"
        exit 1
        ;;
esac

exit $?
