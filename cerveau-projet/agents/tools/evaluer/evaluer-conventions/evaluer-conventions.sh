#!/bin/bash
# evaluer-conventions.sh
# Evalue le respect des conventions : nommage, ASCII, format
# Proprietaire : Themis (outil partage)
# Version : 0.2.0

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

afficher_aide() {
    echo "=== evaluer-conventions v${VERSION} ==="
    echo ""
    echo "Usage: $0 [DOSSIER]"
    echo ""
    echo "Evalue le respect des conventions."
    echo "Sortie : rapport markdown sur stdout."
}

total=0
ok=0
erreurs=0
avertissements=0

# Main
dossier="${1:-.}"

echo "=== evaluer-conventions v${VERSION} ==="
echo "Cible : $dossier"
echo ""

if [ ! -d "$dossier" ]; then
    echo -e "${RED}[ERREUR] Le dossier n'existe pas : $dossier${NC}"
    exit 1
fi

echo "# Rapport evaluer-conventions"
echo ""

# 1. Nommage des fichiers de contenu (statuts)
echo "## Nommage des statuts"
total=$((total + 1))
# Detecter les fichiers dont le NOM contient des caracteres non-ASCII
# (ex: .prepare-accentue. au lieu de .prepare.) via Python (fiable sur Git Bash)
nb_bad=$(find "$dossier/cerveau-projet" -name "*.md" -type f 2>/dev/null | python -c "
import sys
n = 0
for ligne in sys.stdin:
    nom = ligne.strip()
    if any(ord(c) > 127 for c in nom):
        n += 1
print(n)
")
if [ "$nb_bad" -gt 0 ]; then
    echo "| ERREUR | Fichiers avec accents dans les statuts | $nb_bad fichier(s) avec des caracteres non-ASCII dans le nom (ex: .prepare-accentue.) |"
    erreurs=$((erreurs + 1))
else
    echo "| OK | Fichiers avec accents dans les statuts | Aucun accent dans les noms de fichiers |"
    ok=$((ok + 1))
fi

# 2. Conformite ASCII
echo ""
echo "## Conformite ASCII (hors exceptions)"
total=$((total + 1))
nb_non_ascii=0
while IFS= read -r f; do
    basename_f=$(basename "$f")
    # Exclure les dictionnaires et le fichier de regles
    case "$basename_f" in
        dictionnaire-*.txt|regles-emojis-ascii.md) continue ;;
    esac
    # Exclure le dossier exemples
    case "$f" in
        */exemples/*) continue ;;
    esac
    if LC_ALL=C grep -q '[^[:print:][:space:]]' "$f" 2>/dev/null; then
        nb_non_ascii=$((nb_non_ascii + 1))
    fi
done < <(find "$dossier/cerveau-projet" -name "*.md" -o -name "*.sh" | head -200)

if [ "$nb_non_ascii" -gt 0 ]; then
    echo "| AVERTISSEMENT | Fichiers avec caracteres non-ASCII | $nb_non_ascii fichier(s) restant(s) |"
    avertissements=$((avertissements + 1))
else
    echo "| OK | Fichiers avec caracteres non-ASCII | Tous conformes |"
    ok=$((ok + 1))
fi

# 3. Bandeau EXCEPTION VOLONTAIRE
echo ""
echo "## Bandeaux EXCEPTION VOLONTAIRE"
total=$((total + 1))
dictionnaires_ok=0
for dico in $(find "$dossier/cerveau-projet" -name "dictionnaire-*.txt" -type f 2>/dev/null); do
    if grep -q "EXCEPTION VOLONTAIRE" "$dico" 2>/dev/null; then
        dictionnaires_ok=$((dictionnaires_ok + 1))
    else
        echo "| ERREUR | Bandeau manquant | \`$dico\` |"
        erreurs=$((erreurs + 1))
    fi
done
if [ "$dictionnaires_ok" -gt 0 ]; then
    echo "| OK | Bandeaux dictionnaires | $dictionnaires_ok dictionnaire(s) avec bandeau |"
    ok=$((ok + 1))
fi

# 4. Dossier exemples exclu des outils
echo ""
echo "## Exclusion du dossier exemples"
total=$((total + 1))
exclu_valider=$(grep -c "exemples" "$dossier/cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.sh" 2>/dev/null || true)
exclu_rechercher=$(grep -c "exemples" "$dossier/cerveau-projet/agents/tools/rechercher/rechercher-accents-sensibles/rechercher-accents-sensibles.sh" 2>/dev/null || true)
exclu_corriger=$(grep -c "exemples" "$dossier/cerveau-projet/agents/tools/corriger/corriger-emojis/corriger-emojis.sh" 2>/dev/null || true)
if [ "$exclu_valider" -gt 0 ] && [ "$exclu_rechercher" -gt 0 ] && [ "$exclu_corriger" -gt 0 ]; then
    echo "| OK | Exclusion exemples | 3 outils sur 3 excluent le dossier |"
    ok=$((ok + 1))
else
    echo "| ERREUR | Exclusion exemples | Un ou plusieurs outils n'excluent pas exemples |"
    erreurs=$((erreurs + 1))
fi

# 5. Format des fichiers agents (.md presents)
echo ""
echo "## Format des fichiers agents"
total=$((total + 1))
agents_avec_fiche=0
agents_sans_fiche=""
for agent in $(ls "$dossier/cerveau-projet/agents/" 2>/dev/null); do
    [ -d "$dossier/cerveau-projet/agents/$agent" ] || continue
    [ "$agent" = "tools" ] && continue
    if [ -f "$dossier/cerveau-projet/agents/$agent/$agent.md" ]; then
        agents_avec_fiche=$((agents_avec_fiche + 1))
    else
        agents_sans_fiche="$agents_sans_fiche $agent"
    fi
done
if [ -z "$agents_sans_fiche" ]; then
    echo "| OK | Fiches agents | $agents_avec_fiche agent(s) avec fiche |"
    ok=$((ok + 1))
else
    echo "| ERREUR | Fiches agents | Agents sans fiche :$agents_sans_fiche |"
    erreurs=$((erreurs + 1))
fi

# Resume
echo ""
echo "## Resume"
echo ""
echo "- Total elements verifies : $total"
echo "- OK : $ok"
echo "- Erreurs : $erreurs"
echo "- Avertissements : $avertissements"
echo ""
echo "Score conventions : $(( ok * 100 / total ))/100"
