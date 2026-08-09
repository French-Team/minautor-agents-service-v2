#!/bin/bash
# generateurs-commande.sh
# Genere une commande complexe a lancer, en posant une question par parametre.
# Version : 0.2.1
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
#
# Version bash du generateur. Elle lit le meme catalogue que la version
# Python (catalogue-commandes.json) et applique la meme logique :
#   - --liste           : lister les commandes du catalogue
#   - --commande NOM    : generer une commande precise du catalogue
#   - --reponses "a=b;c=d" : reponses fournies en une fois (mode non interactif)
#   - mode interactif   : menu de choix + une question par parametre

VERSION="0.2.1"
STATUT="ebauche"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

DOSSIER_SCRIPT="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
CATALOGUE="${DOSSIER_SCRIPT}/catalogue-commandes.json"

afficher_aide() {
    echo "=== generateurs-commande v${VERSION} ==="
    echo ""
    echo "Usage: $0 [--liste] [--commande NOM] [--reponses 'cle=valeur;cle2=valeur2']"
    echo ""
    echo "Options :"
    echo "  --liste                  Lister les commandes du catalogue"
    echo "  --commande NOM           Generer une commande precise du catalogue"
    echo "  --reponses 'a=b;c=d'     Reponses fournies en une fois (mode non interactif)"
    echo "  --catalogue CHEMIN       Chemin du catalogue (defaut: a cote du script)"
    echo "  --dry-run                Afficher la commande sans l executer"
    echo "  --verbose                Afficher les details"
    echo "  --help                   Afficher cette aide"
    echo "  --version                Afficher la version"
    echo ""
    echo "Exemples :"
    echo "  $0 --liste"
    echo "  $0"
    echo "  $0 --commande activer-activer"
    echo "  $0 --commande remplir-pense-bete --reponses \"fichier=pb.md;section=idee;contenu=Mon idee\""
    echo ""
}

# Verifier le nommage (regle immuable : dossier generateurs/ -> prefixe generateurs-)
verifier_nommage() {
    local script_nom
    script_nom="$(basename "$0" | sed 's/\.sh$//')"
    [[ "$script_nom" == "outil-template" ]] && return 0
    local dossier
    dossier="$(basename "$(cd "$(dirname "$0")" 2>/dev/null && pwd)")"
    local prefixe
    prefixe="${dossier%%-*}-"
    if [[ "$script_nom" != "${prefixe}"* ]]; then
        echo -e "${RED}[ERREUR] Le nom '${script_nom}' ne commence pas par le prefixe du dossier '${prefixe}'${NC}" >&2
        exit 1
    fi
}

# Extraire une valeur du JSON du catalogue (via python3, fiable)
extraire_json() {
    python3 - "$CATALOGUE" "$1" <<'PYEOF'
import json, sys
try:
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("", end="")
    sys.exit(0)
chemin = sys.argv[2]
for commande in data.get("commandes", []):
    if commande.get("nom") == chemin:
        print(json.dumps(commande, ensure_ascii=False))
        sys.exit(0)
print("", end="")
PYEOF
}

lister_commandes() {
    echo -e "${BLUE}=== Commande generateurs-commande ===${NC}"
    echo -e "${BLUE}Version : ${VERSION} (Statut : ${STATUT})${NC}"
    echo ""
    python3 - "$CATALOGUE" <<'PYEOF'
import json, sys
try:
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("Catalogue illisible : %s" % e)
    sys.exit(0)
print("\033[1;33mCommandes disponibles :\033[0m")
for i, commande in enumerate(data.get("commandes", []), 1):
    print("  %2d. %s : %s" % (i, commande.get("nom", "?"), commande.get("description", "")))
PYEOF
}

generer_commande() {
    local nom="$1"
    local reponses_forcees="$2"
    local json_commande
    json_commande="$(extraire_json "$nom")"
    if [[ -z "$json_commande" ]]; then
        echo -e "${RED}[ERREUR] Commande inconnue : ${nom} (utiliser --liste)${NC}" >&2
        return 1
    fi

    echo -e "${BLUE}=== ${nom} ===${NC}"
    python3 - "$json_commande" "$reponses_forcees" <<'PYEOF'
import json, re, sys

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"

def valider(parametre, reponse):
    cle = parametre.get("cle", "?")
    type_param = parametre.get("type", "texte")
    obligatoire = parametre.get("obligatoire", False)
    defaut = parametre.get("defaut", "")
    if reponse == "" and defaut != "":
        reponse = defaut
    if type_param == "flag":
        r = reponse.strip().lower()
        if r in ("", "non", "false", "faux", "n"):
            return "", None
        if r in ("oui", "true", "vrai", "o", "y", "yes"):
            return parametre.get("flag", cle), None
        return None, "Reponse invalide pour %s (oui ou non attendu)" % cle
    if reponse == "":
        if obligatoire:
            return None, "Le parametre %s est obligatoire" % cle
        return "", None
    if type_param == "choix":
        choix = parametre.get("choix", [])
        if reponse not in choix:
            return None, "Valeur invalide pour %s (attendu : %s)" % (cle, ", ".join(choix))
        return reponse, None
    return reponse, None

def composer_valeur(parametre, valeur):
    if valeur == "":
        return ""
    quoter = parametre.get("quoter", False)
    if quoter or re.search(r"\s", valeur):
        valeur_echappee = valeur.replace("\\", "\\\\").replace('"', '\\"')
        return '"%s"' % valeur_echappee
    return valeur

try:
    commande = json.loads(sys.argv[1])
except Exception as e:
    commande = {}

reponses_forcees = {}
chaine = sys.argv[2] if len(sys.argv) > 2 else ""
for morceau in chaine.split(";"):
    morceau = morceau.strip()
    if morceau and "=" in morceau:
        cle, valeur = morceau.split("=", 1)
        reponses_forcees[cle.strip()] = valeur.strip()

reponses = {}
for parametre in commande.get("parametres", []):
    cle = parametre.get("cle", "?")
    if reponses_forcees:
        if cle in reponses_forcees:
            valeur, erreur = valider(parametre, reponses_forcees[cle])
            if erreur:
                print(RED + "  [ERREUR] " + erreur + NC)
                sys.exit(1)
            reponses[cle] = valeur
            continue
        if parametre.get("obligatoire", False):
            print(RED + "  [ERREUR] Parametre obligatoire manquant : " + cle + NC)
            sys.exit(1)
        valeur, erreur = valider(parametre, parametre.get("defaut", ""))
        if erreur:
            print(RED + "  [ERREUR] " + erreur + NC)
            sys.exit(1)
        reponses[cle] = valeur
        continue
    while True:
        question = parametre.get("question", "Valeur pour %s ?" % cle)
        suffixe = ""
        if parametre.get("type") == "choix":
            suffixe = " [choix : %s]" % ", ".join(parametre.get("choix", []))
        defaut = parametre.get("defaut", "")
        if defaut != "":
            suffixe += " [defaut : %s]" % defaut
        print(YELLOW + "[Question] " + question + suffixe + NC)
        try:
            reponse = sys.stdin.readline().strip()
        except EOFError:
            reponse = ""
        if reponse == "" and not defaut:
            print(RED + "  [ABANDON] Entree standard epuisee (EOF)" + NC)
            sys.exit(1)
        valeur, erreur = valider(parametre, reponse)
        if erreur:
            print(RED + "  [ERREUR] " + erreur + NC)
            continue
        reponses[cle] = valeur
        break

modele = commande.get("modele", "")
for parametre in commande.get("parametres", []):
    cle = parametre.get("cle", "?")
    valeur = reponses.get(cle, "")
    if valeur == "":
        # Flag a valeur en dur dans le modele (--cle {cle}) : retirer le flag ET le placeholder si la valeur est vide
        # (corrige 2026-08-09 : parite avec le .py - les flags optionnels vides n etaient jamais retires)
        modele = re.sub(r"--[a-z0-9-]+\s+\{%s\}" % re.escape(cle), "", modele)
        modele = re.sub(r"\s+\{%s\}" % re.escape(cle), "", modele)
    modele = modele.replace("{%s}" % cle, composer_valeur(parametre, valeur))
modele = re.sub(r"\s+", " ", modele).strip()

base = [commande.get("interpreteur", "python3")]
script = commande.get("script", "")
if script:
    base.append(script)
if modele:
    base.append(modele)
print("")
print(GREEN + "=== COMMANDE A LANCER ===" + NC)
print(" ".join(base))
print("")
PYEOF
}

main() {
    local liste="false"
    local nom=""
    local reponses_forcees=""
    local catalogue_defaut="true"
    local verbose="false"
    local help="false"
    local version="false"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --liste) liste="true"; shift ;;
            --commande) nom="$2"; shift 2 ;;
            --reponses) reponses_forcees="$2"; shift 2 ;;
            --catalogue) CATALOGUE="$2"; catalogue_defaut="false"; shift 2 ;;
            --dry-run) shift ;;
            --verbose) verbose="true"; shift ;;
            --help|-h) help="true"; shift ;;
            --version) version="true"; shift ;;
            *) echo -e "${RED}[ERREUR] Option inconnue : $1${NC}" >&2; afficher_aide; exit 1 ;;
        esac
    done

    if [[ "$help" == "true" ]]; then
        afficher_aide
        exit 0
    fi
    if [[ "$version" == "true" ]]; then
        echo "generateurs-commande v${VERSION}"
        exit 0
    fi

    if [[ "$liste" == "true" ]]; then
        lister_commandes
        exit 0
    fi

    if [[ -z "$nom" ]]; then
        # Mode interactif : menu de choix
        lister_commandes
        echo ""
        echo -e "${YELLOW}Quelle commande generer ? (numero ou nom)${NC}"
        read -r choix
        if [[ "$choix" =~ ^[0-9]+$ ]]; then
            nom="$(python3 - "$CATALOGUE" "$choix" <<'PYEOF'
import json, sys
try:
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    index = int(sys.argv[2]) - 1
    commandes = data.get("commandes", [])
    if 0 <= index < len(commandes):
        print(commandes[index].get("nom", ""))
PYEOF
)"
        else
            nom="$choix"
        fi
        if [[ -z "$nom" ]]; then
            echo -e "${RED}[ERREUR] Choix invalide${NC}" >&2
            exit 1
        fi
    fi

    generer_commande "$nom" "$reponses_forcees"
}

verifier_nommage
main "$@"
