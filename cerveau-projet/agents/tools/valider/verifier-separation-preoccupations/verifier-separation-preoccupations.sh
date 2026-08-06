#!/bin/bash
# verifier-separation-preoccupations.sh
# Vérifie la séparation des préoccupations dans les fichiers
# Propriétaire : Vulcain (outil partagé)

DOSSIER=${1:-.}

if [ ! -d "$DOSSIER" ]; then
    echo "[ERREUR] Dossier non trouvé : $DOSSIER"
    exit 1
fi

echo "=== Vérification de la séparation des préoccupations ==="
echo ""

# Vérifier les index - chercher des SECTIONS (pas des colonnes de tableau)
echo "--- Vérification des index ---"
find "$DOSSIER" -name "index-*.md" -type f | while read FICHIER; do
    # Chercher des sections comme "## Prochaines étapes" ou "## TODO"
    if grep -qE "^## .*Prochaines étapes|^## .*TODO|^## .*À faire|^## .*Faire|^## .*Statut du|^## .*Corrections récentes" "$FICHIER" 2>/dev/null; then
        echo "[ERREUR] $FICHIER contient une section de suivi"
        grep -nE "^## .*Prochaines étapes|^## .*TODO|^## .*À faire|^## .*Faire|^## .*Statut du|^## .*Corrections récentes" "$FICHIER"
    fi
done

# Vérifier les conventions
echo ""
echo "--- Vérification des conventions ---"
find "$DOSSIER" -name "convention-*.md" -type f | while read FICHIER; do
    if grep -qE "^## .*Prochaines étapes|^## .*TODO|^## .*À faire|^## .*Faire|^## .*Statut|^## .*Historique" "$FICHIER" 2>/dev/null; then
        echo "[ERREUR] $FICHIER contient une section de suivi"
        grep -nE "^## .*Prochaines étapes|^## .*TODO|^## .*À faire|^## .*Faire|^## .*Statut|^## .*Historique" "$FICHIER"
    fi
done

# Vérifier les protocoles (ignorer les descriptions de templates)
echo ""
echo "--- Vérification des protocoles ---"
find "$DOSSIER" -name "protocole-*.md" -type f | while read FICHIER; do
    # Ignorer les fichiers qui contiennent "template" ou "modèle" dans le contenu
    if ! grep -qi "template\|modèle\|结构\|structure" "$FICHIER" 2>/dev/null; then
        if grep -qE "^## .*Prochaines étapes|^## .*TODO|^## .*À faire|^## .*Faire|^## .*Statut|^## .*Historique" "$FICHIER" 2>/dev/null; then
            echo "[ERREUR] $FICHIER contient une section de suivi"
            grep -nE "^## .*Prochaines étapes|^## .*TODO|^## .*À faire|^## .*Faire|^## .*Statut|^## .*Historique" "$FICHIER"
        fi
    fi
done

echo ""
echo "=== Terminé ==="
