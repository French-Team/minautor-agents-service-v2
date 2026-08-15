#!/bin/bash
# rechercher-fichier.sh
# Verifier si un fichier existe
# Version : 0.2.0-beta
# Statut : ebauche

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
STATUT="prepare"

afficher_aide() {
    echo "=== rechercher-fichier v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] <fichier>"
    echo ""
    echo "Retourne 0 si le fichier existe, 1 sinon."
    echo ""
    echo "Options :"
    echo "  --verbose   Afficher le resultat"
    echo "  --help      Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 fichier.md && echo \"Existe\""
    echo "  if $0 fichier.md; then echo \"OK\"; fi"
    echo ""
}

# Main
main() {
    local fichier=""
    local verbose="false"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            *) fichier="$1"; shift ;;
        esac
    done
    
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    if [ -z "$fichier" ]; then
        echo "ERREUR: Aucun fichier specifie" >&2
        exit 1
    fi
    
    if [ -f "$fichier" ]; then
        if [ "$verbose" = "true" ]; then
            echo "EXiste: $fichier"
        fi
        exit 0
    else
        if [ "$verbose" = "true" ]; then
            echo "Inexistant: $fichier"
        fi
        exit 1
    fi
}

main "$@"