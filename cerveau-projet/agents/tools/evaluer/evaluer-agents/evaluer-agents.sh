#!/bin/bash
# evaluer-agents.sh
# Evalue le comportement des agents : respect des protocoles, outils, fiches
# Proprietaire : Themis (outil partage)
# Version : 0.1.0

VERSION="0.1.0"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

afficher_aide() {
    echo "=== evaluer-agents v${VERSION} ==="
    echo ""
    echo "Usage: $0 [DOSSIER]"
    echo ""
    echo "Evalue le comportement des agents."
    echo "Sortie : rapport markdown sur stdout."
}

total=0
ok=0
erreurs=0
avertissements=0

dossier="${1:-.}"

echo "=== evaluer-agents v${VERSION} ==="
echo "Cible : $dossier"
echo ""

if [ ! -d "$dossier" ]; then
    echo -e "${RED}[ERREUR] Le dossier n'existe pas : $dossier${NC}"
    exit 1
fi

echo "# Rapport evaluer-agents"
echo ""

# 1. Chaque agent a une fiche
echo "## Fiches agents"
for agent_dir in "$dossier/cerveau-projet/agents"/*/; do
    agent=$(basename "$agent_dir")
    # Ignorer les dossiers non-agents
    case "$agent" in
        tools|examples|exemples|corrections-template.md|fiche-agent-template.md|index-agents.md) continue ;;
    esac
    [ -d "$agent_dir" ] || continue

    total=$((total + 1))
    if [ -f "$agent_dir/$agent.md" ]; then
        echo "| OK | Fiche $agent | \`$agent/$agent.md\` |"
        ok=$((ok + 1))
    else
        echo "| ERREUR | Fiche $agent | \`$agent/$agent.md\` MANQUANT |"
        erreurs=$((erreurs + 1))
    fi
done

# 2. Chaque agent a corrections.md
echo ""
echo "## Fichiers corrections"
for agent_dir in "$dossier/cerveau-projet/agents"/*/; do
    agent=$(basename "$agent_dir")
    case "$agent" in
        tools|examples|exemples) continue ;;
    esac
    [ -d "$agent_dir" ] || continue

    total=$((total + 1))
    if [ -f "$agent_dir/corrections.md" ]; then
        echo "| OK | Corrections $agent | \`$agent/corrections.md\` |"
        ok=$((ok + 1))
    else
        echo "| AVERTISSEMENT | Corrections $agent | \`$agent/corrections.md\` MANQUANT |"
        avertissements=$((avertissements + 1))
    fi
done

# 3. Chaque outil a un .sh et un .md
echo ""
echo "## Outils complets (sh + md)"
for tool_dir in "$dossier/cerveau-projet/agents/tools"/*/*/*/; do
    tool=$(basename "$tool_dir")
    [ -d "$tool_dir" ] || continue
    [ "$tool" = "spec" ] || [ "$tool" = "todo" ] || [ "$tool" = "rapports" ] || [ "$tool" = "protections" ] || [ "$tool" = "test" ] && continue

    total=$((total + 1))
    has_sh=0
    has_md=0
    [ -f "$tool_dir/$tool.sh" ] && has_sh=1
    [ -f "$tool_dir/$tool.md" ] && has_md=1

    if [ "$has_sh" -eq 1 ] && [ "$has_md" -eq 1 ]; then
        echo "| OK | Outil $tool | .sh + .md presents |"
        ok=$((ok + 1))
    elif [ "$has_sh" -eq 1 ]; then
        echo "| AVERTISSEMENT | Outil $tool | .sh present, .md MANQUANT |"
        avertissements=$((avertissements + 1))
    elif [ "$has_md" -eq 1 ]; then
        echo "| AVERTISSEMENT | Outil $tool | .md present, .sh MANQUANT |"
        avertissements=$((avertissements + 1))
    else
        echo "| ERREUR | Outil $tool | .sh ET .md MANQUANTS |"
        erreurs=$((erreurs + 1))
    fi
done

# 4. Agents declares dans AGENTS.md
echo ""
echo "## Declaration dans AGENTS.md"
total=$((total + 1))
agents_declares=0
for agent_dir in "$dossier/cerveau-projet/agents"/*/; do
    agent=$(basename "$agent_dir")
    case "$agent" in
        tools|examples|exemples) continue ;;
    esac
    [ -d "$agent_dir" ] || continue
    if grep -q "$agent" "$dossier/AGENTS.md" 2>/dev/null; then
        agents_declares=$((agents_declares + 1))
    else
        echo "| ERREUR | Agent $agent | Non declare dans AGENTS.md |"
        erreurs=$((erreurs + 1))
    fi
done
if [ "$erreurs" -eq 0 ]; then
    echo "| OK | Declaration agents | $agents_declares agent(s) declare(s) dans AGENTS.md |"
    ok=$((ok + 1))
fi

# 5. Agent actif = Cerberus (verification)
echo ""
echo "## Agent actif"
total=$((total + 1))
agent_actif=$(grep -m1 'Nom' "$dossier/AGENTS.md" 2>/dev/null | sed -n 's/.*\*\*Nom\*\* *| *\([^|]*\).*/\1/p' | tr -d ' ')
if [ "$agent_actif" = "Cerberus" ]; then
    echo "| OK | Agent actif | Cerberus (attendu) |"
    ok=$((ok + 1))
else
    echo "| AVERTISSEMENT | Agent actif | '$agent_actif' au lieu de Cerberus |"
    avertissements=$((avertissements + 1))
fi

# Resume
echo ""
echo "## Resume"
echo ""
echo "- Total elements verifies : $total"
echo "- OK : $ok"
echo "- Erreurs : $erreurs"
echo "- Avertissements : $avertissements"
echo ""
echo "Score agents : $(( ok * 100 / total ))/100"
