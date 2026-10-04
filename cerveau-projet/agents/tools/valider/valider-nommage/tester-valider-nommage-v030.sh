#!/bin/bash
# tester-valider-nommage-v030.sh
# Test formel du mode --mots-seuls de valider-nommage v0.3.0
# Verifie la regle fondamentale 'aucun mot seul' (identifiants generiques)
# Test: 2026-08-08
# Auteur: Morpheus (validation formelle)
# REGLE WORKSPACE : zone temporaire DANS le workspace, supprimee en fin de test
# identite:
#   type: test
#   appartient_a: commun
#   commun: true

RACINE="Z:/analyste-in-console"
OUTIL_PY="python3 $RACINE/cerveau-projet/agents/tools/valider/valider-nommage/valider-nommage.py"
OUTIL_SH="bash $RACINE/cerveau-projet/agents/tools/valider/valider-nommage/valider-nommage.sh"

TMP="$RACINE/cerveau-projet/.tmp-test-valider-nommage"
mkdir -p "$TMP"
cd "$TMP" || exit 1

# Copier les fichiers de reference pour les tests
cp "$RACINE/cerveau-projet/agents/cerberus/cerberus.md" ./fiche-propre.md
cp "$RACINE/cerveau-projet/demarrage/parcours-demarrage.json" ./parcours-propre.json

PASS=0
FAIL=0

check() {
    local nom=$1
    local attendu=$2
    local obtenu=$3
    if [[ "$obtenu" == "$attendu" ]]; then
        echo "[OK] $nom"
        PASS=$((PASS + 1))
    else
        echo "[ERREUR] $nom : attendu=$attendu obtenu=$obtenu"
        FAIL=$((FAIL + 1))
    fi
}

# --- PT1 : fiche propre (aucun mot seul) ---
# Les cles de schema (version, cree, specialites...) sont autorisees
r=$($OUTIL_PY --mots-seuls ./fiche-propre.md 2>&1 | grep -c "IDENTIFIANT MOT SEUL")
check "PT1: fiche propre py = 0 mot seul" "0" "$r"
r=$($OUTIL_SH --mots-seuls ./fiche-propre.md 2>&1 | grep -c "IDENTIFIANT MOT SEUL")
check "PT2: fiche propre sh = 0 mot seul" "0" "$r"

# --- PT3 : test negatif YAML (3 identifiants interdits) ---
cat > ./negatif.md <<'EOF'
identite:
  type: outil
  nom: test
  role: dev
agent:
  statut: ok
  nom-agent: cerberus
EOF
r=$($OUTIL_PY --mots-seuls ./negatif.md 2>&1 | grep -c "IDENTIFIANT MOT SEUL")
check "PT3: negatif py = 3 mots seuls (nom, role, statut)" "3" "$r"
r=$($OUTIL_SH --mots-seuls ./negatif.md 2>&1 | grep -c "IDENTIFIANT MOT SEUL")
check "PT4: negatif sh = 3 mots seuls" "3" "$r"

# --- PT5 : frontmatter commente .py (1 identifiant) ---
cat > ./negatif.py <<'EOF'
# identite:
#   type: outil
#   nom: bug
#   nom-agent: ok
EOF
r=$($OUTIL_PY --mots-seuls ./negatif.py 2>&1 | grep -c "IDENTIFIANT MOT SEUL")
check "PT5: py commente = 1 mot seul" "1" "$r"
r=$($OUTIL_SH --mots-seuls ./negatif.py 2>&1 | grep -c "IDENTIFIANT MOT SEUL")
check "PT6: py commente sh = 1 mot seul" "1" "$r"

# --- PT7 : JSON propre ---
r=$($OUTIL_PY --mots-seuls ./parcours-propre.json 2>&1 | grep -c "IDENTIFIANT MOT SEUL")
check "PT7: json propre py = 0" "0" "$r"

# --- PT8 : JSON negatif (cle 'nom' dans identite) ---
cat > ./negatif.json <<'EOF'
{
  "identite": {
    "type": "outil",
    "nom": "bug",
    "nom-agent": "ok"
  }
}
EOF
r=$($OUTIL_PY --mots-seuls ./negatif.json 2>&1 | grep -c "IDENTIFIANT MOT SEUL")
check "PT8: json negatif py = 1" "1" "$r"
r=$($OUTIL_SH --mots-seuls ./negatif.json 2>&1 | grep -c "IDENTIFIANT MOT SEUL")
check "PT9: json negatif sh = 1" "1" "$r"

# --- PT10 : fichier inexistant ---
r=$($OUTIL_PY --mots-seuls ./fichier-inexistant.md 2>&1 | grep -c "n'existe pas")
check "PT10: fichier inexistant detecte" "1" "$r"

# --- PT11 : parite py/sh sur dossier recursif (traces ignorees) ---
r_py=$($OUTIL_PY --mots-seuls --recursive "$RACINE/cerveau-projet/agents/" 2>&1 | grep "Fichiers avec mots seuls" | grep -oE "[0-9]+")
r_sh=$($OUTIL_SH --mots-seuls --recursive "$RACINE/cerveau-projet/agents/" 2>&1 | grep "Fichiers avec mots seuls" | grep -oE "[0-9]+")
check "PT11: parite recursif py=$r_py sh=$r_sh" "$r_py" "$r_sh"
# PT11b : les deux doivent etre a 0 (aucun mot seul sur agents/ actif)
check "PT11b: recursif agents/ = 0 mot seul" "0" "$r_py"

# --- PT12 : compatibilite anciens modes (regression) ---
r=$($OUTIL_PY --type agent "$RACINE/cerveau-projet/agents/cerberus/cerberus.md" 2>&1 | grep -c "\[OK\]")
check "PT12: mode agent compatible (regression)" "1" "$r"

echo ""
echo "=== Resume ==="
echo "  Reussis : $PASS"
echo "  Echecs : $FAIL"
cd "$RACINE"
rm -rf "$TMP"  # Nettoyage de la zone temporaire (regle workspace)
if [[ $FAIL -gt 0 ]]; then
    exit 1
fi
exit 0
