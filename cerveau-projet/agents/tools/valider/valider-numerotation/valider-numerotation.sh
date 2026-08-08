#!/bin/bash
# valider-numerotation.sh
# Verifie que les tableaux d'etapes de mission des fiches agents
# n'ont pas de doublons de numerotation (etape X x2)
# Version : 0.2.0
# Statut : prepare
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier
# ============================================================

# Configuration
VERSION="0.2.0"
STATUT="prepare"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Racine du projet (5 niveaux au-dessus du script : valider-numerotation/ -> valider/ -> tools/ -> agents/ -> cerveau-projet/ -> racine)
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
RACINE=$(cd "$SCRIPT_DIR/../../../../.." && pwd)

# Dossier par defaut : les fiches agents
DOSSIER_DEFAUT="$RACINE/cerveau-projet/agents"

# Afficher l'aide
afficher_aide() {
    echo "=== valider-numerotation v${VERSION} ==="
    echo ""
    echo "Verifie que les tableaux d'etapes de mission des fiches agents"
    echo "n'ont pas de doublons de numerotation (etape X x2)."
    echo ""
    echo "Usage: $0 [OPTIONS] [FICHIER|DOSSIER]"
    echo ""
    echo "Arguments :"
    echo "  [FICHIER]  Verifier un fichier fiche agent (ex: buffy.md)"
    echo "  [DOSSIER]  Verifier toutes les fiches d'un dossier (defaut: agents/)"
    echo ""
    echo "Options :"
    echo "  --agent <nom>   Verifier un seul agent (ex: --agent buffy)"
    echo "  --verbose       Afficher les missions sans doublon"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0                         # Toutes les fiches agents"
    echo "  $0 --agent buffy           # La fiche de Buffy"
    echo "  $0 chemin/vers/fiche.md    # Une fiche precise"
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

# La detection se fait en Python (regex fiable, ASCII strict)
detecter_doublons() {
    local cible="$1"
    python - "$cible" << 'PYEOF'
import io, re, os, sys

cible = sys.argv[1]

def analyser_fichier(f):
    """Retourne la liste des doublons d'etapes dans un fichier fiche agent."""
    c = io.open(f, encoding='utf-8').read()
    lignes = c.split('\n')
    in_mission = False
    mission = None
    in_etapes_table = False
    numeros = []
    doublons = []
    for l in lignes:
        m = re.match(r'^### Mission : (.+)$', l)
        if m:
            if in_mission and numeros:
                for num in sorted(set([n for n in numeros if numeros.count(n) > 1])):
                    doublons.append(mission + ' : etape ' + num + ' x' + str(numeros.count(num)))
            mission = m.group(1)
            in_mission = True
            in_etapes_table = False
            numeros = []
            continue
        if in_mission:
            # Nouvelle section -> la mission est terminee
            if re.match(r'^#{2,3} ', l):
                if numeros:
                    for num in sorted(set([n for n in numeros if numeros.count(n) > 1])):
                        doublons.append(mission + ' : etape ' + num + ' x' + str(numeros.count(num)))
                in_mission = False
                numeros = []
                continue
            # Detecter le tableau d'etapes de mission
            if re.match(r'^\| Etape \|', l):
                in_etapes_table = True
                continue
            # Ligne d'etape dans le tableau : | 5 | ou | **5** |
            m2 = re.match(r'^\|\s*\*{0,2}([0-9]+)\*{0,2}\s*\|', l)
            if m2 and in_etapes_table:
                numeros.append(m2.group(1))
                continue
            # Sortir du tableau si on n'est plus dans un tableau
            if in_etapes_table and not l.strip().startswith('|'):
                in_etapes_table = False
    if in_mission and numeros:
        for num in sorted(set([n for n in numeros if numeros.count(n) > 1])):
            doublons.append(mission + ' : etape ' + num + ' x' + str(numeros.count(num)))
    return doublons

def lister_fiches(cible):
    """Retourne la liste des fichiers fiche agent a analyser."""
    if os.path.isfile(cible):
        return [cible]
    fichiers = []
    # Cas dossier agent direct (ex: agents/buffy -> contient buffy.md)
    nom_dossier = os.path.basename(os.path.normpath(cible))
    fiche_directe = os.path.join(cible, nom_dossier + '.md')
    if os.path.isfile(fiche_directe):
        fichiers.append(fiche_directe)
    # Cas dossier racine agents/ -> parcourir les sous-dossiers
    for d in sorted(os.listdir(cible)):
        chemin = os.path.join(cible, d)
        if os.path.isdir(chemin):
            fiche = os.path.join(chemin, d + '.md')
            if os.path.isfile(fiche):
                fichiers.append(fiche)
    return fichiers

fiches = lister_fiches(cible)
total_doublons = 0
for f in fiches:
    doublons = analyser_fichier(f)
    if doublons:
        nom = os.path.basename(f)
        print('[DOUBLON] ' + nom)
        for d in doublons:
            print('    - ' + d)
        total_doublons += len(doublons)
    else:
        print('[OK] ' + os.path.basename(f))
print('---')
print('Fichiers analyses : ' + str(len(fiches)) + ' | Doublons detectes : ' + str(total_doublons))
sys.exit(1 if total_doublons > 0 else 0)
PYEOF
}

# Main
main() {
    local cible="$DOSSIER_DEFAUT"
    local verbose="false"

    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --agent)
                shift
                cible="$DOSSIER_DEFAUT/$1"
                shift
                ;;
            --verbose)
                verbose="true"
                shift
                ;;
            --help)
                afficher_aide
                exit 0
                ;;
            -*)
                echo -e "${RED}[ERREUR] Option inconnue : $1${NC}"
                afficher_aide
                exit 1
                ;;
            *)
                cible="$1"
                shift
                ;;
        esac
    done

    echo -e "${BLUE}=== valider-numerotation v${VERSION} ===${NC}"
    echo "Cible : $cible"
    echo ""

    if [ ! -e "$cible" ]; then
        echo -e "${RED}[ERREUR] Le chemin n'existe pas : $cible${NC}"
        exit 1
    fi

    detecter_doublons "$cible"
    local code=$?

    if [ $code -eq 0 ]; then
        echo -e "${GREEN}=== Resultat : CONFORME (aucun doublon) ===${NC}"
    else
        echo -e "${RED}=== Resultat : DOUBLONS DETECTES ===${NC}"
    fi
    exit $code
}

# Verifier le nommage au demarrage (regle immuable)
verifier_nommage

# Executer
main "$@"
