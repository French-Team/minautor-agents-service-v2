#!/usr/bin/env bash
# executer-formulaire.sh
# Wrapper bash de executer-formulaire.py (parite .py/.sh).
# DECISION D6/D7 : l agent affiche le formulaire (--schema) puis fournit ses
# reponses dans un fichier JSON (--reponses <fichier>, anti-heredoc) ;
# l outil valide, compose et execute la commande a sa place.
set -eu

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$DIR/executer-formulaire.py" "$@"