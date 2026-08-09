#!/usr/bin/env bash
# verifier-restauration-sure.sh
# Wrapper : delegue au .py (parite py/sh)
# Detecte les fichiers non commites avant toute restauration git (regle Restauration securisee)

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$DIR/verifier-restauration-sure.py" "$@"
