#!/bin/bash
# verifier-systeme.sh
# Verifie le systeme de l'utilisateur et retourne les informations
# Version: 0.1.0-beta
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
VERSION="0.2.0"
DATE="2026-08-05"

# Couleurs pour la sortie
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'aide
aide() {
    echo "=========================================="
    echo "  verifier-systeme v${VERSION}"
    echo "  Verifie le systeme de l'utilisateur"
    echo "=========================================="
    echo ""
    echo "Usage: verifier-systeme [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --format FORMAT     Format de sortie: table, json, resume (defaut: table)"
    echo "  --detail DETAIL     Niveau de detail: standard, complet (defaut: standard)"
    echo "  --version           Afficher la version"
    echo ""
    echo "Exemples:"
    echo "  verifier-systeme"
    echo "  verifier-systeme --format json"
    echo "  verifier-systeme --format resume --detail complet"
    echo ""
}

# Fonction pour detecter l'OS
detecter_os() {
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "Windows"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Mac"
    else
        echo "Inconnu ($OSTYPE)"
    fi
}

# Fonction pour obtenir la version de Bash
version_bash() {
    bash --version 2>/dev/null | head -n1 | awk '{print $4}' || echo "Non disponible"
}

# Fonction pour verifier si un outil est disponible
verifier_outil() {
    local outil=$1
    if command -v "$outil" &> /dev/null; then
        local version=$($outil --version 2>/dev/null | head -n1 || echo "Version inconnue")
        echo "Oui|$version|$(command -v $outil)"
    else
        echo "Non|-|-"
    fi
}

# Fonction pour obtenir les informations systeme
informations_systeme() {
    local os=$(detecter_os)
    local arch=$(uname -m 2>/dev/null || echo "Inconnu")
    
    if [[ "$os" == "Windows" ]]; then
        local version_os=$(systeminfo 2>/dev/null | grep "OS Name" | cut -d: -f2 | xargs || echo "Inconnu")
        echo "$os|$version_os|$arch"
    else
        local version_os=$(uname -r 2>/dev/null || echo "Inconnu")
        echo "$os|$version_os|$arch"
    fi
}

# Fonction pour afficher en format table
afficher_table() {
    echo "| Categorie | Element | Disponible | Version | Chemin |"
    echo "|---|---|---|---|---|"
    
    # Systeme
    local sys_info=$(informations_systeme)
    IFS='|' read -r os version arch <<< "$sys_info"
    echo "| Systeme | OS | $os | $version | - |"
    echo "| Systeme | Architecture | $arch | - | - |"
    
    # Shells
    local bash_info=$(verifier_outil "bash")
    IFS='|' read -r bash_dispo bash_version bash_chemin <<< "$bash_info"
    echo "| Shell | Bash | $bash_dispo | $bash_version | $bash_chemin |"
    
    # Langages
    local python_info=$(verifier_outil "python3")
    IFS='|' read -r python_dispo python_version python_chemin <<< "$python_info"
    echo "| Langage | Python | $python_dispo | $python_version | $python_chemin |"
    
    local node_info=$(verifier_outil "node")
    IFS='|' read -r node_dispo node_version node_chemin <<< "$node_info"
    echo "| Langage | Node.js | $node_dispo | $node_version | $node_chemin |"
    
    # Outils
    local git_info=$(verifier_outil "git")
    IFS='|' read -r git_dispo git_version git_chemin <<< "$git_info"
    echo "| Outil | Git | $git_dispo | $git_version | $git_chemin |"
    
    local npm_info=$(verifier_outil "npm")
    IFS='|' read -r npm_dispo npm_version npm_chemin <<< "$npm_info"
    echo "| Outil | npm | $npm_dispo | $npm_version | $npm_chemin |"
}

# Fonction pour afficher en format JSON
afficher_json() {
    local sys_info=$(informations_systeme)
    IFS='|' read -r os version arch <<< "$sys_info"
    
    local bash_info=$(verifier_outil "bash")
    IFS='|' read -r bash_dispo bash_version bash_chemin <<< "$bash_info"
    
    local python_info=$(verifier_outil "python3")
    IFS='|' read -r python_dispo python_version python_chemin <<< "$python_info"
    
    local node_info=$(verifier_outil "node")
    IFS='|' read -r node_dispo node_version node_chemin <<< "$node_info"
    
    local git_info=$(verifier_outil "git")
    IFS='|' read -r git_dispo git_version git_chemin <<< "$git_info"
    
    local npm_info=$(verifier_outil "npm")
    IFS='|' read -r npm_dispo npm_version npm_chemin <<< "$npm_info"
    
    echo "{"
    echo "  \"systeme\": {"
    echo "    \"os\": \"$os\","
    echo "    \"version\": \"$version\","
    echo "    \"arch\": \"$arch\""
    echo "  },"
    echo "  \"shells\": ["
    echo "    {\"nom\": \"Bash\", \"disponible\": $([[ "$bash_dispo" == "Oui" ]] && echo "true" || echo "false"), \"version\": \"$bash_version\"}"
    echo "  ],"
    echo "  \"langages\": ["
    echo "    {\"nom\": \"Python\", \"disponible\": $([[ "$python_dispo" == "Oui" ]] && echo "true" || echo "false"), \"version\": \"$python_version\"},"
    echo "    {\"nom\": \"Node.js\", \"disponible\": $([[ "$node_dispo" == "Oui" ]] && echo "true" || echo "false"), \"version\": \"$node_version\"}"
    echo "  ],"
    echo "  \"outils\": ["
    echo "    {\"nom\": \"Git\", \"disponible\": $([[ "$git_dispo" == "Oui" ]] && echo "true" || echo "false"), \"version\": \"$git_version\"},"
    echo "    {\"nom\": \"npm\", \"disponible\": $([[ "$npm_dispo" == "Oui" ]] && echo "true" || echo "false"), \"version\": \"$npm_version\"}"
    echo "  ]"
    echo "}"
}

# Fonction pour afficher en format resume
afficher_resume() {
    local sys_info=$(informations_systeme)
    IFS='|' read -r os version arch <<< "$sys_info"
    
    local bash_info=$(verifier_outil "bash")
    IFS='|' read -r bash_dispo bash_version bash_chemin <<< "$bash_info"
    
    local python_info=$(verifier_outil "python3")
    IFS='|' read -r python_dispo python_version python_chemin <<< "$python_info"
    
    local node_info=$(verifier_outil "node")
    IFS='|' read -r node_dispo node_version node_chemin <<< "$node_info"
    
    local git_info=$(verifier_outil "git")
    IFS='|' read -r git_dispo git_version git_chemin <<< "$git_info"
    
    echo "**Systeme** : $os $version ($arch)"
    echo "**Shells** : Bash $bash_version"
    echo "**Langages** : $python_version, $node_version"
    echo "**Outils** : Git $git_version"
}

# Valeurs par defaut
FORMAT="table"
DETAIL="standard"

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --aide|-h)
            aide
            exit 0
            ;;
        --format)
            FORMAT="$2"
            shift 2
            ;;
        --detail)
            DETAIL="$2"
            shift 2
            ;;
        --version)
            echo "verifier-systeme v${VERSION}"
            exit 0
            ;;
        *)
            echo "Option inconnue: $1"
            echo "Utilisez --aide pour l'aide"
            exit 1
            ;;
    esac
done

# Verification du format
case $FORMAT in
    table|json|resume)
        ;;
    *)
        echo "Format inconnu: $FORMAT"
        echo "Formats disponibles: table, json, resume"
        exit 1
        ;;
esac

# Execution
case $FORMAT in
    table)
        afficher_table
        ;;
    json)
        afficher_json
        ;;
    resume)
        afficher_resume
        ;;
esac

exit 0
