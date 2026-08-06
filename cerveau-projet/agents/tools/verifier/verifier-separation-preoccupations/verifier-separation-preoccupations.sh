#!/bin/bash
# verifier-separation-preoccupations.sh
# Verifie la separation des preoccupations dans les fichiers
# Proprietaire : Vulcain (outil partage)

DOSSIER=${1:-.}

if [ ! -d "$DOSSIER" ]; then
    echo "[ERREUR] Dossier non trouve : $DOSSIER"
    exit 1
fi

echo "=== Verification de la separation des preoccupations ==="
echo ""

# Verifier les index - chercher des SECTIONS (pas des colonnes de tableau)
echo "--- Verification des index ---"
find "$DOSSIER" -name "index-*.md" -type f | while read FICHIER; do
    # Chercher des sections comme "## Prochaines etapes" ou "## TODO"
    if grep -qE "^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut du|^## .*Corrections recentes" "$FICHIER" 2>/dev/null; then
        echo "[ERREUR] $FICHIER contient une section de suivi"
        grep -nE "^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut du|^## .*Corrections recentes" "$FICHIER"
    fi
done

# Verifier les conventions
echo ""
echo "--- Verification des conventions ---"
find "$DOSSIER" -name "convention-*.md" -type f | while read FICHIER; do
    if grep -qE "^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut|^## .*Historique" "$FICHIER" 2>/dev/null; then
        echo "[ERREUR] $FICHIER contient une section de suivi"
        grep -nE "^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut|^## .*Historique" "$FICHIER"
    fi
done

# Verifier les protocoles (ignorer les descriptions de templates)
echo ""
echo "--- Verification des protocoles ---"
find "$DOSSIER" -name "protocole-*.md" -type f | while read FICHIER; do
    # Ignorer les fichiers qui contiennent "template" ou "modele" dans le contenu
    if ! grep -qi "template\|modele\|structure\|structure" "$FICHIER" 2>/dev/null; then
        if grep -qE "^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut|^## .*Historique" "$FICHIER" 2>/dev/null; then
            echo "[ERREUR] $FICHIER contient une section de suivi"
            grep -nE "^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut|^## .*Historique" "$FICHIER"
        fi
    fi
done

echo ""
echo "=== Termine ==="
