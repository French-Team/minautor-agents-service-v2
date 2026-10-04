#!/bin/bash
# tester-detecter-impacts.sh
# Tests formels de l'outil detecter-impacts (+ combo-controle-impacts + --var moteur)
# Version : 0.2.0
# Statut : ebauche

OUTIL_PY="cerveau-projet/agents/tools/detecter/detecter-impacts/detecter-impacts.py"
OUTIL_SH="cerveau-projet/agents/tools/detecter/detecter-impacts/detecter-impacts.sh"
MOTEUR_PY="cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.py"
COMBO="cerveau-projet/combos/combo-controle-impacts/definition-combo.json"
BASE="/tmp/impact-test-formel"
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

# Preparation : mini-cerveau de test
rm -rf "$BASE"
mkdir -p "$BASE/agents/cerberus" "$BASE/pense-betes"
printf -- '---\nidentite:\n  type: fiche-agent\n  appartient_a: cerberus\n  commun: false\n---\n# Fiche Cerberus\n' > "$BASE/agents/cerberus/cerberus.md"
printf -- '---\nidentite:\n  type: corrections\n  appartient_a: cerberus\n  commun: false\n---\n# Corrections Cerberus\n' > "$BASE/agents/cerberus/corrections.md"
printf -- '---\nidentite:\n  type: protocole\n  appartient_a: commun\n  commun: true\n---\n# Protocole activation\n' > "$BASE/pense-betes/protocole-activation.md"

# PT1 : syntaxe py_compile + bash -n (les 2 outils)
python3 -m py_compile "$OUTIL_PY" > /dev/null 2>&1
verifier "PT1a py_compile detecter-impacts" $?
python3 -m py_compile "$MOTEUR_PY" > /dev/null 2>&1
verifier "PT1b py_compile combos-moteur" $?
bash -n "$OUTIL_SH"
verifier "PT1c bash -n detecter-impacts.sh" $?

# PT2 : parite --version py/sh
V1=$(python3 "$OUTIL_PY" x --version 2>&1)
V2=$(bash "$OUTIL_SH" x --version 2>&1)
if [ "$V1" = "$V2" ]; then verifier "PT2 parite --version" 0; else verifier "PT2 parite --version" 1; fi

# PT3 : detection fichier non commun (corrections impliquee)
python3 "$OUTIL_PY" "$BASE/agents/cerberus/cerberus.md" --racine "$BASE" > /tmp/di-scan.txt 2>&1
if grep -q "corrections.md" /tmp/di-scan.txt && grep -q "appartient_a=cerberus" /tmp/di-scan.txt; then
    verifier "PT3 detection implique non commun" 0
else
    verifier "PT3 detection implique non commun" 1
fi

# PT4 : statut NON MIS A JOUR (corrections plus vieille que la fiche modifiee)
touch "$BASE/agents/cerberus/corrections.md"
sleep 1
touch "$BASE/agents/cerberus/cerberus.md"
python3 "$OUTIL_PY" "$BASE/agents/cerberus/cerberus.md" --racine "$BASE" > /tmp/di-statut.txt 2>&1
if grep -q "NON MIS A JOUR" /tmp/di-statut.txt; then verifier "PT4 statut NON MIS A JOUR" 0; else verifier "PT4 statut NON MIS A JOUR" 1; fi

# PT5 : fichier commun detecte par reference
printf -- '---\nidentite:\n  type: regle\n  appartient_a: commun\n  commun: false\n---\n# Regle\nVoir protocole-activation.md\n' > "$BASE/pense-betes/regle-cite.md"
touch "$BASE/pense-betes/protocole-activation.md"
sleep 1
touch "$BASE/pense-betes/regle-cite.md"
python3 "$OUTIL_PY" "$BASE/pense-betes/protocole-activation.md" --racine "$BASE" > /tmp/di-commun.txt 2>&1
if grep -q "regle-cite.md" /tmp/di-commun.txt && grep -q "(reference)" /tmp/di-commun.txt; then
    verifier "PT5 fichier commun par reference" 0
else
    verifier "PT5 fichier commun par reference" 1
fi

# PT6 : fichier sans identite -> ERREUR code 2
printf '# pas d identite\n' > "$BASE/sans-identite.md"
python3 "$OUTIL_PY" "$BASE/sans-identite.md" --racine "$BASE" > /tmp/di-err1.txt 2>&1
CODE=$?
if [ "$CODE" = "2" ] && grep -q "ERREUR" /tmp/di-err1.txt; then verifier "PT6 sans identite -> code 2" 0; else verifier "PT6 sans identite -> code 2 (code=$CODE)" 1; fi

# PT7 : fichier introuvable -> ERREUR code 2
python3 "$OUTIL_PY" "$BASE/inexistant.md" --racine "$BASE" > /tmp/di-err2.txt 2>&1
CODE=$?
if [ "$CODE" = "2" ]; then verifier "PT7 introuvable -> code 2" 0; else verifier "PT7 introuvable -> code 2 (code=$CODE)" 1; fi

# PT8 : parite py/sh sur scan (comparer py ET sh au MEME instant)
python3 "$OUTIL_PY" "$BASE/agents/cerberus/cerberus.md" --racine "$BASE" > /tmp/di-parite-py.txt 2>&1
bash "$OUTIL_SH" "$BASE/agents/cerberus/cerberus.md" --racine "$BASE" > /tmp/di-parite-sh.txt 2>&1
if diff -q /tmp/di-parite-py.txt /tmp/di-parite-sh.txt > /dev/null 2>&1; then
    verifier "PT8 parite scan py/sh" 0
else
    verifier "PT8 parite scan py/sh" 1
fi

# PT9 : moteur --var + combo (interpolation {fichier})
python3 "$MOTEUR_PY" "$COMBO" --var fichier="$BASE/agents/cerberus/cerberus.md" > /tmp/di-combo.txt 2>&1
if grep -q "COMBO TERMINE" /tmp/di-combo.txt; then verifier "PT9 combo --var termine" 0; else verifier "PT9 combo --var termine" 1; fi

# PT10 : generateur compose la commande detecter-impacts
python3 cerveau-projet/agents/tools/generateurs/generateurs-commande/generateurs-commande.py \
    --commande detecter-impacts --reponses "fichier=cerveau-projet/agents/cerberus/cerberus.md" > /tmp/di-gen.txt 2>&1
if grep -q "detecter-impacts.py cerveau-projet/agents/cerberus/cerberus.md" /tmp/di-gen.txt; then
    verifier "PT10 generateur compose commande" 0
else
    verifier "PT10 generateur compose commande" 1
fi

# PT11 : ASCII 0 sur les fichiers de l'outil
for f in detecter-impacts.py detecter-impacts.sh detecter-impacts.md; do
    RES=$(python3 cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.py \
        "cerveau-projet/agents/tools/detecter/detecter-impacts/$f" 2>&1 | grep -c 'non-ASCII : 0')
    if [ "$RES" = "1" ]; then verifier "PT11 ASCII $f" 0; else verifier "PT11 ASCII $f" 1; fi
done

# PT12 : CAS REEL sans --racine - le fichier source est EXCLU des impliques (bug v0.1.0 corrige en v0.1.1)
REEL="cerveau-projet/agents/cerberus/cerberus.md"
if [ -f "$REEL" ]; then
    python3 "$OUTIL_PY" "$REEL" > /tmp/di-reel.txt 2>&1
    NB_SOURCE=$(grep -c "cerberus.md" /tmp/di-reel.txt)
    if [ "$NB_SOURCE" = "1" ] && grep -q "corrections.md" /tmp/di-reel.txt; then
        verifier "PT12 cas reel : source exclu + corrections detecte" 0
    else
        verifier "PT12 cas reel : source exclu + corrections detecte (source x$NB_SOURCE)" 1
    fi
else
    verifier "PT12 cas reel (fichier cerberus.md absent)" 1
fi

# PT13 : SCHEMA HYBRIDE - format .py (commentaires en tete, fenetre 12 lignes)
# PT13a : .py SANS bloc identite en tete -> ERREUR (faux positif elimine v0.2.0)
python3 "$OUTIL_PY" "$OUTIL_PY" > /tmp/di-py0.txt 2>&1
CODE=$?
if [ "$CODE" = "2" ] && grep -q "ERREUR" /tmp/di-py0.txt; then verifier "PT13a .py sans identite -> code 2 (faux positif elimine)" 0; else verifier "PT13a .py sans identite -> code 2 (code=$CODE)" 1; fi

# PT13b : .py AVEC bloc identite en commentaires (lignes 3-7) -> identite lue
printf '#!/usr/bin/env python3\n# outil-hybride.py\n# Version : 0.1.0\n# identite:\n#   type: outil\n#   appartient_a: cerberus\n#   commun: false\nimport sys\n' > "$BASE/agents/cerberus/outil-hybride.py"
python3 "$OUTIL_PY" "$BASE/agents/cerberus/outil-hybride.py" --racine "$BASE" > /tmp/di-py1.txt 2>&1
if grep -q "type=outil, appartient_a=cerberus" /tmp/di-py1.txt; then verifier "PT13b .py bloc identite lu" 0; else verifier "PT13b .py bloc identite lu" 1; fi

# PT13c : le .py est aussi detecte comme implique (meme appartient_a) depuis la fiche source
python3 "$OUTIL_PY" "$BASE/agents/cerberus/cerberus.md" --racine "$BASE" > /tmp/di-py2.txt 2>&1
if grep -q "outil-hybride.py" /tmp/di-py2.txt; then verifier "PT13c .py detecte comme implique" 0; else verifier "PT13c .py detecte comme implique" 1; fi

# PT13d : parite py/sh sur le format .py
python3 "$OUTIL_PY" "$BASE/agents/cerberus/outil-hybride.py" --racine "$BASE" > /tmp/di-py3.txt 2>&1
bash "$OUTIL_SH" "$BASE/agents/cerberus/outil-hybride.py" --racine "$BASE" > /tmp/di-py4.txt 2>&1
if diff -q /tmp/di-py3.txt /tmp/di-py4.txt > /dev/null 2>&1; then verifier "PT13d parite .py py/sh" 0; else verifier "PT13d parite .py py/sh" 1; fi

# PT14 : SCHEMA HYBRIDE - format .json (cle top-level identite)
printf '{\n  "identite": {\n    "type": "parcours",\n    "appartient_a": "cerberus",\n    "commun": false\n  },\n  "cases": {}\n}\n' > "$BASE/agents/cerberus/parcours-cerberus.json"
python3 "$OUTIL_PY" "$BASE/agents/cerberus/parcours-cerberus.json" --racine "$BASE" > /tmp/di-json1.txt 2>&1
if grep -q "type=parcours, appartient_a=cerberus" /tmp/di-json1.txt; then verifier "PT14a .json cle top-level lue" 0; else verifier "PT14a .json cle top-level lue" 1; fi

# PT14b : parite py/sh sur le format .json
python3 "$OUTIL_PY" "$BASE/agents/cerberus/parcours-cerberus.json" --racine "$BASE" > /tmp/di-json2.txt 2>&1
bash "$OUTIL_SH" "$BASE/agents/cerberus/parcours-cerberus.json" --racine "$BASE" > /tmp/di-json3.txt 2>&1
if diff -q /tmp/di-json2.txt /tmp/di-json3.txt > /dev/null 2>&1; then verifier "PT14b parite .json py/sh" 0; else verifier "PT14b parite .json py/sh" 1; fi

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
