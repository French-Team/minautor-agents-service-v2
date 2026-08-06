#!/bin/bash
# corriger-accents.sh
# Outil pour détecter et corriger les accents et caractères non-ASCII
# Conforme à la règle regles-emojis-ascii.md

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Symboles de remplacement (ASCII)
INFO="[INFO]"
OK="[OK]"
ERREUR="[ERREUR]"
ATTENTION="[ATTENTION]"

# Répertoire de l'outil
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DICTIONNAIRE_DEFAUT="${SCRIPT_DIR}/dictionnaire-accents.txt"

# Fonction d'aide
utilisation() {
    echo "Utilisation: $0 [OPTIONS] <fichier>"
    echo ""
    echo "Options:"
    echo "  --dry-run        Afficher les changements sans les appliquer"
    echo "  --verbose        Afficher les détails"
    echo "  --dictionnaire   Chemin vers le dictionnaire (défaut: dictionnaire-accents.txt)"
    echo "  --help           Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 fichier.md                    # Corriger les accents"
    echo "  $0 --dry-run fichier.md          # Voir les changements"
    echo "  $0 --verbose --dry-run fichier.md  # Détails + preview"
}

# Paramètres
DRY_RUN=0
VERBOSE=0
DICTIONNAIRE="$DICTIONNAIRE_DEFAUT"
FICHIER=""

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        --verbose)
            VERBOSE=1
            shift
            ;;
        --dictionnaire)
            DICTIONNAIRE="$2"
            shift 2
            ;;
        --help|-h)
            utilisation
            exit 0
            ;;
        -*)
            echo -e "${ERREUR} Option inconnue: $1"
            utilisation
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
    echo -e "${ERREUR} Aucun fichier spécifié"
    utilisation
    exit 1
fi

if [[ ! -f "$FICHIER" ]]; then
    echo -e "${ERREUR} Fichier non trouvé: $FICHIER"
    exit 1
fi

# Vérification du dictionnaire
if [[ ! -f "$DICTIONNAIRE" ]]; then
    echo -e "${ERREUR} Dictionnaire non trouvé: $DICTIONNAIRE"
    exit 1
fi

echo -e "${INFO} Correction des accents et caractères non-ASCII"
echo "Fichier: $FICHIER"
echo "Dictionnaire: $DICTIONNAIRE"
echo ""

# Compteur de changements
CHANGEMENTS=0

# Création du fichier temporaire
TEMP_FILE=$(mktemp)
cp "$FICHIER" "$TEMP_FILE"

# Détection initiale des caractères non-ASCII
NON_ASCII_AVANT=$(perl -CSD -ne "print if /[^\x00-\x7F]/" "$TEMP_FILE" | wc -l)
if [[ "$VERBOSE" -eq 1 ]]; then
    echo -e "${INFO} Lignes avec caractères non-ASCII avant correction: $NON_ASCII_AVANT"
fi

# Si aucun caractère non-ASCII, on arrête
if [[ "$NON_ASCII_AVANT" -eq 0 ]]; then
    echo -e "${OK} Aucun caractère non-ASCII détecté"
    rm -f "$TEMP_FILE"
    exit 0
fi

# Lecture du dictionnaire et application des remplacements avec perl
while IFS='|' read -r accent remplacement; do
    # Ignorer les commentaires et lignes vides
    [[ "$accent" =~ ^#.*$ ]] && continue
    [[ -z "$accent" ]] && continue
    
    # Échapper les caractères spéciaux pour perl
    accent_escaped=$(printf '%s' "$accent" | sed 's/[.[\*^$()+?{|\\]/\\&/g')
    remplacement_escaped=$(printf '%s' "$remplacement" | sed 's/[.[\*^$()+?{|\\]/\\&/g')
    
    # Compter les occurrences avant
    AVANT=$(perl -CSD -ne "print if /$accent_escaped/" "$TEMP_FILE" | wc -l)
    
    if [[ "$AVANT" -gt 0 ]]; then
        # Remplacement avec perl
        perl -CSD -pi -e "s/$accent_escaped/$remplacement_escaped/g" "$TEMP_FILE"
        
        CHANGEMENTS=$((CHANGEMENTS + AVANT))
        
        if [[ "$VERBOSE" -eq 1 ]]; then
            echo -e "${OK} Remplacé: '$accent' -> '$remplacement' ($AVANT lignes affectées)"
        fi
    fi
done < "$DICTIONNAIRE"

# Vérification des caractères non-ASCII restants
NON_ASCII_APRES=$(perl -CSD -ne "print if /[^\x00-\x7F]/" "$TEMP_FILE" | wc -l)

if [[ "$VERBOSE" -eq 1 ]]; then
    echo ""
    echo "Lignes avec caractères non-ASCII après correction: $NON_ASCII_APRES"
fi

# Application ou affichage
if [[ "$DRY_RUN" -eq 1 ]]; then
    echo -e "${INFO} [DRY-RUN] Changements proposés:"
    echo ""
    diff --color=always "$FICHIER" "$TEMP_FILE" || true
    echo ""
    echo -e "${INFO} Total: $CHANGEMENTS lignes modifiées"
    echo -e "${INFO} Aucune modification appliquée (dry-run)"
else
    if [[ "$CHANGEMENTS" -gt 0 ]]; then
        # Sauvegarde
        cp "$FICHIER" "${FICHIER}.bak"
        
        # Application
        cp "$TEMP_FILE" "$FICHIER"
        
        echo -e "${OK} $CHANGEMENTS lignes modifiées"
        echo -e "${INFO} Sauvegarde créée: ${FICHIER}.bak"
    else
        echo -e "${OK} Aucun accent ou caractère non-ASCII détecté"
    fi
fi

# Nettoyage
rm -f "$TEMP_FILE"

exit 0