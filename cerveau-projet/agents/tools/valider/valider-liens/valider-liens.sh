#!/bin/bash
# valider-liens.sh
# Valide les liens dans un fichier Markdown
# Version: 0.4.0
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
VERSION="0.4.0"
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
    echo "  valider-liens v${VERSION}"
    echo "  Valide les liens dans un fichier Markdown"
    echo "=========================================="
    echo ""
    echo "Usage: valider-liens [OPTIONS] FICHIER"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les détails"
    echo "  --version           Afficher la version"
    echo "  --racine RACINE     Racine du projet (défaut: .)"
    echo ""
    echo "Arguments:"
    echo "  FICHIER             Fichier Markdown à valider"
    echo ""
    echo "Exemples:"
    echo "  valider-liens fichier.md"
    echo "  valider-liens --verbose --racine /chemin/projet autre-fichier.md"
    echo ""
}

# Fonction pour valider les liens
valider_liens() {
    local fichier=$1
    local verbose=$2
    local racine=$3

    local liens_valides=0
    local liens_invalides=0
    local liens_externes=0

    # Obtenir le répertoire du fichier
    local dossier_fichier
    dossier_fichier=$(dirname "$fichier")

    echo -e "${BLUE}[LIEN] Validation des liens dans : ${fichier}${NC}"
    echo -e "${BLUE}[DOSSIER] Répertoire du fichier : ${dossier_fichier}${NC}"
    echo ""

    # Extraire les liens Markdown [texte](chemin) avec sed
    local liens
    liens=$(sed -n 's/.*\[\([^]]*\)\](\([^)]*\)).*/\1|\2/p' "$fichier" 2>/dev/null)

    if [[ -z "$liens" ]]; then
        echo -e "${YELLOW}Aucun lien Markdown trouvé.${NC}"
        return 0
    fi

    # Compter le nombre total de liens
    local total
    total=$(echo "$liens" | wc -l)

    echo -e "${BLUE}Trouvé ${total} lien(s) Markdown${NC}"
    echo ""

    # Traiter chaque lien
    while IFS= read -r lien; do
        # Séparer texte et chemin (séparateur |)
        local texte
        local chemin
        texte=$(echo "$lien" | cut -d'|' -f1)
        chemin=$(echo "$lien" | cut -d'|' -f2)

        # Vérifier si c'est un lien interne (pas http/https)
        if echo "$chemin" | grep -qE '^https?://'; then
            # Lien externe
            liens_externes=$((liens_externes + 1))
            if [[ "$verbose" == "true" ]]; then
                echo -e "${YELLOW}[LIEN] ${texte} -> ${chemin} (externe)${NC}"
            fi
        else
            # Lien interne - vérifier depuis le répertoire du fichier
            local chemin_complet="${dossier_fichier}/${chemin}"
            
            # Normaliser le chemin (gérer ../)
            chemin_complet=$(cd "$dossier_fichier" 2>/dev/null && cd "$(dirname "$chemin")" 2>/dev/null && pwd)/$(basename "$chemin") 2>/dev/null || echo "$chemin_complet"
            
            if [[ -f "$chemin_complet" ]] || [[ -d "$chemin_complet" ]]; then
                liens_valides=$((liens_valides + 1))
                if [[ "$verbose" == "true" ]]; then
                    echo -e "${GREEN}[OK] ${texte} -> ${chemin}${NC}"
                fi
            else
                liens_invalides=$((liens_invalides + 1))
                echo -e "${RED}[ERREUR] ${texte} -> ${chemin}${NC}"
                if [[ "$verbose" == "true" ]]; then
                    echo -e "   Chemin vérifié : ${chemin_complet}"
                fi
            fi
        fi
    done <<< "$liens"

    echo ""
    echo -e "${BLUE}Résumé :${NC}"
    echo -e "${GREEN}[OK] Liens valides : ${liens_valides}${NC}"
    echo -e "${RED}[ERREUR] Liens invalides : ${liens_invalides}${NC}"
    echo -e "${YELLOW}[LIEN] Liens externes : ${liens_externes}${NC}"

    if [[ $liens_invalides -gt 0 ]]; then
        return 1
    else
        return 0
    fi
}

# Valeurs par défaut
VERBOSE="false"
RACINE="."

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
            echo "valider-liens v${VERSION}"
            exit 0
            ;;
        --racine)
            RACINE="$2"
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

# Exécution
valider_liens "$FICHIER" "$VERBOSE" "$RACINE"

exit $?
