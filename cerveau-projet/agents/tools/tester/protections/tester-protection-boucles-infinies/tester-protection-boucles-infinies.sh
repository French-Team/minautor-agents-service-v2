#!/bin/bash
# tester-protection-boucles-infinies.sh
# Protection contre les boucles infinies
# Version : 0.1.0
# Statut : ebauche

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
PROTECTION_TIMEOUT=${PROTECTION_TIMEOUT:-30}  # Delai maximum en secondes
PROTECTION_ACTION=${PROTECTION_ACTION:-kill}  # Action : kill, signal, log

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonction pour lancer un test avec protection
lancer_avec_protection() {
    local test_cmd="$1"
    local test_name="$2"
    local timeout="${3:-$PROTECTION_TIMEOUT}"
    
    echo "[PROTECTION] Lancement de: $test_name (timeout: ${timeout}s)"
    
    # Creer un fichier temporaire pour la sortie
    local temp_out=$(mktemp)
    local temp_err=$(mktemp)
    
    # Lancer la commande avec timeout en arriere-plan
    timeout $timeout bash -c "$test_cmd" > "$temp_out" 2> "$temp_err" &
    local pid=$!
    
    # Surveiller le processus
    local start_time=$(date +%s)
    while kill -0 $pid 2>/dev/null; do
        sleep 1
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))
        
        if [ $elapsed -ge $timeout ]; then
            echo -e "${RED}[ERREUR] Timeout: $test_name a depasse ${timeout}s${NC}"
            echo "  -> Le test semble etre en boucle infinie"
            
            # Tuer le processus
            kill -TERM $pid 2>/dev/null
            sleep 1
            kill -KILL $pid 2>/dev/null
            
            # Afficher la sortie partielle
            echo "  -> Sortie partielle:"
            cat "$temp_out" | tail -5
            
            # Nettoyer
            rm -f "$temp_out" "$temp_err"
            return 124
        fi
    done
    
    # Recuperer le code de sortie
    wait $pid 2>/dev/null
    local exit_code=$?
    
    # Afficher les sorties si erreur
    if [ $exit_code -ne 0 ]; then
        echo -e "${YELLOW}[ATTENTION] Test echoue avec le code: $exit_code${NC}"
        if [ -s "$temp_err" ]; then
            echo "  -> Erreur:"
            cat "$temp_err" | tail -5
        fi
    fi
    
    # Nettoyer
    rm -f "$temp_out" "$temp_err"
    return $exit_code
}

# Fonction pour executer une serie de tests avec protection
executer_tests_avec_protection() {
    local test_file="$1"
    
    if [ ! -f "$test_file" ]; then
        echo -e "${RED}[ERREUR] Fichier de test non trouve: $test_file${NC}"
        return 1
    fi
    
    echo "=== Execution des tests avec protection ==="
    echo "Fichier: $test_file"
    echo "Timeout: ${PROTECTION_TIMEOUT}s"
    echo ""
    
    local total=0
    local passed=0
    local failed=0
    local timeout=0
    
    # Lire et executer chaque test
    while IFS= read -r line; do
        # Ignorer les commentaires et lignes vides
        [[ "$line" =~ ^#.*$ ]] && continue
        [ -z "$line" ] && continue
        
        # Executer le test
        total=$((total + 1))
        lancer_avec_protection "$line" "Test $total"
        local result=$?
        
        if [ $result -eq 0 ]; then
            passed=$((passed + 1))
            echo -e "${GREEN}[OK] Test $total passe${NC}"
        elif [ $result -eq 124 ]; then
            timeout=$((timeout + 1))
            echo -e "${RED}[ERREUR] Test $total timeout${NC}"
        else
            failed=$((failed + 1))
            echo -e "${RED}[ERREUR] Test $total echoue${NC}"
        fi
    done < "$test_file"
    
    # Rapport
    echo ""
    echo "=== Rapport ==="
    echo "Total: $total"
    echo -e "Reussis: ${GREEN}$passed${NC}"
    echo -e "Echecs: ${RED}$failed${NC}"
    echo -e "Timeouts: ${YELLOW}$timeout${NC}"
    
    return $((failed + timeout))
}

# Si le script est appele directement
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [ $# -eq 0 ]; then
        echo "Usage: $0 <commande> [nom] [timeout]"
        echo ""
        echo "Exemples:"
        echo "  $0 './mon-outil.sh --test' 'Mon test' 30"
        echo "  $0 './mon-outil.sh' 'Test rapide' 10"
    else
        lancer_avec_protection "$1" "${2:-Test}" "${3:-$PROTECTION_TIMEOUT}"
    fi
fi
