#!/usr/bin/env bash
# -*- coding: ascii -*-
# generateurs-case.sh
# Wrapper bash vers generateurs-case.py (parite stricte par construction).
# Version : 0.4.2
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom DOIT commencer par le
# prefixe du dossier de categorie (generateurs-) : controle au demarrage.
# REGLE IMMUABLE : ASCII strict (aucun accent, emoji ou Unicode).
# ============================================================

# Chemin absolu du script Python (5 remontees depuis ce fichier)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/generateurs-case.py"

if [ ! -f "$PY_SCRIPT" ]; then
    echo "ERREUR: $PY_SCRIPT introuvable" >&2
    exit 1
fi

exec python3 "$PY_SCRIPT" "$@"
