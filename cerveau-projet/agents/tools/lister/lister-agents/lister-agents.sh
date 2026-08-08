#!/bin/bash
# lister-agents.sh
# Lister les agents avec leurs informations
# Version: 0.4.0
# Date: 2026-08-08
# Auteur: Vulcain
# Convention identification v0.3.0 : champs YAML role-agent / statut-<agent>
# (anciens noms role: / statut: acceptes en repli pendant la transition)
# v0.4.0 : option --tag (convention-tags, cle tags: dans identite)

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.4.0"
DATE="2026-08-08"
AGENTS_DIR="cerveau-projet/agents"

# Couleurs pour la sortie
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction d'aide
aide() {
    echo "=========================================="
    echo "  lister-agents v${VERSION}"
    echo "  Lister les agents avec leurs informations"
    echo "=========================================="
    echo ""
    echo "Usage: lister-agents [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les details"
    echo "  --version           Afficher la version"
    echo "  --detail, -d        Afficher les details complets"
    echo "  --tag TAG           Filtrer par tag (convention-tags)"
    echo ""
    echo "Exemples:"
    echo "  lister-agents"
    echo "  lister-agents --detail"
    echo "  lister-agents --tag coordination"
    echo ""
}

# Lire les tags d'une fiche agent (frontmatter identite)
# Arg1: fichier -> stdout: liste des tags separes par des espaces
lire_tags() {
    local fichier=$1
    [[ -f "$fichier" ]] || return 0
    local dans_identite=0
    while IFS= read -r ligne; do
        if [[ "$ligne" == *"identite:"* ]]; then
            dans_identite=1
            continue
        fi
        if [[ $dans_identite -eq 1 ]]; then
            if [[ "$ligne" =~ ^[[:space:]]*tags:[[:space:]]*(.*)$ ]]; then
                echo "${BASH_REMATCH[1]}"
                return 0
            fi
        fi
    done < "$fichier"
    return 0
}

# Fonction pour lister les agents
lister_agents() {
    local verbose=$1
    local detail=$2
    local tag=$3

    echo -e "${BLUE}[LISTE] Liste des agents du cerveau-projet${NC}"
    if [[ -n "$tag" ]]; then
        echo -e "${YELLOW}[FILTRE] Tag : ${tag}${NC}"
    fi
    echo ""

    # Verifier si le dossier agents existe
    if [[ ! -d "$AGENTS_DIR" ]]; then
        echo -e "${RED}Erreur: Le dossier ${AGENTS_DIR} n'existe pas${NC}"
        return 1
    fi

    local total=0
    local actifs=0
    local en_attente=0

    # Parcourir les dossiers d'agents
    for agent_dir in "$AGENTS_DIR"/*/; do
        if [[ -d "$agent_dir" ]]; then
            local agent_name=$(basename "$agent_dir")
            
            # Ignorer le dossier tools
            if [[ "$agent_name" == "tools" ]]; then
                continue
            fi

            local agent_file="${agent_dir}${agent_name}.md"
            local corrections_file="${agent_dir}corrections.md"

            if [[ -f "$agent_file" ]]; then
                # Filtre par tag (convention-tags)
                if [[ -n "$tag" ]]; then
                    local tags_agent=$(lire_tags "$agent_file")
                    # Normaliser les virgules en espaces pour une comparaison fiable
                    local tags_norm=$(echo "$tags_agent" | tr ',' ' ')
                    if [[ " $tags_norm " != *" $tag "* ]]; then
                        continue
                    fi
                fi

                echo -e "${CYAN}----------------------------------------${NC}"
                echo -e "${GREEN}[AGENT] Agent : ${agent_name}${NC}"
                echo -e "${CYAN}----------------------------------------${NC}"

                # Extraire le role (convention v0.3.0 : role-agent, repli role:)
                local role=$(grep -E '^[[:space:]]*role-agent:' "$agent_file" 2>/dev/null | head -1 | sed 's/.*role-agent:[[:space:]]*//' | sed 's/^"//' | sed 's/"$//' | tr -d '\r')
                if [[ -z "$role" ]]; then
                    role=$(grep -E '^[[:space:]]*role:' "$agent_file" 2>/dev/null | head -1 | sed 's/.*role:[[:space:]]*//' | sed 's/^"//' | sed 's/"$//' | tr -d '\r')
                fi
                if [[ -n "$role" ]]; then
                    echo -e "  [ROLE] ${role}"
                fi

                # Extraire le statut (convention v0.3.0 : statut-<agent>, repli statut:)
                local statut=$(grep -E "^[[:space:]]*statut-${agent_name}:" "$agent_file" 2>/dev/null | head -1 | sed "s/.*statut-${agent_name}:[[:space:]]*//" | sed 's/^"//' | sed 's/"$//' | tr -d '\r')
                if [[ -z "$statut" ]]; then
                    statut=$(grep -E '^[[:space:]]*statut:' "$agent_file" 2>/dev/null | head -1 | sed 's/.*statut:[[:space:]]*//' | sed 's/^"//' | sed 's/"$//' | tr -d '\r')
                fi
                if [[ -n "$statut" ]]; then
                    echo -e "  [STATUT] ${statut}"
                fi

                # Verifier si c'est un agent principal
                local principal=$(grep -E '^[[:space:]]*role_principal:' "$agent_file" 2>/dev/null | head -1 | sed 's/.*role_principal:[[:space:]]*//' | tr -d '\r')
                if [[ "$principal" == "true" ]]; then
                    echo -e "  [PRINCIPAL] Oui"
                    actifs=$((actifs + 1))
                else
                    en_attente=$((en_attente + 1))
                fi

                # Extraire la version
                local version=$(grep -E '^[[:space:]]*version:' "$agent_file" 2>/dev/null | head -1 | sed 's/.*version:[[:space:]]*//' | sed 's/^"//' | sed 's/"$//' | tr -d '\r')
                if [[ -n "$version" ]]; then
                    echo -e "  [VERSION] ${version}"
                fi

                if [[ "$detail" == "true" ]]; then
                    echo ""
                    echo -e "  ${YELLOW}Details :${NC}"
                    
                    # Verifier les fichiers de surcharge
                    if [[ -f "$corrections_file" ]]; then
                        echo -e "    [OK] Fichier corrections : Present"
                    else
                        echo -e "    [ERREUR] Fichier corrections : Absent"
                    fi

                    # Verifier la carte de decision
                    if grep -q "CARTE DE DECISION" "$agent_file" 2>/dev/null; then
                        echo -e "    [OK] Carte de decision : Presente"
                    else
                        echo -e "    [ERREUR] Carte de decision : Absente"
                    fi

                    # Verifier les boucles de retro-action
                    local retro_dir="${agent_dir}retro-actions"
                    if [[ -d "$retro_dir" ]]; then
                        local nb_boucles=$(ls -1 "$retro_dir"/*.md 2>/dev/null | wc -l)
                        echo -e "    [BOUCLES] Boucles de retro-action : ${nb_boucles}"
                    else
                        echo -e "    [BOUCLES] Boucles de retro-action : Aucune"
                    fi
                fi

                total=$((total + 1))
                echo ""
            else
                echo -e "  ${YELLOW}[ATTENTION]  Fiche d'agent non trouvee${NC}"
                echo ""
            fi
        fi
    done

    echo -e "${CYAN}----------------------------------------${NC}"
    echo -e "${BLUE}Resume :${NC}"
    echo -e "  [TOTAL] Agents : ${total}"
    echo -e "  [PRINCIPAUX] ${actifs}"
    echo -e "  [ATTENTE] ${en_attente}"
    echo -e "${CYAN}----------------------------------------${NC}"
}

# Valeurs par defaut
VERBOSE="false"
DETAIL="false"
TAG=""

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --aide|-h)
            aide
            exit 0
            ;;
        --verbose|-v)
            VERBOSE="true"
            shift
            ;;
        --version)
            echo "lister-agents v${VERSION}"
            exit 0
            ;;
        --detail|-d)
            DETAIL="true"
            shift
            ;;
        --tag)
            TAG="$2"
            shift 2
            ;;
        -*)
            echo "Option inconnue: $1"
            echo "Utilisez --aide pour l'aide"
            exit 1
            ;;
        *)
            shift
            ;;
    esac
done

# Execution
lister_agents "$VERBOSE" "$DETAIL" "$TAG"

exit $?
