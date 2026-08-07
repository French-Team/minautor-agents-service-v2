#!/bin/bash
# evaluer-coherence.sh
# Evalue la coherence inter-fichiers : liens, references croisees
# Proprietaire : Themis (outil partage)
# Version : 0.2.1

VERSION="0.2.1"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

afficher_aide() {
    echo "=== evaluer-coherence v${VERSION} ==="
    echo ""
    echo "Usage: $0 [DOSSIER]"
    echo ""
    echo "Evalue la coherence inter-fichiers."
    echo "Sortie : rapport markdown sur stdout."
}

total=0
ok=0
erreurs=0
avertissements=0

dossier="${1:-.}"

echo "=== evaluer-coherence v${VERSION} ==="
echo "Cible : $dossier"
echo ""

if [ ! -d "$dossier" ]; then
    echo -e "${RED}[ERREUR] Le dossier n'existe pas : $dossier${NC}"
    exit 1
fi

echo "# Rapport evaluer-coherence"
echo ""

# 1. Liens internes casses
# Parseur Python : ignore les blocs de code (``` ou ~~~), les motifs generiques
# (exemples de documentation) et les ancres (#section). Verifie l'existence des
# cibles et sort uniquement les liens casses au format "fichier|chemin".
echo "## Liens internes casses"
total=$((total + 1))
liens_casses=0

LIENS_CASSES=$(python - "$dossier/cerveau-projet" "$dossier" << 'PYEOF'
import io
import os
import re
import sys

racine = sys.argv[1]
racine_projet = sys.argv[2]

# Motifs generiques : exemples de documentation, pas des liens reels
# (inclut les exemples de syntaxe des conventions de liens : index.md, frere-b,
#  sous-dossier -- aucun vrai fichier ne porte ces noms fictifs)
motifs_generiques = ('texte', 'chemin', 'ancien.md', 'nouveau.md', 'perdu.md',
                     'exemple.md', '.*', 'fichier.md', 'dossier.md', 'cible.md',
                     'source.md', 'destination.md', 'fichier-exemple', 'index.md',
                     'frere-a', 'frere-b', 'sous-dossier', 'parent.md', 'racine/')

pattern = re.compile(r'\[[^]]+\]\(([^)]+)\)')

sortie = []
for base, dossiers, fichiers in os.walk(racine):
    # Exclure le dossier exemples/ : contient des problemes volontaires pour tester
    if '/exemples/' in base.replace('\\', '/') + '/':
        continue
    for nom_fichier in fichiers:
        if not nom_fichier.endswith('.md'):
            continue
        fichier = os.path.join(base, nom_fichier).replace('\\', '/')
        try:
            contenu = io.open(fichier, encoding='utf-8', errors='replace').read()
            # Normaliser les fins de ligne (CRLF -> LF) pour eviter les \r residuels
            contenu = contenu.replace('\r\n', '\n').replace('\r', '\n')
            lignes = contenu.split('\n')
        except IOError:
            continue
        dans_bloc = False
        for ligne in lignes:
            # Basculer l'etat 'dans un bloc de code'
            if ligne.strip().startswith('```') or ligne.strip().startswith('~~~'):
                dans_bloc = not dans_bloc
                continue
            if dans_bloc:
                continue
            for m in pattern.finditer(ligne):
                chemin = m.group(1).strip()
                if not chemin:
                    continue
                # Ignorer les liens externes et les ancres internes
                if chemin.startswith('http://') or chemin.startswith('https://'):
                    continue
                if chemin.startswith('#'):
                    continue
                # Ignorer les motifs generiques (exemples de documentation)
                if any(motif in chemin for motif in motifs_generiques):
                    continue
                # Resoudre la cible : relative au fichier, a la racine cerveau-projet, ou au projet root
                cible_fichier = os.path.normpath(os.path.join(os.path.dirname(fichier), chemin))
                cible_racine = os.path.normpath(os.path.join(racine, chemin))
                cible_projet = os.path.normpath(os.path.join(racine_projet, chemin))
                if not os.path.exists(cible_fichier) and not os.path.exists(cible_racine) and not os.path.exists(cible_projet):
                    sortie.append(fichier + '|' + chemin)

print('\n'.join(sortie))
PYEOF
)

# Git Bash/MSYS peut convertir les fins de ligne en CRLF dans les substitutions
# de commande : retirer tout \r residuel avant le traitement
LIENS_CASSES=$(printf '%s' "$LIENS_CASSES" | tr -d '\r')

# Afficher les liens casses (max 5)
while IFS='|' read -r fichier chemin; do
    [ -z "$fichier" ] && continue
    liens_casses=$((liens_casses + 1))
    if [ "$liens_casses" -le 5 ]; then
        echo "  - \`$chemin\` dans \`$fichier\`"
    fi
done << EOF
$LIENS_CASSES
EOF

if [ "$liens_casses" -eq 0 ]; then
    echo "| OK | Liens internes | Aucun lien casse detecte |"
    ok=$((ok + 1))
else
    echo "| ERREUR | Liens internes | $liens_casses lien(s) casse(s) (max 5 affiches) |"
    erreurs=$((erreurs + 1))
fi

# 2. Dossiers vides (hors exemples)
echo ""
echo "## Dossiers vides"
total=$((total + 1))
dossiers_vides=0
while IFS= read -r dir; do
    # Exclure les dossiers de test et exemples
    case "$dir" in
        */exemples/*|*/spec/*|*/todo/*|*/.git/*|*/rapports/*) continue ;;
    esac
    nb=$(find "$dir" -maxdepth 0 -type d -empty 2>/dev/null | wc -l)
    if [ "$nb" -gt 0 ]; then
        dossiers_vides=$((dossiers_vides + 1))
        if [ "$dossiers_vides" -le 3 ]; then
            echo "  - \`$dir\`"
        fi
    fi
done < <(find "$dossier/cerveau-projet" -type d 2>/dev/null)

if [ "$dossiers_vides" -eq 0 ]; then
    echo "| OK | Dossiers vides | Aucun dossier vide suspect |"
    ok=$((ok + 1))
else
    echo "| AVERTISSEMENT | Dossiers vides | $dossiers_vides dossier(s) vide(s) |"
    avertissements=$((avertissements + 1))
fi

# 3. Agents references dans AGENTS.md
echo ""
echo "## Agents dans AGENTS.md"
total=$((total + 1))
agents_ref=0
agents_manquants=""
for agent in cerberus buffy athena atlas clio janus minerve morpheus promethee vulcain themis; do
    if grep -q "$agent" "$dossier/AGENTS.md" 2>/dev/null; then
        agents_ref=$((agents_ref + 1))
    else
        agents_manquants="$agents_manquants $agent"
    fi
done
if [ -z "$agents_manquants" ]; then
    echo "| OK | References agents | $agents_ref agent(s) reference(s) dans AGENTS.md |"
    ok=$((ok + 1))
else
    echo "| ERREUR | References agents | Agents non references :$agents_manquants |"
    erreurs=$((erreurs + 1))
fi

# 4. Outils references par les agents
echo ""
echo "## Outils references par les agents"
total=$((total + 1))
outils_casses=0
while IFS= read -r agent_dir; do
    agent_md="$agent_dir/$(basename "$agent_dir").md"
    [ -f "$agent_md" ] || continue
    while IFS= read -r outil_ref; do
        # Extraire le nom de l'outil entre backticks
        outil=$(echo "$outil_ref" | sed -n 's/.*`\([^`]*\)`.*/\1/p' | head -1)
        if [ -n "$outil" ]; then
            # Exclure les conventions, protocoles, regles, templates et workflows
            # (ils vivent dans pense-betes/, pas dans tools/ -- ce ne sont pas des outils)
            case "$outil" in
                convention-*|protocole-*|regles-*|rvav-*|sous-protocole-*) continue ;;
                *-template|template-*) continue ;;
                combos-combos-*) continue ;;
                cat|grep|sed|basher|read_files|write_file|python|ruby|perl|node|awk|sort|find|xargs|chmod|chown|rm|mv|cp|touch|wc|head|tail|cut|tr|uniq|diff|ls|man|echo|printf|sudo|apt|brew|pip) continue ;;
            esac
            # Chercher si l'outil existe dans tools/
            if ! find "$dossier/cerveau-projet/agents/tools" -name "$outil" -type d 2>/dev/null | grep -q .; then
                if ! find "$dossier/cerveau-projet/agents/tools" -name "$outil.sh" -type f 2>/dev/null | grep -q .; then
                    outils_casses=$((outils_casses + 1))
                    if [ "$outils_casses" -le 3 ]; then
                        echo "  - \`$outil\` reference par \`$(basename "$agent_dir")\` mais introuvable"
                    fi
                fi
            fi
        fi
    done < <(grep -oE '`[a-z-]+`' "$agent_md" 2>/dev/null)
done < <(find "$dossier/cerveau-projet/agents" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)

if [ "$outils_casses" -eq 0 ]; then
    echo "| OK | Outils references | Tous les outils references existent |"
    ok=$((ok + 1))
else
    echo "| ERREUR | Outils references | $outils_casses outil(s) reference(s) mais introuvable(s) |"
    erreurs=$((erreurs + 1))
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
echo "Score coherence : $(( ok * 100 / total ))/100"
