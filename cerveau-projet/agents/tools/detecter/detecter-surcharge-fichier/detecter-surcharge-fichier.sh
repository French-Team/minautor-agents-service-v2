#!/bin/bash
# detecter-surcharge-fichier.sh
# Detecte les fichiers qui grossissent trop
# Proprietaire : Vulcain (outil partage)
# Version : 0.2.0
# Statut : prepare

# Configuration
VERSION="0.2.0"
STATUT_DOC="prepare"

DOSSIER=${1:-.}
SEUIL=${2:-250}

if [ ! -d "$DOSSIER" ]; then
    echo "[ERREUR] Dossier non trouve : $DOSSIER"
    exit 1
fi

echo "=== Detection de surcharge dans $DOSSIER ==="
echo "Seuil : $SEUIL lignes"
echo ""

TROUBLE=0
TOTAL=0

# Boucle sans pipeline (process substitution) pour que TROUBLE/TOTAL restent visibles
while IFS= read -r FICHIER; do
    TOTAL=$((TOTAL + 1))
    LIGNES=$(wc -l < "$FICHIER")
    if [ "$LIGNES" -gt "$SEUIL" ]; then
        echo "[ATTENTION] $FICHIER : $LIGNES lignes"
        TROUBLE=$((TROUBLE + 1))
    fi
done < <(find "$DOSSIER" -name "*.md" -type f 2>/dev/null)

echo ""
echo "=== Resume ==="
echo "Fichiers analyses : $TOTAL"
echo "En surcharge : $TROUBLE"

if [ "$TROUBLE" -eq 0 ]; then
    echo "[OK] Aucun fichier en surcharge"
    exit 0
else
    echo "[ERREUR] $TROUBLE fichier(s) en surcharge"
    exit 1
fi
