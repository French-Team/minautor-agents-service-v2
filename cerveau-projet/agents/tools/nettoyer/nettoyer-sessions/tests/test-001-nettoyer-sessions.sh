#!/bin/bash
# test-001-nettoyer-sessions.sh
# Tests formels v0.1.2 : nettoyer-sessions
# Perimetre (decision utilisateur - etats actifs uniquement) :
#   - AGENTS.md          : blocs '### Session : session-llm-N' + section '## Sessions connues'
#   - classeur-variables : lignes 'profil-session-*'
# Preserve : frontmatter, en-tete '## Sessions LLM', Configuration Active, Liste des agents.
# v0.1.2 : l'en-tete '## Sessions LLM' est PRESERVE (bug sidentifier corrige) - tests 4b + 7c/7d/7e.
# AGENTS-historique.md (le journal) JAMAIS modifie.
# Tests sur COPIES : variables AGENTS_FILE + CLASSEUR_STOCKAGE redirigees.

# --- Protections -----------------------------------------------------------
PROTECTIONS_DIR="$(cd "$(dirname "$0")/../../../tester/protections" 2>/dev/null && pwd)"
if [ -z "$PROTECTIONS_DIR" ] || [ ! -d "$PROTECTIONS_DIR" ]; then
    PROTECTIONS_DIR="$(dirname "$0")/../../../tester/protections"
fi

source "$PROTECTIONS_DIR/tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh"
source "$PROTECTIONS_DIR/tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh"
source "$PROTECTIONS_DIR/tester-protection-blocage/tester-protection-blocage.sh"

OUTIL_PY="$(cd "$(dirname "$0")/.." && pwd)/nettoyer-sessions.py"
OUTIL_SH="$(cd "$(dirname "$0")/.." && pwd)/nettoyer-sessions.sh"
# Zone temporaire DANS le workspace (regle immuable regles-perimetre-workspace)
RACINE="$(cd "$(dirname "$0")/../../../../../.." && pwd)"
ESPACE="$RACINE/.tmp-test-nettoyer-sessions"

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

# Creer les fichiers de test (imitation de la structure reelle)
preparer() {
    local espace="$1"
    rm -rf "$espace"
    mkdir -p "$espace"

    cat > "$espace/AGENTS.md" << 'EOF'
---
identite:
  type: racine
  appartient_a: commun
  commun: true
---

# Agents du Cerveau-Projet

---

## Sessions LLM

### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom LLM** | llm-1 |
| **Nom Agent** | Cerberus |
| **Role Agent** | Gardien de l'entree |
| **Derniere mise a jour** | 2026-08-08 |
| **Fiche** | [fiche](chemin) |
| **Corrections** | [corrections](chemin) |
| **Active par** | identification |
| **Raison** | identification LLM |

---

### Session : session-llm-2

| Champ | Valeur |
|---|---|
| **Nom LLM** | llm-2 |
| **Nom Agent** | Buffy |
| **Role Agent** | Developpeur principal |
| **Derniere mise a jour** | 2026-08-08 |
| **Fiche** | [fiche](chemin) |
| **Corrections** | [corrections](chemin) |
| **Active par** | identification |
| **Raison** | identification LLM |

---

## Sessions connues

| Session | Nom LLM | Agent |
|---|---|---|
| session-llm-1 | llm-1 | Cerberus |
| session-llm-2 | llm-2 | Buffy |

---

## Liste des agents

| Agent | Role |
|---|---|
| Cerberus | Gardien |

---

## Configuration Active

### Regles specifiques a Cerberus

1. **Ecouter avant de decider**

---
EOF

    cat > "$espace/classeur.md" << 'EOF'
---
identite:
  type: classeur
  appartient_a: commun
  commun: true
---

# Stockage -- Variables Actuelles

---

## Variables

| Variable | Valeur | Source | Date | Statut |
|---|---|---|---|---|
| `profil-systeme` | OS: Windows | verifier-systeme | 2026-08-07 | [OK] |
| `profil-session-llm-1` | session: session-llm-1 / agent: Cerberus | activer-agent-principal | 2026-08-08 | [OK] |
| `profil-session-llm-2` | session: session-llm-2 / agent: Buffy | activer-agent-principal | 2026-08-08 | [OK] |

---

## Fin

---
EOF

    cat > "$espace/historique.md" << 'EOF'
# Historique des Agents

---

| Date | Session | Agent | Action |
|---|---|---|---|
| 2026-08-08 | session-llm-1 | Cerberus | identification |

---
EOF
}

# ===========================================================================
echo "=== TEST 001 -- NETTOYER-SESSIONS v0.1.2 (etats actifs uniquement) ==="
echo ""

# --- Test 1 : compilation + version ---
verifier "1. py_compile OK" \
    "python3 -m py_compile '$OUTIL_PY' 2>&1"
verifier "1b. bash -n OK" \
    "bash -n '$OUTIL_SH' 2>&1"
PY_VERSION=$(python3 "$OUTIL_PY" --version 2>&1)
SH_VERSION=$(bash "$OUTIL_SH" --version 2>&1)
verifier "2. --version py = v0.1.2" \
    "[ \"\$PY_VERSION\" = 'nettoyer-sessions v0.1.2 (prepare)' ]"
verifier "2b. --version sh = identique a py" \
    "[ \"\$PY_VERSION\" = \"\$SH_VERSION\" ]"

# --- Test 3 : dry-run ne modifie rien ---
preparer "$ESPACE"
cp "$ESPACE/AGENTS.md" "$ESPACE/AGENTS.avant"
cp "$ESPACE/classeur.md" "$ESPACE/classeur.avant"
SORTIE_DRY=$(AGENTS_FILE="$ESPACE/AGENTS.md" CLASSEUR_STOCKAGE="$ESPACE/classeur.md" python3 "$OUTIL_PY" --dry-run 2>&1)
verifier "3. dry-run: message [DRY-RUN] AGENTS.md" \
    "echo \"\$SORTIE_DRY\" | grep -q 'DRY-RUN'"
verifier "3b. dry-run: aucun fichier modifie (AGENTS identique)" \
    "diff -q '$ESPACE/AGENTS.md' '$ESPACE/AGENTS.avant' >/dev/null"
verifier "3c. dry-run: aucun fichier modifie (classeur identique)" \
    "diff -q '$ESPACE/classeur.md' '$ESPACE/classeur.avant' >/dev/null"

# --- Test 4 : execution reelle py ---
SORTIE=$(AGENTS_FILE="$ESPACE/AGENTS.md" CLASSEUR_STOCKAGE="$ESPACE/classeur.md" python3 "$OUTIL_PY" 2>&1)
verifier "4. Nettoyage: blocs ### Session supprimes (0)" \
    "NB=\$(grep -c '^### Session :' '$ESPACE/AGENTS.md' 2>/dev/null); [ \"\$NB\" = '0' ]"
verifier "4b. Nettoyage: en-tete ## Sessions LLM PRESERVE (bug v0.1.2)" \
    "NB=\$(grep -c '^## Sessions LLM\$' '$ESPACE/AGENTS.md' 2>/dev/null); [ \"\$NB\" = '1' ]"
verifier "4c. Nettoyage: section ## Sessions connues supprimee" \
    "NB=\$(grep -c '^## Sessions connues\$' '$ESPACE/AGENTS.md' 2>/dev/null); [ \"\$NB\" = '0' ]"
verifier "4d. Nettoyage: lignes profil-session-* supprimees (0)" \
    "NB=\$(grep -c 'profil-session-' '$ESPACE/classeur.md' 2>/dev/null); [ \"\$NB\" = '0' ]"

# --- Test 5 : preservation ---
verifier "5. frontmatter identite PRESERVE" \
    "grep -q '^identite:' '$ESPACE/AGENTS.md'"
verifier "5b. entete # Agents PRESERVE" \
    "grep -q '^# Agents du Cerveau-Projet' '$ESPACE/AGENTS.md'"
verifier "5c. Configuration Active PRESERVEE" \
    "grep -q '^## Configuration Active' '$ESPACE/AGENTS.md'"
verifier "5d. Liste des agents PRESERVEE" \
    "grep -q '^## Liste des agents' '$ESPACE/AGENTS.md'"
verifier "5e. variable non-session du classeur PRESERVEE (profil-systeme)" \
    "grep -q 'profil-systeme' '$ESPACE/classeur.md'"

# --- Test 6 : AGENTS-historique (le journal) JAMAIS modifie ---
verifier "6. Historique intact (aucune reference session-llm ajoutee/supprimee)" \
    "grep -q 'session-llm-1' '$ESPACE/historique.md'"

# --- Test 7 : idempotence (2e execution = 0 ligne) ---
SORTIE2=$(AGENTS_FILE="$ESPACE/AGENTS.md" CLASSEUR_STOCKAGE="$ESPACE/classeur.md" python3 "$OUTIL_PY" 2>&1)
verifier "7. Idempotence: 2e execution AGENTS.md = 0 ligne" \
    "echo \"\$SORTIE2\" | grep 'AGENTS.md' | grep -q '0 ligne'"
verifier "7b. Idempotence: 2e execution classeur = 0 ligne" \
    "echo \"\$SORTIE2\" | grep 'Classeur' | grep -q '0 ligne'"

# --- Test 7c-7e : INTEGRATION nettoyage -> re-identification (bug v0.1.2) ---
ACTIVER_PY="$RACINE/cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py"
SORTIE_SID=$(AGENTS_FILE="$ESPACE/AGENTS.md" AGENTS_HISTORIQUE="$ESPACE/historique.md" CLASSEUR_STOCKAGE="$ESPACE/classeur.md" python3 "$ACTIVER_PY" sidentifier llm-1 2>&1)
verifier "7c. Integration: sidentifier fonctionne apres nettoyage (bug v0.1.2)" \
    "echo \"\$SORTIE_SID\" | grep -q 'session-llm-1'"
verifier "7d. Integration: bloc session recree par sidentifier" \
    "NB=\$(grep -c '^### Session : session-llm-1' '$ESPACE/AGENTS.md' 2>/dev/null); [ \"\$NB\" = '1' ]"
verifier "7e. Integration: en-tete ## Sessions LLM toujours present apres re-identification" \
    "NB=\$(grep -c '^## Sessions LLM\$' '$ESPACE/AGENTS.md' 2>/dev/null); [ \"\$NB\" = '1' ]"

# --- Test 8 : parite py/sh (fichiers resultants identiques) ---
preparer "$ESPACE/py"
preparer "$ESPACE/sh"
AGENTS_FILE="$ESPACE/py/AGENTS.md" CLASSEUR_STOCKAGE="$ESPACE/py/classeur.md" python3 "$OUTIL_PY" > /dev/null 2>&1
AGENTS_FILE="$ESPACE/sh/AGENTS.md" CLASSEUR_STOCKAGE="$ESPACE/sh/classeur.md" bash "$OUTIL_SH" > /dev/null 2>&1
verifier "8. Parite: AGENTS.md resultant identique py/sh" \
    "diff -q '$ESPACE/py/AGENTS.md' '$ESPACE/sh/AGENTS.md' >/dev/null"
verifier "8b. Parite: classeur resultant identique py/sh" \
    "diff -q '$ESPACE/py/classeur.md' '$ESPACE/sh/classeur.md' >/dev/null"
verifier "8c. Parite: historique jamais touche (identique aux 2 sources)" \
    "diff -q '$ESPACE/py/historique.md' '$ESPACE/sh/historique.md' >/dev/null"

# --- Test 9 : messages de sortie (documentation divergence) ---
verifier "9. Sortie py: message final avec total" \
    "echo \"\$SORTIE\" | grep -q 'Nettoyage termine'"
SH_SORTIE=$(AGENTS_FILE="$ESPACE/sh/AGENTS.md" CLASSEUR_STOCKAGE="$ESPACE/sh/classeur.md" bash "$OUTIL_SH" 2>&1)
verifier "9b. Sortie sh: message final present" \
    "echo \"\$SH_SORTIE\" | grep -q 'Nettoyage termine'"

# --- Test 10 : parite stricte des SORTIES py/sh (le coeur de la correction v0.1.1) ---
preparer "$ESPACE/sortie-py"
preparer "$ESPACE/sortie-sh"
AGENTS_FILE="$ESPACE/sortie-py/AGENTS.md" CLASSEUR_STOCKAGE="$ESPACE/sortie-py/classeur.md" python3 "$OUTIL_PY" > "$ESPACE/sortie-py/out.txt" 2>&1
AGENTS_FILE="$ESPACE/sortie-sh/AGENTS.md" CLASSEUR_STOCKAGE="$ESPACE/sortie-sh/classeur.md" bash "$OUTIL_SH" > "$ESPACE/sortie-sh/out.txt" 2>&1
verifier "10. Parite sorties reelles py/sh (CRLF normalise)" \
    "diff <(tr -d '\\r' < '$ESPACE/sortie-py/out.txt') <(tr -d '\\r' < '$ESPACE/sortie-sh/out.txt') >/dev/null"
verifier "10b. Message final py: Nettoyage termine avec total" \
    "grep -q 'Nettoyage termine : .* lignes supprimees' '$ESPACE/sortie-py/out.txt'"
verifier "10c. Message final sh: Nettoyage termine avec total" \
    "grep -q 'Nettoyage termine : .* lignes supprimees' '$ESPACE/sortie-sh/out.txt'"
verifier "10d. Parite sorties dry-run py/sh (CRLF normalise)" \
    "AGENTS_FILE='$ESPACE/sortie-py/AGENTS.md' CLASSEUR_STOCKAGE='$ESPACE/sortie-py/classeur.md' python3 '$OUTIL_PY' --dry-run > '$ESPACE/sortie-py/dry.txt' 2>&1; AGENTS_FILE='$ESPACE/sortie-sh/AGENTS.md' CLASSEUR_STOCKAGE='$ESPACE/sortie-sh/classeur.md' bash '$OUTIL_SH' --dry-run > '$ESPACE/sortie-sh/dry.txt' 2>&1; diff <(tr -d '\\r' < '$ESPACE/sortie-py/dry.txt') <(tr -d '\\r' < '$ESPACE/sortie-sh/dry.txt') >/dev/null"
verifier "10e. Message dry-run py: Total a supprimer" \
    "grep -q 'Total : .* lignes a supprimer' '$ESPACE/sortie-py/dry.txt'"
verifier "10f. Message dry-run sh: Total a supprimer" \
    "grep -q 'Total : .* lignes a supprimer' '$ESPACE/sortie-sh/dry.txt'"

# --- Test 11 : ASCII du test + des fichiers modifies ---
verifier "11. Fichier de test 100% ASCII" \
    "NB=\$(LC_ALL=C grep -P '[^\\x00-\\x7F]' '$0' 2>/dev/null | wc -l); [ \"\$NB\" = '0' ]"
verifier "11b. AGENTS.md nettoye 100% ASCII" \
    "NB=\$(LC_ALL=C grep -P '[^\\x00-\\x7F]' '$ESPACE/AGENTS.md' 2>/dev/null | wc -l); [ \"\$NB\" = '0' ]"

# --- Nettoyage (regle workspace) ---
rm -rf "$ESPACE"

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
