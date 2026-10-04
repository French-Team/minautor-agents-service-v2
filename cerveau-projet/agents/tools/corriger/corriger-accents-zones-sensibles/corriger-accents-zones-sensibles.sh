#!/bin/bash
# corriger-accents-zones-sensibles.sh
# Outil pour corriger les accents dans les zones sensibles
# Mode standard --all : purge totale (texte francais et titres inclus)
# Conforme a la regle regles-emojis-ascii.md
# Version : 0.2.3
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.3"

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Repertoire de l'outil
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DICTIONNAIRE_DEFAUT="${SCRIPT_DIR}/../corriger-dictionnaire-accents/corriger-dictionnaire-accents.txt"

# Fonction d'aide
utilisation() {
    echo "Utilisation: $0 [OPTIONS] <fichier|dossier>"
    echo ""
    echo "Options:"
    echo "  --dry-run        Afficher les changements sans les appliquer"
    echo "  --all            (compat) Corriger TOUS les accents - desormais le MODE PAR DEFAUT (regle immuable)"
    echo "  --zones-seules   Mode ponctuel : zones sensibles uniquement (accents du corps CONSERVES)"
    echo "  --zones          Zones a corriger (defaut: frontmatter,noms,blocs,code,liens)"
    echo "  --recursive      Traiter recursivement les sous-dossiers"
    echo "  --verbose        Afficher les details"
    echo "  --extensions     Extensions des fichiers de code"
    echo "  --exclure        Motifs de chemins a exclure"
    echo "  --dictionnaire   Chemin vers le dictionnaire"
    echo "  --help           Afficher cette aide"
}

# Parametres
DRY_RUN=0
VERBOSE=0
RECURSIVE=0
ALL_MODE=1  # MODE PAR DEFAUT = --all (purge totale, regle immuable)
ZONES="frontmatter,noms,blocs,code,liens"
DICTIONNAIRE="$DICTIONNAIRE_DEFAUT"
CIBLE=""
EXTENSIONS="sh,py,js,json,yaml,yml,txt"
EXCLUSIONS="node_modules,.git,.agents,.backup,.tmp,test-,dictionnaire-,exemples"

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=1; shift ;;
        --all) ALL_MODE=1; shift ;;
        --zones-seules) ALL_MODE=0; shift ;;
        --zones) ZONES="$2"; shift 2 ;;
        --recursive) RECURSIVE=1; shift ;;
        --verbose) VERBOSE=1; shift ;;
        --extensions) EXTENSIONS="$2"; shift 2 ;;
        --exclure) EXCLUSIONS="$2"; shift 2 ;;
        --dictionnaire) DICTIONNAIRE="$2"; shift 2 ;;
        --help|-h) utilisation; exit 0 ;;
        -*) echo -e "${RED}[ERREUR] Option inconnue: $1${NC}"; exit 1 ;;
        *) CIBLE="$1"; shift ;;
    esac
done

if [[ -z "$CIBLE" ]]; then
    echo -e "${RED}[ERREUR] Aucune cible specifiee${NC}"
    utilisation
    exit 1
fi

if [[ ! -e "$CIBLE" ]]; then
    echo -e "${RED}[ERREUR] Cible non trouvee: $CIBLE${NC}"
    exit 1
fi

if [[ ! -f "$DICTIONNAIRE" ]]; then
    echo -e "${RED}[ERREUR] Dictionnaire non trouve: $DICTIONNAIRE${NC}"
    exit 1
fi

if [[ "$ALL_MODE" -eq 1 ]]; then
    echo "[INFO] Correction de TOUS les accents (mode par defaut --all)"
else
    echo "[INFO] Correction intelligente des accents dans les zones sensibles (--zones-seules)"
fi
echo "Cible: $CIBLE"
echo "Zones: $ZONES"
echo "Dictionnaire: $DICTIONNAIRE"
echo ""

# Construire la liste des fichiers
FICHIERS=""
if [[ -f "$CIBLE" ]]; then
    FICHIERS="$CIBLE"
elif [[ -d "$CIBLE" ]]; then
    if [[ "$RECURSIVE" -eq 1 ]]; then
        # Construire les patterns d'exclusion (tableau bash, pas d'echappements)
        EXCLUDE_ARGS=()
        IFS=',' read -ra EXCL_ARRAY <<< "$EXCLUSIONS"
        for excl in "${EXCL_ARRAY[@]}"; do
            EXCLUDE_ARGS+=( -not -path "*${excl}*" )
        done
        
        # Construire les patterns d'extension (tableau bash)
        EXT_ARGS=()
        IFS=',' read -ra EXT_ARRAY <<< "$EXTENSIONS"
        for ext in "${EXT_ARRAY[@]}"; do
            EXT_ARGS+=( -o -name "*.${ext}" )
        done
        
        # Trouver les fichiers markdown et de code
        FICHIERS=$(find "$CIBLE" -type f \( -name "*.md" "${EXT_ARGS[@]}" \) "${EXCLUDE_ARGS[@]}" 2>/dev/null | tr '\n' ' ')
    else
        # Mode non recursif : uniquement les fichiers du dossier courant
        FICHIERS=$(find "$CIBLE" -maxdepth 1 -type f \( -name "*.md" -o -name "*.sh" -o -name "*.py" -o -name "*.js" \) 2>/dev/null | tr '\n' ' ')
    fi
fi

if [[ -z "$FICHIERS" ]]; then
    echo -e "${YELLOW}[AVERTISSEMENT] Aucun fichier trouve${NC}"
    exit 0
fi

# Compteurs
TOTAL_FICHIERS=0
TOTAL_CORRECTIONS=0
TOTAL_CONSERVE=0

# Traiter chaque fichier
for FICHIER in $FICHIERS; do
    if [[ ! -f "$FICHIER" ]]; then
        continue
    fi
    
    # Verifier les exclusions
    EXCLURE=0
    IFS=',' read -ra EXCL_ARRAY <<< "$EXCLUSIONS"
    for excl in "${EXCL_ARRAY[@]}"; do
        # Verifier si le chemin contient le motif d'exclusion
        if [[ "$FICHIER" == *"$excl"* ]]; then
            EXCLURE=1
            break
        fi
    done
    
    # Exclusion speciale pour le dossier exemples (zone de test)
    if [[ "$FICHIER" == *"exemples/"* ]] || [[ "$FICHIER" == *"/exemples/*" ]]; then
        EXCLURE=1
    fi
    
    if [[ "$EXCLURE" -eq 1 ]]; then
        continue
    fi
    
    TOTAL_FICHIERS=$((TOTAL_FICHIERS + 1))
    
    if [[ "$VERBOSE" -eq 1 ]]; then
        echo -e "${GREEN}[INFO] Traitement: $FICHIER${NC}"
    fi
    
    # Executer la correction via python
    RESULTAT=$(python - "$DICTIONNAIRE" "$FICHIER" "$DRY_RUN" "$VERBOSE" "$ZONES" "$ALL_MODE" <<'PYEOF'
import io, sys, os, difflib, re

dict_file = sys.argv[1]
fichier = sys.argv[2]
dry_run = (sys.argv[3] == "1")
verbose = (sys.argv[4] == "1")
zones = sys.argv[5].split(",")
all_mode = (sys.argv[6] == "1")

# Detector si le fichier est un fichier de code (fichier entier = zone technique)
ext_code = (".sh", ".py", ".js", ".json", ".yaml", ".yml", ".txt")
base = fichier.lower()
est_fichier_code = base.endswith(ext_code)

# Lire le dictionnaire
replacements = []
with io.open(dict_file, encoding="utf-8") as df:
    for line in df:
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            accent, repl = line.split("|", 1)
            if accent:
                replacements.append((accent, repl))

# Lire le fichier
with io.open(fichier, encoding="utf-8") as f:
    lines = f.readlines()

original = "".join(lines)
content = original

# Fonction pour identifier les zones sensibles
def extraire_zones(lines, zones):
    """Retourne un ensemble de numeros de ligne (0-indexed) dans les zones sensibles"""
    lignes_sensibles = set()
    
    # Detecter le frontmatter (lignes 0 et premiere ligne "---" suivante)
    if "frontmatter" in zones:
        if len(lines) > 0 and lines[0].strip() == "---":
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    for j in range(0, i+1):
                        lignes_sensibles.add(j)
                    break
    
    # Detecter les blocs de code
    if "blocs" in zones:
        dans_bloc = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("```"):
                dans_bloc = not dans_bloc
                lignes_sensibles.add(i)
            elif dans_bloc:
                lignes_sensibles.add(i)
    
    # Detecter les liens
    if "liens" in zones:
        pattern = r'\[([^\]]*)\]\(([^)]*)\)'
        for i, line in enumerate(lines):
            matches = re.finditer(pattern, line)
            for match in matches:
                # Ajouter la ligne contenant le lien
                lignes_sensibles.add(i)
    
    # Detecter les noms de fichiers (toutes les lignes pour les noms)
    # Note: les noms de fichiers sont detectes par le pattern de chemin
    if "noms" in zones:
        for i, line in enumerate(lines):
            # Patterns de chemins de fichiers
            if re.search(r'[/\\][a-zA-Z0-9_-]+\.[a-zA-Z]{1,4}', line):
                lignes_sensibles.add(i)
    
    # Pour le code et les autres zones, on traite toutes les lignes
    if "code" in zones or "liens" in zones or "noms" in zones:
        # Ajouter toutes les lignes pour ces zones (sera filtre apres)
        pass
    
    return lignes_sensibles

def est_zone_technique(line, line_num, zones, lines, frontmatter_end, dans_bloc):
    """Determine si une ligne est dans une zone technique"""
    
    # Frontmatter
    if "frontmatter" in zones and line_num <= frontmatter_end:
        return True
    
    # Blocs de code
    if "blocs" in zones and dans_bloc:
        return True
    
    # Liens (pattern [texte](chemin))
    if "liens" in zones:
        if re.search(r'\[([^\]]*)\]\(([^)]*)\)', line):
            return True
    
    # Noms de fichiers (chemins avec extensions)
    if "noms" in zones:
        if re.search(r'[/\\][a-zA-Z0-9_-]+\.[a-zA-Z]{1,4}', line):
            return True
    
    # Code (fichiers de code : fichier entier = zone technique)
    if "code" in zones and est_fichier_code:
        return True
    
    return False

# Identifier les zones
lignes_sensibles = extraire_zones(lines, zones)

# Calculer le frontmatter end
frontmatter_end = -1
if "frontmatter" in zones and len(lines) > 0 and lines[0].strip() == "---":
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            frontmatter_end = i
            break

# Traiter chaque ligne
total_changes = 0
total_conserve = 0
changes_per_zone = {zone: 0 for zone in zones}

for i, line in enumerate(lines):
    dans_bloc = (i in lignes_sensibles and "blocs" in zones)
    
    # En mode --all, traiter toutes les lignes comme zones techniques
    if all_mode or est_zone_technique(line, i, zones, lines, frontmatter_end, dans_bloc):
        # Zone technique : appliquer les remplacements
        new_line = line
        for accent, repl in replacements:
            count = new_line.count(accent)
            if count > 0:
                new_line = new_line.replace(accent, repl)
                total_changes += count
                # Identifier la zone
                if i <= frontmatter_end:
                    changes_per_zone["frontmatter"] += count
                elif dans_bloc:
                    changes_per_zone["blocs"] += count
                elif re.search(r'\[([^\]]*)\]\(([^)]*)\)', line):
                    changes_per_zone["liens"] += count
                elif re.search(r'[/\\][a-zA-Z0-9_-]+\.[a-zA-Z]{1,4}', line):
                    changes_per_zone["noms"] += count
                else:
                    changes_per_zone["code"] += count
        
        if new_line != line:
            lines[i] = new_line
    else:
        # Mode cible : le texte francais n'est pas traite (usage ponctuel)
        # Compter les accents conserves dans ce mode
        for accent, _ in replacements:
            count = line.count(accent)
            if count > 0:
                total_conserve += count

# Reconstruction du contenu
content = "".join(lines)

# Sauvegarder si necessaire
if not dry_run and total_changes > 0:
    backup = fichier + ".bak"
    with io.open(backup, "w", encoding="utf-8", newline="") as f:
        f.write(original)
    with io.open(fichier, "w", encoding="utf-8", newline="") as f:
        f.write(content)

# Rapport
print("FICHIER:{}".format(fichier))
print("CORRECTIONS:{}".format(total_changes))
print("CONSERVE:{}".format(total_conserve))
for zone, count in changes_per_zone.items():
    if count > 0:
        print("ZONE_{}:{}".format(zone.upper(), count))

# Afficher les details en verbose
if verbose and total_changes > 0:
    print("DETAILS:")
    for accent, repl in replacements:
        count_original = original.count(accent)
        count_final = content.count(accent)
        if count_original > 0:
            print("  '{}' -> '{}' : {} -> {}".format(accent, repl, count_original, count_final))
PYEOF
    )
    
    # Parser le resultat
    CORRECTIONS=$(echo "$RESULTAT" | grep "^CORRECTIONS:" | cut -d: -f2)
    CONSERVE=$(echo "$RESULTAT" | grep "^CONSERVE:" | cut -d: -f2)
    
    if [[ -n "$CORRECTIONS" ]] && [[ "$CORRECTIONS" -gt 0 ]]; then
        TOTAL_CORRECTIONS=$((TOTAL_CORRECTIONS + CORRECTIONS))
        TOTAL_CONSERVE=$((TOTAL_CONSERVE + CONSERVE))
        
        if [[ "$VERBOSE" -eq 1 ]]; then
            echo -e "${GREEN}  [OK] $CORRECTIONS corrections, $CONSERVE accents conserves${NC}"
            
            # Afficher les details par zone
            echo "$RESULTAT" | grep "^ZONE_" | while read zone_line; do
                ZONE=$(echo "$zone_line" | cut -d: -f1 | sed 's/ZONE_//')
                COUNT=$(echo "$zone_line" | cut -d: -f2)
                echo "    $ZONE: $COUNT corrections"
            done
        fi
    elif [[ "$VERBOSE" -eq 1 ]]; then
        echo -e "${YELLOW}  [OK] Aucune correction necessaire${NC}"
    fi
done

# Rapport final
echo ""
echo "=== Resume ==="
echo "Fichiers analyses: $TOTAL_FICHIERS"
echo "Corrections appliquees: $TOTAL_CORRECTIONS"
echo "Accents francais conserves: $TOTAL_CONSERVE"

if [[ "$DRY_RUN" -eq 1 ]]; then
    echo -e "${YELLOW}[INFO] Dry-run : aucun fichier n'a ete modifie${NC}"
elif [[ "$TOTAL_CORRECTIONS" -gt 0 ]]; then
    echo -e "${GREEN}[OK] Corrections appliquees avec succes${NC}"
else
    echo -e "${GREEN}[OK] Aucune correction necessaire${NC}"
fi
