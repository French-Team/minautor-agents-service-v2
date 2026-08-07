#!/bin/bash
# condenser-fichier.sh
# Outil pour condenser les fichiers markdown
# Proprietaire : Vulcain (outil partage)
VERSION="0.2.0"

# Configuration
VERBOSE=false
DRY_RUN=false
BACKUP=false
FICHIER=""

# Fonction pour afficher l'aide
afficher_aide() {
    echo "Usage: $0 <fichier> [options]"
    echo ""
    echo "Options:"
    echo "  --dry-run     Afficher les changements SANS les appliquer"
    echo "  --verbose     Afficher les details"
    echo "  --backup      Creer une copie de sauvegarde"
    echo "  --analyser    Analyser le fichier uniquement"
    echo "  --aide        Afficher cette aide"
}

# Fonction pour analyser un fichier
analyser_fichier() {
    local fichier=$1
    local nom=$(basename "$fichier")
    local lignes=$(wc -l < "$fichier")
    
    echo "=== Analyse de $nom ==="
    echo ""
    echo "Lignes totales : $lignes"
    
    # Analyser le frontmatter
    local fin_fm=$(grep -n "^---$" "$fichier" | tail -1 | cut -d: -f1)
    if [ -n "$fin_fm" ]; then
        echo "Frontmatter : $fin_fm lignes"
    fi
    
    # Analyser les sections
    local sections=$(grep -cE "^## [^#]" "$fichier")
    echo "Sections : $sections"
    
    # Analyser les tableaux
    local tableaux=$(grep -cE "^\|.*\|" "$fichier")
    echo "Lignes de tableaux : $tableaux"
    
    # Detecter les problemes
    echo ""
    echo "Problemes detectes :"
    
    if [ -n "$fin_fm" ] && [ $fin_fm -gt 30 ]; then
        echo "- Frontmatter trop long ($fin_fm lignes, max recommande: 30)"
    fi
    
    if [ $tableaux -gt 50 ]; then
        echo "- Trop de tableaux ($tableaux lignes)"
    fi
    
    if [ $lignes -gt 200 ]; then
        echo "- Fichier trop long ($lignes lignes, seuil: 200)"
    fi
}

# Fonction pour condenser un fichier
condenser_fichier() {
    local fichier=$1
    local backup="${fichier}.backup"
    local temp="${fichier}.tmp"
    
    if [ ! -f "$fichier" ]; then
        echo "ERREUR: Le fichier $fichier n'existe pas"
        exit 1
    fi
    
    # TOUJOURS creer une sauvegarde avant modification
    cp "$fichier" "$backup"
    
    if [ "$VERBOSE" = true ] || [ "$DRY_RUN" = true ]; then
        echo "=== Condensation de $(basename $fichier) ==="
        echo ""
    fi
    
    cp "$fichier" "$temp"
    
    local lignes_avant=$(wc -l < "$fichier")
    
    # 1. NE PAS supprimer les commentaires YAML - ils peuvent etre importants
    # Les commentaires sont conserves pour preserver le contenu
    
    # 2. NE PAS supprimer les commentaires dans le code - ils peuvent etre importants
    # Les commentaires sont conserves pour preserver le contenu
    
    # 3. NE PAS supprimer les separateurs - ils structurent le document
    # Les separateurs sont conserves pour preserver la structure
    
    local lignes_apres=$(wc -l < "$temp")
    local diff=$((lignes_avant - lignes_apres))
    
    echo ""
    echo "=== Resume ==="
    echo "Lignes avant : $lignes_avant"
    echo "Lignes apres : $lignes_apres"
    echo "Economie    : $diff lignes"
    
    if [ "$DRY_RUN" = true ]; then
        echo ""
        echo "[DRY-RUN] Aucun changement applique"
        rm "$temp"
    else
        mv "$temp" "$fichier"
        echo ""
        echo "[APPLIQUE] Fichier mis a jour"
    fi
}

# Parser les arguments
ANALYSER=false

while [ $# -gt 0 ]; do
    case $1 in
        "--aide"|"--help"|"-h")
            afficher_aide
            exit 0
            ;;
        "--dry-run")
            DRY_RUN=true
            shift
            ;;
        "--verbose")
            VERBOSE=true
            shift
            ;;
        "--backup")
            BACKUP=true
            shift
            ;;
        "--analyser")
            ANALYSER=true
            shift
            ;;
        *)
            FICHIER="$1"
            shift
            ;;
    esac
done

if [ -z "$FICHIER" ]; then
    echo "ERREUR: Fichier non specifie"
    afficher_aide
    exit 1
fi

if [ ! -f "$FICHIER" ]; then
    echo "ERREUR: Le fichier $FICHIER n'existe pas"
    exit 1
fi

if [ "$ANALYSER" = true ]; then
    analyser_fichier "$FICHIER"
else
    condenser_fichier "$FICHIER"
fi
