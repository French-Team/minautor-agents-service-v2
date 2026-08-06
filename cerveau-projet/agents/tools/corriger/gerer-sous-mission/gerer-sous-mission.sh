#!/bin/bash
# gerer-sous-mission.sh
# Gère les sorties et retrées du flux principal
# Version: 0.1.0
# Date: 2026-08-05
# Auteur: Vulcain

# Configuration
VERSION="0.1.0"
DATE="2026-08-05"
DOSSIER_SAUVEGARDES="cerveau-projet/agents/vulcain/sauvegardes"

# Couleurs pour la sortie
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction d'aide
aide() {
    echo "=========================================="
    echo "  gerer-sous-mission v${VERSION}"
    echo "  Gère les sorties et retrées du flux"
    echo "=========================================="
    echo ""
    echo "Usage: gerer-sous-mission COMMANDE [OPTIONS]"
    echo ""
    echo "Commandes:"
    echo "  sauvegarder    Sauvegarder la position actuelle"
    echo "  sortir         Marquer la sortie du flux principal"
    echo "  revenir        Marquer le retour au flux principal"
    echo "  lister         Lister les sous-missions et positions"
    echo "  aide           Afficher cette aide"
    echo ""
    echo "Options pour sauvegarder:"
    echo "  --mission DESCRIPTION    Description de la mission"
    echo "  --etape NUMERO           Numéro de l'étape en cours"
    echo "  --donnees DONNEES        Données collectées"
    echo ""
    echo "Options pour sortir:"
    echo "  --raison RAISON          Raison de la sortie"
    echo "  --outil OUTIL            Outil nécessaire"
    echo ""
    echo "Options pour revenir:"
    echo "  --resultat RESULTAT      Résultat: succès/échec"
    echo "  --outil-créé OUI/NON    Outil créé: oui/non"
    echo ""
    echo "Exemples:"
    echo "  gerer-sous-mission sauvegarder --mission \"Créer outil\" --etape 1"
    echo "  gerer-sous-mission sortir --raison \"outil manquant\" --outil \"mon-outil\""
    echo "  gerer-sous-mission revenir --resultat succès --outil-créé oui"
    echo "  gerer-sous-mission lister"
    echo ""
}

# Créer le dossier de sauvegarde s'il n'existe pas
creer_dossier_sauvegardes() {
    if [[ ! -d "$DOSSIER_SAUVEGARDES" ]]; then
        mkdir -p "$DOSSIER_SAUVEGARDES"
    fi
}

# Fonction pour sauvegarder la position
sauvegarder() {
    local mission=""
    local etape=""
    local donnees=""
    
    # Parsing des arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --mission)
                mission="$2"
                shift 2
                ;;
            --etape)
                etape="$2"
                shift 2
                ;;
            --donnees)
                donnees="$2"
                shift 2
                ;;
            *)
                echo "Option inconnue: $1"
                exit 1
                ;;
        esac
    done
    
    # Vérification des paramètres
    if [[ -z "$mission" ]] || [[ -z "$etape" ]]; then
        echo "Erreur: --mission et --etape sont obligatoires"
        exit 1
    fi
    
    # Créer le dossier de sauvegarde
    creer_dossier_sauvegardes
    
    # Générer le nom du fichier
    local date_format=$(date +%Y%m%d_%H%M%S)
    local nom_fichier=$(echo "$mission" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
    local fichier="$DOSSIER_SAUVEGARDES/${nom_fichier}_${date_format}.json"
    
    # Créer le fichier de sauvegarde
    cat > "$fichier" << EOF
{
  "mission": "$mission",
  "etape": "$etape",
  "donnees": "$donnees",
  "date_sauvegarde": "$(date -Iseconds)",
  "sous_missions": []
}
EOF
    
    echo -e "${GREEN}✅ Position sauvegardée${NC}"
    echo "- Mission : $mission"
    echo "- Étape : $etape"
    echo "- Données : $donnees"
    echo "- Fichier : $fichier"
}

# Fonction pour marquer la sortie
sortir() {
    local raison=""
    local outil=""
    
    # Parsing des arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --raison)
                raison="$2"
                shift 2
                ;;
            --outil)
                outil="$2"
                shift 2
                ;;
            *)
                echo "Option inconnue: $1"
                exit 1
                ;;
        esac
    done
    
    # Vérification des paramètres
    if [[ -z "$raison" ]] || [[ -z "$outil" ]]; then
        echo "Erreur: --raison et --outil sont obligatoires"
        exit 1
    fi
    
    echo -e "${YELLOW}🔄 Sortie du flux principal${NC}"
    echo "- Raison : $raison"
    echo "- Outil nécessaire : $outil"
    echo "- Sous-mission : Créer/reprendre $outil"
    echo ""
    echo -e "${CYAN}Utilisez gerer-sous-mission revenir une fois la sous-mission terminée${NC}"
}

# Fonction pour marquer le retour
revenir() {
    local resultat=""
    local outil_cree=""
    
    # Parsing des arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --resultat)
                resultat="$2"
                shift 2
                ;;
            --outil-créé)
                outil_cree="$2"
                shift 2
                ;;
            *)
                echo "Option inconnue: $1"
                exit 1
                ;;
        esac
    done
    
    # Vérification des paramètres
    if [[ -z "$resultat" ]] || [[ -z "$outil_cree" ]]; then
        echo "Erreur: --resultat et --outil-créé sont obligatoires"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Retour au flux principal${NC}"
    echo "- Résultat : $resultat"
    echo "- Outil créé : $outil_cree"
    echo ""
    
    if [[ "$resultat" == "succès" ]] && [[ "$outil_cree" == "oui" ]]; then
        echo -e "${GREEN}L'outil est maintenant disponible !${NC}"
    elif [[ "$resultat" == "échec" ]]; then
        echo -e "${RED}La sous-mission a échoué.${NC}"
    fi
}

# Fonction pour lister les sous-missions
lister() {
    creer_dossier_sauvegardes
    
    echo -e "${BLUE}📋 Sous-missions et positions sauvegardées${NC}"
    echo ""
    
    local fichiers=$(find "$DOSSIER_SAUVEGARDES" -name "*.json" -type f 2>/dev/null | head -10)
    
    if [[ -z "$fichiers" ]]; then
        echo "Aucune sauvegarde trouvée."
        return
    fi
    
    local i=1
    for fichier in $fichiers; do
        echo -e "${CYAN}--- Sauvegarde $i ---${NC}"
        echo "Fichier : $fichier"
        echo ""
        
        # Extraire les informations du JSON (sans jq, on utilise grep/sed)
        local mission=$(grep '"mission"' "$fichier" | sed 's/.*"mission": *"//;s/".*//')
        local etape=$(grep '"etape"' "$fichier" | sed 's/.*"etape": *"//;s/".*//')
        local date_sauvegarde=$(grep '"date_sauvegarde"' "$fichier" | sed 's/.*"date_sauvegarde": *"//;s/".*//')
        
        echo "Mission : $mission"
        echo "Étape : $etape"
        echo "Date : $date_sauvegarde"
        echo ""
        
        i=$((i + 1))
    done
}

# Parsing des arguments principaux
if [[ $# -eq 0 ]]; then
    aide
    exit 0
fi

COMMANDE="$1"
shift

case $COMMANDE in
    sauvegarder)
        sauvegarder "$@"
        ;;
    sortir)
        sortir "$@"
        ;;
    revenir)
        revenir "$@"
        ;;
    lister)
        lister
        ;;
    aide|--aide|-h)
        aide
        ;;
    *)
        echo "Commande inconnue: $COMMANDE"
        echo "Utilisez 'gerer-sous-mission aide' pour l'aide"
        exit 1
        ;;
esac

exit 0
