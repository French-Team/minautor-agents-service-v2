#!/bin/bash
# test-006-activer-agent-principal-v040.sh
# Tests formels v0.4.0 : REGLE ALIGNEMENT - id llm-N -> session-llm-N (le numero de session
# porte le numero de l'id), champ **Id LLM** dans les blocs AGENTS.md (reconnaissance par
# lecture), SOURCE DOUBLE (AGENTS.md champ Id LLM + classeur), CONFLIT si session-llm-N
# deja liee a un autre id, ABSORPTION d'une session-llm-N orpheline (sans id).
# + regressions v0.3.5 (liaison preservee), v0.3.4 (MODE ID), v0.3.3, v0.3.2, v0.3.0

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
ESPACE="/tmp/test-activer-agent-v040"
AGENTS_FILE="$ESPACE/AGENTS.md"
AGENTS_HISTORIQUE="$ESPACE/AGENTS-historique.md"
CLASSEUR_STOCKAGE="$ESPACE/variables-actuelles.md"
export AGENTS_FILE AGENTS_HISTORIQUE CLASSEUR_STOCKAGE

NB_OK=0
NB_ECHEC=0

# Extraire le champ Id LLM du bloc d'une session
id_llm_session() {
    awk -v cible="$1" '
        /^### Session : / {
            s = $0
            sub(/^### Session : /, "", s)
            if (s == cible) { dans = 1 } else { dans = 0 }
            next
        }
        dans == 1 && /^\| \*\*Id LLM\*\* \| / {
            ligne = $0
            sub(/^\| \*\*Id LLM\*\* \| /, "", ligne)
            sub(/ \|$/, "", ligne)
            print ligne
            exit
        }
    ' "$AGENTS_FILE"
}

check() {
    local description="$1"
    if [ "$2" = "0" ]; then
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
echo "=== TEST 006 -- REGLE ALIGNEMENT (v0.4.0) ==="
echo ""

# --- Test 1 : id llm-1 inconnu -> session-llm-1 (ALIGNE sur l'id) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier llm-1 > "$ESPACE/sortie1.txt" 2>&1
grep -q '^### Session : session-llm-1$' "$AGENTS_FILE"
check "1. sidentifier llm-1 -> session-llm-1 (alignement)" $?
grep -q 'alignee sur l.id' "$ESPACE/sortie1.txt"
check "1b. Message 'alignee sur l.id'" $?
ID1=$(id_llm_session session-llm-1)
[ "$ID1" = "llm-1" ]
check "1c. Champ **Id LLM** = llm-1 dans le bloc (lu=$ID1)" $?

# --- Test 2 : id llm-2 inconnu -> session-llm-2 (pas prochaine libre) ---
python3 "$OUTIL_PY" sidentifier llm-2 > "$ESPACE/sortie2.txt" 2>&1
grep -q '^### Session : session-llm-2$' "$AGENTS_FILE"
check "2. sidentifier llm-2 -> session-llm-2 (alignement)" $?
ID2=$(id_llm_session session-llm-2)
[ "$ID2" = "llm-2" ]
check "2b. Champ **Id LLM** = llm-2 dans le bloc llm-2 (lu=$ID2)" $?

# --- Test 3 : redemarrage llm-1 -> retrouve session-llm-1 (SOURCE DOUBLE AGENTS.md) ---
python3 "$OUTIL_PY" sidentifier llm-1 > "$ESPACE/sortie3.txt" 2>&1
grep -q 'Session retrouvee pour id llm-1' "$ESPACE/sortie3.txt"
check "3. Redemarrage llm-1 -> 'Session retrouvee' (source AGENTS.md)" $?
NB3=$(grep -c '^### Session :' "$AGENTS_FILE")
[ "$NB3" = "2" ]
check "3b. Toujours 2 blocs (pas de doublon, lu=$NB3)" $?

# --- Test 4 : CONFLIT - session-llm-N deja liee a un AUTRE id -> prochaine libre ---
preparer_vide
cat > "$AGENTS_FILE" << 'EOF'
# Agents du Cerveau-Projet

---

## Sessions LLM

### Session : session-llm-2

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus |
| **Id LLM** | llm-9 |
| **Role** | Gardien |
| **Raison** | - |

---
EOF
python3 "$OUTIL_PY" sidentifier llm-2 > "$ESPACE/sortie4.txt" 2>&1
grep -q 'ATTENTION' "$ESPACE/sortie4.txt"
check "4. CONFLIT: session-llm-2 liee a llm-9 -> 'ATTENTION'" $?
if grep -q 'session-llm-1' "$ESPACE/sortie4.txt" || grep -q 'session-llm-3' "$ESPACE/sortie4.txt"; then
    check "4b. Session attribuee differente de session-llm-2 (prochaine libre)" 0
else
    check "4b. Session attribuee differente de session-llm-2 (prochaine libre)" 1
fi

# --- Test 5 : ABSORPTION - session-llm-N orpheline (sans id) -> llm-N l'absorbe ---
preparer_vide
cat > "$AGENTS_FILE" << 'EOF'
# Agents du Cerveau-Projet

---

## Sessions LLM

### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus |
| **Role** | Gardien |
| **Raison** | bloc orphelin sans Id LLM |

---
EOF
python3 "$OUTIL_PY" sidentifier llm-1 > "$ESPACE/sortie5.txt" 2>&1
grep -q 'Nouvelle session pour id llm-1' "$ESPACE/sortie5.txt"
check "5. ABSORPTION: session-llm-1 orpheline -> llm-1 l'absorbe" $?
ID5=$(id_llm_session session-llm-1)
[ "$ID5" = "llm-1" ]
check "5b. Le bloc session-llm-1 porte maintenant **Id LLM** = llm-1 (lu=$ID5)" $?

# --- Test 6 : id NON numerique (llm-atlas) -> prochaine libre (pas d'alignement) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier llm-atlas > "$ESPACE/sortie6.txt" 2>&1
grep -q '^### Session : session-llm-1$' "$AGENTS_FILE"
check "6. llm-atlas (non numerique) -> session-llm-1 (prochaine libre)" $?
ID6=$(id_llm_session session-llm-1)
[ "$ID6" = "llm-atlas" ]
check "6b. Champ **Id LLM** = llm-atlas (lu=$ID6)" $?

# --- Test 7 : parite .sh (alignement + champ Id LLM) ---
preparer_vide
bash "$OUTIL_SH" sidentifier llm-3 > "$ESPACE/sortie7.txt" 2>&1
grep -q '^### Session : session-llm-3$' "$AGENTS_FILE"
check "7. Parite .sh: llm-3 -> session-llm-3 (alignement)" $?
ID7=$(id_llm_session session-llm-3)
[ "$ID7" = "llm-3" ]
check "7b. Parite .sh: champ **Id LLM** = llm-3 (lu=$ID7)" $?
bash "$OUTIL_SH" sidentifier llm-3 > "$ESPACE/sortie7b.txt" 2>&1
grep -q 'Session retrouvee pour id llm-3' "$ESPACE/sortie7b.txt"
check "7c. Parite .sh: redemarrage -> 'Session retrouvee'" $?

# --- Test 8 : regression v0.3.5 (liaison id PRESERVEE par activer/reactiver) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier llm-1 > /dev/null 2>&1
python3 "$OUTIL_PY" activer session-llm-1 vulcain "Test reg v035" > /dev/null 2>&1
ID8=$(id_llm_session session-llm-1)
[ "$ID8" = "llm-1" ]
check "8. Regression v0.3.5: activer PRESERVE **Id LLM** = llm-1 (bloc, lu=$ID8)" $?
grep 'profil-session-llm-1' "$CLASSEUR_STOCKAGE" | grep -q 'id: llm-1'
check "8b. Regression v0.3.5: activer PRESERVE id: llm-1 (classeur)" $?
python3 "$OUTIL_PY" reactiver session-llm-1 "Fin reg v035" vulcain > /dev/null 2>&1
ID8c=$(id_llm_session session-llm-1)
[ "$ID8c" = "llm-1" ]
check "8c. Regression v0.3.5: reactiver PRESERVE **Id LLM** = llm-1 (lu=$ID8c)" $?
grep 'profil-session-llm-1' "$CLASSEUR_STOCKAGE" | grep -q 'id: llm-1'
check "8d. Regression v0.3.5: reactiver PRESERVE id: llm-1 (classeur)" $?

# --- Test 9 : regression v0.3.4 (MODE ID - 2 ids differents isoles) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier llm-atlas > /dev/null 2>&1
python3 "$OUTIL_PY" sidentifier llm-athena > /dev/null 2>&1
NB9=$(grep -c '^### Session :' "$AGENTS_FILE")
[ "$NB9" = "2" ]
check "9. Regression v0.3.4: 2 ids non numeriques -> 2 sessions isolees (lu=$NB9)" $?
grep 'profil-session-llm-1' "$CLASSEUR_STOCKAGE" | grep -q 'id: llm-atlas' && grep 'profil-session-llm-2' "$CLASSEUR_STOCKAGE" | grep -q 'id: llm-athena'
check "9b. Isolation: llm-atlas = llm-1, llm-athena = llm-2" $?

# --- Test 10 : regression v0.3.3 (sans argument -> prochaine libre, pas de liaison) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier > /dev/null 2>&1
python3 "$OUTIL_PY" sidentifier > /dev/null 2>&1
grep -q '^### Session : session-llm-1$' "$AGENTS_FILE" && grep -q '^### Session : session-llm-2$' "$AGENTS_FILE"
check "10. Regression v0.3.3: sans argument 2x -> llm-1 puis llm-2" $?
NB10=$(grep -c '| \*\*Id LLM\*\* |' "$AGENTS_FILE"); NB10=${NB10:-0}
[ "$NB10" = "0" ]
check "10b. Sans argument -> AUCUN champ **Id LLM** (pas de liaison, lu=$NB10)" $?

# --- Test 11 : regression v0.3.2 (regle derivation profil-session) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier llm-cerberus > /dev/null 2>&1
grep -q 'profil-session-llm-1' "$CLASSEUR_STOCKAGE"
check "11. Regression v0.3.2: ligne profil-session-llm-1 (derivation)" $?
NB11=$(grep -c 'profil-session-session-' "$CLASSEUR_STOCKAGE" 2>/dev/null); NB11=${NB11:-0}
[ "$NB11" = "0" ]
check "11b. AUCUNE ligne profil-session-session-* (lu=$NB11)" $?

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
