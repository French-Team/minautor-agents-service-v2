#!/bin/bash
# modifier-agents-md.sh
# Outil pour modifier AGENTS.md de manière fiable
# Propriétaire : Vulcain

# Configuration
AGENTS_FILE="AGENTS.md"
AGENTS_HISTORIQUE="AGENTS-historique.md"
CERBERUS_FICHE="cerveau-projet/agents/cerberus/cerberus.md"
MAX_ENTREES_HISTORIQUE=150

# Fonction pour obtenir la date actuelle (format YYYY-MM-DD)
get_date() {
    date +"%Y-%m-%d"
}

# Fonction pour obtenir la date et l'heure actuelles (format YYYY-MM-DD HH:MM)
get_timestamp() {
    date +"%Y-%m-%d %H:%M"
}

# Fonction pour obtenir le rôle d'un agent
get_agent_role() {
    local agent=$1
    case $agent in
        "Cerberus"|"cerberus")
            echo "Gardien de l'entrée — analyse et active les agents"
            ;;
        "Buffy"|"buffy")
            echo "Développeur principal — contenu et structures"
            ;;
        "Atlas"|"atlas")
            echo "Explorateur — recherche et découverte"
            ;;
        "Janus"|"janus")
            echo "Contrôleur des statuts — validation et vérification"
            ;;
        "Vulcain"|"vulcain")
            echo "Constructeur d'outils — création et développement"
            ;;
        "Athena"|"athena")
            echo "Rédactrice de pense-bêtes — transformation des demandes"
            ;;
        "Morpheus"|"morpheus")
            echo "Testeur — validation des outils et des tests"
            ;;
        "Promethee"|"promethee")
            echo "Rédacteur de specs — specification technique"
            ;;
        "Minerve"|"minerve")
            echo "Rédactrice de todos — organisation des taches"
            ;;
        "Clio"|"clio")
            echo "Muse de l'histoire — mise a jour du README"
            ;;
        *)
            echo "Agent inconnu"
            ;;
    esac
}

# Fonction pour ajouter une ligne dans l'historique (fichier séparé)
# La ligne est insérée EN HAUT du tableau (ordre décroissant : les plus récentes en premier)
# Le fichier est limité à MAX_ENTREES_HISTORIQUE entrées
ajouter_historique() {
    local timestamp=$1
    local agent=$2
    local raison=$3
    
    # Vérifier que le fichier historique existe
    if [ ! -f "$AGENTS_HISTORIQUE" ]; then
        echo "ERREUR: Le fichier $AGENTS_HISTORIQUE n'existe pas"
        return 1
    fi
    
    # Nouvelle ligne avec date et heure
    local nouvelle_ligne="| $timestamp | $agent | $raison |"
    
    # Insérer la ligne en haut du tableau (après la ligne de séparation)
    # puis ne garder que les MAX_ENTREES_HISTORIQUE plus récentes
    awk -v ligne="$nouvelle_ligne" -v max="$MAX_ENTREES_HISTORIQUE" '
        BEGIN { insere = 0; compteur = 0 }
        {
            # Ligne de séparation du tableau -> insérer juste après
            if ($0 ~ /^\|---/) {
                print $0
                if (insere == 0) {
                    print ligne
                    insere = 1
                    compteur++
                }
                next
            }
            # Ligne d intervention (commence par | 20XX-XX-XX)
            if ($0 ~ /^\| 20[0-9][0-9]-/) {
                if (compteur < max) {
                    print $0
                    compteur++
                }
                next
            }
            print $0
        }
    ' "$AGENTS_HISTORIQUE" > "$AGENTS_HISTORIQUE.tmp" && mv "$AGENTS_HISTORIQUE.tmp" "$AGENTS_HISTORIQUE"
    
    echo "Historique mis à jour dans $AGENTS_HISTORIQUE"
}

# Fonction pour activer un agent
activer_agent() {
    local agent=$1
    local raison=$2
    local mission=$3
    local date=$(get_date)
    local timestamp=$(get_timestamp)
    local role=$(get_agent_role "$agent")
    
    # Vérifier que le fichier existe
    if [ ! -f "$AGENTS_FILE" ]; then
        echo "ERREUR: Le fichier $AGENTS_FILE n'existe pas"
        exit 1
    fi
    
    # Mettre à jour la section "Agent Principal Actuel"
    # NB: les sed sont robustes — ils remplacent la valeur actuelle quel qu'elle soit
    sed -i "s/\*\*Nom\*\* | [^|]*/\*\*Nom\*\* | $agent/g" "$AGENTS_FILE"
    sed -i "s/\*\*Rôle\*\* | [^|]*/\*\*Rôle\*\* | $role/g" "$AGENTS_FILE"
    sed -i "s/\*\*Dernière mise à jour\*\* | [0-9-]*/\*\*Dernière mise à jour\*\* | $date/g" "$AGENTS_FILE"
    sed -i "s/\*\*Activé par\*\* | [^|]*/\*\*Activé par\*\* | Cerberus (automatique)/g" "$AGENTS_FILE"
    # NB: delimiter '#' pour supporter les raisons contenant des '/' (sinon le sed casse)
    sed -i "s#\*\*Raison\*\* | [^|]*#\*\*Raison\*\* | $raison#g" "$AGENTS_FILE"
    
    # Ajouter dans l'historique (fichier séparé) avec date et heure
    ajouter_historique "$timestamp" "$agent" "$raison"
    
    echo "Agent $agent activé avec succès"
}

# Fonction pour réactiver Cerberus
reactiver_cerberus() {
    local raison=$1
    local agent_precedent=$2
    local date=$(get_date)
    local timestamp=$(get_timestamp)
    
    # Vérifier que les fichiers existent
    if [ ! -f "$AGENTS_FILE" ]; then
        echo "ERREUR: Le fichier $AGENTS_FILE n'existe pas"
        exit 1
    fi
    
    if [ ! -f "$CERBERUS_FICHE" ]; then
        echo "ERREUR: Le fichier $CERBERUS_FICHE n'existe pas"
        exit 1
    fi
    
    # Lire la fiche de Cerberus
    echo "Lecture de $CERBERUS_FICHE..."
    cat "$CERBERUS_FICHE" > /dev/null
    
    # Mettre à jour la section "Agent Principal Actuel"
    # NB: les sed sont robustes — ils remplacent la valeur actuelle quel qu'elle soit
    sed -i "s/\*\*Nom\*\* | [^|]*/\*\*Nom\*\* | Cerberus/g" "$AGENTS_FILE"
    sed -i "s/\*\*Rôle\*\* | [^|]*/\*\*Rôle\*\* | Gardien de l'entrée — analyse et active les agents/g" "$AGENTS_FILE"
    sed -i "s/\*\*Dernière mise à jour\*\* | [0-9-]*/\*\*Dernière mise à jour\*\* | $date/g" "$AGENTS_FILE"
    sed -i "s/\*\*Activé par\*\* | [^|]*/\*\*Activé par\*\* | $agent_precedent (retour de mission)/g" "$AGENTS_FILE"
    # NB: delimiter '#' pour supporter les raisons contenant des '/' (sinon le sed casse)
    sed -i "s#\*\*Raison\*\* | [^|]*#\*\*Raison\*\* | $raison#g" "$AGENTS_FILE"
    
    # Ajouter dans l'historique (fichier séparé) avec date et heure
    ajouter_historique "$timestamp" "Cerberus" "$raison"
    
    echo "Cerberus réactivé avec succès"
}

# Fonction d'aide
afficher_aide() {
    echo "Usage: $0 <action> [paramètres]"
    echo ""
    echo "Actions disponibles:"
    echo "  activer <agent> <raison> [mission]  - Activer un agent"
    echo "  reactiver <raison> <agent_precedent> - Réactiver Cerberus"
    echo "  aide                               - Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 activer Buffy \"Mission correction\" \"Mettre à jour demarrer.md\""
    echo "  $0 reactiver \"Mission terminée\" Buffy"
}

# Point d'entrée principal
case $1 in
    "activer")
        if [ $# -lt 3 ]; then
            echo "ERREUR: Paramètres manquants pour l'action 'activer'"
            afficher_aide
            exit 1
        fi
        activer_agent "$2" "$3" "$4"
        ;;
    "reactiver")
        if [ $# -lt 3 ]; then
            echo "ERREUR: Paramètres manquants pour l'action 'reactiver'"
            afficher_aide
            exit 1
        fi
        reactiver_cerberus "$2" "$3"
        ;;
    "aide"|"--help"|"-h"|"")
        afficher_aide
        ;;
    *)
        echo "ERREUR: Action inconnue '$1'"
        afficher_aide
        exit 1
        ;;
esac
