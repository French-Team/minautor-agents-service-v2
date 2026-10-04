#!/bin/bash
# test-007-activer-agent-principal-v050.sh
# Tests formels v0.5.0 : CONVENTION IDENTIFICATION - aucun mot seul.
#   - Bloc de session : **Nom LLM** (id) EN TETE, **Nom Agent** au lieu de **Nom**,
#     **Role Agent** au lieu de **Role**
#   - Migration automatique des anciens blocs (Nom/Role/Id LLM) lors de chaque edition
#   - Table Sessions connues : colonne **Nom LLM**
# + regressions v0.4.0 (alignement, source double, conflit) et v0.3.5 (liaison preservee)

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
ESPACE="/tmp/test-activer-agent-v050"
AGENTS_FILE="$ESPACE/AGENTS.md"
AGENTS_HISTORIQUE="$ESPACE/AGENTS-historique.md"
CLASSEUR_STOCKAGE="$ESPACE/variables-actuelles.md"
export AGENTS_FILE AGENTS_HISTORIQUE CLASSEUR_STOCKAGE

NB_OK=0
NB_ECHEC=0

# Extraire le champ Nom LLM du bloc d'une session (repli sur l'ancien **Id LLM**)
id_llm_session() {
    awk -v cible="$1" '
        /^### Session : / {
            s = $0
            sub(/^### Session : /, "", s)
            if (s == cible) { dans = 1 } else { dans = 0 }
            next
        }
        dans == 1 && /^\| \*\*(Nom LLM|Id LLM)\*\* \| / {
            ligne = $0
            sub(/^\| \*\*(Nom LLM|Id LLM)\*\* \| /, "", ligne)
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
echo "=== TEST 007 -- CONVENTION IDENTIFICATION (v0.5.0) ==="
echo ""

# --- Test 1 : nouveau bloc en format v0.5.0 (Nom LLM en tete, Nom Agent, Role Agent) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier llm-1 > /dev/null 2>&1
grep -q '^| \*\*Nom LLM\*\* | llm-1 |$' "$AGENTS_FILE"
check "1. Nouveau bloc : champ **Nom LLM** = llm-1" $?
grep -q '^| \*\*Nom Agent\*\* | Cerberus |$' "$AGENTS_FILE"
check "1b. Nouveau bloc : champ **Nom Agent** = Cerberus" $?
grep -q '^| \*\*Role Agent\*\* |' "$AGENTS_FILE"
check "1c. Nouveau bloc : champ **Role Agent** present" $?
if grep -q '^| \*\*Nom\*\* |' "$AGENTS_FILE"; then
    check "1d. AUCUN champ **Nom** seul (lu=$(grep -c '^| \*\*Nom\*\* |' "$AGENTS_FILE"))" 1
else
    check "1d. AUCUN champ **Nom** seul (lu=0)" 0
fi
if grep -q '^| \*\*Role\*\* |' "$AGENTS_FILE"; then
    check "1e. AUCUN champ **Role** seul" 1
else
    check "1e. AUCUN champ **Role** seul" 0
fi

# --- Test 2 : Nom LLM en TETE du bloc (avant Nom Agent) ---
NBL=$(grep -n '^| \*\*Nom LLM\*\* |' "$AGENTS_FILE" | head -1 | cut -d: -f1)
NBA=$(grep -n '^| \*\*Nom Agent\*\* |' "$AGENTS_FILE" | head -1 | cut -d: -f1)
if [ -n "$NBL" ] && [ -n "$NBA" ] && [ "$NBL" -lt "$NBA" ]; then
    check "2. **Nom LLM** ligne $NBL AVANT **Nom Agent** ligne $NBA" 0
else
    check "2. **Nom LLM** AVANT **Nom Agent** (lignes $NBL / $NBA)" 1
fi

# --- Test 3 : MIGRATION d'un ancien bloc (Nom/Role/Id LLM) par activer ---
preparer_vide
cat > "$AGENTS_FILE" << 'EOF'
# Agents du Cerveau-Projet

---

## Sessions LLM

### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus |
| **Id LLM** | llm-1 |
| **Role** | Gardien |
| **Raison** | ancien format |

---
EOF
python3 "$OUTIL_PY" activer session-llm-1 buffy "Migration v050" > /dev/null 2>&1
grep -q '^| \*\*Nom LLM\*\* | llm-1 |$' "$AGENTS_FILE"
check "3. Migration : **Id LLM** -> **Nom LLM** = llm-1" $?
grep -q '^| \*\*Nom Agent\*\* | buffy |$' "$AGENTS_FILE"
check "3b. Migration : **Nom** -> **Nom Agent** = buffy" $?
grep -q '^| \*\*Role Agent\*\* | Developpeur' "$AGENTS_FILE"
check "3c. Migration : **Role** -> **Role Agent**" $?
NB=$(grep -c -e '^| \*\*Nom\*\* |' -e '^| \*\*Role\*\* |' -e '^| \*\*Id LLM\*\* |' "$AGENTS_FILE")
[ "$NB" = "0" ]
check "3d. Aucun ancien champ restant (lu=$NB)" $?
# Nom LLM en tete apres migration
NBL=$(grep -n '^| \*\*Nom LLM\*\* |' "$AGENTS_FILE" | head -1 | cut -d: -f1)
NBA=$(grep -n '^| \*\*Nom Agent\*\* |' "$AGENTS_FILE" | head -1 | cut -d: -f1)
if [ -n "$NBL" ] && [ -n "$NBA" ] && [ "$NBL" -lt "$NBA" ]; then
    check "3e. Apres migration, **Nom LLM** reste EN TETE" 0
else
    check "3e. Apres migration, **Nom LLM** reste EN TETE (lignes $NBL / $NBA)" 1
fi

# --- Test 4 : PARITE .sh (migration d'un ancien bloc) ---
preparer_vide
cat > "$AGENTS_FILE" << 'EOF'
# Agents du Cerveau-Projet

---

## Sessions LLM

### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus |
| **Id LLM** | llm-2 |
| **Role** | Gardien |

---
EOF
bash "$OUTIL_SH" activer session-llm-1 clio "Parite sh v050" > /dev/null 2>&1
grep -q '^| \*\*Nom LLM\*\* | llm-2 |$' "$AGENTS_FILE"
check "4. Parite .sh : migration **Nom LLM** = llm-2" $?
grep -q '^| \*\*Nom Agent\*\* | clio |$' "$AGENTS_FILE"
check "4b. Parite .sh : **Nom Agent** = clio" $?
grep -q '^| \*\*Role Agent\*\* |' "$AGENTS_FILE"
check "4c. Parite .sh : **Role Agent** present" $?

# --- Test 5 : reactiver migre aussi + garde Nom LLM ---
python3 "$OUTIL_PY" reactiver session-llm-1 "Fin mission" clio > /dev/null 2>&1
ID=$(id_llm_session session-llm-1)
[ "$ID" = "llm-2" ]
check "5. Reactiver (py) : **Nom LLM** = llm-2 preserve (lu=$ID)" $?
grep -q '^| \*\*Nom Agent\*\* | Cerberus |$' "$AGENTS_FILE"
check "5b. Reactiver (py) : **Nom Agent** = Cerberus" $?

# --- Test 6 : table Sessions connues avec colonne **Nom LLM** ---
grep -q '^| Session | Nom LLM | Agent actif | Derniere activite |$' "$AGENTS_FILE"
check "6. Table Sessions connues : colonne **Nom LLM**" $?
if grep -q '^| Session | Id LLM |' "$AGENTS_FILE"; then
    check "6b. AUCUNE colonne **Id LLM** dans la table" 1
else
    check "6b. AUCUNE colonne **Id LLM** dans la table" 0
fi

# --- Test 7 : regression v0.4.0 (alignement + source double AGENTS.md) ---
preparer_vide
python3 "$OUTIL_PY" sidentifier llm-3 > /dev/null 2>&1
grep -q '^### Session : session-llm-3$' "$AGENTS_FILE"
check "7. Regression v0.4.0 : llm-3 -> session-llm-3" $?
python3 "$OUTIL_PY" sidentifier llm-3 > /dev/null 2>&1
ID7=$(id_llm_session session-llm-3)
[ "$ID7" = "llm-3" ]
check "7b. Regression v0.4.0 : redemarrage retrouve **Nom LLM** = llm-3 (lu=$ID7)" $?

# --- Test 8 : regression v0.3.5 (liaison preservee par activer/reactiver) ---
python3 "$OUTIL_PY" activer session-llm-3 vulcain "Test reg v035" > /dev/null 2>&1
ID8=$(id_llm_session session-llm-3)
[ "$ID8" = "llm-3" ]
check "8. Regression v0.3.5 : activer PRESERVE **Nom LLM** = llm-3 (lu=$ID8)" $?
grep 'profil-session-llm-3' "$CLASSEUR_STOCKAGE" | grep -q 'id: llm-3'
check "8b. Regression v0.3.5 : activer PRESERVE id: llm-3 (classeur)" $?

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
