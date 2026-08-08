#!/bin/bash
# rechercher-fichiers-vides.sh
# Outil pour rechercher les fichiers markdown vides ou quasi vides
# Version : 0.2.0

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
STATUT="ebauche"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== rechercher-fichiers-vides v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] [DOSSIER]"
    echo ""
    echo "Options :"
    echo "  --seuil <n>      Taille minimale pour considerer un fichier comme vide (defaut: 5 lignes)"
    echo "  --extensions     Extensions a chercher (defaut: md)"
    echo "  --exclure        Dossiers a exclure (defaut: .git,node_modules,.agents)"
    echo "  --verbose        Afficher les details"
    echo "  --help           Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0                                   # Rechercher dans le dossier courant"
    echo "  $0 cerveau-projet/                  # Rechercher dans cerveau-projet"
    echo "  $0 --seuil 10 cerveau-projet/       # Fichiers de moins de 10 lignes"
    echo "  $0 --extensions md,txt .            # Chercher .md et .txt"
    echo ""
}

# Fonction pour verifier si un fichier est vide ou quasi vide
est_fichier_vide() {
    local fichier="$1"
    local seuil="$2"
    
    # Compter les lignes non vides (ignorer les lignes vides et les commentaires frontmatter)
    local lignes_non_vides=$(grep -v '^\s*$' "$fichier" 2>/dev/null | grep -v '^---$' | wc -l)
    
    if [ "$lignes_non_vides" -lt "$seuil" ]; then
        return 0  # Fichier vide ou quasi vide
    fi
    return 1  # Fichier avec contenu
}

# Main
main() {
    local dossier="."
    local seuil=5
    local extensions="md"
    local exclude=".git,node_modules,.agents"
    local verbose="false"
    local help="false"
    
    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --seuil)
                seuil="$2"
                shift 2
                ;;
            --extensions)
                extensions="$2"
                shift 2
                ;;
            --exclure)
                exclude="$2"
                shift 2
                ;;
            --verbose)
                verbose="true"
                shift
                ;;
            --help)
                help="true"
                shift
                ;;
            *)
                dossier="$1"
                shift
                ;;
        esac
    done
    
    # Afficher l'aide
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    # Verifier que le dossier existe
    if [ ! -d "$dossier" ]; then
        echo -e "${RED}[ERREUR] Le dossier n'existe pas : $dossier${NC}"
        exit 1
    fi
    
    echo "=== Recherche de fichiers vides ==="
    echo "Dossier : ${dossier}"
    echo "Seuil : ${seuil} lignes non vides"
    echo "Extensions : ${extensions}"
    echo ""
    
    # Construire la commande find
    local cmd="find \"$dossier\" -type f"
    
    # Exclure les dossiers
    IFS=',' read -ra EXCLUDE_DIRS <<< "$exclude"
    for dir in "${EXCLUDE_DIRS[@]}"; do
        cmd="$cmd -not -path \"*/$dir/*\""
    done
    
    # Filtrer par extensions
    IFS=',' read -ra EXT_LIST <<< "$extensions"
    local first=true
    for ext in "${EXT_LIST[@]}"; do
        if [ "$first" = "true" ]; then
            cmd="$cmd \\( -name \"*.${ext}\""
            first=false
        else
            cmd="$cmd -o -name \"*.${ext}\""
        fi
    done
    cmd="$cmd \\)"
    
    # Variables pour le resume
    local total_fichiers=0
    local fichiers_vides=0
    local fichiers_ok=0
    
    # Traiter chaque fichier
    while IFS= read -r fichier; do
        if [ ! -f "$fichier" ]; then
            continue
        fi
        
        total_fichiers=$((total_fichiers + 1))
        
        if est_fichier_vide "$fichier" "$seuil"; then
            fichiers_vides=$((fichiers_vides + 1))
            local lignes=$(wc -l < "$fichier" 2>/dev/null)
            local lignes_non_vides=$(grep -v '^\s*$' "$fichier" 2>/dev/null | grep -v '^---$' | wc -l)
            echo -e "  ${RED}[VIDE]${NC} $fichier"
            if [ "$verbose" = "true" ]; then
                echo -e "        ${YELLOW}-> ${lignes} lignes au total, ${lignes_non_vides} non vides${NC}"
            fi
        else
            fichiers_ok=$((fichiers_ok + 1))
            if [ "$verbose" = "true" ]; then
                echo -e "  ${GREEN}[OK]${NC} $fichier"
            fi
        fi
    done < <(eval "$cmd")
    
    # Resume
    echo ""
    echo "=== Resume ==="
    echo "Fichiers trouves : ${total_fichiers}"
    echo -e "Fichiers vides ou quasi vides : ${RED}${fichiers_vides}${NC}"
    echo -e "Fichiers avec contenu : ${GREEN}${fichiers_ok}${NC}"
    
    # Code de sortie
    if [ "$fichiers_vides" -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}[ATTENTION] Des fichiers vides ont ete trouves${NC}"
        exit 1
    fi
    
    exit 0
}

# Executer
main "$@"
