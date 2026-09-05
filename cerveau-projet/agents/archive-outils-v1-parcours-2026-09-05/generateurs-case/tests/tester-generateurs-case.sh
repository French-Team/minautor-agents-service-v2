#!/bin/bash
# tester-generateurs-case.sh
# Tests formels de l'outil generateurs-case (sur COPIES dans /tmp -- jamais les vrais parcours)
# Version : 0.1.0
# Statut : ebauche

OUTIL_PY="cerveau-projet/agents/tools/generateurs/generateurs-case/generateurs-case.py"
OUTIL_SH="cerveau-projet/agents/tools/generateurs/generateurs-case/generateurs-case.sh"
PARCOURS_SRC="cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json"
BASE="/tmp/gc-test-formel"
BASE_WIN=$(cygpath -m "$BASE" 2>/dev/null || echo "$BASE")
NOMBRE_PASS=0
NOMBRE_ECHEC=0

verifier() {
    local nom="$1"
    local resultat="$2"
    if [ "$resultat" = "0" ]; then
        echo "[OK] $nom"
        NOMBRE_PASS=$((NOMBRE_PASS + 1))
    else
        echo "[ECHEC] $nom"
        NOMBRE_ECHEC=$((NOMBRE_ECHEC + 1))
    fi
}

# Preparation : copie de travail
rm -rf "$BASE"
mkdir -p "$BASE"
cp "$PARCOURS_SRC" "$BASE/parcours.json"

# PT1 : nommage (prefixe generateurs-) -- le script ne doit pas planter
python3 "$OUTIL_PY" "$BASE/parcours.json" liste > /dev/null 2>&1
verifier "PT1 nommage + chargement" $?

# PT2 : syntaxe py_compile
python3 -m py_compile "$OUTIL_PY" > /dev/null 2>&1
verifier "PT2 py_compile" $?

# PT3 : syntaxe bash -n
bash -n "$OUTIL_SH"
verifier "PT3 bash -n" $?

# PT4 : --version py et sh identiques
V1=$(python3 "$OUTIL_PY" x liste --version 2>&1)
V2=$(bash "$OUTIL_SH" x liste --version 2>&1)
if [ "$V1" = "$V2" ]; then verifier "PT4 parite --version" 0; else verifier "PT4 parite --version" 1; fi

# PT5 : liste charge la carte (nb de cases du parcours source, dynamique)
NB0=$(python3 "$OUTIL_PY" "$BASE/parcours.json" liste 2>&1 | grep -c '^  \[')
if [ "$NB0" -gt "0" ]; then verifier "PT5 liste charge $NB0 cases" 0; else verifier "PT5 liste charge (trouve $NB0)" 1; fi

# PT6 : ajouter une case apres c8 (recablage du suivant) - id = prochain libre (dynamique)
python3 "$OUTIL_PY" "$BASE/parcours.json" ajouter \
    --type indice --titre "Verifier le rapport" --suivant c9 --apres c8 \
    --indice-regle "REGLE : verifier avant d agir" > /dev/null 2>&1
verifier "PT6 ajouter case" $?
NB=$(python3 "$OUTIL_PY" "$BASE/parcours.json" liste 2>&1 | grep -c '^  \[')
if [ "$NB" = "$((NB0 + 1))" ]; then verifier "PT6b NB0+1 cases apres ajout" 0; else verifier "PT6b NB0+1 cases apres ajout (trouve $NB)" 1; fi

# La nouvelle case inseree apres c8 : c8.suivant pointe vers elle (recablage --apres)
NOUVELLE=$(python3 -c "import json; print(json.load(open('$BASE_WIN/parcours.json', encoding='utf-8'))['cases']['c8'].get('suivant',''))")

# PT7 : editer la case ajoutee (id dynamique)
python3 "$OUTIL_PY" "$BASE/parcours.json" editer "$NOUVELLE" --titre "Verifie (v2)" > /dev/null 2>&1
verifier "PT7 editer case ($NOUVELLE)" $?
TITRE=$(python3 -c "import json; print(json.load(open('$BASE_WIN/parcours.json', encoding='utf-8'))['cases']['$NOUVELLE'].get('titre',''))")
if echo "$TITRE" | grep -q "Verifie (v2)"; then verifier "PT7b titre modifie" 0; else verifier "PT7b titre modifie (trouve: $TITRE)" 1; fi

# PT8 : supprimer c8 -> recablage du pointant reel (c7b pointe vers c8, pas c7)
python3 "$OUTIL_PY" "$BASE/parcours.json" supprimer c8 > /dev/null 2>&1
verifier "PT8 supprimer c8" $?
SUIVANT=$(grep -A30 '"c7b": {' "$BASE/parcours.json" | grep suivant | head -1)
if echo "$SUIVANT" | grep -q "$NOUVELLE"; then verifier "PT8b recablage c7b->$NOUVELLE" 0; else verifier "PT8b recablage c7b (trouve: $SUIVANT)" 1; fi
if grep -q '"c8"' "$BASE/parcours.json"; then verifier "PT8c c8 disparu" 1; else verifier "PT8c c8 disparu" 0; fi
# PT9 : supprimer une case fin sans --vers -> ERREUR attendue
cp "$PARCOURS_SRC" "$BASE/p2.json"
RES=$(python3 "$OUTIL_PY" "$BASE/p2.json" supprimer c9 2>&1 | grep -c 'ERREUR')
if [ "$RES" -ge "1" ]; then verifier "PT9 fin sans vers -> ERREUR" 0; else verifier "PT9 fin sans vers -> ERREUR" 1; fi

# PT10 : supprimer une case fin avec --vers -> OK
python3 "$OUTIL_PY" "$BASE/p2.json" supprimer c9 --vers c19 > /dev/null 2>&1
verifier "PT10 supprimer fin avec --vers" $?

# PT11 : --dry-run ne modifie pas le fichier
cp "$PARCOURS_SRC" "$BASE/p3.json"
python3 "$OUTIL_PY" "$BASE/p3.json" ajouter --type fin --titre TESTFIN --dry-run > /dev/null 2>&1
if grep -q 'TESTFIN' "$BASE/p3.json"; then verifier "PT11 dry-run sans modification" 1; else verifier "PT11 dry-run sans modification" 0; fi

# PT12 : JSON invalide refuse
echo "not json" > "$BASE/invalide.json"
RES=$(python3 "$OUTIL_PY" "$BASE/invalide.json" liste 2>&1 | grep -c 'ERREUR')
if [ "$RES" -ge "1" ]; then verifier "PT12 JSON invalide refuse" 0; else verifier "PT12 JSON invalide refuse" 1; fi

# PT13 : navigation inchangee apres modifications (guider-parcours)
RES=$(python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \
    "$BASE/parcours.json" --reponses 'OUI|construire|OUI|OUI|OUI|OUI|OUI' 2>&1 | grep -c 'PARCOURS TERMINE')
if [ "$RES" = "1" ]; then verifier "PT13 navigation PARCOURS TERMINE" 0; else verifier "PT13 navigation PARCOURS TERMINE" 1; fi

# PT14 : ASCII 0 sur les fichiers de l outil
for f in generateurs-case.py generateurs-case.sh generateurs-case.md; do
    RES=$(python3 cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.py \
        "cerveau-projet/agents/tools/generateurs/generateurs-case/$f" 2>&1 | grep -c 'non-ASCII : 0')
    if [ "$RES" = "1" ]; then verifier "PT14 ASCII $f" 0; else verifier "PT14 ASCII $f" 1; fi
done

# PT15 : parite py/sh sur la liste
S1=$(python3 "$OUTIL_PY" "$BASE/parcours.json" liste 2>&1)
S2=$(bash "$OUTIL_SH" "$BASE/parcours.json" liste 2>&1)
if [ "$S1" = "$S2" ]; then verifier "PT15 parite liste py/sh" 0; else verifier "PT15 parite liste py/sh" 1; fi

# PT16 : convertir --dry-run ne modifie pas le fichier
cp "$PARCOURS_SRC" "$BASE/c1.json"
V_AVANT=$(python3 -c "import json; print(json.load(open('$BASE_WIN/c1.json', encoding='utf-8'))['parcours']['version'])")
python3 "$OUTIL_PY" "$BASE/c1.json" convertir --version-parcours 9.9.9 --dry-run > /dev/null 2>&1
V_APRES=$(python3 -c "import json; print(json.load(open('$BASE_WIN/c1.json', encoding='utf-8'))['parcours']['version'])")
if [ "$V_AVANT" = "$V_APRES" ]; then verifier "PT16 dry-run version inchangee" 0; else verifier "PT16 dry-run version inchangee ($V_AVANT->$V_APRES)" 1; fi

# PT17 : convertir wet convertit indice -> action (0 indice restant) + bump version
python3 "$OUTIL_PY" "$BASE/c1.json" convertir --version-parcours 9.9.9 > /dev/null 2>&1
verifier "PT17 convertir wet" $?
INDICES=$(python3 -c "import json; d=json.load(open('$BASE_WIN/c1.json', encoding='utf-8')); print(sum(1 for c in d['cases'].values() if c.get('type')=='indice'))")
if [ "$INDICES" = "0" ]; then verifier "PT17b 0 indice restant" 0; else verifier "PT17b 0 indice restant (trouve $INDICES)" 1; fi
V_NOW=$(python3 -c "import json; print(json.load(open('$BASE_WIN/c1.json', encoding='utf-8'))['parcours']['version'])")
if [ "$V_NOW" = "9.9.9" ]; then verifier "PT17c version bumpee" 0; else verifier "PT17c version bumpee (trouve $V_NOW)" 1; fi

# PT18 : convertir avec mapping remplace les regles longues par des refs
cp "$PARCOURS_SRC" "$BASE/c2.json"
cat > "$BASE/mapping.json" <<'MJSON'
{
  "motifs": [
    {"contient": "REGLE IMMUABLE ASCII", "ref": "pattern-2"},
    {"contient": "CONTEXTE TEMPS REEL", "ref": "pattern-6"},
    {"contient": "UNE CARTE = UN ROLE", "ref": "pattern-10"}
  ]
}
MJSON
python3 "$OUTIL_PY" "$BASE/c2.json" convertir --refs "$BASE/mapping.json" > /dev/null 2>&1
NB_REFS=$(python3 -c "import json; d=json.load(open('$BASE_WIN/c2.json', encoding='utf-8')); print(sum(1 for c in d['cases'].values() for i in c.get('indices',[]) if i.get('type')=='ref'))")
if [ "$NB_REFS" -gt "0" ]; then verifier "PT18 refs via mapping ($NB_REFS)" 0; else verifier "PT18 refs via mapping (0 ref)" 1; fi

# PT19 : parite py/sh sur convertir (dry-run, meme sortie)
cp "$PARCOURS_SRC" "$BASE/c3.json"
S1=$(python3 "$OUTIL_PY" "$BASE/c3.json" convertir --dry-run 2>&1)
cp "$PARCOURS_SRC" "$BASE/c3.json"
S2=$(bash "$OUTIL_SH" "$BASE/c3.json" convertir --dry-run 2>&1)
if [ "$S1" = "$S2" ]; then verifier "PT19 parite convertir py/sh" 0; else verifier "PT19 parite convertir py/sh" 1; fi

# PT20 : convertir sans --version-parcours conserve la version
cp "$PARCOURS_SRC" "$BASE/c4.json"
V0=$(python3 -c "import json; print(json.load(open('$BASE_WIN/c4.json', encoding='utf-8'))['parcours']['version'])")
python3 "$OUTIL_PY" "$BASE/c4.json" convertir > /dev/null 2>&1
V1=$(python3 -c "import json; print(json.load(open('$BASE_WIN/c4.json', encoding='utf-8'))['parcours']['version'])")
if [ "$V0" = "$V1" ]; then verifier "PT20 version conservee sans --version-parcours" 0; else verifier "PT20 version conservee ($V0->$V1)" 1; fi

# Nettoyage
rm -rf "$BASE"

echo ""
echo "=== RESULTAT : $NOMBRE_PASS reussi(s), $NOMBRE_ECHEC echec(s) ==="
if [ "$NOMBRE_ECHEC" = "0" ]; then
    echo "VERDICT : VALIDE"
    exit 0
else
    echo "VERDICT : A CORRIGER"
    exit 1
fi
