#!/bin/bash
# mettre-a-jour-agents-md.sh
# Outil pour modifier AGENTS.md de maniere fiable
# Proprietaire : Vulcain
VERSION="0.2.0"

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

# Fonction pour obtenir le role d'un agent
get_agent_role() {
    local agent=$1
    case $agent in
        "Cerberus"|"cerberus")
            echo "Gardien de l'entree -- analyse et active les agents"
            ;;
        "Buffy"|"buffy")
            echo "Developpeur principal -- contenu et structures"
            ;;
        "Atlas"|"atlas")
            echo "Explorateur -- recherche et decouverte"
            ;;
        "Janus"|"janus")
            echo "Controleur des statuts -- validation et verification"
            ;;
        "Vulcain"|"vulcain")
            echo "Constructeur d'outils -- creation et developpement"
            ;;
        "Athena"|"athena")
            echo "Redactrice de pense-betes -- transformation des demandes"
            ;;
        "Morpheus"|"morpheus")
            echo "Testeur -- validation des outils et des tests"
            ;;
        "Promethee"|"promethee")
            echo "Redacteur de specs -- specification technique"
            ;;
        "Minerve"|"minerve")
            echo "Redactrice de todos -- organisation des taches"
            ;;
        "Clio"|"clio")
            echo "Muse de l'histoire -- mise a jour du README"
            ;;
        *)
            echo "Agent inconnu"
            ;;
    esac
}

# Lecon permanente (2026-08-07): verifier_ascii garantit qu'aucun caractere
# non-ASCII ne peut etre ecrit dans AGENTS-historique.md (cause racine de la
# corruption U+00E9 detectee lors de l'audit general).
# Retourne 0 si la chaine est 100% ASCII, 1 sinon.
verifier_ascii() {
    local chaine=$1
    CHAINE_ASCII="$chaine" python -c "
import os, sys
for ch in os.environ.get('CHAINE_ASCII', ''):
    if ord(ch) > 127:
        sys.exit(1)
sys.exit(0)
"
    return $?
}

# Verifier qu'un fichier entier est 100% ASCII.
# Affiche les lignes concernees et retourne 1 si non-ASCII detecte, 0 sinon.
verifier_fichier_ascii() {
    local fichier=$1
    python -c "
import io, sys
nb = 0
with io.open(sys.argv[1], encoding='utf-8', errors='replace') as fh:
    for i, l in enumerate(fh, 1):
        for ch in l:
            if ord(ch) > 127:
                nb += 1
                print('  Ligne ' + str(i) + ': caractere non-ASCII U+' + format(ord(ch), '04X'))
                break
sys.exit(1 if nb > 0 else 0)
" "$fichier"
    return $?
}

# Fonction pour ajouter une ligne dans l'historique (fichier separe)
# La ligne est inseree EN HAUT du tableau (ordre decroissant : les plus recentes en premier)
# Le fichier est limite a MAX_ENTREES_HISTORIQUE entrees
ajouter_historique() {
    local timestamp=$1
    local agent=$2
    local raison=$3
    
    # Verifier que le fichier historique existe
    if [ ! -f "$AGENTS_HISTORIQUE" ]; then
        echo "ERREUR: Le fichier $AGENTS_HISTORIQUE n'existe pas"
        return 1
    fi
    
    # Nouvelle ligne avec date et heure
    local nouvelle_ligne="| $timestamp | $agent | $raison |"
    
    # VERIFICATION ASCII PRE-ECRITURE (lecon permanente):
    # refuser toute ecriture non-ASCII, l'historique doit rester 100% pur
    if ! verifier_ascii "$nouvelle_ligne"; then
        echo "ERREUR: Caractere non-ASCII detecte dans la raison - ecriture historique REFUSEE"
        return 1
    fi
    
    # Inserer la ligne en haut du tableau (apres la ligne de separation)
    # puis ne garder que les MAX_ENTREES_HISTORIQUE plus recentes
    awk -v ligne="$nouvelle_ligne" -v max="$MAX_ENTREES_HISTORIQUE" '
        BEGIN { insere = 0; compteur = 0 }
        {
            # Ligne de separation du tableau -> inserer juste apres
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
    
    # VERIFICATION ASCII POST-ECRITURE (protection contre corruption pre-existante)
    if ! verifier_fichier_ascii "$AGENTS_HISTORIQUE"; then
        echo "WARNING: Caracteres non-ASCII presents dans $AGENTS_HISTORIQUE (voir lignes ci-dessus)"
    fi
    
    echo "Historique mis a jour dans $AGENTS_HISTORIQUE"
}

# Fonction pour activer un agent
activer_agent() {
    local agent=$1
    local raison=$2
    local mission=$3
    local date=$(get_date)
    local timestamp=$(get_timestamp)
    local role=$(get_agent_role "$agent")
    
    # VERIFICATION ASCII PREVENTIVE: refuser une raison non-ASCII avant
    # toute modification de AGENTS.md (lecon permanente)
    if ! verifier_ascii "$raison"; then
        echo "ERREUR: Caractere non-ASCII detecte dans la raison - activation REFUSEE"
        exit 1
    fi
    
    # Verifier que le fichier existe
    if [ ! -f "$AGENTS_FILE" ]; then
        echo "ERREUR: Le fichier $AGENTS_FILE n'existe pas"
        exit 1
    fi
    
    # Mettre a jour la section "Agent Principal Actuel"
    # NB: les sed sont robustes -- ils remplacent la valeur actuelle quel qu'elle soit
    sed -i "s/\*\*Nom\*\* | [^|]*/\*\*Nom\*\* | $agent/g" "$AGENTS_FILE"
    sed -i "s/\*\*Role\*\* | [^|]*/\*\*Role\*\* | $role/g" "$AGENTS_FILE"
    sed -i "s/\*\*Derniere mise a jour\*\* | [0-9-]*/\*\*Derniere mise a jour\*\* | $date/g" "$AGENTS_FILE"
    sed -i "s/\*\*Active par\*\* | [^|]*/\*\*Active par\*\* | Cerberus (automatique)/g" "$AGENTS_FILE"
    # NB: delimiter '#' pour supporter les raisons contenant des '/' (sinon le sed casse)
    sed -i "s#\*\*Raison\*\* | [^|]*#\*\*Raison\*\* | $raison#g" "$AGENTS_FILE"
    
    # Ajouter dans l'historique (fichier separe) avec date et heure
    ajouter_historique "$timestamp" "$agent" "$raison"
    
    echo "Agent $agent active avec succes"
}

# Fonction pour reactiver Cerberus
reactiver_cerberus() {
    local raison=$1
    local agent_precedent=$2
    local date=$(get_date)
    local timestamp=$(get_timestamp)
    
    # VERIFICATION ASCII PREVENTIVE: refuser une raison non-ASCII avant
    # toute modification de AGENTS.md (lecon permanente)
    if ! verifier_ascii "$raison"; then
        echo "ERREUR: Caractere non-ASCII detecte dans la raison - reactivation REFUSEE"
        exit 1
    fi
    
    # Verifier que les fichiers existent
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
    
    # Mettre a jour la section "Agent Principal Actuel"
    # NB: les sed sont robustes -- ils remplacent la valeur actuelle quel qu'elle soit
    sed -i "s/\*\*Nom\*\* | [^|]*/\*\*Nom\*\* | Cerberus/g" "$AGENTS_FILE"
    sed -i "s/\*\*Role\*\* | [^|]*/\*\*Role\*\* | Gardien de l'entree -- analyse et active les agents/g" "$AGENTS_FILE"
    sed -i "s/\*\*Derniere mise a jour\*\* | [0-9-]*/\*\*Derniere mise a jour\*\* | $date/g" "$AGENTS_FILE"
    sed -i "s/\*\*Active par\*\* | [^|]*/\*\*Active par\*\* | $agent_precedent (retour de mission)/g" "$AGENTS_FILE"
    # NB: delimiter '#' pour supporter les raisons contenant des '/' (sinon le sed casse)
    sed -i "s#\*\*Raison\*\* | [^|]*#\*\*Raison\*\* | $raison#g" "$AGENTS_FILE"
    
    # Ajouter dans l'historique (fichier separe) avec date et heure
    ajouter_historique "$timestamp" "Cerberus" "$raison"
    
    echo "Cerberus reactive avec succes"
}

# Fonction d'aide
afficher_aide() {
    echo "Usage: $0 <action> [parametres]"
    echo ""
    echo "Actions disponibles:"
    echo "  activer <agent> <raison> [mission]  - Activer un agent"
    echo "  reactiver <raison> <agent_precedent> - Reactiver Cerberus"
    echo "  aide                               - Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 activer Buffy \"Mission correction\" \"Mettre a jour demarrer.md\""
    echo "  $0 reactiver \"Mission terminee\" Buffy"
}

# Point d'entree principal
case $1 in
    "activer")
        if [ $# -lt 3 ]; then
            echo "ERREUR: Parametres manquants pour l'action 'activer'"
            afficher_aide
            exit 1
        fi
        activer_agent "$2" "$3" "$4"
        ;;
    "reactiver")
        if [ $# -lt 3 ]; then
            echo "ERREUR: Parametres manquants pour l'action 'reactiver'"
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
