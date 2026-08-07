#!/bin/bash
# test-001-detecter-usage-outils-externes.sh
# Tests formels v0.1.0 : detecter-usage-outils-externes (levier B - detection par traces)
# Signes detectes: BOM UTF-8, CRLF, non-ASCII. Parite .py / .sh.

# --- Protections -----------------------------------------------------------
PROTECTIONS_DIR="$(cd "$(dirname "$0")/../../../tester/protections" 2>/dev/null && pwd)"
if [ -z "$PROTECTIONS_DIR" ] || [ ! -d "$PROTECTIONS_DIR" ]; then
    PROTECTIONS_DIR="$(dirname "$0")/../../../tester/protections"
fi

source "$PROTECTIONS_DIR/tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh"
source "$PROTECTIONS_DIR/tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh"
source "$PROTECTIONS_DIR/tester-protection-blocage/tester-protection-blocage.sh"

OUTIL_PY="$(cd "$(dirname "$0")/.." && pwd)/detecter-usage-outils-externes.py"
OUTIL_SH="$(cd "$(dirname "$0")/.." && pwd)/detecter-usage-outils-externes.sh"
ESPACE="/tmp/test-detecter-usage"

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

preparer_espace() {
    rm -rf "$ESPACE"
    mkdir -p "$ESPACE/propre" "$ESPACE/crlf" "$ESPACE/accents" "$ESPACE/bom" "$ESPACE/multi" "$ESPACE/ignore" "$ESPACE/vide" "$ESPACE/sous/dossier"
    # 1. Fichier propre (ASCII + LF)
    printf '# Titre\n\nTexte ASCII en LF.\n' > "$ESPACE/propre/propre.md"
    # 2. Fichier CRLF
    printf '# Titre\r\n\r\nLigne avec CRLF.\r\n' > "$ESPACE/crlf/crlf.md"
    # 3. Fichier avec accents (non-ASCII)
    printf '# Titre avec accent\n' | sed 's/accent/\xc3\xa9/' > "$ESPACE/accents/accent.md"
    # 4. Fichier avec BOM
    printf '\xef\xbb\xbf# Titre avec BOM\n' > "$ESPACE/bom/bom.md"
    # 5. Fichier multi-signes (BOM + CRLF + accents)
    printf '\xef\xbb\xbf# Titre multi\r\navec accent \xc3\xa9\r\n' > "$ESPACE/multi/multi.md"
    # 6. Fichier sans extension supportee
    printf 'contenu binaire quelconque\n' > "$ESPACE/ignore/ignore.exe"
    # 7. Fichier dans sous-dossier (mode recursif)
    printf '# Sous dossier\n' > "$ESPACE/sous/dossier/sous.md"
}

echo "=== PREPARATION ==="
preparer_espace
echo "OK"

echo ""
echo "=== TESTS .py ==="

# Test 1: fichier propre -> PROPRE, exit 0
python3 "$OUTIL_PY" "$ESPACE/propre" > /tmp/due-py-1.txt 2>&1
RC1=$?
verifier "1. Fichier propre -> PROPRE (py)" "grep -q 'PROPRE' /tmp/due-py-1.txt"
verifier "2. Fichier propre -> exit 0 (py)" "[ $RC1 -eq 0 ]"
verifier "3. Fichier propre -> aucun SUSPECT (py)" "! grep -q 'SUSPECT' /tmp/due-py-1.txt"

# Test 2: fichier CRLF -> SUSPECT + CRLF, exit 1
python3 "$OUTIL_PY" "$ESPACE/crlf" > /tmp/due-py-2.txt 2>&1
RC2=$?
verifier "4. Fichier CRLF -> SUSPECT (py)" "grep -q 'SUSPECT' /tmp/due-py-2.txt"
verifier "5. Fichier CRLF -> signe CRLF (py)" "grep -q 'CRLF' /tmp/due-py-2.txt"
verifier "6. Fichier CRLF -> exit 1 (py)" "[ $RC2 -eq 1 ]"

# Test 3: fichier accents -> SUSPECT + non-ASCII, exit 1
python3 "$OUTIL_PY" "$ESPACE/accents" > /tmp/due-py-3.txt 2>&1
RC3=$?
verifier "7. Fichier accents -> SUSPECT (py)" "grep -q 'SUSPECT' /tmp/due-py-3.txt"
verifier "8. Fichier accents -> signe non-ASCII (py)" "grep -q 'non-ASCII' /tmp/due-py-3.txt"
verifier "9. Fichier accents -> exit 1 (py)" "[ $RC3 -eq 1 ]"

# Test 4: fichier BOM -> SUSPECT + BOM, exit 1
python3 "$OUTIL_PY" "$ESPACE/bom" > /tmp/due-py-4.txt 2>&1
RC4=$?
verifier "10. Fichier BOM -> SUSPECT (py)" "grep -q 'SUSPECT' /tmp/due-py-4.txt"
verifier "11. Fichier BOM -> signe BOM UTF-8 (py)" "grep -q 'BOM UTF-8' /tmp/due-py-4.txt"
verifier "12. Fichier BOM -> exit 1 (py)" "[ $RC4 -eq 1 ]"

# Test 5: fichier multi-signes -> SUSPECT avec les 3 signes
python3 "$OUTIL_PY" "$ESPACE/multi" > /tmp/due-py-5.txt 2>&1
RC5=$?
verifier "13. Multi-signes -> SUSPECT (py)" "grep -q 'SUSPECT' /tmp/due-py-5.txt"
verifier "14. Multi-signes -> BOM detecte (py)" "grep -q 'BOM UTF-8' /tmp/due-py-5.txt"
verifier "15. Multi-signes -> CRLF detecte (py)" "grep -q 'CRLF' /tmp/due-py-5.txt"
verifier "16. Multi-signes -> non-ASCII detecte (py)" "grep -q 'non-ASCII' /tmp/due-py-5.txt"
verifier "17. Multi-signes -> exit 1 (py)" "[ $RC5 -eq 1 ]"

# Test 6: fichier sans extension supportee -> ignore
python3 "$OUTIL_PY" "$ESPACE/ignore" > /tmp/due-py-6.txt 2>&1
RC6=$?
verifier "18. Extension non supportee -> ignore (py)" "! grep -q 'SUSPECT\|ignore.exe' /tmp/due-py-6.txt"
verifier "19. Extension non supportee -> exit 0 (py)" "[ $RC6 -eq 0 ]"

# Test 7: dossier vide -> verdict OK
python3 "$OUTIL_PY" "$ESPACE/vide" > /tmp/due-py-7.txt 2>&1
RC7=$?
verifier "20. Dossier vide -> aucun fichier analyse (py)" "grep -q 'Fichiers analyses : 0' /tmp/due-py-7.txt"
verifier "21. Dossier vide -> exit 0 (py)" "[ $RC7 -eq 0 ]"

# Test 8: cible inexistante -> ERREUR, exit 1
python3 "$OUTIL_PY" "$ESPACE/nexiste-pas" > /tmp/due-py-8.txt 2>&1
RC8=$?
verifier "22. Cible inexistante -> ERREUR (py)" "grep -q 'ERREUR' /tmp/due-py-8.txt"
verifier "23. Cible inexistante -> exit 1 (py)" "[ $RC8 -eq 1 ]"

# Test 10: mode --recursive -> trouve le fichier du sous-dossier
python3 "$OUTIL_PY" --recursive "$ESPACE/sous" > /tmp/due-py-10.txt 2>&1
RC10=$?
verifier "24. --recursive -> trouve sous.md (py)" "grep -q 'sous.md' /tmp/due-py-10.txt"
verifier "25. --recursive -> sous.md PROPRE (py)" "grep -q 'PROPRE' /tmp/due-py-10.txt"
verifier "26. --recursive -> exit 0 (py)" "[ $RC10 -eq 0 ]"

# Test 12: ASCII strict + LF sur l outil lui-meme (heredoc fiable)
python3 "$OUTIL_PY" --version > /dev/null 2>&1
python3 - "$OUTIL_PY" <<'PYEOF' > /dev/null 2>&1
import io, sys
c = io.open(sys.argv[1], 'rb').read()
sys.exit(0 if all(b < 128 for b in c) and b'\r\n' not in c else 1)
PYEOF
verifier "27. outil .py ASCII strict + LF" "[ $? -eq 0 ]"

echo ""
echo "=== TESTS .sh (parite) ==="

# Test 9a: parite sur le dossier propre
bash "$OUTIL_SH" "$ESPACE/propre" > /tmp/due-sh-1.txt 2>&1
SH_RC1=$?
verifier "28. Parite .sh: propre -> PROPRE" "grep -q 'PROPRE' /tmp/due-sh-1.txt"
verifier "29. Parite .sh: propre -> exit 0" "[ $SH_RC1 -eq 0 ]"

# Test 9b: parite sur le dossier multi
bash "$OUTIL_SH" "$ESPACE/multi" > /tmp/due-sh-2.txt 2>&1
SH_RC2=$?
verifier "30. Parite .sh: multi -> SUSPECT" "grep -q 'SUSPECT' /tmp/due-sh-2.txt"
verifier "31. Parite .sh: multi -> BOM detecte" "grep -q 'BOM UTF-8' /tmp/due-sh-2.txt"
verifier "32. Parite .sh: multi -> CRLF detecte" "grep -q 'CRLF' /tmp/due-sh-2.txt"
verifier "33. Parite .sh: multi -> non-ASCII detecte" "grep -q 'non-ASCII' /tmp/due-sh-2.txt"
verifier "34. Parite .sh: multi -> exit 1" "[ $SH_RC2 -eq 1 ]"

# Test 9c: parite sur le dossier crlf
bash "$OUTIL_SH" "$ESPACE/crlf" > /tmp/due-sh-3.txt 2>&1
SH_RC3=$?
verifier "35. Parite .sh: crlf -> SUSPECT" "grep -q 'SUSPECT' /tmp/due-sh-3.txt"
verifier "36. Parite .sh: crlf -> exit 1" "[ $SH_RC3 -eq 1 ]"

# Test 9d: parite cible inexistante
bash "$OUTIL_SH" "$ESPACE/nexiste-pas" > /tmp/due-sh-4.txt 2>&1
SH_RC4=$?
verifier "37. Parite .sh: cible inexistante -> ERREUR" "grep -q 'ERREUR' /tmp/due-sh-4.txt"
verifier "38. Parite .sh: cible inexistante -> exit 1" "[ $SH_RC4 -eq 1 ]"

# Test 11: regle de nommage (le nom commence par detecter-)
NOM_SH=$(basename "$OUTIL_SH")
verifier "39. Regle nommage .sh: prefixe detecter-" "[[ '$NOM_SH' == detecter-* ]]"
NOM_PY=$(basename "$OUTIL_PY")
verifier "40. Regle nommage .py: prefixe detecter-" "[[ '$NOM_PY' == detecter-* ]]"

# Test 12 bis: ASCII + LF sur le .sh (heredoc fiable)
python3 - "$OUTIL_SH" <<'PYEOF' > /dev/null 2>&1
import io, sys
c = io.open(sys.argv[1], 'rb').read()
sys.exit(0 if all(b < 128 for b in c) and b'\r\n' not in c else 1)
PYEOF
verifier "41. outil .sh ASCII strict + LF" "[ $? -eq 0 ]"

# Nettoyage
rm -rf "$ESPACE" /tmp/due-py-*.txt /tmp/due-sh-*.txt

echo ""
echo "=== RESUME ==="
echo "OK: $NB_OK | ECHEC: $NB_ECHEC"
if [ "$NB_ECHEC" -eq 0 ]; then
    echo "VERDICT: VALIDE (41/41)"
    exit 0
else
    echo "VERDICT: A CORRIGER ($NB_ECHEC echecs)"
    exit 1
fi
