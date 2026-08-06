#!/bin/bash
# rechercher-templates.sh
# Outil pour rechercher les fichiers template dans le projet
# Version : 0.1.0-beta
# Statut : ebauche

# Configuration
VERSION="0.1.0-beta"
STATUT="ebauche"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== rechercher-templates v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] [DOSSIER]"
    echo ""
    echo "Options :"
    echo "  --mode nom          Rechercher par nom (contient 'template') - defaut"
    echo "  --mode frontmatter  Rechercher les fichiers avec un frontmatter de template"
    echo "  --mode contenu      Rechercher les fichiers contenant 'template' dans le contenu"
    echo "  --tous              Combiner tous les modes"
    echo "  --extensions        Extensions a chercher (defaut: md)"
    echo "  --exclure           Dossiers a exclure (defaut: .git,node_modules,.agents)"
    echo "  --verbose           Afficher les details"
    echo "  --help              Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0                                    # Rechercher par nom dans le dossier courant"
    echo "  $0 cerveau-projet/                   # Rechercher dans cerveau-projet"
    echo "  $0 --tous cerveau-projet/            # Tous les modes combines"
    echo "  $0 --mode contenu cerveau-projet/    # Rechercher dans le contenu"
    echo ""
}

# Vérifier si un fichier est un template (par nom)
est_template_nom() {
    local fichier="$1"
    local nom_base=$(basename "$fichier" | tr '[:upper:]' '[:lower:]')
    case "$nom_base" in
        *template*) return 0 ;;
        *) return 1 ;;
    esac
}

# Vérifier si un fichier a un frontmatter de template
est_template_frontmatter() {
    local fichier="$1"
    local premiere_ligne=$(head -n 1 "$fichier" 2>/dev/null)
    if [ "$premiere_ligne" = "---" ]; then
        # Chercher des marqueurs de template dans le frontmatter
        if head -n 15 "$fichier" 2>/dev/null | grep -qiE 'template|modele|placeholder|\[.*\]'; then
            return 0
        fi
    fi
    return 1
}

# Vérifier si un fichier mentionne 'template' dans son contenu
est_template_contenu() {
    local fichier="$1"
    if grep -qiE 'template|modele|placeholder' "$fichier" 2>/dev/null; then
        return 0
    fi
    return 1
}

# Main
main() {
    local dossier="."
    local extensions="md"
    local exclude=".git,node_modules,.agents"
    local verbose="false"
    local help="false"
    local mode="nom"
    local tous="false"
    
    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --mode)
                mode="$2"
                shift 2
                ;;
            --tous)
                tous="true"
                shift
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
    
    echo "=== Recherche de templates ==="
    echo "Dossier : ${dossier}"
    if [ "$tous" = "true" ]; then
        echo "Mode : tous (nom + frontmatter + contenu)"
    else
        echo "Mode : ${mode}"
    fi
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
    local templates_trouves=0
    local fichiers_ok=0
    
    # Traiter chaque fichier
    while IFS= read -r fichier; do
        if [ ! -f "$fichier" ]; then
            continue
        fi
        
        total_fichiers=$((total_fichiers + 1))
        local est_template="false"
        local raisons=""
        
        # Mode nom (par defaut)
        if [ "$mode" = "nom" ] || [ "$tous" = "true" ]; then
            if est_template_nom "$fichier"; then
                est_template="true"
                raisons="${raisons}nom"
            fi
        fi
        
        # Mode frontmatter
        if [ "$mode" = "frontmatter" ] || [ "$tous" = "true" ]; then
            if [ "$est_template" = "false" ] && est_template_frontmatter "$fichier"; then
                est_template="true"
                raisons="${raisons}${raisons:+|}frontmatter"
            fi
        fi
        
        # Mode contenu
        if [ "$mode" = "contenu" ] || [ "$tous" = "true" ]; then
            if [ "$est_template" = "false" ] && est_template_contenu "$fichier"; then
                est_template="true"
                raisons="${raisons}${raisons:+|}contenu"
            fi
        fi
        
        if [ "$est_template" = "true" ]; then
            templates_trouves=$((templates_trouves + 1))
            echo -e "  ${GREEN}[TEMPLATE]${NC} $fichier"
            if [ "$verbose" = "true" ]; then
                echo -e "        ${YELLOW}-> detecte par : ${raisons}${NC}"
            fi
        else
            fichiers_ok=$((fichiers_ok + 1))
        fi
    done < <(eval "$cmd")
    
    # Resume
    echo ""
    echo "=== Resume ==="
    echo "Fichiers trouves : ${total_fichiers}"
    echo -e "Templates detectes : ${GREEN}${templates_trouves}${NC}"
    echo -e "Fichiers non-templates : ${fichiers_ok}"
    
    # Code de sortie
    if [ "$templates_trouves" -eq 0 ]; then
        echo ""
        echo -e "${YELLOW}[ATTENTION] Aucun template trouve${NC}"
        exit 1
    fi
    
    exit 0
}

# Executer
main "$@"
