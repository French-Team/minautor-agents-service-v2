#!/bin/bash
# tester-protection-blocage.sh
# Protection contre les tests qui bloquent
# Version : 0.1.0
# Statut : ebauche

# Configuration
PROTECTION_blocage_TIMEOUT=${PROTECTION_blocage_TIMEOUT:-60}
PROTECTION_blocage_INTERVAL=${PROTECTION_blocage_INTERVAL:-5}
PROTECTION_blocage_MAX_OUTPUT=${PROTECTION_blocage_MAX_OUTPUT:-1000}

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonction pour detecter si un processus est bloque
detecter_blocage() {
    local pid="$1"
    local nom="$2"
    
    # Verifier si le processus tourne encore
    if ! kill -0 $pid 2>/dev/null; then
        return 0  # Le processus est termine
    fi
    
    # Verifier l'utilisation CPU
    local cpu=$(ps -p $pid -o %cpu= 2>/dev/null | tr -d ' ')
    if [ -n "$cpu" ]; then
        # Si CPU est tres bas pendant longtemps, c'est probablement bloque
        if (( $(echo "$cpu < 0.1" | bc -l 2>/dev/null || echo 0) )); then
            return 1  # Probablement bloque
        fi
    fi
    
    return 0  # Pas bloque
}

# Fonction pour executer un test avec protection contre le blocage
executer_sans_blocage() {
    local test_cmd="$1"
    local test_name="$2"
    local timeout="${3:-$PROTECTION_blocage_TIMEOUT}"
    
    echo "[PROTECTION] Test anti-blocage: $test_name (timeout: ${timeout}s)"
    
    # Creer un fichier temporaire pour la sortie
    local temp_file=$(mktemp)
    
    # Lancer la commande en arriere-plan
    eval "$test_cmd" > "$temp_file" 2>&1 &
    local pid=$!
    
    # Surveiller le processus
    local start_time=$(date +%s)
    local last_output_size=0
    local no_change_count=0
    
    while kill -0 $pid 2>/dev/null; do
        sleep $PROTECTION_blocage_INTERVAL
        
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))
        
        # Verifier le timeout
        if [ $elapsed -ge $timeout ]; then
            echo -e "${RED}[ERREUR] Timeout: $test_name a depasse ${timeout}s${NC}"
            echo "  -> Le test semble etre bloque"
            
            # Tuer le processus
            kill -TERM $pid 2>/dev/null
            sleep 2
            kill -KILL $pid 2>/dev/null
            
            # Afficher la sortie partielle
            echo "  -> Sortie partielle:"
            tail -10 "$temp_file"
            
            rm -f "$temp_file"
            return 1
        fi
        
        # Verifier si la sortie a change
        local current_size=$(wc -c < "$temp_file" 2>/dev/null || echo 0)
        if [ $current_size -eq $last_output_size ]; then
            no_change_count=$((no_change_count + 1))
            
            # Si pas de changement pendant 3 intervals, c'est suspect
            if [ $no_change_count -ge 3 ]; then
                echo -e "${YELLOW}[ATTENTION] Pas de sortie pendant ${PROTECTION_blocage_INTERVAL}s${NC}"
                echo "  -> Le test pourrait etre bloque"
            fi
        else
            no_change_count=0
        fi
        
        last_output_size=$current_size
        
        # Verifier la taille de la sortie (protection contre les sorties infinies)
        if [ $current_size -gt $PROTECTION_blocage_MAX_OUTPUT ]; then
            echo -e "${YELLOW}[ATTENTION] Sortie tres longue: $current_size octets${NC}"
            echo "  -> Le test pourrait generer une sortie infinie"
        fi
    done
    
    # Recuperer le code de sortie
    wait $pid 2>/dev/null
    local exit_code=$?
    
    # Afficher le resultat
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}[OK] Termine en ${elapsed}s${NC}"
    else
        echo -e "${RED}[ERREUR] Echec avec le code: $exit_code${NC}"
    fi
    
    rm -f "$temp_file"
    return $exit_code
}

# Fonction pour executer une serie de tests
executer_tests_anti_blocage() {
    local test_file="$1"
    
    if [ ! -f "$test_file" ]; then
        echo -e "${RED}[ERREUR] Fichier de test non trouve: $test_file${NC}"
        return 1
    fi
    
    echo "=== Execution des tests anti-blocage ==="
    echo "Fichier: $test_file"
    echo "Timeout: ${PROTECTION_blocage_TIMEOUT}s"
    echo ""
    
    local total=0
    local passed=0
    local failed=0
    
    while IFS= read -r line; do
        [[ "$line" =~ ^#.*$ ]] && continue
        [ -z "$line" ] && continue
        
        total=$((total + 1))
        executer_sans_blocage "$line" "Test $total"
        local result=$?
        
        if [ $result -eq 0 ]; then
            passed=$((passed + 1))
        else
            failed=$((failed + 1))
        fi
    done < "$test_file"
    
    echo ""
    echo "=== Rapport ==="
    echo "Total: $total"
    echo -e "Reussis: ${GREEN}$passed${NC}"
    echo -e "Echecs: ${RED}$failed${NC}"
    
    return $failed
}

# Si le script est appele directement
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [ $# -eq 0 ]; then
        echo "Usage: $0 <commande> [nom] [timeout]"
        echo ""
        echo "Exemples:"
        echo "  $0 './mon-outil.sh --test' 'Mon test' 30"
        echo "  $0 './mon-outil.sh' 'Test long' 60"
    else
        executer_sans_blocage "$1" "${2:-Test}" "${3:-$PROTECTION_blocage_TIMEOUT}"
    fi
fi
