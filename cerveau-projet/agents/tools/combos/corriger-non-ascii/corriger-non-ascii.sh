#!/bin/bash
# corriger-non-ascii.sh
# Combo corriger-non-ascii : detecte et corrige les accents et emojis
# Ressource partagee : utilise par Themis, Buffy, ou tout autre agent
# Version : 0.1.0
#
# Chainage :
#   1. rechercher-accents-sensibles -> detecter les problemes
#   2. corriger-emojis -> remplacer les emojis
#   3. corriger-accents -> remplacer les accents
#   4. rechercher-accents-sensibles -> verifier le nettoyage

VERSION="0.1.0"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR/../.."

CORRIGER_EMOJIS="$TOOLS_DIR/corriger/corriger-emojis/corriger-emojis.sh"
CORRIGER_ACCENTS="$TOOLS_DIR/corriger/corriger-accents/corriger-accents.sh"
RECHERCHER="$TOOLS_DIR/explorer/rechercher-accents-sensibles/rechercher-accents-sensibles.sh"

afficher_aide() {
    echo "=== corriger-non-ascii v${VERSION} ==="
    echo ""
    echo "Usage: $0 [DOSSIER] [OPTIONS]"
    echo ""
    echo "Combo : detecte et corrige les accents et emojis."
    echo "Ressource partagee pour tous les agents."
    echo ""
    echo "Options:"
    echo "  --dry-run     Afficher les changements sans les appliquer"
    echo "  --rapport     Sauvegarder un rapport dans $TOOLS_DIR/../themis/rapports/"
    echo "  --help        Afficher cette aide"
}

DOSSIER="${1:-.}"
DRY_RUN=false
SAUVEGARDER=false

while [ $# -gt 0 ]; do
    case $1 in
        --dry-run) DRY_RUN=true; shift ;;
        --rapport) SAUVEGARDER=true; shift ;;
        --help|-h) afficher_aide; exit 0 ;;
        *) DOSSIER="$1"; shift ;;
    esac
done

echo -e "${BLUE}=== corriger-non-ascii v${VERSION} ===${NC}"
echo "Cible : $DOSSIER"
echo "Mode : $([ \"$DRY_RUN\" = true ] && echo 'DRY-RUN' || echo 'APPLICATION')"
echo "Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

if [ ! -d "$DOSSIER" ]; then
    echo -e "${RED}[ERREUR] Le dossier n'existe pas : $DOSSIER${NC}"
    exit 1
fi

# Etape 1 : Detection
echo -e "${BLUE}--- Etape 1/4 : Detection des problemes ---${NC}"
AVANT=$(bash "$RECHERCHER" "$DOSSIER" 2>&1 | grep -c '\[' || true)
echo "Lignes detectees avant correction : $AVANT"
echo ""

# Etape 2 : Correction des emojis
echo -e "${BLUE}--- Etape 2/4 : Correction des emojis ---${NC}"
if [ "$DRY_RUN" = true ]; then
    bash "$CORRIGER_EMOJIS" --dry-run "$DOSSIER" 2>&1 | tail -5
else
    bash "$CORRIGER_EMOJIS" "$DOSSIER" 2>&1 | tail -5
fi
echo ""

# Etape 3 : Correction des accents (fichier par fichier)
echo -e "${BLUE}--- Etape 3/4 : Correction des accents ---${NC}"
NB_ACCENTS=0
while IFS= read -r fichier; do
    basename_f=$(basename "$fichier")
    # Exclure les dictionnaires et le fichier de regles
    case "$basename_f" in
        dictionnaire-*.txt|regles-emojis-ascii.md) continue ;;
    esac
    # Exclure le dossier exemples
    case "$fichier" in
        */exemples/*) continue ;;
    esac
    if [ "$DRY_RUN" = true ]; then
        resultat=$(bash "$CORRIGER_ACCENTS" --dry-run "$fichier" 2>&1)
    else
        resultat=$(bash "$CORRIGER_ACCENTS" "$fichier" 2>&1)
    fi
    if echo "$resultat" | grep -qE 'Total.*modifie|Remplace'; then
        NB_ACCENTS=$((NB_ACCENTS + 1))
        echo "  $([ "$DRY_RUN" = true ] && echo '[DRY-RUN]' || echo '[OK]') $fichier"
    fi
done < <(find "$DOSSIER/cerveau-projet" \( -name "*.md" -o -name "*.sh" \) -type f 2>/dev/null | tr -d '\r')
echo "Fichiers avec accents corriges : $NB_ACCENTS"
echo ""

# Etape 4 : Verification
echo -e "${BLUE}--- Etape 4/4 : Verification ---${NC}"
APRES=$(bash "$RECHERCHER" "$DOSSIER" 2>&1 | grep -c '\[' || true)
echo "Lignes detectees apres correction : $APRES"

if [ "$APRES" -lt "$AVANT" ]; then
    echo -e "${GREEN}[OK] Reduction : $AVANT -> $APRES ($(( AVANT - APRES )) lignes corrigees)${NC}"
elif [ "$AVANT" -eq 0 ] && [ "$APRES" -eq 0 ]; then
    echo -e "${GREEN}[OK] Aucun probleme detecte${NC}"
else
    echo -e "${YELLOW}[INFO] $APRES lignes restantes (accents dans le texte francais ou exceptions)${NC}"
fi

# Rapport
if [ "$SAUVEGARDER" = true ]; then
    RAPPORT_DIR="$DOSSIER/cerveau-projet/agents/themis/rapports"
    DATE=$(date '+%Y-%m-%d-%H-%M')
    RAPPORT_FILE="$RAPPORT_DIR/corriger-non-ascii-$DATE.md"
    mkdir -p "$RAPPORT_DIR"

    {
        echo "# Rapport corriger-non-ascii -- $DATE"
        echo ""
        echo "## Contexte"
        echo "- Cible : $DOSSIER"
        echo "- Mode : $([ \"$DRY_RUN\" = true ] && echo 'DRY-RUN' || echo 'APPLICATION')"
        echo ""
        echo "## Resultats"
        echo "- Lignes avant : $AVANT"
        echo "- Lignes apres : $APRES"
        echo "- Reduction : $(( AVANT - APRES )) lignes"
        echo "- Fichiers accents corriges : $NB_ACCENTS"
    } > "$RAPPORT_FILE"
    echo ""
    echo -e "${GREEN}Rapport sauvegarde : $RAPPORT_FILE${NC}"
fi
