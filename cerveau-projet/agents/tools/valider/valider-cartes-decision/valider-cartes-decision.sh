#!/bin/bash
# valider-cartes-decision.sh
# Outil pour vérifier que les agents respectent les cartes de décision
# Propriétaire : Vulcain

# Configuration
AGENTS_DIR="cerveau-projet/agents"

# Fonction pour obtenir la date actuelle
get_date() {
    date +"%Y-%m-%d"
}

# Fonction pour vérifier un agent
verifier_agent() {
    local agent=$1
    local fichier="$AGENTS_DIR/$agent/$agent.md"
    
    echo "=== Vérification de l'agent : $agent ==="
    echo ""
    
    # Vérifier que le fichier existe
    if [ ! -f "$fichier" ]; then
        echo "ERREUR : Le fichier $fichier n'existe pas"
        return 1
    fi
    
    # Vérifier la section Carte de Décision
    echo "1. Vérification de la section Carte de Décision"
    if grep -q "CARTE DE DÉCISION" "$fichier"; then
        echo "   [OK] Section présente"
    else
        echo "   [ERREUR] Section manquante"
        return 1
    fi
    
    # Vérifier le tableau des missions
    echo "2. Vérification du tableau des missions"
    if grep -q "Missions disponibles" "$fichier"; then
        echo "   [OK] Tableau présent"
    else
        echo "   [ERREUR] Tableau manquant"
        return 1
    fi
    
    # Vérifier les détails des missions
    echo "3. Vérification des détails des missions"
    if grep -q "Mission :" "$fichier"; then
        echo "   [OK] Détails présents"
    else
        echo "   [ERREUR] Détails manquants"
        return 1
    fi
    
    # Vérifier les règles absolues
    echo "4. Vérification des règles absolues"
    if grep -q "RÈGLE ABSOLUE" "$fichier"; then
        echo "   [OK] Règles présentes"
    else
        echo "   [ERREUR] Règles manquantes"
        return 1
    fi
    
    echo ""
    echo "=== Résultat : CONFORME ==="
    return 0
}

# Fonction pour vérifier tous les agents
verifier_tous() {
    echo "=== Vérification de tous les agents ==="
    echo ""
    
    local agents=("cerberus" "buffy" "atlas" "janus" "vulcain")
    local conformes=0
    local total=0
    
    for agent in "${agents[@]}"; do
        if [ -d "$AGENTS_DIR/$agent" ]; then
            total=$((total + 1))
            if verifier_agent "$agent"; then
                conformes=$((conformes + 1))
            fi
            echo ""
        fi
    done
    
    echo "=== Résumé ==="
    echo "Agents vérifiés : $total"
    echo "Agents conformes : $conformes"
    echo "Agents non conformes : $((total - conformes))"
}

# Fonction pour vérifier un fichier spécifique
verifier_fichier() {
    local fichier=$1
    
    echo "=== Vérification du fichier : $fichier ==="
    echo ""
    
    if [ ! -f "$fichier" ]; then
        echo "ERREUR : Le fichier $fichier n'existe pas"
        return 1
    fi
    
    # Vérifier la section Carte de Décision
    echo "1. Vérification de la section Carte de Décision"
    if grep -q "CARTE DE DÉCISION" "$fichier"; then
        echo "   [OK] Section présente"
    else
        echo "   [ERREUR] Section manquante"
        return 1
    fi
    
    # Vérifier le tableau des missions
    echo "2. Vérification du tableau des missions"
    if grep -q "Missions disponibles" "$fichier"; then
        echo "   [OK] Tableau présent"
    else
        echo "   [ERREUR] Tableau manquant"
        return 1
    fi
    
    # Vérifier les détails des missions
    echo "3. Vérification des détails des missions"
    if grep -q "Mission :" "$fichier"; then
        echo "   [OK] Détails présents"
    else
        echo "   [ERREUR] Détails manquants"
        return 1
    fi
    
    # Vérifier les règles absolues
    echo "4. Vérification des règles absolues"
    if grep -q "RÈGLE ABSOLUE" "$fichier"; then
        echo "   [OK] Règles présentes"
    else
        echo "   [ERREUR] Règles manquantes"
        return 1
    fi
    
    echo ""
    echo "=== Résultat : CONFORME ==="
    return 0
}

# Fonction d'aide
afficher_aide() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --agent <nom>          Vérifier un agent spécifique"
    echo "  --tous                 Vérifier tous les agents"
    echo "  --fichier <chemin>     Vérifier un fichier spécifique"
    echo "  --aide                 Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 --agent Buffy"
    echo "  $0 --tous"
    echo "  $0 --fichier cerveau-projet/agents/buffy/buffy.md"
}

# Point d'entrée principal
case $1 in
    "--agent")
        if [ -z "$2" ]; then
            echo "ERREUR : Nom de l'agent manquant"
            afficher_aide
            exit 1
        fi
        verifier_agent "$2"
        ;;
    "--tous")
        verifier_tous
        ;;
    "--fichier")
        if [ -z "$2" ]; then
            echo "ERREUR : Chemin du fichier manquant"
            afficher_aide
            exit 1
        fi
        verifier_fichier "$2"
        ;;
    "--aide"|"-h"|"")
        afficher_aide
        ;;
    *)
        echo "ERREUR : Option inconnue '$1'"
        afficher_aide
        exit 1
        ;;
esac
