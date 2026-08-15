#!/bin/bash
# combos-corriger-non-ascii.sh
# Combo corriger-non-ascii : detecte et corrige les accents et emojis
# Ressource partagee : utilise par Themis, Buffy, ou tout autre agent
# Version : 0.2.1
#
# Chainage :
#   1. rechercher-accents-sensibles -> detecter les problemes
#   2. corriger-emojis -> remplacer les emojis
#   3. corriger-accents-zones-sensibles -> remplacer les accents
#   4. rechercher-accents-sensibles -> verifier le nettoyage
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

VERSION="0.2.1"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR/../.."

CORRIGER_EMOJIS="$TOOLS_DIR/corriger/corriger-emojis/corriger-emojis.sh"
CORRIGER_ACCENTS="$TOOLS_DIR/corriger/corriger-accents-zones-sensibles/corriger-accents-zones-sensibles.sh"
RECHERCHER="$TOOLS_DIR/rechercher/rechercher-accents-sensibles/rechercher-accents-sensibles.sh"

afficher_aide() {
    echo "=== combos-corriger-non-ascii v${VERSION} ==="
    echo ""
    echo "Usage: $0 [DOSSIER] [OPTIONS]"
    echo ""
    echo "Combo : detecte et corrige les accents et emojis."
    echo "Ressource partagee pour tous les agents."
    echo ""
    echo "Options:"
    echo "  --dry-run     Afficher les changements sans les appliquer"
    echo "  --all         Corriger TOUS les accents (y compris texte francais et titres)"
    echo "  --rapport     Sauvegarder un rapport dans $TOOLS_DIR/../themis/rapports/"
    echo "  --help        Afficher cette aide"
}

DRY_RUN=false
SAUVEGARDER=false
ALL_MODE=false
DOSSIER=""

while [ $# -gt 0 ]; do
    case $1 in
        --dry-run) DRY_RUN=true; shift ;;
        --all) ALL_MODE=true; shift ;;
        --rapport) SAUVEGARDER=true; shift ;;
        --help|-h) afficher_aide; exit 0 ;;
        *) DOSSIER="$1"; shift ;;
    esac
done

# Defaut : repertoire courant
DOSSIER="${DOSSIER:-.}"
# Normaliser le chemin : supprimer le slash final
DOSSIER="${DOSSIER%/}"
# Si le chemin contient deja "cerveau-projet", l'utiliser tel quel ; sinon prefixer
if [[ "$DOSSIER" == *cerveau-projet* ]]; then
    CIBLE="$DOSSIER"
else
    CIBLE="$DOSSIER/cerveau-projet"
fi

# Mode (variable simple, evite les pieges d'echappement)
if [ "$DRY_RUN" = true ]; then
    MODE="DRY-RUN"
else
    MODE="APPLICATION"
fi

echo -e "${BLUE}=== combos-corriger-non-ascii v${VERSION} ===${NC}"
echo "Cible : $DOSSIER"
echo "Mode : $MODE"
echo "Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

if [ ! -d "$DOSSIER" ]; then
    echo -e "${RED}[ERREUR] Le dossier n'existe pas : $DOSSIER${NC}"
    exit 1
fi

# Etape 1 : Detection
echo -e "${BLUE}--- Etape 1/4 : Detection des problemes ---${NC}"
AVANT=$(bash "$RECHERCHER" "$DOSSIER" 2>&1 | grep -cE '^  \[[a-z]+\]' || true)
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

# Etape 3 : Correction des accents (mode dossier recursif, un seul appel)
echo -e "${BLUE}--- Etape 3/4 : Correction des accents ---${NC}"
ACCENTS_ARGS=""
if [ "$ALL_MODE" = true ]; then
    ACCENTS_ARGS="--all"
fi
if [ "$DRY_RUN" = true ]; then
    RESULTAT_ACCENTS=$(bash "$CORRIGER_ACCENTS" --recursive $ACCENTS_ARGS --dry-run "$CIBLE" 2>&1)
else
    RESULTAT_ACCENTS=$(bash "$CORRIGER_ACCENTS" --recursive $ACCENTS_ARGS "$CIBLE" 2>&1)
fi
# Parser le resume final de l'outil (lignes stables du rapport)
NB_ACCENTS=$(echo "$RESULTAT_ACCENTS" | tr -d '\r' | grep "^Fichiers analys" | grep -oE '[0-9]+' | head -1)
TOTAL_CORR=$(echo "$RESULTAT_ACCENTS" | tr -d '\r' | grep "^Corrections appliqu" | grep -oE '[0-9]+' | head -1)
TOTAL_CONS=$(echo "$RESULTAT_ACCENTS" | tr -d '\r' | grep "^Accents fran" | grep -oE '[0-9]+' | head -1)
echo "Fichiers analyses : ${NB_ACCENTS:-0}"
echo "Corrections zones sensibles : ${TOTAL_CORR:-0}"
echo "Accents francais conserves : ${TOTAL_CONS:-0}"
echo ""

# Etape 4 : Verification
echo -e "${BLUE}--- Etape 4/4 : Verification ---${NC}"
APRES=$(bash "$RECHERCHER" "$DOSSIER" 2>&1 | grep -cE '^  \[[a-z]+\]' || true)
echo "Lignes detectees apres correction : $APRES"

if [ "$APRES" -lt "$AVANT" ]; then
    echo -e "${GREEN}[OK] Reduction : $AVANT -> $APRES ($(( AVANT - APRES )) lignes corrigees)${NC}"
elif [ "$AVANT" -eq 0 ] && [ "$APRES" -eq 0 ]; then
    echo -e "${GREEN}[OK] Aucun probleme detecte${NC}"
else
    echo -e "${YELLOW}[ATTENTION] $APRES lignes restantes : relancez avec --all (regle immuable : aucun accent tolere)${NC}"
    echo -e "${YELLOW}Les seules exceptions admises : exemples/ et dictionnaires fonctionnels.${NC}"
fi

# Rapport
if [ "$SAUVEGARDER" = true ]; then
    RAPPORT_DIR="$CIBLE/agents/themis/rapports"
    DATE=$(date '+%Y-%m-%d-%H-%M')
    RAPPORT_FILE="$RAPPORT_DIR/corriger-non-ascii-$DATE.md"
    mkdir -p "$RAPPORT_DIR"

    {
        echo "# Rapport corriger-non-ascii -- $DATE"
        echo ""
        echo "## Contexte"
        echo "- Cible : $DOSSIER"
        echo "- Mode : $MODE"
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
