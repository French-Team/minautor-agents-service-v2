#!/bin/bash
# corriger-dictionnaire-accents.sh
# Outil pour detecter et corriger les accents et caracteres non-ASCII
# Conforme a la regle regles-emojis-ascii.md
# Version : 0.3.0 (refonte python pour compatibilite Git Bash)

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Repertoire de l'outil
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DICTIONNAIRE_DEFAUT="${SCRIPT_DIR}/corriger-dictionnaire-accents.txt"

# Fonction d'aide
utilisation() {
    echo "Utilisation: $0 [OPTIONS] <fichier>"
    echo ""
    echo "Options:"
    echo "  --dry-run        Afficher les changements sans les appliquer"
    echo "  --verbose        Afficher les details"
    echo "  --dictionnaire   Chemin vers le dictionnaire"
    echo "  --help           Afficher cette aide"
}

# Parametres
DRY_RUN=0
VERBOSE=0
DICTIONNAIRE="$DICTIONNAIRE_DEFAUT"
FICHIER=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=1; shift ;;
        --verbose) VERBOSE=1; shift ;;
        --dictionnaire) DICTIONNAIRE="$2"; shift 2 ;;
        --help|-h) utilisation; exit 0 ;;
        -*) echo -e "${RED}[ERREUR] Option inconnue: $1${NC}"; exit 1 ;;
        *) FICHIER="$1"; shift ;;
    esac
done

if [[ -z "$FICHIER" ]]; then
    echo -e "${RED}[ERREUR] Aucun fichier specifie${NC}"
    utilisation
    exit 1
fi

if [[ ! -f "$FICHIER" ]]; then
    echo -e "${RED}[ERREUR] Fichier non trouve: $FICHIER${NC}"
    exit 1
fi

if [[ ! -f "$DICTIONNAIRE" ]]; then
    echo -e "${RED}[ERREUR] Dictionnaire non trouve: $DICTIONNAIRE${NC}"
    exit 1
fi

echo "[INFO] Correction des accents et caracteres non-ASCII"
echo "Fichier: $FICHIER"
echo "Dictionnaire: $DICTIONNAIRE"
echo ""

# Execution via python (evite les problemes d'encodage bash/perl sur Git Bash)
python - "$DICTIONNAIRE" "$FICHIER" "$DRY_RUN" "$VERBOSE" <<'PYEOF'
import io, sys, os, difflib

dict_file = sys.argv[1]
fichier = sys.argv[2]
dry_run = (sys.argv[3] == "1")
verbose = (sys.argv[4] == "1")

# Lire le dictionnaire (lignes "accent|remplacement", ignorer # et vides)
replacements = []
with io.open(dict_file, encoding="utf-8") as df:
    for line in df:
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            accent, repl = line.split("|", 1)
            if accent:
                replacements.append((accent, repl))

# Lire le fichier
with io.open(fichier, encoding="utf-8") as f:
    original = f.read()

content = original

# Appliquer les remplacements
total_changes = 0
for accent, repl in replacements:
    count = content.count(accent)
    if count > 0:
        content = content.replace(accent, repl)
        total_changes += count
        if verbose:
            print("[OK] Remplace: '{}' -> '{}' ({} lignes)".format(accent, repl, count))

# Compter les non-ASCII restants
non_ascii = sum(1 for c in content if ord(c) > 127)

if dry_run:
    if total_changes > 0:
        # Afficher les differences
        diff = list(difflib.unified_diff(
            original.splitlines(True),
            content.splitlines(True),
            fromfile=fichier,
            tofile=fichier + " (corrige)",
            lineterm=""
        ))
        for line in diff[:50]:
            print(line)
        if len(diff) > 50:
            print("... ({} lignes de diff en plus)".format(len(diff) - 50))
    print("")
    print("[INFO] Total: {} lignes modifiees".format(total_changes))
    print("[INFO] Caracteres non-ASCII restants: {}".format(non_ascii))
    print("[INFO] Aucune modification appliquee (dry-run)")
else:
    if total_changes > 0:
        # Sauvegarde
        backup = fichier + ".bak"
        with io.open(backup, "w", encoding="utf-8", newline="") as f:
            f.write(original)
        # Application
        with io.open(fichier, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        print("[OK] {} lignes modifiees".format(total_changes))
        print("[INFO] Sauvegarde creee: {}".format(backup))
        print("[INFO] Caracteres non-ASCII restants: {}".format(non_ascii))
    else:
        print("[OK] Aucun accent ou caractere non-ASCII detecte")
PYEOF
