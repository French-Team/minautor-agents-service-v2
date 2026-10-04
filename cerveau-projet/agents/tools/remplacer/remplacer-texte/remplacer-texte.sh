#!/bin/bash
# remplacer-texte.sh
# Remplacer une liste de paires ancien->nouveau dans plusieurs fichiers d'un dossier.
# Version : 0.3.1
# Statut : prepare
#
# PERFORMANCE (round 2) : l'ancienne boucle bash lancait python3 par paire x
# fichier (2 paires x 30 fichiers = 60 process, 8.5s). Desormais la version
# bash delegue a UN SEUL appel du .py du meme dossier : meme resultat, meme
# comportement, ~50x plus rapide (0.16s). Parite py/sh par construction.

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.3.1"
STATUT="prepare"

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
    echo "  --exclu-dossier NOM   Exclure un dossier (repetable)"
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

# Delegation : UN SEUL appel python3 (performance ~50x, parite par construction)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/remplacer-texte.py"
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}[ERREUR] $PYTHON_SCRIPT introuvable${NC}"
    exit 1
fi

python3 "$PYTHON_SCRIPT" "$@"
exit $?
