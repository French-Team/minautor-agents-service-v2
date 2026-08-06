#!/bin/bash
# valider-todo.sh
# Verifie l'integrite d'un todo (structure, phases, ASCII)
# Version : 0.1.0-beta
# Statut : ebauche

# Configuration
VERSION="0.1.0-beta"
STATUT="ebauche"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== valider-todo v${VERSION} ==="
    echo ""
    echo "Usage: $0 <fichier>"
    echo ""
    echo "Arguments :"
    echo "  <fichier>   Chemin du todo a valider"
    echo ""
    echo "Options :"
    echo "  --verbose   Afficher les details de chaque verification"
    echo "  --help      Afficher cette aide"
    echo ""
    echo "Verifications effectuees :"
    echo "  1. Le fichier existe et n'est pas vide"
    echo "  2. La Phase 0 (activation de l'agent) est presente -- OBLIGATOIRE"
    echo "  3. Les 10 phases (0 a 9) sont presentes"
    echo "  4. La Phase 9 (reactivation de Cerberus) est presente -- OBLIGATOIRE"
    echo "  5. Le nommage du fichier est conforme (todo-[theme].[id].[class].[statut].md)"
    echo "  6. Aucun placeholder non remplace ([...] restants)"
    echo "  7. Conformite ASCII (pas d'accents, pas d'emojis)"
    echo ""
    echo "Exemple :"
    echo "  $0 todo-pipeline.001.01.ebauche.md"
    echo ""
}

# Verifier une phase
verifier_phase() {
    local fichier="$1"
    local phase="$2"
    local libelle="$3"
    local obligatoire="$4"
    
    if grep -qF "$phase" "$fichier" 2>/dev/null; then
        if [ "$verbose" = "true" ]; then
            echo -e "  ${GREEN}[OK]${NC} Phase : ${libelle}"
        fi
        return 0
    else
        if [ "$obligatoire" = "true" ]; then
            echo -e "  ${RED}[ERREUR]${NC} Phase obligatoire manquante : ${libelle}"
        else
            echo -e "  ${YELLOW}[ATTENTION]${NC} Phase manquante : ${libelle}"
        fi
        return 1
    fi
}

# Verifier les phases
verifier_phases() {
    local fichier="$1"
    local erreurs=0
    
    # Phase 0 - OBLIGATOIRE
    verifier_phase "$fichier" "## Phase 0 -- Activation de l'agent" "Phase 0 -- Activation de l'agent" "true"
    erreurs=$((erreurs + $?))
    
    # Phases 1-8
    verifier_phase "$fichier" "## Phase 1 -- Analyse de la demande" "Phase 1 -- Analyse de la demande" "false"
    verifier_phase "$fichier" "## Phase 2 -- Verification du cerveau" "Phase 2 -- Verification du cerveau" "false"
    verifier_phase "$fichier" "## Phase 3 -- Recherches" "Phase 3 -- Recherches" "false"
    verifier_phase "$fichier" "## Phase 4 -- Preparation des outils" "Phase 4 -- Preparation des outils" "false"
    verifier_phase "$fichier" "## Phase 5 -- Developpement" "Phase 5 -- Developpement" "false"
    verifier_phase "$fichier" "## Phase 6 -- Tests et validation" "Phase 6 -- Tests et validation" "false"
    verifier_phase "$fichier" "## Phase 7 -- Controle secondaire" "Phase 7 -- Controle secondaire" "false"
    verifier_phase "$fichier" "## Phase 8 -- Finalisation" "Phase 8 -- Finalisation" "false"
    
    # Phase 9 - OBLIGATOIRE
    verifier_phase "$fichier" "## Phase 9 -- Reactivation de Cerberus" "Phase 9 -- Reactivation de Cerberus" "true"
    erreurs=$((erreurs + $?))
    
    return $erreurs
}

# Verifier le nommage
verifier_nommage() {
    local fichier="$1"
    local nom=$(basename "$fichier")
    
    if echo "$nom" | grep -qE '^todo-[a-z0-9-]+\.[0-9]+\.[0-9]+\.[a-z]+\.md$'; then
        if [ "$verbose" = "true" ]; then
            echo -e "  ${GREEN}[OK]${NC} Nommage conforme : ${nom}"
        fi
        return 0
    else
        echo -e "  ${RED}[ERREUR]${NC} Nommage non conforme : ${nom}"
        echo "  Attendu : todo-[theme].[id].[class].[statut].md"
        return 1
    fi
}

# Verifier les placeholders non remplis
verifier_placeholders() {
    local fichier="$1"
    local placeholders=$(grep -nE '\[[A-Za-z][A-Za-z ]+\]' "$fichier" 2>/dev/null | head -10)
    
    if [ -n "$placeholders" ]; then
        echo -e "  ${YELLOW}[ATTENTION]${NC} Placeholders non remplis :"
        echo "$placeholders" | head -5 | while read ligne; do
            echo "    $ligne"
        done
        return 1
    else
        if [ "$verbose" = "true" ]; then
            echo -e "  ${GREEN}[OK]${NC} Aucun placeholder restant"
        fi
        return 0
    fi
}

# Verifier la conformite ASCII
verifier_ascii() {
    local fichier="$1"
    
    if python -c "import io,sys; sys.exit(0 if any(ord(ch)>127 for ch in io.open(sys.argv[1],encoding='utf-8').read()) else 1)" "$fichier"; then
        echo -e "  ${RED}[ERREUR]${NC} Caracteres non-ASCII detectes :"
        python -c "import io,sys; [print(str(i)+': '+l.rstrip()) for i,l in enumerate(io.open(sys.argv[1],encoding='utf-8').read().split(chr(10)),1) if any(ord(ch)>127 for ch in l)][:5]" "$fichier" | while read ligne; do
            echo "    $ligne"
        done
        return 1
    else
        if [ "$verbose" = "true" ]; then
            echo -e "  ${GREEN}[OK]${NC} Conformite ASCII"
        fi
        return 0
    fi
}

# Main
main() {
    local fichier=""
    local verbose="false"
    local help="false"
    
    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verbose)
                verbose="true"
                shift
                ;;
            --help)
                help="true"
                shift
                ;;
            *)
                fichier="$1"
                shift
                ;;
        esac
    done
    
    # Afficher l'aide
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    # Verifier le fichier obligatoire
    if [ -z "$fichier" ]; then
        echo -e "${RED}[ERREUR] Le fichier est obligatoire${NC}"
        afficher_aide
        exit 1
    fi
    
    # Verifier que le fichier existe et n'est pas vide
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve : ${fichier}${NC}"
        exit 1
    fi
    
    if [ ! -s "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier vide : ${fichier}${NC}"
        exit 1
    fi
    
    echo "=== Validation du todo ==="
    echo "Fichier : ${fichier}"
    echo ""
    
    local total_erreurs=0
    
    # 1. Phases (dont 0 et 9 obligatoires)
    if [ "$verbose" = "true" ]; then echo "--- Phases ---"; fi
    verifier_phases "$fichier"
    total_erreurs=$((total_erreurs + $?))
    
    # 2. Nommage
    if [ "$verbose" = "true" ]; then echo "--- Nommage ---"; fi
    verifier_nommage "$fichier"
    total_erreurs=$((total_erreurs + $?))
    
    # 3. Placeholders (attention : pas une erreur bloquante)
    if [ "$verbose" = "true" ]; then echo "--- Placeholders ---"; fi
    verifier_placeholders "$fichier"
    
    # 4. ASCII
    if [ "$verbose" = "true" ]; then echo "--- ASCII ---"; fi
    verifier_ascii "$fichier"
    total_erreurs=$((total_erreurs + $?))
    
    # Resume
    echo ""
    echo "=== Resume ==="
    if [ "$total_erreurs" -eq 0 ]; then
        echo -e "${GREEN}[OK] Le todo est valide${NC}"
        exit 0
    else
        echo -e "${RED}[ERREUR] ${total_erreurs} probleme(s) detecte(s)${NC}"
        exit 1
    fi
}

# Executer
main "$@"
