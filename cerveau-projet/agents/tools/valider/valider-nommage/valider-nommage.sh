#!/bin/bash
# valider-nommage.sh
# Verifier que le nommage est correct selon les conventions
# Version: 0.2.0
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
DATE="2026-08-05"

# Couleurs pour la sortie
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'aide
aide() {
    echo "=========================================="
    echo "  valider-nommage v${VERSION}"
    echo "  Verifier le nommage selon les conventions"
    echo "=========================================="
    echo ""
    echo "Usage: valider-nommage [OPTIONS] CHEMIN"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les details"
    echo "  --version           Afficher la version"
    echo "  --type TYPE         Type de fichier (protocole, convention, agent, outil)
  --recursive, -r     Valider tous les outils d'un dossier (ignore --type)"
    echo ""
    echo "Types de fichiers:"
    echo "  protocole     nom-protocole.XX.XX.statut.md"
    echo "  agent         nom-agent.md"
    echo "  outil         nom-outil.sh, nom-outil.py ou nom-outil.md"
    echo "  convention    convention-nom.md"
    echo ""
    echo "Statuts valides (protocoles):"
    echo "  ebauche, prepare, dev, test, valide"
    echo ""
    echo "Exemples:"
    echo "  valider-nommage --type protocole chemin/vers/protocole.md"
    echo "  valider-nommage --type agent chemin/vers/agent.md"
    echo "  valider-nommage --recursive cerveau-projet/agents/tools/"
    echo ""
}

# Fonction pour valider le nommage d'un protocole
valider_protocole() {
    local fichier=$1
    local verbose=$2
    local erreurs=0

    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    # Extraire les parties du nom
    local nom_part=$(echo "$basename" | cut -d'.' -f1)
    local major_part=$(echo "$basename" | cut -d'.' -f2)
    local minor_part=$(echo "$basename" | cut -d'.' -f3)
    local statut_part=$(echo "$basename" | cut -d'.' -f4)

    # Verifier que les parties existent
    if [[ -z "$nom_part" || -z "$major_part" || -z "$minor_part" || -z "$statut_part" ]]; then
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : nom-protocole.XX.XX.statut.md"
        return 1
    fi

    # Verifier que major et minor sont des nombres
    if ! [[ "$major_part" =~ ^[0-9]+$ ]] || ! [[ "$minor_part" =~ ^[0-9]+$ ]]; then
        echo -e "  ${RED}[ERREUR] Version invalide : ${major_part}.${minor_part}${NC}"
        echo -e "    Les versions doivent etre des nombres"
        return 1
    fi

    # Verifier que le statut est valide
    # NB: ASCII pur uniquement (prepare, jamais prepare) pour eviter les bugs d'encodage
    case "$statut_part" in
        ebauche|prepare|dev|test|valide)
            echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
            
            if [[ "$verbose" == "true" ]]; then
                echo -e "    Nom : ${nom_part}"
                echo -e "    Version : ${major_part}.${minor_part}"
                echo -e "    Statut : ${statut_part}"
            fi
            return 0
            ;;
        *)
            echo -e "  ${RED}[ERREUR] Statut invalide : ${statut_part}${NC}"
            echo -e "    Statuts valides : ebauche, prepare, dev, test, valide"
            return 1
            ;;
    esac
}

# Fonction pour valider le nommage d'un agent
valider_agent() {
    local fichier=$1
    local verbose=$2

    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    # Verifier le format : nom-agent.md
    if [[ "$basename" =~ ^[a-z]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
        return 0
    else
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : nom-agent.md"
        return 1
    fi
}

# Fonction pour valider le nommage d'un outil
# Arg1: chemin du fichier, Arg2: verbose, Arg3: nom du dossier categorie (optionnel)
valider_outil() {
    local fichier=$1
    local verbose=$2
    local categorie=$3

    local basename=$(basename "$fichier")
    local erreurs=0

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    # Verifier le format : nom-outil.sh, nom-outil.py ou nom-outil.md
    if [[ "$basename" =~ ^[a-z-]+\.sh$ ]] || [[ "$basename" =~ ^[a-z-]+\.py$ ]] || [[ "$basename" =~ ^[a-z-]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
    else
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : nom-outil.sh, nom-outil.py ou nom-outil.md"
        erreurs=$((erreurs + 1))
    fi

    # Verifier le prefixe du dossier (regle immuable)
    local nom=$(echo "$basename" | sed 's/\.sh$//; s/\.py$//; s/\.md$//')

    # Si la categorie n est pas fournie, l extraire du chemin
    if [[ -z "$categorie" ]]; then
        # Remonter de 2 niveaux depuis le fichier pour trouver la categorie
        # Structure: tools/[categorie]/[outil]/[fichier]
        local dossier_outil=$(dirname "$fichier")
        categorie=$(basename "$(dirname "$dossier_outil")")
    fi

    if [[ "$nom" == "${categorie}-"* ]] || [[ "$nom" == "$categorie" ]]; then
        if [[ "$verbose" == "true" ]]; then
            echo -e "  ${GREEN}[OK] Prefixe dossier respecte : ${categorie}/${NC}"
        fi
    else
        echo -e "  ${RED}[ERREUR] Prefixe dossier manquant : ${basename}${NC}"
        echo -e "    Le nom doit commencer par '${categorie}-' (dossier: ${categorie}/)"
        erreurs=$((erreurs + 1))
    fi

    return $erreurs
}

# Fonction pour valider le nommage d'une convention
valider_convention() {
    local fichier=$1
    local verbose=$2

    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    # Verifier le format : convention-nom.md
    if [[ "$basename" =~ ^convention-[a-z-]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
        return 0
    else
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : convention-nom.md"
        return 1
    fi
}

# Valeurs par defaut
VERBOSE="false"
TYPE=""
FICHIER=""
RECURSIVE="false"

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --aide|-h)
            aide
            exit 0
            ;;
        --verbose|-v)
            VERBOSE="true"
            shift
            ;;
        --version)
            echo "valider-nommage v${VERSION}"
            exit 0
            ;;
        --type)
            TYPE="$2"
            shift 2
            ;;
        --recursive|-r)
            RECURSIVE="true"
            shift
            ;;
        -*)
            echo "Option inconnue: $1"
            echo "Utilisez --aide pour l'aide"
            exit 1
            ;;
        *)
            FICHIER="$1"
            shift
            ;;
    esac
done

# Mode recursive : valider tous les outils d'un dossier
if [[ "$RECURSIVE" == "true" ]]; then
    if [[ -z "$FICHIER" ]]; then
        echo "Erreur: Aucun dossier specifie pour --recursive"
        exit 1
    fi
    if [[ ! -d "$FICHIER" ]]; then
        echo "Erreur: '$FICHIER' n'est pas un dossier"
        exit 1
    fi
    echo -e "${BLUE}=== Validation recursive des outils dans : ${FICHIER} ===${NC}"
    echo ""
    total=0
    ok=0
    ko=0
    # Parcourir tous les dossiers d'outils (structure: tools/categorie/outil/)
    while IFS= read -r dossier_outil; do
        # Extraire la categorie (dossier parent du dossier outil)
        categorie=$(basename "$(dirname "$dossier_outil")")
        nom_outil=$(basename "$dossier_outil")
        # Parcourir les .sh du dossier
        for f in "$dossier_outil"/*.sh; do
            [[ ! -f "$f" ]] && continue
            total=$((total + 1))
            valider_outil "$f" "$VERBOSE" "$categorie"
            [[ $? -eq 0 ]] && ok=$((ok + 1)) || ko=$((ko + 1))
            echo ""
        done
        # Parcourir les .md du dossier
        for f in "$dossier_outil"/*.md; do
            [[ ! -f "$f" ]] && continue
            total=$((total + 1))
            valider_outil "$f" "$VERBOSE" "$categorie"
            [[ $? -eq 0 ]] && ok=$((ok + 1)) || ko=$((ko + 1))
            echo ""
        done
        # Parcourir les .py du dossier
        for f in "$dossier_outil"/*.py; do
            [[ ! -f "$f" ]] && continue
            total=$((total + 1))
            valider_outil "$f" "$VERBOSE" "$categorie"
            [[ $? -eq 0 ]] && ok=$((ok + 1)) || ko=$((ko + 1))
            echo ""
        done
    done < <(find "$FICHIER" -mindepth 2 -maxdepth 2 -type d 2>/dev/null | sort)
    echo -e "${BLUE}=== Resume ===${NC}"
    echo -e "  Total : ${total}"
    echo -e "  ${GREEN}OK : ${ok}${NC}"
    [[ $ko -gt 0 ]] && echo -e "  ${RED}Erreurs : ${ko}${NC}" || echo -e "  Erreurs : 0"
    exit $ko
fi

# Verification du fichier
if [[ -z "$FICHIER" ]]; then
    echo "Erreur: Aucun fichier specifie"
    echo "Utilisez --aide pour l'aide"
    exit 1
fi

if [[ ! -f "$FICHIER" ]]; then
    echo "Erreur: Le fichier '$FICHIER' n'existe pas"
    exit 1
fi

# Verifier le type
if [[ -z "$TYPE" ]]; then
    echo "Erreur: Type non specifie"
    echo "Utilisez --type pour specifier le type"
    exit 1
fi

# Execution selon le type
case $TYPE in
    protocole)
        valider_protocole "$FICHIER" "$VERBOSE"
        ;;
    agent)
        valider_agent "$FICHIER" "$VERBOSE"
        ;;
    outil)
        valider_outil "$FICHIER" "$VERBOSE"
        ;;
    convention)
        valider_convention "$FICHIER" "$VERBOSE"
        ;;
    *)
        echo "Erreur: Type inconnu '$TYPE'"
        echo "Types disponibles : protocole, agent, outil, convention"
        exit 1
        ;;
esac

exit $?
