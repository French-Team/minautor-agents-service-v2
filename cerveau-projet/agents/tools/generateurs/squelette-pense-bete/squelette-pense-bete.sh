#!/bin/bash
# squelette-pense-bete.sh
# Genere le squelette d'un pense-bete conforme au pense-bete-template
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
    echo "=== squelette-pense-bete v${VERSION} ==="
    echo ""
    echo "Usage: $0 --theme <theme> [--id <id>] [--class <class>] [--statut <statut>] [--dossier <dossier>]"
    echo ""
    echo "Options :"
    echo "  --theme <theme>     Theme du pense-bete (obligatoire, sans accents ni espaces)"
    echo "  --id <id>           Identifiant numerique (defaut: 001)"
    echo "  --class <class>     Classe numerique (defaut: 01)"
    echo "  --statut <statut>   Statut (defaut: ebauche)"
    echo "  --dossier <dossier> Dossier de destination (defaut: .)"
    echo "  --dry-run           Afficher le squelette sans creer le fichier"
    echo "  --help              Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 --theme pipeline"
    echo "  $0 --theme pipeline --id 001 --class 01 --dossier cerveau-projet/pense-betes/"
    echo "  $0 --theme pipeline --dry-run"
    echo ""
}

# Generer le squelette
generer_squelette() {
    local theme="$1"
    local id="$2"
    local class="$3"
    local statut="$4"
    local date=$(date +%Y-%m-%d)
    
    cat << EOF
# Pense-bete — [Titre du pense-bete]

**Statut :** ${statut}
**ID :** ${id}
**Class :** ${class}
**Cree :** ${date}
**Theme :** ${theme}

---

## 1. Idee (1-2 phrases)

[L'essence du concept - ce que ce pense-bete apporte de nouveau ou resout]

## 2. Probleme / Question

[Quel probleme ou question ce pense-bete adresse-t-il ?]

## 3. Contexte

[Comment s'inscrit ce pense-bete dans le projet ou le cerveau ?]

## 4. Liens

- Pense-betes connexes : [a completer]
- Conventions applicables : [a completer]
- Regles immuables : [a completer]

## 5. Structure prevue (RVAV par sous-partie)

| Sous-partie | Fichier cible | Statut | RVAV |
|---|---|---|---|
| Idee | \`pense-bete-${theme}.${id}.${class}.${statut}.md\` | ${statut} | a valider |
| Spec | \`spec/spec-${theme}.${id}.${class}.${statut}.md\` | - | a creer |
| Todo | \`spec/todo/todo-${theme}.${id}.${class}.${statut}.md\` | - | a creer |
| Liens | \`liens/liens-${theme}.${id}.${class}.${statut}.md\` | - | a creer |

## 6. RVAV du pense-bete

- [rechercher] — toutes les references/liens externes sont rassembles
- [verifier] — la structure (idee + probleme + contexte + liens) est complete
- [analyser] — l'idee est coherente avec le cerveau existant (pas de doublon)
- [valider] — pret pour le statut suivant (prepare)
EOF
}

# Main
main() {
    local theme=""
    local id="001"
    local class="01"
    local statut="ebauche"
    local dossier="."
    local dry_run="false"
    local help="false"
    
    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --theme)
                theme="$2"
                shift 2
                ;;
            --id)
                id="$2"
                shift 2
                ;;
            --class)
                class="$2"
                shift 2
                ;;
            --statut)
                statut="$2"
                shift 2
                ;;
            --dossier)
                dossier="$2"
                shift 2
                ;;
            --dry-run)
                dry_run="true"
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
    
    # Afficher l'aide
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    # Verifier le theme obligatoire
    if [ -z "$theme" ]; then
        echo -e "${RED}[ERREUR] Le theme est obligatoire (--theme)${NC}"
        afficher_aide
        exit 1
    fi
    
    # Verifier le theme (pas d'accents, pas d'espaces)
    if echo "$theme" | grep -qE '[^a-z0-9-]'; then
        echo -e "${RED}[ERREUR] Le theme doit etre en minuscules sans accents ni espaces : $theme${NC}"
        exit 1
    fi
    
    # Nom du fichier
    local nom_fichier="pense-bete-${theme}.${id}.${class}.${statut}.md"
    local chemin_fichier="${dossier}/${nom_fichier}"
    
    # Generer le squelette
    local squelette=$(generer_squelette "$theme" "$id" "$class" "$statut")
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} Squelette de : ${nom_fichier}"
        echo ""
        echo "$squelette"
        exit 0
    fi
    
    # Verifier que le fichier n'existe pas deja
    if [ -f "$chemin_fichier" ]; then
        echo -e "${RED}[ERREUR] Le fichier existe deja : ${chemin_fichier}${NC}"
        exit 1
    fi
    
    # Creer le fichier
    echo "$squelette" > "$chemin_fichier"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK]${NC} Squelette cree : ${chemin_fichier}"
        exit 0
    else
        echo -e "${RED}[ERREUR] Impossible de creer le fichier${NC}"
        exit 1
    fi
}

# Executer
main "$@"
