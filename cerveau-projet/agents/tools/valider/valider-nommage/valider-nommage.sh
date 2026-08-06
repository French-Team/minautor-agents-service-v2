#!/bin/bash
# valider-nommage.sh
# Vérifier que le nommage est correct selon les conventions
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
NC='\033[0m' # No Color

# Fonction d'aide
aide() {
    echo "=========================================="
    echo "  valider-nommage v${VERSION}"
    echo "  Vérifier le nommage selon les conventions"
    echo "=========================================="
    echo ""
    echo "Usage: valider-nommage [OPTIONS] CHEMIN"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les détails"
    echo "  --version           Afficher la version"
    echo "  --type TYPE         Type de fichier (protocole, convention, agent, outil)"
    echo ""
    echo "Types de fichiers:"
    echo "  protocole     nom-protocole.XX.XX.statut.md"
    echo "  agent         nom-agent.md"
    echo "  outil         nom-outil.sh ou nom-outil.md"
    echo "  convention    convention-nom.md"
    echo ""
    echo "Statuts valides (protocoles):"
    echo "  ebauche, prepare, dev, test, valide"
    echo ""
    echo "Exemples:"
    echo "  valider-nommage --type protocole chemin/vers/protocole.md"
    echo "  valider-nommage --type agent chemin/vers/agent.md"
    echo ""
}

# Fonction pour valider le nommage d'un protocole
valider_protocole() {
    local fichier=$1
    local verbose=$2
    local erreurs=0

    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    # Extraire les parties du nom
    local nom_part=$(echo "$basename" | cut -d'.' -f1)
    local major_part=$(echo "$basename" | cut -d'.' -f2)
    local minor_part=$(echo "$basename" | cut -d'.' -f3)
    local statut_part=$(echo "$basename" | cut -d'.' -f4)

    # Vérifier que les parties existent
    if [[ -z "$nom_part" || -z "$major_part" || -z "$minor_part" || -z "$statut_part" ]]; then
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : nom-protocole.XX.XX.statut.md"
        return 1
    fi

    # Vérifier que major et minor sont des nombres
    if ! [[ "$major_part" =~ ^[0-9]+$ ]] || ! [[ "$minor_part" =~ ^[0-9]+$ ]]; then
        echo -e "  ${RED}[ERREUR] Version invalide : ${major_part}.${minor_part}${NC}"
        echo -e "    Les versions doivent être des nombres"
        return 1
    fi

    # Vérifier que le statut est valide
    # NB: ASCII pur uniquement (prepare, jamais preparé) pour eviter les bugs d'encodage
    case "$statut_part" in
        ebauche|prepare|dev|test|valide)
            echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
            
            if [[ "$verbose" == "true" ]]; then
                echo -e "    Nom : ${nom_part}"
                echo -e "    Version : ${major_part}.${minor_part}"
                echo -e "    Statut : ${statut_part}"
            fi
            return 0
            ;;
        *)
            echo -e "  ${RED}[ERREUR] Statut invalide : ${statut_part}${NC}"
            echo -e "    Statuts valides : ebauche, prepare, dev, test, valide"
            return 1
            ;;
    esac
}

# Fonction pour valider le nommage d'un agent
valider_agent() {
    local fichier=$1
    local verbose=$2

    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    # Vérifier le format : nom-agent.md
    if [[ "$basename" =~ ^[a-z]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
        return 0
    else
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : nom-agent.md"
        return 1
    fi
}

# Fonction pour valider le nommage d'un outil
valider_outil() {
    local fichier=$1
    local verbose=$2

    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    # Vérifier le format : nom-outil.sh ou nom-outil.md
    if [[ "$basename" =~ ^[a-z-]+\.sh$ ]] || [[ "$basename" =~ ^[a-z-]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
        return 0
    else
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : nom-outil.sh ou nom-outil.md"
        return 1
    fi
}

# Fonction pour valider le nommage d'une convention
valider_convention() {
    local fichier=$1
    local verbose=$2

    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    # Vérifier le format : convention-nom.md
    if [[ "$basename" =~ ^convention-[a-z-]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
        return 0
    else
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : convention-nom.md"
        return 1
    fi
}

# Valeurs par défaut
VERBOSE="false"
TYPE=""
FICHIER=""

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
            echo "valider-nommage v${VERSION}"
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

# Vérifier le type
if [[ -z "$TYPE" ]]; then
    echo "Erreur: Type non spécifié"
    echo "Utilisez --type pour spécifier le type"
    exit 1
fi

# Exécution selon le type
case $TYPE in
    protocole)
        valider_protocole "$FICHIER" "$VERBOSE"
        ;;
    agent)
        valider_agent "$FICHIER" "$VERBOSE"
        ;;
    outil)
        valider_outil "$FICHIER" "$VERBOSE"
        ;;
    convention)
        valider_convention "$FICHIER" "$VERBOSE"
        ;;
    *)
        echo "Erreur: Type inconnu '$TYPE'"
        echo "Types disponibles : protocole, agent, outil, convention"
        exit 1
        ;;
esac

exit $?
