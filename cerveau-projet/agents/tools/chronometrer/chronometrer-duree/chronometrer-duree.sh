#!/bin/bash
# chronometrer-duree.sh
# Mesure la duree d une intervention d agent (journal traces/chronos.jsonl).
# Version : 0.1.2
# Statut : prepare

# ============================================================
# OUTIL BASSE SUR LE MODELE outil-template.sh (source de verite)
# ============================================================
# REGLE IMMUABLE DE NOMMAGE :
#   Le nom de l'outil DOIT commencer par le prefixe du dossier de categorie.
#   Le bloc verifier_nommage ci-dessous controle cela au demarrage.
#   (Ne pas supprimer ce bloc lors de la creation de l'outil)

# Configuration
VERSION="0.1.2"
STATUT="prepare"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== chronometrer-duree v${VERSION} ==="
    echo ""
    echo "Usage: $0 demarrer <session> <agent> | arreter <session> | etat [OPTIONS]"
    echo ""
    echo "Options :"
    echo "  --dry-run         Simuler sans appliquer"
    echo "  --verbose         Afficher les details"
    echo "  --help            Afficher cette aide"
    echo "  --doc             Afficher le .md complet et sortir"
    echo "  --confirme-doc    Confirmer la lecture de la doc (requis en mode reel)"
    echo ""
    echo "Exemples :"
    echo "  $0 demarrer session-llm-1 vulcain --confirme-doc"
    echo "  $0 arreter session-llm-1 --confirme-doc"
    echo "  $0 etat --confirme-doc"
    echo ""
}

# Verifier que le nom de l'outil commence par le prefixe de la categorie
verifier_nommage() {
    local script_nom=$(basename "$0" | sed 's/\.sh$//')
    [[ "$script_nom" == "outil-template" ]] && return 0
    local chemin_script=$(cd "$(dirname "$0")" 2>/dev/null && pwd)
    local categorie=$(basename "$(dirname "$chemin_script")")
    if [[ -z "$categorie" || "$categorie" == "." || "$categorie" == "/" ]]; then
        return 0
    fi
    if [[ "$script_nom" != "${categorie}-"* ]]; then
        echo -e "${RED}[ERREUR] Nommage invalide : $script_nom${NC}"
        echo -e "  Le nom doit commencer par '${categorie}-' (categorie: ${categorie}/)"
        exit 1
    fi
}

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
        return 0
    fi
    if [ "$confirme_doc" = "true" ]; then
        return 0
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

# MESSAGES INFORMATIONNELS (regle immuable v0.3.0)
afficher_messages_info() {
    local message
    if [ "$dry_run" = "true" ]; then
        return 0
    fi
    echo ""
    echo -e "${YELLOW}=== MESSAGES POUR L AGENT ===${NC}"
    for message in "$@"; do
        echo "  > $message"
    done
}

# ---------------------------------------------------------------------------
# Logique du chronometre (parite avec chronometrer-duree.py)
# ---------------------------------------------------------------------------

chemin_chronos() {
    if [ -n "$CHRONOS_FICHIER" ]; then
        echo "$CHRONOS_FICHIER"
        return
    fi
    # remonter de chronometrer/chronometrer-duree/ vers la racine projet
    local dossier
    dossier=$(cd "$(dirname "$0")" && pwd)
    # remonter de chronometrer/chronometrer-duree/ vers la racine projet :
    # chronometrer-duree -> chronometrer -> tools -> agents -> cerveau-projet
    local racine
    racine=$(cd "$dossier/../../../.." && pwd)
    echo "${racine}/agents/traces/chronos.jsonl"
}

chrono_actif_awk() {
    # Imprime la derniere entree ouverte (sans "date_fin") du fichier
    local fichier="$1"
    local session="$2"
    [ -f "$fichier" ] || return 0
    awk -v session="$session" '
        {
            if ($0 ~ /"date_fin": null/ || $0 ~ /"date_fin": null/) {
                if (session == "" || $0 ~ session) {
                    ligne = $0
                }
            }
        }
        END { if (ligne != "") print ligne }
    ' "$fichier"
}

formater_duree() {
    local secondes=$1
    if [ "$secondes" -lt 60 ]; then
        echo "${secondes}s"
    else
        echo "$((secondes / 60))min $((secondes % 60))s"
    fi
}

executer() {
    local action="$1"
    local session="$2"
    local agent="$3"
    local tokens="$4"
    local fichier
    fichier=$(chemin_chronos)

    case "$action" in
        demarrer)
            if [ -z "$session" ] || [ -z "$agent" ]; then
                echo -e "${RED}[ERREUR] demarrer <session> <agent> requis${NC}" >&2
                exit 1
            fi
            if [ "$dry_run" = "true" ]; then
                echo -e "${YELLOW}[DRY-RUN]${NC} demarrer $session $agent (aucun changement)"
                exit 0
            fi
            mkdir -p "$(dirname "$fichier")"
            # fermer un eventuel chrono ouvert pour cette session
            local actif
            actif=$(chrono_actif_awk "$fichier" "$session")
            if [ -n "$actif" ]; then
                # fermeture simple : reecriture via python (parite)
                CHRONOS_FICHIER="$fichier" python3 - "$session" "$agent" <<'PYEOF'
import io, json, os, sys
from datetime import datetime
session, agent = sys.argv[1], sys.argv[2]
fichier = os.environ["CHRONOS_FICHIER"]
entrees = []
if os.path.isfile(fichier):
    with io.open(fichier, encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if ligne:
                try:
                    entrees.append(json.loads(ligne))
                except ValueError:
                    pass
for e in reversed(entrees):
    if not e.get("date_fin") and e.get("session") == session:
        e["date_fin"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            from datetime import datetime as dt
            d = dt.strptime(e["date_debut"], "%Y-%m-%d %H:%M:%S")
            f = dt.strptime(e["date_fin"], "%Y-%m-%d %H:%M:%S")
            e["duree_secondes"] = max(0, int((f - d).total_seconds()))
        except (KeyError, ValueError):
            e["duree_secondes"] = 0
        break
with io.open(fichier, "w", encoding="utf-8", newline="\n") as fh:
    for e in entrees:
        fh.write(json.dumps(e, ensure_ascii=True) + "\n")
print("AVERTISSEMENT: chrono precedent ferme")
PYEOF
            fi
            local maintenant
            maintenant=$(date "+%Y-%m-%d %H:%M:%S")
            # snapshot tokens de debut (option --tokens, JSON) : utilise par
            # activer-agent-principal pour la conso par difference
            local tokens_json="null"
            if [ -n "$tokens" ]; then
                tokens_json="$tokens"
            fi
            echo "{\"date_debut\": \"$maintenant\", \"session\": \"$session\", \"agent\": \"$agent\", \"date_fin\": null, \"duree_secondes\": null, \"tokens_debut\": $tokens_json}" >> "$fichier"
            echo -e "${GREEN}[OK]${NC} Chrono demarre : $session / $agent"
            afficher_messages_info \
                "le chrono de $agent tourne : arreter a la fin de la mission (activer l agent suivant)" \
                "duree affichee dans AGENTS-historique au passage du relais (repere ###)"
            ;;
        arreter)
            if [ -z "$session" ]; then
                echo -e "${RED}[ERREUR] arreter <session> requis${NC}" >&2
                exit 1
            fi
            if [ "$dry_run" = "true" ]; then
                echo -e "${YELLOW}[DRY-RUN]${NC} arreter $session (aucun changement)"
                exit 0
            fi
            [ -f "$fichier" ] || { echo "AUCUN_CHRONO"; exit 0; }
            local resultat
            resultat=$(CHRONOS_FICHIER="$fichier" python3 - "$session" <<'PYEOF'
import io, json, os, sys
from datetime import datetime
session = sys.argv[1]
fichier = os.environ["CHRONOS_FICHIER"]
entrees = []
if os.path.isfile(fichier):
    with io.open(fichier, encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if ligne:
                try:
                    entrees.append(json.loads(ligne))
                except ValueError:
                    pass
actif = None
for e in reversed(entrees):
    if not e.get("date_fin") and e.get("session") == session:
        actif = e
        break
if actif is None:
    print("AUCUN_CHRONO")
    sys.exit(0)
actif["date_fin"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
try:
    d = datetime.strptime(actif["date_debut"], "%Y-%m-%d %H:%M:%S")
    f = datetime.strptime(actif["date_fin"], "%Y-%m-%d %H:%M:%S")
    actif["duree_secondes"] = max(0, int((f - d).total_seconds()))
except (KeyError, ValueError):
    actif["duree_secondes"] = 0
with io.open(fichier, "w", encoding="utf-8", newline="\n") as fh:
    for e in entrees:
        fh.write(json.dumps(e, ensure_ascii=True) + "\n")
secs = actif["duree_secondes"]
if secs < 60:
    duree = "%ds" % secs
else:
    duree = "%dmin %ds" % (secs // 60, secs % 60)
td = actif.get("tokens_debut") or {}
if td:
    print("%s | %s | %s" % (actif.get("agent", ""), duree,
                             json.dumps(td, ensure_ascii=True)))
else:
    print("%s | %s" % (actif.get("agent", ""), duree))
PYEOF
            )
            echo "$resultat"
            if [ "$resultat" != "AUCUN_CHRONO" ]; then
                afficher_messages_info \
                    "duree enregistree dans traces/chronos.jsonl" \
                    "activer-agent-principal ajoute la duree au repere ### de l entree de l agent dans AGENTS-historique"
            fi
            ;;
        etat)
            [ -f "$fichier" ] || { echo "Aucun chrono actif"; exit 0; }
            CHRONOS_FICHIER="$fichier" SESSION_FILTRE="$session" python3 - <<'PYEOF'
import io, json, os
fichier = os.environ["CHRONOS_FICHIER"]
session_filtre = os.environ.get("SESSION_FILTRE", "") or None
entrees = []
with io.open(fichier, encoding="utf-8") as fh:
    for ligne in fh:
        ligne = ligne.strip()
        if ligne:
            try:
                entrees.append(json.loads(ligne))
            except ValueError:
                pass
# COEXISTENCE MULTI-SESSIONS : etat <session> -> cette session ;
# etat (sans session) -> TOUS les chronos actifs, un par session.
actifs = {}
for e in entrees:
    if e.get("date_fin"):
        continue
    if session_filtre is not None and e.get("session") != session_filtre:
        continue
    actifs[e.get("session")] = e
if not actifs:
    if session_filtre:
        print("Aucun chrono actif pour %s" % session_filtre)
    else:
        print("Aucun chrono actif")
else:
    for e in actifs.values():
        print("Chrono actif : %s / %s (demarre %s)" % (e.get("session"), e.get("agent"), e.get("date_debut")))
PYEOF
            ;;
        *)
            echo -e "${RED}[ERREUR] action inconnue : $action${NC}" >&2
            afficher_aide
            exit 1
            ;;
    esac
}

# Main
main() {
    local dry_run="false"
    local verbose="false"
    local help="false"
    local doc="false"
    local confirme_doc="false"
    local action=""
    local session=""
    local agent=""
    local tokens=""

    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run) dry_run="true"; shift ;;
            --verbose) verbose="true"; shift ;;
            --help) help="true"; shift ;;
            --doc) doc="true"; shift ;;
            --confirme-doc) confirme_doc="true"; shift ;;
            --tokens) tokens="$2"; shift 2 ;;
            demarrer|arreter|etat) action="$1"; shift ;;
            *)
                if [ -z "$session" ]; then
                    session="$1"
                elif [ -z "$agent" ]; then
                    agent="$1"
                fi
                shift
                ;;
        esac
    done

    verifier_nommage

    verifier_doc_presente

    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi

    if [ "$doc" = "true" ]; then
        cat "${0%.*}.md"
        exit 0
    fi

    exiger_confirmation_doc "$dry_run" "$confirme_doc"

    if [ -z "$action" ]; then
        afficher_aide
        exit 0
    fi

    # propager le snapshot tokens (option --tokens) au sous-processus
    export CHRONO_TOKENS="$tokens"
    executer "$action" "$session" "$agent" "$tokens"
}

verifier_nommage
main "$@"
