#!/bin/bash
# creer-remplir-spec.sh
# Remplit une section d'une spec sans ouvrir le fichier
# Version : 0.1.0-beta
# Statut : ebauche

# Configuration
VERSION="0.2.0"
STATUT="prepare"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== creer-remplir-spec v${VERSION} ==="
    echo ""
    echo "Usage: $0 <fichier> <section> <contenu>"
    echo ""
    echo "Arguments :"
    echo "  <fichier>   Chemin de la spec a remplir"
    echo "  <section>   Section a remplir : titre | objectif | contexte | exigences | architecture | liens | parent"
    echo "  <contenu>   Contenu a inserer (entre guillemets)"
    echo ""
    echo "Options :"
    echo "  --dry-run   Afficher ce qui serait fait sans modifier"
    echo "  --help      Afficher cette aide"
    echo ""
    echo "Sections disponibles :"
    echo "  titre        Remplacer le titre de la spec"
    echo "  parent       Remplir le lien pense-bete source (Header)"
    echo "  objectif     Remplir la section 1. Objectif"
    echo "  contexte     Remplir la section 2. Contexte (contenu multiligne avec \\n)"
    echo "  exigences    Remplir la section 3. Exigences Fonctionnelles"
    echo "  architecture Remplir la section 5. Architecture / Structure Technique"
    echo "  risques      Remplir la section 6. Contraintes et Risques"
    echo "  livrables    Remplir la section 7. Livrables attendus"
    echo "  validation   Remplir la section 8. Plan de validation"
    echo "  liens        Remplir la section 9. Liens et References"
    echo "  rvav         Remplir la section 10. RVAV de la spec"
    echo ""
    echo "Exemples :"
    echo "  $0 spec-pipeline.001.01.ebauche.md objectif \"Definir comment les pipelines fonctionnent\""
    echo "  $0 spec-pipeline.001.01.ebauche.md titre \"Spec du pipeline\""
    echo "  $0 spec-pipeline.001.01.ebauche.md parent \"pense-bete-pipeline.001.01.ebauche.md\""
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
    local est_header="false"
    case "$section" in
        titre)
            marqueur="^# Gabarit -- Specification"
            est_titre="true"
            ;;
        parent)
            marqueur="^\\*\\*Pense-bete source :"
            est_header="true"
            ;;
        objectif)
            marqueur="^## 1. Objectif"
            ;;
        contexte)
            marqueur="^## 2. Contexte"
            ;;
        exigences)
            marqueur="^## 3. Exigences Fonctionnelles"
            ;;
        architecture)
            marqueur="^## 5. Architecture / Structure Technique"
            ;;
        risques)
            marqueur="^## 6. Contraintes et Risques"
            ;;
        livrables)
            marqueur="^## 7. Livrables attendus"
            ;;
        validation)
            marqueur="^## 8. Plan de validation"
            ;;
        liens)
            marqueur="^## 9. Liens et References"
            ;;
        rvav)
            marqueur="^## 10. RVAV de la spec"
            ;;
        *)
            echo -e "${RED}[ERREUR] Section inconnue : ${section}${NC}"
            echo "Sections disponibles : titre, parent, objectif, contexte, exigences, architecture, risques, livrables, validation, liens, rvav"
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
        sed -i "${ligne_section}s|.*|# Spec -- ${contenu}|" "$fichier"
    elif [ "$est_header" = "true" ]; then
        # Remplacer la ligne du header (pense-bete source)
        sed -i "${ligne_section}s|.*|**Pense-bete source :** ${contenu}|" "$fichier"
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
