#!/bin/bash
# activer-agent-principal.sh
# Outil pour modifier AGENTS.md de maniere fiable, multi-session LLM
# Proprietaire : Vulcain
VERSION="0.3.4"

# Configuration
AGENTS_FILE="${AGENTS_FILE:-AGENTS.md}"
AGENTS_HISTORIQUE="${AGENTS_HISTORIQUE:-AGENTS-historique.md}"
CLASSEUR_STOCKAGE="${CLASSEUR_STOCKAGE:-cerveau-projet/classeur-variables/stockage/variables-actuelles.md}"
CERBERUS_FICHE="cerveau-projet/agents/cerberus/cerberus.md"
MAX_ENTREES_HISTORIQUE=150
PREFIXE_SESSION="session-llm-"

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
        "Cerberus"|"cerberus") echo "Gardien de l'entree -- analyse et active les agents" ;;
        "Buffy"|"buffy") echo "Developpeur principal -- contenu et structures" ;;
        "Atlas"|"atlas") echo "Explorateur -- recherche et decouverte" ;;
        "Janus"|"janus") echo "Controleur des statuts -- validation et verification" ;;
        "Vulcain"|"vulcain") echo "Constructeur d'outils -- creation et developpement" ;;
        "Athena"|"athena") echo "Redactrice de pense-betes -- transformation des demandes" ;;
        "Morpheus"|"morpheus") echo "Testeur -- validation des outils et des tests" ;;
        "Promethee"|"promethee") echo "Redacteur de specs -- specification technique" ;;
        "Minerve"|"minerve") echo "Redactrice de todos -- organisation des taches" ;;
        "Clio"|"clio") echo "Muse de l'histoire -- mise a jour du README" ;;
        "Themis"|"themis") echo "Evaluatrice croisee -- evaluation et audit" ;;
        *) echo "Agent inconnu" ;;
    esac
}

# Fonction pour obtenir la fiche d'un agent
get_agent_fiche() {
    local agent=$1
    case $agent in
        "Cerberus"|"cerberus") echo "cerveau-projet/agents/cerberus/cerberus.md" ;;
        "Buffy"|"buffy") echo "cerveau-projet/agents/buffy/buffy.md" ;;
        "Atlas"|"atlas") echo "cerveau-projet/agents/atlas/atlas.md" ;;
        "Janus"|"janus") echo "cerveau-projet/agents/janus/janus.md" ;;
        "Vulcain"|"vulcain") echo "cerveau-projet/agents/vulcain/vulcain.md" ;;
        "Athena"|"athena") echo "cerveau-projet/agents/athena/athena.md" ;;
        "Morpheus"|"morpheus") echo "cerveau-projet/agents/morpheus/morpheus.md" ;;
        "Promethee"|"promethee") echo "cerveau-projet/agents/promethee/promethee.md" ;;
        "Minerve"|"minerve") echo "cerveau-projet/agents/minerve/minerve.md" ;;
        "Clio"|"clio") echo "cerveau-projet/agents/clio/clio.md" ;;
        "Themis"|"themis") echo "cerveau-projet/agents/themis/themis.md" ;;
        *) echo "cerveau-projet/agents/inconnu/inconnu.md" ;;
    esac
}

# Fonction pour obtenir les corrections d'un agent
get_agent_corrections() {
    local agent=$1
    case $agent in
        "Cerberus"|"cerberus") echo "cerveau-projet/agents/cerberus/corrections.md" ;;
        "Buffy"|"buffy") echo "cerveau-projet/agents/buffy/corrections.md" ;;
        "Atlas"|"atlas") echo "cerveau-projet/agents/atlas/corrections.md" ;;
        "Janus"|"janus") echo "cerveau-projet/agents/janus/corrections.md" ;;
        "Vulcain"|"vulcain") echo "cerveau-projet/agents/vulcain/corrections.md" ;;
        "Athena"|"athena") echo "cerveau-projet/agents/athena/corrections.md" ;;
        "Morpheus"|"morpheus") echo "cerveau-projet/agents/morpheus/corrections.md" ;;
        "Promethee"|"promethee") echo "cerveau-projet/agents/promethee/corrections.md" ;;
        "Minerve"|"minerve") echo "cerveau-projet/agents/minerve/corrections.md" ;;
        "Clio"|"clio") echo "cerveau-projet/agents/clio/corrections.md" ;;
        "Themis"|"themis") echo "cerveau-projet/agents/themis/corrections.md" ;;
        *) echo "cerveau-projet/agents/inconnu/corrections.md" ;;
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

# Migrer l'ancienne structure mono-session (## Agent Principal Actuel)
# vers la nouvelle structure multi-session (## Sessions LLM).
# Definit MIGRE=1 si la conversion a eu lieu.
migrer_si_necessaire() {
    MIGRE=0
    if ! grep -q "^## Sessions LLM" "$AGENTS_FILE"; then
        if grep -q "^## Agent Principal Actuel" "$AGENTS_FILE"; then
            sed -i "s/^## Agent Principal Actuel$/## Sessions LLM/" "$AGENTS_FILE"
            sed -i "s/^## Sessions LLM$/## Sessions LLM\n\n### Session : session-llm-1/" "$AGENTS_FILE"
            MIGRE=1
        fi
    fi
}

# Trouver le prochain session-llm-N libre
trouver_prochaine_session() {
    local n=1
    while grep -q "^### Session : ${PREFIXE_SESSION}$n$" "$AGENTS_FILE"; do
        n=$((n+1))
    done
    echo "${PREFIXE_SESSION}$n"
}

# Creer un bloc de session (Cerberus par defaut) si absent
trouver_session_par_id() {
    local llm_id=$1
    if [ ! -f "$CLASSEUR_STOCKAGE" ]; then
        return 0
    fi
    grep "id: $llm_id" "$CLASSEUR_STOCKAGE" 2>/dev/null | grep -oE "session: session-llm-[0-9]+" | head -1 | sed 's/session: //'
}

creer_bloc_session() {
    local session=$1
    if grep -q "^### Session : $session$" "$AGENTS_FILE"; then
        return 0
    fi
    local date=$(get_date)
    local role=$(get_agent_role "Cerberus")
    local fiche=$(get_agent_fiche "Cerberus")
    local corrections=$(get_agent_corrections "Cerberus")
    local bloc
    bloc=$(printf '\n### Session : %s\n\n| Champ | Valeur |\n|---|---|\n| **Nom** | Cerberus |\n| **Role** | %s |\n| **Derniere mise a jour** | %s |\n| **Fiche** | [%s](%s) |\n| **Corrections** | [%s](%s) |\n| **Active par** | Identification |\n| **Raison** | Identification LLM - demarrage de session |\n' "$session" "$role" "$date" "$fiche" "$fiche" "$corrections" "$corrections")
    awk -v bloc="$bloc" '
        /^## Sessions LLM$/ {
            print $0
            print bloc
            bloc = ""
            next
        }
        { print }
        END { if (bloc != "") print bloc }
    ' "$AGENTS_FILE" > "$AGENTS_FILE.tmp" && mv "$AGENTS_FILE.tmp" "$AGENTS_FILE"
}

# Editer les champs du bloc de session cible uniquement (awk)
editer_bloc_session() {
    local session=$1
    local nom=$2
    local role=$3
    local date=$4
    local fiche=$5
    local corrections=$6
    local active_par=$7
    local raison=$8
    awk -v session="$session" -v nom="$nom" -v role="$role" -v date="$date" \
        -v fiche="$fiche" -v corrections="$corrections" -v active_par="$active_par" -v raison="$raison" '
        BEGIN { dans_bloc = 0 }
        {
            if (dans_bloc == 1 && ($0 ~ /^### Session : / || $0 ~ /^## /)) { dans_bloc = 0 }
            if ($0 == ("### Session : " session)) { dans_bloc = 1 }
            if (dans_bloc == 1) {
                if ($0 ~ /^\| \*\*Nom\*\* \| /) { print "| **Nom** | " nom " |"; next }
                if ($0 ~ /^\| \*\*Role\*\* \| /) { print "| **Role** | " role " |"; next }
                if ($0 ~ /^\| \*\*Derniere mise a jour\*\* \| /) { print "| **Derniere mise a jour** | " date " |"; next }
                if ($0 ~ /^\| \*\*Fiche\*\* \| /) { print "| **Fiche** | [" fiche "](" fiche ") |"; next }
                if ($0 ~ /^\| \*\*Corrections\*\* \| /) { print "| **Corrections** | [" corrections "](" corrections ") |"; next }
                if ($0 ~ /^\| \*\*Active par\*\* \| /) { print "| **Active par** | " active_par " |"; next }
                if ($0 ~ /^\| \*\*Raison\*\* \| /) { print "| **Raison** | " raison " |"; next }
            }
            print
        }
    ' "$AGENTS_FILE" > "$AGENTS_FILE.tmp" && mv "$AGENTS_FILE.tmp" "$AGENTS_FILE"
}

# Ecrire ou mettre a jour profil-session-<session> dans le classeur-variables
mettre_a_jour_profil_session() {
    local session=$1
    local agent=$2
    local llm_id=$3
    local timestamp=$(get_timestamp)
    local jour=$(get_date)
    local bq=$(python -c "import sys; sys.stdout.write(chr(96))")  # backtick
    # REGLE DE DERIVATION (IMMUABLE): id = profil-session- + partie apres le prefixe session-
    local id_session="${session#session-}"
    if [ -n "$llm_id" ]; then
        local nouvelle_ligne="| ${bq}profil-session-$id_session${bq} | session: $session / id: $llm_id / agent: $agent / date: $timestamp | activer-agent-principal | $jour | [OK] |"
    else
        local nouvelle_ligne="| ${bq}profil-session-$id_session${bq} | session: $session / agent: $agent / date: $timestamp | activer-agent-principal | $jour | [OK] |"
    fi

    if ! verifier_ascii "$nouvelle_ligne"; then
        echo "ERREUR: Caractere non-ASCII dans le profil session - ecriture classeur REFUSEE"
        return 1
    fi

    if [ ! -f "$CLASSEUR_STOCKAGE" ]; then
        echo "WARNING: Fichier classeur $CLASSEUR_STOCKAGE introuvable - profil session non ecrit"
        return 1
    fi

    CLASSEUR_LIGNE="$nouvelle_ligne" CLASSEUR_FICHIER="$CLASSEUR_STOCKAGE" CLASSEUR_SESSION="$session" python -c "
import io, os, sys
bt = chr(96)
ligne = os.environ.get('CLASSEUR_LIGNE', '')
fichier = os.environ.get('CLASSEUR_FICHIER', '')
session = os.environ.get('CLASSEUR_SESSION', '')
id_session = session[len('session-'):] if session.startswith('session-') else session
prefixe = '| ' + bt + 'profil-session-' + id_session + bt
with io.open(fichier, encoding='utf-8', errors='replace') as fh:
    lignes = fh.read().split(chr(10))
trouve = False
for i, l in enumerate(lignes):
    if l.startswith(prefixe):
        lignes[i] = ligne
        trouve = True
        break
if not trouve:
    idx = -1
    for i, l in enumerate(lignes):
        if l.startswith('| ' + bt):
            idx = i
    if idx >= 0:
        lignes.insert(idx + 1, ligne)
    else:
        lignes.append(ligne)
with io.open(fichier, 'w', encoding='utf-8', newline=chr(10)) as fh:
    fh.write(chr(10).join(lignes))
print('Profil session mis a jour dans ' + fichier + ' : ' + session)
"
}

# Ajouter une entree dans l'historique (4 colonnes, en haut, max 150)
ajouter_historique() {
    local timestamp=$1
    local session=$2
    local agent=$3
    local raison=$4

    if [ ! -f "$AGENTS_HISTORIQUE" ]; then
        echo "ERREUR: Le fichier $AGENTS_HISTORIQUE n'existe pas"
        return 1
    fi

    local nouvelle_ligne="| $timestamp | $session | $agent | $raison |"

    if ! verifier_ascii "$nouvelle_ligne"; then
        echo "ERREUR: Caractere non-ASCII detecte dans la raison - ecriture historique REFUSEE"
        return 1
    fi

    awk -v ligne="$nouvelle_ligne" -v max="$MAX_ENTREES_HISTORIQUE" '
        BEGIN { insere = 0; compteur = 0 }
        {
            if ($0 ~ /^\|---/) {
                print $0
                if (insere == 0) {
                    print ligne
                    insere = 1
                    compteur++
                }
                next
            }
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

    if ! verifier_fichier_ascii "$AGENTS_HISTORIQUE"; then
        echo "WARNING: Caracteres non-ASCII presents dans $AGENTS_HISTORIQUE (voir lignes ci-dessus)"
    fi

    echo "Historique mis a jour dans $AGENTS_HISTORIQUE"
}

# S'identifier : creer/choisir sa session (agent principal = Cerberus)
sidentifier() {
    local llm_id=$1
    local session=""
    migrer_si_necessaire

    if [ -n "$llm_id" ]; then
        # MODE ID : chercher si cet id est deja lie a une session dans le classeur
        session=$(trouver_session_par_id "$llm_id")
        if [ -n "$session" ]; then
            echo "Session retrouvee pour id $llm_id : $session (agent principal : Cerberus)"
        else
            # id inconnu -> prochaine session libre + liaison
            if [ "$MIGRE" = "1" ]; then
                session="session-llm-1"
            else
                session=$(trouver_prochaine_session)
            fi
            echo "Nouvelle session pour id $llm_id : $session (agent principal : Cerberus)"
        fi
    else
        # Sans argument : compatibilite heritage -> prochaine session libre
        if [ "$MIGRE" = "1" ]; then
            session="session-llm-1"
        else
            session=$(trouver_prochaine_session)
        fi
        echo "Session attribuee : $session (agent principal : Cerberus)"
    fi

    if ! grep -q "^### Session : $session$" "$AGENTS_FILE"; then
        creer_bloc_session "$session"
    fi

    local timestamp=$(get_timestamp)
    ajouter_historique "$timestamp" "$session" "Cerberus" "Identification LLM - demarrage de session"
    mettre_a_jour_profil_session "$session" "Cerberus" "$llm_id"
}

activer_agent() {
    local session=$1
    local agent=$2
    local raison=$3
    local mission=$4
    local date=$(get_date)
    local timestamp=$(get_timestamp)

    if ! verifier_ascii "$raison"; then
        echo "ERREUR: Caractere non-ASCII detecte dans la raison - activation REFUSEE"
        exit 1
    fi

    if [ ! -f "$AGENTS_FILE" ]; then
        echo "ERREUR: Le fichier $AGENTS_FILE n'existe pas"
        exit 1
    fi

    local role=$(get_agent_role "$agent")
    if [ "$role" = "Agent inconnu" ]; then
        echo "ERREUR: Agent inconnu '$agent'"
        exit 1
    fi

    migrer_si_necessaire
    creer_bloc_session "$session"

    local fiche=$(get_agent_fiche "$agent")
    local corrections=$(get_agent_corrections "$agent")
    editer_bloc_session "$session" "$agent" "$role" "$date" "$fiche" "$corrections" "Cerberus (automatique)" "$raison"

    ajouter_historique "$timestamp" "$session" "$agent" "$raison"
    mettre_a_jour_profil_session "$session" "$agent"
    echo "Session $session : agent $agent active avec succes"
}

# Reactiver Cerberus dans sa session
reactiver_cerberus() {
    local session=$1
    local raison=$2
    local agent_precedent=$3
    local date=$(get_date)
    local timestamp=$(get_timestamp)

    if ! verifier_ascii "$raison"; then
        echo "ERREUR: Caractere non-ASCII detecte dans la raison - reactivation REFUSEE"
        exit 1
    fi

    if [ ! -f "$AGENTS_FILE" ]; then
        echo "ERREUR: Le fichier $AGENTS_FILE n'existe pas"
        exit 1
    fi

    if [ ! -f "$CERBERUS_FICHE" ]; then
        echo "ERREUR: Le fichier $CERBERUS_FICHE n'existe pas"
        exit 1
    fi

    echo "Lecture de $CERBERUS_FICHE..."
    cat "$CERBERUS_FICHE" > /dev/null

    migrer_si_necessaire
    creer_bloc_session "$session"

    local role=$(get_agent_role "Cerberus")
    local fiche=$(get_agent_fiche "Cerberus")
    local corrections=$(get_agent_corrections "Cerberus")
    editer_bloc_session "$session" "Cerberus" "$role" "$date" "$fiche" "$corrections" "$agent_precedent (retour de mission)" "$raison"

    ajouter_historique "$timestamp" "$session" "Cerberus" "$raison"
    mettre_a_jour_profil_session "$session" "Cerberus"
    echo "Session $session : Cerberus reactive avec succes"
}

# Lister les sessions et leur agent principal
lister_sessions() {
    if [ ! -f "$AGENTS_FILE" ]; then
        echo "ERREUR: Le fichier $AGENTS_FILE n'existe pas"
        exit 1
    fi
    if ! grep -q "^### Session : " "$AGENTS_FILE"; then
        echo "Aucune session LLM enregistree"
        return 0
    fi
    awk '
        /^### Session : / {
            if (session != "") { print session " : " nom }
            session = $0
            sub(/^### Session : /, "", session)
            nom = "?"
            next
        }
        /^\| \*\*Nom\*\* \| / {
            nom = $0
            sub(/^\| \*\*Nom\*\* \| /, "", nom)
            sub(/ \|$/, "", nom)
        }
        END { if (session != "") { print session " : " nom } }
    ' "$AGENTS_FILE"
}

# Fonction d'aide
afficher_aide() {
    echo "Usage: $0 <action> [parametres]"
    echo ""
    echo "Actions disponibles:"
    echo "  sidentifier [session]              - Creer/choisir sa session (agent principal = Cerberus)"
    echo "  activer <session> <agent> <raison> [mission]  - Activer un agent dans sa session"
    echo "  reactiver <session> <raison> <agent_precedent> - Reactiver Cerberus dans sa session"
    echo "  sessions                           - Lister les sessions et leur agent principal"
    echo "  aide                               - Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 sidentifier"
    echo "  $0 sidentifier session-llm-1"
    echo "  $0 activer session-llm-1 Buffy \"Mission correction\""
    echo "  $0 reactiver session-llm-1 \"Mission terminee\" Buffy"
}

# Point d'entree principal
case $1 in
    "sidentifier")
        sidentifier "$2"
        ;;
    "activer")
        if [ $# -lt 4 ]; then
            echo "ERREUR: Parametres manquants pour l'action 'activer' (session, agent, raison)"
            afficher_aide
            exit 1
        fi
        activer_agent "$2" "$3" "$4" "$5"
        ;;
    "reactiver")
        if [ $# -lt 4 ]; then
            echo "ERREUR: Parametres manquants pour l'action 'reactiver' (session, raison, agent_precedent)"
            afficher_aide
            exit 1
        fi
        reactiver_cerberus "$2" "$3" "$4"
        ;;
    "sessions")
        lister_sessions
        ;;
    "aide"|"--help"|"-h"|"")
        afficher_aide
        ;;
    "--version")
        echo "activer-agent-principal v$VERSION"
        ;;
    *)
        echo "ERREUR: Action inconnue '$1'"
        afficher_aide
        exit 1
        ;;
esac
