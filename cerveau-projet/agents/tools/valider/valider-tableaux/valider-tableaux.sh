#!/bin/bash
# valider-tableaux.sh
# Verifie la coherence des tableaux des fiches agents :
#   1. Nombres d'etapes annonces vs lignes reelles (tableau des missions)
#   2. Numerotation continue des tableaux numerotes (etapes, points de controle)
#   3. Completude des listes d'agents (Agents disponibles vs fiches existantes)
# Version : 0.2.0
# Statut : prepare

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

# Racine du projet (5 niveaux au-dessus du script : valider-tableaux/ -> valider/ -> tools/ -> agents/ -> cerveau-projet/ -> racine)
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
RACINE=$(cd "$SCRIPT_DIR/../../../../.." && pwd)

# Dossier par defaut : les fiches agents
DOSSIER_DEFAUT="$RACINE/cerveau-projet/agents"

# Afficher l'aide
afficher_aide() {
    echo "=== valider-tableaux v${VERSION} ==="
    echo ""
    echo "Verifie la coherence des tableaux des fiches agents :"
    echo "  1. Nombres d'etapes annonces vs lignes reelles (missions)"
    echo "  2. Numerotation continue des tableaux numerotes"
    echo "  3. Completude des listes d'agents"
    echo ""
    echo "Usage: $0 [OPTIONS] [FICHIER|DOSSIER]"
    echo ""
    echo "Arguments :"
    echo "  [FICHIER]  Verifier un fichier fiche agent (ex: buffy.md)"
    echo "  [DOSSIER]  Verifier toutes les fiches d'un dossier (defaut: agents/)"
    echo ""
    echo "Options :"
    echo "  --agent <nom>       Verifier la fiche d'un agent precis"
    echo "  --detail            Afficher le detail complet des verifications"
    echo "  --help              Afficher cette aide"
    echo ""
}

# Parsing des arguments
AGENT=""
DETAIL=0
CIBLE=""
while [ $# -gt 0 ]; do
    case "$1" in
        --help|-h)
            afficher_aide
            exit 0
            ;;
        --agent)
            shift
            AGENT="$1"
            ;;
        --detail)
            DETAIL=1
            ;;
        *)
            CIBLE="$1"
            ;;
    esac
    shift
done

# Determiner la cible
if [ -n "$AGENT" ]; then
    CIBLE="$DOSSIER_DEFAUT/$AGENT/$AGENT.md"
elif [ -z "$CIBLE" ]; then
    CIBLE="$DOSSIER_DEFAUT"
fi

# Option --detail pour le script python
DETAIL_PY=0
[ "$DETAIL" = "1" ] && DETAIL_PY=1

# ============================================================
# Logique Python (fiable pour le parsing des tableaux markdown)
# ============================================================
python3 - "$CIBLE" "$DETAIL_PY" "$RACINE" <<'PYEOF'
# -*- coding: utf-8 -*-
import io, re, os, sys, glob

cible = sys.argv[1]
detail = int(sys.argv[2])
RACINE = sys.argv[3]

# --- 1. Verification: nombres annonces vs lignes reelles ---
def verifier_nombres_annonces(fichier):
    c = io.open(fichier, encoding='utf-8').read()
    lignes = c.split('\n')
    annonces = []   # (mission, nombre annonce)
    details = {}    # mission -> lignes d'etapes
    in_tab = False
    for l in lignes:
        if re.match(r'^#{2,3} .*[Mm]issions [Dd]isponibles', l):
            in_tab = True
            continue
        if in_tab:
            if re.match(r'^#{2,3} ', l):
                in_tab = False
            else:
                m = re.match(r'^\|\s*\*\*(.+?)\*\*\s*\|\s*(\d+)\s*etapes?\s*\|', l)
                if m:
                    annonces.append((m.group(1).strip(), int(m.group(2))))
    in_sec = False
    nom = None
    for l in lignes:
        m = re.match(r'^### Mission : (.+)$', l)
        if m:
            nom = m.group(1).strip()
            details.setdefault(nom, 0)
            in_sec = True
            continue
        if in_sec:
            if re.match(r'^#{2,3} ', l):
                in_sec = False
                continue
            if re.match(r'^\|\s*(\*{0,2}\d+\*{0,2}|\*{0,2}FIN\*{0,2})\s*\|', l):
                details[nom] += 1
    erreurs = []
    for nom_annonce, nb in annonces:
        candidats = [d for d in details if d == nom_annonce or d.startswith(nom_annonce + ' (')]
        if candidats:
            reel = details[candidats[0]]
            if reel != nb:
                erreurs.append('  [NOMBRES] ' + os.path.basename(fichier) + ' : "' + nom_annonce + '" annonce ' + str(nb) + ' etapes, section en contient ' + str(reel))
        else:
            erreurs.append('  [NOMBRES] ' + os.path.basename(fichier) + ' : "' + nom_annonce + '" annonce ' + str(nb) + ' etapes mais AUCUNE section trouvee')
    return erreurs

# --- 2. Verification: numerotation continue (doublons + trous) ---
def verifier_numerotation(fichier):
    c = io.open(fichier, encoding='utf-8').read()
    lignes = c.split('\n')
    erreurs = []
    section = '(debut)'
    numeros = []
    in_table = False
    for l in lignes:
        m = re.match(r'^(#{1,3}) (.+)$', l)
        if m:
            if in_table and numeros:
                err = analyser_numeros(section, numeros, fichier)
                erreurs.extend(err)
                numeros = []
                in_table = False
            section = m.group(2).strip()
            continue
        if l.strip().startswith('|'):
            m2 = re.match(r'^\|\s*(\*{0,2}\d+\*{0,2})\s*\|', l.strip())
            if m2:
                if not in_table:
                    in_table = True
                    numeros = []
                numeros.append(int(m2.group(1).replace('*', '')))
            elif in_table:
                # fin du tableau numerote (ligne sans numero)
                err = analyser_numeros(section, numeros, fichier)
                erreurs.extend(err)
                numeros = []
                in_table = False
        else:
            if in_table and numeros:
                err = analyser_numeros(section, numeros, fichier)
                erreurs.extend(err)
                numeros = []
                in_table = False
    if in_table and numeros:
        erreurs.extend(analyser_numeros(section, numeros, fichier))
    return erreurs

def analyser_numeros(section, numeros, fichier):
    """Detecte doublons et trous dans une sequence de numeros."""
    erreurs = []
    # Doublons
    vus = {}
    for n in numeros:
        vus[n] = vus.get(n, 0) + 1
    for n, count in vus.items():
        if count > 1:
            erreurs.append('  [NUMEROTATION] ' + os.path.basename(fichier) + ' : section "' + section + '" -- numero ' + str(n) + ' en double (x' + str(count) + ')')
    # Trous (sequence qui commence a 0 ou 1)
    uniq = sorted(vus.keys())
    if uniq and uniq[0] in (0, 1):
        debut = uniq[0]
        attendu = list(range(debut, max(uniq) + 1))
        manquants = [x for x in attendu if x not in vus]
        if manquants:
            erreurs.append('  [NUMEROTATION] ' + os.path.basename(fichier) + ' : section "' + section + '" -- numeros manquants : ' + str(manquants))
    return erreurs

# --- 3. Verification: completude des listes d'agents ---
def verifier_liste_agents(fichier_cerberus):
    erreurs = []
    agents_dossiers = []
    agents_dir = os.path.join(RACINE, 'cerveau-projet', 'agents')
    if os.path.isdir(agents_dir):
        for d in sorted(os.listdir(agents_dir)):
            if os.path.isdir(os.path.join(agents_dir, d)) and os.path.exists(os.path.join(agents_dir, d, d + '.md')):
                agents_dossiers.append(d)
    if not os.path.exists(fichier_cerberus):
        return erreurs
    c = io.open(fichier_cerberus, encoding='utf-8').read()
    lignes = c.split('\n')
    in_tab = False
    listes = []
    for l in lignes:
        if re.match(r'^#{2,3} .*[Aa]gents [Dd]isponibles', l):
            in_tab = True
            listes = []
            continue
        if in_tab:
            if re.match(r'^#{2,3} ', l):
                if listes:
                    # verifier la liste completee
                    erreurs.extend(analyser_liste(listes, agents_dossiers, fichier_cerberus))
                    listes = []
                in_tab = False
                continue
            m = re.match(r'^\|\s*\*\*(.+?)\*\*\s*\|', l)
            if m:
                listes.append(m.group(1).strip())
    if listes:
        erreurs.extend(analyser_liste(listes, agents_dossiers, fichier_cerberus))
    return erreurs

def analyser_liste(listes, agents_dossiers, fichier):
    erreurs = []
    # Cerberus ne se liste pas lui-meme
    attends = [a for a in agents_dossiers if a.lower() != 'cerberus']
    manquants = [a for a in attends if a.lower() not in [x.lower() for x in listes]]
    if manquants:
        erreurs.append('  [COMPLETUDE] ' + os.path.basename(fichier) + ' : agents absents de la liste : ' + ', '.join(manquants))
    # Agents listes qui n'existent pas (fausses entrees)
    fantomes = [x for x in listes if x.lower() not in agents_dossiers]
    if fantomes:
        erreurs.append('  [COMPLETUDE] ' + os.path.basename(fichier) + ' : agents listes mais inexistants : ' + ', '.join(fantomes))
    return erreurs

# ============================================================
# Execution
# ============================================================
erreurs = []
fichiers = []
if os.path.isfile(cible):
    fichiers = [cible]
elif os.path.isdir(cible):
    # 1) fiches .md directes dans le dossier
    for f in sorted(glob.glob(os.path.join(cible, '*.md'))):
        fichiers.append(f)
    # 2) fiches dans les sous-dossiers (pattern agent/agent.md)
    for a in sorted(os.listdir(cible)):
        f = os.path.join(cible, a, a + '.md')
        if os.path.exists(f) and f not in fichiers:
            fichiers.append(f)
else:
    print('ERREUR: cible introuvable: ' + cible)
    sys.exit(1)

fichiers_ok = 0
for f in fichiers:
    err_f = []
    err_f += verifier_nombres_annonces(f)
    err_f += verifier_numerotation(f)
    # completude uniquement pour la fiche de Cerberus
    if os.path.basename(f) == 'cerberus.md':
        err_f += verifier_liste_agents(f)
    if err_f:
        erreurs.extend(err_f)
    else:
        fichiers_ok += 1

print('=== valider-tableaux : rapport ===')
print('Fichiers analyses : ' + str(len(fichiers)) + ' | Conformes : ' + str(fichiers_ok) + ' | Problemes : ' + str(len(erreurs)))
print('')
if erreurs:
    for e in erreurs:
        print(e)
    print('')
    print('=== Resultat : NON CONFORME (' + str(len(erreurs)) + ' probleme(s)) ===')
    sys.exit(1)
else:
    print('=== Resultat : CONFORME ===')
    sys.exit(0)
PYEOF
