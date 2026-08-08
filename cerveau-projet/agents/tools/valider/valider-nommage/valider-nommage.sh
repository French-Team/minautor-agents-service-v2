#!/bin/bash
# valider-nommage.sh
# Verifier que le nommage est correct selon les conventions
# Version: 0.3.0
# Date: 2026-08-08
# Auteur: Vulcain
#
# Mode --mots-seuls : applique la REGLE FONDAMENTALE "aucun mot seul"
# (convention-renommage.md) : tout identifiant = 2+ mots. Detecte les
# IDENTIFIANTS generiques a un seul mot (nom, role, statut, id, date,
# cible...) dans les blocs YAML (agent:, profil:, identite:) et les objets
# JSON identite/agent/profil.

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.3.0"
DATE="2026-08-08"

# Couleurs pour la sortie
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Identifiants generiques INTERDITS a un seul mot (le coeur de la regle)
MOTS_SEULS_INTERDITS="nom role statut id date cible titre description theme type_controle derniere mise"

# Cles autorisees (exceptions structurelles + cles de schema de fiche)
CLES_AUTORISEES="type commun tags appartient_a version cree specialites forces faiblesses config commandes outils parcours corrections fiche profil identite session agent raison mission"

# Dossiers de TRACES HISTORISEES ignores en mode recursif
DOSSIERS_TRACES="controles rapports retro-actions historique exemples"

# Fichiers de TRACES DOCUMENTAIRES assumees (notes d'exemple YAML historiques)
FICHIERS_TRACES="mission-condenseur.md"

# Blocs d'identification a verifier
BLOCS_IDENTIFICATION="identite agent profil session"

# Fonction d'aide
aide() {
    echo "=========================================="
    echo "  valider-nommage v${VERSION}"
    echo "  Verifier le nommage selon les conventions"
    echo "=========================================="
    echo ""
    echo "Usage: valider-nommage [OPTIONS] CHEMIN"
    echo ""
    echo "Options:"
    echo "  --aide, -h          Afficher cette aide"
    echo "  --verbose, -v       Afficher les details"
    echo "  --version           Afficher la version"
    echo "  --type TYPE         Type de fichier (protocole, convention, agent, outil)"
    echo "  --recursive, -r     Valider tous les outils d'un dossier (ignore --type)"
    echo "  --mots-seuls        Regle fondamentale 'aucun mot seul' (YAML/JSON)"
    echo ""
    echo "Types de fichiers:"
    echo "  protocole     nom-protocole.XX.XX.statut.md"
    echo "  agent         nom-agent.md"
    echo "  outil         nom-outil.sh, nom-outil.py ou nom-outil.md"
    echo "  convention    convention-nom.md"
    echo ""
    echo "Statuts valides (protocoles):"
    echo "  ebauche, prepare, dev, test, valide"
    echo ""
    echo "Mode --mots-seuls:"
    echo "  Applique la REGLE FONDAMENTALE : tout identifiant = 2+ mots."
    echo "  Detecte les IDENTIFIANTS generiques a un seul mot (nom, role, statut,"
    echo "  id, date, cible...) dans les blocs YAML (agent:, profil:, identite:) et"
    echo "  les objets JSON identite/agent/profil."
    echo "  Autorises : exceptions structurelles (type, commun, tags, appartient_a)"
    echo "  et cles de schema de fiche (version, cree, specialites, forces...)."
    echo "  En recursif : dossiers de traces ignores (controles, rapports,"
    echo "  retro-actions, historique, exemples)."
    echo ""
    echo "Exemples:"
    echo "  valider-nommage --type protocole chemin/vers/protocole.md"
    echo "  valider-nommage --type agent chemin/vers/agent.md"
    echo "  valider-nommage --recursive cerveau-projet/agents/tools/"
    echo "  valider-nommage --mots-seuls cerveau-projet/agents/cerberus/cerberus.md"
    echo "  valider-nommage --mots-seuls --recursive cerveau-projet/agents/"
    echo ""
}

# Verifier si une cle est un identifiant generique interdit
est_mot_seul_interdit() {
    local cle=$1
    # Non compose (pas de - ni _) ?
    if [[ "$cle" =~ ^[a-z]+$ ]]; then
        # Autorisee ?
        if [[ " $CLES_AUTORISEES " == *" $cle "* ]]; then
            return 1
        fi
        # Interdite ?
        if [[ " $MOTS_SEULS_INTERDITS " == *" $cle "* ]]; then
            return 0
        fi
    fi
    return 1
}

# Analyser les blocs YAML d'un fichier .md/.py/.sh
# Renvoie le nombre de mots seuls interdits detectes via stdout (ligne:cle)
verifier_yaml() {
    local fichier=$1
    local num=0
    local bloc=""
    local mots=""
    while IFS= read -r ligne || [[ -n "$ligne" ]]; do
        num=$((num + 1))
        # Frontmatter commente (.py/.sh) : '# identite:' racine (1 espace)
        if [[ "$ligne" =~ ^\#[[:space:]]+[a-zA-Z0-9_-]+:[[:space:]]*$ || "$ligne" =~ ^\#[[:space:]]+[a-zA-Z0-9_-]+:[[:space:]]+ ]]; then
            if [[ "$ligne" =~ ^\#[[:space:]]+([a-zA-Z0-9_-]+): ]]; then
                local racine="${BASH_REMATCH[1]}"
                # S'il s'agit d'une sous-cle (3 espaces), c'est une sous-cle
                if [[ "$ligne" =~ ^\#[[:space:]]{3} ]]; then
                    local cle3=$(echo "$ligne" | sed 's/^#[[:space:]]*//' | cut -d: -f1)
                    if [[ -n "$bloc" ]] && est_mot_seul_interdit "$cle3"; then
                        mots="$mots $fichier:$num:$cle3"
                    fi
                else
                    if [[ " $BLOCS_IDENTIFICATION " == *" $racine "* ]]; then
                        bloc="$racine"
                    else
                        bloc=""
                    fi
                fi
            fi
            continue
        fi
        # Bloc YAML indentee de 2 espaces : '  cle: valeur'
        if [[ "$ligne" =~ ^[[:space:]]{2}([a-zA-Z0-9_-]+): ]]; then
            local cle2="${BASH_REMATCH[1]}"
            if [[ -n "$bloc" ]] && est_mot_seul_interdit "$cle2"; then
                mots="$mots $fichier:$num:$cle2"
            fi
            continue
        fi
        # Ligne racine YAML non indentee : 'agent:', 'profil:', ...
        if [[ "$ligne" =~ ^([a-zA-Z0-9_-]+): ]]; then
            local racine2="${BASH_REMATCH[1]}"
            if [[ " $BLOCS_IDENTIFICATION " == *" $racine2 "* ]]; then
                bloc="$racine2"
            else
                bloc=""
            fi
            continue
        fi
    done < "$fichier"
    echo "$mots"
}

# Analyser un fichier JSON : cles des objets identite/agent/profil
verifier_json() {
    local fichier=$1
    local mots=""
    # Extraction simple des blocs identite/agent/profil
    python3 - "$fichier" <<'PYEOF'
import io, json, re, sys
fichier = sys.argv[1]
try:
    with io.open(fichier, encoding="utf-8", errors="replace") as fh:
        data = json.loads(fh.read())
except Exception as e:
    print("JSON invalide: %s" % e)
    sys.exit(0)
BLOCS = ("identite", "agent", "profil", "session")
AUTORISEES = set("type commun tags appartient_a version cree specialites forces faiblesses config commandes outils parcours corrections fiche profil identite session agent raison mission".split())
INTERDITS = set("nom role statut id date cible titre description theme type_controle derniere mise".split())
PAT = re.compile(r"^[a-z]+$")
def check(obj, chemin):
    if isinstance(obj, dict):
        for cle, valeur in obj.items():
            if cle in BLOCS and isinstance(valeur, dict):
                for scle in valeur.keys():
                    if PAT.match(scle) and scle not in AUTORISEES and scle in INTERDITS:
                        print("%s:%s:%s" % (fichier, chemin + cle, scle))
            else:
                check(valeur, chemin + cle + "/")
check(data, "")
PYEOF
}

# Fonction pour valider le nommage d'un protocole
valider_protocole() {
    local fichier=$1
    local verbose=$2
    local erreurs=0

    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    # Extraire les parties du nom
    local nom_part=$(echo "$basename" | cut -d'.' -f1)
    local major_part=$(echo "$basename" | cut -d'.' -f2)
    local minor_part=$(echo "$basename" | cut -d'.' -f3)
    local statut_part=$(echo "$basename" | cut -d'.' -f4)

    # Verifier que les parties existent
    if [[ -z "$nom_part" || -z "$major_part" || -z "$minor_part" || -z "$statut_part" ]]; then
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : nom-protocole.XX.XX.statut.md"
        return 1
    fi

    # Verifier que major et minor sont des nombres
    if ! [[ "$major_part" =~ ^[0-9]+$ ]] || ! [[ "$minor_part" =~ ^[0-9]+$ ]]; then
        echo -e "  ${RED}[ERREUR] Version invalide : ${major_part}.${minor_part}${NC}"
        echo -e "    Les versions doivent etre des nombres"
        return 1
    fi

    # Verifier que le statut est valide
    case "$statut_part" in
        ebauche|prepare|dev|test|valide)
            echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"

            if [[ "$verbose" == "true" ]]; then
                echo -e "    Nom : ${nom_part}"
                echo -e "    Version : ${major_part}.${minor_part}"
                echo -e "    Statut : ${statut_part}"
            fi
            return 0
            ;;
        *)
            echo -e "  ${RED}[ERREUR] Statut invalide : ${statut_part}${NC}"
            echo -e "    Statuts valides : ebauche, prepare, dev, test, valide"
            return 1
            ;;
    esac
}

# Fonction pour valider le nommage d'un agent
valider_agent() {
    local fichier=$1
    local verbose=$2

    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    if [[ "$basename" =~ ^[a-z]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
        return 0
    else
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : nom-agent.md"
        return 1
    fi
}

# Fonction pour valider le nommage d'un outil
valider_outil() {
    local fichier=$1
    local verbose=$2
    local categorie=$3

    local basename=$(basename "$fichier")
    local erreurs=0

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    if [[ "$basename" =~ ^[a-z-]+\.sh$ ]] || [[ "$basename" =~ ^[a-z-]+\.py$ ]] || [[ "$basename" =~ ^[a-z-]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
    else
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : nom-outil.sh, nom-outil.py ou nom-outil.md"
        erreurs=$((erreurs + 1))
    fi

    local nom=$(echo "$basename" | sed 's/\.sh$//; s/\.py$//; s/\.md$//')

    if [[ -z "$categorie" ]]; then
        local dossier_outil=$(dirname "$fichier")
        categorie=$(basename "$(dirname "$dossier_outil")")
    fi

    if [[ "$nom" == "${categorie}-"* ]] || [[ "$nom" == "$categorie" ]]; then
        if [[ "$verbose" == "true" ]]; then
            echo -e "  ${GREEN}[OK] Prefixe dossier respecte : ${categorie}/${NC}"
        fi
    else
        echo -e "  ${RED}[ERREUR] Prefixe dossier manquant : ${basename}${NC}"
        echo -e "    Le nom doit commencer par '${categorie}-' (dossier: ${categorie}/)"
        erreurs=$((erreurs + 1))
    fi

    return $erreurs
}

# Fonction pour valider le nommage d'une convention
valider_convention() {
    local fichier=$1
    local verbose=$2

    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Validation du nommage : ${basename}${NC}"
    echo ""

    if [[ "$basename" =~ ^convention-[a-z-]+\.md$ ]]; then
        echo -e "  ${GREEN}[OK] Format valide : ${basename}${NC}"
        return 0
    else
        echo -e "  ${RED}[ERREUR] Format invalide : ${basename}${NC}"
        echo -e "    Attendu : convention-nom.md"
        return 1
    fi
}

# Mode --mots-seuls sur un fichier
verifier_mots_seuls_fichier() {
    local fichier=$1
    local basename=$(basename "$fichier")

    echo -e "${BLUE}[CHECKLIST] Regle fondamentale 'aucun mot seul' : ${basename}${NC}"
    echo ""

    if [[ ! -f "$fichier" ]]; then
        echo -e "  ${RED}[ERREUR] Le fichier '${fichier}' n'existe pas${NC}"
        return 1
    fi

    local resultat=""
    case "$fichier" in
        *.md|*.py|*.sh)
            resultat=$(verifier_yaml "$fichier")
            ;;
        *.json)
            resultat=$(verifier_json "$fichier")
            ;;
        *)
            echo -e "  ${RED}[ERREUR] Extension non analysee (md, json, py ou sh requis)${NC}"
            return 1
            ;;
    esac

    if [[ -n "$resultat" ]]; then
        local total=0
        for item in $resultat; do
            local chemin=$(echo "$item" | cut -d: -f1-2)
            local cle=$(echo "$item" | cut -d: -f3)
            echo -e "  ${RED}[ERREUR] ${chemin} : cle '${cle}' = IDENTIFIANT MOT SEUL (regle fondamentale : 2+ mots)${NC}"
            total=$((total + 1))
        done
        echo ""
        echo "  Total : ${total} identifiant(s) mot(s) seul(s) detecte(s)"
        return $total
    fi
    echo -e "  ${GREEN}[OK] Aucun mot seul detecte${NC}"
    return 0
}

# Mode --mots-seuls recursif
verifier_mots_seuls_recursif() {
    local dossier=$1
    if [[ ! -d "$dossier" ]]; then
        echo "Erreur: '$dossier' n'est pas un dossier"
        return 1
    fi

    local total=0
    local ko=0
    echo -e "${BLUE}=== Regle fondamentale 'aucun mot seul' (recursif) : ${dossier} ===${NC}"
    echo ""

    while IFS= read -r f; do
        [[ -f "$f" ]] || continue
        local basename=$(basename "$f")
        # Ignorer les traces documentaires assumees
        [[ " $FICHIERS_TRACES " == *" $basename "* ]] && continue
        total=$((total + 1))
        verifier_mots_seuls_fichier "$f"
        local code=$?
        [[ $code -ne 0 ]] && ko=$((ko + 1))
        echo ""
    done < <(find "$dossier" -type f \( -name "*.md" -o -name "*.json" \) | grep -vE "/(controles|rapports|retro-actions|historique|exemples)/" | sort)

    echo -e "${BLUE}=== Resume ===${NC}"
    echo "  Fichiers analyses : ${total}"
    [[ $ko -gt 0 ]] && echo -e "  ${RED}Fichiers avec mots seuls : ${ko}${NC}" || echo "  Fichiers avec mots seuls : 0"
    return $ko
}

# Valeurs par defaut
VERBOSE="false"
TYPE=""
FICHIER=""
RECURSIVE="false"
MOTS_SEULS="false"

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --aide|-h)
            aide
            exit 0
            ;;
        --verbose|-v)
            VERBOSE="true"
            shift
            ;;
        --version)
            echo "valider-nommage v${VERSION}"
            exit 0
            ;;
        --type)
            TYPE="$2"
            shift 2
            ;;
        --recursive|-r)
            RECURSIVE="true"
            shift
            ;;
        --mots-seuls)
            MOTS_SEULS="true"
            shift
            ;;
        -*)
            echo "Option inconnue: $1"
            echo "Utilisez --aide pour l'aide"
            exit 1
            ;;
        *)
            FICHIER="$1"
            shift
            ;;
    esac
done

# Mode --mots-seuls (prioritaire)
if [[ "$MOTS_SEULS" == "true" ]]; then
    if [[ -z "$FICHIER" ]]; then
        echo "Erreur: Aucun fichier ou dossier specifie pour --mots-seuls"
        exit 1
    fi
    if [[ "$RECURSIVE" == "true" ]]; then
        verifier_mots_seuls_recursif "$FICHIER"
        exit $?
    fi
    verifier_mots_seuls_fichier "$FICHIER"
    exit $?
fi

# Mode recursive : valider tous les outils d'un dossier
if [[ "$RECURSIVE" == "true" ]]; then
    if [[ -z "$FICHIER" ]]; then
        echo "Erreur: Aucun dossier specifie pour --recursive"
        exit 1
    fi
    if [[ ! -d "$FICHIER" ]]; then
        echo "Erreur: '$FICHIER' n'est pas un dossier"
        exit 1
    fi
    echo -e "${BLUE}=== Validation recursive des outils dans : ${FICHIER} ===${NC}"
    echo ""
    total=0
    ok=0
    ko=0
    while IFS= read -r dossier_outil; do
        categorie=$(basename "$(dirname "$dossier_outil")")
        nom_outil=$(basename "$dossier_outil")
        for f in "$dossier_outil"/*.sh; do
            [[ ! -f "$f" ]] && continue
            total=$((total + 1))
            valider_outil "$f" "$VERBOSE" "$categorie"
            [[ $? -eq 0 ]] && ok=$((ok + 1)) || ko=$((ko + 1))
            echo ""
        done
        for f in "$dossier_outil"/*.md; do
            [[ ! -f "$f" ]] && continue
            total=$((total + 1))
            valider_outil "$f" "$VERBOSE" "$categorie"
            [[ $? -eq 0 ]] && ok=$((ok + 1)) || ko=$((ko + 1))
            echo ""
        done
        for f in "$dossier_outil"/*.py; do
            [[ ! -f "$f" ]] && continue
            total=$((total + 1))
            valider_outil "$f" "$VERBOSE" "$categorie"
            [[ $? -eq 0 ]] && ok=$((ok + 1)) || ko=$((ko + 1))
            echo ""
        done
    done < <(find "$FICHIER" -mindepth 2 -maxdepth 2 -type d 2>/dev/null | sort)
    echo -e "${BLUE}=== Resume ===${NC}"
    echo -e "  Total : ${total}"
    echo -e "  ${GREEN}OK : ${ok}${NC}"
    [[ $ko -gt 0 ]] && echo -e "  ${RED}Erreurs : ${ko}${NC}" || echo -e "  Erreurs : 0"
    exit $ko
fi

# Verification du fichier
if [[ -z "$FICHIER" ]]; then
    echo "Erreur: Aucun fichier specifie"
    echo "Utilisez --aide pour l'aide"
    exit 1
fi

if [[ ! -f "$FICHIER" ]]; then
    echo "Erreur: Le fichier '$FICHIER' n'existe pas"
    exit 1
fi

# Verifier le type
if [[ -z "$TYPE" ]]; then
    echo "Erreur: Type non specifie"
    echo "Utilisez --type pour specifier le type"
    exit 1
fi

# Execution selon le type
case $TYPE in
    protocole)
        valider_protocole "$FICHIER" "$VERBOSE"
        ;;
    agent)
        valider_agent "$FICHIER" "$VERBOSE"
        ;;
    outil)
        valider_outil "$FICHIER" "$VERBOSE"
        ;;
    convention)
        valider_convention "$FICHIER" "$VERBOSE"
        ;;
    *)
        echo "Erreur: Type inconnu '$TYPE'"
        echo "Types disponibles : protocole, agent, outil, convention"
        exit 1
        ;;
esac

exit $?
