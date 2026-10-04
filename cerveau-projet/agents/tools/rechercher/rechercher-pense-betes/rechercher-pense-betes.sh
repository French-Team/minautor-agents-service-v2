#!/bin/bash
# rechercher-pense-betes.sh
# Outil pour rechercher les pense-betes existants et eviter les doublons
# Version : 0.2.0

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
STATUT="ebauche"
PREFIX="pense-bete"
LABEL="pense-betes"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== rechercher-pense-betes v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options :"
    echo "  --theme <motif>   Rechercher les pense-betes dont le theme est identique ou proche"
    echo "  --tous            Lister tous les pense-betes existants (inventaire complet)"
    echo "  --dossier <chemin> Dossier de recherche (defaut: racine du projet)"
    echo "  --verbose         Afficher les details de correspondance"
    echo "  --help            Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 --tous                              # Inventaire complet"
    echo "  $0 --theme pipeline                    # Chercher les doublons du theme pipeline"
    echo "  $0 --theme pipeline --verbose          # Avec details de similarite"
    echo ""
}

# Extraire le theme d'un fichier (la partie apres le prefixe, avant le premier point)
extraire_theme() {
    local fichier="$1"
    local nom_base=$(basename "$fichier")
    echo "$nom_base" | sed "s/^${PREFIX}-//; s/\..*$//"
}

# Extraire le statut d'un fichier (la partie avant .md)
extraire_statut() {
    local fichier="$1"
    local nom_base=$(basename "$fichier")
    echo "$nom_base" | sed 's/.*\.\([a-z-]*\)\.md$/\1/'
}

# Normaliser un theme pour la comparaison (minuscules, _ et espaces -> -)
normaliser() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | tr '_ ' '--' | tr -s '-'
}

# Verifier si un theme correspond au motif (exact, partiel, ou mots-cles partages)
correspond() {
    local motif="$1"
    local theme="$2"
    if [ "$motif" = "$theme" ]; then
        echo "EXACT"
        return 0
    fi
    if [[ "$theme" == *"$motif"* ]] || [[ "$motif" == *"$theme"* ]]; then
        echo "PROCHE"
        return 0
    fi
    # Mots-cles partages (longueur >= 4)
    for mot in $(echo "$motif" | tr '-' ' '); do
        if [ ${#mot} -ge 4 ]; then
            if echo "$theme" | tr '-' ' ' | grep -qw "$mot"; then
                echo "PARTIEL"
                return 0
            fi
        fi
    done
    echo "AUCUN"
    return 1
}

# Main
main() {
    local motif=""
    local tous="false"
    local dossier="."
    local verbose="false"
    local help="false"

    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --theme)
                motif="$2"
                shift 2
                ;;
            --tous)
                tous="true"
                shift
                ;;
            --dossier)
                dossier="$2"
                shift 2
                ;;
            --verbose)
                verbose="true"
                shift
                ;;
            --help)
                help="true"
                shift
                ;;
            *)
                echo -e "${RED}[ERREUR] Option inconnue : $1${NC}"
                afficher_aide
                exit 1
                ;;
        esac
    done

    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi

    if [ ! -d "$dossier" ]; then
        echo -e "${RED}[ERREUR] Le dossier n'existe pas : $dossier${NC}"
        exit 1
    fi

    # Recueillir tous les pense-betes (fichiers <prefixe>-*.md, hors templates et index)
    local fichiers=()
    while IFS= read -r f; do
        local base=$(basename "$f")
        case "$base" in
            *-template.md|index-*) continue ;;
            *) fichiers+=("$f") ;;
        esac
    done < <(find "$dossier" -type f -name "${PREFIX}-*.md" -not -path "*/.git/*" -not -path "*/node_modules/*" 2>/dev/null)

    if [ ${#fichiers[@]} -eq 0 ]; then
        echo -e "${YELLOW}[ATTENTION] Aucun ${LABEL} trouve${NC}"
        exit 0
    fi

    # Mode inventaire complet
    if [ "$tous" = "true" ] || [ -z "$motif" ]; then
        echo "=== Inventaire des ${LABEL} ==="
        echo "Dossier : ${dossier}"
        echo ""
        printf "  %-40s %-30s %s\n" "THEME" "FICHIER" "STATUT"
        echo "  -----------------------------------------------------------------------"
        local nb=0
        for f in "${fichiers[@]}"; do
            local theme=$(extraire_theme "$f")
            local statut=$(extraire_statut "$f")
            printf "  %-40s %-30s %s\n" "$theme" "$(basename "$f")" "$statut"
            nb=$((nb + 1))
        done
        echo ""
        echo -e "Total : ${GREEN}${nb}${NC} ${LABEL}"
        exit 0
    fi

    # Mode anti-doublon (avec motif)
    local motif_norm=$(normaliser "$motif")
    echo "=== Recherche anti-doublon : theme '${motif}' ==="
    echo ""
    local trouves=0
    for f in "${fichiers[@]}"; do
        local theme=$(extraire_theme "$f")
        local theme_norm=$(normaliser "$theme")
        local resultat=$(correspond "$motif_norm" "$theme_norm")
        if [ "$resultat" != "AUCUN" ]; then
            trouves=$((trouves + 1))
            case "$resultat" in
                EXACT)
                    echo -e "  ${RED}[EXACT]${NC} ${theme} -> $(basename "$f")" ;;
                PROCHE)
                    echo -e "  ${YELLOW}[PROCHE]${NC} ${theme} -> $(basename "$f")" ;;
                PARTIEL)
                    echo -e "  ${BLUE}[PARTIEL]${NC} ${theme} -> $(basename "$f")" ;;
            esac
            if [ "$verbose" = "true" ]; then
                echo -e "        motif: '${motif}' | theme: '${theme}' | score: ${resultat}"
            fi
        fi
    done

    echo ""
    if [ "$trouves" -eq 0 ]; then
        echo -e "${GREEN}[OK] Aucun doublon trouve pour le theme '${motif}'. Vous pouvez creer le fichier.${NC}"
        exit 0
    else
        echo -e "${YELLOW}[ATTENTION] ${trouves} correspondance(s) trouvee(s). Verifiez avant de creer.${NC}"
        if [ "$trouves" -ge 1 ]; then
            echo -e "${RED}-> Ne pas creer si un [EXACT] ou [PROCHE] existe deja.${NC}"
        fi
        exit 1
    fi
}

# Executer
main "$@"
