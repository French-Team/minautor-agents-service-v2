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
# Version : 0.2.1
# Statut : beta

VERSION="0.2.1"
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

# Template identique au .py v0.2.0 : le triplet (PROTECTIONS + OPTIONS
# ON/OFF + CHRONO) est embarque dans le script genere. Les valeurs sont
# passees via l'environnement (le contenu Python contient des $ et des
# backticks que bash ne doit pas interpreter dans le heredoc quote).
CONTENU=$(cat <<'EOF'
#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil-temporaire
#   appartient_a: commun
#   commun: false
"""
${NOM_CORRIGE}.py
${DESCRIPTION}

Usage:
  python3 ${NOM_CORRIGE}.py [arguments]
  python3 ${NOM_CORRIGE}.py --dry-run [arguments]   (affiche sans executer)
  python3 ${NOM_CORRIGE}.py --isoler N              (isole la fonction N)
  python3 ${NOM_CORRIGE}.py --desactiver 1,3,5      (desactive les fonctions listees)
  python3 ${NOM_CORRIGE}.py --no-chrono             (sans bilan chrono)

REGLE WORKSPACE : outil TEMPORAIRE - cree dans le workspace uniquement.
JAMAIS dans tools/ (outil durable = role Vulcain, protocole 5 fichiers).
Supprime en fin de mission (0 residu) OU promu en outil durable si le
besoin se reproduit (2e utilisation -> activer Vulcain).

TRIPLET (regle immuable generalisee) : ce script embarque les PROTECTIONS
(nommage, dry-run, gestion erreur) + OPTIONS ON/OFF (--isoler/--desactiver)
+ CHRONO (--chrono par defaut, --no-chrono pour le couper) - comme le
template-test v0.3.0 et le template des outils durables.

DECLARATION USAGES (regle immuable) : tout script temporaire de mission est
DECLARE au registre (enregistrer-usage-outil --mode script-temporaire) ainsi
que chaque outil utilise - la fonction declarer_usages() en fin de main()
l assure (renseigner AGENT avec le nom de l agent qui lance ce script).

Version : 0.1.0-tmp
Statut : temporaire
Cree : ${DATE}
"""

import os
import sys
import time

VERSION = "0.1.0-tmp"


def verifier_nommage():
    # Protection : le script doit porter son nom d origine (anti-renommage)
    attendu = "${NOM_CORRIGE}.py"
    if os.path.basename(sys.argv[0]) != attendu:
        print("[ERREUR] Nom de fichier invalide : " + os.path.basename(sys.argv[0]))
        print("  Attendu : " + attendu)
        sys.exit(2)


# --- DECLARATION USAGES (regle immuable, anti-recurrence registre vide) ---
# Tout script temporaire de mission DOIT etre declare au registre + declarer
# les outils utilises. Renseigner AGENT avec le nom de l agent qui lance ce
# script (ex: AGENT = "buffy"). Sans declaration, la mission est invisible
# pour les controles (lecon : registre reste a 0 ligne).
AGENT = "a-completer"


def racine_projet():
    # Remonte depuis ce script jusqu au dossier contenant AGENTS.md (racine)
    courant = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.exists(os.path.join(courant, "AGENTS.md")):
            return courant
        parent = os.path.dirname(courant)
        if parent == courant:
            return None
        courant = parent


def declarer_usage(agent, outil, contexte):
    # Declare un usage au registre (mode script-temporaire par defaut)
    import subprocess as _sp
    racine = racine_projet()
    if not racine:
        print("[AVERTISSEMENT] racine projet introuvable, declaration sautee")
        return
    enregistrer = os.path.join(racine, "cerveau-projet", "agents", "tools",
                               "enregistrer", "enregistrer-usage-outil",
                               "enregistrer-usage-outil.py")
    cmd = [sys.executable, enregistrer, "--agent", agent, "--outil", outil,
           "--mode", "script-temporaire", "--contexte", contexte]
    _sp.run(cmd, check=False)


def declarer_usages():
    # DECLARATION OBLIGATOIRE : le script lui-meme puis, pour chaque outil
    # utilise pendant la mission, un appel declarer_usage(AGENT, outil, contexte)
    if AGENT == "a-completer":
        print("[ERREUR] AGENT non renseigne - renseigner AGENT en tete de script")
        sys.exit(2)
    declarer_usage(AGENT, "${NOM_CORRIGE}.py", "outil temporaire de mission")
    # A COMPLETER : declarer chaque outil utilise pendant la mission
    # declarer_usage(AGENT, "editer-fichier", "<contexte>")
    # declarer_usage(AGENT, "valider-cartes-decision", "<contexte>")


# --- OPTIONS ON/OFF + CHRONO (triplet, regle immuable) ---
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
DRY_RUN = "--dry-run" in sys.argv
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            ISOLE = None
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        DESACTIVES = [int(x) for x in sys.argv[i + 1].split(",")
                      if x.strip().isdigit()]

DEBUT = time.monotonic()
ETAPES = []  # (nom, duree_secondes) alimente le bilan chrono


def point_actif(numero):
    # True si la fonction N doit s executer (options on/off)
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    # Enregistre la duree d une etape (no-op si --no-chrono)
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    # Affiche le bilan des durees : total + detail par etape
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT
    detail = " | ".join("%s=%.2fs" % e for e in ETAPES)
    print("=== CHRONO : total %.2fs (%s) ===" % (total, detail))


def main():
    verifier_nommage()
    if DRY_RUN:
        print("[DRY-RUN] aucune action reelle")
        return 0
    # A COMPLETER : logique du besoin (decouper en fonctions 1., 2., ...)
    # Exemple de squelette avec point_actif + chrono :
    if point_actif(1):
        t = time.monotonic()
        print("${NOM_CORRIGE} : logique a completer")
        chrono_etape("1. logique", t)
    # DECLARATION OBLIGATOIRE (regle immuable) : le script et ses usages
    declarer_usages()
    bilan_chrono()
    return 0


if __name__ == "__main__":
    sys.exit(main())
EOF
)

# Substitution des valeurs dans le template (via env, sans echappement)
CONTENU=$(NOM_CORRIGE="$NOM_CORRIGE" DESCRIPTION="$DESCRIPTION" DATE="$DATE" python3 -c '
import os
import sys
contenu = sys.stdin.read()
contenu = contenu.replace("${NOM_CORRIGE}", os.environ["NOM_CORRIGE"])
contenu = contenu.replace("${DESCRIPTION}", os.environ["DESCRIPTION"])
contenu = contenu.replace("${DATE}", os.environ["DATE"])
sys.stdout.write(contenu)
' <<< "$CONTENU")

# Normalisation : LF pur (le heredoc bash peut produire des CRLF sur Windows)
CONTENU=$(printf '%s' "$CONTENU" | tr -d '\r')

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
