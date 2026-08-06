#!/bin/bash
# remplir-pense-bete.sh
# Remplit une section d'un pense-bete sans ouvrir le fichier
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
    echo "=== remplir-pense-bete v${VERSION} ==="
    echo ""
    echo "Usage: $0 <fichier> <section> <contenu>"
    echo ""
    echo "Arguments :"
    echo "  <fichier>   Chemin du pense-bete a remplir"
    echo "  <section>   Section a remplir : idee | probleme | contexte | liens | titre"
    echo "  <contenu>   Contenu a inserer (entre guillemets)"
    echo ""
    echo "Options :"
    echo "  --dry-run   Afficher ce qui serait fait sans modifier"
    echo "  --help      Afficher cette aide"
    echo ""
    echo "Sections disponibles :"
    echo "  titre       Remplacer le titre du pense-bete"
    echo "  idee        Remplir la section 1. Idee"
    echo "  probleme    Remplir la section 2. Probleme / Question"
    echo "  contexte    Remplir la section 3. Contexte"
    echo "  liens       Remplir la section 4. Liens (contenu multiligne avec \\n)"
    echo ""
    echo "Exemples :"
    echo "  $0 pense-bete-pipeline.001.01.ebauche.md idee \"Le pipeline permet de composer des fonctions\""
    echo "  $0 pense-bete-pipeline.001.01.ebauche.md titre \"Concept de Pipeline\""
    echo "  $0 pense-bete-pipeline.001.01.ebauche.md liens \"- Conventions : convention-pipelines.md\\n- Regles : rvav-workflow.md\""
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
            marqueur="^# Pense-bete"
            est_titre="true"
            ;;
        idee)
            marqueur="^## 1. Idee"
            ;;
        probleme)
            marqueur="^## 2. Probleme / Question"
            ;;
        contexte)
            marqueur="^## 3. Contexte"
            ;;
        liens)
            marqueur="^## 4. Liens"
            ;;
        *)
            echo -e "${RED}[ERREUR] Section inconnue : ${section}${NC}"
            echo "Sections disponibles : titre, idee, probleme, contexte, liens"
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
    
    # Trouver la prochaine section (ligne qui commence par ## ou fin de fichier)
    local ligne_fin=$(tail -n +$((ligne_section + 1)) "$fichier" | grep -n '^## ' | head -1 | cut -d: -f1)
    local fin_absolue=""
    if [ -z "$ligne_fin" ]; then
        fin_absolue=""
    else
        fin_absolue=$((ligne_section + ligne_fin))
    fi
    
    # Construire le nouveau contenu
    local contenu_echappe=$(printf '%s' "$contenu")
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} Section '${section}' de ${fichier}"
        echo "  Contenu a inserer :"
        echo "  -----------------"
        echo "$contenu_echappe"
        echo "  -----------------"
        exit 0
    fi
    
    # Remplacer le contenu
    if [ "$est_titre" = "true" ]; then
        # Remplacer la ligne du titre
        sed -i "${ligne_section}s|.*|# Pense-bete — ${contenu}|" "$fichier"
    else
        # Construire le fichier temporaire
        local tmp=$(mktemp)
        
        if [ -n "$fin_absolue" ]; then
            # Section au milieu : remplacer entre ligne_section et fin_absolue
            head -n $ligne_section "$fichier" > "$tmp"
            echo "" >> "$tmp"
            echo "$contenu_echappe" >> "$tmp"
            echo "" >> "$tmp"
            tail -n +$fin_absolue "$fichier" >> "$tmp"
        else
            # Section en fin de fichier
            head -n $ligne_section "$fichier" > "$tmp"
            echo "" >> "$tmp"
            echo "$contenu_echappe" >> "$tmp"
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
