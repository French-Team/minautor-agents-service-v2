#!/bin/bash
# lister-agents.sh
# Lister les agents avec leurs informations
# Version: 0.1.0
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
VERSION="0.1.0"
DATE="2026-08-05"
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
    echo "  --verbose, -v       Afficher les détails"
    echo "  --version           Afficher la version"
    echo "  --detail, -d        Afficher les détails complets"
    echo ""
    echo "Exemples:"
    echo "  lister-agents"
    echo "  lister-agents --detail"
    echo ""
}

# Fonction pour lister les agents
lister_agents() {
    local verbose=$1
    local detail=$2

    echo -e "${BLUE}📋 Liste des agents du cerveau-projet${NC}"
    echo ""

    # Vérifier si le dossier agents existe
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

            echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${GREEN}🤖 Agent : ${agent_name}${NC}"
            echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

            if [[ -f "$agent_file" ]]; then
                # Extraire le rôle
                local role=$(grep -A1 "role:" "$agent_file" 2>/dev/null | head -2 | tail -1 | sed 's/^ *//' | sed 's/^"//' | sed 's/"$//')
                if [[ -n "$role" ]]; then
                    echo -e "  📌 Rôle : ${role}"
                fi

                # Extraire le statut
                local statut=$(grep "statut:" "$agent_file" 2>/dev/null | head -1 | sed 's/.*statut: *//' | sed 's/^"//' | sed 's/"$//')
                if [[ -n "$statut" ]]; then
                    echo -e "  📊 Statut : ${statut}"
                fi

                # Vérifier si c'est un agent principal
                local principal=$(grep "role_principal:" "$agent_file" 2>/dev/null | head -1 | sed 's/.*role_principal: *//')
                if [[ "$principal" == "true" ]]; then
                    echo -e "  ⭐ Rôle principal : Oui"
                    actifs=$((actifs + 1))
                else
                    en_attente=$((en_attente + 1))
                fi

                # Extraire la version
                local version=$(grep "version:" "$agent_file" 2>/dev/null | head -1 | sed 's/.*version: *//' | sed 's/^"//' | sed 's/"$//')
                if [[ -n "$version" ]]; then
                    echo -e "  📦 Version : ${version}"
                fi

                if [[ "$detail" == "true" ]]; then
                    echo ""
                    echo -e "  ${YELLOW}Détails :${NC}"
                    
                    # Vérifier les fichiers de surcharge
                    if [[ -f "$corrections_file" ]]; then
                        echo -e "    ✅ Fichier corrections : Présent"
                    else
                        echo -e "    ❌ Fichier corrections : Absent"
                    fi

                    # Vérifier la carte de décision
                    if grep -q "CARTE DE DÉCISION" "$agent_file" 2>/dev/null; then
                        echo -e "    ✅ Carte de décision : Présente"
                    else
                        echo -e "    ❌ Carte de décision : Absente"
                    fi

                    # Vérifier les boucles de rétro-action
                    local retro_dir="${agent_dir}retro-actions"
                    if [[ -d "$retro_dir" ]]; then
                        local nb_boucles=$(ls -1 "$retro_dir"/*.md 2>/dev/null | wc -l)
                        echo -e "    🔄 Boucles de rétro-action : ${nb_boucles}"
                    else
                        echo -e "    🔄 Boucles de rétro-action : Aucune"
                    fi
                fi

                total=$((total + 1))
                echo ""
            else
                echo -e "  ${YELLOW}⚠️  Fiche d'agent non trouvée${NC}"
                echo ""
            fi
        fi
    done

    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Résumé :${NC}"
    echo -e "  📊 Total agents : ${total}"
    echo -e "  ⭐ Agents principaux : ${actifs}"
    echo -e "  🕐 Agents en attente : ${en_attente}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Valeurs par défaut
VERBOSE="false"
DETAIL="false"

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

# Exécution
lister_agents "$VERBOSE" "$DETAIL"

exit $?
