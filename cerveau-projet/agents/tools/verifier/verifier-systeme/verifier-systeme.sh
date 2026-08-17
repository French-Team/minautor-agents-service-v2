#!/bin/bash
# verifier-systeme.sh
# Verifie le systeme de l'utilisateur et retourne les informations
# Version: 0.1.0-beta
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.3"
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
    echo "  --enregistrer       Ecrire le profil systeme dans le classeur-variables"
    echo "  --version           Afficher la version"
    echo ""
    echo "Exemples:"
    echo "  verifier-systeme"
    echo "  verifier-systeme --format json"
    echo "  verifier-systeme --format resume --detail complet"
    echo "  verifier-systeme --enregistrer"
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

# Fonction pour enregistrer le profil dans le classeur-variables
enregistrer_profil() {
    local classeur_stockage="cerveau-projet/agents/classeur-variables/stockage/variables-actuelles.md"
    local classeur_hist="cerveau-projet/agents/classeur-variables/historique/historique-modifications.md"

    if [ ! -f "$classeur_stockage" ]; then
        echo "ERREUR: classeur introuvable: $classeur_stockage"
        return 1
    fi

    local date_jour=$(date +%F)

    # Collecter les informations systeme
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

    # Versions courtes (premier numero de version)
    local bash_short=$(echo "$bash_version" | grep -oE '[0-9]+(\.[0-9]+)+' | head -1)
    [ -z "$bash_short" ] && bash_short="-"
    local python_short=$(echo "$python_version" | grep -oE '[0-9]+(\.[0-9]+)+' | head -1)
    [ -z "$python_short" ] && python_short="-"
    local node_short=$(echo "$node_version" | grep -oE '[0-9]+(\.[0-9]+)+' | head -1)
    [ -z "$node_short" ] && node_short="-"
    local git_short=$(echo "$git_version" | grep -oE '[0-9]+(\.[0-9]+)+' | head -1)
    [ -z "$git_short" ] && git_short="-"

    local nouvelle_valeur="OS: $os / Bash: $bash_short / Python: $python_short / Git: $git_short / Node: $node_short"
    local nouvelle_ligne=$(printf '| `profil-systeme` | %s | verifier-systeme | %s | [OK] |' "$nouvelle_valeur" "$date_jour")

    # Ancienne valeur pour l'historique
    local ancienne_valeur="(aucune)"
    while IFS= read -r ligne || [ -n "$ligne" ]; do
        case "$ligne" in
            *"profil-systeme"*)
                ancienne_valeur=$(echo "$ligne" | sed 's/.*| `profil-systeme` | //; s/ | verifier-systeme.*//')
                ;;
        esac
    done < "$classeur_stockage"

    # Detecter si la ligne profil-systeme existe deja
    local existe_profil=0
    while IFS= read -r ligne || [ -n "$ligne" ]; do
        case "$ligne" in
            *"profil-systeme"*) existe_profil=1 ;;
        esac
    done < "$classeur_stockage"

    # Mise a jour du tableau (remplacer si existe, sinon ajouter apres fichier-final)
    local tmp=$(mktemp)
    if [ "$existe_profil" -eq 1 ]; then
        local fait=0
        while IFS= read -r ligne || [ -n "$ligne" ]; do
            case "$ligne" in
                *"profil-systeme"*)
                    if [ "$fait" -eq 0 ]; then
                        echo "$nouvelle_ligne"
                        fait=1
                    fi
                    ;;
                *) echo "$ligne" ;;
            esac
        done < "$classeur_stockage" > "$tmp"
    else
        local insere=0
        while IFS= read -r ligne || [ -n "$ligne" ]; do
            echo "$ligne"
            if [ "$insere" -eq 0 ] && echo "$ligne" | grep -q "fichier-final"; then
                echo "$nouvelle_ligne"
                insere=1
            fi
        done < "$classeur_stockage" > "$tmp"
    fi
    mv "$tmp" "$classeur_stockage"

    # Ajout de l'entree dans l'historique (apres '## Entrees recentes')
    if [ -f "$classeur_hist" ]; then
        local tmp_hist=$(mktemp)
        local insere_hist=0
        while IFS= read -r ligne || [ -n "$ligne" ]; do
            echo "$ligne"
            if [ "$insere_hist" -eq 0 ] && echo "$ligne" | grep -q "## Entrees recentes"; then
                echo "## $date_jour -- Ecriture"
                echo ""
                echo "- **Variable** : profil-systeme"
                echo "- **Ancienne valeur** : $ancienne_valeur"
                echo "- **Nouvelle valeur** : $nouvelle_valeur"
                echo "- **Source** : verifier-systeme"
                echo "- **Raison** : Mise a jour du profil systeme utilisateur"
                echo ""
                insere_hist=1
            fi
        done < "$classeur_hist" > "$tmp_hist"
        mv "$tmp_hist" "$classeur_hist"
    fi

    echo "[OK] Profil systeme enregistre dans le classeur-variables"
    echo "Variable : profil-systeme"
    echo "Valeur   : $nouvelle_valeur"
    echo "Source   : verifier-systeme"
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
ENREGISTRER="non"

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
        --enregistrer)
            ENREGISTRER="oui"
            shift
            ;;
        --version)
            echo "verifier-systeme v${VERSION}"
            exit 0
            ;;
        --bloc-fiche)
            # Delegue au .py : le bloc Environnement de travail est genere
            # par le moteur Python (parite garantie avec le .py)
            exec python3 "$(dirname "${BASH_SOURCE[0]}")/verifier-systeme.py" --bloc-fiche "$2"
            ;;
        *)
            echo "Option inconnue: $1"
            echo "Utilisez --aide pour l'aide"
            exit 1
            ;;
    esac
done

# Si --enregistrer est demande, on enregistre et on termine
if [ "$ENREGISTRER" = "oui" ]; then
    enregistrer_profil
    exit 0
fi

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
