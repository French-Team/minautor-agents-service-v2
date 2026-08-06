#!/bin/bash
# changer-statut.sh
# Change le statut d'un fichier en le renommant
# Propriétaire : Vulcain (outil partagé)

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VERBOSE=false
DRY_RUN=false
FORCE=false
FICHIER=""
NOUVEAU_STATUT=""

# Fonction pour afficher l'aide
afficher_aide() {
    echo "Usage: $0 <fichier> <nouveau-statut> [options]"
    echo ""
    echo "Change le statut d'un fichier en le renommant."
    echo ""
    echo "Statuts valides : ebauche, préparé, dev, test, valide"
    echo ""
    echo "Options:"
    echo "  --dry-run     Afficher les changements sans les appliquer"
    echo "  --force       Forcer le changement même si des liens pointent vers le fichier"
    echo "  --verbose     Afficher les détails"
    echo "  --aide        Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 protocole-xxx.001.01.ebauche.md préparé"
    echo "  $0 --dry-run protocole-xxx.001.01.ebauche.md préparé"
    echo "  $0 --force protocole-xxx.001.01.ebauche.md préparé"
}

# Fonction pour vérifier si le statut est valide
statut_valide() {
    local statut=$1
    case "$statut" in
        "ebauche"|"préparé"|"prepare"|"dev"|"test"|"valide")
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Fonction pour normaliser le statut (préparé → prepare)
normaliser_statut() {
    local statut=$1
    case "$statut" in
        "préparé") echo "prepare" ;;
        *) echo "$statut" ;;
    esac
}

# Fonction pour extraire les parties du nom de fichier
extraire_parties() {
    local fichier=$1
    local basename=$(basename "$fichier" .md)
    
    # Format: [type]-[theme].[id].[class].[statut]
    # Exemple: protocole-auto-correction.001.01.ebauche
    
    # Utiliser awk pour extraire les parties
    # Le séparateur est le point
    local parties=$(echo "$basename" | awk -F'.' '{
        # Nombre total de parties
        n = NF;
        
        # Statut = dernière partie
        statut = $n;
        
        # Class = avant-dernière partie
        class = $(n-1);
        
        # Id = troisième partie depuis la fin
        id = $(n-2);
        
        # Nom = tout sauf les 3 dernières parties
        nom = "";
        for (i = 1; i <= n-3; i++) {
            if (i > 1) nom = nom ".";
            nom = nom $i;
        }
        
        print nom "|" id "|" class "|" statut;
    }')
    
    echo "$parties"
}

# Fonction pour trouver les liens qui pointent vers ce fichier
trouver_liens() {
    local fichier=$1
    local dossier=$(dirname "$fichier")
    local basename=$(basename "$fichier")
    
    # Chercher les liens dans le même dossier et les sous-dossiers
    local liens=$(grep -r "\]$basename]" "$dossier" 2>/dev/null | head -5)
    
    if [ -n "$liens" ]; then
        echo "$liens"
    fi
}

# Fonction pour incrémenter le class
incrementer_class() {
    local class=$1
    local nouveau_class=$((class + 1))
    
    # Formater sur 2 chiffres
    printf "%02d" $nouveau_class
}

# Fonction principale pour changer le statut
changer_statut() {
    local fichier=$1
    local nouveau_statut=$2
    
    echo -e "${BLUE}=== Changement de statut ===${NC}"
    echo "Fichier : $fichier"
    echo "Nouveau statut : $nouveau_statut"
    echo ""
    
    # Vérifier que le fichier existe
    if [ ! -f "$fichier" ]; then
        echo -e "${RED}[ERREUR] Fichier non trouvé : $fichier${NC}"
        exit 1
    fi
    
    # Vérifier que le nouveau statut est valide
    if ! statut_valide "$nouveau_statut"; then
        echo -e "${RED}[ERREUR] Statut invalide : $nouveau_statut${NC}"
        echo "  Statuts valides : ebauche, préparé, dev, test, valide"
        exit 1
    fi
    
    # Normaliser le statut
    local nouveau_statut_norm=$(normaliser_statut "$nouveau_statut")
    
    # Extraire les parties du nom
    local parties=$(extraire_parties "$fichier")
    local nom_sans_statut=$(echo "$parties" | cut -d'|' -f1)
    local id=$(echo "$parties" | cut -d'|' -f2)
    local class_actuel=$(echo "$parties" | cut -d'|' -f3)
    local statut_actuel=$(echo "$parties" | cut -d'|' -f4)
    
    # Vérifier qu'on a bien extrait les informations
    if [ -z "$nom_sans_statut" ] || [ -z "$id" ] || [ -z "$class_actuel" ] || [ -z "$statut_actuel" ]; then
        echo -e "${RED}[ERREUR] Impossible d'extraire les parties du nom de fichier${NC}"
        echo "  Format attendu : [type]-[theme].[id].[class].[statut].md"
        exit 1
    fi
    
    # Incrémenter le class
    local nouveau_class=$(incrementer_class "$class_actuel")
    
    # Construire le nouveau nom
    local nouveau_nom="${nom_sans_statut}.${id}.${nouveau_class}.${nouveau_statut_norm}.md"
    local dossier=$(dirname "$fichier")
    local nouveau_chemin="$dossier/$nouveau_nom"
    
    echo -e "${BLUE}--- Détails ---${NC}"
    echo "Nom actuel : $(basename "$fichier")"
    echo "Nom nouveau : $nouveau_nom"
    echo "Class : $class_actuel → $nouveau_class"
    echo "Statut : $statut_actuel → $nouveau_statut_norm"
    echo ""
    
    # Vérifier si des liens pointent vers ce fichier
    echo -e "${BLUE}--- Vérification des liens ---${NC}"
    local liens=$(trouver_liens "$fichier")
    if [ -n "$liens" ]; then
        echo -e "${YELLOW}[ATTENTION]  Des liens pointent vers ce fichier :${NC}"
        echo "$liens"
        echo ""
        
        if [ "$FORCE" = false ]; then
            echo -e "${RED}[ERREUR] Utiliser --force pour ignorer les liens${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}[OK] Aucun lien trouvé${NC}"
    fi
    
    # Vérifier que le nouveau nom n'existe pas déjà
    if [ -f "$nouveau_chemin" ]; then
        echo -e "${RED}[ERREUR] Le fichier existe déjà : $nouveau_chemin${NC}"
        exit 1
    fi
    
    # Appliquer le changement
    echo ""
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY-RUN] Changement non appliqué${NC}"
        echo "  Renommer : $(basename "$fichier") → $nouveau_nom"
    else
        # Renommer le fichier
        mv "$fichier" "$nouveau_chemin"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[OK] Fichier renommé avec succès${NC}"
            echo "  $(basename "$fichier") → $nouveau_nom"
        else
            echo -e "${RED}[ERREUR] Erreur lors du renommage${NC}"
            exit 1
        fi
    fi
    
    echo ""
    echo -e "${GREEN}=== Terminé ===${NC}"
}

# Parser les arguments
while [ $# -gt 0 ]; do
    case $1 in
        "--aide"|"--help"|"-h")
            afficher_aide
            exit 0
            ;;
        "--verbose")
            VERBOSE=true
            shift
            ;;
        "--dry-run")
            DRY_RUN=true
            shift
            ;;
        "--force")
            FORCE=true
            shift
            ;;
        *)
            if [ -z "$FICHIER" ]; then
                FICHIER="$1"
            elif [ -z "$NOUVEAU_STATUT" ]; then
                NOUVEAU_STATUT="$1"
            fi
            shift
            ;;
    esac
done

# Vérifier les arguments
if [ -z "$FICHIER" ] || [ -z "$NOUVEAU_STATUT" ]; then
    echo -e "${RED}[ERREUR] Arguments manquants${NC}"
    afficher_aide
    exit 1
fi

# Changer le statut
changer_statut "$FICHIER" "$NOUVEAU_STATUT"
