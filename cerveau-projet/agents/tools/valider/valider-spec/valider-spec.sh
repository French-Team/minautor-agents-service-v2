#!/bin/bash
# valider-spec.sh
# Verifie l'integrite d'une spec (structure, sections, ASCII)
# Version : 0.2.0

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
STATUT="ebauche"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== valider-spec v${VERSION} ==="
    echo ""
    echo "Usage: $0 <fichier>"
    echo ""
    echo "Arguments :"
    echo "  <fichier>   Chemin de la spec a valider"
    echo ""
    echo "Options :"
    echo "  --verbose   Afficher les details de chaque verification"
    echo "  --help      Afficher cette aide"
    echo ""
    echo "Verifications effectuees :"
    echo "  1. Le fichier existe et n'est pas vide"
    echo "  2. Le header est present (Statut, ID, Class, Cree, Theme, Pense-bete source)"
    echo "  3. Les 10 sections sont presentes (1. Objectif ... 10. RVAV)"
    echo "  4. Le nommage du fichier est conforme (spec-[theme].[id].[class].[statut].md)"
    echo "  5. Aucun placeholder non remplace ([...] restants)"
    echo "  6. Conformite ASCII (pas d'accents, pas d'emojis)"
    echo ""
    echo "Exemple :"
    echo "  $0 spec-pipeline.001.01.ebauche.md"
    echo ""
}

# Verifier le header
verifier_header() {
    local fichier="$1"
    local erreurs=0
    
    for champ in "Statut" "ID" "Class" "Cree" "Theme" "Pense-bete source"; do
        if grep -q "\\*\\*${champ} :" "$fichier" 2>/dev/null; then
            if [ "$verbose" = "true" ]; then
                echo -e "  ${GREEN}[OK]${NC} Header : ${champ}"
            fi
        else
            echo -e "  ${RED}[ERREUR]${NC} Header manquant : ${champ}"
            erreurs=$((erreurs + 1))
        fi
    done
    
    return $erreurs
}

# Verifier les sections
verifier_sections() {
    local fichier="$1"
    local erreurs=0
    
    for section in "## 1. Objectif" "## 2. Contexte" "## 3. Exigences Fonctionnelles" "## 4. Exigences Non-Fonctionnelles" "## 5. Architecture / Structure Technique" "## 6. Contraintes et Risques" "## 7. Livrables attendus" "## 8. Plan de validation" "## 9. Liens et References" "## 10. RVAV de la spec"; do
        if grep -qF "$section" "$fichier" 2>/dev/null; then
            if [ "$verbose" = "true" ]; then
                echo -e "  ${GREEN}[OK]${NC} Section : ${section}"
            fi
        else
            echo -e "  ${RED}[ERREUR]${NC} Section manquante : ${section}"
            erreurs=$((erreurs + 1))
        fi
    done
    
    return $erreurs
}

# Verifier le nommage
verifier_nommage() {
    local fichier="$1"
    local nom=$(basename "$fichier")
    
    if echo "$nom" | grep -qE '^spec-[a-z0-9-]+\.[0-9]+\.[0-9]+\.[a-z]+\.md$'; then
        if [ "$verbose" = "true" ]; then
            echo -e "  ${GREEN}[OK]${NC} Nommage conforme : ${nom}"
        fi
        return 0
    else
        echo -e "  ${RED}[ERREUR]${NC} Nommage non conforme : ${nom}"
        echo "  Attendu : spec-[theme].[id].[class].[statut].md"
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
    
    echo "=== Validation de la spec ==="
    echo "Fichier : ${fichier}"
    echo ""
    
    local total_erreurs=0
    
    # 1. Header
    if [ "$verbose" = "true" ]; then echo "--- Header ---"; fi
    verifier_header "$fichier"
    total_erreurs=$((total_erreurs + $?))
    
    # 2. Sections
    if [ "$verbose" = "true" ]; then echo "--- Sections ---"; fi
    verifier_sections "$fichier"
    total_erreurs=$((total_erreurs + $?))
    
    # 3. Nommage
    if [ "$verbose" = "true" ]; then echo "--- Nommage ---"; fi
    verifier_nommage "$fichier"
    total_erreurs=$((total_erreurs + $?))
    
    # 4. Placeholders (attention : pas une erreur bloquante)
    if [ "$verbose" = "true" ]; then echo "--- Placeholders ---"; fi
    verifier_placeholders "$fichier"
    
    # 5. ASCII
    if [ "$verbose" = "true" ]; then echo "--- ASCII ---"; fi
    verifier_ascii "$fichier"
    total_erreurs=$((total_erreurs + $?))
    
    # Resume
    echo ""
    echo "=== Resume ==="
    if [ "$total_erreurs" -eq 0 ]; then
        echo -e "${GREEN}[OK] La spec est valide${NC}"
        exit 0
    else
        echo -e "${RED}[ERREUR] ${total_erreurs} probleme(s) detecte(s)${NC}"
        exit 1
    fi
}

# Executer
main "$@"
