#!/bin/bash
# detecter-usage-outils-externes.sh
# Detecte les traces d'utilisation d'outils externes (CRLF, non-ASCII, BOM)
# dans les fichiers du cerveau-projet.
# Version : 0.1.1
# Statut : prepare

# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.1.1"
STATUT="prepare"

# Verifier la regle de nommage
NOM_FICHIER=$(basename "$0" .sh)
PREFIXE_ATTENDU="detecter-"
if [[ "$NOM_FICHIER" != "$PREFIXE_ATTENDU"* ]]; then
    echo "ERREUR: Le nom '$NOM_FICHIER' ne commence pas par le prefixe '$PREFIXE_ATTENDU'" >&2
    exit 1
fi

CIBLE="${1:-.}"
RECURSIF=0
if [ "$2" = "--recursive" ] || [ "$1" = "--recursive" ]; then
    RECURSIF=1
    if [ "$1" = "--recursive" ]; then
        CIBLE="${2:-.}"
    fi
fi

if [ ! -e "$CIBLE" ]; then
    echo "ERREUR: Cible introuvable: $CIBLE" >&2
    exit 1
fi

# Collecter les fichiers
FICHIERS=""
if [ -f "$CIBLE" ]; then
    FICHIERS="$CIBLE"
elif [ "$RECURSIF" = "1" ]; then
    FICHIERS=$(find "$CIBLE" -type f \( -name '*.md' -o -name '*.sh' -o -name '*.py' -o -name '*.txt' -o -name '*.json' \) \
        -not -path '*/__pycache__/*' -not -path '*/.git/*' 2>/dev/null)
else
    FICHIERS=$(find "$CIBLE" -maxdepth 1 -type f \( -name '*.md' -o -name '*.sh' -o -name '*.py' -o -name '*.txt' -o -name '*.json' \) 2>/dev/null)
fi

# Exclusions par defaut : fichiers/chemins volontairement non conformes
# (dictionnaires d accents/emojis a corriger, exemples pedagogiques de
# tests, documents externes fournis par l utilisateur).
EXCLURE_DEFAUT="corriger-dictionnaire-accents.txt|dictionnaire-emojis.txt|/exemples/|docs-dev-cerveau-projet"

TOTAL_FICHIERS=0
SUSPECTS=0
TOTAL_SIGNES=0

for f in $FICHIERS; do
    # Ignorer les exclusions par defaut (sous-chaine de chemin)
    if echo "$f" | tr '\\' '/' | grep -Eq "$EXCLURE_DEFAUT"; then
        continue
    fi
    TOTAL_FICHIERS=$((TOTAL_FICHIERS + 1))
    SIGNE=""
    # BOM UTF-8 : EF BB BF en tete (od + tr pour fiabilite Git Bash)
    if head -c 3 "$f" 2>/dev/null | od -An -tx1 | tr -d ' \n' | grep -q 'efbbbf'; then
        SIGNE="BOM UTF-8"
    fi
    # CRLF : compter les retours chariot (nos outils ecrivent en LF pur)
    NB_CRLF=$(tr -cd '\r' < "$f" | wc -c)
    NB_CRLF=$(echo "$NB_CRLF" | tr -d ' ')
    if [ "${NB_CRLF:-0}" -gt 0 ] 2>/dev/null; then
        SIGNE="${SIGNE:+$SIGNE, }CRLF (${NB_CRLF} lignes)"
    fi
    # Non-ASCII : octets hors [espace-tilde, tab, LF, CR]
    NON_ASCII=$(LC_ALL=C tr -d '\n\r\t -~' < "$f" | wc -c)
    NON_ASCII=$(echo "$NON_ASCII" | tr -d ' ')
    if [ "${NON_ASCII:-0}" -gt 0 ] 2>/dev/null; then
        SIGNE="${SIGNE:+$SIGNE, }non-ASCII (${NON_ASCII} octets)"
    fi
    if [ -n "$SIGNE" ]; then
        SUSPECTS=$((SUSPECTS + 1))
        NB_SIGNES=$(echo "$SIGNE" | tr ',' '\n' | wc -l)
        NB_SIGNES=$(echo "$NB_SIGNES" | tr -d ' ')
        TOTAL_SIGNES=$((TOTAL_SIGNES + NB_SIGNES))
        echo "SUSPECT: $f"
        echo "    - $SIGNE"
    else
        echo "PROPRE : $f"
    fi
done

echo ""
echo "=== RESUME ==="
echo "Fichiers analyses : $TOTAL_FICHIERS"
echo "Fichiers suspects  : $SUSPECTS"
echo "Signes detectes    : $TOTAL_SIGNES"

if [ "$SUSPECTS" -gt 0 ]; then
    echo "VERDICT : traces d'outils externes detectees (CRLF/non-ASCII/BOM)"
    exit 1
fi

echo "VERDICT : aucun signe d'outil externe -- conformite OK"
exit 0
