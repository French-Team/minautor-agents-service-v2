#!/bin/bash
# corriger-emojis.sh
# Detecte et remplace les emojis par des symboles ASCII
# Proprietaire : Vulcain (outil partage)

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VERBOSE=false
DRY_RUN=false
DOSSIER="."
FICHIER=""

# Chemin vers le dictionnaire
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DICTIONNAIRE="$SCRIPT_DIR/dictionnaire-emojis.txt"

# Fonction pour afficher l'aide
afficher_aide() {
    echo "Usage: $0 <fichier|dossier> [options]"
    echo ""
    echo "Detecte et remplace les emojis par des symboles ASCII."
    echo ""
    echo "Options:"
    echo "  --dry-run     Afficher les changements sans les appliquer"
    echo "  --verbose     Afficher les details"
    echo "  --aide        Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 fichier.md"
    echo "  $0 --dry-run fichier.md"
    echo "  $0 cerveau-projet/"
    echo "  $0 --dry-run cerveau-projet/"
}

# Fonction pour detecter les emojis dans un fichier
detecter_emojis() {
    local fichier=$1
    
    if [ ! -f "$fichier" ]; then
        return 1
    fi
    
    # Lire le dictionnaire et detecter chaque emoji
    if [ -f "$DICTIONNAIRE" ]; then
        while IFS='|' read -r emoji remplacement; do
            # Ignorer les commentaires et les lignes vides
            [[ "$emoji" =~ ^#.*$ ]] && continue
            [[ -z "$emoji" ]] && continue
            
            # Chercher l'emoji dans le fichier
            local lignes=$(grep -n "$emoji" "$fichier" 2>/dev/null)
            if [ -n "$lignes" ]; then
                echo "$lignes"
            fi
        done < "$DICTIONNAIRE"
    fi
    
    return 0
}

# Fonction pour remplacer les emojis dans un fichier
remplacer_emojis() {
    local fichier=$1
    local dry_run=$2
    
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve : $fichier${NC}"
        return 1
    fi
    
    # Detecter les emojis
    local emojis_trouves=$(detecter_emojis "$fichier")
    
    if [ -z "$emojis_trouves" ]; then
        if [ "$VERBOSE" = true ]; then
            echo -e "${GREEN}[OK] $fichier - aucun emoji detecte${NC}"
        fi
        return 0
    fi
    
    echo -e "${YELLOW}[ATTENTION] $fichier - emojis detects :${NC}"
    echo "$emojis_trouves" | head -10
    
    if [ "$dry_run" = true ]; then
        echo -e "${YELLOW}[DRY-RUN] Changements non appliques${NC}"
        return 0
    fi
    
    # Creer une copie de sauvegarde
    cp "$fichier" "${fichier}.bak"
    
    # Remplacer les emojis en utilisant le dictionnaire
    if [ -f "$DICTIONNAIRE" ]; then
        while IFS='|' read -r emoji remplacement; do
            # Ignorer les commentaires et les lignes vides
            [[ "$emoji" =~ ^#.*$ ]] && continue
            [[ -z "$emoji" ]] && continue
            
            # Remplacer l'emoji par le texte de remplacement
            sed -i "s|$emoji|$remplacement|g" "$fichier" 2>/dev/null
        done < "$DICTIONNAIRE"
    fi
    
    # Verifier si des emojis restent
    local emojis_restants=$(detecter_emojis "$fichier")
    if [ -n "$emojis_restants" ]; then
        echo -e "${YELLOW}[ATTENTION] Certains emojis n'ont pas ete remplaces :${NC}"
        echo "$emojis_restants" | head -3
    else
        echo -e "${GREEN}[OK] $fichier - tous les emojis ont ete remplaces${NC}"
    fi
    
    return 0
}

# Fonction principale
corriger_emojis() {
    local cible=$1
    local dry_run=$2
    
    echo -e "${BLUE}=== Correction des emojis ===${NC}"
    echo "Cible : $cible"
    echo "Dictionnaire : $DICTIONNAIRE"
    echo ""
    
    # Verifier que le dictionnaire existe
    if [ ! -f "$DICTIONNAIRE" ]; then
        echo -e "${RED}[ERREUR] Dictionnaire non trouve : $DICTIONNAIRE${NC}"
        exit 1
    fi
    
    if [ -f "$cible" ]; then
        # C'est un fichier
        remplacer_emojis "$cible" "$dry_run"
    elif [ -d "$cible" ]; then
        # C'est un dossier
        local fichiers_modifies=0
        local fichiers_errores=0
        
        while IFS= read -r fichier; do
            remplacer_emojis "$fichier" "$dry_run"
            if [ $? -eq 0 ]; then
                fichiers_modifies=$((fichiers_modifies + 1))
            else
                fichiers_errores=$((fichiers_errores + 1))
            fi
        done < <(find "$cible" -name "*.md" -name "*.sh" -type f 2>/dev/null)
        
        echo ""
        echo -e "${BLUE}=== Resumer ===${NC}"
        echo "Fichiers analyses : $fichiers_modifies"
        echo "Erreurs : $fichiers_errores"
    else
        echo -e "${RED}[ERREUR] Cible non trouvee : $cible${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${GREEN}=== Termine ===${NC}"
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
        "--dry-run")
            DRY_RUN=true
            shift
            ;;
        *)
            if [ -z "$FICHIER" ]; then
                FICHIER="$1"
            fi
            shift
            ;;
    esac
done

# Verifier les arguments
if [ -z "$FICHIER" ]; then
    echo -e "${RED}[ERREUR] Aucune cible specifiee${NC}"
    afficher_aide
    exit 1
fi

# Corriger les emojis
corriger_emojis "$FICHIER" "$DRY_RUN"
