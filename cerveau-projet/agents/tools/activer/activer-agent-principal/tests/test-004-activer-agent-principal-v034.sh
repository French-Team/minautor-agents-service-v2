#!/bin/bash
# test-004-activer-agent-principal-v034.sh
# Tests formels v0.3.4 : MODE ID (chaque LLM a son id, sidentifier <llm-id> compare
# l'id aux sessions enregistrees - id connu = SA session, id inconnu = prochaine libre + liaison)
# + regression v0.3.3 / v0.3.2

# --- Protections -----------------------------------------------------------
PROTECTIONS_DIR="$(cd "$(dirname "$0")/../../../tester/protections" 2>/dev/null && pwd)"
if [ -z "$PROTECTIONS_DIR" ] || [ ! -d "$PROTECTIONS_DIR" ]; then
    PROTECTIONS_DIR="$(dirname "$0")/../../../tester/protections"
fi

source "$PROTECTIONS_DIR/tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh"
source "$PROTECTIONS_DIR/tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh"
source "$PROTECTIONS_DIR/tester-protection-blocage/tester-protection-blocage.sh"

OUTIL_PY="$(cd "$(dirname "$0")/.." && pwd)/activer-agent-principal.py"
OUTIL_SH="$(cd "$(dirname "$0")/.." && pwd)/activer-agent-principal.sh"
ESPACE="/tmp/test-activer-agent-v034"
export AGENTS_FILE="$ESPACE/AGENTS.md"
export AGENTS_HISTORIQUE="$ESPACE/AGENTS-historique.md"
export CLASSEUR_STOCKAGE="$ESPACE/variables-actuelles.md"

NB_OK=0
NB_ECHEC=0

verifier() {
    local description="$1"
    local condition="$2"
    if eval "$condition"; then
        echo "[OK] $description"
        NB_OK=$((NB_OK + 1))
    else
        echo "[ERREUR] $description"
        NB_ECHEC=$((NB_ECHEC + 1))
    fi
}

preparer_vide() {
    rm -rf "$ESPACE"
    mkdir -p "$ESPACE"
    cat > "$AGENTS_FILE" << 'EOF'
# Agents du Cerveau-Projet

---

## Sessions LLM

---

## Liste des agents

| Agent | Role |
|---|---|
| Cerberus | Gardien |

---
EOF
    cat > "$AGENTS_HISTORIQUE" << 'EOF'
# Historique des Agents

---

---
EOF
    cat > "$CLASSEUR_STOCKAGE" << 'EOF'
# Stockage -- Variables Actuelles

---

## Variables

| Variable | Valeur | Source | Date | Statut |
|---|---|---|---|---|
| `profil-systeme` | OS: Windows | verifier-systeme | 2026-08-07 | [OK] |

---

## Fin

---
EOF
}

# ===========================================================================
echo "=== TEST 004 -- MODE ID (v0.3.4) ==="
echo ""

# --- Test 1 : id inconnu sur fichier vide -> cree session-llm-1 + liaison id ---
preparer_vide
SORTIE=$(python3 "$OUTIL_PY" sidentifier llm-atlas 2>&1)
verifier "1. sidentifier llm-atlas (id inconnu) -> cree session-llm-1" \
    "grep -q '^### Session : session-llm-1\$' '$AGENTS_FILE'"
verifier "1b. Message 'Nouvelle session pour id llm-atlas'" \
    "echo \"\$SORTIE\" | grep -q 'Nouvelle session pour id llm-atlas'"
verifier "1c. Ligne profil contient id: llm-atlas (liaison)" \
    "grep 'profil-session-llm-1' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-atlas'"

# --- Test 2 : meme id relance -> retrouve SA session (pas de doublon) ---
SORTIE=$(python3 "$OUTIL_PY" sidentifier llm-atlas 2>&1)
verifier "2. Meme id relance -> 'Session retrouvee pour id llm-atlas'" \
    "echo \"\$SORTIE\" | grep -q 'Session retrouvee pour id llm-atlas'"
verifier "2b. Meme session session-llm-1 (pas de nouveau bloc)" \
    "[ \"\$(grep -c '^### Session :' '$AGENTS_FILE')\" = '1' ]"
verifier "2c. Une seule ligne profil pour llm-1" \
    "[ \"\$(grep -c 'profil-session-llm-1' '$CLASSEUR_STOCKAGE')\" = '1' ]"

# --- Test 3 : 2e LLM id inconnu -> session-llm-2 + liaison ---
SORTIE=$(python3 "$OUTIL_PY" sidentifier llm-athena 2>&1)
verifier "3. sidentifier llm-athena -> cree session-llm-2" \
    "grep -q '^### Session : session-llm-2\$' '$AGENTS_FILE'"
verifier "3b. Ligne profil llm-2 contient id: llm-athena" \
    "grep 'profil-session-llm-2' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-athena'"

# --- Test 4 : deux LLM differents -> JAMAIS la meme session ---
verifier "4. llm-atlas = session-llm-1, llm-athena = session-llm-2 (isolees)" \
    "grep 'profil-session-llm-1' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-atlas' && grep 'profil-session-llm-2' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-athena'"

# --- Test 5 : redemarrage du 2e LLM (llm-athena) -> retrouve llm-2 ---
SORTIE=$(python3 "$OUTIL_PY" sidentifier llm-athena 2>&1)
verifier "5. Redemarrage llm-athena -> retrouve session-llm-2" \
    "echo \"\$SORTIE\" | grep -q 'Session retrouvee pour id llm-athena'"
verifier "5b. Toujours 2 sessions (pas de doublon)" \
    "[ \"\$(grep -c '^### Session :' '$AGENTS_FILE')\" = '2' ]"

# --- Test 6 : sidentifier SANS argument (compatibilite heritage) ---
SORTIE=$(python3 "$OUTIL_PY" sidentifier 2>&1)
verifier "6. Sans argument -> prochaine libre (session-llm-3)" \
    "grep -q '^### Session : session-llm-3\$' '$AGENTS_FILE'"
verifier "6b. Pas de liaison id (pas de 'id: ' dans la ligne llm-3)" \
    "grep 'profil-session-llm-3' '$CLASSEUR_STOCKAGE' | grep -qv ' id: '"

# --- Test 7 : parite .sh ---
preparer_vide
SORTIE_SH=$(bash "$OUTIL_SH" sidentifier llm-buffy 2>&1)
verifier "7. Parite .sh: id inconnu -> session-llm-1" \
    "grep -q '^### Session : session-llm-1\$' '$AGENTS_FILE'"
verifier "7b. Parite .sh: liaison id dans la ligne profil" \
    "grep 'profil-session-llm-1' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-buffy'"
SORTIE_SH=$(bash "$OUTIL_SH" sidentifier llm-buffy 2>&1)
verifier "7c. Parite .sh: relance -> retrouve session-llm-1" \
    "echo \"\$SORTIE_SH\" | grep -q 'Session retrouvee pour id llm-buffy'"

# --- Test 8 : regression v0.3.3 (attribution prochaine libre sans argument) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier > /dev/null 2>&1
python3 "$OUTIL_PY" sidentifier > /dev/null 2>&1
verifier "8. Regression v0.3.3: sans argument 2x -> llm-1 puis llm-2" \
    "grep -q '^### Session : session-llm-1\$' '$AGENTS_FILE' && grep -q '^### Session : session-llm-2\$' '$AGENTS_FILE'"

# --- Test 9 : regression v0.3.2 (regle derivation profil-session) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier llm-cerberus > /dev/null 2>&1
verifier "9. Regression v0.3.2: ligne profil-session-llm-1 (regle derivation)" \
    "grep -q 'profil-session-llm-1' '$CLASSEUR_STOCKAGE'"
verifier "9b. AUCUNE ligne profil-session-session-*" \
    "grep -c 'profil-session-session-' '$CLASSEUR_STOCKAGE' 2>/dev/null | grep -q '^0$'"

# ===========================================================================
echo ""
echo "=== RESUME ==="
echo "Total: $((NB_OK + NB_ECHEC)) | Reussis: $NB_OK | Echecs: $NB_ECHEC"
if [ "$NB_ECHEC" -eq 0 ]; then
    echo "VERDICT : VALIDE"
else
    echo "VERDICT : A REVOIR"
fi
exit 0
