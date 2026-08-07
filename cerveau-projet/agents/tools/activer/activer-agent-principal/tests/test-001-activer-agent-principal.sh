#!/bin/bash
# test-001-activer-agent-principal.sh
# Tests formels de l'outil activer-agent-principal v0.3.0 (multi-session LLM) avec protections

# Chemin vers les protections (tools/tester/protections/)
PROTECTIONS_DIR="$(cd "$(dirname "$0")/../../../tester/protections" 2>/dev/null && pwd)"
if [ -z "$PROTECTIONS_DIR" ] || [ ! -d "$PROTECTIONS_DIR" ]; then
    PROTECTIONS_DIR="$(dirname "$0")/../../../tester/protections"
fi

# Charger les protections
source "$PROTECTIONS_DIR/tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh"
source "$PROTECTIONS_DIR/tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh"
source "$PROTECTIONS_DIR/tester-protection-blocage/tester-protection-blocage.sh"

# Configuration
OUTIL_PY="$(cd "$(dirname "$0")/.." && pwd)/activer-agent-principal.py"
OUTIL_SH="$(cd "$(dirname "$0")/.." && pwd)/activer-agent-principal.sh"
ESPACE="/tmp/test-activer-agent-morpheus"
export AGENTS_FILE="$ESPACE/AGENTS.md"
export AGENTS_HISTORIQUE="$ESPACE/AGENTS-historique.md"

# Preparer l'espace de test avec une copie de l'ANCIENNE structure (mono-session)
preparer_ancienne_structure() {
    rm -rf "$ESPACE"
    mkdir -p "$ESPACE"
    cat > "$AGENTS_FILE" << 'EOF'
# Agents du Cerveau-Projet

---

## Agent Principal Actuel

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus |
| **Role** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-08-07 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | - |
| **Raison** | - |

---

## Autre section

Contenu qui doit rester intact.

---

## Liste des agents

| Agent | Role |
|---|---|
| [Cerberus](cerveau-projet/agents/cerberus/cerberus.md) | Gardien de l'entree |
EOF
    cat > "$AGENTS_HISTORIQUE" << 'EOF'
# Historique des Agents

---

| 2026-08-07 10:00 | Cerberus | Ancienne entree |
EOF
}

echo "=== Test: activer-agent-principal v0.3.0 (multi-session LLM) ==="
echo "Date: $(date)"
echo ""

# ---------------------------------------------------------------------
# Test 1: MIGRATION + sidentifier automatique (py)
# ---------------------------------------------------------------------
preparer_ancienne_structure
echo "--- Test 1: Migration + sidentifier auto (py) ---"
RESULT=$(python3 "$OUTIL_PY" sidentifier 2>&1)
echo "$RESULT"
if echo "$RESULT" | grep -q "Session attribuee : session-llm-1" \
   && grep -q "^## Sessions LLM" "$AGENTS_FILE" \
   && grep -q "^### Session : session-llm-1" "$AGENTS_FILE" \
   && grep -q "^| \*\*Nom\*\* | Cerberus |" "$AGENTS_FILE" \
   && grep -q "^## Autre section" "$AGENTS_FILE" \
   && grep -q "session-llm-1" "$AGENTS_HISTORIQUE"; then
    echo "[OK] Test 1 passe (migration + bloc + valeurs conservees + historique)"
    result1=0
else
    echo "[ERREUR] Test 1 echoue"
    result1=1
fi

# ---------------------------------------------------------------------
# Test 2: Deuxieme sidentifier auto -> session-llm-2 (py)
# ---------------------------------------------------------------------
echo "--- Test 2: Deuxieme sidentifier auto -> session-llm-2 ---"
RESULT=$(python3 "$OUTIL_PY" sidentifier 2>&1)
echo "$RESULT"
if echo "$RESULT" | grep -q "Session attribuee : session-llm-2" \
   && grep -q "^### Session : session-llm-2" "$AGENTS_FILE"; then
    echo "[OK] Test 2 passe"
    result2=0
else
    echo "[ERREUR] Test 2 echoue"
    result2=1
fi

# ---------------------------------------------------------------------
# Test 3: sidentifier avec nom explicite (py)
# ---------------------------------------------------------------------
echo "--- Test 3: sidentifier session-llm-5 (nom explicite) ---"
RESULT=$(python3 "$OUTIL_PY" sidentifier session-llm-5 2>&1)
echo "$RESULT"
if grep -q "^### Session : session-llm-5" "$AGENTS_FILE"; then
    echo "[OK] Test 3 passe (bloc session-llm-5 cree)"
    result3=0
else
    echo "[ERREUR] Test 3 echoue"
    result3=1
fi

# ---------------------------------------------------------------------
# Test 4: ISOLATION des sessions (py) - activer dans session-llm-1 ne touche pas session-llm-2
# ---------------------------------------------------------------------
echo "--- Test 4: Isolation des sessions (activer session-llm-1, session-llm-2 intacte) ---"
RESULT=$(python3 "$OUTIL_PY" activer session-llm-1 Buffy "Mission isolation" 2>&1)
echo "$RESULT"
NOM_S2=$(grep -A 8 "^### Session : session-llm-2" "$AGENTS_FILE" | grep "^| \*\*Nom\*\*" | sed 's/.*| //; s/ |//')
echo "Agent principal session-llm-2: $NOM_S2"
if echo "$RESULT" | grep -q "agent Buffy active" \
   && grep -q "^| \*\*Nom\*\* | Buffy |" "$AGENTS_FILE" \
   && [ "$NOM_S2" = "Cerberus" ]; then
    echo "[OK] Test 4 passe (session-llm-2 intacte: $NOM_S2)"
    result4=0
else
    echo "[ERREUR] Test 4 echoue"
    result4=1
fi

# ---------------------------------------------------------------------
# Test 5: activer - tous les champs du bon bloc (py)
# ---------------------------------------------------------------------
echo "--- Test 5: activer - tous les champs (py) ---"
RESULT=$(python3 "$OUTIL_PY" activer session-llm-1 Morpheus "Mission tests" 2>&1)
echo "$RESULT"
if grep -q "^| \*\*Nom\*\* | Morpheus |" "$AGENTS_FILE" \
   && grep -q "^| \*\*Role\*\* | Testeur -- validation des outils et des tests |" "$AGENTS_FILE" \
   && grep -q "morpheus.md" "$AGENTS_FILE" \
   && grep -q "corrections.md" "$AGENTS_FILE" \
   && grep -q "^| \*\*Active par\*\* | Cerberus (automatique) |" "$AGENTS_FILE" \
   && grep -q "^| \*\*Raison\*\* | Mission tests |" "$AGENTS_FILE"; then
    echo "[OK] Test 5 passe (Nom, Role, Fiche, Corrections, Active par, Raison)"
    result5=0
else
    echo "[ERREUR] Test 5 echoue"
    result5=1
fi

# ---------------------------------------------------------------------
# Test 6: reactiver - Cerberus remis dans le bon bloc (py)
# ---------------------------------------------------------------------
echo "--- Test 6: reactiver session-llm-1 (py) ---"
RESULT=$(python3 "$OUTIL_PY" reactiver session-llm-1 "Mission terminee" Morpheus 2>&1)
echo "$RESULT"
if echo "$RESULT" | grep -q "Cerberus reactive" \
   && grep -q "^| \*\*Nom\*\* | Cerberus |" "$AGENTS_FILE" \
   && grep -q "^| \*\*Active par\*\* | Morpheus (retour de mission) |" "$AGENTS_FILE"; then
    echo "[OK] Test 6 passe"
    result6=0
else
    echo "[ERREUR] Test 6 echoue"
    result6=1
fi

# ---------------------------------------------------------------------
# Test 7: HISTORIQUE 4 colonnes (py)
# ---------------------------------------------------------------------
echo "--- Test 7: Historique 4 colonnes ---"
ENTREES=$(grep -c "^| 20[0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9] | session-llm-1 |" "$AGENTS_HISTORIQUE")
echo "Entrees avec colonne session-llm-1: $ENTREES"
PREMIERE=$(grep "^| 20[0-9][0-9]-" "$AGENTS_HISTORIQUE" | head -1)
echo "Premiere entree (doit etre la plus recente): $PREMIERE"
if [ "$ENTREES" -ge 1 ] && echo "$PREMIERE" | grep -q "session-llm-1"; then
    echo "[OK] Test 7 passe (4 colonnes + ordre decroissant)"
    result7=0
else
    echo "[ERREUR] Test 7 echoue"
    result7=1
fi

# ---------------------------------------------------------------------
# Test 8: PARITE .sh (migration + activer via bash)
# ---------------------------------------------------------------------
preparer_ancienne_structure
echo "--- Test 8: Parite .sh ---"
RESULT=$(bash "$OUTIL_SH" sidentifier 2>&1)
echo "$RESULT"
RESULT2=$(bash "$OUTIL_SH" activer session-llm-1 Vulcain "Parite sh" 2>&1)
echo "$RESULT2"
if echo "$RESULT" | grep -q "session-llm-1" \
   && echo "$RESULT2" | grep -q "agent Vulcain active" \
   && grep -q "^| \*\*Nom\*\* | Vulcain |" "$AGENTS_FILE"; then
    echo "[OK] Test 8 passe (version .sh fonctionnelle)"
    result8=0
else
    echo "[ERREUR] Test 8 echoue"
    result8=1
fi

# ---------------------------------------------------------------------
# Test 9: ASCII - raison non-ASCII REFUSEE (py)
# ---------------------------------------------------------------------
preparer_ancienne_structure
echo "--- Test 9: Raison non-ASCII refusee ---"
RAISON_ACCENT=$(printf 'raison avec accent \xc3\xa9 accentue')
python3 "$OUTIL_PY" activer session-llm-1 Buffy "$RAISON_ACCENT" > /tmp/ascii-out.txt 2>&1
CODE=$?
echo "Code de retour: $CODE"
cat /tmp/ascii-out.txt
rm -f /tmp/ascii-out.txt
if [ "$CODE" -ne 0 ] && grep -q "^| \*\*Nom\*\* | Cerberus |" "$AGENTS_FILE"; then
    echo "[OK] Test 9 passe (refuse + fichier intact)"
    result9=0
else
    echo "[ERREUR] Test 9 echoue"
    result9=1
fi

# ---------------------------------------------------------------------
# Test 10: ACTION sessions (py)
# ---------------------------------------------------------------------
preparer_ancienne_structure
python3 "$OUTIL_PY" sidentifier > /dev/null 2>&1
python3 "$OUTIL_PY" sidentifier > /dev/null 2>&1
python3 "$OUTIL_PY" activer session-llm-1 Buffy "Mission test 10" > /dev/null 2>&1
echo "--- Test 10: Action sessions ---"
RESULT=$(python3 "$OUTIL_PY" sessions 2>&1)
echo "$RESULT"
if echo "$RESULT" | grep -q "session-llm-1 : Buffy" \
   && echo "$RESULT" | grep -q "session-llm-2 : Cerberus"; then
    echo "[OK] Test 10 passe"
    result10=0
else
    echo "[ERREUR] Test 10 echoue"
    result10=1
fi

# ---------------------------------------------------------------------
# Test 11: SYNTAXE (bash -n + py_compile)
# ---------------------------------------------------------------------
echo "--- Test 11: Syntaxe bash + python ---"
if bash -n "$OUTIL_SH" && python3 -m py_compile "$OUTIL_PY"; then
    echo "[OK] Test 11 passe"
    result11=0
else
    echo "[ERREUR] Test 11 echoue"
    result11=1
fi

# ---------------------------------------------------------------------
# Test 12: CONVENTIONS (ASCII strict + nommage)
# ---------------------------------------------------------------------
echo "--- Test 12: Conventions (ASCII + nommage) ---"
ASCII_OK=1
for f in "$(dirname "$OUTIL_PY")/activer-agent-principal.py" "$(dirname "$OUTIL_SH")/activer-agent-principal.sh"; do
    if python3 -c "
import io, sys
c = io.open(sys.argv[1], encoding='utf-8').read()
sys.exit(0 if all(ord(ch) < 128 for ch in c) else 1)
" "$f"; then
        :
    else
        ASCII_OK=0
    fi
done
python3 cerveau-projet/agents/tools/valider/valider-nommage/valider-nommage.py --type outil "$OUTIL_PY" > /dev/null 2>&1
NOM_OK=$?
if [ "$ASCII_OK" -eq 1 ] && [ "$NOM_OK" -eq 0 ]; then
    echo "[OK] Test 12 passe (ASCII strict + nommage)"
    result12=0
else
    echo "[ERREUR] Test 12 echoue (ASCII_OK=$ASCII_OK nommage=$NOM_OK)"
    result12=1
fi

# ---------------------------------------------------------------------
# Nettoyage + rapport final
# ---------------------------------------------------------------------
rm -rf "$ESPACE"

echo ""
echo "=== Rapport ==="
total=12
passed=0
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
    eval "r=\$result$i"
    if [ "$r" -eq 0 ]; then
        passed=$((passed + 1))
    fi
done
echo "Total: $total"
echo "Reussis: $passed"
echo "Echecs: $((total - passed))"

# Generer le rapport (protection erreurs silencieuses)
if command -v generer_rapport > /dev/null 2>&1; then
    generer_rapport "activer-agent-principal-v0.3.0" $total $passed $((total - passed))
fi

# Sortie
[ $((total - passed)) -eq 0 ] && exit 0 || exit 1
