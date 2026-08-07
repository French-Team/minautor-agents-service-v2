#!/bin/bash
# lister-statuts.sh
# Outil pour lister les fichiers par statut
# Proprietaire : Vulcain
VERSION="0.2.0"

# Configuration
VERBOSE=false
STATUT=""
CHEMIN="."

# Fonction pour afficher l'aide
afficher_aide() {
    echo "Usage: $0 [chemin] [options]"
    echo ""
    echo "Options:"
    echo "  --statut <statut>   Filtrer par statut (ebauche, prepare, dev, test, valide)"
    echo "  --verbose           Afficher les details"
    echo "  --aide              Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0                              # Lister tous les fichiers avec statut"
    echo "  $0 --statut ebauche             # Lister les fichiers en ebauche"
    echo "  $0 cerveau-projet/agents        # Lister dans un dossier specifique"
    echo "  $0 --statut ebauche cerveau-projet/  # Lister les ebauche dans cerveau-projet"
}

# Fonction pour extraire le statut d'un fichier
extraire_statut() {
    local fichier=$1
    local basename=$(basename "$fichier")
    
    # Extraire le statut du nom de fichier
    # Format: [type]-[theme].[id].[class].[statut].md
    # NB: ASCII pur uniquement (prepare, jamais prepare) pour eviter les bugs d'encodage
    echo "$basename" | grep -oE '\.(ebauche|prepare|dev|test|valide)\.md$' | sed 's/\.md$//' | sed 's/^\.//'
}

# Fonction pour lister les fichiers par statut
lister_fichiers() {
    local chemin=$1
    local statut=$2
    
    if [ "$VERBOSE" = true ]; then
        echo "Recherche dans: $chemin"
        if [ -n "$statut" ]; then
            echo "Filtrage par statut: $statut"
        fi
        echo "---"
    fi
    
    # Trouver tous les fichiers .md
    local fichiers_trouves=0
    local fichiers_ebauche=0
    local fichiers_prepare=0
    local fichiers_dev=0
    local fichiers_test=0
    local fichiers_valide=0
    
    while IFS= read -r fichier; do
        local fstatut=$(extraire_statut "$fichier")
        
        if [ -n "$fstatut" ]; then
            fichiers_trouves=$((fichiers_trouves + 1))
            
            # Compter par statut
            case "$fstatut" in
                "ebauche") fichiers_ebauche=$((fichiers_ebauche + 1)) ;;
                "prepare") fichiers_prepare=$((fichiers_prepare + 1)) ;;
                "dev") fichiers_dev=$((fichiers_dev + 1)) ;;
                "test") fichiers_test=$((fichiers_test + 1)) ;;
                "valide") fichiers_valide=$((fichiers_valide + 1)) ;;
            esac
            
            # Afficher si pas de filtre ou si le statut correspond
            if [ -z "$statut" ] || [ "$fstatut" = "$statut" ]; then
                echo "$fichier | $fstatut"
            fi
        fi
    done < <(find "$chemin" -name "*.md" -type f 2>/dev/null)
    
    if [ "$VERBOSE" = true ]; then
        echo "---"
        echo "Resume:"
        echo "  Total fichiers avec statut: $fichiers_trouves"
        echo "  ebauche: $fichiers_ebauche"
        echo "  prepare: $fichiers_prepare"
        echo "  dev: $fichiers_dev"
        echo "  test: $fichiers_test"
        echo "  valide: $fichiers_valide"
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
        "--statut")
            STATUT="$2"
            shift 2
            ;;
        *)
            CHEMIN="$1"
            shift
            ;;
    esac
done

# Lister les fichiers
lister_fichiers "$CHEMIN" "$STATUT"
