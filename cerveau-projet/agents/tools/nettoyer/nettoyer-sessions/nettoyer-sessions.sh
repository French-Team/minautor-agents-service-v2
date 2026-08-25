#!/bin/bash
# nettoyer-sessions.sh
# Supprime TOUTES les sessions LLM (etats actifs uniquement) :
#   - AGENTS.md          : blocs '### Session : session-llm-N' + section '## Sessions connues'
#   - classeur-variables : lignes 'profil-session-*'
# Le frontmatter, l'en-tete de section '## Sessions LLM' et le reste de chaque
# fichier sont PRESERVES : l'en-tete conserve permet a activer-agent-principal
# (sidentifier) de recreer un bloc session a neuf apres le nettoyage.
# AGENTS-historique.md (le journal) n'est JAMAIS modifie : c'est un temoignage.
# Proprietaire : Vulcain
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.1.2"
STATUT="prepare"

AGENTS_FILE="${AGENTS_FILE:-AGENTS.md}"
CLASSEUR_STOCKAGE="${CLASSEUR_STOCKAGE:-cerveau-projet/agents/classeur-variables/stockage/variables-actuelles.md}"

verifier_ascii() {
    local chaine=$1
    CHAINE_ASCII="$chaine" python -c "
import os, sys
for ch in os.environ.get('CHAINE_ASCII', ''):
    if ord(ch) > 127:
        sys.exit(1)
sys.exit(0)
"
    return $?
}

# Nettoyer AGENTS.md : blocs session + section Sessions connues.
# $1 = 1 si dry-run (ne pas ecrire)
nettoyer_agents() {
    local dry_run=$1
    local fichier="$AGENTS_FILE"
    if [ ! -f "$fichier" ]; then
        echo "WARNING: $fichier introuvable - rien a nettoyer"
        NB_AGENTS=0
        return 0
    fi
    local resultat
    resultat=$(AGENTS_FILE_ENV="$fichier" DRY="$dry_run" python - << 'PYEOF'
import io, os
fichier = os.environ.get('AGENTS_FILE_ENV', '')
dry = os.environ.get('DRY', '0') == '1'
with io.open(fichier, encoding='utf-8', errors='replace') as fh:
    lignes = fh.readlines()
sortie = []
dans_section = False
dans_sessions_llm = False
dans_bloc_session = False
nb = 0
sections = ('## Sessions connues',)
en_tete_sessions_llm = '## Sessions LLM'
for ligne in lignes:
    entete = ligne.strip()
    if entete.startswith('## '):
        dans_section = entete in sections
        dans_sessions_llm = (entete == en_tete_sessions_llm)
        dans_bloc_session = False
        if dans_section:
            nb += 1
            continue
        sortie.append(ligne)
        continue
    if dans_section:
        nb += 1
        continue
    if dans_sessions_llm:
        # v0.1.3 (sessions NOMMEES) : session-admin, session-freelance,
        # session-llm-N (legacy) - tout bloc '### Session : session-*'
        if ligne.startswith('### Session : session-'):
            dans_bloc_session = True
            nb += 1
            continue
        if dans_bloc_session:
            if ligne.startswith('### '):
                dans_bloc_session = False
            else:
                nb += 1
                continue
        sortie.append(ligne)
        continue
    sortie.append(ligne)
finale = []
vide = False
for ligne in sortie:
    est_vide = (ligne.strip() == '')
    if est_vide and vide:
        continue
    finale.append(ligne)
    vide = est_vide
if not dry:
    with io.open(fichier, 'w', encoding='utf-8', newline='\n') as fh:
        fh.writelines(finale)
print(nb)
PYEOF
)
    NB_AGENTS="$resultat"
    if [ "$dry_run" = "1" ]; then
        echo "[DRY-RUN] AGENTS.md : $resultat lignes supprimees (blocs session + Sessions connues)"
    else
        echo "AGENTS.md : $resultat lignes supprimees (blocs session + Sessions connues)"
    fi
    return 0
}

# Nettoyer le classeur : lignes profil-session-*.
# $1 = 1 si dry-run (ne pas ecrire)
nettoyer_classeur() {
    local dry_run=$1
    local fichier="$CLASSEUR_STOCKAGE"
    if [ ! -f "$fichier" ]; then
        echo "WARNING: $fichier introuvable - rien a nettoyer"
        NB_CLASSEUR=0
        return 0
    fi
    local nb
    nb=$(grep -c "profil-session-" "$fichier" 2>/dev/null)
    nb=${nb:-0}
    if [ "$dry_run" = "1" ]; then
        echo "[DRY-RUN] Classeur : $nb lignes profil-session supprimees"
        NB_CLASSEUR="$nb"
        return 0
    fi
    if [ "$nb" = "0" ]; then
        echo "Classeur : 0 lignes profil-session supprimees"
        NB_CLASSEUR=0
        return 0
    fi
    local tmp="${fichier}.nettoye"
    grep -v "profil-session-" "$fichier" > "$tmp" && mv "$tmp" "$fichier"
    echo "Classeur : $nb lignes profil-session supprimees"
    NB_CLASSEUR="$nb"
    return 0
}

afficher_aide() {
    echo "Usage: nettoyer-sessions.sh [options]"
    echo ""
    echo "Supprime TOUTES les sessions LLM (etats actifs uniquement) :"
    echo "  - AGENTS.md          : blocs ### Session : session-llm-N + section ## Sessions connues"
    echo "  - classeur-variables : lignes profil-session-*"
    echo ""
    echo "Options:"
    echo "  --dry-run   Afficher ce qui serait supprime sans ecrire"
    echo "  --verbose   Afficher les details"
    echo "  --version   Afficher la version"
    echo ""
    echo "AGENTS-historique.md (le journal) n'est JAMAIS modifie : c'est un temoignage."
}

for arg in "$@"; do
    case $arg in
        --version)
            echo "nettoyer-sessions v$VERSION ($STATUT)"
            exit 0
            ;;
        --aide|-h)
            afficher_aide
            exit 0
            ;;
    esac
done

DRY=0
VERBOSE=0
for arg in "$@"; do
    case $arg in
        --dry-run) DRY=1 ;;
        --verbose) VERBOSE=1 ;;
    esac
done

NB_AGENTS=0
NB_CLASSEUR=0
nettoyer_agents "$DRY"
nettoyer_classeur "$DRY"
if [ "$DRY" = "1" ]; then
    echo "[DRY-RUN] Total : $((NB_AGENTS + NB_CLASSEUR)) lignes a supprimer (aucune modification reelle)"
else
    echo "Nettoyage termine : $((NB_AGENTS + NB_CLASSEUR)) lignes supprimees"
fi
exit 0
