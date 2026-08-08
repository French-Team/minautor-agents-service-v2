#!/bin/bash
# evaluer-structure.sh
# Evalue la structure du cerveau-projet : dossiers, fichiers critiques, arborescence
# Proprietaire : Themis (outil partage)
# Version : 0.2.0

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== evaluer-structure v${VERSION} ==="
    echo ""
    echo "Usage: $0 [DOSSIER]"
    echo ""
    echo "Evalue la structure du cerveau-projet."
    echo "Sortie : rapport markdown sur stdout."
}

# Compteurs
total=0
ok=0
erreurs=0
avertissements=0

evaluer() {
    local description="$1"
    local chemin="$2"
    local type="$3"  # "fichier" ou "dossier"

    total=$((total + 1))

    if [ "$type" = "fichier" ]; then
        if [ -f "$chemin" ]; then
            echo "| OK | $description | \`$chemin\` |"
            ok=$((ok + 1))
        else
            echo "| ERREUR | $description | \`$chemin\` MANQUANT |"
            erreurs=$((erreurs + 1))
        fi
    elif [ "$type" = "dossier" ]; then
        if [ -d "$chemin" ]; then
            echo "| OK | $description | \`$chemin\` |"
            ok=$((ok + 1))
        else
            echo "| ERREUR | $description | \`$chemin\` MANQUANT |"
            erreurs=$((erreurs + 1))
        fi
    fi
}

evaluer_vide() {
    local description="$1"
    local chemin="$2"

    total=$((total + 1))

    if [ -d "$chemin" ]; then
        local nb=$(find "$chemin" -type f | wc -l)
        if [ "$nb" -eq 0 ]; then
            echo "| AVERTISSEMENT | $description | \`$chemin\` VIDE |"
            avertissements=$((avertissements + 1))
        else
            echo "| OK | $description | \`$chemin\` ($nb fichiers) |"
            ok=$((ok + 1))
        fi
    fi
}

# Main
dossier="${1:-.}"

echo "=== evaluer-structure v${VERSION} ==="
echo "Cible : $dossier"
echo ""

if [ ! -d "$dossier" ]; then
    echo -e "${RED}[ERREUR] Le dossier n'existe pas : $dossier${NC}"
    exit 1
fi

echo "# Rapport evaluer-structure"
echo ""
echo "| Statut | Description | Chemin |"
echo "|---|---|---|"

# Dossiers critiques
echo ""
echo "## Dossiers critiques"
evaluer "Point d'entree du cerveau" "$dossier/cerveau-projet" "dossier"
evaluer "Dossier agents" "$dossier/cerveau-projet/agents" "dossier"
evaluer "Dossier tools" "$dossier/cerveau-projet/agents/tools" "dossier"
evaluer "Dossier pense-betes" "$dossier/cerveau-projet/pense-betes" "dossier"
evaluer "Dossier conventions" "$dossier/cerveau-projet/pense-betes/conventions" "dossier"
evaluer "Dossier regles-immuables" "$dossier/cerveau-projet/pense-betes/regles-immuables" "dossier"
evaluer "Dossier classeur-variables" "$dossier/cerveau-projet/classeur-variables" "dossier"
evaluer "Dossier exemples" "$dossier/cerveau-projet/exemples" "dossier"

# Fichiers critiques
echo ""
echo "## Fichiers critiques"
evaluer "Point de demarrage" "$dossier/demarrer.md" "fichier"
evaluer "Index agents" "$dossier/AGENTS.md" "fichier"
evaluer "README" "$dossier/README.md" "fichier"
evaluer "Index cerveau" "$dossier/cerveau-projet/index-cerveau.md" "fichier"
evaluer "Index agents (detail)" "$dossier/cerveau-projet/agents/index-agents.md" "fichier"
evaluer "Template agent" "$dossier/cerveau-projet/agents/fiche-agent-template.md" "fichier"
evaluer "Index regles" "$dossier/cerveau-projet/pense-betes/regles-immuables/index-regles-immuables.md" "fichier"
evaluer "Regle emojis-ascii" "$dossier/cerveau-projet/pense-betes/regles-immuables/general/regles-emojis-ascii.md" "fichier"
evaluer "RVAV workflow" "$dossier/cerveau-projet/pense-betes/regles-immuables/general/rvav-workflow.md" "fichier"
evaluer "Historique agents" "$dossier/AGENTS-historique.md" "fichier"

# Categories d'outils (par action)
echo ""
echo "## Categories d'outils"
evaluer "Categorie ajouter" "$dossier/cerveau-projet/agents/tools/ajouter" "dossier"
evaluer "Categorie analyser" "$dossier/cerveau-projet/agents/tools/analyser" "dossier"
evaluer "Categorie changer" "$dossier/cerveau-projet/agents/tools/changer" "dossier"
evaluer "Categorie combos" "$dossier/cerveau-projet/agents/tools/combos" "dossier"
evaluer "Categorie condenser" "$dossier/cerveau-projet/agents/tools/condenser" "dossier"
evaluer "Categorie copier" "$dossier/cerveau-projet/agents/tools/copier" "dossier"
evaluer "Categorie corriger" "$dossier/cerveau-projet/agents/tools/corriger" "dossier"
evaluer "Categorie creer" "$dossier/cerveau-projet/agents/tools/creer" "dossier"
evaluer "Categorie decomposer" "$dossier/cerveau-projet/agents/tools/decomposer" "dossier"
evaluer "Categorie deplacer" "$dossier/cerveau-projet/agents/tools/deplacer" "dossier"
evaluer "Categorie detecter" "$dossier/cerveau-projet/agents/tools/detecter" "dossier"
evaluer "Categorie ecrire" "$dossier/cerveau-projet/agents/tools/ecrire" "dossier"
evaluer "Categorie editer" "$dossier/cerveau-projet/agents/tools/editer" "dossier"
evaluer "Categorie evaluer" "$dossier/cerveau-projet/agents/tools/evaluer" "dossier"
evaluer "Categorie generateurs" "$dossier/cerveau-projet/agents/tools/generateurs" "dossier"
evaluer "Categorie gerer" "$dossier/cerveau-projet/agents/tools/gerer" "dossier"
evaluer "Categorie inserer" "$dossier/cerveau-projet/agents/tools/inserer" "dossier"
evaluer "Categorie lire" "$dossier/cerveau-projet/agents/tools/lire" "dossier"
evaluer "Categorie lister" "$dossier/cerveau-projet/agents/tools/lister" "dossier"
evaluer "Categorie mettre-a-jour" "$dossier/cerveau-projet/agents/tools/mettre-a-jour" "dossier"
evaluer "Categorie nettoyer" "$dossier/cerveau-projet/agents/tools/nettoyer" "dossier"
evaluer "Categorie rechercher" "$dossier/cerveau-projet/agents/tools/rechercher" "dossier"
evaluer "Categorie supprimer" "$dossier/cerveau-projet/agents/tools/supprimer" "dossier"
evaluer "Categorie valider" "$dossier/cerveau-projet/agents/tools/valider" "dossier"
evaluer "Categorie verifier" "$dossier/cerveau-projet/agents/tools/verifier" "dossier"
evaluer "Categorie tester (protections)" "$dossier/cerveau-projet/agents/tools/tester" "dossier"

# Dossiers agents (chaque agent a-t-il son dossier ?)
echo ""
echo "## Dossiers agents"
for agent in cerberus buffy athena atlas clio janus minerve morpheus promethee vulcain themis; do
    evaluer "Agent $agent" "$dossier/cerveau-projet/agents/$agent" "dossier"
done

# Contenu des dossiers outils (pas vides)
echo ""
echo "## Contenu des categories d'outils"
evaluer_vide "Categorie ajouter" "$dossier/cerveau-projet/agents/tools/ajouter"
evaluer_vide "Categorie analyser" "$dossier/cerveau-projet/agents/tools/analyser"
evaluer_vide "Categorie changer" "$dossier/cerveau-projet/agents/tools/changer"
evaluer_vide "Categorie combos" "$dossier/cerveau-projet/agents/tools/combos"
evaluer_vide "Categorie condenser" "$dossier/cerveau-projet/agents/tools/condenser"
evaluer_vide "Categorie copier" "$dossier/cerveau-projet/agents/tools/copier"
evaluer_vide "Categorie corriger" "$dossier/cerveau-projet/agents/tools/corriger"
evaluer_vide "Categorie creer" "$dossier/cerveau-projet/agents/tools/creer"
evaluer_vide "Categorie decomposer" "$dossier/cerveau-projet/agents/tools/decomposer"
evaluer_vide "Categorie deplacer" "$dossier/cerveau-projet/agents/tools/deplacer"
evaluer_vide "Categorie detecter" "$dossier/cerveau-projet/agents/tools/detecter"
evaluer_vide "Categorie ecrire" "$dossier/cerveau-projet/agents/tools/ecrire"
evaluer_vide "Categorie editer" "$dossier/cerveau-projet/agents/tools/editer"
evaluer_vide "Categorie evaluer" "$dossier/cerveau-projet/agents/tools/evaluer"
evaluer_vide "Categorie generateurs" "$dossier/cerveau-projet/agents/tools/generateurs"
evaluer_vide "Categorie gerer" "$dossier/cerveau-projet/agents/tools/gerer"
evaluer_vide "Categorie inserer" "$dossier/cerveau-projet/agents/tools/inserer"
evaluer_vide "Categorie lire" "$dossier/cerveau-projet/agents/tools/lire"
evaluer_vide "Categorie lister" "$dossier/cerveau-projet/agents/tools/lister"
evaluer_vide "Categorie mettre-a-jour" "$dossier/cerveau-projet/agents/tools/mettre-a-jour"
evaluer_vide "Categorie nettoyer" "$dossier/cerveau-projet/agents/tools/nettoyer"
evaluer_vide "Categorie rechercher" "$dossier/cerveau-projet/agents/tools/rechercher"
evaluer_vide "Categorie supprimer" "$dossier/cerveau-projet/agents/tools/supprimer"
evaluer_vide "Categorie valider" "$dossier/cerveau-projet/agents/tools/valider"
evaluer_vide "Categorie verifier" "$dossier/cerveau-projet/agents/tools/verifier"
evaluer_vide "Categorie tester (protections)" "$dossier/cerveau-projet/agents/tools/tester"

# Resume
echo ""
echo "## Resume"
echo ""
echo "- Total elements verifies : $total"
echo "- OK : $ok"
echo "- Erreurs : $erreurs"
echo "- Avertissements : $avertissements"
echo ""
echo "Score structure : $(( ok * 100 / total ))/100"
