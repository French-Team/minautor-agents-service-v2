#!/bin/bash
# corriger-liens.sh
# Corrige les liens casses dans un fichier Markdown
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
    echo "  corriger-liens v${VERSION}"
    echo "  Corrige les liens casses"
    echo "=========================================="
    echo ""
    echo "Usage: corriger-liens [OPTIONS] FICHIER"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --dry-run           Simuler sans modifier"
    echo "  --verbose, -v       Afficher les details"
    echo "  --version           Afficher la version"
    echo ""
    echo "Arguments:"
    echo "  FICHIER             Fichier Markdown a corriger"
    echo ""
    echo "Exemples:"
    echo "  corriger-liens fichier.md"
    echo "  corriger-liens --dry-run fichier.md"
    echo ""
}

# Fonction pour corriger les liens
corriger_liens() {
    local fichier=$1
    local dry_run=$2
    local verbose=$3

    local liens_corriges=0
    local liens_valides=0

    # Obtenir le repertoire du fichier
    local dossier_fichier
    dossier_fichier=$(dirname "$fichier")

    echo -e "${BLUE}[OUTIL] Correction des liens dans : ${fichier}${NC}"
    echo -e "${BLUE}[DOSSIER] Repertoire du fichier : ${dossier_fichier}${NC}"
    echo ""

    # Creer une copie de sauvegarde
    if [[ "$dry_run" == "false" ]]; then
        cp "$fichier" "${fichier}.backup"
        echo -e "${YELLOW}[CHECKLIST] Copie de sauvegarde : ${fichier}.backup${NC}"
    fi

    # Extraire les liens Markdown [texte](chemin) avec sed
    local liens
    liens=$(sed -n 's/.*\[\([^]]*\)\](\([^)]*\)).*/\1|\2/p' "$fichier" 2>/dev/null)

    if [[ -z "$liens" ]]; then
        echo -e "${YELLOW}Aucun lien Markdown trouve.${NC}"
        return 0
    fi

    # Compter le nombre total de liens
    local total
    total=$(echo "$liens" | wc -l)

    echo -e "${BLUE}Trouve ${total} lien(s) Markdown${NC}"
    echo ""

    # Traiter chaque lien
    while IFS= read -r lien; do
        # Separer texte et chemin (separateur |)
        local texte
        local chemin
        texte=$(echo "$lien" | cut -d'|' -f1)
        chemin=$(echo "$lien" | cut -d'|' -f2)

        # Verifier si c'est un lien interne (pas http/https)
        if echo "$chemin" | grep -qE '^https?://'; then
            # Lien externe - on ne le corrige pas
            liens_valides=$((liens_valides + 1))
            if [[ "$verbose" == "true" ]]; then
                echo -e "${YELLOW}[LIEN] ${texte} -> ${chemin} (externe)${NC}"
            fi
        else
            # Lien interne - verifier depuis le repertoire du fichier
            local chemin_complet
            chemin_complet=$(cd "$dossier_fichier" 2>/dev/null && cd "$(dirname "$chemin")" 2>/dev/null && pwd)/$(basename "$chemin") 2>/dev/null || echo "${dossier_fichier}/${chemin}"

            if [[ -f "$chemin_complet" ]] || [[ -d "$chemin_complet" ]]; then
                liens_valides=$((liens_valides + 1))
                if [[ "$verbose" == "true" ]]; then
                    echo -e "${GREEN}[OK] ${texte} -> ${chemin}${NC}"
                fi
            else
                echo -e "${RED}[ERREUR] Lien casse : ${texte} -> ${chemin}${NC}"
                echo -e "   Chemin verifie : ${chemin_complet}"
                
                # Suggestions de correction
                echo "  Suggestions :"
                echo "    - Verifier le nom du fichier"
                echo "    - Verifier le chemin"
                echo "    - Creer le fichier manquant"
                
                liens_corriges=$((liens_corriges + 1))
            fi
        fi
    done <<< "$liens"

    echo ""
    echo -e "${BLUE}Resume :${NC}"
    echo -e "${GREEN}[OK] Liens valides : ${liens_valides}${NC}"
    echo -e "${YELLOW}[ATTENTION]  Liens a corriger : ${liens_corriges}${NC}"

    if [[ "$dry_run" == "true" ]]; then
        echo -e "${YELLOW}Mode dry-run : aucun fichier modifie${NC}"
    else
        echo -e "${GREEN}Copie de sauvegarde : ${fichier}.backup${NC}"
    fi

    return 0
}

# Valeurs par defaut
DRY_RUN="false"
VERBOSE="false"

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
            echo "corriger-liens v${VERSION}"
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
corriger_liens "$FICHIER" "$DRY_RUN" "$VERBOSE"

exit 0
