#!/bin/bash
# [nom-outil].sh
# [Description courte de ce que fait l'outil]
# Version : 0.2.0-beta
# Statut : ebauche

# ============================================================
# OUTIL-TEMPLATE - MODELE DE SCRIPT
# ============================================================
# Instructions d'utilisation de ce template :
#   1. Copier ce fichier vers agents/tools/[categorie]/[nom-outil]/[nom-outil].sh
#      (categorie = dossier d'ACTION : ajouter, analyser, corriger, lister, ...)
#   2. Remplacer [nom-outil] par le nom reel de l'outil
#   3. Remplacer [Description courte] par la vraie description
#   4. Completer les fonctions selon le besoin
#   5. Remplir le modele de documentation [nom-outil].md (outil-template.md)
#   6. Ajouter l'outil dans index-tools.md
#   7. Assigner l'outil a l'agent concerne (protocole-outils Regle 6)
#   8. Tester en --dry-run avant toute utilisation
#   9. Valider la conformite ASCII avec valider-conformite-ascii
# ============================================================
# REGLE IMMUABLE DE NOMMAGE :
#   Le nom de l'outil DOIT commencer par le prefixe du dossier de categorie.
#   Exemples : dossier 'rechercher/' -> outil 'rechercher-xxx'
#             dossier 'lire/'       -> outil 'lire-xxx'
#   Le bloc verifier_nommage ci-dessous controle cela au demarrage.
#   (Ne pas supprimer ce bloc lors de la creation de l'outil)

# Configuration
VERSION="0.2.0-beta"
STATUT="ebauche"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== [nom-outil] v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] [ARGUMENTS]"
    echo ""
    echo "Options :"
    echo "  --dry-run         Simuler sans appliquer"
    echo "  --verbose         Afficher les details"
    echo "  --help            Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 [argument 1]"
    echo "  $0 --dry-run [argument 1]"
    echo ""
}

# Fonction utilitaire : verifier qu'un argument est fourni
verifier_argument() {
    local valeur="$1"
    local nom="$2"
    if [ -z "$valeur" ]; then
        echo -e "${RED}[ERREUR] L'argument '${nom}' est obligatoire${NC}"
        afficher_aide
        exit 1
    fi
}

# Verifier que le nom de l'outil commence par le prefixe de la categorie (regle immuable)
# Structure : tools/[categorie]/[outil]/[outil].sh
verifier_nommage() {
    local script_nom=$(basename "$0" | sed 's/\.sh$//')
    # outil-template est un modele, pas un outil -> exemption
    [[ "$script_nom" == "outil-template" ]] && return 0
    # Extraire la categorie (2 niveaux au-dessus du fichier)
    local chemin_script=$(cd "$(dirname "$0")" 2>/dev/null && pwd)
    local categorie=$(basename "$(dirname "$chemin_script")")
    if [[ -z "$categorie" || "$categorie" == "." || "$categorie" == "/" ]]; then
        return 0
    fi
    if [[ "$script_nom" != "${categorie}-"* ]]; then
        echo -e "${RED}[ERREUR] Nommage invalide : $script_nom${NC}"
        echo -e "  Le nom doit commencer par '${categorie}-' (categorie: ${categorie}/)"
        echo -e "  Exemple attendu : ${categorie}-$(echo "$script_nom" | sed 's/^[a-z]*-//')"
        echo -e "  Voir convention-renommage.md (regle immuable)"
        exit 1
    fi
}

# Fonction principale de l'outil
# [Description de ce que fait cette fonction]
# PROTECTION DOC (regle immuable) : le .md doit exister a cote du script.
verifier_doc_presente() {
    local script="$0"
    local doc="${script%.*}.md"
    if [ ! -f "$doc" ]; then
        echo -e "${RED}[ERREUR]${NC} Documentation manquante : ${doc}" >&2
        echo "  Le .md de l outil est OBLIGATOIRE (regle immuable, protocole-outils)." >&2
        exit 2
    fi
}

# Affiche la section Utilisation du .md (auto-affichage en cas de refus).
afficher_section_utilisation() {
    local script="$0"
    local doc="${script%.*}.md"
    if [ ! -f "$doc" ]; then
        return
    fi
    local dans_usage="false"
    while IFS= read -r ligne; do
        if [[ "$ligne" == "## "* ]]; then
            case "$ligne" in
                "## Utilisation"*|"## UTILISATION"*|"## utilisation"*)
                    dans_usage="true"
                    ;;
                *)
                    dans_usage="false"
                    ;;
            esac
            continue
        fi
        if [ "$dans_usage" = "true" ] && [ -n "$ligne" ]; then
            echo "  $ligne"
        fi
    done < "$doc"
}

# PROTECTION DOC : le mode reel exige --confirme-doc (lecture du .md).
exiger_confirmation_doc() {
    local dry_run="$1"
    local confirme_doc="$2"
    if [ "$dry_run" = "true" ]; then
        return 0  # le dry-run est le mode de decouverte, libre
    fi
    if [ "$confirme_doc" = "true" ]; then
        return 0  # l agent a confirme la lecture de la documentation
    fi
    verifier_doc_presente
    echo -e "${YELLOW}=== DOCUMENTATION OBLIGATOIRE ===${NC}"
    echo "  Cet outil exige la lecture de sa documentation avant usage reel."
    echo "  Section Utilisation de $0.md :"
    echo ""
    afficher_section_utilisation
    echo ""
    echo -e "${RED}[REFUS]${NC} Relancez avec --confirme-doc apres lecture de la doc." >&2
    exit 2
}

executer() {
    local cible="$1"
    
    # [Logique de l'outil ici]
    echo -e "${BLUE}[INFO]${NC} Traitement de : ${cible}"
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} Aucune modification appliquee"
    else
        # [Actions reelles ici]
        echo -e "${GREEN}[OK]${NC} Operation terminee"
    fi
}

# Main
main() {
    local dry_run="false"
    local verbose="false"
    local help="false"
    local doc="false"
    local confirme_doc="false"
    local cible=""
    
    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run="true"
                shift
                ;;
            --verbose)
                verbose="true"
                shift
                ;;
            --help)
                help="true"
                shift
                ;;
            --doc)
                doc="true"
                shift
                ;;
            --confirme-doc)
                confirme_doc="true"
                shift
                ;;
            *)
                cible="$1"
                shift
                ;;
        esac
    done
    
    # Verifier la regle immuable de nommage (au demarrage)
    verifier_nommage
    
    # PROTECTION DOC : le .md doit exister
    verifier_doc_presente
    
    # Afficher l'aide
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    # --doc : afficher la documentation complete et sortir
    if [ "$doc" = "true" ]; then
        local md="${0%.*}.md"
        cat "$md"
        exit 0
    fi
    
    # PROTECTION DOC : le mode reel exige --confirme-doc
    exiger_confirmation_doc "$dry_run" "$confirme_doc"
    
    # Verifier les arguments obligatoires
    verifier_argument "$cible" "cible"
    
    # Executer
    executer "$cible"
}

# Verifier le nommage au demarrage (regle immuable)
verifier_nommage

# Executer
main "$@"
