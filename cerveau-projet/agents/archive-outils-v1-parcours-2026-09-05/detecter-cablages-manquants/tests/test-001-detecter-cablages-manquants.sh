#!/bin/bash
# test-001-detecter-cablages-manquants.sh
# Tests formels v0.1.1 : detecter-cablages-manquants
# Detecte les cablages manquants des cartes de decision (parcours JSON) :
#   - CASE_DEPART        : manquante ou inexistante
#   - FIN_NON_JOIGNABLE  : fin jamais atteignable depuis la case de depart
#   - CAS_ORPHELINE      : TOUTE case jamais atteignable (maillon manquant du
#                          bug des questions Ameliorations orphelines)
#   - BOUCLE_BLOQUANTE   : cycle SANS sortie (vs BOUCLE_RE_TRAVAIL = cycle
#                          avec sortie, voulu, en avertissement)
#   - REF_MORTE          : suivant/branche vers une case inexistante
# Tests sur COPIES : parcours JSON copies dans un espace temporaire.

# --- Protections -----------------------------------------------------------
PROTECTIONS_DIR="$(cd "$(dirname "$0")/../../../tester/protections" 2>/dev/null && pwd)"
if [ -z "$PROTECTIONS_DIR" ] || [ ! -d "$PROTECTIONS_DIR" ]; then
    PROTECTIONS_DIR="$(dirname "$0")/../../../tester/protections"
fi

source "$PROTECTIONS_DIR/tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh"
source "$PROTECTIONS_DIR/tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh"
source "$PROTECTIONS_DIR/tester-protection-blocage/tester-protection-blocage.sh"

OUTIL_PY="$(cd "$(dirname "$0")/.." && pwd)/detecter-cablages-manquants.py"
# Zone temporaire DANS le workspace (regle immuable regles-perimetre-workspace)
RACINE="$(cd "$(dirname "$0")/../../../../../.." && pwd)"
ESPACE="$RACINE/.tmp-test-detecter-cablages"

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

preparer() {
    local espace="$1"
    rm -rf "$espace"
    mkdir -p "$espace"
    # Copie du parcours sain cerberus (source de verite : le vrai parcours)
    cp "$RACINE/cerveau-projet/agents/cerberus/parcours/parcours-cerberus.json" "$espace/parcours-sain.json"
    # Parcours avec bug simule : 1 case orpheline + 1 boucle indirecte + 1 ref morte
    python3 - "$espace/parcours-bug.json" << 'EOF'
import json, io, sys
src = "cerveau-projet/agents/cerberus/parcours/parcours-cerberus.json"
c = json.load(io.open(src, encoding="utf-8"))
# 1. case orpheline non-fin (le maillon manquant)
c["cases"]["zorp"] = {"titre": "Orpheline", "type": "action", "suivant": "c9", "branches": []}
# 2. boucle indirecte SANS sortie dans le graphe atteignable (c15c -> z1 -> z2 -> z1)
c["cases"]["c15c"]["suivant"] = "z1"
c["cases"]["z1"] = {"titre": "BoucleA", "type": "question", "suivant": None,
                    "branches": [{"reponse": "OUI", "vers": "z2"}]}
c["cases"]["z2"] = {"titre": "BoucleB", "type": "question", "suivant": None,
                    "branches": [{"reponse": "OUI", "vers": "z1"}]}
# 3. reference morte (suivant vers une case inexistante)
c["cases"]["c99"] = {"titre": "RefMorte", "type": "action", "suivant": "zzinexistant",
                     "branches": []}
io.open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(
    json.dumps(c, ensure_ascii=True, indent=2))
EOF
}

echo "=== Tests formels : detecter-cablages-manquants ==="

preparer "$ESPACE"

# 1. Version
VER=$(python3 "$OUTIL_PY" --version 2>&1)
verifier "1. --version = detecter-cablages-manquants v0.1.1" \
    "[ \"$VER\" = 'detecter-cablages-manquants v0.1.1' ]"

# 2. Parcours sain (cerberus) : 0 probleme bloquant
OUT=$(python3 "$OUTIL_PY" "$ESPACE/parcours-sain.json" 2>&1)
verifier "2. parcours sain : verdict PROPRE" \
    "echo \"$OUT\" | grep -q 'Verdict global : PROPRE'"
verifier "3. parcours sain : aucun [CAS_ORPHELINE] ni [REF_MORTE] ni [BOUCLE_BLOQUANTE]" \
    "! echo \"$OUT\" | grep -qE '\[(CAS_ORPHELINE|REF_MORTE|BOUCLE_BLOQUANTE)\]'"

# 4-6. Parcours avec bug simule : les 3 familles detectees
OUTB=$(python3 "$OUTIL_PY" "$ESPACE/parcours-bug.json" 2>&1)
verifier "4. bug simule : CAS_ORPHELINE detecte (case zorp)" \
    "echo \"$OUTB\" | grep -q 'CAS_ORPHELINE.*zorp'"
verifier "5. bug simule : BOUCLE_BLOQUANTE detectee (z1 -> z2)" \
    "echo \"$OUTB\" | grep -q 'BOUCLE_BLOQUANTE.*z1 -> z2'"
verifier "6. bug simule : REF_MORTE detectee (zzinexistant)" \
    "echo \"$OUTB\" | grep -q 'REF_MORTE.*zzinexistant'"

# 7. --tous : les 11 parcours reels, 0 probleme bloquant
OUTT=$(python3 "$OUTIL_PY" --tous 2>&1)
verifier "7. --tous : verdict PROPRE sur 11 parcours" \
    "echo \"$OUTT\" | grep -q 'PROPRE sur 11 parcours'"

# 8. --rapport : le fichier est ecrit
python3 "$OUTIL_PY" --tous --rapport "$ESPACE/rapport.md" > /dev/null 2>&1
verifier "8. --rapport : fichier genere" \
    "[ -f \"$ESPACE/rapport.md\" ] && grep -q 'Problemes bloquants : 0' \"$ESPACE/rapport.md\""

# Nettoyage
rm -rf "$ESPACE"

echo ""
if [ "$NB_ECHEC" -eq 0 ]; then
    echo "=== RESULTAT : $NB_OK OK / 0 KO ==="
    exit 0
else
    echo "=== RESULTAT : $NB_OK OK / $NB_ECHEC KO ==="
    exit 1
fi
