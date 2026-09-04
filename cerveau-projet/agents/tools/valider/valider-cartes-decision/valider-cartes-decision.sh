#!/bin/bash
# valider-cartes-decision.sh
# Verifie que les agents respectent leur CARTE DE DECISION.
# Depuis la v0.2.0 (allegement des fiches), la carte de decision d'un agent est
# son PARCOURS JSON (agents/<agent>/parcours/parcours-<agent>.json) : c'est la
# SOURCE DE VERITE du guidage.
# Ce .sh est un WRAPPER : il transmet les arguments au .py (logique unique)
# pour garantir une parite stricte des sorties (pattern detecter-impacts).
# Proprietaire : Vulcain (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.5.0"

PY_SCRIPT="cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.py"

# Le .sh transmet tous les arguments au .py (source unique de la logique)
exec python3 "$PY_SCRIPT" "$@"
