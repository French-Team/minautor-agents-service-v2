#!/bin/bash
# mettre-a-jour-readme.sh
# Outil pour corriger le README afin qu'il reflete l'etat reel du projet
# Version : 0.4.8
# Statut : prepare
# Proprietaire : Clio (agent dedie au README)

# Configuration
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.4.8"
STATUT="prepare"
README="README.md"
README_DEV="cerveau-projet/readme-dev.md"
HISTORIQUE="AGENTS-historique.md"
AGENTS_DIR="cerveau-projet/agents"
TOOLS_DIR="cerveau-projet/agents/tools"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== mettre-a-jour-readme v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options :"
    echo "  --verifier         Comparer l'etat reel au README, lister les ecarts (sans modifier)"
    echo "  --dry-run          Preview AVANT/APRES sans ecrire (obligatoire avant --maj)"
    echo "  --maj              Corriger le texte du README (agents, outils, compteurs)"
    echo "  --journal [N]      Consulter les N dernieres interventions (diagnostic, non inscrit au README)"
    echo "  --logo CHEMIN      Inserer une image (logo) en tete du README, apres le titre H1"
    echo "  --badges SPEC      Inserer des badges statiques Shields (label=message:couleur;...), apres le titre H1"
    echo "  --agents           Afficher le compte reel des agents"
    echo "  --outils           Afficher le compte reel des outils par categorie"
    echo "  --help             Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 --verifier                    # Apercu des ecarts"
    echo "  $0 --dry-run                     # Preview AVANT/APRES"
    echo "  $0 --maj                         # Corriger le README"
    echo "  $0 --journal 5                   # 5 dernieres interventions"
    echo "  $0 --logo cerveau-projet/assets/images/logo.jpg   # Inserer un logo en tete"
    echo "  $0 --badges \"Plateforme=Windows:blue;Statut=stable:brightgreen\"   # Inserer des badges"
    echo ""
}

# Compter les agents reels (dossiers dans agents/, hors tools)
compter_agents() {
    local nb=0
    for d in "$AGENTS_DIR"/*/; do
        [ -d "$d" ] || continue
        local nom=$(basename "$d")
        [ "$nom" != "tools" ] || continue
        # Un agent d action a un arbre v2 : agents/<nom>/parcours/arbre-<nom>.json
        # (migration v1->v2 : les parcours v1 sont retires)
        [ -f "$AGENTS_DIR/$nom/parcours/arbre-$nom.json" ] || continue
        nb=$((nb + 1))
    done
    echo "$nb"
}

# Lister les agents reels (noms des dossiers)
lister_agents_reels() {
    for d in "$AGENTS_DIR"/*/; do
        [ -d "$d" ] || continue
        local nom=$(basename "$d")
        [ "$nom" != "tools" ] || continue
        # Un agent d action a un arbre v2 : agents/<nom>/parcours/arbre-<nom>.json
        # (migration v1->v2 : les parcours v1 sont retires)
        [ -f "$AGENTS_DIR/$nom/parcours/arbre-$nom.json" ] || continue
        echo "$nom"
    done
}

# Lire le role specifique d'un agent depuis sa fiche
lire_role_agent() {
    local agent="$1"
    local fiche="$AGENTS_DIR/$agent/$agent.md"
    if [ -f "$fiche" ]; then
        grep -E '^[[:space:]]*role_specifique:' "$fiche" | head -1 \
            | sed 's/^[[:space:]]*role_specifique:[[:space:]]*//' \
            | tr -d '"' | tr -d "'" | tr -d '\r'
    fi
}

# Nom de categorie affichable (capitalise + 'Mettre a jour')
# Implementation 100% bash (pas de sous-processus : lent sur Windows/msys)
nom_categorie_affichable() {
    local cle="$1"
    local cat="${cle^}"
    echo "${cat//Mettre-a-jour/Mettre a jour}"
}

# Lister les outils reels d'une categorie (noms des sous-dossiers, separes par ', ')
lister_outils_categorie() {
    local categorie="$1"
    local dir="$TOOLS_DIR/$categorie"
    local liste=""
    local first=""
    local d nom
    # Cas special templates
    if [ "$categorie" = "templates" ]; then
        [ -f "$TOOLS_DIR/outil-template.md" ] && echo "outil-template"
        return
    fi
    if [ ! -d "$dir" ]; then
        echo ""
        return
    fi
    # v0.4.7 : un dossier technique (__pycache__) n'est pas un outil
    # (filtre en bash pur, pas de sous-processus par dossier)
    if [ "$categorie" = "tester" ]; then
        for d in "$dir/protections"/*/; do
            [ -d "$d" ] || continue
            nom=${d%/}; nom=${nom##*/}
            case "$nom" in __*) continue ;; esac
            if [ -z "$first" ]; then
                liste="$nom"
                first="1"
            else
                liste="${liste}, ${nom}"
            fi
        done
        echo "$liste"
        return
    fi
    for d in "$dir"/*/; do
        [ -d "$d" ] || continue
        nom=${d%/}; nom=${nom##*/}
        case "$nom" in __*) continue ;; esac
        if [ -z "$first" ]; then
            liste="$nom"
            first="1"
        else
            liste="${liste}, ${nom}"
        fi
    done
    echo "$liste"
}

# Lister les categories d'outils (chaque sous-dossier, plus combos et templates)
lister_categories() {
    local d nom
    for d in "$TOOLS_DIR"/*/; do
        [ -d "$d" ] || continue
        nom=${d%/}; nom=${nom##*/}
        case "$nom" in
            combos) continue ;;
            __*) continue ;;
        esac
        echo "$nom"
    done
    # Categories speciales
    echo "combos"
    echo "templates"
}

# Cache des compteurs : les categories et leurs comptes sont calcules UNE
# SEULE fois par invocation (les sous-processus coutent ~0.4 s chacun sur
# Windows/msys : boucler sur $(compter_outils_categorie ...) ruinerait le temps).
# CATS_TOTAL : total des outils. CATS_CNT : cle -> compte. CATS_SPEC : lignes
# 'Nom|compte' des categories actives (compte > 0), dans l ordre reel.
declare -A CATS_CNT
CATS_TOTAL=""
CATS_SPEC=""

_remplir_cache() {
    [ -n "$CATS_TOTAL" ] && return
    local d nom cle nb total=0 spec=""
    # Categories reelles : sous-dossiers de tools/ (hors combos et '__'),
    # puis combos et templates (meme ordre que lister_categories).
    for d in "$TOOLS_DIR"/*/; do
        [ -d "$d" ] || continue
        nom=${d%/}; nom=${nom##*/}
        case "$nom" in combos|__*) continue ;; esac
        cle="$nom"
        nb=0
        for sd in "$d"/*/; do
            [ -d "$sd" ] || continue
            case "${sd%/}" in *"/__"*) continue ;; esac
            nb=$((nb + 1))
        done
        [ "$cle" = "tester" ] && nb=$(compter_outils_categorie "tester")
        CATS_CNT["$cle"]=$nb
        total=$((total + nb))
        if [ "$nb" -gt 0 ]; then
            spec="${spec}$(nom_categorie_affichable "$cle")|${nb}\n"
        fi
    done
    # combos (sous-dossiers reels) et templates (fichier outil-template.md)
    nb=0
    for sd in "$TOOLS_DIR/combos"/*/; do [ -d "$sd" ] || continue; nb=$((nb + 1)); done
    CATS_CNT["combos"]=$nb; total=$((total + nb))
    if [ "$nb" -gt 0 ]; then spec="${spec}Combos|${nb}\n"; fi
    nb=0
    [ -f "$TOOLS_DIR/outil-template.md" ] && nb=1
    CATS_CNT["templates"]=$nb; total=$((total + nb))
    if [ "$nb" -gt 0 ]; then spec="${spec}Templates|${nb}\n"; fi
    CATS_TOTAL=$total
    CATS_SPEC="$spec"
}

# Total des outils (calcule une seule fois par invocation)
compter_total_outils() {
    _remplir_cache
    echo "$CATS_TOTAL"
}

# Compte d'une categorie (via le cache quand il est rempli)
compter_outils_categorie() {
    if [ -n "$CATS_TOTAL" ]; then
        echo "${CATS_CNT[$1]:-0}"
        return
    fi
    compter_outils_categorie_reel "$1"
}

# Compte reel d'une categorie (sans cache) : boucle bash pur, aucun
# sous-processus par dossier.
compter_outils_categorie_reel() {
    local categorie="$1"
    local dir="$TOOLS_DIR/$categorie"
    local nb=0
    local d nom
    if [ "$categorie" = "templates" ]; then
        [ -f "$TOOLS_DIR/outil-template.md" ] && nb=1
        echo "$nb"
        return
    fi
    if [ ! -d "$dir" ]; then
        echo 0
        return
    fi
    if [ "$categorie" = "tester" ]; then
        for d in "$dir/protections"/*/; do
            [ -d "$d" ] || continue
            nom=${d%/}; nom=${nom##*/}
            case "$nom" in __*) continue ;; esac
            nb=$((nb + 1))
        done
        echo "$nb"
        return
    fi
    for d in "$dir"/*/; do
        [ -d "$d" ] || continue
        nom=${d%/}; nom=${nom##*/}
        case "$nom" in __*) continue ;; esac
        nb=$((nb + 1))
    done
    echo "$nb"
}

# Lire les N dernieres interventions de l'historique (diagnostic uniquement)
lire_journal() {
    local n="${1:-10}"
    # v0.4.3 : les entrees commencent par '| <span' (agent colore en
    # 1re colonne, format v0.5.15 de l historique)
    grep '^| <span' "$HISTORIQUE" 2>/dev/null | head -n "$n"
}

# Extraire la region de la table 'Mes agents' du README public (v0.4.8) :
# du titre '## Mes agents' jusqu'au titre suivant (### ou ##). La presence
# des agents se verifie dans cette table uniquement -- avant, la recherche
# globale laissait une mention narrative ('**Oracle**') ou des lignes
# orphelines masquer des agents absents de la table.
extraire_region_agents() {
    awk '
        /^## Mes agents/ { f = 1; print; next }
        f && /^(###|##) / { exit }
        f { print }
    ' "$README"
}

# Verifier la SOMME des compteurs du tableau readme-dev (section 6)
# = le total reel. Retourne 0 si coherent.
# Boucle en bash pur (un seul awk de prefiltre ; pas de sous-processus par
# ligne : tres lent sur Windows/msys).
verifier_somme_comptes() {
    if [ ! -f "$README_DEV" ]; then
        echo -e "  ${RED}[MANQUANT]${NC} readme-dev introuvable : $README_DEV"
        return 1
    fi
    _remplir_cache
    local total="$CATS_TOTAL"
    local somme=0 nb_lignes=0 ecarts=0
    local nom nb cle reel
    while IFS='|' read -r _ nom nb _; do
        # Nettoyer espaces de bord en bash pur
        while [ "$nom" != "${nom# }" ]; do nom="${nom# }"; done
        while [ "$nom" != "${nom% }" ]; do nom="${nom% }"; done
        [ "$nom" = "Categorie" ] && continue
        nb="${nb//[!0-9]/}"
        [ -z "$nb" ] && continue
        # cle : minuscules + espaces -> tirets (compte lu dans le cache)
        cle="${nom,,}"
        cle="${cle// /-}"
        reel="${CATS_CNT[$cle]:-0}"
        somme=$((somme + nb))
        nb_lignes=$((nb_lignes + 1))
        if [ "$reel" != "$nb" ]; then
            echo -e "  ${RED}[ECART]${NC} ${nom} : tableau dit ${nb}, reel = ${reel}"
            ecarts=$((ecarts + 1))
        fi
    done < <(awk '/^\| [A-Za-z][^|]* \| [0-9]+ \|/ { print }' "$README_DEV")
    if [ "$somme" != "$total" ]; then
        echo -e "  ${RED}[ECART SOMME]${NC} readme-dev tableau : somme = ${somme}, total reel = ${total}"
        ecarts=$((ecarts + 1))
    fi
    if [ "$ecarts" -eq 0 ]; then
        echo -e "  ${GREEN}[OK]${NC} readme-dev tableau : ${nb_lignes} categories, somme ${somme} = total reel ${total}"
    fi
    return "$ecarts"
}

# Verifier l'etat reel et comparer avec le README
verifier() {
    echo "=== ETAT REEL DU PROJET ==="
    echo ""
    echo "Agents reels : $(compter_agents)"
    echo ""
    echo "Outils par categorie :"
    local total=0
    local cat nb
    for cat in $(lister_categories); do
        nb=$(compter_outils_categorie "$cat")
        printf "  %-14s : %s\n" "$cat" "$nb"
        total=$((total + nb))
    done
    echo "  TOTAL         : ${total}"
    echo ""
    echo "=== ECARTS AVEC LE README ==="
    echo ""

    # Agents manquants dans la table 'Mes agents' du README public
    # (v0.4.8 : presence dans la table uniquement, pas dans tout le fichier)
    local ecart=0
    local agent region_agents
    region_agents=$(extraire_region_agents)
    for agent in $(lister_agents_reels); do
        case "$region_agents" in
            *"| **${agent^}** |"*) ;;
            *)
                echo -e "  ${RED}[MANQUANT]${NC} Agent '${agent}' absent de la table 'Mes agents'"
                ecart=$((ecart + 1))
                ;;
        esac
    done
    if [ "$ecart" -eq 0 ]; then
        echo -e "  ${GREEN}[OK]${NC} Tous les agents sont dans la table 'Mes agents'"
    fi

    # Badge Outils du README public (nouvelle norme 1ere personne 20/08) :
    # la liste technique exhaustive vit dans readme-dev (section 6), pas dans
    # le README public. Le verifier tolere l absence de la section 'La boite
    # a outils' (ancien format) et s appuie sur readme-dev pour les compteurs.
    local badge=$(grep -o 'Outils-[0-9]*' "$README" | head -1 | grep -o '[0-9]*')
    if [ -n "$badge" ] && [ "$badge" != "$total" ]; then
        echo -e "  ${RED}[OBSOLETE]${NC} Badge Outils-$badge -> devrait etre $total"
    elif [ -n "$badge" ]; then
        echo -e "  ${GREEN}[OK]${NC} Badge Outils-$badge (README public)"
    fi
    # Badge Agents du README public (v0.4.6)
    local badge_agents=$(grep -o 'Agents-[0-9]*' "$README" | head -1 | grep -o '[0-9]*')
    local reel_agents=$(compter_agents)
    if [ -n "$badge_agents" ] && [ "$badge_agents" != "$reel_agents" ]; then
        echo -e "  ${RED}[OBSOLETE]${NC} Badge Agents-$badge_agents -> devrait etre $reel_agents"
    elif [ -n "$badge_agents" ]; then
        echo -e "  ${GREEN}[OK]${NC} Badge Agents-$badge_agents (README public)"
    fi
    if grep -q '^## La boite a outils ([0-9]* outils)' "$README"; then
        echo -e "  ${YELLOW}[INFO]${NC} Section 'La boite a outils' encore presente (ancien format) : compteurs verifies ci-dessous"
    else
        echo -e "  ${YELLOW}[INFO]${NC} README public sans section 'La boite a outils' (nouvelle norme) : compteurs verifies dans readme-dev (section 6)"
    fi

    # Compteurs et outils par categorie : uniquement si l ancienne section
    # existe encore dans le README public (retro-compatibilite).
    if grep -q '^## La boite a outils ([0-9]* outils)' "$README"; then
    for cle in $(lister_categories); do
        local cat=$(nom_categorie_affichable "$cle")
        local nb=$(compter_outils_categorie "$cle")
        local lue=$(grep -o "\*\*${cat} ([0-9]*)\*\*" "$README" | grep -o '[0-9]*' | head -1)
        if [ -n "$lue" ] && [ "$lue" != "$nb" ]; then
            echo -e "  ${RED}[OBSOLETE]${NC} ${cat} : README dit ${lue}, reel = ${nb}"
        else
            echo -e "  ${GREEN}[OK]${NC} ${cat} : ${nb}"
        fi
        # Outils manquants dans la liste de la categorie
        local liste_reelle=$(lister_outils_categorie "$cle")
        local ligne_readme=$(grep -o "\*\*${cat} ([0-9]*)\*\* | [^|]*" "$README" | head -1 | sed "s/.*| //")
        for outil in $(echo "$liste_reelle" | tr ',' '\n' | sed 's/^ *//; s/ *$//'); do
            local nom=${outil##*: }
            if [ -n "$nom" ] && ! echo "$ligne_readme" | grep -q "$nom"; then
                echo -e "  ${YELLOW}[MANQUANT]${NC} ${cat} : outil '${nom}' absent de la liste"
            fi
        done
    done
    fi

    # Somme des compteurs du readme-dev (anti-recurrence bug Clio 132 vs 134)
    echo ""
    echo "=== README-DEV (tableau des categories, section 6) ==="
    verifier_somme_comptes

    echo ""
    echo "Utilisez --maj pour corriger le texte du README."
}

# Mode dry-run : montrer le AVANT/APRES sans ecrire
# Regle Clio : dry-run OBLIGATOIRE avant toute modification
dry_run() {
    local total=$(compter_total_outils)
    echo "=== DRY-RUN (preview AVANT/APRES) ==="
    echo ""
    echo "Ce qui changerait avec --maj :"
    echo ""

    local changements=()

    # 1. Titre boite a outils
    local titre_actuel=$(grep -o '^## La boite a outils ([0-9]* outils)' "$README" | grep -o '[0-9]*' | head -1)
    if [ -n "$titre_actuel" ] && [ "$titre_actuel" != "$total" ]; then
        changements+=("Titre : '${titre_actuel} outils' -> '${total} outils'")
    fi

    # 2. Compteurs par categorie : uniquement si l ancienne section
    # 'La boite a outils' existe dans le README public (retro-compatibilite).
    # Nouvelle norme : les compteurs vivent dans readme-dev (section 6).
    if grep -q '^## La boite a outils ([0-9]* outils)' "$README"; then
    for cle in $(lister_categories); do
        local cat=$(nom_categorie_affichable "$cle")
        local nb=$(compter_outils_categorie "$cle")
        local lue=$(grep -o "\*\*${cat} ([0-9]*)\*\*" "$README" | grep -o '[0-9]*' | head -1)
        if [ -n "$lue" ] && [ "$lue" != "$nb" ]; then
            changements+=("${cat} : ${lue} -> ${nb}")
        fi
    done
    fi

    # 3. Agents manquants (v0.4.8 : dans la table 'Mes agents' uniquement)
    local agents_manquants=""
    local agent region_agents
    region_agents=$(extraire_region_agents)
    for agent in $(lister_agents_reels); do
        case "$region_agents" in
            *"| **${agent^}** |"*) ;;
            *)
                local nom_affichable="${agent^}"
                if [ -z "$agents_manquants" ]; then
                    agents_manquants="$nom_affichable"
                else
                    agents_manquants="${agents_manquants}, ${nom_affichable}"
                fi
                ;;
        esac
    done
    if [ -n "$agents_manquants" ]; then
        changements+=("Agents a ajouter : ${agents_manquants}")
    fi

    # 4. Badges du header (Outils-N, Agents-N) : affichage + href
    local b_actuel b_reel
    b_actuel=$(grep -o 'badge/Outils-[0-9]*-' "$README" | head -1 | grep -o '[0-9]*')
    if [ -n "$b_actuel" ] && [ "$b_actuel" != "$total" ]; then
        changements+=("Badge Outils : ${b_actuel} -> ${total} (affichage + href)")
    fi
    b_actuel=$(grep -o 'badge/Agents-[0-9]*-' "$README" | head -1 | grep -o '[0-9]*')
    b_reel=$(compter_agents)
    if [ -n "$b_actuel" ] && [ "$b_actuel" != "$b_reel" ]; then
        changements+=("Badge Agents : ${b_actuel} -> ${b_reel} (affichage + href)")
    fi

    # 5. readme-dev : intro, synthese (les lignes du tableau sont verifiees
    # ligne a ligne par --verifier / verifier_somme_comptes)
    if [ -f "$README_DEV" ]; then
        local m_intro=$(grep -o '^\*\*[0-9]* outils dans [0-9]* categories\*\* :' "$README_DEV" | head -1)
        if [ -n "$m_intro" ]; then
            local actuel_outils=$(echo "$m_intro" | grep -o '[0-9]*' | head -1)
            local actuel_cats=$(echo "$m_intro" | grep -o '[0-9]*' | tail -1)
            local nb_cats=0 cle2
            for cle2 in $(lister_categories); do
                [ "$(compter_outils_categorie "$cle2")" -gt 0 ] && nb_cats=$((nb_cats + 1))
            done
            if [ "$actuel_outils" != "$total" ] || [ "$actuel_cats" != "$nb_cats" ]; then
                changements+=("readme-dev intro : '${actuel_outils} outils dans ${actuel_cats} categories' -> '${total} outils dans ${nb_cats} categories'")
            fi
        fi
    fi

    if [ ${#changements[@]} -eq 0 ]; then
        echo "  [AUCUN CHANGEMENT] Le README est deja a jour."
    else
        local i=1
        for chgt in "${changements[@]}"; do
            echo "  ${i}. ${chgt}"
            i=$((i + 1))
        done
    fi

    echo ""
    echo "=== FIN DRY-RUN ==="
    echo "Pour appliquer ces changements, utilisez --maj."
}

# Aligner les badges du header README (affichage + href) sur les comptes reels
# v0.4.6 : badges Outils et Agents (2 occurrences : affichage + href)
aligner_badges_header() {
    local modifie=0
    local contenu nouveau
    # Outils
    local total_outils=$(compter_total_outils)
    contenu=$(cat "$README")
    nouveau=$(printf '%s' "$contenu" | sed "s|badge/Outils-[0-9]*-|badge/Outils-${total_outils}-|g")
    if [ "$nouveau" != "$contenu" ]; then
        printf '%s' "$nouveau" > "$README"
        echo -e "  ${GREEN}[CORRIGE]${NC} Badge Outils aligne : ${total_outils} (affichage + href)."
        modifie=1
    fi
    # Agents
    local total_agents=$(compter_agents)
    contenu=$(cat "$README")
    nouveau=$(printf '%s' "$contenu" | sed "s|badge/Agents-[0-9]*-|badge/Agents-${total_agents}-|g")
    if [ "$nouveau" != "$contenu" ]; then
        printf '%s' "$nouveau" > "$README"
        echo -e "  ${GREEN}[CORRIGE]${NC} Badge Agents aligne : ${total_agents} (affichage + href)."
        modifie=1
    fi
    if [ "$modifie" -eq 0 ]; then
        echo -e "  ${GREEN}[OK]${NC} Badges du header deja a jour."
    fi
}

# Corriger readme-dev : tableau section 6 (comptes reels par categorie,
# categories obsoletes retirees, manquantes ajoutees) + ligne d'intro +
# lignes de synthese (section 1 : Agents, Outils).
# v0.4.6 : verifier SANS corriger ne suffisait pas (bug Clio 132 vs 134).
# v0.4.7 : la ligne de separation |---|---| est conservee, les exemples deja
# curates sont conserves, les lignes de synthese de la section 1 sont
# corrigees aussi.
# La cle de categorie (dossier) se deduit du nom affiche : minuscules +
# espaces -> tirets (ex : 'Mettre a jour' -> 'mettre-a-jour').
cle_depuis_nom() {
    printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g'
}

corriger_readme_dev() {
    if [ ! -f "$README_DEV" ]; then
        echo -e "  ${RED}[MANQUANT]${NC} readme-dev introuvable : $README_DEV"
        return
    fi
    # Spec : categories actives (compte > 0) dans l ordre reel, fournie par
    # le cache (calcule une seule fois par invocation).
    _remplir_cache
    local total="$CATS_TOTAL"
    local tmp="$README_DEV.tmp"
    local spec="$README_DEV.spec"
    local cle nb cat nb_cats=0
    printf '%b' "$CATS_SPEC" > "$spec"
    nb_cats=$(printf '%b' "$CATS_SPEC" | grep -c '|')

    # --- 1. Construire le fichier corrige dans $tmp (intro + tableau +
    # categories manquantes avant la ligne 'Combos' + synthese section 1).
    local nouvelle_intro="**${total} outils dans ${nb_cats} categories**"
    local syn_agents="| **Agents** | $(compter_agents) agents + classeur-variables (voir section 4) |"
    local syn_outils="| **Outils** | ${total} outils dans ${nb_cats} categories (voir section 6) |"

    # Pass 1 (awk) : lire la spec, reconstruire chaque ligne de donnees avec
    # le compte reel (exemples curates conserves), retirer les categories
    # obsoletes, corriger l intro et les lignes de synthese.
    awk -F'|' -v intro="$nouvelle_intro" -v sa="$syn_agents" -v so="$syn_outils" '
        NR == FNR {
            split($0, s, "|")
            cnt[s[1]] = s[2]
            next
        }
        {
            if ($0 ~ /^\*\*[0-9]* outils dans [0-9]* categories\*\* :/) {
                print intro " :"
                next
            }
            if (index($0, "| **Agents** |") == 1) {
                print sa
                next
            }
            if (index($0, "| **Outils** |") == 1) {
                print so
                next
            }
            if ($0 ~ /^\| [A-Za-z][^|]* \| [0-9]+ \|/) {
                name = $2
                gsub(/^ +| +$/, "", name)
                if (name in cnt) {
                    ex = $4
                    gsub(/^ +| +$/, "", ex)
                    printf "| %s | %s | %s |\n", name, cnt[name], ex
                    vu[name] = 1
                    next
                }
                next   # categorie obsolete : retiree
            }
            print
        }
    ' "$spec" "$README_DEV" > "$tmp"

    # --- 2. Categories manquantes : a ajouter avant la ligne 'Combos'
    # (toutes les categories reelles precedant combos/templates).
    # Recherche en bash pur sur le contenu deja genere (pas de grep par ligne).
    local manquantes=""
    local contenu_tmp
    contenu_tmp=$(cat "$tmp")
    while IFS= read -r cat; do
        [ -n "$cat" ] || continue
        case "$contenu_tmp" in
            *"| ${cat} |"*) ;;
            *)
                [ -z "$manquantes" ] && manquantes="${cat}" || manquantes="${manquantes}\n${cat}"
                ;;
        esac
    done < <(cut -d'|' -f1 "$spec")
    if [ -n "$manquantes" ]; then
        local bloc_manquantes=""
        while IFS= read -r cat; do
            [ -n "$cat" ] || continue
            cle=$(cle_depuis_nom "$cat")
            nb=$(awk -F'|' -v n="$cat" '$1==n{print $2}' "$spec")
            bloc_manquantes="${bloc_manquantes}| ${cat} | ${nb} | $(lister_outils_categorie "$cle") |\n"
        done <<< "$(printf '%b' "$manquantes")"
        if grep -q '^| Combos |' "$tmp"; then
            awk -v b="$(printf '%b' "$bloc_manquantes")" '
                /^\| Combos \|/ && !done { printf "%s", b; done = 1 }
                { print }
            ' "$tmp" > "$tmp.2" && mv "$tmp.2" "$tmp"
        else
            printf '%b' "$bloc_manquantes" >> "$tmp"
        fi
    fi

    # --- 3. Appliquer uniquement si le contenu change (idempotence).
    if ! diff -q "$README_DEV" "$tmp" > /dev/null 2>&1; then
        mv "$tmp" "$README_DEV"
        echo -e "  ${GREEN}[CORRIGE]${NC} Tableau readme-dev section 6 : ${nb_cats} categories (${total} outils)."
    else
        rm -f "$tmp"
        echo -e "  ${GREEN}[OK]${NC} Tableau readme-dev section 6 deja a jour (${nb_cats} categories)."
    fi
    rm -f "$spec" "$tmp.2" 2> /dev/null
}

# Corriger le README pour qu'il reflete l'etat reel
mettre_a_jour() {
    local total=$(compter_total_outils)
    echo "=== CORRECTION DU README ==="

    # 1. Titre boite a outils
    if grep -q '^## La boite a outils ([0-9]* outils)' "$README"; then
        sed -i "s/^## La boite a outils ([0-9]* outils)/## La boite a outils ($total outils)/" "$README"
        echo -e "  ${GREEN}[CORRIGE]${NC} Titre : La boite a outils ($total outils)"
    fi

    # 2. Compteurs par categorie (capitaliser les noms) : uniquement si
    # l ancienne section 'La boite a outils' existe encore (retro-compatibilite)
    local contenu_readme="$(cat "$README")"
    if grep -q '^## La boite a outils ([0-9]* outils)' "$README"; then
    for cle in $(lister_categories); do
        local cat=$(nom_categorie_affichable "$cle")
        local nb=$(compter_outils_categorie "$cle")
        case "$contenu_readme" in
            *"**${cat} ("*)
                sed -i "s/\*\*${cat} ([0-9]*)\*\*/**${cat} ($nb)**/g" "$README"
                echo -e "  ${GREEN}[CORRIGE]${NC} ${cat} : ${nb}"
                ;;
        esac
    done
    fi

    # 3. Ajouter les agents manquants dans la table 'Mes agents' (v0.4.8 :
    # presence dans la table uniquement, insertion en fin de table au format
    # 2 colonnes -- avant : recherche globale + ancre obsolete + format
    # 3 colonnes creaient des lignes orphelines en fin de fichier)
    local agents_ajoutes=0
    local agent region_agents
    region_agents=$(extraire_region_agents)
    local bloc_ajout=""
    for agent in $(lister_agents_reels); do
        case "$region_agents" in
            *"| **${agent^}** |"*) ;;
            *)
                local role=$(lire_role_agent "$agent")
                [ -z "$role" ] && role="Agent"
                # Capitaliser le nom (cerberus -> Cerberus)
                local nom_affichable="${agent^}"
                bloc_ajout="${bloc_ajout}| **${nom_affichable}** | ${role} |\n"
                echo -e "  ${GREEN}[AJOUTE]${NC} Agent '${nom_affichable}' ajoute dans la table 'Mes agents'"
                agents_ajoutes=$((agents_ajoutes + 1))
                ;;
        esac
    done
    if [ "$agents_ajoutes" -gt 0 ]; then
        # Inserer le bloc en fin de table : coller a la derniere ligne de la
        # table (juste avant le titre suivant). Si la ligne qui precedait le
        # titre est vide, elle passe apres le bloc.
        local insert_at=$(awk '/^## Mes agents/{f=1;next} f && /^(###|##) /{print NR; exit}' "$README")
        if [ -n "$insert_at" ]; then
            if sed -n "$((insert_at - 1))p" "$README" | grep -q '^[[:space:]]*$'; then
                head -n $((insert_at - 1)) "$README" | sed '$d' > "$README.tmp"
            else
                head -n $((insert_at - 1)) "$README" > "$README.tmp"
            fi
            printf '%b' "$bloc_ajout" >> "$README.tmp"
            printf '\n' >> "$README.tmp"
            tail -n +"$insert_at" "$README" >> "$README.tmp"
            mv "$README.tmp" "$README"
        else
            printf '%b' "$bloc_ajout" >> "$README"
        fi
    else
        echo -e "  ${GREEN}[OK]${NC} Table des agents complete"
    fi

    # 4. Reconstruire la liste des outils de chaque categorie : uniquement si
    # l ancienne section 'La boite a outils' existe encore (retro-compatibilite).
    # Nouvelle norme : les listes d outils vivent dans readme-dev (section 6).
    if grep -q '^## La boite a outils ([0-9]* outils)' "$README"; then
    for cle in $(lister_categories); do
        local cat=$(nom_categorie_affichable "$cle")
        local nb=$(compter_outils_categorie "$cle")
        local liste_reelle=$(lister_outils_categorie "$cle")
        # Reconstruire la ligne de la categorie en conservant la colonne Usage
        # Format de ligne : | **Cat (N)** | liste outils | usage |
        # Decoupage par | : parts[1]="", parts[2]=" **Cat (N)** ", parts[3]="liste outils", parts[4]="usage"
        awk -v nb="$nb" -v liste="$liste_reelle" '
            $0 ~ "^\\| \\*\\*" cat " \\(" {
                n = split($0, parts, "|")
                usage = (n >= 5) ? parts[4] : ""
                gsub(/^ +| +$/, "", usage)
                printf "| **%s (%d)** | %s | %s |\n", cat, nb, liste, usage
                next
            }
            { print }
        ' cat="$cat" "$README" > "$README.tmp" && mv "$README.tmp" "$README"
        echo -e "  ${GREEN}[RECONSTRUIT]${NC} ${cat} : ${nb} outils"
    done
    fi

    # 5. Aligner les badges du header (Outils-N, Agents-N) : affichage + href
    # (lecon Clio/Janus : --maj corrigeait les tables mais pas les badges)
    aligner_badges_header

    # 6. Corriger le tableau readme-dev (section 6) : comptes reels par
    # categorie, categories obsoletes retirees, manquantes ajoutees
    # (anti-recurrence bug Clio 132 vs 134 : verifier SANS corriger ne
    # suffisait pas - v0.4.6 corrige le tableau lui-meme)
    corriger_readme_dev

    echo ""
    echo -e "${GREEN}[OK]${NC} README corrige pour refleter l'etat reel."
    echo ""
    echo "=== CONTROLE FINAL : somme des compteurs readme-dev ==="
    if verifier_somme_comptes; then
        echo "[OK] somme des compteurs = total reel (readme-dev coherent)."
    else
        echo "[ECART] readme-dev incoherent - corriger le tableau (section 6) avant de conclure."
    fi
}

# Inserer une image (logo) en tete du README, apres le titre H1
# Idempotent : si le chemin est deja present, n'insere rien.
inserer_logo() {
    local chemin_image="$1"
    local contenu
    if [ -z "$chemin_image" ]; then
        echo -e "${RED}[ERREUR] Option --logo necessite un chemin d'image.${NC}"
        return 1
    fi
    if [ ! -f "$chemin_image" ]; then
        echo -e "${RED}[ERREUR] Fichier image introuvable : ${chemin_image}${NC}"
        return 1
    fi
    if grep -qF -- "$chemin_image" "$README"; then
        echo -e "${GREEN}[OK]${NC} Le logo ${chemin_image} est deja present dans le README (aucun doublon)."
        return 0
    fi
    # Inserer "\n![Logo](chemin)\n\n" juste apres la premiere ligne de titre H1 ("# ")
    awk -v img="$chemin_image" '
        BEGIN { done = 0 }
        {
            if (!done && $0 ~ /^# /) {
                print $0
                print ""
                print "![Logo](" img ")"
                print ""
                done = 1
                next
            }
            print
        }
    ' "$README" > "$README.tmp" && mv "$README.tmp" "$README"
    # Verifier que l'insertion a reellement ete faite (un titre H1 existait)
    if grep -qF -- "![Logo]($chemin_image)" "$README"; then
        echo -e "${GREEN}[OK]${NC} Logo ${chemin_image} insere en tete du README, apres le titre H1."
        return 0
    fi
    echo -e "${RED}[ERREUR]${NC} Aucun titre H1 (# ...) trouve : rien n'a ete insere."
    return 1
}

# Encoder une portion de badge Shields : espace -> '_', tiret -> '--'
encoder_badge() {
    local texte="$1"
    local out=""
    local i c
    for (( i=0; i<${#texte}; i++ )); do
        c="${texte:$i:1}"
        if [ "$c" = " " ]; then
            out="${out}_"
        elif [ "$c" = "-" ]; then
            out="${out}--"
        else
            out="${out}${c}"
        fi
    done
    echo "$out"
}

# Inserer des badges statiques Shields en tete du README, apres le titre H1
# SPEC : liste separee par ';', chaque badge au format label=message:couleur
# Idempotent : si la ligne de badges identique existe deja, n'insere rien.
inserer_badges() {
    local spec="$1"
    local IFS_save="$IFS"
    if [ -z "$spec" ]; then
        echo -e "${RED}[ERREUR] Option --badges necessite une specification.${NC}"
        return 1
    fi
    # Construire la ligne de badges
    local ligne=""
    local b label reste message couleur url label_enc message_enc
    IFS=';' read -ra badges <<< "$spec"
    IFS="$IFS_save"
    for b in "${badges[@]}"; do
        b="$(echo "$b" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
        [ -z "$b" ] && continue
        if [[ "$b" != *"="* ]] || [[ "$b" != *":"* ]]; then
            echo -e "${RED}[ERREUR] Badge invalide (attendu label=message:couleur) : ${b}${NC}"
            return 1
        fi
        label="${b%%=*}"
        reste="${b#*=}"
        # La couleur est apres le dernier ':'
        couleur="${reste##*:}"
        message="${reste%:*}"
        label="$(echo "$label" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
        message="$(echo "$message" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
        couleur="$(echo "$couleur" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
        if [ -z "$label" ] || [ -z "$message" ] || [ -z "$couleur" ]; then
            echo -e "${RED}[ERREUR] Badge incomplet (label, message et couleur requis) : ${b}${NC}"
            return 1
        fi
        # Rejeter tout caractere non-ASCII (regle immuable)
        if printf '%s' "$label$message$couleur" | LC_ALL=C grep -q '[^ -~]'; then
            echo -e "${RED}[ERREUR] Caractere non-ASCII dans un badge : ${b}${NC}"
            return 1
        fi
        label_enc="$(encoder_badge "$label")"
        message_enc="$(encoder_badge "$message")"
        url="https://img.shields.io/badge/${label_enc}-${message_enc}-${couleur}?style=flat"
        if [ -n "$ligne" ]; then ligne="$ligne "; fi
        ligne="${ligne}[![${label}](${url})](${url})"
    done
    if [ -z "$ligne" ]; then
        echo -e "${RED}[ERREUR] Aucun badge valide fourni.${NC}"
        return 1
    fi
    if grep -qF -- "$ligne" "$README"; then
        echo -e "${GREEN}[OK]${NC} Ces badges sont deja presents dans le README (aucun doublon)."
        return 0
    fi
    # Inserer la ligne de badges juste apres la premiere ligne H1
    awk -v badges_ligne="$ligne" '
        BEGIN { done = 0 }
        {
            if (!done && $0 ~ /^# /) {
                print $0
                print ""
                print badges_ligne
                print ""
                done = 1
                next
            }
            print
        }
    ' "$README" > "$README.tmp" && mv "$README.tmp" "$README"
    if grep -qF -- "$ligne" "$README"; then
        echo -e "${GREEN}[OK]${NC} Badge(s) insere(s) en tete du README, apres le titre H1."
        return 0
    fi
    echo -e "${RED}[ERREUR]${NC} Aucun titre H1 (# ...) trouve : rien n'a ete insere."
    return 1
}

# Afficher le journal (diagnostic, non inscrit au README)
afficher_journal() {
    local n="${1:-10}"
    echo "=== Dernieres interventions (${n}) -- diagnostic ==="
    lire_journal "$n"
    echo ""
    echo "Note : ces interventions servent a savoir CE QUI A CHANGE."
    echo "Le README est corrige (--maj), jamais rempli de lignes."
}

# Main
main() {
    local action=""
    local n="10"
    local help="false"
    local logo_chemin=""
    local badges_spec=""

    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verifier)
                action="verifier"
                shift
                ;;
            --dry-run)
                action="dry-run"
                shift
                ;;
            --maj)
                action="maj"
                shift
                ;;
            --journal)
                action="journal"
                shift
                if [[ $1 =~ ^[0-9]+$ ]]; then
                    n="$1"
                    shift
                fi
                ;;
            --logo)
                action="logo"
                shift
                if [[ $# -gt 0 && "$1" != --* ]]; then
                    logo_chemin="$1"
                    shift
                fi
                ;;
            --badges)
                action="badges"
                shift
                if [[ $# -gt 0 && "$1" != --* ]]; then
                    badges_spec="$1"
                    shift
                fi
                ;;
            --agents)
                action="agents"
                shift
                ;;
            --outils)
                action="outils"
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

    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi

    if [ ! -f "$README" ]; then
        echo -e "${RED}[ERREUR] Fichier README introuvable : $README${NC}"
        exit 1
    fi

    case "$action" in
        verifier)
            verifier
            ;;
        dry-run)
            dry_run
            ;;
        maj)
            mettre_a_jour
            ;;
        journal)
            afficher_journal "$n"
            ;;
        logo)
            inserer_logo "$logo_chemin"
            ;;
        badges)
            inserer_badges "$badges_spec"
            ;;
        agents)
            echo "Agents reels : $(compter_agents)"
            ;;
        outils)
            echo "=== Outils par categorie ==="
            local total=0
            for cat in $(lister_categories); do
                local nb=$(compter_outils_categorie "$cat")
                echo "  ${cat} : ${nb}"
                total=$((total + nb))
            done
            echo "  TOTAL : ${total}"
            ;;
        *)
            verifier
            ;;
    esac
}

# Executer
main "$@"
