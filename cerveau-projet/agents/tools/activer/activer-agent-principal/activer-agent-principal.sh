#!/bin/bash
# activer-agent-principal.sh
# Outil pour modifier AGENTS.md de maniere fiable, multi-session LLM
# Proprietaire : Vulcain
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.5.5"
STATUT="prepare"

# Configuration
AGENTS_FILE="${AGENTS_FILE:-AGENTS.md}"
AGENTS_HISTORIQUE="${AGENTS_HISTORIQUE:-AGENTS-historique.md}"
CLASSEUR_STOCKAGE="${CLASSEUR_STOCKAGE:-cerveau-projet/agents/classeur-variables/stockage/variables-actuelles.md}"
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
        "Hygie"|"hygie") echo "Agent de nettoyage -- seul agent habilite a acceder a tout le workspace et a supprimer sans demande prealable" ;;
        "Hermes"|"hermes") echo "Agent de la langue -- orthographe, vocabulaire et fautes de francais commises par les agents" ;;
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
        "Hygie"|"hygie") echo "cerveau-projet/agents/hygie/hygie.md" ;;
        "Hermes"|"hermes") echo "cerveau-projet/agents/hermes/hermes.md" ;;
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
        "Hygie"|"hygie") echo "cerveau-projet/agents/hygie/corrections.md" ;;
        "Hermes"|"hermes") echo "cerveau-projet/agents/hermes/corrections.md" ;;
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

# GARDE-FOU (v0.5.2) : detecter dans le repertoire courant les fichiers nommes
# comme des versions semver pures (ex: 0.2.1, v0.2.6) - residus probables de
# redirections accidentelles de sortie d une commande precedente (souvent la
# sortie de cet outil). Anti-residu : les supprimer, les sources de verite de
# version vivent dans cerveau-projet/agents/clio/.
verifier_residus_racine() {
    local residus
    residus=$(ls -p 2>/dev/null | grep -v '/' | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+$' | head -10)
    if [ -z "$residus" ]; then
        return 0
    fi
    echo "============================================================"
    echo "!!! WARNING GARDE-FOU (activer-agent-principal v$VERSION) !!!"
    echo "Des fichiers nommes comme des versions semver sont presents dans le"
    echo "repertoire courant (residus probables de redirections accidentelles"
    echo "de sortie) :"
    echo "$residus" | sed 's/^/    - /'
    echo "ANTI-RESIDU : supprimez-les. Les sources de verite de version vivent"
    echo "dans cerveau-projet/agents/clio/ (version-readme.txt,"
    echo "statut-projet.txt), JAMAIS a la racine."
    echo "============================================================"
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

# Trouver la session liee a un llm-id (SOURCE DOUBLE v0.4.0) :
# 1) AGENTS.md -- bloc avec le champ '**Nom LLM** | <id>' (ancien nom **Id LLM** accepte)
# 2) classeur -- ligne profil-session avec 'id: <llm-id>'
# Permet au LLM de se reconnaitre directement en lisant AGENTS.md.
trouver_session_par_id() {
    local llm_id=$1
    # 1. AGENTS.md : champ Nom LLM dans les blocs de session
    if [ -f "$AGENTS_FILE" ] && grep -q "^### Session : " "$AGENTS_FILE"; then
        local session_agents
        session_agents=$(awk -v cible="$llm_id" '
            /^### Session : / {
                session = $0
                sub(/^### Session : /, "", session)
                dans = 1
                next
            }
            dans == 1 && /^\| \*\*(Id LLM|Nom LLM)\*\* \| / {
                id = $0
                sub(/^\| \*\*(Id LLM|Nom LLM)\*\* \| /, "", id)
                sub(/ \|$/, "", id)
                if (id == cible) { print session; exit }
                dans = 0
            }
        ' "$AGENTS_FILE")
        if [ -n "$session_agents" ]; then
            echo "$session_agents"
            return 0
        fi
    fi
    # 2. Classeur : liaison id dans les lignes profil-session
    if [ ! -f "$CLASSEUR_STOCKAGE" ]; then
        return 0
    fi
    grep "id: $llm_id" "$CLASSEUR_STOCKAGE" 2>/dev/null | grep -oE "session: session-llm-[0-9]+" | head -1 | sed 's/session: //'
}

# Retourner l'id LLM lie a une session (AGENTS.md champ Nom LLM, puis classeur),
# ou vide si la session n'est liee a aucun id. Detecte un CONFLIT d'alignement.
id_lie_a_session() {
    local session=$1
    local id=""
    # 1. AGENTS.md
    if [ -f "$AGENTS_FILE" ] && grep -q "^### Session : " "$AGENTS_FILE"; then
        id=$(awk -v cible="$session" '
            /^### Session : / {
                s = $0
                sub(/^### Session : /, "", s)
                if (s == cible) { dans = 1 } else { dans = 0 }
                next
            }
            dans == 1 && /^\| \*\*(Id LLM|Nom LLM)\*\* \| / {
                ligne = $0
                sub(/^\| \*\*(Id LLM|Nom LLM)\*\* \| /, "", ligne)
                sub(/ \|$/, "", ligne)
                print ligne
                exit
            }
        ' "$AGENTS_FILE")
    fi
    if [ -n "$id" ]; then
        echo "$id"
        return 0
    fi
    # 2. Classeur
    if [ -f "$CLASSEUR_STOCKAGE" ]; then
        id=$(grep "session: $session" "$CLASSEUR_STOCKAGE" 2>/dev/null | grep -oE "id: [^ /]+" | head -1 | sed 's/^id: //')
    fi
    echo "$id"
}

# REGLE ALIGNEMENT (v0.4.0) : id llm-N -> session-llm-N (le numero de session porte
# le numero de l'id). Echo la session cible, ou rien si l'id n'est pas de la forme llm-N.
session_cible_pour_id() {
    local llm_id=$1
    case $llm_id in
        llm-[0-9]*) echo "session-llm-${llm_id#llm-}" ;;
        *) echo "" ;;
    esac
}

creer_bloc_session() {
    local session=$1
    local llm_id=$2
    if grep -q "^### Session : $session$" "$AGENTS_FILE"; then
        return 0
    fi
    local date=$(get_date)
    local role=$(get_agent_role "Cerberus")
    local fiche=$(get_agent_fiche "Cerberus")
    local corrections=$(get_agent_corrections "Cerberus")
    local champ_id=""
    if [ -n "$llm_id" ]; then
        champ_id="| **Nom LLM** | $llm_id |"
    fi
    local bloc
    if [ -n "$llm_id" ]; then
        bloc=$(printf '\n### Session : %s\n\n| Champ | Valeur |\n|---|---|\n| **Nom LLM** | %s |\n| **Nom Agent** | Cerberus |\n| **Role Agent** | %s |\n| **Derniere mise a jour** | %s |\n| **Fiche** | [%s](%s) |\n| **Corrections** | [%s](%s) |\n| **Active par** | Identification |\n| **Raison** | Identification LLM - demarrage de session |\n' "$session" "$llm_id" "$role" "$date" "$fiche" "$fiche" "$corrections" "$corrections")
    else
        bloc=$(printf '\n### Session : %s\n\n| Champ | Valeur |\n|---|---|\n| **Nom Agent** | Cerberus |\n| **Role Agent** | %s |\n| **Derniere mise a jour** | %s |\n| **Fiche** | [%s](%s) |\n| **Corrections** | [%s](%s) |\n| **Active par** | Identification |\n| **Raison** | Identification LLM - demarrage de session |\n' "$session" "$role" "$date" "$fiche" "$fiche" "$corrections" "$corrections")
    fi
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

# Ajouter ou mettre a jour le champ '**Nom LLM** | <id>' EN TETE du bloc de session.
# L'ancien champ **Id LLM** est migre vers **Nom LLM**. Les autres champs sont
# preserves (parametres vides) ou remplaces (parametres renseignes).
poser_nom_llm_bloc() {
    editer_bloc_session "$1" "" "" "" "" "" "" "" "$2"
}

# Editer les champs du bloc de session cible uniquement (awk), avec migration
# v0.5.0 : anciens noms (Nom, Role, Id LLM) -> nouveaux (Nom Agent, Role Agent,
# Nom LLM) et ordre canonique (Nom LLM en tete, puis Nom Agent, Role Agent...).
editer_bloc_session() {
    local session=$1
    local nom=$2
    local role=$3
    local date=$4
    local fiche=$5
    local corrections=$6
    local active_par=$7
    local raison=$8
    local nom_llm=$9
    awk -v session="$session" -v nom="$nom" -v role="$role" -v date="$date" \
        -v fiche="$fiche" -v corrections="$corrections" -v active_par="$active_par" -v raison="$raison" -v nom_llm="$nom_llm" '
        function emettre_bloc(   i, ligne, v_nom, v_role, v_date, v_fiche, v_corr, v_actif, v_raison, v_llm, v_suite, autres, na, a) {
            v_nom = ""; v_role = ""; v_date = ""; v_fiche = ""; v_corr = ""
            v_actif = ""; v_raison = ""; v_llm = ""; v_suite = ""; na = 0
            for (i in bloc) {
                ligne = bloc[i]
                if (ligne ~ /^\| \*\*(Id LLM|Nom LLM)\*\* \| /) { sub(/^\| \*\*(Id LLM|Nom LLM)\*\* \| /, "", ligne); sub(/ \|$/, "", ligne); v_llm = ligne }
                else if (ligne ~ /^\| \*\*(Nom Agent|Nom)\*\* \| /) { sub(/^\| \*\*(Nom Agent|Nom)\*\* \| /, "", ligne); sub(/ \|$/, "", ligne); v_nom = ligne }
                else if (ligne ~ /^\| \*\*(Role Agent|Role)\*\* \| /) { sub(/^\| \*\*(Role Agent|Role)\*\* \| /, "", ligne); sub(/ \|$/, "", ligne); v_role = ligne }
                else if (ligne ~ /^\| \*\*Derniere mise a jour\*\* \| /) { sub(/^\| \*\*Derniere mise a jour\*\* \| /, "", ligne); sub(/ \|$/, "", ligne); v_date = ligne }
                else if (ligne ~ /^\| \*\*Fiche\*\* \| /) { sub(/^\| \*\*Fiche\*\* \| /, "", ligne); sub(/ \|$/, "", ligne); sub(/^\[/, "", ligne); sub(/\]\(.*$/, "", ligne); v_fiche = ligne }
                else if (ligne ~ /^\| \*\*Corrections\*\* \| /) { sub(/^\| \*\*Corrections\*\* \| /, "", ligne); sub(/ \|$/, "", ligne); sub(/^\[/, "", ligne); sub(/\]\(.*$/, "", ligne); v_corr = ligne }
                else if (ligne ~ /^\| \*\*Active par\*\* \| /) { sub(/^\| \*\*Active par\*\* \| /, "", ligne); sub(/ \|$/, "", ligne); v_actif = ligne }
                else if (ligne ~ /^\| \*\*Raison\*\* \| /) { sub(/^\| \*\*Raison\*\* \| /, "", ligne); sub(/ \|$/, "", ligne); v_raison = ligne }
                else if (ligne ~ /^\| \*\*/) { autres[na++] = ligne }
                else if (v_raison != "") { v_suite = v_suite ligne "\n" }
            }
            if (nom != "") v_nom = nom
            if (role != "") v_role = role
            if (date != "") v_date = date
            if (fiche != "") v_fiche = fiche
            if (corrections != "") v_corr = corrections
            if (active_par != "") v_actif = active_par
            if (raison != "") v_raison = raison
            if (nom_llm != "") v_llm = nom_llm
            if (v_suite != "") v_raison = v_raison "\n" substr(v_suite, 1, length(v_suite) - 1)
            print ""
            print "| Champ | Valeur |"
            print "|---|---|"
            if (v_llm != "") print "| **Nom LLM** | " v_llm " |"
            if (v_nom != "") print "| **Nom Agent** | " v_nom " |"
            if (v_role != "") print "| **Role Agent** | " v_role " |"
            if (v_date != "") print "| **Derniere mise a jour** | " v_date " |"
            if (v_fiche != "") print "| **Fiche** | [" v_fiche "](" v_fiche ") |"
            if (v_corr != "") print "| **Corrections** | [" v_corr "](" v_corr ") |"
            if (v_actif != "") print "| **Active par** | " v_actif " |"
            if (v_raison != "") {
                n = split(v_raison, lignes_r, "\n")
                print "| **Raison** | " lignes_r[1] " |"
                for (k = 2; k <= n; k++) print lignes_r[k]
            }
            for (a = 0; a < na; a++) print autres[a]
        }
        BEGIN { dans_bloc = 0; nb = 0 }
        {
            if (dans_bloc == 1 && ($0 ~ /^### Session : / || $0 ~ /^## /)) {
                emettre_bloc()
                dans_bloc = 0
                delete bloc
                nb = 0
            }
            if ($0 == ("### Session : " session)) { dans_bloc = 1; nb = 0; print; next }
            if (dans_bloc == 1) { bloc[nb++] = $0; next }
            print
        }
        END { if (dans_bloc == 1) emettre_bloc() }
    ' "$AGENTS_FILE" > "$AGENTS_FILE.tmp" && mv "$AGENTS_FILE.tmp" "$AGENTS_FILE"
}

# Ecrire ou mettre a jour profil-session-<session> dans le classeur-variables
# REGLE LIAISON ID (v0.3.5) : si llm_id non fourni (activer/reactiver), lire l'id deja
# lie dans la ligne existante et le PRESERVER -- sinon la liaison id<->session posee par
# sidentifier serait ECRASEE et le prochain sidentifier creerait une session fantome.
mettre_a_jour_profil_session() {
    local session=$1
    local agent=$2
    local llm_id=$3
    local timestamp=$(get_timestamp)
    local jour=$(get_date)
    local bq=$(python -c "import sys; sys.stdout.write(chr(96))")  # backtick
    # REGLE DE DERIVATION (IMMUABLE): id = profil-session- + partie apres le prefixe session-
    local id_session="${session#session-}"
    local prefixe_ligne="| ${bq}profil-session-$id_session${bq}"

    # REGLE LIAISON ID (v0.3.5): preserver l'id existant si non fourni
    if [ -z "$llm_id" ] && [ -f "$CLASSEUR_STOCKAGE" ]; then
        llm_id=$(grep -F "$prefixe_ligne" "$CLASSEUR_STOCKAGE" 2>/dev/null | grep -oE "id: [^ /]+" | head -1 | sed 's/^id: //')
    fi

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

# Reconstruire la section '## Sessions connues' d'AGENTS.md a partir du classeur
# (lignes profil-session-*) : table | Session | Nom LLM | Agent actif | Derniere activite |.
# Relit AGENTS_FILE, remplace/insere la section, reecrit.
mettre_a_jour_sessions_connues() {
    CLASSEUR_ENV="$CLASSEUR_STOCKAGE" AGENTS_ENV="$AGENTS_FILE" python - << 'PYEOF'
import io, os, re, sys
classeur = os.environ.get('CLASSEUR_ENV', '')
agents_file = os.environ.get('AGENTS_ENV', '')
if not os.path.isfile(classeur) or not os.path.isfile(agents_file):
    sys.exit(0)
lignes = []
with io.open(classeur, encoding='utf-8', errors='replace') as fh:
    for ligne in fh:
        if 'profil-session-' not in ligne:
            continue
        m = re.search(r'session: (session-llm-\d+)', ligne)
        if not m:
            continue
        session = m.group(1)
        mid = re.search(r'id: (\S+)', ligne)
        llm_id = mid.group(1) if mid else '-'
        mage = re.search(r'agent: (\S+)', ligne)
        agent = mage.group(1) if mage else '?'
        mdate = re.search(r'date: (\S+ \S+)', ligne)
        date = mdate.group(1) if mdate else '-'
        lignes.append((session, llm_id, agent, date))
if not lignes:
    sys.exit(0)

def cle_session(entree):
    m = re.search(r'session-llm-(\d+)', entree[0])
    return int(m.group(1)) if m else 0

lignes.sort(key=cle_session)
table = ('## Sessions connues' + chr(10) + chr(10) +
         '| Session | Nom LLM | Agent actif | Derniere activite |' + chr(10) +
         '|---|---|---|---|' + chr(10))
for session, llm_id, agent, date in lignes:
    table += '| ' + session + ' | ' + llm_id + ' | ' + agent + ' | ' + date + ' |' + chr(10)

with io.open(agents_file, encoding='utf-8', errors='replace') as fh:
    contenu = fh.read()
ls = contenu.split(chr(10))
sortie = []
i = 0
while i < len(ls):
    if ls[i].strip() == '## Sessions connues':
        i += 1
        while i < len(ls) and not ls[i].startswith('## '):
            i += 1
        continue
    sortie.append(ls[i])
    i += 1
contenu = chr(10).join(sortie)
if '## Configuration Active' in contenu:
    contenu = contenu.replace('## Configuration Active', table + '## Configuration Active', 1)
else:
    contenu = contenu.rstrip(chr(10)) + chr(10) + chr(10) + table
with io.open(agents_file, 'w', encoding='utf-8', newline=chr(10)) as fh:
    fh.write(contenu)
PYEOF
    return $?
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
            if (index($0, "| 20") == 1) {
                if (insere == 0) {
                    print ligne
                    insere = 1
                    compteur++
                }
                if (compteur < max) {
                    print $0
                    compteur++
                }
                next
            }
            print $0
        }
        END { if (insere == 0) print ligne }
    ' "$AGENTS_HISTORIQUE" > "$AGENTS_HISTORIQUE.tmp" && mv "$AGENTS_HISTORIQUE.tmp" "$AGENTS_HISTORIQUE"

    if ! verifier_fichier_ascii "$AGENTS_HISTORIQUE"; then
        echo "WARNING: Caracteres non-ASCII presents dans $AGENTS_HISTORIQUE (voir lignes ci-dessus)"
    fi

    echo "Historique mis a jour dans $AGENTS_HISTORIQUE"
}

# Retourner l'agent REEL du bloc de session (champ Nom Agent), ou Cerberus
# si absent. CORRECTION v0.5.1 : sidentifier ecrivait Cerberus en dur, ce qui
# falsifiait le profil classeur quand un AUTRE agent (ex: morpheus) etait actif
# -> double source contradictoire -> l agent s arretait au demarrage.
agent_actif_bloc() {
    local session=$1
    if [ ! -f "$AGENTS_FILE" ]; then
        echo "Cerberus"
        return 0
    fi
    awk -v cible="$session" '
        /^### Session : / {
            if (session != "") {
                if (session == cible) { print nom; exit }
            }
            session = $0
            sub(/^### Session : /, "", session)
            nom = "Cerberus"
            next
        }
        /^\| \*\*(Nom Agent|Nom)\*\* \| / {
            nom = $0
            sub(/^\| \*\*(Nom Agent|Nom)\*\* \| /, "", nom)
            sub(/ \|$/, "", nom)
        }
        END { if (session == cible) { print nom } }
    ' "$AGENTS_FILE"
}

# S'identifier : creer/choisir sa session (agent principal = agent reel du bloc,
# Cerberus pour une nouvelle session)
sidentifier() {
    local llm_id=$1
    local session=""
    migrer_si_necessaire

    if [ -n "$llm_id" ]; then
        # MODE ID : chercher si cet id est deja lie (AGENTS.md champ Nom LLM + classeur)
        session=$(trouver_session_par_id "$llm_id")
        if [ -n "$session" ]; then
            local agent_affiche=$(agent_actif_bloc "$session")
            echo "Session retrouvee pour id $llm_id : $session (agent principal : $agent_affiche)"
        else
            # REGLE ALIGNEMENT (v0.4.0) : id llm-N -> session-llm-N
            local cible=$(session_cible_pour_id "$llm_id")
            if [ -n "$cible" ]; then
                local id_deja_lie=$(id_lie_a_session "$cible")
                if [ -n "$id_deja_lie" ] && [ "$id_deja_lie" != "$llm_id" ]; then
                    # CONFLIT : session-llm-N deja liee a un autre LLM
                    if [ "$MIGRE" = "1" ]; then
                        session="session-llm-1"
                    else
                        session=$(trouver_prochaine_session)
                    fi
                    echo "ATTENTION: $cible deja liee a l'id $id_deja_lie - attribution $session (agent principal : Cerberus)"
                else
                    # Libre ou orpheline (aucun id) -> absorption
                    session="$cible"
                    echo "Nouvelle session pour id $llm_id : $session (alignee sur l'id, agent principal : Cerberus)"
                fi
            else
                if [ "$MIGRE" = "1" ]; then
                    session="session-llm-1"
                else
                    session=$(trouver_prochaine_session)
                fi
                echo "Nouvelle session pour id $llm_id : $session (agent principal : Cerberus)"
            fi
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
        creer_bloc_session "$session" "$llm_id"
    elif [ -n "$llm_id" ]; then
        # Bloc existant : poser/mettre a jour le champ Nom LLM (reconnaissance par lecture)
        poser_nom_llm_bloc "$session" "$llm_id"
    fi

    local agent_actif=$(agent_actif_bloc "$session")
    local timestamp=$(get_timestamp)
    ajouter_historique "$timestamp" "$session" "$agent_actif" "Identification LLM - demarrage de session"
    mettre_a_jour_profil_session "$session" "$agent_actif" "$llm_id"
    mettre_a_jour_sessions_connues
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
    # v0.5.4 : instruction de demarrage automatique (anti-bug arret a c0)
    local raison_finale="$raison"
    if [ "$agent" != "cerberus" ] && [[ "$raison" != *"DEMARRAGE OBLIGATOIRE"* ]]; then
        raison_finale="$raison

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \\
  cerveau-projet/agents/$agent/parcours/parcours-$agent.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case par
case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>')."
    fi
    editer_bloc_session "$session" "$agent" "$role" "$date" "$fiche" "$corrections" "Cerberus (automatique)" "$raison_finale"

    ajouter_historique "$timestamp" "$session" "$agent" "$raison_finale"
    mettre_a_jour_profil_session "$session" "$agent"
    mettre_a_jour_sessions_connues
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
    mettre_a_jour_sessions_connues
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
        /^\| \*\*(Nom Agent|Nom)\*\* \| / {
            nom = $0
            sub(/^\| \*\*(Nom Agent|Nom)\*\* \| /, "", nom)
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
    echo "  sidentifier [id]                 - S'identifier (MODE ID: id llm-N -> session-llm-N, agent principal = Cerberus)"
    echo "  activer <session> <agent> <raison> [mission]  - Activer un agent dans sa session"
    echo "  reactiver <session> <raison> <agent_precedent> - Reactiver Cerberus dans sa session"
    echo "  sessions                           - Lister les sessions et leur agent principal"
    echo "  aide                               - Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 sidentifier llm-1"
    echo "  $0 activer session-llm-1 Buffy \"Mission correction\""
    echo "  $0 reactiver session-llm-1 \"Mission terminee\" Buffy"
}

# Point d'entree principal
# GARDE-FOU (v0.5.2) : les actions reelles declenchent la detection des residus
case $1 in
    "sidentifier"|"activer"|"reactiver"|"sessions")
        verifier_residus_racine
        ;;
esac

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
        echo "activer-agent-principal v$VERSION ($STATUT)"
        ;;
    *)
        echo "ERREUR: Action inconnue '$1'"
        afficher_aide
        exit 1
        ;;
esac
