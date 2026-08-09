#!/usr/bin/env bash
# -*- coding: ascii -*-
# generateurs-carte.sh
# Wrapper bash vers generateurs-carte.py (parite stricte).
# Version : 0.3.0
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
PY_SCRIPT="$SCRIPT_DIR/generateurs-carte.py"

if [ ! -f "$PY_SCRIPT" ]; then
    echo "ERREUR: $PY_SCRIPT introuvable" >&2
    exit 1
fi

exec python3 "$PY_SCRIPT" "$@"
