#!/bin/bash
# ============================================================================
# TEST FORMEL -- valider-cartes-decision v0.3.2
# Cible : parcours JSON (source de verite), plus les fiches allegees.
# v0.3.2 : point 25 ajoute (garde-fou suivant mort, controle 7).
# Ecrit par Morpheus (testeur dedie), livre par Vulcain.
# Usage : bash tester-valider-cartes-decision.sh
# ============================================================================

PY_SCRIPT="cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.py"
SH_SCRIPT="cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.sh"
DOSSIER="cerveau-projet/agents/tools/valider/valider-cartes-decision"
TMP=".tmp-vcd-test"
PARCOURS_BUFFY="cerveau-projet/agents/buffy/parcours/parcours-buffy.json"

OK=0
ECHEC=0

verifier() {
    local nom=$1
    local condition=$2
    if eval "$condition"; then
        echo "[OK] $nom"
        OK=$((OK + 1))
    else
        echo "[ERREUR] $nom"
        ECHEC=$((ECHEC + 1))
    fi
}

# Capture la sortie d'une commande py dans une variable (pas de eval pour la capture)
run_py() {
    python3 "$PY_SCRIPT" "$@" 2>&1
}

echo "=== TEST FORMEL valider-cartes-decision v0.3.2 ==="
echo ""

# --- Preparation : parcours corrompu + zone temp (workspace uniquement)
rm -rf "$TMP"
mkdir -p "$TMP"
cat > "$TMP/parcours-casse.json" << 'EOF'
{
  "identite": {"type": "parcours", "appartient_a": "test", "commun": false},
  "parcours": {"nom": "parcours-test", "agent": "test", "version": "0.1.0", "case_depart": "c1"},
  "cases": {
    "c1": {"titre": "Case avec type invalide", "type": "mauvais", "suivant": "c9"}
  }
}
EOF

# --- 1. Version
verifier "1. --version py = 0.3.2" \
    "[ '$(run_py --version | grep -o '0.3.2')' = '0.3.2' ]"
verifier "2. --version sh = 0.3.2" \
    "[ '$(bash "$SH_SCRIPT" --version | grep -o '0.3.2')' = '0.3.2' ]"

# --- 2. --tous : 11/11 conformes (avant : 5/5 non conformes)
verifier "3. --tous = 11 agents verifies" \
    "[ '$(run_py --tous | grep 'Agents verifies' | grep -o '11')' = '11' ]"
verifier "4. --tous = 11 conformes" \
    "[ '$(run_py --tous | grep 'Agents conformes' | grep -o '11')' = '11' ]"
verifier "5. --tous = 0 non conformes" \
    "[ '$(run_py --tous | grep 'Agents non conformes' | grep -o '0')' = '0' ]"

# --- 3. --agent conforme
verifier "6. --agent cerberus = CONFORME" \
    "[ '$(run_py --agent cerberus | grep -c 'CONFORME')' -ge 1 ]"
verifier "7. --agent buffy = CONFORME" \
    "[ '$(run_py --agent buffy | grep -c 'CONFORME')' -ge 1 ]"

# --- 4. --fichier parcours conforme
verifier "8. --fichier parcours-buffy.json = CONFORME" \
    "[ '$(run_py --fichier "$PARCOURS_BUFFY" | grep -c 'CONFORME')' -ge 1 ]"

# --- 5. --fichier .md = mauvaise cible (NON CONFORME + note)
verifier "9. --fichier fiche .md = NON CONFORME (mauvaise cible)" \
    "[ '$(run_py --fichier cerveau-projet/agents/buffy/buffy.md | grep -c 'NON CONFORME')' -ge 1 ]"
verifier "10. --fichier .md mentionne le parcours JSON" \
    "[ '$(run_py --fichier cerveau-projet/agents/buffy/buffy.md | grep -c 'parcours')' -ge 1 ]"

# --- 6. Parcours corrompu : 3 erreurs detectees
verifier "11. parcours corrompu = 3 erreurs (type, ref, c0)" \
    "[ '$(run_py --fichier "$TMP/parcours-casse.json" | grep -c 'ERREUR')' -eq 3 ]"
verifier "12. parcours corrompu = NON CONFORME" \
    "[ '$(run_py --fichier "$TMP/parcours-casse.json" | grep -c 'NON CONFORME')' -ge 1 ]"
verifier "13. erreur type invalide detectee" \
    "[ '$(run_py --fichier "$TMP/parcours-casse.json" | grep -c 'Types invalides')' -ge 1 ]"
verifier "14. erreur reference cassee detectee" \
    "[ '$(run_py --fichier "$TMP/parcours-casse.json" | grep -c 'References cassees')' -ge 1 ]"
verifier "15. erreur c0 absente detectee" \
    "[ '$(run_py --fichier "$TMP/parcours-casse.json" | grep -c 'Case c0 absente')' -ge 1 ]"

# --- 7. Garde-fou suivant mort (controle 7, v0.3.2)
# Parcours infeste : c1 = fin avec suivant, c2 = branches + suivant
cat > "$TMP/parcours-infeste.json" << 'EOF'
{
  "identite": {"type": "parcours", "appartient_a": "test", "commun": false},
  "parcours": {"nom": "parcours-test", "agent": "test", "version": "0.1.0", "case_depart": "c0"},
  "cases": {
    "c0": {"type": "question", "question": "Relu ma fiche ?",
          "branches": [{"reponse": "OUI", "vers": "c1"}, {"reponse": "NON", "vers": "c0"}],
          "suivant": "c1"},
    "c1": {"type": "fin", "titre": "Fin", "suivant": "c2"},
    "c2": {"type": "fin", "titre": "Fin 2"}
  }
}
EOF
verifier "25. parcours infeste = NON CONFORME (suivants morts)" \
    "[ '$(run_py --fichier "$TMP/parcours-infeste.json" | grep -c 'NON CONFORME')' -ge 1 ]"
verifier "26. suivants morts detectes (fin + branches)" \
    "[ '$(run_py --fichier "$TMP/parcours-infeste.json" | grep -c 'Suivants morts')' -ge 1 ]"
verifier "27. fin avec suivant detectee" \
    "[ '$(run_py --fichier "$TMP/parcours-infeste.json" | grep -c 'fin avec suivant')' -ge 1 ]"
verifier "28. branches + suivant detectes" \
    "[ '$(run_py --fichier "$TMP/parcours-infeste.json" | grep -c 'branches priment')' -ge 1 ]"

# --- 8. Fichier inexistant
compte_16=$(run_py --fichier "$TMP/absent.json" | grep -c "existe pas")
verifier "16. fichier inexistant = ERREUR" \
    "[ '$compte_16' -ge 1 ]"

# --- 9. Parite py/sh (CRLF normalise)
parite() {
    local cible=$1
    diff <(run_py "$cible" | tr -d '\r') <(bash "$SH_SCRIPT" "$cible" 2>&1 | tr -d '\r') > /dev/null
}
verifier "17. parite --tous" "parite --tous"
verifier "18. parite --agent cerberus" "parite --agent cerberus"
verifier "19. parite --fichier parcours" "parite --fichier $PARCOURS_BUFFY"
verifier "20. parite --fichier .md" "parite --fichier cerveau-projet/agents/buffy/buffy.md"

# --- 10. ASCII des 3 fichiers + nommage
verifier "21. ASCII py" \
    "[ '$(python3 cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.py "$DOSSIER/valider-cartes-decision.py" | grep -c 'OK')' -ge 1 ]"
verifier "22. ASCII sh" \
    "[ '$(python3 cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.py "$DOSSIER/valider-cartes-decision.sh" | grep -c 'OK')' -ge 1 ]"
verifier "23. ASCII md" \
    "[ '$(python3 cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.py "$DOSSIER/valider-cartes-decision.md" | grep -c 'OK')' -ge 1 ]"
verifier "24. nommage outil py" \
    "[ '$(python3 cerveau-projet/agents/tools/valider/valider-nommage/valider-nommage.py --type outil "$DOSSIER/valider-cartes-decision.py" 2>&1 | grep -c 'ERREUR')' -eq 0 ]"

# --- Nettoyage
rm -rf "$TMP"

echo ""
echo "=== RESUME ==="
echo "Tests reussis : $OK"
echo "Tests echoues : $ECHEC"
if [ "$ECHEC" -eq 0 ]; then
    echo "VERDICT : VALIDE ($OK/$((OK + ECHEC)))"
    exit 0
else
    echo "VERDICT : NON VALIDE ($OK/$((OK + ECHEC)))"
    exit 1
fi
