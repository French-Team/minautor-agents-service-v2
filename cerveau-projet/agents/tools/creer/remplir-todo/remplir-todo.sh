#!/bin/bash
# remplir-todo.sh
# Remplit une section d'un todo sans ouvrir le fichier
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
    echo "=== remplir-todo v${VERSION} ==="
    echo ""
    echo "Usage: $0 <fichier> <section> <contenu>"
    echo ""
    echo "Arguments :"
    echo "  <fichier>   Chemin du todo a remplir"
    echo "  <section>   Section a remplir : titre | statut | phaseN | historique | notes | liens"
    echo "  <contenu>   Contenu a inserer (entre guillemets)"
    echo ""
    echo "Options :"
    echo "  --dry-run   Afficher ce qui serait fait sans modifier"
    echo "  --help      Afficher cette aide"
    echo ""
    echo "Sections disponibles :"
    echo "  titre        Remplacer le titre du todo"
    echo "  statut       Remplir le tableau Statut de l'intervention"
    echo "  phase0       Phase 0 — Activation de l'agent"
    echo "  phase1       Phase 1 — Analyse de la demande"
    echo "  phase2       Phase 2 — Verification du cerveau"
    echo "  phase3       Phase 3 — Recherches"
    echo "  phase4       Phase 4 — Preparation des outils"
    echo "  phase5       Phase 5 — Developpement"
    echo "  phase6       Phase 6 — Tests et validation"
    echo "  phase7       Phase 7 — Controle secondaire"
    echo "  phase8       Phase 8 — Finalisation"
    echo "  phase9       Phase 9 — Reactivation de Cerberus"
    echo "  historique   Remplir le tableau Historique"
    echo "  notes        Remplir la section Notes"
    echo "  liens        Remplir la section Liens"
    echo ""
    echo "Exemples :"
    echo "  $0 todo-pipeline.001.01.ebauche.md titre \"Todo du pipeline\""
    echo "  $0 todo-pipeline.001.01.ebauche.md phase5 \"1. Creer le pipeline\\n2. Documenter\""
    echo ""
}

# Remplir une section
remplir_section() {
    local fichier="$1"
    local section="$2"
    local contenu="$3"
    local dry_run="$4"
    
    # Choisir le marqueur de section
    local marqueur=""
    local est_titre="false"
    case "$section" in
        titre)
            marqueur="^# Todo"
            est_titre="true"
            ;;
        statut)
            marqueur="^## Statut de l'intervention"
            ;;
        phase0)
            marqueur="^## Phase 0 — Activation de l'agent"
            ;;
        phase1)
            marqueur="^## Phase 1 — Analyse de la demande"
            ;;
        phase2)
            marqueur="^## Phase 2 — Verification du cerveau"
            ;;
        phase3)
            marqueur="^## Phase 3 — Recherches"
            ;;
        phase4)
            marqueur="^## Phase 4 — Preparation des outils"
            ;;
        phase5)
            marqueur="^## Phase 5 — Developpement"
            ;;
        phase6)
            marqueur="^## Phase 6 — Tests et validation"
            ;;
        phase7)
            marqueur="^## Phase 7 — Controle secondaire"
            ;;
        phase8)
            marqueur="^## Phase 8 — Finalisation"
            ;;
        phase9)
            marqueur="^## Phase 9 — Reactivation de Cerberus"
            ;;
        historique)
            marqueur="^## Historique"
            ;;
        notes)
            marqueur="^## Notes"
            ;;
        liens)
            marqueur="^## Liens"
            ;;
        *)
            echo -e "${RED}[ERREUR] Section inconnue : ${section}${NC}"
            echo "Sections disponibles : titre, statut, phase0..phase9, historique, notes, liens"
            exit 1
            ;;
    esac
    
    # Verifier que le fichier existe
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouve : ${fichier}${NC}"
        exit 1
    fi
    
    # Trouver la ligne de la section
    local ligne_section=$(grep -n "$marqueur" "$fichier" | head -1 | cut -d: -f1)
    if [ -z "$ligne_section" ]; then
        echo -e "${RED}[ERREUR] Section '${section}' non trouvee dans ${fichier}${NC}"
        exit 1
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} Section '${section}' de ${fichier}"
        echo "  Contenu a inserer :"
        echo "  -----------------"
        echo "$contenu"
        echo "  -----------------"
        exit 0
    fi
    
    # Remplacer le contenu
    if [ "$est_titre" = "true" ]; then
        # Remplacer la ligne du titre
        sed -i "${ligne_section}s|.*|# Todo — ${contenu}|" "$fichier"
    else
        # Trouver la prochaine section (ligne qui commence par ## ou fin de fichier)
        local ligne_fin=$(tail -n +$((ligne_section + 1)) "$fichier" | grep -n '^## ' | head -1 | cut -d: -f1)
        local fin_absolue=""
        if [ -n "$ligne_fin" ]; then
            fin_absolue=$((ligne_section + ligne_fin))
        fi
        
        # Interpreter les sequences d'echappement (\n -> retour a la ligne)
        local contenu_multiligne=$(printf '%b' "$contenu")
        
        # Construire le fichier temporaire
        local tmp=$(mktemp)
        
        if [ -n "$fin_absolue" ]; then
            # Section au milieu : remplacer entre ligne_section et fin_absolue
            head -n $ligne_section "$fichier" > "$tmp"
            echo "" >> "$tmp"
            echo "$contenu_multiligne" >> "$tmp"
            echo "" >> "$tmp"
            tail -n +$fin_absolue "$fichier" >> "$tmp"
        else
            # Section en fin de fichier
            head -n $ligne_section "$fichier" > "$tmp"
            echo "" >> "$tmp"
            echo "$contenu_multiligne" >> "$tmp"
            echo "" >> "$tmp"
        fi
        
        mv "$tmp" "$fichier"
    fi
    
    echo -e "${GREEN}[OK]${NC} Section '${section}' remplie dans ${fichier}"
}

# Main
main() {
    local fichier=""
    local section=""
    local contenu=""
    local dry_run="false"
    local help="false"
    
    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run="true"
                shift
                ;;
            --help)
                help="true"
                shift
                ;;
            *)
                if [ -z "$fichier" ]; then
                    fichier="$1"
                elif [ -z "$section" ]; then
                    section="$1"
                elif [ -z "$contenu" ]; then
                    contenu="$1"
                else
                    echo -e "${RED}[ERREUR] Trop d'arguments${NC}"
                    afficher_aide
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Afficher l'aide
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    # Verifier les arguments obligatoires
    if [ -z "$fichier" ] || [ -z "$section" ] || [ -z "$contenu" ]; then
        echo -e "${RED}[ERREUR] Arguments manquants : fichier, section, contenu${NC}"
        afficher_aide
        exit 1
    fi
    
    # Remplir
    remplir_section "$fichier" "$section" "$contenu" "$dry_run"
}

# Executer
main "$@"
