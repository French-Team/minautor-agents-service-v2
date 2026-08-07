#!/bin/bash
# test-002-activer-agent-principal-v031.sh
# Tests formels v0.3.1 : profil session classeur (mettre_a_jour_profil_session) + regression v0.3.0

# Chemin vers les protections
PROTECTIONS_DIR="$(cd "$(dirname "$0")/../../../tester/protections" 2>/dev/null && pwd)"
if [ -z "$PROTECTIONS_DIR" ] || [ ! -d "$PROTECTIONS_DIR" ]; then
    PROTECTIONS_DIR="$(dirname "$0")/../../../tester/protections"
fi

source "$PROTECTIONS_DIR/tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh"
source "$PROTECTIONS_DIR/tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh"
source "$PROTECTIONS_DIR/tester-protection-blocage/tester-protection-blocage.sh"

OUTIL_PY="$(cd "$(dirname "$0")/.." && pwd)/activer-agent-principal.py"
OUTIL_SH="$(cd "$(dirname "$0")/.." && pwd)/activer-agent-principal.sh"
ESPACE="/tmp/test-activer-agent-v031"
export AGENTS_FILE="$ESPACE/AGENTS.md"
export AGENTS_HISTORIQUE="$ESPACE/AGENTS-historique.md"
export CLASSEUR_STOCKAGE="$ESPACE/variables-actuelles.md"

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
EOF
    cat > "$AGENTS_HISTORIQUE" << 'EOF'
# Historique des Agents

---

| 2026-08-07 10:00 | Cerberus | Ancienne entree |
EOF
    cat > "$CLASSEUR_STOCKAGE" << 'EOF'
# Stockage -- Variables Actuelles
---

## Variables
| Variable | Valeur | Source | Date | Statut |
|---|---|---|---|---|
| `donnees-brutes` | *(tableau de 5 objets)* | charger-donnees | 2026-08-04 | [OK] |
| `profil-systeme` | OS: Windows / Python: 3.14 | verifier-systeme | 2026-08-07 | [OK] |

---

## Comment mettre a jour

Texte de la section qui doit rester intact.
EOF
}

echo "=== Test: activer-agent-principal v0.3.1 (profil session classeur) ==="
echo "Date: $(date)"
echo ""

# ---------------------------------------------------------------------
# Test 1: sidentifier cree la ligne profil-session-llm-1 (agent=Cerberus) (py)
# ---------------------------------------------------------------------
preparer_ancienne_structure
echo "--- Test 1: sidentifier -> profil-session-llm-1 creee (Cerberus) (py) ---"
RESULT=$(python3 "$OUTIL_PY" sidentifier 2>&1)
echo "$RESULT"
LIGNE=$(grep '^| `profil-session-llm-1`' "$CLASSEUR_STOCKAGE" | head -1)
echo "Ligne classeur: $LIGNE"
if echo "$LIGNE" | grep -q 'session: session-llm-1 / agent: Cerberus / date: 20[0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]' \
   && echo "$LIGNE" | grep -q 'activer-agent-principal' \
   && echo "$LIGNE" | grep -q '\[OK\] \|$'; then
    echo "[OK] Test 1 passe (ligne creee avec Cerberus + format)"
    result1=0
else
    echo "[ERREUR] Test 1 echoue"
    result1=1
fi

# ---------------------------------------------------------------------
# Test 2: activer Buffy -> mise a jour (agent=Buffy), PAS de doublon (py)
# ---------------------------------------------------------------------
echo "--- Test 2: activer session-llm-1 Buffy -> mise a jour, pas de doublon (py) ---"
RESULT=$(python3 "$OUTIL_PY" activer session-llm-1 Buffy "Mission v031" 2>&1)
echo "$RESULT"
NB=$(grep -c '^| `profil-session-llm-1`' "$CLASSEUR_STOCKAGE")
echo "Lignes profil-session-llm-1: $NB"
LIGNE=$(grep '^| `profil-session-llm-1`' "$CLASSEUR_STOCKAGE" | head -1)
if [ "$NB" -eq 1 ] && echo "$LIGNE" | grep -q 'agent: Buffy'; then
    echo "[OK] Test 2 passe (1 seule ligne, agent=Buffy)"
    result2=0
else
    echo "[ERREUR] Test 2 echoue"
    result2=1
fi

# ---------------------------------------------------------------------
# Test 3: reactiver -> agent=Cerberus (py)
# ---------------------------------------------------------------------
echo "--- Test 3: reactiver session-llm-1 -> agent=Cerberus (py) ---"
RESULT=$(python3 "$OUTIL_PY" reactiver session-llm-1 "Mission terminee" Buffy 2>&1)
echo "$RESULT"
LIGNE=$(grep '^| `profil-session-llm-1`' "$CLASSEUR_STOCKAGE" | head -1)
if echo "$LIGNE" | grep -q 'agent: Cerberus'; then
    echo "[OK] Test 3 passe (agent=Cerberus)"
    result3=0
else
    echo "[ERREUR] Test 3 echoue"
    result3=1
fi

# ---------------------------------------------------------------------
# Test 4: session inexistante -> ligne AJOUTEE a la fin du tableau (py)
# ---------------------------------------------------------------------
echo "--- Test 4: activer session-llm-2 -> ligne profil-session-llm-2 ajoutee ---"
RESULT=$(python3 "$OUTIL_PY" activer session-llm-2 Vulcain "Nouvelle session" 2>&1)
echo "$RESULT"
LIGNE2=$(grep '^| `profil-session-llm-2`' "$CLASSEUR_STOCKAGE" | head -1)
echo "Ligne session-llm-2: $LIGNE2"
if echo "$LIGNE2" | grep -q 'session: session-llm-2 / agent: Vulcain'; then
    echo "[OK] Test 4 passe (ligne ajoutee)"
    result4=0
else
    echo "[ERREUR] Test 4 echoue"
    result4=1
fi

# ---------------------------------------------------------------------
# Test 5: autres lignes du stockage intactes + section intacte (py)
# ---------------------------------------------------------------------
echo "--- Test 5: autres lignes du stockage intactes ---"
if grep -q '`donnees-brutes`' "$CLASSEUR_STOCKAGE" \
   && grep -q '`profil-systeme`' "$CLASSEUR_STOCKAGE" \
   && grep -q 'Texte de la section qui doit rester intact' "$CLASSEUR_STOCKAGE"; then
    echo "[OK] Test 5 passe (aucune perte)"
    result5=0
else
    echo "[ERREUR] Test 5 echoue"
    result5=1
fi

# ---------------------------------------------------------------------
# Test 6: PARITE .sh (sidentifier + activer via bash -> ligne classeur)
# ---------------------------------------------------------------------
preparer_ancienne_structure
echo "--- Test 6: Parite .sh (classeur) ---"
RESULT=$(bash "$OUTIL_SH" sidentifier 2>&1)
echo "$RESULT"
RESULT2=$(bash "$OUTIL_SH" activer session-llm-1 Themis "Parite sh v031" 2>&1)
echo "$RESULT2"
LIGNE=$(grep '^| `profil-session-llm-1`' "$CLASSEUR_STOCKAGE" | head -1)
if echo "$LIGNE" | grep -q 'agent: Themis'; then
    echo "[OK] Test 6 passe (version .sh ecrit le classeur)"
    result6=0
else
    echo "[ERREUR] Test 6 echoue"
    result6=1
fi

# ---------------------------------------------------------------------
# Test 7: VERIFICATION NEGATIVE - aucune ligne profil-session-session-*
# ---------------------------------------------------------------------
echo "--- Test 7: Aucune ligne double-session creee ---"
preparer_ancienne_structure
python3 "$OUTIL_PY" sidentifier > /dev/null 2>&1
python3 "$OUTIL_PY" activer session-llm-2 Vulcain "Test negatif v032" > /dev/null 2>&1
NB=$(grep -c 'profil-session-session-' "$CLASSEUR_STOCKAGE" || true)
echo "Lignes double-session: $NB"
if [ "$NB" -eq 0 ]; then
    echo "[OK] Test 7 passe (aucune ligne profil-session-session-*)"
    result7=0
else
    echo "[ERREUR] Test 7 echoue"
    result7=1
fi

# ---------------------------------------------------------------------
# Test 8: REGRESSION v0.3.0 -- relance du test-001 (12 cas)
# ---------------------------------------------------------------------
echo "--- Test 7: Regression v0.3.0 (test-001, 12 cas) ---"
unset AGENTS_FILE AGENTS_HISTORIQUE CLASSEUR_STOCKAGE
bash "$(dirname "$0")/test-001-activer-agent-principal.sh" > /tmp/regression-v030.log 2>&1
CODE=$?
tail -5 /tmp/regression-v030.log
rm -f /tmp/regression-v030.log
if [ "$CODE" -eq 0 ]; then
    echo "[OK] Test 8 passe (regression v0.3.0: 12/12)"
    result8=0
else
    echo "[ERREUR] Test 8 echoue (code $CODE)"
    result8=1
fi

# ---------------------------------------------------------------------
# Nettoyage + rapport final
# ---------------------------------------------------------------------
rm -rf "$ESPACE"

echo ""
echo "=== Rapport ==="
total=8
passed=0
for i in 1 2 3 4 5 6 7 8; do
    eval "r=\$result$i"
    if [ "$r" -eq 0 ]; then
        passed=$((passed + 1))
    fi
done
echo "Total: $total"
echo "Reussis: $passed"
echo "Echecs: $((total - passed))"

if command -v generer_rapport > /dev/null 2>&1; then
    generer_rapport "activer-agent-principal-v0.3.1" $total $passed $((total - passed))
fi

[ $((total - passed)) -eq 0 ] && exit 0 || exit 1
