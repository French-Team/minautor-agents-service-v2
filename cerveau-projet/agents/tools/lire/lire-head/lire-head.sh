#!/bin/bash
# lire-head.sh
# Lire le head (en-tete) de fichiers sans configurer le nombre de lignes.
# Version : 0.1.1
# Statut : ebauche

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.1.1"
STATUT="ebauche"

RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

afficher_aide() {
    echo "=== lire-head v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier> [fichier2 ...]"
    echo ""
    echo "Options :"
    echo "  --info-commune MOTIF   Chercher un motif dans chaque head"
    echo "  --lignes N             Forcer la lecture de N lignes"
    echo "  --max-lignes N         Borne de securite de la detection (defaut 100)"
    echo "  --verbose              Afficher les details"
    echo "  --dry-run              Simuler sans afficher le contenu"
    echo "  --version              Afficher la version"
    echo "  --help                 Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md"
    echo "  $0 fichier1.md fichier2.md fichier3.md --info-commune version"
    echo ""
}

# Le .sh est un WRAPPER : toute la logique vit dans le .py (parite garantie
# par construction, lecon valider-cartes-decision v0.3.0).
PY_SCRIPT="$(cd "$(dirname "$0")" && pwd)/lire-head.py"

main() {
    # Aide locale (le .py a aussi --aide)
    for arg in "$@"; do
        if [ "$arg" = "--help" ] || [ "$arg" = "-h" ]; then
            afficher_aide
            exit 0
        fi
        if [ "$arg" = "--version" ]; then
            echo "lire-head v${VERSION} (${STATUT})"
            exit 0
        fi
    done

    if [ ! -f "$PY_SCRIPT" ]; then
        echo -e "${RED}[ERREUR] Script python introuvable: $PY_SCRIPT${NC}"
        exit 2
    fi

    exec python3 "$PY_SCRIPT" "$@"
}

main "$@"
