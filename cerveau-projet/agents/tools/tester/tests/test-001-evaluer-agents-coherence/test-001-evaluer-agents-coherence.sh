#!/bin/bash
# test-001-evaluer-agents-coherence.sh
# Test des corrections apportees a evaluer-agents et evaluer-coherence.
#
# Corrections testees:
#   1. evaluer-agents exclut __pycache__ des outils manquants
#   2. evaluer-coherence utilise le projet root pour cible_racine
#   3. evaluer-coherence exclut les commandes systeme (cat, grep, sed, basher)

VERSION="0.1.0"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Chemin vers les protections
PROTECTIONS_DIR="$(cd "$(dirname "$0")/../protections" && pwd)"

# Charger les protections
source "$PROTECTIONS_DIR/tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh"
source "$PROTECTIONS_DIR/tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh"
source "$PROTECTIONS_DIR/tester-protection-blocage/tester-protection-blocage.sh"

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
TEST_LOG_DIR="/tmp/test-logs"
mkdir -p "$TEST_LOG_DIR"

echo "=== Test: evaluer-agents-coherence corrections ==="
echo "Date: $(date)"
echo "Project root: $PROJECT_ROOT"
echo ""

passed=0
total=0

# Test 1: evaluer-agents exclut __pycache__
echo "--- Test 1: evaluer-agents exclut __pycache__ ---"
total=$((total + 1))
result=$(python3 "$PROJECT_ROOT/cerveau-projet/agents/tools/evaluer/evaluer-agents/evaluer-agents.py" 2>&1)
if echo "$result" | grep -q "Outil __pycache__"; then
    echo -e "${RED}[ECHEC] Test 1: __pycache__ detecte comme outil manquant${NC}"
else
    echo -e "${GREEN}[OK] Test 1: __pycache__ exclu${NC}"
    passed=$((passed + 1))
fi

# Test 2: score evaluer-agents > 50/100
echo "--- Test 2: score evaluer-agents > 50/100 ---"
total=$((total + 1))
score=$(echo "$result" | grep -oP 'Score agents : \K\d+')
if [ -n "$score" ] && [ "$score" -gt 50 ]; then
    echo -e "${GREEN}[OK] Test 2: score = ${score}/100${NC}"
    passed=$((passed + 1))
else
    echo -e "${RED}[ECHEC] Test 2: score = ${score:-non trouve}/100${NC}"
fi

# Test 3: evaluer-coherence exclut commandes systeme
echo "--- Test 3: evaluer-coherence exclut cat/grep/sed/basher ---"
total=$((total + 1))
result2=$(python3 "$PROJECT_ROOT/cerveau-projet/agents/tools/evaluer/evaluer-coherence/evaluer-coherence.py" 2>&1)
if echo "$result2" | grep -q "cat.*reference par\|grep.*reference par\|sed.*reference par\|basher.*reference par"; then
    echo -e "${RED}[ECHEC] Test 3: commandes systeme signalees comme outils casses${NC}"
else
    echo -e "${GREEN}[OK] Test 3: commandes systeme exclues${NC}"
    passed=$((passed + 1))
fi

# Test 4: faux positifs liens structures resolus
echo "--- Test 4: faux positifs liens structures resolus ---"
total=$((total + 1))
if echo "$result2" | grep -q "agents/conventions/structures/convention-structures.md\|agents/conventions/structures/convention-classeur-variables.md"; then
    echo -e "${RED}[ECHEC] Test 4: liens structures encore signales comme casses${NC}"
else
    echo -e "${GREEN}[OK] Test 4: liens structures resolus${NC}"
    passed=$((passed + 1))
fi

# Test 5: evaluer-coherence dit 'Tous les outils references existent'
echo "--- Test 5: evaluer-coherence dit 'Tous les outils references existent' ---"
total=$((total + 1))
if echo "$result2" | grep -q "Tous les outils references existent"; then
    echo -e "${GREEN}[OK] Test 5: tous les outils references existent${NC}"
    passed=$((passed + 1))
else
    echo -e "${RED}[ECHEC] Test 5: message 'Tous les outils references existent' absent${NC}"
fi

# Rapport final
echo ""
echo "=== Rapport ==="
echo "Total: $total"
echo "Reussis: $passed"
echo "Echecs: $((total - passed))"

generer_rapport "test-001-evaluer-agents-coherence" $total $passed $((total - passed))

[ $((total - passed)) -eq 0 ] && exit 0 || exit 1
