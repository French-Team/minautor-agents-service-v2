#!/bin/bash
# test-003-activer-agent-principal-v033.sh
# Tests formels v0.3.3 : REGLE UTILISATEUR identification (session vide au demarrage,
# 1er LLM -> llm-1, session occupee -> attribution automatique de la prochaine libre)
# + regression v0.3.2 (profil session classeur)

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
ESPACE="/tmp/test-activer-agent-v033"
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

# Extraire le champ Nom Agent du bloc d'une session (repli sur l'ancien **Nom**)
nom_session() {
    awk -v cible="$1" '
        /^### Session : / {
            if ($0 == ("### Session : " cible)) { dans = 1 } else { dans = 0 }
            next
        }
        dans == 1 && /^\| \*\*(Nom Agent|Nom)\*\* \| / {
            ligne = $0
            sub(/^\| \*\*(Nom Agent|Nom)\*\* \| /, "", ligne)
            sub(/ \|$/, "", ligne)
            print ligne
            exit
        }
    ' "$AGENTS_FILE"
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
echo "=== TEST 003 -- REGLE UTILISATEUR IDENTIFICATION (v0.3.3) ==="
echo ""

# --- Test 1 : fichier VIDE -> sidentifier sans argument -> session-llm-1 ---
preparer_vide
SORTIE=$(python3 "$OUTIL_PY" sidentifier 2>&1)
verifier "1. Fichier vide + sidentifier sans arg -> bloc session-llm-1 cree" \
    "grep -q '^### Session : session-llm-1\$' '$AGENTS_FILE'"
verifier "1b. Fichier vide -> AUCUN autre bloc session" \
    "[ \"\$(grep -c '^### Session :' '$AGENTS_FILE')\" = '1' ]"
verifier "1c. Agent principal du bloc = Cerberus" \
    "[ \"\$(nom_session session-llm-1)\" = 'Cerberus' ]"

# --- Test 2 : llm-1 existe -> sidentifier sans argument -> session-llm-2 ---
SORTIE=$(python3 "$OUTIL_PY" sidentifier 2>&1)
verifier "2. 2e LLM sans argument -> session-llm-2 (pas llm-1)" \
    "grep -q '^### Session : session-llm-2\$' '$AGENTS_FILE'"
verifier "2b. Le bloc llm-1 reste intact" \
    "grep -q '^### Session : session-llm-1\$' '$AGENTS_FILE'"
verifier "2c. La sortie mentionne session-llm-2" \
    "echo \"\$SORTIE\" | grep -q 'session-llm-2'"

# --- Test 3 : MODE ID (v0.3.4+) - id inconnu -> prochaine libre + liaison ---
SORTIE=$(python3 "$OUTIL_PY" sidentifier llm-atlas 2>&1)
verifier "3. sidentifier llm-atlas (id inconnu) -> prochaine libre session-llm-3" \
    "grep -q '^### Session : session-llm-3\$' '$AGENTS_FILE'"
verifier "3b. Message 'Nouvelle session pour id llm-atlas'" \
    "echo \"\$SORTIE\" | grep -q 'Nouvelle session pour id llm-atlas'"
verifier "3c. Liaison id: llm-atlas posee sur la ligne profil llm-3" \
    "grep 'profil-session-llm-3' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-atlas'"
verifier "3d. Le bloc llm-1 n'a pas change (toujours Cerberus)" \
    "[ \"\$(nom_session session-llm-1)\" = 'Cerberus' ]"

# --- Test 4 : MODE ID - redemarrage (meme id) -> retrouve SA session (pas de fantome) ---
SORTIE=$(python3 "$OUTIL_PY" sidentifier llm-atlas 2>&1)
verifier "4. Redemarrage llm-atlas -> 'Session retrouvee'" \
    "echo \"\$SORTIE\" | grep -q 'Session retrouvee pour id llm-atlas'"
verifier "4b. Toujours 3 sessions (aucun nouveau bloc fantome)" \
    "[ \"\$(grep -c '^### Session :' '$AGENTS_FILE')\" = '3' ]"

# --- Test 5 : historique utilise la NOUVELLE session ---
verifier "5. Historique contient session-llm-3 (la session attribuee)" \
    "grep -q 'session-llm-3' '$AGENTS_HISTORIQUE'"
verifier "5b. Historique contient 'Identification LLM - demarrage de session'" \
    "grep -q 'Identification LLM - demarrage de session' '$AGENTS_HISTORIQUE'"

# --- Test 6 : profil-session classeur suit la NOUVELLE session ---
verifier "6. Profil classeur: ligne profil-session-llm-3 creee" \
    "grep -q 'profil-session-llm-3' '$CLASSEUR_STOCKAGE'"
verifier "6b. Profil classeur: agent = Cerberus pour la session attribuee" \
    "grep 'profil-session-llm-3' '$CLASSEUR_STOCKAGE' | grep -q 'agent: Cerberus'"
verifier "6c. Profil classeur: AUCUNE ligne profil-session-session-* (regle derivation)" \
    "grep -c 'profil-session-session-' '$CLASSEUR_STOCKAGE' 2>/dev/null | grep -q '^0$'"

# --- Test 7 : parite .sh (MODE ID) ---
preparer_vide
SORTIE_SH=$(bash "$OUTIL_SH" sidentifier llm-buffy 2>&1)
verifier "7. Parite .sh: id inconnu -> session-llm-1 + liaison id" \
    "grep -q '^### Session : session-llm-1\$' '$AGENTS_FILE' && grep 'profil-session-llm-1' '$CLASSEUR_STOCKAGE' | grep -q 'id: llm-buffy'"
SORTIE_SH=$(bash "$OUTIL_SH" sidentifier llm-buffy 2>&1)
verifier "7b. Parite .sh: relance -> retrouve SA session (pas de doublon)" \
    "echo \"\$SORTIE_SH\" | grep -q 'Session retrouvee pour id llm-buffy'"
verifier "7c. Parite .sh: 1 seul bloc session (aucun fantome)" \
    "[ \"\$(grep -c '^### Session :' '$AGENTS_FILE')\" = '1' ]"

# --- Test 8 : regression v0.3.2 (profil session) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier > /dev/null 2>&1
python3 "$OUTIL_PY" activer session-llm-1 Buffy "Test regression v033" > /dev/null 2>&1
verifier "8. Regression: activer met a jour profil-session-llm-1 (agent Buffy)" \
    "grep 'profil-session-llm-1' '$CLASSEUR_STOCKAGE' | grep -q 'agent: Buffy'"
python3 "$OUTIL_PY" reactiver session-llm-1 "Fin regression" Buffy > /dev/null 2>&1
verifier "8b. Regression: reactiver -> profil agent Cerberus" \
    "grep 'profil-session-llm-1' '$CLASSEUR_STOCKAGE' | grep -q 'agent: Cerberus'"

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
