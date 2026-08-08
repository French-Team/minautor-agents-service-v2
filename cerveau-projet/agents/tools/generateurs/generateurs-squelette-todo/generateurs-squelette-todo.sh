#!/bin/bash
# generateurs-squelette-todo.sh
# Genere le squelette d'un todo conforme au todo-template et a la convention-renommage
# Version : 0.2.0
# Statut : prepare

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
    echo "=== generateurs-squelette-todo v${VERSION} ==="
    echo ""
    echo "Usage: $0 --theme <theme> [--id <id>] [--class <class>] [--statut <statut>] [--dossier <dossier>]"
    echo ""
    echo "Options :"
    echo "  --theme <theme>     Theme du todo (obligatoire, sans accents ni espaces)"
    echo "  --id <id>           Identifiant numerique (defaut: 001)"
    echo "  --class <class>     Classe numerique (defaut: 01)"
    echo "  --statut <statut>   Statut (defaut: ebauche)"
    echo "  --dossier <dossier> Dossier de destination (defaut: spec/todo)"
    echo "  --dry-run           Afficher le squelette sans creer le fichier"
    echo "  --help              Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 --theme pipeline"
    echo "  $0 --theme pipeline --id 001 --dossier cerveau-projet/exemples/pense-bete-exemple-01/spec/todo/"
    echo "  $0 --theme pipeline --dry-run"
    echo ""
}

# Generer le squelette
generer_squelette() {
    local theme="$1"
    local id="$2"
    local class="$3"
    local statut="$4"
    local date=$(date +%Y-%m-%d)
    
    cat << EOF
# Todo -- [Titre de la mission]

> **Taches a realiser pour implementer et maintenir le concept de ${theme}.**

---

## Phase 0 -- Activation de l'agent

> **Regle OBLIGATOIRE** : La premiere action de tout todo est d'activer l'agent adapte.

1. Identifier l'agent adapte
2. Mettre a jour AGENTS.md
3. Lire la fiche et corrections de l'agent
4. Agent active et pret

---

## Header

\`\`\`yaml
mission:
  id: "[MISSION-XXX]"
  titre: "[Titre de la mission]"
  statut: "en-attente"
  date_debut: "[YYYY-MM-DD]"
  date_fin: "[YYYY-MM-DD]"
  agent: "[nom-agent]"
  pense_bete: "[lien]"
  spec: "[lien]"
\`\`\`

---

## Statut de l'intervention

| Element | Statut | Lien |
|---|---|---|
| **Pense-bete** | [en-attente/cree/valide] | [lien] |
| **Spec** | [en-attente/cree/valide] | [lien] |
| **Todo** | [en-attente/en-cours/terminee] | [lien] |

---

## Phase 1 -- Analyse de la demande

1. **Comprendre le besoin** : Qu'est-ce que l'utilisateur demande vraiment ?
2. **Tours de question** : Si ambiguites, poser des questions
3. **Classifier** : Nouveau projet, composant, bug fix, etc.

---

## Phase 2 -- Verification du cerveau

1. **Conventions** : renommage, structures, liens, protocoles
2. **Regles immuables** : validation, emojis, hierarchie
3. **Protocoles** : demarrer, reprendre, installer regles
4. **Recherches-web** : recherches similaires existantes

---

## Phase 3 -- Recherches

1. **Recherches-web** : documenter les sources
2. **Documentation technique** : versions et liens
3. **Comparaison** : code vs recherches
4. **Mise a jour cerveau** : sauvegarder les trouvailles

---

## Phase 4 -- Preparation des outils

1. **Outils disponibles** : lister ceux qui existent
2. **Outils a creer** : identifier les manquants
3. **Protocole** : suivre protocole-outils pour creation

---

## Phase 5 -- Developpement

1. **Taches** : lister avec dependances
2. **Verifications** : conventions, regles, liens

---

## Phase 6 -- Tests et validation

1. **Tests unitaires** : chaque fonction
2. **Tests d'integration** : ensemble
3. **Validation manuelle** : execution reelle
4. **Checklist** : tous les points coches

---

## Phase 7 -- Controle secondaire

1. **Preparer** : fichiers modifies, recherches, tests
2. **Executer** : verifier chaque critere
3. **Decider** : valide, non valide, partiel

---

## Phase 8 -- Finalisation

1. **Statut** : mettre a jour dans le cerveau
2. **Documentation** : historique, recherches
3. **Declaration** : mission terminee

---

## Phase 9 -- Reactivation de Cerberus

> **Regle OBLIGATOIRE** : La derniere action de tout todo est de reactiver Cerberus.

1. Verifier que tout est termine
2. Mettre a jour AGENTS.md (Cerberus agent principal)
3. Documenter la raison du retour

---

## Historique

| Date | Etape | Action | Resultat |
|---|---|---|---|
| ${date} | [Etape] | [Action] | [Resultat] |

---

## Notes

[Notes supplementaires sur la mission]

---

## Liens

- **Pense-bete** : [lien]
- **Spec** : [lien]
- **Recherches-web** : [lien]
- **Cerveau** : [lien]
EOF
}

# Main
main() {
    local theme=""
    local id="001"
    local class="01"
    local statut="ebauche"
    local dossier="spec/todo"
    local dry_run="false"
    local help="false"
    
    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --theme)
                theme="$2"
                shift 2
                ;;
            --id)
                id="$2"
                shift 2
                ;;
            --class)
                class="$2"
                shift 2
                ;;
            --statut)
                statut="$2"
                shift 2
                ;;
            --dossier)
                dossier="$2"
                shift 2
                ;;
            --dry-run)
                dry_run="true"
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
    
    # Verifier le theme obligatoire
    if [ -z "$theme" ]; then
        echo -e "${RED}[ERREUR] Le theme est obligatoire (--theme)${NC}"
        afficher_aide
        exit 1
    fi
    
    # Verifier le theme (pas d'accents, pas d'espaces)
    if echo "$theme" | grep -qE '[^a-z0-9-]'; then
        echo -e "${RED}[ERREUR] Le theme doit etre en minuscules sans accents ni espaces : $theme${NC}"
        exit 1
    fi
    
    # Nom du fichier selon convention-renommage : todo-[theme].[id].[class].[statut].md
    local nom_fichier="todo-${theme}.${id}.${class}.${statut}.md"
    local chemin_fichier="${dossier}/${nom_fichier}"
    
    # Generer le squelette
    local squelette=$(generer_squelette "$theme" "$id" "$class" "$statut")
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} Squelette de : ${nom_fichier}"
        echo ""
        echo "$squelette"
        exit 0
    fi
    
    # Verifier que le fichier n'existe pas deja
    if [ -f "$chemin_fichier" ]; then
        echo -e "${RED}[ERREUR] Le fichier existe deja : ${chemin_fichier}${NC}"
        exit 1
    fi
    
    # Creer le dossier si necessaire
    mkdir -p "$dossier"
    
    # Creer le fichier
    echo "$squelette" > "$chemin_fichier"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK]${NC} Squelette cree : ${chemin_fichier}"
        exit 0
    else
        echo -e "${RED}[ERREUR] Impossible de creer le fichier${NC}"
        exit 1
    fi
}

# Executer
main "$@"
