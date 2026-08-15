#!/bin/bash
# mettre-a-jour-readme.sh
# Outil pour corriger le README afin qu'il reflete l'etat reel du projet
# Version : 0.4.2
# Statut : ebauche
# Proprietaire : Clio (agent dedie au README)

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.4.2"
STATUT="ebauche"
README="README.md"
HISTORIQUE="AGENTS-historique.md"
AGENTS_DIR="cerveau-projet/agents"
TOOLS_DIR="cerveau-projet/agents/tools"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== mettre-a-jour-readme v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options :"
    echo "  --verifier         Comparer l'etat reel au README, lister les ecarts (sans modifier)"
    echo "  --maj              Corriger le texte du README (agents, outils, compteurs)"
    echo "  --journal [N]      Consulter les N dernieres interventions (diagnostic, non inscrit au README)"
    echo "  --logo CHEMIN      Inserer une image (logo) en tete du README, apres le titre H1"
    echo "  --badges SPEC      Inserer des badges statiques Shields (label=message:couleur;...), apres le titre H1"
    echo "  --agents           Afficher le compte reel des agents"
    echo "  --outils           Afficher le compte reel des outils par categorie"
    echo "  --help             Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 --verifier                    # Apercu des ecarts"
    echo "  $0 --maj                         # Corriger le README"
    echo "  $0 --journal 5                   # 5 dernieres interventions"
    echo "  $0 --logo cerveau-projet/assets/images/logo.jpg   # Inserer un logo en tete"
    echo "  $0 --badges \"Plateforme=Windows:blue;Statut=stable:brightgreen\"   # Inserer des badges"
    echo ""
}

# Compter les agents reels (dossiers dans agents/, hors tools)
compter_agents() {
    local nb=0
    for d in "$AGENTS_DIR"/*/; do
        [ -d "$d" ] || continue
        local nom=$(basename "$d")
        [ "$nom" != "tools" ] || continue
        # Un agent d action a un parcours JSON : agents/<nom>/parcours/parcours-<nom>.json
        [ -f "$AGENTS_DIR/$nom/parcours/parcours-$nom.json" ] || continue
        nb=$((nb + 1))
    done
    echo "$nb"
}

# Lister les agents reels (noms des dossiers)
lister_agents_reels() {
    for d in "$AGENTS_DIR"/*/; do
        [ -d "$d" ] || continue
        local nom=$(basename "$d")
        [ "$nom" != "tools" ] || continue
        # Un agent d action a un parcours JSON : agents/<nom>/parcours/parcours-<nom>.json
        [ -f "$AGENTS_DIR/$nom/parcours/parcours-$nom.json" ] || continue
        echo "$nom"
    done
}

# Lire le role specifique d'un agent depuis sa fiche
lire_role_agent() {
    local agent="$1"
    local fiche="$AGENTS_DIR/$agent/$agent.md"
    if [ -f "$fiche" ]; then
        grep -E '^[[:space:]]*role_specifique:' "$fiche" | head -1 | sed 's/.*: *//; s/["'"'"']//g' | tr -d '\r'
    fi
}

# Compter les outils d'une categorie (chaque outil = un sous-dossier)
compter_outils_categorie() {
    local categorie="$1"
    local dir="$TOOLS_DIR/$categorie"
    local nb=0
    # Cas special templates : outil-template (fichiers a la racine de tools/)
    if [ "$categorie" = "templates" ]; then
        [ -f "$TOOLS_DIR/outil-template.md" ] && nb=1
        echo "$nb"
        return
    fi
    if [ ! -d "$dir" ]; then
        echo 0
        return
    fi
    # Cas special tester : compter les protections dans tester/protections/
    if [ "$categorie" = "tester" ]; then
        for d in "$dir/protections"/*/; do
            [ -d "$d" ] && nb=$((nb + 1))
        done
        echo "$nb"
        return
    fi
    # Cas special combos : compter les sous-dossiers
    if [ "$categorie" = "combos" ]; then
        for d in "$dir"/*/; do
            [ -d "$d" ] && nb=$((nb + 1))
        done
        echo "$nb"
        return
    fi
    for d in "$dir"/*/; do
        [ -d "$d" ] && nb=$((nb + 1))
    done
    echo "$nb"
}

# Lister les outils reels d'une categorie (noms des sous-dossiers, separes par ', ')
lister_outils_categorie() {
    local categorie="$1"
    local dir="$TOOLS_DIR/$categorie"
    local liste=""
    # Cas special templates
    if [ "$categorie" = "templates" ]; then
        [ -f "$TOOLS_DIR/outil-template.md" ] && echo "outil-template"
        return
    fi
    if [ ! -d "$dir" ]; then
        echo ""
        return
    fi
    # Cas special tester : lister les protections
    if [ "$categorie" = "tester" ]; then
        local first=""
        for d in "$dir/protections"/*/; do
            [ -d "$d" ] || continue
            local nom=$(basename "$d")
            if [ -z "$first" ]; then
                liste="$nom"
                first="1"
            else
                liste="${liste}, ${nom}"
            fi
        done
        echo "$liste"
        return
    fi
    # Cas special combos : lister les sous-dossiers
    if [ "$categorie" = "combos" ]; then
        local first=""
        for d in "$dir"/*/; do
            [ -d "$d" ] || continue
            local nom=$(basename "$d")
            if [ -z "$first" ]; then
                liste="$nom"
                first="1"
            else
                liste="${liste}, ${nom}"
            fi
        done
        echo "$liste"
        return
    fi
    local first=""
    for d in "$dir"/*/; do
        [ -d "$d" ] || continue
        local nom=$(basename "$d")
        if [ -z "$first" ]; then
            liste="$nom"
            first="1"
        else
            liste="${liste}, ${nom}"
        fi
    done
    echo "$liste"
}

# Lister les categories d'outils (chaque sous-dossier, plus tester et templates)
lister_categories() {
    for d in "$TOOLS_DIR"/*/; do
        [ -d "$d" ] || continue
        local nom=$(basename "$d")
        case "$nom" in
            combos) continue ;;
        esac
        echo "$nom"
    done
    # Categories speciales
    echo "combos"
    echo "templates"
}

# Total des outils
compter_total_outils() {
    local total=0
    for cat in $(lister_categories); do
        total=$((total + $(compter_outils_categorie "$cat")))
    done
    echo "$total"
}

# Lire les N dernieres interventions de l'historique (diagnostic uniquement)
lire_journal() {
    local n="${1:-10}"
    grep '^| 20' "$HISTORIQUE" 2>/dev/null | head -n "$n"
}

# Verifier l'etat reel et comparer avec le README
verifier() {
    echo "=== ETAT REEL DU PROJET ==="
    echo ""
    echo "Agents reels : $(compter_agents)"
    echo ""
    echo "Outils par categorie :"
    local total=0
    for cat in $(lister_categories); do
        local nb=$(compter_outils_categorie "$cat")
        printf "  %-14s : %s\n" "$cat" "$nb"
        total=$((total + nb))
    done
    echo "  TOTAL         : ${total}"
    echo ""
    echo "=== ECARTS AVEC LE README ==="
    echo ""

    # Agents manquants dans la table du README (casse insensible)
    local ecart=0
    for agent in $(lister_agents_reels); do
        if ! grep -qi "\*\*${agent}\*\*" "$README"; then
            echo -e "  ${RED}[MANQUANT]${NC} Agent '${agent}' absent de la table 'Les agents'"
            ecart=$((ecart + 1))
        fi
    done
    if [ "$ecart" -eq 0 ]; then
        echo -e "  ${GREEN}[OK]${NC} Tous les agents sont dans la table"
    fi

    # Titre boite a outils
    local titre_actuel=$(grep -o '^## La boite a outils ([0-9]* outils)' "$README" | grep -o '[0-9]*' | head -1)
    if [ -n "$titre_actuel" ] && [ "$titre_actuel" != "$total" ]; then
        echo -e "  ${RED}[OBSOLETE]${NC} Titre : 'La boite a outils ($titre_actuel outils)' -> devrait etre $total"
    else
        echo -e "  ${GREEN}[OK]${NC} Titre 'La boite a outils ($titre_actuel outils)'"
    fi

    # Compteurs et outils par categorie (capitaliser les noms de categories)
    for cle in $(lister_categories); do
        local cat=$(echo "${cle:0:1}" | tr '[:lower:]' '[:upper:]')${cle:1}
        cat=$(echo "$cat" | sed 's/Mettre-a-jour/Mettre a jour/')
        local nb=$(compter_outils_categorie "$cle")
        local lue=$(grep -o "\*\*${cat} ([0-9]*)\*\*" "$README" | grep -o '[0-9]*' | head -1)
        if [ -n "$lue" ] && [ "$lue" != "$nb" ]; then
            echo -e "  ${RED}[OBSOLETE]${NC} ${cat} : README dit ${lue}, reel = ${nb}"
        else
            echo -e "  ${GREEN}[OK]${NC} ${cat} : ${nb}"
        fi
        # Outils manquants dans la liste de la categorie
        local liste_reelle=$(lister_outils_categorie "$cle")
        local ligne_readme=$(grep -o "\*\*${cat} ([0-9]*)\*\* | [^|]*" "$README" | head -1 | sed "s/.*| //")
        for outil in $(echo "$liste_reelle" | tr ',' '\n' | sed 's/^ *//; s/ *$//'); do
            local nom=${outil##*: }
            if [ -n "$nom" ] && ! echo "$ligne_readme" | grep -q "$nom"; then
                echo -e "  ${YELLOW}[MANQUANT]${NC} ${cat} : outil '${nom}' absent de la liste"
            fi
        done
    done

    echo ""
    echo "Utilisez --maj pour corriger le texte du README."
}

# Corriger le README pour qu'il reflete l'etat reel
mettre_a_jour() {
    local total=$(compter_total_outils)
    echo "=== CORRECTION DU README ==="

    # 1. Titre boite a outils
    if grep -q '^## La boite a outils ([0-9]* outils)' "$README"; then
        sed -i "s/^## La boite a outils ([0-9]* outils)/## La boite a outils ($total outils)/" "$README"
        echo -e "  ${GREEN}[CORRIGE]${NC} Titre : La boite a outils ($total outils)"
    fi

    # 2. Compteurs par categorie (capitaliser les noms)
    for cle in $(lister_categories); do
        local cat=$(echo "${cle:0:1}" | tr '[:lower:]' '[:upper:]')${cle:1}
        cat=$(echo "$cat" | sed 's/Mettre-a-jour/Mettre a jour/')
        local nb=$(compter_outils_categorie "$cle")
        if grep -q "\*\*${cat} ([0-9]*)\*\*" "$README"; then
            sed -i "s/\*\*${cat} ([0-9]*)\*\*/**${cat} ($nb)**/g" "$README"
            echo -e "  ${GREEN}[CORRIGE]${NC} ${cat} : ${nb}"
        fi
    done

    # 3. Ajouter les agents manquants dans la table 'Les agents' (casse insensible)
    local agents_ajoutes=0
    for agent in $(lister_agents_reels); do
        if ! grep -qi "\*\*${agent}\*\*" "$README"; then
            local role=$(lire_role_agent "$agent")
            [ -z "$role" ] && role="Agent"
            # Capitaliser le nom (cerberus -> Cerberus)
            local nom_affichable="$(echo "${agent:0:1}" | tr '[:lower:]' '[:upper:]')${agent:1}"
            # Inserer la ligne avant '### Le cycle fondamental' (fin de la table des agents)
            local ligne="| **${nom_affichable}** | ${role} | Selon sa carte de decision |"
            sed -i "/^### Le cycle fondamental/i ${ligne}" "$README"
            echo -e "  ${GREEN}[AJOUTE]${NC} Agent '${nom_affichable}' ajoute dans la table"
            agents_ajoutes=$((agents_ajoutes + 1))
        fi
    done
    [ "$agents_ajoutes" -eq 0 ] && echo -e "  ${GREEN}[OK]${NC} Table des agents complete"

    # 4. Reconstruire la liste des outils de chaque categorie (ajout + suppression + renommage)
    # La cellule 'outils' du README doit correspondre EXACTEMENT aux outils reels
    for cle in $(lister_categories); do
        local cat=$(echo "${cle:0:1}" | tr '[:lower:]' '[:upper:]')${cle:1}
        cat=$(echo "$cat" | sed 's/Mettre-a-jour/Mettre a jour/')
        local nb=$(compter_outils_categorie "$cle")
        local liste_reelle=$(lister_outils_categorie "$cle")
        # Reconstruire la ligne de la categorie en conservant la colonne Usage
        # Format de ligne : | **Cat (N)** | liste outils | usage |
        # Decoupage par | : parts[1]="", parts[2]=" **Cat (N)** ", parts[3]="liste outils", parts[4]="usage"
        awk -v nb="$nb" -v liste="$liste_reelle" '
            $0 ~ "^\\| \\*\\*" cat " \\(" {
                n = split($0, parts, "|")
                usage = (n >= 5) ? parts[4] : ""
                gsub(/^ +| +$/, "", usage)
                printf "| **%s (%d)** | %s | %s |\n", cat, nb, liste, usage
                next
            }
            { print }
        ' cat="$cat" "$README" > "$README.tmp" && mv "$README.tmp" "$README"
        echo -e "  ${GREEN}[RECONSTRUIT]${NC} ${cat} : ${nb} outils"
    done

    echo ""
    echo -e "${GREEN}[OK]${NC} README corrige pour refleter l'etat reel."
}

# Inserer une image (logo) en tete du README, apres le titre H1
# Idempotent : si le chemin est deja present, n'insere rien.
inserer_logo() {
    local chemin_image="$1"
    local contenu
    if [ -z "$chemin_image" ]; then
        echo -e "${RED}[ERREUR] Option --logo necessite un chemin d'image.${NC}"
        return 1
    fi
    if [ ! -f "$chemin_image" ]; then
        echo -e "${RED}[ERREUR] Fichier image introuvable : ${chemin_image}${NC}"
        return 1
    fi
    if grep -qF -- "$chemin_image" "$README"; then
        echo -e "${GREEN}[OK]${NC} Le logo ${chemin_image} est deja present dans le README (aucun doublon)."
        return 0
    fi
    # Inserer "\n![Logo](chemin)\n\n" juste apres la premiere ligne de titre H1 ("# ")
    awk -v img="$chemin_image" '
        BEGIN { done = 0 }
        {
            if (!done && $0 ~ /^# /) {
                print $0
                print ""
                print "![Logo](" img ")"
                print ""
                done = 1
                next
            }
            print
        }
    ' "$README" > "$README.tmp" && mv "$README.tmp" "$README"
    # Verifier que l'insertion a reellement ete faite (un titre H1 existait)
    if grep -qF -- "![Logo]($chemin_image)" "$README"; then
        echo -e "${GREEN}[OK]${NC} Logo ${chemin_image} insere en tete du README, apres le titre H1."
        return 0
    fi
    echo -e "${RED}[ERREUR]${NC} Aucun titre H1 (# ...) trouve : rien n'a ete insere."
    return 1
}

# Encoder une portion de badge Shields : espace -> '_', tiret -> '--'
encoder_badge() {
    local texte="$1"
    local out=""
    local i c
    for (( i=0; i<${#texte}; i++ )); do
        c="${texte:$i:1}"
        if [ "$c" = " " ]; then
            out="${out}_"
        elif [ "$c" = "-" ]; then
            out="${out}--"
        else
            out="${out}${c}"
        fi
    done
    echo "$out"
}

# Inserer des badges statiques Shields en tete du README, apres le titre H1
# SPEC : liste separee par ';', chaque badge au format label=message:couleur
# Idempotent : si la ligne de badges identique existe deja, n'insere rien.
inserer_badges() {
    local spec="$1"
    local IFS_save="$IFS"
    if [ -z "$spec" ]; then
        echo -e "${RED}[ERREUR] Option --badges necessite une specification.${NC}"
        return 1
    fi
    # Construire la ligne de badges
    local ligne=""
    local b label reste message couleur url label_enc message_enc
    IFS=';' read -ra badges <<< "$spec"
    IFS="$IFS_save"
    for b in "${badges[@]}"; do
        b="$(echo "$b" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
        [ -z "$b" ] && continue
        if [[ "$b" != *"="* ]] || [[ "$b" != *":"* ]]; then
            echo -e "${RED}[ERREUR] Badge invalide (attendu label=message:couleur) : ${b}${NC}"
            return 1
        fi
        label="${b%%=*}"
        reste="${b#*=}"
        # La couleur est apres le dernier ':'
        couleur="${reste##*:}"
        message="${reste%:*}"
        label="$(echo "$label" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
        message="$(echo "$message" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
        couleur="$(echo "$couleur" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
        if [ -z "$label" ] || [ -z "$message" ] || [ -z "$couleur" ]; then
            echo -e "${RED}[ERREUR] Badge incomplet (label, message et couleur requis) : ${b}${NC}"
            return 1
        fi
        # Rejeter tout caractere non-ASCII (regle immuable)
        if printf '%s' "$label$message$couleur" | LC_ALL=C grep -q '[^ -~]'; then
            echo -e "${RED}[ERREUR] Caractere non-ASCII dans un badge : ${b}${NC}"
            return 1
        fi
        label_enc="$(encoder_badge "$label")"
        message_enc="$(encoder_badge "$message")"
        url="https://img.shields.io/badge/${label_enc}-${message_enc}-${couleur}?style=flat"
        if [ -n "$ligne" ]; then ligne="$ligne "; fi
        ligne="${ligne}[![${label}](${url})](${url})"
    done
    if [ -z "$ligne" ]; then
        echo -e "${RED}[ERREUR] Aucun badge valide fourni.${NC}"
        return 1
    fi
    if grep -qF -- "$ligne" "$README"; then
        echo -e "${GREEN}[OK]${NC} Ces badges sont deja presents dans le README (aucun doublon)."
        return 0
    fi
    # Inserer la ligne de badges juste apres la premiere ligne H1
    awk -v badges_ligne="$ligne" '
        BEGIN { done = 0 }
        {
            if (!done && $0 ~ /^# /) {
                print $0
                print ""
                print badges_ligne
                print ""
                done = 1
                next
            }
            print
        }
    ' "$README" > "$README.tmp" && mv "$README.tmp" "$README"
    if grep -qF -- "$ligne" "$README"; then
        echo -e "${GREEN}[OK]${NC} Badge(s) insere(s) en tete du README, apres le titre H1."
        return 0
    fi
    echo -e "${RED}[ERREUR]${NC} Aucun titre H1 (# ...) trouve : rien n'a ete insere."
    return 1
}

# Afficher le journal (diagnostic, non inscrit au README)
afficher_journal() {
    local n="${1:-10}"
    echo "=== Dernieres interventions (${n}) -- diagnostic ==="
    lire_journal "$n"
    echo ""
    echo "Note : ces interventions servent a savoir CE QUI A CHANGE."
    echo "Le README est corrige (--maj), jamais rempli de lignes."
}

# Main
main() {
    local action=""
    local n="10"
    local help="false"
    local logo_chemin=""
    local badges_spec=""

    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verifier)
                action="verifier"
                shift
                ;;
            --maj)
                action="maj"
                shift
                ;;
            --journal)
                action="journal"
                shift
                if [[ $1 =~ ^[0-9]+$ ]]; then
                    n="$1"
                    shift
                fi
                ;;
            --logo)
                action="logo"
                shift
                if [[ $# -gt 0 && "$1" != --* ]]; then
                    logo_chemin="$1"
                    shift
                fi
                ;;
            --badges)
                action="badges"
                shift
                if [[ $# -gt 0 && "$1" != --* ]]; then
                    badges_spec="$1"
                    shift
                fi
                ;;
            --agents)
                action="agents"
                shift
                ;;
            --outils)
                action="outils"
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

    if [ ! -f "$README" ]; then
        echo -e "${RED}[ERREUR] Fichier README introuvable : $README${NC}"
        exit 1
    fi

    case "$action" in
        verifier)
            verifier
            ;;
        maj)
            mettre_a_jour
            ;;
        journal)
            afficher_journal "$n"
            ;;
        logo)
            inserer_logo "$logo_chemin"
            ;;
        badges)
            inserer_badges "$badges_spec"
            ;;
        agents)
            echo "Agents reels : $(compter_agents)"
            ;;
        outils)
            echo "=== Outils par categorie ==="
            local total=0
            for cat in $(lister_categories); do
                local nb=$(compter_outils_categorie "$cat")
                echo "  ${cat} : ${nb}"
                total=$((total + nb))
            done
            echo "  TOTAL : ${total}"
            ;;
        *)
            verifier
            ;;
    esac
}

# Executer
main "$@"
