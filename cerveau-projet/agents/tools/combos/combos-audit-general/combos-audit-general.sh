#!/bin/bash
# combos-audit-general.sh
# Combo audit-general : chainage des 4 evaluateurs + synthese
# Proprietaire : Themis (outil partage)
# Version : 0.2.0
#
# Ce combo execute les 4 evaluateurs en sequence et produit une synthese.
# Chaque evaluateur enrichit le contexte pour le suivant.

# identite:
#   type: combo
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== combos-audit-general v${VERSION} ==="
    echo ""
    echo "Usage: $0 [DOSSIER] [OPTIONS]"
    echo ""
    echo "Combo audit-general : chainage des 4 evaluateurs + synthese."
    echo ""
    echo "Options:"
    echo "  --rapport   Sauvegarder le rapport dans themis/rapports/"
    echo "  --help      Afficher cette aide"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVALUER_DIR="$SCRIPT_DIR/../../evaluer"
DOSSIER="${1:-.}"
SAUVEGARDER=false

# Parser les arguments
while [ $# -gt 0 ]; do
    case $1 in
        --rapport) SAUVEGARDER=true; shift ;;
        --help|-h) afficher_aide; exit 0 ;;
        *) DOSSIER="$1"; shift ;;
    esac
done

echo -e "${BLUE}=== combos-audit-general v${VERSION} ===${NC}"
echo "Cible : $DOSSIER"
echo "Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

if [ ! -d "$DOSSIER" ]; then
    echo -e "${RED}[ERREUR] Le dossier n'existe pas : $DOSSIER${NC}"
    exit 1
fi

# Collecter les resultats
RESULTATS=""
SCORES=""
ERREURS_TOTALES=0
AVERTISSEMENTS_TOTAUX=0

executer_evaluateur() {
    local nom="$1"
    local script="$2"

    echo -e "${BLUE}--- Etape : $nom ---${NC}"

    if [ ! -f "$script" ]; then
        echo -e "${RED}[ERREUR] Script introuvable : $script${NC}"
        RESULTATS="$RESULTATS\n## $nom\n\nERREUR : script introuvable\n"
        return 1
    fi

    chmod +x "$script" 2>/dev/null
    local resultat
    resultat=$(bash "$script" "$DOSSIER" 2>&1)
    local code=$?

    # Extraire le score
    local score=$(echo "$resultat" | sed -n 's/.*Score [a-z]* : \([0-9]*\).*/\1/p' | head -1)
    local erreurs=$(echo "$resultat" | grep -c '| ERREUR |' || true)
    local avertissements=$(echo "$resultat" | grep -c '| AVERTISSEMENT |' || true)

    RESULTATS="$RESULTATS\n## $nom\n\nScore : ${score:-?}/100\n\n$resultat\n"

    if [ -n "$score" ]; then
        SCORES="$SCORES\n|$nom|$score|"
    fi

    ERREURS_TOTALES=$((ERREURS_TOTALES + erreurs))
    AVERTISSEMENTS_TOTAUX=$((AVERTISSEMENTS_TOTAUX + avertissements))

    echo "$resultat" | grep -E '^(\| |## |Score)'
    echo ""

    return 0
}

# Executer les 4 evaluateurs en sequence
executer_evaluateur "evaluer-structure" "$EVALUER_DIR/evaluer-structure/evaluer-structure.sh"
executer_evaluateur "evaluer-conventions" "$EVALUER_DIR/evaluer-conventions/evaluer-conventions.sh"
executer_evaluateur "evaluer-coherence" "$EVALUER_DIR/evaluer-coherence/evaluer-coherence.sh"
executer_evaluateur "evaluer-agents" "$EVALUER_DIR/evaluer-agents/evaluer-agents.sh"

# Calculer le score global
SCORE_GLOBAL=0
NB_SCORES=0
for s in $(echo "$SCORES" | tr '|' '\n' | grep -E '^[0-9]+$'); do
    SCORE_GLOBAL=$((SCORE_GLOBAL + s))
    NB_SCORES=$((NB_SCORES + 1))
done
if [ "$NB_SCORES" -gt 0 ]; then
    SCORE_GLOBAL=$((SCORE_GLOBAL / NB_SCORES))
fi

# Determiner la severite
SEVERITE="INFORMATION"
if [ "$ERREURS_TOTALES" -gt 0 ]; then
    SEVERITE="CRITIQUE"
elif [ "$AVERTISSEMENTS_TOTAUX" -gt 2 ]; then
    SEVERITE="MAJEUR"
elif [ "$AVERTISSEMENTS_TOTAUX" -gt 0 ]; then
    SEVERITE="MINEUR"
fi

# Synthese
echo -e "${BLUE}=== SYNTHSE ===${NC}"
echo ""
echo "Score global : $SCORE_GLOBAL/100"
echo "Severite : $SEVERITE"
echo "Erreurs : $ERREURS_TOTALES"
echo "Avertissements : $AVERTISSEMENTS_TOTAUX"
echo ""
echo "Tableau des scores :"
echo "| Evaluateur | Score |"
echo "|---|---|"
echo -e "$SCORES" | grep -E '^\|' | while IFS='|' read -r _ nom score _; do
    [ -n "$nom" ] && echo "| $nom | $score/100 |"
done

# Sauvegarder si demande
if [ "$SAUVEGARDER" = true ]; then
    RAPPORT_DIR="$DOSSIER/cerveau-projet/agents/themis/rapports"
    DATE=$(date '+%Y-%m-%d-%H-%M')
    RAPPORT_FILE="$RAPPORT_DIR/audit-general-$DATE.md"

    mkdir -p "$RAPPORT_DIR"

    {
        echo "# Rapport d'evaluation -- $DATE"
        echo ""
        echo "## Contexte"
        echo "- Active par : Cerberus"
        echo "- Combo utilise : audit-general"
        echo "- Cible : $DOSSIER"
        echo ""
        echo "## Score global : $SCORE_GLOBAL/100"
        echo "- Severite : $SEVERITE"
        echo "- Erreurs : $ERREURS_TOTALES"
        echo "- Avertissements : $AVERTISSEMENTS_TOTAUX"
        echo ""
        echo -e "$RESULTATS"
    } > "$RAPPORT_FILE"

    echo ""
    echo -e "${GREEN}Rapport sauvegarde : $RAPPORT_FILE${NC}"
fi
