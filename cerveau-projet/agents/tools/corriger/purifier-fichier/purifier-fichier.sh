#!/bin/bash
# purifier-fichier.sh
# Outil pour purifier un fichier markdown
# Propriétaire : Vulcain (outil partagé)

# Configuration
VERBOSE=false
DRY_RUN=false
BACKUP=false
FICHIER=""
LIGNES_SUPPRIMEES=0

# Fonction pour afficher l'aide
afficher_aide() {
    echo "Usage: $0 <fichier> [options]"
    echo ""
    echo "Options:"
    echo "  --dry-run     Afficher les changements SANS les appliquer"
    echo "  --verbose     Afficher les détails"
    echo "  --backup      Créer une copie de sauvegarde"
    echo "  --aide        Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 --dry-run cerveau-projet/agents/buffy/buffy.md"
    echo "  $0 --verbose cerveau-projet/agents/buffy/buffy.md"
    echo "  $0 cerveau-projet/agents/buffy/buffy.md"
}

# Fonction pour afficher un changement
afficher_changement() {
    local type=$1
    local description=$2
    local lignes=$3
    
    if [ "$VERBOSE" = true ] || [ "$DRY_RUN" = true ]; then
        echo "[$type] $description ($lignes lignes)"
    fi
}

# Fonction pour purifier un fichier
purifier_fichier() {
    local fichier=$1
    local backup="${fichier}.backup"
    local temp="${fichier}.tmp"
    
    if [ ! -f "$fichier" ]; then
        echo "ERREUR: Le fichier $fichier n'existe pas"
        exit 1
    fi
    
    LIGNES_SUPPRIMEES=0
    
    # TOUJOURS créer une sauvegarde avant modification
    cp "$fichier" "$backup"
    
    if [ "$VERBOSE" = true ]; then
        echo "=== Purification de $(basename $fichier) ==="
        echo ""
    fi
    
    cp "$fichier" "$temp"
    
    # 1. NE PAS supprimer les blockquotes - ils contiennent souvent des règles importantes
    # Les blockquotes sont conservés par défaut pour préserver le contenu
    
    # 2. Supprimer les lignes vides consécutives
    avant=$(wc -l < "$temp")
    sed -i '/^$/N;/^\n$/d' "$temp"
    apres=$(wc -l < "$temp")
    diff=$((avant - apres))
    if [ $diff -gt 0 ]; then
        LIGNES_SUPPRIMEES=$((LIGNES_SUPPRIMEES + diff))
        afficher_changement "SUPPRIMÉ" "Lignes vides consécutives" "$diff"
    fi
    
    # 3. Supprimer les notes de rappel
    avant=$(wc -l < "$temp")
    sed -i '/^> Note:/d' "$temp"
    sed -i '/^> Important:/d' "$temp"
    sed -i '/^> Rappel:/d' "$temp"
    apres=$(wc -l < "$temp")
    diff=$((avant - apres))
    if [ $diff -gt 0 ]; then
        LIGNES_SUPPRIMEES=$((LIGNES_SUPPRIMEES + diff))
        afficher_changement "SUPPRIMÉ" "Notes de rappel" "$diff"
    fi
    
    # 4. Supprimer les commentaires YAML inutiles
    avant=$(wc -l < "$temp")
    sed -i '/^# Type:/d' "$temp"
    sed -i '/^# Convention:/d' "$temp"
    sed -i '/^# Comment devenir/d' "$temp"
    apres=$(wc -l < "$temp")
    diff=$((avant - apres))
    if [ $diff -gt 0 ]; then
        LIGNES_SUPPRIMEES=$((LIGNES_SUPPRIMEES + diff))
        afficher_changement "SUPPRIMÉ" "Commentaires YAML inutiles" "$diff"
    fi
    
    # 5. Condenser le frontmatter YAML (garder l'essentiel)
    avant=$(wc -l < "$temp")
    # NE PAS supprimer les commentaires YAML - ils peuvent être importants
    # Seulement supprimer les commentaires vides ou purement décoratifs
    # sed -i '/^---$/,/^---$/{
    #     /^#/d
    #     /^  #/d
    # }' "$temp"
    apres=$(wc -l < "$temp")
    diff=$((avant - apres))
    if [ $diff -gt 0 ]; then
        LIGNES_SUPPRIMEES=$((LIGNES_SUPPRIMEES + diff))
        afficher_changement "CONDENSÉ" "Commentaires YAML" "$diff"
    fi
    
    # 6. Réduire les blocs de code vides ou simples
    avant=$(wc -l < "$temp")
    # Supprimer les blocs de code avec juste un commentaire
    sed -i '/^```$/,/^```$/{
        /^```$/d
        /^#.*$/d
    }' "$temp"
    apres=$(wc -l < "$temp")
    diff=$((avant - apres))
    if [ $diff -gt 0 ]; then
        LIGNES_SUPPRIMEES=$((LIGNES_SUPPRIMEES + diff))
        afficher_changement "RÉDUIT" "Blocs de code vides" "$diff"
    fi
    
    # 7. NE PAS supprimer les séparateurs - ils structurent le document
    # Les séparateurs sont conservés pour préserver la structure
    
    # Résumé
    local lignes_avant=$(wc -l < "$fichier")
    local lignes_apres=$(wc -l < "$temp")
    local total_supprime=$((lignes_avant - lignes_apres))
    
    echo ""
    echo "=== Résumé ==="
    echo "Lignes avant  : $lignes_avant"
    echo "Lignes après  : $lignes_apres"
    echo "Supprimées   : $total_supprime"
    
    if [ "$DRY_RUN" = true ]; then
        echo ""
        echo "[DRY-RUN] Aucun changement appliqué"
        rm "$temp"
    else
        mv "$temp" "$fichier"
        echo ""
        echo "[APPLIQUÉ] Fichier mis à jour"
    fi
}

# Parser les arguments
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
        *)
            FICHIER="$1"
            shift
            ;;
    esac
done

if [ -z "$FICHIER" ]; then
    echo "ERREUR: Fichier non spécifié"
    afficher_aide
    exit 1
fi

purifier_fichier "$FICHIER"
