#!/usr/bin/env bash
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# generateurs-outil-temporaire.sh
# Genere un outil TEMPORAIRE (script Python jetable) dans le workspace pour
# repondre a un besoin ponctuel d'une mission. L'outil temporaire est cree
# DANS le workspace uniquement (jamais hors workspace, jamais dans tools/),
# porte un en-tete standard (identite type: outil-temporaire, ASCII strict,
# LF, 100% stdlib) et se termine par la question de PROMOTION : si le besoin
# se reproduit (2e utilisation), l'agent ACTIVE VULCAIN pour creer l'outil
# durable (protocole 5 fichiers) ; Vulcain reactive ensuite l'agent precedent.
# Version : 0.1.0
# Statut : beta

VERSION="0.1.0"
STATUT="beta"

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
NC="\033[0m"

usage() {
    cat <<EOF
generateurs-outil-temporaire.sh --nom <besoin> [--description <texte>]
    [--dossier <chemin>] [--force] [--version]

Options:
  --nom <besoin>        Nom du besoin (obligatoire, sans accents ni espaces,
                        prefixe tmp- ajoute automatiquement)
  --description <texte> Description courte de ce que fait l'outil temporaire
  --dossier <chemin>    Dossier de destination DANS le workspace (defaut:
                        racine du workspace)
  --force               Ecrire reellement le fichier (sans --force : dry-run)
  --version             Afficher la version
  --aide, -h            Afficher cette aide

Retour: 0 si succes, 1 si erreur.
EOF
}

# Protection du nommage : refuser si le script est renomme
NOM_ATTENDU="generateurs-outil-temporaire.sh"
NOM_SCRIPT=$(basename "$0")
if [ "$NOM_SCRIPT" != "$NOM_ATTENDU" ]; then
    echo -e "${RED}[ERREUR] Nom de fichier invalide : $NOM_SCRIPT${NC}"
    echo -e "${YELLOW}  Attendu : $NOM_ATTENDU${NC}"
    exit 2
fi

# Detection du workspace : remonter jusqu'au dossier contenant AGENTS.md
resoudre_workspace() {
    local courant
    courant=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
    while [ ! -f "$courant/AGENTS.md" ]; do
        local parent
        parent=$(dirname "$courant")
        [ "$parent" = "$courant" ] && return 1
        courant="$parent"
    done
    echo "$courant"
}

question_promotion() {
    local nom="$1"
    echo ""
    echo -e "${YELLOW}=== QUESTION (destinee a l'agent, reponse selon la carte) ===${NC}"
    echo -e "${YELLOW}Ce besoin est-il deja apparu auparavant (2e utilisation) ?${NC}"
    echo ""
    echo -e "${GREEN}[NON] - Usage ponctuel :${NC}"
    echo "  L'outil temporaire ${nom}.py est utilisable pour la mission."
    echo "  Il sera SUPPRIME en fin de mission (0 residu, regle workspace)."
    echo ""
    echo -e "${GREEN}[OUI] - Besoin recurrent (PROMOTION) :${NC}"
    echo "  1) ACTIVER VULCAIN directement (maillon de chaine, pas Cerberus) :"
    echo "     activer-agent-principal.py activer <session> vulcain <raison>"
    echo "  2) Vulcain cree l'outil DURABLE (protocole 5 fichiers : py+sh+md+spec+index)"
    echo "  3) Vulcain termine puis REACTIVE L'AGENT PRECEDENT :"
    echo "     activer-agent-principal.py reactiver <session> <raison> <agent_precedent>"
    echo "  4) L'agent precedent reprend SA mission avec l'outil durable."
    echo ""
    echo "La promotion systematique : un besoin utilise 2x n'a pas le droit"
    echo "de rester temporaire (lecon : script temporaire -> outil durable)."
}

NOM=""
DESCRIPTION=""
DOSSIER=""
FORCE="false"

while [ $# -gt 0 ]; do
    case "$1" in
        --nom)
            NOM="$2"
            shift 2
            ;;
        --description)
            DESCRIPTION="$2"
            shift 2
            ;;
        --dossier)
            DOSSIER="$2"
            shift 2
            ;;
        --force)
            FORCE="true"
            shift
            ;;
        --version)
            echo "generateurs-outil-temporaire.sh $VERSION ($STATUT)"
            exit 0
            ;;
        --aide|-h)
            usage
            exit 0
            ;;
        *)
            echo -e "${RED}[ERREUR] Option inconnue : $1${NC}"
            usage
            exit 1
            ;;
    esac
done

if [ -z "$NOM" ]; then
    echo -e "${RED}[ERREUR] Parametre --nom obligatoire${NC}"
    usage
    exit 1
fi

# Normalisation du nom
NOM_CORRIGE=$(echo "$NOM" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
if ! echo "$NOM_CORRIGE" | grep -qE '^[a-z0-9-]+$'; then
    echo -e "${RED}[ERREUR] Nom invalide : $NOM${NC}"
    echo -e "${YELLOW}  Le nom doit contenir uniquement des minuscules, chiffres et tirets${NC}"
    exit 1
fi

# Prefixe tmp- automatique
case "$NOM_CORRIGE" in
    tmp-*) ;;
    *) NOM_CORRIGE="tmp-$NOM_CORRIGE" ;;
esac

WORKSPACE=$(resoudre_workspace)
if [ -z "$WORKSPACE" ]; then
    echo -e "${RED}[ERREUR] Workspace introuvable (marqueur AGENTS.md absent)${NC}"
    exit 1
fi

if [ -n "$DOSSIER" ]; then
    DOSSIER_ABS=$(cd "$DOSSIER" 2>/dev/null && pwd)
    if [ -z "$DOSSIER_ABS" ]; then
        echo -e "${RED}[ERREUR] Dossier inaccessible : $DOSSIER${NC}"
        exit 1
    fi
else
    DOSSIER_ABS="$WORKSPACE"
fi

# Verification du perimetre workspace
case "$DOSSIER_ABS" in
    "$WORKSPACE"|"$WORKSPACE"/*) ;;
    *)
        echo -e "${RED}[ERREUR] Chemin hors workspace : $DOSSIER_ABS${NC}"
        echo -e "${YELLOW}  REGLE WORKSPACE : ecriture = workspace seul, jamais hors workspace.${NC}"
        exit 1
        ;;
esac

CHEMIN="$DOSSIER_ABS/$NOM_CORRIGE.py"
DATE=$(date +%Y-%m-%d)
# Nom sans le prefixe tmp- pour la description par defaut
NOM_SIMPLE="$NOM_CORRIGE"
case "$NOM_SIMPLE" in
    tmp-*) NOM_SIMPLE="${NOM_SIMPLE#tmp-}" ;;
esac
[ -z "$DESCRIPTION" ] && DESCRIPTION="Outil temporaire pour le besoin $NOM_SIMPLE"

CONTENU=$(cat <<EOF
#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil-temporaire
#   appartient_a: commun
#   commun: false
"""
$NOM_CORRIGE.py
$DESCRIPTION

Usage:
  python3 $NOM_CORRIGE.py [arguments]

REGLE WORKSPACE : outil TEMPORAIRE - cree dans le workspace uniquement.
JAMAIS dans tools/ (outil durable = role Vulcain, protocole 5 fichiers).
Supprime en fin de mission (0 residu) OU promu en outil durable si le
besoin se reproduit (2e utilisation -> activer Vulcain).

Version : 0.1.0-tmp
Statut : temporaire
Cree : $DATE
"""

import sys

VERSION = "0.1.0-tmp"


def main():
    # A COMPLETER : logique du besoin
    print("$NOM_CORRIGE : logique a completer")


if __name__ == "__main__":
    main()
EOF
)

if [ "$FORCE" = "false" ]; then
    echo -e "${YELLOW}=== DRY-RUN (aucun fichier cree) : contenu de $CHEMIN ===${NC}"
    echo "$CONTENU"
    echo -e "${GREEN}[OK] Re-lancer avec --force pour ecrire reellement le fichier.${NC}"
    question_promotion "$NOM_CORRIGE"
    exit 0
fi

if [ -f "$CHEMIN" ]; then
    echo -e "${RED}[ERREUR] Le fichier existe deja : $CHEMIN${NC}"
    exit 1
fi

if printf '%s\n' "$CONTENU" > "$CHEMIN" 2>/dev/null; then
    echo -e "${GREEN}[OK] Outil temporaire cree : $CHEMIN${NC}"
    echo -e "${GREEN}[OK] ASCII strict + LF pur appliques.${NC}"
    echo -e "${GREEN}[OK] Lire le .md d'usage avant utilisation (Pattern 9).${NC}"
    question_promotion "$NOM_CORRIGE"
    exit 0
else
    echo -e "${RED}[ERREUR] Impossible d'ecrire : $CHEMIN${NC}"
    exit 1
fi
