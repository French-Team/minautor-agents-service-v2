#!/bin/bash
# combos-valider-cerveau.sh
# Combo de validation : etat de sante du cerveau-projet en une commande
# Version : 0.2.0
# Statut : prepare

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier
# ============================================================

# Configuration
# identite:
#   type: combo
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
STATUT="prepare"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Racine du projet (4 niveaux au-dessus du script : combos-valider-cerveau/ -> combos/ -> tools/ -> agents/ -> cerveau-projet/)
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
RACINE=$(cd "$SCRIPT_DIR/../../../../.." && pwd)

# Chemins des 3 outils
VALIDER_RELECTURE="$RACINE/cerveau-projet/agents/tools/valider/valider-relecture/valider-relecture.sh"
VALIDER_CARTES="$RACINE/cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.sh"
VALIDER_ASCII="$RACINE/cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.sh"

# Afficher l'aide
afficher_aide() {
    echo "=== combos-valider-cerveau v${VERSION} ==="
    echo ""
    echo "Etat de sante du cerveau-projet en une commande :"
    echo "  1. valider-relecture        - regle de relecture dans les 11 fiches agents"
    echo "  2. valider-cartes-decision  - les 11 cartes de decision sont conformes"
    echo "  3. valider-conformite-ascii - 0 caractere non-ASCII dans le projet"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options :"
    echo "  --detail          Afficher la sortie complete des 3 outils"
    echo "  --stop            Arreter au premier echec"
    echo "  --help            Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0                          # Rapport combine resume"
    echo "  $0 --detail                 # Avec le detail des 3 outils"
    echo "  $0 --stop                   # Arreter au premier echec"
    echo ""
}

# Verifier que le nom de l'outil commence par le prefixe de la categorie (regle immuable)
verifier_nommage() {
    local script_nom=$(basename "$0" | sed 's/\.sh$//')
    [[ "$script_nom" == "outil-template" ]] && return 0
    local chemin_script=$(cd "$(dirname "$0")" 2>/dev/null && pwd)
    local categorie=$(basename "$(dirname "$chemin_script")")
    if [[ -z "$categorie" || "$categorie" == "." || "$categorie" == "/" ]]; then
        return 0
    fi
    if [[ "$script_nom" != "${categorie}-"* ]]; then
        echo -e "${RED}[ERREUR] Nommage invalide : $script_nom${NC}"
        echo -e "  Le nom doit commencer par '${categorie}-' (categorie: ${categorie}/)"
        echo -e "  Voir convention-renommage.md (regle immuable)"
        exit 1
    fi
}

# Verifier qu'un outil existe
verifier_outil() {
    local chemin="$1"
    if [ ! -f "$chemin" ]; then
        echo -e "${RED}[ERREUR] Outil introuvable : $chemin${NC}"
        return 1
    fi
    return 0
}

# Executer un outil et capturer verdict + code retour
executer_outil() {
    local nom="$1"
    local chemin="$2"
    local detail="$3"
    local sortie

    echo -e "${BLUE}--- $nom ---${NC}"

    if ! verifier_outil "$chemin"; then
        echo -e "  ${RED}[ERREUR] outil absent${NC}"
        echo "STATUT=${nom}=ABSENT"
        return 2
    fi

    sortie=$(timeout 60 bash "$chemin" 2>&1)
    local code=$?

    if [ "$detail" = "true" ]; then
        echo "$sortie" | head -30
        echo ""
    fi

    if [ $code -eq 0 ]; then
        echo -e "  ${GREEN}[OK]${NC} ${nom}"
        echo "STATUT=${nom}=OK"
        return 0
    else
        echo -e "  ${RED}[ERREUR]${NC} ${nom} (code $code)"
        echo "STATUT=${nom}=ERREUR"
        return 1
    fi
}

# Fonction principale
executer() {
    local detail="$1"
    local stop="$2"

    echo -e "${BLUE}=== combos-valider-cerveau v${VERSION} ===${NC}"
    echo "Etat de sante du cerveau-projet"
    echo ""

    local code_relecture=-1
    local code_cartes=-1
    local code_ascii=-1

    # 1. valider-relecture
    executer_outil "valider-relecture" "$VALIDER_RELECTURE" "$detail"
    code_relecture=$?
    if [ "$stop" = "true" ] && [ $code_relecture -ne 0 ]; then
        echo ""
        echo -e "${RED}=== VERDICT GLOBAL : NON CONFORME (arrete sur valider-relecture) ===${NC}"
        exit 1
    fi

    # 2. valider-cartes-decision
    executer_outil "valider-cartes-decision" "$VALIDER_CARTES" "$detail"
    code_cartes=$?
    if [ "$stop" = "true" ] && [ $code_cartes -ne 0 ]; then
        echo ""
        echo -e "${RED}=== VERDICT GLOBAL : NON CONFORME (arrete sur valider-cartes-decision) ===${NC}"
        exit 1
    fi

    # 3. valider-conformite-ascii
    executer_outil "valider-conformite-ascii" "$VALIDER_ASCII" "$detail"
    code_ascii=$?
    if [ "$stop" = "true" ] && [ $code_ascii -ne 0 ]; then
        echo ""
        echo -e "${RED}=== VERDICT GLOBAL : NON CONFORME (arrete sur valider-conformite-ascii) ===${NC}"
        exit 1
    fi

    # Rapport combine
    echo ""
    echo -e "${BLUE}=== VERDICT GLOBAL ===${NC}"
    [ $code_relecture -eq 0 ] && echo -e "  Relecture     : ${GREEN}OK${NC}" || echo -e "  Relecture     : ${RED}ERREUR${NC}"
    [ $code_cartes -eq 0 ] && echo -e "  Cartes        : ${GREEN}OK${NC}" || echo -e "  Cartes        : ${RED}ERREUR${NC}"
    [ $code_ascii -eq 0 ] && echo -e "  ASCII         : ${GREEN}OK${NC}" || echo -e "  ASCII         : ${RED}ERREUR${NC}"

    local total_ok=0
    [ $code_relecture -eq 0 ] && total_ok=$((total_ok + 1))
    [ $code_cartes -eq 0 ] && total_ok=$((total_ok + 1))
    [ $code_ascii -eq 0 ] && total_ok=$((total_ok + 1))

    if [ $total_ok -eq 3 ]; then
        echo -e "  RESULTAT      : ${GREEN}CONFORME${NC}"
        echo -e "  Code retour   : 0"
        exit 0
    else
        echo -e "  RESULTAT      : ${RED}NON CONFORME (${total_ok}/3)${NC}"
        echo -e "  Code retour   : 1"
        exit 1
    fi
}

# Main
main() {
    local detail="false"
    local stop="false"
    local help="false"

    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --detail)
                detail="true"
                shift
                ;;
            --stop)
                stop="true"
                shift
                ;;
            --help)
                help="true"
                shift
                ;;
            *)
                echo -e "${RED}[ERREUR] Option inconnue : $1${NC}"
                afficher_aide
                exit 1
                ;;
        esac
    done

    # Afficher l'aide
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi

    # Executer
    executer "$detail" "$stop"
}

# Verifier le nommage au demarrage (regle immuable)
verifier_nommage

# Executer
main "$@"
