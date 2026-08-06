#!/bin/bash
# corriger-emojis.sh
# Detecte et remplace les emojis par des symboles ASCII
# Proprietaire : Vulcain (outil partage)
# Version : 0.2.0
# Optimisation : une passe unique python (le dictionnaire est lu une fois,
#                les remplacements appliques en un seul passage par fichier)

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
VERBOSE=false
DRY_RUN=false
DOSSIER="."
FICHIER=""

# Chemin vers le dictionnaire
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DICTIONNAIRE="$SCRIPT_DIR/dictionnaire-emojis.txt"

# Afficher l'aide
afficher_aide() {
    echo "Usage: $0 <fichier|dossier> [options]"
    echo ""
    echo "Detecte et remplace les emojis par des symboles ASCII (une passe unique)."
    echo ""
    echo "Options:"
    echo "  --dry-run     Afficher les changements sans les appliquer"
    echo "  --verbose     Afficher les details"
    echo "  --aide        Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 fichier.md"
    echo "  $0 --dry-run fichier.md"
    echo "  $0 cerveau-projet/"
    echo "  $0 --dry-run cerveau-projet/"
}

# Fonction python unique : lire le dictionnaire, detecter et remplacer.
# Arguments : $1 = fichier, $2 = "detect" ou "corriger"
executer_python() {
    local fichier=$1
    local mode=$2
    local dry_flag="0"
    [ "$DRY_RUN" = true ] && dry_flag="1"
    local verb_flag="0"
    [ "$VERBOSE" = true ] && verb_flag="1"

    python - "$DICTIONNAIRE" "$fichier" "$mode" "$dry_flag" "$verb_flag" <<'PYEOF'
import io, sys, os

# Forcer UTF-8 sur stdout (console Windows cp1252 sinon)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

dict_file, fichier, mode = sys.argv[1], sys.argv[2], sys.argv[3]
dry_run = (sys.argv[4] == "1")
verbose = (sys.argv[5] == "1")

# Lire le dictionnaire : lignes "EMOJI|REMPLACEMENT" (ignorer # et vides)
replacements = []
with io.open(dict_file, encoding="utf-8") as df:
    for line in df:
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            emoji, repl = line.split("|", 1)
            if emoji:
                replacements.append((emoji, repl))

# Lire le fichier
with io.open(fichier, encoding="utf-8") as f:
    content = f.read()

# Detecter les emojis presents
present = []
for emoji, repl in replacements:
    if emoji in content:
        present.append((emoji, repl, content.count(emoji)))

if not present:
    if verbose:
        print("[OK] aucun emoji detecte")
    sys.exit(0)

# Lister les emojis trouves
print("[ATTENTION] emojis detectes :")
for emoji, repl, n in present:
    print("  {} (x{}) -> {}".format(emoji, n, repl))

if dry_run:
    print("[DRY-RUN] Changements non appliques")
    sys.exit(0)

# Appliquer les remplacements (le plus long d'abord pour eviter les conflits)
for emoji, repl, n in sorted(present, key=lambda x: -len(x[0])):
    content = content.replace(emoji, repl)

# Ecrire le resultat (pas de .bak : l'outil est confirme fonctionnel)
with io.open(fichier, "w", encoding="utf-8", newline="") as f:
    f.write(content)

print("[OK] {} emoji(s) remplace(s)".format(len(present)))
PYEOF
}

# Fonction : traiter un fichier
traiter_fichier() {
    local fichier=$1

    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve : $fichier${NC}"
        return 1
    fi

    executer_python "$fichier" "corriger"
}

# Fonction principale
corriger_emojis() {
    local cible=$1

    echo -e "${BLUE}=== Correction des emojis ===${NC}"
    echo "Cible : $cible"
    echo "Dictionnaire : $DICTIONNAIRE"
    echo ""

    # Verifier que le dictionnaire existe
    if [ ! -f "$DICTIONNAIRE" ]; then
        echo -e "${RED}[ERREUR] Dictionnaire non trouve : $DICTIONNAIRE${NC}"
        exit 1
    fi

    if [ -f "$cible" ]; then
        traiter_fichier "$cible"
    elif [ -d "$cible" ]; then
        local nb_fichiers=0
        local nb_modifies=0
        local nb_errores=0

        while IFS= read -r fichier; do
            nb_fichiers=$((nb_fichiers + 1))
            local resultat
            resultat=$(executer_python "$fichier" "corriger" 2>&1)
            local code=$?
            if echo "$resultat" | grep -q "emoji(s) remplace(s)"; then
                nb_modifies=$((nb_modifies + 1))
            elif [ "$code" -ne 0 ]; then
                nb_errores=$((nb_errores + 1))
                echo "$resultat" | tail -2
            fi
        done < <(find "$cible" \( -name "*.md" -o -name "*.sh" \) -type f -not -path "*/exemples/*" 2>/dev/null)

        echo ""
        echo -e "${BLUE}=== Resumer ===${NC}"
        echo "Fichiers analyses : $nb_fichiers"
        echo "Fichiers modifies : $nb_modifies"
        echo "Erreurs : $nb_errores"
    else
        echo -e "${RED}[ERREUR] Cible non trouvee : $cible${NC}"
        exit 1
    fi

    echo ""
    echo -e "${GREEN}=== Termine ===${NC}"
}

# Parser les arguments
while [ $# -gt 0 ]; do
    case $1 in
        "--aide"|"--help"|"-h")
            afficher_aide
            exit 0
            ;;
        "--verbose")
            VERBOSE=true
            shift
            ;;
        "--dry-run")
            DRY_RUN=true
            shift
            ;;
        *)
            if [ -z "$FICHIER" ]; then
                FICHIER="$1"
            fi
            shift
            ;;
    esac
done

# Verifier les arguments
if [ -z "$FICHIER" ]; then
    echo -e "${RED}[ERREUR] Aucune cible specifiee${NC}"
    afficher_aide
    exit 1
fi

# Corriger les emojis
corriger_emojis "$FICHIER"
