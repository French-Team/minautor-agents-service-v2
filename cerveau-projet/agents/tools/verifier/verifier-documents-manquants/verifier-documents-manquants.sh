#!/bin/bash
# verifier-documents-manquants.sh
# Verifie que chaque script .sh ET .py a sa documentation .md et inversement.
# Version : 0.3.0
# Statut : prepare
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# VERIFIER-DOCUMENTS-MANQUANTS - OUTIL DE CONTROLE DES PAIRES
# ============================================================
# WRAPPER PUR (pattern documente) : toute la logique vit dans le .py,
# le .sh verifie le nommage puis delegue a python3 -- la parite des
# sorties est garantie PAR CONSTRUCTION (aucun doublon de logique).
# ============================================================

# Verifier le nommage (regle immuable)
verifier_nommage() {
    local script_nom=$(basename "$0" | sed 's/\.sh$//')
    [[ "$script_nom" == "outil-template" ]] && return 0
    local chemin_script=$(cd "$(dirname "$0")" 2>/dev/null && pwd)
    local categorie=$(basename "$(dirname "$chemin_script")")
    if [[ -z "$categorie" || "$categorie" == "." || "$categorie" == "/" ]]; then
        return 0
    fi
    if [[ "$script_nom" != "${categorie}-"* ]]; then
        echo "[ERREUR] Nommage invalide : $script_nom"
        echo "  Le nom doit commencer par '${categorie}-' (categorie: ${categorie}/)"
        exit 1
    fi
}

# Main : verifie le nommage puis delegue au .py (wrapper pur)
main() {
    verifier_nommage
    local script_dir=$(cd "$(dirname "$0")" && pwd)
    local py_script="$script_dir/verifier-documents-manquants.py"
    if [ ! -f "$py_script" ]; then
        echo "[ERREUR] verifier-documents-manquants.py introuvable a cote du .sh : $py_script"
        exit 1
    fi
    if ! command -v python3 >/dev/null 2>&1; then
        echo "[ERREUR] python3 est requis pour verifier-documents-manquants.sh (parite avec le .py)"
        exit 1
    fi
    exec python3 "$py_script" "$@"
}

main "$@"
