#!/usr/bin/env bash
# verifier-coherence-agents.sh
# Parite shell du verificateur de coherence AGENTS.md vs fichiers reels.
# Version : 0.1.0
# Statut : prepare
# Ce script est un wrapper vers la version Python (meme logique).

set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    echo "=== verifier-coherence-agents v0.1.0 ==="
    echo "Verifie la coherence des blocs session d AGENTS.md vs fichiers reels."
    echo ""
    echo "Usage : verifier-coherence-agents.sh [options]"
    echo "Options :"
    echo "  --dry-run        Simuler sans rien modifier"
    echo "  --verbose        Afficher les details"
    echo "  --version        Afficher la version"
    echo "  --confirme-doc   Confirmer la lecture de la documentation"
    echo "  --agents-md <f>  Chemin vers AGENTS.md (defaut: racine du projet)"
    echo "  --seuil <n>      Code de sortie si incoherences (defaut 1)"
    echo "  --doc            Afficher le .md de documentation"
}

if [ "$#" -eq 0 ]; then
    usage
    exit 2
fi

case "$1" in
    --version)
        echo "verifier-coherence-agents v0.1.0"
        exit 0
        ;;
    --doc)
        python3 "$SCRIPT_DIR/verifier-coherence-agents.py" --doc
        exit $?
        ;;
esac

# Relayer vers la version Python : c'est elle qui porte la logique.
python3 "$SCRIPT_DIR/verifier-coherence-agents.py" "$@"
exit $?