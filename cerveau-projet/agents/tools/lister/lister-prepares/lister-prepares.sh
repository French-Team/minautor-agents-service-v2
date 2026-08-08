#!/bin/bash
# lister-prepares.sh
# Liste les fichiers 'prepare' et verifie l'existence des specs
# Proprietaire : Vulcain (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VERBOSE=false
DOSSIER="."
CREER_SPEC=false

# Fonction pour afficher l'aide
afficher_aide() {
    echo "Usage: $0 [DOSSIER] [OPTIONS]"
    echo ""
    echo "Liste les fichiers 'prepare' et verifie l'existence des specs."
    echo ""
    echo "Options:"
    echo "  --creer-spec   Proposer de creer les specs manquantes"
    echo "  --verbose      Afficher les details"
    echo "  --aide         Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0                              # Lister tous les fichiers 'prepare'"
    echo "  $0 cerveau-projet/              # Lister dans un dossier"
    echo "  $0 --creer-spec                 # Proposer de creer les specs"
}

# Fonction pour extraire le nom du fichier (sans le statut)
extraire_nom() {
    local fichier=$1
    local basename=$(basename "$fichier" .md)
    echo "$basename" | sed 's/\.(ebauche|prepare|dev|test|valide)$//'
}

# Fonction pour extraire le statut
extraire_statut() {
    local fichier=$1
    local basename=$(basename "$fichier")
    echo "$basename" | grep -oE '\.(ebauche|prepare|dev|test|valide)\.md$' | sed 's/\.md$//' | sed 's/^\.//'
}

# Fonction pour verifier si une spec existe pour un fichier
verifier_spec() {
    local fichier=$1
    local nom=$(extraire_nom "$fichier")
    local dossier=$(dirname "$fichier")
    
    # Chercher une spec dans le dossier spec/ parent
    local dossier_spec=""
    
    # Remonter les dossiers pour trouver spec/
    local current="$dossier"
    while [ "$current" != "." ] && [ "$current" != "/" ]; do
        if [ -d "$current/spec" ]; then
            dossier_spec="$current/spec"
            break
        fi
        current=$(dirname "$current")
    done
    
    if [ -n "$dossier_spec" ]; then
        # Chercher une spec avec le meme nom
        local spec_trouvee=$(find "$dossier_spec" -name "spec-${nom}*.md" -type f 2>/dev/null | head -1)
        if [ -n "$spec_trouvee" ]; then
            echo "OUI|$spec_trouvee"
            return 0
        fi
    fi
    
    # Chercher une spec dans le meme dossier
    local spec_locale=$(find "$dossier" -name "spec-${nom}*.md" -type f 2>/dev/null | head -1)
    if [ -n "$spec_locale" ]; then
        echo "OUI|$spec_locale"
        return 0
    fi
    
    echo "NON|"
    return 1
}

# Fonction pour lister les fichiers 'prepare'
lister_prepares() {
    local dossier=$1
    local creer_spec=$2
    
    echo -e "${BLUE}=== Fichiers 'prepare' ===${NC}"
    echo "Dossier : $dossier"
    echo ""
    
    local fichiers_trouves=0
    local specs_manquantes=0
    
    while IFS= read -r fichier; do
        local statut=$(extraire_statut "$fichier")
        
        # Verifier que c'est bien un 'prepare'
        if [ "$statut" != "prepare" ]; then
            continue
        fi
        
        fichiers_trouves=$((fichiers_trouves + 1))
        
        # Verifier si une spec existe
        local spec_result=$(verifier_spec "$fichier")
        local spec_existe=$(echo "$spec_result" | cut -d'|' -f1)
        local spec_chemin=$(echo "$spec_result" | cut -d'|' -f2)
        
        if [ "$spec_existe" = "OUI" ]; then
            echo -e "${GREEN}[OK]$(basename "$fichier")${NC}"
            if [ "$VERBOSE" = true ]; then
                echo "     Spec : $spec_chemin"
            fi
        else
            echo -e "${YELLOW}[SANS SPEC]$(basename "$fichier")${NC}"
            specs_manquantes=$((specs_manquantes + 1))
            
            if [ "$creer_spec" = true ]; then
                echo -e "     ${BLUE}-> Proposer de creer une spec${NC}"
            fi
        fi
    done < <(find "$dossier" -name "*.prepare.md" -type f 2>/dev/null)
    
    echo ""
    echo -e "${BLUE}=== Resumer ===${NC}"
    echo "Fichiers 'prepare' trouves : $fichiers_trouves"
    echo "Specs manquantes : $specs_manquantes"
    
    if [ "$specs_manquantes" -gt 0 ] && [ "$creer_spec" = true ]; then
        echo ""
        echo -e "${YELLOW}Des specs sont a creer pour les fichiers 'prepare'.${NC}"
        echo "Utiliser le template : cerveau-projet/pense-betes/specs/spec-template.md"
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
        "--creer-spec")
            CREER_SPEC=true
            shift
            ;;
        *)
            DOSSIER="$1"
            shift
            ;;
    esac
done

# Lister les fichiers 'prepare'
lister_prepares "$DOSSIER" "$CREER_SPEC"
