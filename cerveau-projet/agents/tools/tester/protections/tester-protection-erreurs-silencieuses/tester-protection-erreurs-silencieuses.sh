#!/bin/bash
# tester-protection-erreurs-silencieuses.sh
# Protection contre les erreurs silencieuses
# Version : 0.1.0
# Statut : ebauche

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
PROTECTION_LOG_DIR=${PROTECTION_LOG_DIR:-/tmp/test-logs}
PROTECTION_VERIFY_OUTPUT=${PROTECTION_VERIFY_OUTPUT:-true}

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Creer le dossier de logs
mkdir -p "$PROTECTION_LOG_DIR"

# Fonction pour executer un test avec verification des erreurs
executer_test_securise() {
    local test_cmd="$1"
    local test_name="$2"
    local expected_exit="${3:-0}"
    
    echo "[PROTECTION] Test securise: $test_name"
    
    # Creer les fichiers de log
    local log_file="$PROTECTION_LOG_DIR/${test_name// /_}.log"
    local stdout_file="$PROTECTION_LOG_DIR/${test_name// /_}_stdout.log"
    local stderr_file="$PROTECTION_LOG_DIR/${test_name// /_}_stderr.log"
    
    # Initialiser les logs
    echo "=== Test: $test_name ===" > "$log_file"
    echo "Date: $(date)" >> "$log_file"
    echo "Commande: $test_cmd" >> "$log_file"
    echo "---" >> "$log_file"
    
    # Executer la commande
    eval "$test_cmd" > "$stdout_file" 2> "$stderr_file"
    local exit_code=$?
    
    # Enregistrer le resultat
    echo "Code de sortie: $exit_code" >> "$log_file"
    echo "Attendu: $expected_exit" >> "$log_file"
    
    # Verifier le code de sortie
    local erreurs=0
    
    if [ $exit_code -ne $expected_exit ]; then
        echo -e "${RED}[ERREUR] Code de sortie inattendu: $exit_code (attendu: $expected_exit)${NC}"
        echo "Erreur: Code de sortie inattendu" >> "$log_file"
        erreurs=$((erreurs + 1))
    fi
    
    # Verifier si le stdout est vide (possiblement une erreur silencieuse)
    if [ ! -s "$stdout_file" ] && [ "$PROTECTION_VERIFY_OUTPUT" = "true" ]; then
        echo -e "${YELLOW}[ATTENTION] Sortie stdout vide${NC}"
        echo "Attention: Sortie stdout vide" >> "$log_file"
    fi
    
    # Verifier si le stderr contient des erreurs
    if [ -s "$stderr_file" ]; then
        echo -e "${YELLOW}[ATTENTION] Erreurs dans stderr:${NC}"
        head -5 "$stderr_file"
        echo "Erreur: Erreurs detectees dans stderr" >> "$log_file"
        erreurs=$((erreurs + 1))
    fi
    
    # Verifier les mots-cles d'erreur dans la sortie
    if grep -qiE '(error|erreur|failed|echec|exception|fatal)' "$stdout_file" 2>/dev/null; then
        echo -e "${YELLOW}[ATTENTION] Mots-cles d'erreur detectes dans stdout${NC}"
        grep -iE '(error|erreur|failed|echec|exception|fatal)' "$stdout_file" | head -5
        echo "Erreur: Mots-cles d'erreur dans stdout" >> "$log_file"
        erreurs=$((erreurs + 1))
    fi
    
    # Enregistrer les sorties dans le log
    echo "--- STDOUT ---" >> "$log_file"
    cat "$stdout_file" >> "$log_file" 2>/dev/null
    echo "" >> "$log_file"
    echo "--- STDERR ---" >> "$log_file"
    cat "$stderr_file" >> "$log_file" 2>/dev/null
    
    # Nettoyer les fichiers temporaires
    rm -f "$stdout_file" "$stderr_file"
    
    if [ $erreurs -gt 0 ]; then
        echo -e "${RED}[ERREUR] $erreurs erreur(s) detectee(s)${NC}"
        echo "Resultat: ECHEC" >> "$log_file"
        return 1
    else
        echo -e "${GREEN}[OK] Test reussi sans erreur silencieuse${NC}"
        echo "Resultat: SUCCES" >> "$log_file"
        return 0
    fi
}

# Fonction pour valider la sortie d'un test
valider_sortie() {
    local stdout_file="$1"
    local pattern="$2"
    local description="$3"
    
    if grep -q "$pattern" "$stdout_file" 2>/dev/null; then
        echo -e "${GREEN}[OK] $description${NC}"
        return 0
    else
        echo -e "${RED}[ERREUR] $description${NC}"
        echo "  -> Pattern '$pattern' non trouve dans la sortie"
        return 1
    fi
}

# Fonction pour generer un rapport
generer_rapport() {
    local test_name="$1"
    local total="$2"
    local passed="$3"
    local failed="$4"
    
    local report_file="$PROTECTION_LOG_DIR/rapport_${test_name// /_}.md"
    
    cat > "$report_file" << EOF
# Rapport de Test: $test_name

## Resume
- Date: $(date)
- Total: $total tests
- Reussis: $passed
- Echecs: $failed

## Statut
$([ $failed -eq 0 ] && echo "SUCCES" || echo "ECHEC")

## Details
Voir les fichiers de log dans: $PROTECTION_LOG_DIR
EOF
    
    echo -e "${BLUE}[INFO] Rapport genere: $report_file${NC}"
}

# Si le script est appele directement
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [ $# -eq 0 ]; then
        echo "Usage: $0 <commande> [nom] [exit-attendu]"
        echo ""
        echo "Exemples:"
        echo "  $0 './mon-outil.sh --test' 'Mon test' 0"
        echo "  $0 './mon-outil.sh' 'Test avec erreur' 1"
    else
        executer_test_securise "$1" "${2:-Test}" "${3:-0}"
    fi
fi
