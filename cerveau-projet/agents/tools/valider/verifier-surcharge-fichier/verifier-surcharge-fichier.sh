#!/bin/bash
# verifier-surcharge-fichier.sh
# Détecte les fichiers qui grossissent trop
# Propriétaire : Vulcain (outil partagé)

DOSSIER=${1:-.}
SEUIL=${2:-250}

if [ ! -d "$DOSSIER" ]; then
    echo "[ERREUR] Dossier non trouvé : $DOSSIER"
    exit 1
fi

echo "=== Vérification de surcharge dans $DOSSIER ==="
echo "Seuil : $SEUIL lignes"
echo ""

TROUBLE=0

find "$DOSSIER" -name "*.md" -type f | while read FICHIER; do
    LIGNES=$(wc -l < "$FICHIER")
    if [ "$LIGNES" -gt "$SEUIL" ]; then
        echo "[ATTENTION] $FICHIER : $LIGNES lignes"
        TROUBLE=$((TROUBLE + 1))
    fi
done

echo ""
echo "=== Terminé ==="
