#!/bin/bash
# test-005-activer-agent-principal-v035.sh
# Tests formels v0.3.5 : CORRECTION BUG MAJEUR - la liaison id<->session posee par
# sidentifier etait ECRASEE par activer/reactiver (mettre_a_jour_profil_session sans
# llm_id reecrivait la ligne sans le champ id) -> sessions fantomes au redemarrage.
# Test : la liaison id est PRESERVEE a travers activer/reactiver, et un redemarrage
# (meme id) retrouve SA session sans creer de nouveau bloc.
# + regression v0.3.4 (MODE ID), v0.3.3 (attribution libre), v0.3.2 (derivation)

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
ESPACE="/tmp/test-activer-agent-v035"
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

ligne_profil() {
    grep "profil-session-llm-1" "$CLASSEUR_STOCKAGE"
}

# ===========================================================================
echo "=== TEST 005 -- LIAISON ID PRESERVEE (v0.3.5) ==="
echo ""

# --- Test 1 : sidentifier pose la liaison id ---
preparer_vide
SORTIE=$(python3 "$OUTIL_PY" sidentifier llm-atlas 2>&1)
verifier "1. sidentifier llm-atlas -> cree session-llm-1" \
    "grep -q '^### Session : session-llm-1\$' '$AGENTS_FILE'"
verifier "1b. Ligne profil contient id: llm-atlas (liaison posee)" \
    "ligne_profil | grep -q 'id: llm-atlas'"

# --- Test 2 : BUG -- activer ECRASAIT la liaison (corrige v0.3.5) ---
SORTIE=$(python3 "$OUTIL_PY" activer session-llm-1 vulcain "Test liaison v035" 2>&1)
verifier "2. activer vulcain -> OK (sortie succes)" \
    "echo \"\$SORTIE\" | grep -q 'active avec succes'"
verifier "2b. CORRIGE: ligne profil garde id: llm-atlas apres activer" \
    "ligne_profil | grep -q 'id: llm-atlas'"
verifier "2c. Ligne profil agent = vulcain" \
    "ligne_profil | grep -q 'agent: vulcain'"

# --- Test 3 : BUG -- reactiver ECRASAIT la liaison (corrige v0.3.5) ---
SORTIE=$(python3 "$OUTIL_PY" reactiver session-llm-1 "Test fin v035" vulcain 2>&1)
verifier "3. reactiver Cerberus -> OK (sortie succes)" \
    "echo \"\$SORTIE\" | grep -q 'reactive avec succes'"
verifier "3b. CORRIGE: ligne profil garde id: llm-atlas apres reactiver" \
    "ligne_profil | grep -q 'id: llm-atlas'"
verifier "3c. Ligne profil agent = Cerberus" \
    "ligne_profil | grep -q 'agent: Cerberus'"

# --- Test 4 : redemarrage (meme id) -> retrouve SA session (PAS de fantome) ---
SORTIE=$(python3 "$OUTIL_PY" sidentifier llm-atlas 2>&1)
verifier "4. Redemarrage llm-atlas -> 'Session retrouvee'" \
    "echo \"\$SORTIE\" | grep -q 'Session retrouvee pour id llm-atlas'"
verifier "4b. Toujours 1 seul bloc session (pas de session fantome)" \
    "[ \"\$(grep -c '^### Session :' '$AGENTS_FILE')\" = '1' ]"
verifier "4c. Toujours 1 seule ligne profil (pas de doublon)" \
    "[ \"\$(grep -c 'profil-session-llm-1' '$CLASSEUR_STOCKAGE')\" = '1' ]"
verifier "4d. Ligne profil garde id: llm-atlas apres redemarrage" \
    "ligne_profil | grep -q 'id: llm-atlas'"

# --- Test 5 : cycle complet py -> aucune session fantome ---
verifier "5. Cycle sidentifier+activer+reactiver+sidentifier : 1 seul bloc" \
    "[ \"\$(grep -c '^### Session :' '$AGENTS_FILE')\" = '1' ]"
verifier "5b. Une seule ligne profil llm-1" \
    "[ \"\$(grep -c 'profil-session-llm-1' '$CLASSEUR_STOCKAGE')\" = '1' ]"

# --- Test 6 : deux LLM, liaison isolee apres cycles ---
SORTIE=$(python3 "$OUTIL_PY" sidentifier llm-athena 2>&1)
verifier "6. 2e LLM llm-athena -> cree session-llm-2" \
    "grep -q '^### Session : session-llm-2\$' '$AGENTS_FILE'"
python3 "$OUTIL_PY" activer session-llm-2 morpheus "Test 2e LLM" > /dev/null 2>&1
python3 "$OUTIL_PY" reactiver session-llm-2 "Fin 2e LLM" morpheus > /dev/null 2>&1
verifier "6b. Liaison llm-atlas intacte sur sa ligne" \
    "grep 'profil-session-llm-1' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-atlas'"
verifier "6c. Liaison llm-athena presente sur SA ligne" \
    "grep 'profil-session-llm-2' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-athena'"
verifier "6d. Deux blocs sessions distincts (isolation)" \
    "[ \"\$(grep -c '^### Session :' '$AGENTS_FILE')\" = '2' ]"

# --- Test 7 : parite .sh ---
preparer_vide
SORTIE_SH=$(bash "$OUTIL_SH" sidentifier llm-buffy 2>&1)
verifier "7. Parite .sh: sidentifier llm-buffy -> session-llm-1 + liaison" \
    "grep 'profil-session-llm-1' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-buffy'"
bash "$OUTIL_SH" activer session-llm-1 vulcain "Test sh v035" > /dev/null 2>&1
verifier "7b. Parite .sh: liaison PRESERVEE apres activer" \
    "grep 'profil-session-llm-1' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-buffy'"
bash "$OUTIL_SH" reactiver session-llm-1 "Fin sh v035" vulcain > /dev/null 2>&1
verifier "7c. Parite .sh: liaison PRESERVEE apres reactiver" \
    "grep 'profil-session-llm-1' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-buffy'"
SORTIE_SH=$(bash "$OUTIL_SH" sidentifier llm-buffy 2>&1)
verifier "7d. Parite .sh: redemarrage -> 'Session retrouvee'" \
    "echo \"\$SORTIE_SH\" | grep -q 'Session retrouvee pour id llm-buffy'"
verifier "7e. Parite .sh: 1 seul bloc (pas de fantome)" \
    "[ \"\$(grep -c '^### Session :' '$AGENTS_FILE')\" = '1' ]"

# --- Test 8 : regression v0.3.4 (MODE ID) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier llm-atlas > /dev/null 2>&1
python3 "$OUTIL_PY" sidentifier llm-athena > /dev/null 2>&1
verifier "8. Regression v0.3.4: 2 ids inconnus -> 2 sessions isolees" \
    "[ \"\$(grep -c '^### Session :' '$AGENTS_FILE')\" = '2' ]"
SORTIE=$(python3 "$OUTIL_PY" sidentifier llm-atlas 2>&1)
verifier "8b. Regression v0.3.4: redemarrage llm-atlas -> retrouve SA session" \
    "echo \"\$SORTIE\" | grep -q 'Session retrouvee pour id llm-atlas'"

# --- Test 9 : regression v0.3.3 (attribution prochaine libre sans argument) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier > /dev/null 2>&1
python3 "$OUTIL_PY" sidentifier > /dev/null 2>&1
verifier "9. Regression v0.3.3: sans argument 2x -> llm-1 puis llm-2" \
    "grep -q '^### Session : session-llm-1\$' '$AGENTS_FILE' && grep -q '^### Session : session-llm-2\$' '$AGENTS_FILE'"

# --- Test 10 : regression v0.3.2 (regle derivation profil-session) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier llm-cerberus > /dev/null 2>&1
verifier "10. Regression v0.3.2: ligne profil-session-llm-1 (regle derivation)" \
    "grep -q 'profil-session-llm-1' '$CLASSEUR_STOCKAGE'"
verifier "10b. AUCUNE ligne profil-session-session-*" \
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
