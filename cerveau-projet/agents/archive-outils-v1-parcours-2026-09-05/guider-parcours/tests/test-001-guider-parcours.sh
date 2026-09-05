#!/bin/bash
# test-001-guider-parcours.sh
# Test formel du GUIDE-PARCOURS v0.1.0 (jeu de piste)
# Ecrit par Morpheus (regle delegation - Vulcain ne teste jamais lui-meme)

VERSION_TEST="0.1.0"
REPERTOIRE_TEST="/tmp/test-guider-parcours"
OUTIL_PY="cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py"
OUTIL_SH="cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.sh"
PARCOURS="cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json"

TOTAL=0
REUSSIS=0
ECHECS=0

verifier() {
    local nom="$1"
    local attendu="$2"
    local obtenu="$3"
    TOTAL=$((TOTAL+1))
    if [ "$obtenu" = "$attendu" ]; then
        REUSSIS=$((REUSSIS+1))
        echo "  [OK] $nom"
    else
        ECHECS=$((ECHECS+1))
        echo "  [ECHEC] $nom : attendu '$attendu' obtenu '$obtenu'"
    fi
}

verifier_contient() {
    local nom="$1"
    local pattern="$2"
    local sortie="$3"
    TOTAL=$((TOTAL+1))
    if echo "$sortie" | grep -q "$pattern"; then
        REUSSIS=$((REUSSIS+1))
        echo "  [OK] $nom"
    else
        ECHECS=$((ECHECS+1))
        echo "  [ECHEC] $nom : pattern '$pattern' absent de la sortie"
    fi
}

preparer_parcours_test() {
    mkdir -p "$REPERTOIRE_TEST"
    cat > "$REPERTOIRE_TEST/parcours-ok.json" << 'EOF'
{
  "parcours": {
    "nom": "parcours-test",
    "agent": "test",
    "version": "0.1.0",
    "case_depart": "c1",
    "description": "Parcours de test"
  },
  "cases": {
    "c1": {
      "titre": "Mission",
      "type": "question",
      "question": "Quelle est la mission ?",
      "branches": [
        { "reponse": "construire", "vers": "c2" },
        { "reponse": "autre", "vers": "c4" }
      ]
    },
    "c2": {
      "titre": "Indice sans question",
      "type": "indice",
      "indices": [
        { "type": "regle", "texte": "REGLE TEST" },
        { "type": "outil", "nom": "test-outil", "chemin": "chemin/test.py", "commande": "python3 chemin/test.py" },
        { "type": "fichier", "chemin": "chemin/doc.md", "raison": "raison test" }
      ],
      "suivant": "c3"
    },
    "c3": {
      "titre": "FIN TEST",
      "type": "fin",
      "message": "Fin du parcours de test"
    },
    "c4": {
      "titre": "Branche autre",
      "type": "fin",
      "message": "Branche autre atteinte"
    }
  }
}
EOF
    echo '{ "parcours": { "case_depart": "c1" }, "cases": { "c1": { "titre": "x", "type": "indice" } } }' > "$REPERTOIRE_TEST/parcours-indice-sans-suivant.json"
    echo 'ceci n est pas du json' > "$REPERTOIRE_TEST/parcours-invalide.json"
    echo '{ "parcours": { "case_depart": "c1" }, "cases": { "c1": { "titre": "x", "type": "question", "question": "q?", "branches": [ { "reponse": "oui", "vers": "c999" } ] } } }' > "$REPERTOIRE_TEST/parcours-branche-casse.json"
}

nettoyer() {
    rm -rf "$REPERTOIRE_TEST"
}

echo "=== TEST guider-parcours v$VERSION_TEST ==="
echo ""
echo "--- Preparation ---"
preparer_parcours_test
echo "  Parcours de test crees dans $REPERTOIRE_TEST"

echo ""
echo "--- 1. --liste inventorie les cases ---"
SORTIE_LISTE_PY=$(cd / && python3 "$OLDPWD/$OUTIL_PY" "$OLDPWD/$PARCOURS" --liste 2>&1)
verifier_contient "liste: 19 cases (depart c1)" "\\[c1\\] question Mission" "$SORTIE_LISTE_PY"
verifier_contient "liste: case fin c9" "\\[c9\\] fin" "$SORTIE_LISTE_PY"
verifier_contient "liste: case c19 fin" "\\[c19\\] fin" "$SORTIE_LISTE_PY"

echo ""
echo "--- 2. Navigation --reponses: bonne branche ---"
SORTIE_NAV=$(cd "$REPERTOIRE_TEST" && python3 "$OLDPWD/$OUTIL_PY" parcours-ok.json --reponses "construire" 2>&1)
verifier_contient "branche construire -> c2 (indice)" "\\[OUTIL\\] test-outil" "$SORTIE_NAV"
verifier_contient "indice regle affiche" "REGLE TEST" "$SORTIE_NAV"
verifier_contient "indice fichier affiche" "\\[FICHIER\\] chemin/doc.md" "$SORTIE_NAV"
verifier_contient "case fin atteinte" "PARCOURS TERMINE" "$SORTIE_NAV"

echo ""
echo "--- 3. Reponse inconnue -> erreur claire ---"
SORTIE_INCONNUE=$(cd "$REPERTOIRE_TEST" && python3 "$OLDPWD/$OUTIL_PY" parcours-ok.json --reponses "inconnu" 2>&1)
verifier_contient "reponse inconnue signalee" "REPONSE INCONNUE" "$SORTIE_INCONNUE"

echo ""
echo "--- 4. --case demarre a une case precise ---"
SORTIE_CASE=$(cd "$REPERTOIRE_TEST" && python3 "$OLDPWD/$OUTIL_PY" parcours-ok.json --case c4 2>&1)
verifier_contient "case c4 affichee" "Branche autre atteinte" "$SORTIE_CASE"

echo ""
echo "--- 5. JSON invalide refuse ---"
SORTIE_INVALIDE=$(cd "$REPERTOIRE_TEST" && python3 "$OLDPWD/$OUTIL_PY" parcours-invalide.json 2>&1)
verifier_contient "json invalide signale" "JSON invalide" "$SORTIE_INVALIDE"

echo ""
echo "--- 6. Branche vers case inexistante -> validation refuse ---"
SORTIE_BRANCHE=$(cd "$REPERTOIRE_TEST" && python3 "$OLDPWD/$OUTIL_PY" parcours-branche-casse.json 2>&1)
verifier_contient "branche cassee signalee" "introuvable" "$SORTIE_BRANCHE"

echo ""
echo "--- 7. Parite py/sh (memes sorties) ---"
SORTIE_PY=$(cd "$REPERTOIRE_TEST" && python3 "$OLDPWD/$OUTIL_PY" parcours-ok.json --reponses "construire" 2>&1 | sed 's/[[:space:]]*$//')
SORTIE_SH=$(cd "$REPERTOIRE_TEST" && bash "$OLDPWD/$OUTIL_SH" parcours-ok.json --reponses "construire" 2>&1 | sed 's/[[:space:]]*$//')
if [ "$SORTIE_PY" = "$SORTIE_SH" ]; then
    TOTAL=$((TOTAL+1)); REUSSIS=$((REUSSIS+1))
    echo "  [OK] parite py/sh : sorties identiques"
else
    TOTAL=$((TOTAL+1)); ECHECS=$((ECHECS+1))
    echo "  [ECHEC] parite py/sh : sorties differentes"
fi

echo ""
echo "--- 8. Syntaxe py + sh ---"
cd "$OLDPWD"
python3 -m py_compile "$OUTIL_PY" 2>/dev/null
if [ $? -eq 0 ]; then
    TOTAL=$((TOTAL+1)); REUSSIS=$((REUSSIS+1))
    echo "  [OK] py_compile"
else
    TOTAL=$((TOTAL+1)); ECHECS=$((ECHECS+1))
    echo "  [ECHEC] py_compile"
fi
bash -n "$OUTIL_SH" 2>/dev/null
if [ $? -eq 0 ]; then
    TOTAL=$((TOTAL+1)); REUSSIS=$((REUSSIS+1))
    echo "  [OK] bash -n"
else
    TOTAL=$((TOTAL+1)); ECHECS=$((ECHECS+1))
    echo "  [ECHEC] bash -n"
fi

echo ""
echo "--- Nettoyage ---"
nettoyer
echo "  Fichiers de test supprimes"

echo ""
echo "=== Rapport ==="
echo "Total: $TOTAL"
echo "Reussis: $REUSSIS"
echo "Echecs: $ECHECS"
if [ "$ECHECS" -eq 0 ]; then
    echo "VERDICT : VALIDE"
    exit 0
else
    echo "VERDICT : ECHEC"
    exit 1
fi
