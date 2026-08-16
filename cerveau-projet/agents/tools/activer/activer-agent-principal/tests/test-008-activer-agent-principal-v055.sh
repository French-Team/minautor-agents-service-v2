#!/bin/bash
# test-008-activer-agent-principal-v055.sh
# Tests formels v0.5.7 : FIX BUG DE RECOLLEMENT (anti-accumulation).
#   - Bug v0.5.4 : reconstruire_bloc faisait une EXCEPTION pour la Raison et
#     RECOLLAIT les anciennes continuations (blocs DEMARRAGE) a chaque nouvelle
#     raison -> AGENTS.md corrompu (21 blocs dupliques, mission egaree).
#   - Fix v0.5.7 : un champ REMPLACE (y compris Raison) ignore son ancienne suite.
# Tests :
#   1. Raison corrompue (3 blocs DEMARRAGE en continuations) -> activer remplace
#      proprement : bloc UNIQUE, plus aucun DEMARRAGE recolle
#   2. Reactiver remplace aussi proprement (la Raison multiligne du bilan est
#      conservee telle quelle, sans accumulation)
#   3. Version v0.5.7 (--version, py + sh)
#   4. Normes : AGENTS.md ASCII + LF
# + regression v0.5.0 (Nom LLM en tete preserve par le fix)

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
ESPACE="/tmp/test-activer-agent-v055"
AGENTS_FILE="$ESPACE/AGENTS.md"
AGENTS_HISTORIQUE="$ESPACE/AGENTS-historique.md"
CLASSEUR_STOCKAGE="$ESPACE/variables-actuelles.md"
export AGENTS_FILE AGENTS_HISTORIQUE CLASSEUR_STOCKAGE

rm -rf "$ESPACE"
mkdir -p "$ESPACE"
cat > "$AGENTS_FILE" << 'EOF'
# Agents du Cerveau-Projet

---

## Sessions LLM

---

## Sessions connues

| Session | Nom LLM | Agent actif | Derniere activite |
|---|---|---|---|
| session-llm-1 | llm-1 | Cerberus | 2026-08-14 00:00 |

## Configuration Active

## Liste des agents
EOF
: > "$AGENTS_HISTORIQUE"
echo "# variables" > "$CLASSEUR_STOCKAGE"

NB_OK=0
NB_ECHEC=0

check() {
    if [ "$2" -eq 0 ]; then
        NB_OK=$((NB_OK + 1))
        echo "  [OK] $1"
    else
        NB_ECHEC=$((NB_ECHEC + 1))
        echo "  [ECHEC] $1"
    fi
}

# Compter les occurrences DEMARRAGE OBLIGATOIRE dans un bloc de session
nb_demarrage() {
    awk -v cible="$1" '
        /^### Session : / {
            s = $0
            sub(/^### Session : /, "", s)
            if (s == cible) { dans = 1 } else { dans = 0 }
            next
        }
        dans == 1 && /^## / { dans = 0 }
        dans == 1 && /DEMARRAGE OBLIGATOIRE/ { cpt++ }
        END { print cpt + 0 }
    ' "$AGENTS_FILE"
}

# Extraire la Raison du bloc (premiere ligne de la cellule)
raison_bloc() {
    awk -v cible="$1" '
        /^### Session : / {
            s = $0
            sub(/^### Session : /, "", s)
            if (s == cible) { dans = 1 } else { dans = 0 }
            next
        }
        dans == 1 && /^\| \*\*Raison\*\* \| / {
            ligne = $0
            sub(/^\| \*\*Raison\*\* \| /, "", ligne)
            sub(/ \|$/, "", ligne)
            print ligne
            dans = 0
        }
    ' "$AGENTS_FILE"
}

echo "=== TEST 008 -- FIX BUG DE RECOLLEMENT (v0.5.7) ==="

# --- Test 1 : version v0.5.7 (py + sh) ---
V_PY=$(python3 "$OUTIL_PY" --version 2>&1 | grep -o 'v0\.5\.7' | head -1)
check "1. --version py = v0.5.7 (lu=$V_PY)" "$([ "$V_PY" = "v0.5.7" ]; echo $?)"
V_SH=$(bash "$OUTIL_SH" --version 2>&1 | grep -o 'v0\.5\.7' | head -1)
check "1b. --version sh = v0.5.7 (lu=$V_SH)" "$([ "$V_SH" = "v0.5.7" ]; echo $?)"

# --- Test 2 : corruption avec 3 blocs DEMARRAGE -> activer remplace proprement ---
# Injecter un bloc session-llm-1 corrompu (Raison + 3 continuations DEMARRAGE)
python3 - "$AGENTS_FILE" <<'PYEOF'
import io, re, sys
f = sys.argv[1]
d = io.open(f, encoding='utf-8').read()
bloc = """### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom LLM** | llm-1 |
| **Nom Agent** | Cerberus |
| **Role Agent** | Gardien |
| **Raison** | ANCIENNE RAISON |

DEMARRAGE OBLIGATOIRE (v0.5.4) : bloc parasite 1
DEMARRAGE OBLIGATOIRE (v0.5.4) : bloc parasite 2
DEMARRAGE OBLIGATOIRE (v0.5.4) : bloc parasite 3
"""
d2 = re.sub(r'### Session : session-llm-1\n.*?(?=## Sessions connues)', bloc, d, flags=re.S)
if d2 == d:
    # si la session n'existe pas encore, l'ajouter avant Sessions connues
    d2 = d.replace('## Sessions connues', bloc + '\n## Sessions connues')
io.open(f, 'w', encoding='utf-8', newline='\n').write(d2)
print("injection OK")
PYEOF
python3 "$OUTIL_PY" activer session-llm-1 vulcain "Mission test v055" > /dev/null 2>&1
N1=$(nb_demarrage session-llm-1)
[ "$N1" -eq 1 ]
check "2. activer sur bloc corrompu : 1 seul bloc DEMARRAGE (avant 4, lu=$N1)" $?

R1=$(raison_bloc session-llm-1)
[ "$R1" = "Mission test v055" ]
check "2b. Raison proprement remplacee (pas de recollement, lu=[$R1])" $?

# --- Test 3 : reactiver remplace aussi proprement (multiligne bilan) ---
# Note : reactiver cible Cerberus qui n a PAS de bloc DEMARRAGE (reserve aux
# agents actives) - le test verifie qu AUCUN bloc parasite n est recole.
python3 "$OUTIL_PY" reactiver session-llm-1 "BILAN TEST v055 : premiere ligne

suite multiligne du bilan
autre ligne" Cerberus > /dev/null 2>&1
N2=$(nb_demarrage session-llm-1)
[ "$N2" -eq 0 ]
check "3. reactiver : 0 bloc DEMARRAGE pour Cerberus (pas d accumulation, lu=$N2)" $?
R2=$(raison_bloc session-llm-1)
[ "$R2" = "BILAN TEST v055 : premiere ligne" ]
check "3b. Raison multiligne conservee proprement (lu=[$R2])" $?

# --- Test 4 : regression v0.5.0 (Nom LLM en tete preserve) ---
ID4=$(grep -A8 '^### Session : session-llm-1' "$AGENTS_FILE" | grep 'Nom LLM' | head -1 | grep -o 'llm-1')
[ "$ID4" = "llm-1" ]
check "4. Regression v0.5.0 : **Nom LLM** = llm-1 preserve (lu=$ID4)" $?

# --- Test 5 : normes (ASCII + LF) ---
# Python natif Windows ne voit pas /tmp : on passe le chemin en arg avec un
# chemin Windows mappe (cygpath si dispo, sinon le chemin POSIX fonctionne
# car Python lit le fichier en relatif si on cd dans l espace).
cd "$ESPACE" || exit 1
NONASCII=$(python3 -c "
import io
d = io.open('AGENTS.md', encoding='utf-8', errors='replace').read()
print(sum(1 for c in d if ord(c) > 127))
")
[ "$NONASCII" = "0" ]
check "5. ASCII strict : 0 non-ASCII (lu=$NONASCII)" $?
CRLF=$(python3 -c "
d = open('AGENTS.md', 'rb').read()
print(d.count(b'\r\n'))
")
[ "$CRLF" = "0" ]
check "5b. LF pur : 0 CRLF (lu=$CRLF)" $?
cd - > /dev/null 2>&1 || true

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
