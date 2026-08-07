#!/bin/bash
# verifier-role-fichier.sh
# Verifie qu'un fichier est utilise uniquement pour sa fonction prevue
# Proprietaire : Vulcain (outil partage)
VERSION="0.2.0"

FICHIER=$1

if [ -z "$FICHIER" ]; then
    echo "Usage: $0 [fichier]"
    echo ""
    echo "Verifie qu'un fichier est utilise pour sa fonction prevue."
    echo ""
    echo "Exemples:"
    echo "  $0 cerveau-projet/index-cerveau.md"
    echo "  $0 cerveau-projet/pense-betes/index-pense-bete.md"
    exit 1
fi

if [ ! -f "$FICHIER" ]; then
    echo "[ERREUR] Fichier non trouve : $FICHIER"
    exit 1
fi

# Fonction pour trouver la prochaine ligne non vide
trouver_ligne_suivante() {
    local fichier=$1
    local ligne=$2
    local total=$(wc -l < "$fichier")
    local i=$((ligne + 1))
    while [ $i -le $total ]; do
        local contenu=$(sed -n "${i}p" "$fichier")
        if [ -n "$contenu" ]; then
            echo "$contenu"
            return
        fi
        i=$((i + 1))
    done
    echo ""
}

# Determiner le role du fichier selon son nom
NOM_FICHIER=$(basename "$FICHIER")
ERREURS=0

case "$NOM_FICHIER" in
    index-*.md)
        CONTENU_INTERDIT="^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut du|^## .*Corrections recentes|^## .*Notes de session|^## .*Lecons apprises"
        if grep -qE "$CONTENU_INTERDIT" "$FICHIER" 2>/dev/null; then
            echo "[ERREUR] $FICHIER est un INDEX et contient une section interdite :"
            grep -nE "$CONTENU_INTERDIT" "$FICHIER" | head -5
            ERREURS=$((ERREURS + 1))
        fi
        ;;
    convention-*.md)
        CONTENU_INTERDIT="^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Historique"
        if grep -qE "$CONTENU_INTERDIT" "$FICHIER" 2>/dev/null; then
            LIGNE=$(grep -nE "$CONTENU_INTERDIT" "$FICHIER" | head -1 | cut -d: -f1)
            CONTENU_SUIVANT=$(trouver_ligne_suivante "$FICHIER" "$LIGNE")
            if echo "$CONTENU_SUIVANT" | grep -qE "^\||^\\[|^etat|^Type"; then
                : # OK - c'est une definition
            else
                echo "[ERREUR] $FICHIER est une CONVENTION et contient une section interdite :"
                grep -nE "$CONTENU_INTERDIT" "$FICHIER" | head -5
                ERREURS=$((ERREURS + 1))
            fi
        fi
        ;;
    protocole-*.md)
        CONTENU_INTERDIT="^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut"
        CONTENU_HISTORIQUE="^## .*Historique"
        if grep -qE "$CONTENU_INTERDIT" "$FICHIER" 2>/dev/null; then
            echo "[ERREUR] $FICHIER est un PROTOCOLE et contient une section interdite :"
            grep -nE "$CONTENU_INTERDIT" "$FICHIER" | head -5
            ERREURS=$((ERREURS + 1))
        fi
        if grep -qE "$CONTENU_HISTORIQUE" "$FICHIER" 2>/dev/null; then
            LIGNE=$(grep -nE "$CONTENU_HISTORIQUE" "$FICHIER" | head -1 | cut -d: -f1)
            CONTENU_SUIVANT=$(trouver_ligne_suivante "$FICHIER" "$LIGNE")
            if echo "$CONTENU_SUIVANT" | grep -qE "^\||^\\["; then
                : # OK - c'est une description de template
            else
                echo "[ERREUR] $FICHIER est un PROTOCOLE et contient une section interdite :"
                grep -nE "$CONTENU_HISTORIQUE" "$FICHIER" | head -5
                ERREURS=$((ERREURS + 1))
            fi
        fi
        ;;
    spec-*.md)
        # Les specs peuvent avoir "## Statut" et "## Historique" (c'est de la description)
        CONTENU_INTERDIT="^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire"
        if grep -qE "$CONTENU_INTERDIT" "$FICHIER" 2>/dev/null; then
            echo "[ERREUR] $FICHIER est une SPEC et contient une section interdite :"
            grep -nE "$CONTENU_INTERDIT" "$FICHIER" | head -5
            ERREURS=$((ERREURS + 1))
        fi
        ;;
    *-template.md)
        # Les templates peuvent avoir "## Statut" et "## Historique" (c'est de la description)
        CONTENU_INTERDIT="^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire"
        if grep -qE "$CONTENU_INTERDIT" "$FICHIER" 2>/dev/null; then
            echo "[ERREUR] $FICHIER est un TEMPLATE et contient une section interdite :"
            grep -nE "$CONTENU_INTERDIT" "$FICHIER" | head -5
            ERREURS=$((ERREURS + 1))
        fi
        ;;
esac

# Verifier la taille du fichier
LIGNES=$(wc -l < "$FICHIER")
if [ "$LIGNES" -gt 200 ]; then
    echo "[ATTENTION] $FICHIER fait $LIGNES lignes (seuil: 200)"
    ERREURS=$((ERREURS + 1))
fi

if [ "$ERREURS" -eq 0 ]; then
    echo "[OK] $FICHIER est conforme a son role"
    exit 0
else
    exit 1
fi
