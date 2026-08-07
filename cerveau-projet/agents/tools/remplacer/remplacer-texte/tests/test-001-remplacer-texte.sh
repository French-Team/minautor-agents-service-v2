#!/bin/bash
# test-001-remplacer-texte.sh
# Tests formels de l'outil remplacer-texte avec protections

# Chemin vers les protections (tools/tester/protections/)
PROTECTIONS_DIR="$(cd "$(dirname "$0")/../../../../tester/protections" 2>/dev/null && pwd)"
if [ -z "$PROTECTIONS_DIR" ] || [ ! -d "$PROTECTIONS_DIR" ]; then
    PROTECTIONS_DIR="$(dirname "$0")/../../../../tester/protections"
fi

# Charger les protections
source "$PROTECTIONS_DIR/tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh"
source "$PROTECTIONS_DIR/tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh"
source "$PROTECTIONS_DIR/tester-protection-blocage/tester-protection-blocage.sh"

# Configuration
OUTIL_PY="$(cd "$(dirname "$0")/.." && pwd)/remplacer-texte.py"
OUTIL_SH="$(cd "$(dirname "$0")/.." && pwd)/remplacer-texte.sh"
DOSSIER_TEST="/tmp/test-remplacer-texte-morpheus"

# Preparer le dossier de test
preparer_dossier() {
    rm -rf "$DOSSIER_TEST"
    mkdir -p "$DOSSIER_TEST/sous"
    printf '# Test\n\nancien-nom ici\n' > "$DOSSIER_TEST/a.md"
    printf 'autre fichier avec ancien-nom\n' > "$DOSSIER_TEST/sous/b.md"
    printf 'journal historique\n' > "$DOSSIER_TEST/AGENTS-historique.md"
}

echo "=== Test: remplacer-texte ==="
echo "Date: $(date)"
echo ""

# Test 1: Nominal (py)
preparer_dossier
echo "--- Test 1: Remplacement nominal (py) ---"
RESULT=$(python3 "$OUTIL_PY" "$DOSSIER_TEST" 'ancien-nom=nouveau-nom' 2>&1)
echo "$RESULT"
if echo "$RESULT" | grep -q 'Modifies: 2' && grep -q 'nouveau-nom' "$DOSSIER_TEST/a.md"; then
    echo "[OK] Test 1 passe"
    result1=0
else
    echo "[ERREUR] Test 1 echoue"
    result1=1
fi

# Test 2: Dry-run ne modifie rien (py)
preparer_dossier
echo "--- Test 2: Dry-run ne modifie rien ---"
RESULT=$(python3 "$OUTIL_PY" --dry-run "$DOSSIER_TEST" 'ancien-nom=nouveau-nom' 2>&1)
echo "$RESULT"
if echo "$RESULT" | grep -q 'SERAIT MODIFIE' && grep -q 'ancien-nom' "$DOSSIER_TEST/a.md"; then
    echo "[OK] Test 2 passe"
    result2=0
else
    echo "[ERREUR] Test 2 echoue"
    result2=1
fi

# Test 3: Exclusions (AGENTS-historique.md intact)
preparer_dossier
echo "--- Test 3: Exclusions ---"
python3 "$OUTIL_PY" "$DOSSIER_TEST" 'ancien-nom=nouveau-nom' > /dev/null 2>&1
if grep -q 'journal historique' "$DOSSIER_TEST/AGENTS-historique.md" && ! grep -q 'nouveau-nom' "$DOSSIER_TEST/AGENTS-historique.md"; then
    echo "[OK] Test 3 passe (AGENTS-historique.md intact)"
    result3=0
else
    echo "[ERREUR] Test 3 echoue"
    result3=1
fi

# Test 4: Idempotence (2e execution sans changement)
preparer_dossier
echo "--- Test 4: Idempotence ---"
python3 "$OUTIL_PY" "$DOSSIER_TEST" 'ancien-nom=nouveau-nom' > /dev/null 2>&1
RESULT=$(python3 "$OUTIL_PY" "$DOSSIER_TEST" 'ancien-nom=nouveau-nom' 2>&1)
echo "$RESULT"
if echo "$RESULT" | grep -q 'Modifies: 0'; then
    echo "[OK] Test 4 passe"
    result4=0
else
    echo "[ERREUR] Test 4 echoue"
    result4=1
fi

# Test 5: Version sh
preparer_dossier
echo "--- Test 5: Version sh ---"
RESULT=$(bash "$OUTIL_SH" "$DOSSIER_TEST" 'ancien-nom=nouveau-nom' 2>&1)
echo "$RESULT"
if echo "$RESULT" | grep -q 'Modifies: 2' && grep -q 'nouveau-nom' "$DOSSIER_TEST/sous/b.md"; then
    echo "[OK] Test 5 passe"
    result5=0
else
    echo "[ERREUR] Test 5 echoue"
    result5=1
fi

# Test 6: Erreur - dossier inexistant
echo "--- Test 6: Erreur dossier inexistant ---"
RESULT=$(python3 "$OUTIL_PY" "/tmp/dossier-inexistant-xyz" 'a=b' 2>&1)
echo "$RESULT"
if echo "$RESULT" | grep -q 'ERREUR'; then
    echo "[OK] Test 6 passe"
    result6=0
else
    echo "[ERREUR] Test 6 echoue"
    result6=1
fi

# Nettoyage
rm -rf "$DOSSIER_TEST"

# Rapport final
echo ""
echo "=== Rapport ==="
total=6
passed=0
[ $result1 -eq 0 ] && passed=$((passed + 1))
[ $result2 -eq 0 ] && passed=$((passed + 1))
[ $result3 -eq 0 ] && passed=$((passed + 1))
[ $result4 -eq 0 ] && passed=$((passed + 1))
[ $result5 -eq 0 ] && passed=$((passed + 1))
[ $result6 -eq 0 ] && passed=$((passed + 1))

echo "Total: $total"
echo "Reussis: $passed"
echo "Echecs: $((total - passed))"

# Generer le rapport (protection erreurs silencieuses)
if command -v generer_rapport > /dev/null 2>&1; then
    generer_rapport "remplacer-texte" $total $passed $((total - passed))
fi

# Sortie
[ $((total - passed)) -eq 0 ] && exit 0 || exit 1
