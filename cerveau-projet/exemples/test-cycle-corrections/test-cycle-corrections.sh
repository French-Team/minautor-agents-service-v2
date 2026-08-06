#!/bin/bash
# test-cycle-corrections.sh
# Script de test du cycle d'auto-correction
# Version : 0.1.0
# Statut : ebauche

# Configuration
PROJET_DIR="cerveau-projet"
AGENTS_DIR="$PROJET_DIR/agents"
EXEMPLES_DIR="$PROJET_DIR/exemples/test-cycle-corrections"
RAPPORT_DIR="/tmp/test-corrections-rapports"

# Creer le dossier de rapports
mkdir -p "$RAPPORT_DIR"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Compteurs
total=0
passed=0
failed=0
warnings=0

# Fonction pour afficher un resultat
afficher_resultat() {
    local test_name="$1"
    local result="$2"
    local details="$3"
    
    total=$((total + 1))
    
    case $result in
        OK)
            passed=$((passed + 1))
            echo -e "${GREEN}[OK]${NC} $test_name"
            ;;
        ERREUR)
            failed=$((failed + 1))
            echo -e "${RED}[ERREUR]${NC} $test_name"
            if [ -n "$details" ]; then
                echo "      $details"
            fi
            ;;
        ATTENTION)
            warnings=$((warnings + 1))
            echo -e "${YELLOW}[ATTENTION]${NC} $test_name"
            if [ -n "$details" ]; then
                echo "      $details"
            fi
            ;;
    esac
}

# Fonction pour generer le rapport
generer_rapport() {
    local rapport_file="$RAPPORT_DIR/rapport-$(date +%Y%m%d-%H%M%S).md"
    
    cat > "$rapport_file" << EOF
# Rapport du Test du Cycle d'Auto-Correction

## Resume
- Date : $(date)
- Tests effectues : $total
- Reussis : $passed
- Echecs : $failed
- Avertissements : $warnings

## Statut
$([ $failed -eq 0 ] && echo "SUCCES" || echo "ECHEC")

## Tests

### Test 1 : Memoire persistante
$(for agent in buffy atlas janus vulcain morpheus; do
    corrections_file="$AGENTS_DIR/$agent/corrections.md"
    if [ -f "$corrections_file" ]; then
        if grep -q "Lecon\|lecon\|LECON" "$corrections_file" 2>/dev/null; then
            echo "- [OK] $agent : A des lecons"
        else
            echo "- [ATTENTION] $agent : Pas de lecon"
        fi
    else
        echo "- [ERREUR] $agent : Fichier corrections.md manquant"
    fi
done)

### Test 2 : Personnalisation
$(for agent in buffy vulcain; do
    corrections_file="$AGENTS_DIR/$agent/corrections.md"
    if [ -f "$corrections_file" ]; then
        rules=$(grep -c "^\|.*\|$" "$corrections_file" 2>/dev/null || echo 0)
        echo "- $agent : $rules regles specifiques"
    fi
done)

### Test 3 : Cycle complet
Le test complet necessite une intervention manuelle.
Voir le fichier test-cycle-corrections.md pour les instructions.

## Observations
- A completer lors du test manuel

## Recommandations
- A completer lors du test manuel
EOF
    
    echo -e "${BLUE}[INFO] Rapport genere : $rapport_file${NC}"
}

# Debut des tests
echo "=== Test du Cycle d'Auto-Correction ==="
echo "Date : $(date)"
echo ""

# Test 1 : Memoire persistante
echo "--- Test 1 : Memoire persistante ---"
for agent in buffy atlas janus vulcain morpheus; do
    corrections_file="$AGENTS_DIR/$agent/corrections.md"
    if [ -f "$corrections_file" ]; then
        # Verifier qu'il y a des lecons
        if grep -qi "lecon" "$corrections_file" 2>/dev/null; then
            afficher_resultat "$agent : A des lecons" "OK"
        else
            afficher_resultat "$agent : Pas de lecon" "ATTENTION"
        fi
    else
        afficher_resultat "$agent : Fichier corrections.md manquant" "ERREUR"
    fi
done
echo ""

# Test 2 : Personnalisation
echo "--- Test 2 : Personnalisation ---"
for agent in buffy vulcain; do
    corrections_file="$AGENTS_DIR/$agent/corrections.md"
    if [ -f "$corrections_file" ]; then
        # Compter les regles specifiques
        rules=$(grep -c "^\|.*\|$" "$corrections_file" 2>/dev/null || echo 0)
        if [ $rules -gt 0 ]; then
            afficher_resultat "$agent : $rules regles specifiques" "OK"
        else
            afficher_resultat "$agent : Pas de regles specifiques" "ATTENTION"
        fi
    else
        afficher_resultat "$agent : Fichier corrections.md manquant" "ERREUR"
    fi
done
echo ""

# Test 3 : Verification des fichiers
echo "--- Test 3 : Verification des fichiers ---"
for agent in buffy atlas janus vulcain morpheus; do
    agent_file="$AGENTS_DIR/$agent/$agent.md"
    corrections_file="$AGENTS_DIR/$agent/corrections.md"
    
    if [ -f "$agent_file" ] && [ -f "$corrections_file" ]; then
        afficher_resultat "$agent : Fichiers complets" "OK"
    else
        afficher_resultat "$agent : Fichiers incomplets" "ERREUR"
    fi
done
echo ""

# Test 4 : Cycle complet (instructions)
echo "--- Test 4 : Cycle complet ---"
echo "Pour tester le cycle complet :"
echo "  1. Activer un agent"
echo "  2. Lui faire faire une tache"
echo "  3. Verifier qu'il ajoute des corrections"
echo "  4. Reactiver Cerberus"
echo "  5. Reactiver l'agent"
echo "  6. Verifier qu'il evite l'erreur"
echo ""

# Resume
echo "=== Resume ==="
echo "Total : $total tests"
echo -e "Reussis : ${GREEN}$passed${NC}"
echo -e "Echecs : ${RED}$failed${NC}"
echo -e "Avertissements : ${YELLOW}$warnings${NC}"
echo ""

# Generer le rapport
generer_rapport

# Code de sortie
[ $failed -eq 0 ] && exit 0 || exit 1
