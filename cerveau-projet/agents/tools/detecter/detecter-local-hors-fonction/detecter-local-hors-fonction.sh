#!/bin/bash
# detecter-local-hors-fonction.sh
# Detecte les declarations 'local' utilisees hors d'une fonction dans les scripts bash
# Proprietaire : Vulcain (outil partage)
# Version : 0.2.0
# Statut : prepare

# Couleurs
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VERSION="0.2.0"
STATUT_DOC="prepare"
VERBOSE=false
CIBLE="cerveau-projet/agents/tools"
RECURSIF=false

# Fonction pour afficher l'aide
afficher_aide() {
    echo "=========================================="
    echo "  detecter-local-hors-fonction v$VERSION"
    echo "  Detecter les 'local' hors fonction"
    echo "=========================================="
    echo ""
    echo "Usage: detecter-local-hors-fonction [CHEMIN] [options]"
    echo ""
    echo "Arguments:"
    echo "  CHEMIN          Fichier .sh ou dossier a analyser (defaut: outils/)"
    echo ""
    echo "Options:"
    echo "  --recursive, -r Recursif (scan de toute une arborescence)"
    echo "  --verbose, -v   Afficher les details"
    echo "  --version       Afficher la version"
    echo "  --aide, -h      Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  detecter-local-hors-fonction.sh outil.sh"
    echo "  detecter-local-hors-fonction.sh --recursive cerveau-projet/agents/tools"
    echo ""
    echo "Retour: 0 si aucun 'local' hors fonction, 1 sinon"
}

# Verifier la presence de python (obligatoire pour le parseur)
verifier_python() {
    if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
        echo -e "${RED}[ERREUR] Python est requis pour ce parseur${NC}"
        exit 2
    fi
}

# Analyser un fichier .sh (via python, heredoc)
analyser_fichier() {
    local fichier="$1"
    python - "$fichier" << 'PYEOF'
# -*- coding: ascii -*-
# Parseur brace-tracking: detecte les 'local' hors fonction
import io
import os
import re
import sys

def analyser(chemin):
    """Retourne la liste des (numero_ligne, contenu) avec 'local' hors fonction"""
    try:
        c = io.open(chemin, encoding='utf-8').read()
    except Exception as e:
        return None, str(e)
    lignes = c.split('\n')
    resultats = []
    prof = 0
    dans_fonction = False
    niveau_fonction = -1

    for i, ligne in enumerate(lignes, 1):
        l = ligne.strip()
        if not l or l.startswith('#'):
            continue
        # Detection debut de fonction: "name() {" ou "function name {"
        m_func = re.match(r'^[A-Za-z_][A-Za-z0-9_]*\s*\(\s*\)\s*\{', l) or re.match(r'^function\s+[A-Za-z_][A-Za-z0-9_]*\s*(\(\s*\))?\s*\{', l)
        if m_func and not dans_fonction:
            dans_fonction = True
            niveau_fonction = prof
            prof += 1
            continue
        ouvr = l.count('{')
        ferm = l.count('}')
        prof += ouvr - ferm
        if ferm > 0 and dans_fonction and prof <= niveau_fonction:
            dans_fonction = False
            niveau_fonction = -1
        if prof < 0:
            prof = 0
        if re.match(r'^\s*local\b', l) and not dans_fonction:
            resultats.append((i, l))
    return resultats, None

chemin = sys.argv[1]
res, erreur = analyser(chemin)
if erreur:
    print("ERREUR_LECTURE:" + erreur)
    sys.exit(2)
for num, ligne in res:
    print("LOCAL_HORS_FONCTION:" + str(num) + ":" + ligne.strip()[:100])
print("TOTAL:" + str(len(res)))
sys.exit(1 if res else 0)
PYEOF
}

# Traitement principal
total_fichiers=0
fichiers_ok=0
fichiers_problemes=0

# Parser les arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --aide|-h)
            afficher_aide
            exit 0
            ;;
        --version)
            echo "detecter-local-hors-fonction v$VERSION"
            exit 0
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --recursive|-r)
            RECURSIF=true
            shift
            ;;
        -*)
            echo -e "${RED}[ERREUR] Option inconnue: $1${NC}"
            echo "Utilisez --aide pour l'aide"
            exit 2
            ;;
        *)
            CIBLE="$1"
            shift
            ;;
    esac
done

verifier_python

echo -e "${BLUE}=== Detection des 'local' hors fonction ===${NC}"
echo -e "${BLUE}Version : $VERSION${NC}"
echo -e "${BLUE}Cible : $CIBLE${NC}"
echo ""

if [[ -f "$CIBLE" ]]; then
    # Mode fichier unique
    total_fichiers=1
    nom=$(basename "$CIBLE")
    echo -e "${BLUE}[FICHIER] Analyse de : $CIBLE${NC}"
    resultat=$(analyser_fichier "$CIBLE")
    total_ligne=$(echo "$resultat" | grep '^TOTAL:' | cut -d':' -f2)
    if [[ "$total_ligne" == "0" ]]; then
        echo -e "${GREEN}[OK] $nom : aucun 'local' hors fonction${NC}"
        fichiers_ok=1
    else
        echo -e "${RED}[PROBLEME] $nom : $total_ligne 'local' hors fonction${NC}"
        echo "$resultat" | grep '^LOCAL_HORS_FONCTION:' | while IFS=: read -r tag num contenu; do
            echo "  L$num: $contenu"
        done
        fichiers_problemes=1
    fi
elif [[ -d "$CIBLE" ]]; then
    # Mode dossier (recursif par defaut sur un dossier)
    while IFS= read -r f; do
        [[ ! -f "$f" ]] && continue
        total_fichiers=$((total_fichiers + 1))
        resultat=$(analyser_fichier "$f")
        total_ligne=$(echo "$resultat" | grep '^TOTAL:' | cut -d':' -f2)
        if [[ "$total_ligne" == "0" ]]; then
            fichiers_ok=$((fichiers_ok + 1))
        else
            fichiers_problemes=$((fichiers_problemes + 1))
            echo -e "${RED}[PROBLEME] $f : $total_ligne 'local' hors fonction${NC}"
            echo "$resultat" | grep '^LOCAL_HORS_FONCTION:' | while IFS=: read -r tag num contenu; do
                echo "  L$num: $contenu"
            done
        fi
        [[ "$VERBOSE" == "true" ]] && echo "  [scanne] $f"
    done < <(find "$CIBLE" -type f -name '*.sh' 2>/dev/null | sort)
else
    echo -e "${RED}[ERREUR] '$CIBLE' n'existe pas${NC}"
    exit 2
fi

echo ""
echo -e "${BLUE}=== Resume ===${NC}"
echo "  Total : $total_fichiers"
echo "  OK : $fichiers_ok"
echo "  Fichiers avec 'local' hors fonction : $fichiers_problemes"

if [[ "$fichiers_problemes" -gt 0 ]]; then
    echo -e "${RED}[KO] Des 'local' hors fonction ont ete detectes${NC}"
    exit 1
else
    echo -e "${GREEN}[OK] Aucun 'local' hors fonction${NC}"
    exit 0
fi
