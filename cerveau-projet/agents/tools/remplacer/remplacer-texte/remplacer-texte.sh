#!/bin/bash
# remplacer-texte.sh
# Remplacer une liste de paires ancien->nouveau dans plusieurs fichiers d'un dossier.
# Version : 0.1.0-beta
# Statut : ebauche

VERSION="0.1.0-beta"
STATUT="ebauche"

# Configuration
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== remplacer-texte v${VERSION} ==="
    echo ""
    echo "Usage: $0 <dossier> 'ancien=nouveau' ['ancien2=nouveau2' ...] [OPTIONS]"
    echo ""
    echo "Options :"
    echo "  --dry-run             Simuler sans appliquer"
    echo "  --ext 'md,sh,py'      Extensions a traiter (defaut: md,sh,py)"
    echo "  --exclu-fichier NOM   Exclure un fichier (repetable)"
    echo "  --verbose             Afficher les details"
    echo "  --help                Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 dossier 'ancien=nouveau'"
    echo "  $0 dossier 'a=b' 'c=d' --dry-run"
    echo ""
}

# Verifier le nommage (regle immuable : dossier remplacer/ -> prefixe remplacer-)
verifier_nommage() {
    local script_nom=$(basename "$0" | sed 's/\.sh$//')
    [[ "$script_nom" == "outil-template" ]] && return 0
    local chemin_script=$(cd "$(dirname "$0")" 2>/dev/null && pwd)
    local categorie=$(basename "$(dirname "$chemin_script")")
    if [[ -z "$categorie" || "$categorie" == "." || "$categorie" == "/" ]]; then
        return 0
    fi
    if [[ "$script_nom" != "${categorie}-"* ]]; then
        echo -e "${RED}[ERREUR] Nommage invalide : $script_nom${NC}"
        echo -e "  Le nom doit commencer par '${categorie}-' (categorie: ${categorie}/)"
        exit 1
    fi
}

# Remplacer une paire dans un fichier (retourne 0 si modifie)
remplacer_paire() {
    local fichier="$1"
    local ancien="$2"
    local nouveau_texte="$3"
    if [ ! -f "$fichier" ]; then
        return 1
    fi
    # Utiliser python pour un remplacement litteral fiable (evite sed/regex)
    python3 -c "import io,sys; f=sys.argv[1]; c=io.open(f,encoding='utf-8').read(); n=c.replace(sys.argv[2],sys.argv[3]); io.open(f,'w',encoding='utf-8',newline='').write(n) if n!=c else None; sys.exit(0 if n!=c else 1)" "$fichier" "$ancien" "$nouveau_texte"
    return $?
}

executer() {
    local dossier="$1"
    shift
    local paires=()
    local dry_run="false"
    local verbose="false"
    local ext="md,sh,py"
    local exclu_fichiers="AGENTS-historique.md"
    local exclu_dossiers="exemples .git __pycache__"

    # Parser les arguments
    while [ $# -gt 0 ]; do
        case "$1" in
            --dry-run) dry_run="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --ext) ext="$2"; shift 2 ;;
            --exclu-fichier) exclu_fichiers="$exclu_fichiers $2"; shift 2 ;;
            --help) afficher_aide; exit 0 ;;
            *) paires+=("$1"); shift ;;
        esac
    done

    if [ ${#paires[@]} -eq 0 ]; then
        echo -e "${RED}[ERREUR] Aucune paire ancien=nouveau fournie${NC}"
        afficher_aide
        exit 1
    fi
    if [ ! -d "$dossier" ]; then
        echo -e "${RED}[ERREUR] Dossier introuvable: $dossier${NC}"
        exit 1
    fi

    # Construire la liste des fichiers (find + exclusions)
    local fichiers=""
    fichiers=$(find "$dossier" -type f 2>/dev/null | grep -v '/.git/' | grep -v '/__pycache__/' | grep -v '/exemples/')
    for ef in $exclu_fichiers; do
        fichiers=$(echo "$fichiers" | grep -v "/$ef$")
    done

    local analyses=0
    local modifies=0
    for f in $fichiers; do
        local ext_f="${f##*.}"
        # Verifier l'extension
        local ok="false"
        IFS=',' read -ra exts <<< "$ext"
        for e in "${exts[@]}"; do
            if [ "$ext_f" = "$e" ]; then ok="true"; fi
        done
        [ "$ok" = "false" ] && continue
        analyses=$((analyses+1))
        local avant=""
        local apres=""
        avant=$(cat "$f" 2>/dev/null)
        apres="$avant"
        for p in "${paires[@]}"; do
            local ancien="${p%%=*}"
            local nouveau_texte="${p#*=}"
            apres=$(python3 -c "import sys; print(sys.stdin.read().replace(sys.argv[1],sys.argv[2]), end='')" "$ancien" "$nouveau_texte" <<< "$apres")
        done
        if [ "$apres" != "$avant" ]; then
            modifies=$((modifies+1))
            if [ "$dry_run" = "true" ]; then
                echo -e "${YELLOW}[SERAIT MODIFIE]${NC} $f"
            else
                printf '%s' "$apres" > "$f"
                echo -e "${GREEN}[MODIFIE]${NC} $f"
            fi
        fi
    done

    echo "=== remplacer-texte v${VERSION} ==="
    echo "Fichiers analyses: $analyses | Modifies: $modifies"
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} Aucune modification appliquee"
    fi
}

# Verifier le nommage au demarrage (regle immuable)
verifier_nommage

if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    afficher_aide
    exit 0
fi
if [ -z "$1" ]; then
    afficher_aide
    exit 1
fi

executer "$@"
