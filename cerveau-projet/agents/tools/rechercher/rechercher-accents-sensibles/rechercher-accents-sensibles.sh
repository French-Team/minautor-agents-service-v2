#!/bin/bash
# rechercher-accents-sensibles.sh
# Recherche les caracteres non-ASCII dans les ZONES SENSIBLES uniquement :
#   - frontmatter YAML (blocs --- en tete des .md)
#   - noms de fichiers et dossiers
#   - blocs de code (``` ... ``` dans les .md)
#   - fichiers de code (.sh, .py, .js, etc. - fichier entier)
#   - liens relatifs [texte](chemin) dans les .md
# Mode : RECHERCHE ET RAPPORT UNIQUEMENT (jamais de correction)
# Version : 0.2.0-beta
# Statut : ebauche
# Optimisation : UN SEUL awk pour tout le projet (via find | xargs -0 awk)
#               = rapide meme sur Git Bash Windows (pas de fork par fichier)

# Configuration
VERSION="0.2.0-beta"
STATUT="ebauche"
EXCLUSIONS_DEFAUT="node_modules,.git,.agents,.backup,.tmp,dictionnaire-,exemples"
EXTENSIONS_DEFAUT="sh,py,js,json,yaml,yml,txt"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== rechercher-accents-sensibles v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] [DOSSIER]"
    echo ""
    echo "Options :"
    echo "  --zones <liste>     Zones a rechercher (separees par des virgules)"
    echo "                      Disponibles : frontmatter, noms, blocs, code, liens"
    echo "                      Defaut : toutes les zones"
    echo "  --extensions <liste> Extensions des fichiers de code (ex: sh,py,js)"
    echo "                      Defaut : ${EXTENSIONS_DEFAUT}"
    echo "  --exclure <liste>   Motifs de chemins a exclure"
    echo "  --verbose           Afficher le detail ligne par ligne"
    echo "  --help              Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 cerveau-projet/"
    echo "  $0 --zones frontmatter,liens cerveau-projet/"
    echo "  $0 --zones noms ."
    echo ""
    echo "NOTE : Cet outil ne modifie JAMAIS les fichiers. Il recherche et rapporte."
}

# Main
main() {
    local dossier="."
    local zones="frontmatter,noms,blocs,code,liens"
    local extensions="$EXTENSIONS_DEFAUT"
    local exclusions="$EXCLUSIONS_DEFAUT"
    local verbose="false"
    local help="false"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --zones)
                zones="$2"
                shift 2
                ;;
            --extensions)
                extensions="$2"
                shift 2
                ;;
            --exclure)
                exclusions="$2"
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
                dossier="$1"
                shift
                ;;
        esac
    done

    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi

    echo "=== Rechercher accents dans les zones sensibles ==="
    echo "Version : ${VERSION}"
    echo "Dossier : ${dossier}"
    echo "Zones : ${zones}"
    echo "Fichiers EXCEPTION VOLONTAIRE (dictionnaire-*) exclus automatiquement"
    echo ""

    if [ ! -d "$dossier" ]; then
        echo -e "${RED}[ERREUR] Le dossier n'existe pas : $dossier${NC}"
        exit 1
    fi

    # Construire la commande find (un seul passage, liste de fichiers)
    local cmd="find \"$dossier\" -type f"

    IFS=',' read -ra EXCL <<< "$exclusions"
    for motif in "${EXCL[@]}"; do
        [ -n "$motif" ] && cmd="$cmd -not -path \"*/$motif*\""
    done
    cmd="$cmd -print0"

    # UN SEUL awk pour tout le projet.
    # Les fichiers sont passes via xargs -0 : awk voit FILENAME et FNR par fichier.
    # Zone NOMS : verifie basename(FILENAME) une fois par fichier (FNR==1).
    # Zone FRONTMATTER / BLOCS / LIENS : uniquement pour les .md.
    # Zone CODE : uniquement pour les extensions de code.
    # NB awk : /\\.md$/ = point LITERAL (backslash-point). Ne PAS mettre \\\\.md
    #          (double backslash = backslash literal + wildcard, ne matche jamais).
    LC_ALL=C eval "$cmd" | xargs -0 awk -v zones="$zones" -v exts="$extensions" -v verbose="$verbose" '
        function nom_fichier(f) {
            n = split(f, parts, "/")
            return parts[n]
        }
        function finaliser_fichier(nom_affiche) {
            if (fichier_probleme == 1) {
                nb_fichiers_problemes++
                if (verbose != "true") {
                    printf "  [%s] %s\n", zones_touchees, nom_affiche
                }
            }
        }
        function toucher(zone) {
            fichier_probleme = 1
            nb_detections[zone]++
            if (index(zones_touchees, zone) == 0) {
                if (zones_touchees == "") zones_touchees = zone
                else zones_touchees = zones_touchees ", " zone
            }
        }
        FNR == 1 {
            # Finaliser le fichier precedent (passer son NOM, pas FILENAME courant)
            if (prev_fichier != "") finaliser_fichier(prev_fichier)
            prev_fichier = FILENAME
            fichier_probleme = 0
            zones_touchees = ""
            in_fm = 0
            in_bloc = 0
            nb_fichiers++
            nom = nom_fichier(FILENAME)

            # Determiner le mode : md ou code
            if (FILENAME ~ /\.md$/) mode = "md"
            else {
                mode = "autre"
                n_exts = split(exts, tab_exts, ",")
                for (i = 1; i <= n_exts; i++) {
                    if (FILENAME ~ ("\\." tab_exts[i] "$")) { mode = "code"; break }
                }
            }

            # ZONE NOMS : verifie une seule fois par fichier
            if (zones ~ /noms/ && nom ~ /[^ -~]/) {
                toucher("noms")
                if (verbose == "true") printf "  [noms] %s (nom du fichier) : %s\n", FILENAME, nom
            }

            # Ignorer les fichiers ni .md ni de code
            if (mode == "autre") { ignorer = 1; next }
            ignorer = 0
        }
        {
            if (ignorer == 1) next

            # ZONE CODE : fichier de code entier
            if (mode == "code") {
                if (zones ~ /code/ && $0 ~ /[^ -~]/) {
                    toucher("code")
                    if (verbose == "true") printf "  [code] %s (ligne %d) : %s\n", FILENAME, FNR, $0
                }
                next
            }

            # --- mode md ---
            # FRONTMATTER : bloc --- ... --- en tete
            if (zones ~ /frontmatter/ && FNR == 1 && $0 ~ /^---/) { in_fm = 1; next }
            if (in_fm == 1 && $0 ~ /^---/) { in_fm = 0; next }
            if (in_fm == 1 && $0 ~ /[^ -~]/) {
                toucher("frontmatter")
                if (verbose == "true") printf "  [frontmatter] %s (ligne %d) : %s\n", FILENAME, FNR, $0
            }

            # BLOCS DE CODE : lignes entre ``` et ```
            if (zones ~ /blocs/ && $0 ~ /^```/) { in_bloc = !in_bloc; next }
            if (in_bloc == 1 && $0 ~ /[^ -~]/) {
                toucher("blocs")
                if (verbose == "true") printf "  [blocs] %s (ligne %d) : %s\n", FILENAME, FNR, $0
            }

            # LIENS RELATIFS : extraire les chemins ](...)
            if (zones ~ /liens/) {
                ligne = $0
                while (match(ligne, /\]\([^)]*\)/)) {
                    chemin = substr(ligne, RSTART + 2, RLENGTH - 3)
                    if (chemin ~ /[^ -~]/) {
                        toucher("liens")
                        if (verbose == "true") printf "  [liens] %s (ligne %d) : %s\n", FILENAME, FNR, chemin
                    }
                    ligne = substr(ligne, RSTART + RLENGTH)
                }
            }
        }
        END {
            if (prev_fichier != "") finaliser_fichier(prev_fichier)
            total = nb_detections["frontmatter"] + nb_detections["noms"] + nb_detections["blocs"] + nb_detections["code"] + nb_detections["liens"]
            printf "\n=== Resume ===\n"
            printf "Total fichiers examines : %d\n", nb_fichiers
            printf "Fichiers avec accent en zone sensible : %d\n", nb_fichiers_problemes
            printf "Detections par zone :\n"
            printf "  frontmatter YAML : %d\n", nb_detections["frontmatter"]
            printf "  noms de fichiers : %d\n", nb_detections["noms"]
            printf "  blocs de code    : %d\n", nb_detections["blocs"]
            printf "  fichiers de code : %d\n", nb_detections["code"]
            printf "  liens relatifs   : %d\n", nb_detections["liens"]
            printf "  TOTAL            : %d\n", total
            printf "\n[INFO] Recherche seule : aucun fichier n a ete modifie.\n"
            printf "[INFO] Pour corriger : utiliser corriger-accents-zones-sensibles ou corriger-emojis, puis relancer.\n"
            if (nb_fichiers_problemes > 0) exit 1
        }
    '
    local code_awk=$?

    echo ""
    if [ "$code_awk" -ne 0 ]; then
        exit "$code_awk"
    fi
    exit 0
}

# Executer
main "$@"
