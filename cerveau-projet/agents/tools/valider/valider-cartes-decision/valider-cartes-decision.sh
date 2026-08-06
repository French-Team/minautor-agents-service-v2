#!/bin/bash
# valider-cartes-decision.sh
# Outil pour verifier que les agents respectent les cartes de decision
# Proprietaire : Vulcain

# Configuration
AGENTS_DIR="cerveau-projet/agents"

# Fonction pour obtenir la date actuelle
get_date() {
    date +"%Y-%m-%d"
}

# Fonction pour verifier un agent
verifier_agent() {
    local agent=$1
    local fichier="$AGENTS_DIR/$agent/$agent.md"
    
    echo "=== Verification de l'agent : $agent ==="
    echo ""
    
    # Verifier que le fichier existe
    if [ ! -f "$fichier" ]; then
        echo "ERREUR : Le fichier $fichier n'existe pas"
        return 1
    fi
    
    # Verifier la section Carte de Decision
    echo "1. Verification de la section Carte de Decision"
    if grep -q 'CARTE DE DECISION' "$fichier"; then
        echo "   [OK] Section presente"
    else
        echo "   [ERREUR] Section manquante"
        return 1
    fi
    
    # Verifier le tableau des missions
    echo "2. Verification du tableau des missions"
    if grep -q "Missions disponibles" "$fichier"; then
        echo "   [OK] Tableau present"
    else
        echo "   [ERREUR] Tableau manquant"
        return 1
    fi
    
    # Verifier les details des missions
    echo "3. Verification des details des missions"
    if grep -q "Mission :" "$fichier"; then
        echo "   [OK] Details presents"
    else
        echo "   [ERREUR] Details manquants"
        return 1
    fi
    
    # Verifier les regles absolues
    echo "4. Verification des regles absolues"
    if grep -q 'REGLE ABSOLUE' "$fichier"; then
        echo "   [OK] Regles presentes"
    else
        echo "   [ERREUR] Regles manquantes"
        return 1
    fi
    
    echo ""
    echo "=== Resultat : CONFORME ==="
    return 0
}

# Fonction pour verifier tous les agents
verifier_tous() {
    echo "=== Verification de tous les agents ==="
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
    
    echo "=== Resume ==="
    echo "Agents verifies : $total"
    echo "Agents conformes : $conformes"
    echo "Agents non conformes : $((total - conformes))"
}

# Fonction pour verifier un fichier specifique
verifier_fichier() {
    local fichier=$1
    
    echo "=== Verification du fichier : $fichier ==="
    echo ""
    
    if [ ! -f "$fichier" ]; then
        echo "ERREUR : Le fichier $fichier n'existe pas"
        return 1
    fi
    
    # Verifier la section Carte de Decision
    echo "1. Verification de la section Carte de Decision"
    if grep -q 'CARTE DE DECISION' "$fichier"; then
        echo "   [OK] Section presente"
    else
        echo "   [ERREUR] Section manquante"
        return 1
    fi
    
    # Verifier le tableau des missions
    echo "2. Verification du tableau des missions"
    if grep -q "Missions disponibles" "$fichier"; then
        echo "   [OK] Tableau present"
    else
        echo "   [ERREUR] Tableau manquant"
        return 1
    fi
    
    # Verifier les details des missions
    echo "3. Verification des details des missions"
    if grep -q "Mission :" "$fichier"; then
        echo "   [OK] Details presents"
    else
        echo "   [ERREUR] Details manquants"
        return 1
    fi
    
    # Verifier les regles absolues
    echo "4. Verification des regles absolues"
    if grep -q 'REGLE ABSOLUE' "$fichier"; then
        echo "   [OK] Regles presentes"
    else
        echo "   [ERREUR] Regles manquantes"
        return 1
    fi
    
    echo ""
    echo "=== Resultat : CONFORME ==="
    return 0
}

# Fonction d'aide
afficher_aide() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --agent <nom>          Verifier un agent specifique"
    echo "  --tous                 Verifier tous les agents"
    echo "  --fichier <chemin>     Verifier un fichier specifique"
    echo "  --aide                 Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 --agent Buffy"
    echo "  $0 --tous"
    echo "  $0 --fichier cerveau-projet/agents/buffy/buffy.md"
}

# Point d'entree principal
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
