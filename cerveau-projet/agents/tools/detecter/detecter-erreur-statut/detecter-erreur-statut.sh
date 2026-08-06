#!/bin/bash
# detecter-erreur-statut.sh
# Detecte les fichiers dont le statut ne correspond pas a leur contenu
# Proprietaire : Vulcain (outil partage)
# Version : 0.2.0
# Statut : prepare

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VERSION="0.2.0"
STATUT_DOC="prepare"
VERBOSE=false
DOSSIER="."
STATUT="prepare"

# Fonction pour afficher l'aide
afficher_aide() {
    echo "Usage: $0 [dossier] [options]"
    echo ""
    echo "Detecte les fichiers dont le statut ne correspond pas a leur contenu."
    echo ""
    echo "Options:"
    echo "  --statut <statut>   Filtrer par statut (ebauche, prepare, dev, test, valide)"
    echo "  --verbose           Afficher les details"
    echo "  --aide              Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0                              # Verifier tous les fichiers"
    echo "  $0 --statut ebauche             # Verifier les fichiers ebauche"
    echo "  $0 cerveau-projet/              # Verifier dans un dossier specifique"
}

# Fonction pour extraire le statut d'un fichier
extraire_statut() {
    local fichier=$1
    local basename=$(basename "$fichier")
    
    # Chercher le statut dans le nom de fichier (avec ou sans accent)
    echo "$basename" | grep -oE '\.(ebauche|prepare|dev|test|valide)\.md$' | sed 's/\.md$//' | sed 's/^\.//'
}

# Fonction pour extraire le nom du fichier (sans le statut)
extraire_nom() {
    local fichier=$1
    local basename=$(basename "$fichier")
    echo "$basename" | sed 's/\.(ebauche|prepare|dev|test|valide)\.md$//'
}

# Fonction pour evaluer le niveau de maturite d'un contenu
evaluer_maturite() {
    local fichier=$1
    local maturite=0
    
    # 1. Nombre de lignes
    local lignes=$(wc -l < "$fichier")
    if [ "$lignes" -gt 50 ]; then
        maturite=$((maturite + 3))
    elif [ "$lignes" -gt 20 ]; then
        maturite=$((maturite + 2))
    elif [ "$lignes" -gt 10 ]; then
        maturite=$((maturite + 1))
    fi
    
    # 2. Presence de frontmatter
    if head -n 1 "$fichier" | grep -q "^---"; then
        maturite=$((maturite + 1))
    fi
    
    # 3. Nombre de sections
    local nb_sections=$(grep -c "^## " "$fichier" 2>/dev/null || echo 0)
    if [ "$nb_sections" -gt 5 ]; then
        maturite=$((maturite + 3))
    elif [ "$nb_sections" -gt 3 ]; then
        maturite=$((maturite + 2))
    elif [ "$nb_sections" -gt 1 ]; then
        maturite=$((maturite + 1))
    fi
    
    # 4. Presence de tableaux
    if grep -qE "^\|.*\|" "$fichier"; then
        maturite=$((maturite + 1))
    fi
    
    # 5. Presence de code
    if grep -qE '```' "$fichier"; then
        maturite=$((maturite + 1))
    fi
    
    # 6. Presence de listes
    if grep -qE "^- " "$fichier"; then
        maturite=$((maturite + 1))
    fi
    
    # 7. Liens internes
    local nb_liens=$(grep -oE '\[.*\]\(.*\)' "$fichier" | wc -l)
    if [ "$nb_liens" -gt 5 ]; then
        maturite=$((maturite + 2))
    elif [ "$nb_liens" -gt 2 ]; then
        maturite=$((maturite + 1))
    fi
    
    echo $maturite
}

# Fonction pour determiner le statut recommande selon la maturite
statut_recommande() {
    local maturite=$1
    
    if [ "$maturite" -ge 10 ]; then
        echo "valide"
    elif [ "$maturite" -ge 7 ]; then
        echo "test"
    elif [ "$maturite" -ge 5 ]; then
        echo "dev"
    elif [ "$maturite" -ge 3 ]; then
        echo "prepare"
    else
        echo "ebauche"
    fi
}

# Fonction pour convertir le statut en ordre numerique
statut_vers_ordre() {
    local statut=$1
    
    case "$statut" in
        "ebauche") echo 1 ;;
        "prepare") echo 2 ;;
        "dev") echo 3 ;;
        "test") echo 4 ;;
        "valide") echo 5 ;;
        *) echo 0 ;;
    esac
}

# Fonction pour analyser un fichier
analyser_fichier() {
    local fichier=$1
    local statut_actuel=$(extraire_statut "$fichier")
    local maturite=$(evaluer_maturite "$fichier")
    local statut_recom=$(statut_recommande "$maturite")
    local ordre_actuel=$(statut_vers_ordre "$statut_actuel")
    local ordre_recom=$(statut_vers_ordre "$statut_recom")
    
    # Determiner s'il y a une erreur
    local erreur="aucune"
    
    if [ "$ordre_recom" -gt "$ordre_actuel" ]; then
       erreur="sous-statut"
    elif [ "$ordre_recom" -lt "$ordre_actuel" ]; then
        erreur="sur-statut"
    fi
    
    # Afficher le resultat
    if [ "$erreur" != "aucune" ]; then
        echo -e "${RED}[ERREUR] $(basename "$fichier")${NC}"
        echo "   Statut actuel : $statut_actuel"
        echo "   Maturite : $maturite/15"
        echo "   Statut recommande : $statut_recom"
        
        if [ "$erreur" = "sous-statut" ]; then
            echo -e "   ${YELLOW}-> Devrait etre au statut '$statut_recom'${NC}"
        else
            echo -e "   ${YELLOW}-> Devrait etre au statut '$statut_recom'${NC}"
        fi
        echo ""
        
        return 1
    fi
    
    return 0
}

# Fonction principale
detecter_erreurs() {
    local dossier=$1
    local statut_filtre=$2
    local erreurs_totales=0
    local fichiers_analyses=0
    
    echo -e "${BLUE}=== Detection des erreurs de statut ===${NC}"
    echo "Dossier : $dossier"
    if [ -n "$statut_filtre" ]; then
        echo "Filtre : $statut_filtre"
    fi
    echo ""
    
    # Trouver tous les fichiers .md
    while IFS= read -r fichier; do
        local fstatut=$(extraire_statut "$fichier")
        
        # Verifier si le fichier a un statut
        if [ -z "$fstatut" ]; then
            continue
        fi
        
        # Appliquer le filtre si specifie
        if [ -n "$statut_filtre" ] && [ "$fstatut" != "$statut_filtre" ]; then
            continue
        fi
        
        fichiers_analyses=$((fichiers_analyses + 1))
        
        # Analyser le fichier
        analyser_fichier "$fichier"
        if [ $? -ne 0 ]; then
            erreurs_totales=$((erreurs_totales + 1))
        fi
    done < <(find "$dossier" -name "*.md" -type f 2>/dev/null)
    
    # Resumer
    echo -e "${BLUE}=== Resume ===${NC}"
    echo "Fichiers analyses : $fichiers_analyses"
    echo "Erreurs detectees : $erreurs_totales"
    
    if [ "$erreurs_totales" -eq 0 ]; then
        echo ""
        echo -e "${GREEN}[OK] Aucune erreur de statut detectee${NC}"
        exit 0
    else
        echo ""
        echo -e "${RED}[ERREUR] $erreurs_totales erreur(s) de statut detectee(s)${NC}"
        exit 1
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
            STATUT="prepare"
            shift 2
            ;;
        *)
            DOSSIER="$1"
            shift
            ;;
    esac
done

# Detecter les erreurs
detecter_erreurs "$DOSSIER" "$STATUT"
