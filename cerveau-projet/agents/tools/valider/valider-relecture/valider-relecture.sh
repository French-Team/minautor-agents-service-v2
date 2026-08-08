#!/bin/bash
# valider-relecture.sh
# Verifie que chaque fiche d'agent et son corrections.md contiennent la regle de relecture
# Version : 0.2.0
# Statut : prepare

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier
# ============================================================

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
STATUT="prepare"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== valider-relecture v${VERSION} ==="
    echo ""
    echo "Verifie que chaque agent porte la regle de relecture de sa fiche"
    echo "(fiche [agent].md + corrections.md), a chaque activation."
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options :"
    echo "  --agent <nom>     Verifier un seul agent"
    echo "  --verbose         Afficher la ligne ou la regle a ete trouvee"
    echo "  --help            Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0                          # Verifier tous les agents"
    echo "  $0 --agent buffy            # Verifier uniquement Buffy"
    echo "  $0 --verbose                # Avec le detail des regles trouvees"
    echo ""
}

# Verifier que le nom de l'outil commence par le prefixe de la categorie (regle immuable)
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
        echo -e "  Voir convention-renommage.md (regle immuable)"
        exit 1
    fi
}

# Mots-cles acceptes pour la regle de relecture dans UNE fiche d'agent
# (la fiche peut utiliser des formulations differentes)
fiche_a_regle_relecture() {
    local fichier="$1"
    # Formulations equivalentes : RELECTURE, "relis MA fiche", "sa fiche et SES corrections",
    # "MA fiche et MES corrections" (formulation de cerberus.md)
    grep -qiE 'RELECTURE|relis MA fiche|relire sa fiche|sa fiche et SES corrections|MA fiche et MES corrections' "$fichier" 2>/dev/null
    return $?
}

# Mots-cles acceptes pour la regle de relecture dans corrections.md
corrections_a_regle_relecture() {
    local fichier="$1"
    # Formulations equivalentes : "Relire sa fiche", "relecture", "relis MA fiche"
    grep -qiE 'Relire sa fiche|relecture|relis MA fiche' "$fichier" 2>/dev/null
    return $?
}

# Ligne ou la regle a ete trouvee (mode verbose)
ligne_regle() {
    local fichier="$1"
    grep -niE 'RELECTURE|relis MA fiche|relire sa fiche|sa fiche et SES corrections|MA fiche et MES corrections|relecture' "$fichier" 2>/dev/null | head -1 | cut -d: -f1
}

# Verifier un agent
verifier_agent() {
    local agent="$1"
    local verbose="$2"
    local base="cerveau-projet/agents/$agent"
    local fiche="$base/$agent.md"
    local corrections="$base/corrections.md"

    if [ ! -f "$fiche" ]; then
        echo -e "${RED}[MANQUE] $agent : fiche absente ($fiche)${NC}"
        return 1
    fi
    if [ ! -f "$corrections" ]; then
        echo -e "${RED}[MANQUE] $agent : corrections absentes ($corrections)${NC}"
        return 1
    fi

    local ok_fiche="KO"
    local ok_corr="KO"

    if fiche_a_regle_relecture "$fiche"; then
        ok_fiche="OK"
    fi
    if corrections_a_regle_relecture "$corrections"; then
        ok_corr="OK"
    fi

    if [ "$ok_fiche" = "OK" ] && [ "$ok_corr" = "OK" ]; then
        echo -e "${GREEN}[OK]${NC} $agent : fiche + corrections"
        if [ "$verbose" = "true" ]; then
            local ligne_f=$(ligne_regle "$fiche")
            local ligne_c=$(ligne_regle "$corrections")
            echo -e "      fiche: ligne $ligne_f | corrections: ligne $ligne_c"
        fi
        return 0
    else
        echo -e "${RED}[MANQUE]${NC} $agent : fiche=$ok_fiche corrections=$ok_corr"
        if [ "$verbose" = "true" ]; then
            [ "$ok_fiche" = "KO" ] && echo -e "      fiche: regle de relecture absente"
            [ "$ok_corr" = "KO" ] && echo -e "      corrections: regle de relecture absente"
        fi
        return 1
    fi
}

# Fonction principale
executer() {
    local agent_filtre="$1"
    local verbose="$2"

    echo -e "${BLUE}=== valider-relecture ===${NC}"
    if [ -n "$agent_filtre" ]; then
        echo "Agent : $agent_filtre"
    else
        echo "Agents : tous (dossier agents/)"
    fi
    echo ""

    local total=0
    local conformes=0

    if [ -n "$agent_filtre" ]; then
        # Verifier un seul agent
        total=1
        if verifier_agent "$agent_filtre" "$verbose"; then
            conformes=1
        fi
    else
        # Parcourir les dossiers d'agents (exclure tools/, templates, index)
        for dir in cerveau-projet/agents/*/; do
            [ -d "$dir" ] || continue
            local agent_name=$(basename "$dir")
            [[ "$agent_name" == "tools" ]] && continue
            total=$((total + 1))
            if verifier_agent "$agent_name" "$verbose"; then
                conformes=$((conformes + 1))
            fi
        done
    fi

    echo ""
    echo -e "${BLUE}=== Resume ===${NC}"
    echo -e "Agents verifies : ${total}"
    echo -e "Conformes : ${conformes}"

    if [ "$conformes" -eq "$total" ]; then
        echo ""
        echo -e "${GREEN}[OK] Tous les agents portent la regle de relecture${NC}"
        exit 0
    else
        echo ""
        echo -e "${RED}[ERREUR] $((total - conformes)) agent(s) sans regle de relecture complete${NC}"
        exit 1
    fi
}

# Main
main() {
    local agent_filtre=""
    local verbose="false"
    local help="false"

    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --agent)
                agent_filtre="$2"
                shift 2
                ;;
            --verbose)
                verbose="true"
                shift
                ;;
            --help)
                help="true"
                shift
                ;;
            *)
                echo -e "${RED}[ERREUR] Option inconnue : $1${NC}"
                afficher_aide
                exit 1
                ;;
        esac
    done

    # Afficher l'aide
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi

    # Executer
    executer "$agent_filtre" "$verbose"
}

# Verifier le nommage au demarrage (regle immuable)
verifier_nommage

# Executer
main "$@"
