#!/bin/bash
# tester-combos-moteur-v020.sh
# Test formel de la case critere de combos-moteur v0.2.0
# Verifie les 5 conditions (fichier-existe, egalite, non-vide,
# sortie-contient, fichier-contient) + parite py/sh + interpolation tirets
# Test: 2026-08-08
# Auteur: Vulcain

RACINE="Z:/analyste-in-console"
OUTIL_PY="python3 $RACINE/cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.py"
OUTIL_SH="bash $RACINE/cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.sh"

TMP=$(mktemp -d)
cd "$TMP" || exit 1

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

# Fichier de reference pour les conditions fichier-*
printf 'contenu-attendu' > ./fichier-cible.txt

# Definition du combo de test (les 5 conditions)
cat > ./combo-criteres.json <<'EOF'
{
  "combo": {
    "nom": "test-criteres",
    "version": "0.1.0",
    "description": "Test des 5 conditions de la case critere",
    "case_depart": "c1"
  },
  "cases": {
    "c1": {
      "type": "critere",
      "titre": "fichier-existe (VRAI)",
      "condition": { "type": "fichier-existe", "chemin": "{fichier-cible}" },
      "vers-vrai": "c2",
      "vers-faux": "c6"
    },
    "c2": {
      "type": "critere",
      "titre": "egalite (VRAI)",
      "condition": { "type": "egalite", "variable": "ma-variable", "valeur": "valeur-attendue" },
      "vers-vrai": "c3",
      "vers-faux": "c6"
    },
    "c3": {
      "type": "critere",
      "titre": "non-vide (VRAI)",
      "condition": { "type": "non-vide", "variable": "ma-variable" },
      "vers-vrai": "c4",
      "vers-faux": "c6"
    },
    "c4": {
      "type": "critere",
      "titre": "sortie-contient (FAUX -> c5)",
      "condition": { "type": "sortie-contient", "source": "{resultat-outil}", "texte": "TEXTE-INTROUVABLE" },
      "vers-vrai": "c6",
      "vers-faux": "c5"
    },
    "c5": {
      "type": "critere",
      "titre": "fichier-contient (VRAI -> c7)",
      "condition": { "type": "fichier-contient", "chemin": "{fichier-cible}", "texte": "contenu-attendu" },
      "vers-vrai": "c7",
      "vers-faux": "c6"
    },
    "c6": { "type": "fin", "titre": "ECHEC global", "message": "Echec" },
    "c7": { "type": "fin", "titre": "SUCCES global", "message": "Succes" }
  }
}
EOF

# Definition pour tester le chemin FAUX (fichier absent -> c6 ECHEC attendu)
cat > ./combo-faux.json <<'EOF'
{
  "combo": {
    "nom": "test-faux",
    "version": "0.1.0",
    "description": "Chemin faux : fichier absent",
    "case_depart": "c1"
  },
  "cases": {
    "c1": {
      "type": "critere",
      "titre": "fichier-existe (FAUX -> c6)",
      "condition": { "type": "fichier-existe", "chemin": "./fichier-absent.txt" },
      "vers-vrai": "c7",
      "vers-faux": "c6"
    },
    "c6": { "type": "fin", "titre": "ECHEC", "message": "Chemin faux atteint" },
    "c7": { "type": "fin", "titre": "SUCCES", "message": "Chemin vrai" }
  }
}
EOF

VARS="--var fichier-cible=./fichier-cible.txt --var ma-variable=valeur-attendue --var resultat-outil=sortie-simple"

# --- PT1 : chemin complet VRAI (py) -> c7 SUCCES ---
r=$($OUTIL_PY ./combo-criteres.json $VARS 2>&1 | grep -c "case 'c7'")
check "PT1: py chemin VRAI -> c7" "1" "$r"

# --- PT2 : chemin complet VRAI (sh) -> c7 SUCCES ---
r=$($OUTIL_SH ./combo-criteres.json $VARS 2>&1 | grep -c "case 'c7'")
check "PT2: sh chemin VRAI -> c7" "1" "$r"

# --- PT3 : chemin FAUX (fichier absent) -> c6 ECHEC ---
r=$($OUTIL_PY ./combo-faux.json 2>&1 | grep -c "case 'c6'")
check "PT3: py chemin FAUX -> c6" "1" "$r"
r=$($OUTIL_SH ./combo-faux.json 2>&1 | grep -c "case 'c6'")
check "PT4: sh chemin FAUX -> c6" "1" "$r"

# --- PT5 : --liste affiche le type critere ---
r=$($OUTIL_PY ./combo-criteres.json --liste 2>&1 | grep -cE "\[c[0-9]+\] critere ")
check "PT5: --liste montre 5 cases critere" "5" "$r"

# --- PT6 : validation - critere sans condition.type -> erreur ---
cat > ./combo-invalide.json <<'EOF'
{
  "combo": { "nom": "invalide", "version": "0.1.0", "case_depart": "c1" },
  "cases": {
    "c1": { "type": "critere", "titre": "sans condition", "vers-vrai": "c6", "vers-faux": "c6" },
    "c6": { "type": "fin", "titre": "FIN" }
  }
}
EOF
r=$($OUTIL_PY ./combo-invalide.json 2>&1 | grep -c "critere sans 'condition.type'")
check "PT6: critere sans condition.type refuse" "1" "$r"

# --- PT7 : validation - vers-faux inexistant -> erreur ---
cat > ./combo-invalide2.json <<'EOF'
{
  "combo": { "nom": "invalide2", "version": "0.1.0", "case_depart": "c1" },
  "cases": {
    "c1": {
      "type": "critere",
      "titre": "vers-faux absent",
      "condition": { "type": "non-vide", "variable": "x" },
      "vers-vrai": "c6"
    },
    "c6": { "type": "fin", "titre": "FIN" }
  }
}
EOF
r=$($OUTIL_PY ./combo-invalide2.json 2>&1 | grep -c "critere sans 'vers-vrai' ou 'vers-faux'")
check "PT7: critere sans vers-faux refuse" "1" "$r"

# --- PT8 : parite py/sh sur le meme chemin (c7) ---
r_py=$($OUTIL_PY ./combo-criteres.json $VARS 2>&1 | grep -oE "case 'c[0-9]+'" | tail -1)
r_sh=$($OUTIL_SH ./combo-criteres.json $VARS 2>&1 | grep -oE "case 'c[0-9]+'" | tail -1)
check "PT8: parite fin py=$r_py sh=$r_sh" "$r_py" "$r_sh"

# --- PT9 : interpolation kebab-case {ma-variable} ---
r=$($OUTIL_PY ./combo-criteres.json $VARS --verbose 2>&1 | grep -c "egalite ma-variable=valeur-attendue : VRAI")
check "PT9: interpolation tirets (ma-variable) OK" "1" "$r"

# --- PT10 : condition inconnue -> erreur ---
cat > ./combo-inconnu.json <<'EOF'
{
  "combo": { "nom": "inconnu", "version": "0.1.0", "case_depart": "c1" },
  "cases": {
    "c1": {
      "type": "critere",
      "titre": "condition inconnue",
      "condition": { "type": "condition-impossible" },
      "vers-vrai": "c6",
      "vers-faux": "c6"
    },
    "c6": { "type": "fin", "titre": "FIN" }
  }
}
EOF
r=$($OUTIL_PY ./combo-inconnu.json 2>&1 | grep -c "type de condition inconnu")
check "PT10: condition inconnue refusee" "1" "$r"

echo ""
echo "=== Resume ==="
echo "  Reussis : $PASS"
echo "  Echecs : $FAIL"
cd /
rm -rf "$TMP"
if [[ $FAIL -gt 0 ]]; then
    exit 1
fi
exit 0
