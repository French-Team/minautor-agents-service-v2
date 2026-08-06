#!/bin/bash
# decomposeur.sh
# Outil de décomposition des fichiers markdown
# Permet de voir uniquement ce dont on a besoin
# Propriétaire : Vulcain (outil partagé)

# Configuration
FICHIER=""
ACTION=""
PARAMETRE=""
VERBOSE=false
JSON=false

# Fonction pour afficher l'aide
afficher_aide() {
    echo "Usage: $0 <fichier> [options]"
    echo ""
    echo "Actions:"
    echo "  --lister              Lister les sections"
    echo "  --extraire [section]  Extraire une section"
    echo "  --filtrer [type]      Filtrer par type (titres|regles|tableaux|code|liens)"
    echo "  --resume              Afficher le résumé"
    echo "  --compter             Compter le contenu"
    echo ""
    echo "Options:"
    echo "  --json                Sortie JSON"
    echo "  --verbose             Détails supplémentaires"
    echo "  --aide                Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 protocole-outils.md --lister"
    echo "  $0 protocole-outils.md --extraire \"Règles\""
    echo "  $0 protocole-outils.md --filtrer regles"
    echo "  $0 protocole-outils.md --resume"
}

# Fonction pour lister les sections
lister_sections() {
    local fichier=$1
    local num=0
    local sous_num=0
    local prev_level=0
    
    echo "=== Sections de $(basename $fichier) ==="
    echo ""
    
    while IFS= read -r ligne; do
        num=$((num + 1))
        if echo "$ligne" | grep -qE "^## [^#]"; then
            sous_num=0
            echo "$num. $ligne"
            prev_level=2
        elif echo "$ligne" | grep -qE "^### [^#]"; then
            sous_num=$((sous_num + 1))
            echo "   $num.$sous_num $ligne"
            prev_level=3
        elif echo "$ligne" | grep -qE "^#### [^#]"; then
            echo "      $num.$sous_num.1 $ligne"
        fi
    done < "$fichier"
}

# Fonction pour extraire une section
extraire_section() {
    local fichier=$1
    local section=$2
    local dans_section=false
    local niveau=0
    
    echo "=== Section: $section ==="
    echo ""
    
    while IFS= read -r ligne; do
        # Détecter le début de la section
        if echo "$ligne" | grep -qi "$section"; then
            dans_section=true
            niveau=$(echo "$ligne" | grep -oE '^#{1,4}' | wc -c)
            niveau=$((niveau - 1))
            echo "$ligne"
            continue
        fi
        
        # Si on est dans la section
        if [ "$dans_section" = true ]; then
            # Détecter la fin de la section (nouveau titre de même niveau ou supérieur)
            if echo "$ligne" | grep -qE "^#{1,$niveau} [^#]"; then
                break
            fi
            echo "$ligne"
        fi
    done < "$fichier"
}

# Fonction pour filtrer par type
filtrer_type() {
    local fichier=$1
    local type=$2
    
    case $type in
        titres)
            grep -nE "^#{1,4} " "$fichier"
            ;;
        regles)
            grep -nE "RÈGLE|JAMAIS|TOUJOURS|OBLIGATOIRE|INTERDIT" "$fichier"
            ;;
        tableaux)
            grep -nE "^\|.*\|" "$fichier"
            ;;
        code)
            grep -nE '^\`\`\`' "$fichier"
            ;;
        liens)
            grep -nE "\[.*\]\(.*\)" "$fichier"
            ;;
        *)
            echo "Type inconnu: $type"
            echo "Types disponibles: titres, regles, tableaux, code, liens"
            exit 1
            ;;
    esac
}

# Fonction pour afficher le résumé
afficher_resume() {
    local fichier=$1
    local nom=$(basename "$fichier")
    local lignes=$(wc -l < "$fichier")
    local sections=$(grep -cE "^## [^#]" "$fichier")
    local sous_sections=$(grep -cE "^### [^#]" "$fichier")
    local tableaux=$(grep -cE "^\|.*\|" "$fichier")
    local blocs_code=$(grep -cE '^\`\`\`' "$fichier")
    
    echo "=== Résumé de $nom ==="
    echo ""
    echo "Lignes       : $lignes"
    echo "Sections     : $sections"
    echo "Sous-sections: $sous_sections"
    echo "Tableaux     : $tableaux"
    echo "Blocs de code: $blocs_code"
}

# Fonction pour compter le contenu
compter_contenu() {
    local fichier=$1
    local nom=$(basename "$fichier")
    local lignes=$(wc -l < "$fichier")
    local mots=$(wc -w < "$fichier")
    local caracteres=$(wc -c < "$fichier")
    
    echo "=== Comptage de $nom ==="
    echo ""
    echo "Lignes      : $lignes"
    echo "Mots        : $mots"
    echo "Caractères  : $caracteres"
}

# Parser les arguments
while [ $# -gt 0 ]; do
    case $1 in
        "--aide"|"--help"|"-h")
            afficher_aide
            exit 0
            ;;
        "--lister")
            ACTION="lister"
            shift
            ;;
        "--extraire")
            ACTION="extraire"
            PARAMETRE="$2"
            shift 2
            ;;
        "--filtrer")
            ACTION="filtrer"
            PARAMETRE="$2"
            shift 2
            ;;
        "--resume")
            ACTION="resume"
            shift
            ;;
        "--compter")
            ACTION="compter"
            shift
            ;;
        "--json")
            JSON=true
            shift
            ;;
        "--verbose")
            VERBOSE=true
            shift
            ;;
        *)
            FICHIER="$1"
            shift
            ;;
    esac
done

# Vérifier qu'un fichier a été spécifié
if [ -z "$FICHIER" ]; then
    echo "ERREUR: Fichier non spécifié"
    afficher_aide
    exit 1
fi

# Vérifier que le fichier existe
if [ ! -f "$FICHIER" ]; then
    echo "ERREUR: Le fichier $FICHIER n'existe pas"
    exit 1
fi

# Exécuter l'action
case $ACTION in
    lister)
        lister_sections "$FICHIER"
        ;;
    extraire)
        if [ -z "$PARAMETRE" ]; then
            echo "ERREUR: Section non spécifiée"
            exit 1
        fi
        extraire_section "$FICHIER" "$PARAMETRE"
        ;;
    filtrer)
        if [ -z "$PARAMETRE" ]; then
            echo "ERREUR: Type non spécifié"
            exit 1
        fi
        filtrer_type "$FICHIER" "$PARAMETRE"
        ;;
    resume)
        afficher_resume "$FICHIER"
        ;;
    compter)
        compter_contenu "$FICHIER"
        ;;
    *)
        # Par défaut : afficher le résumé
        afficher_resume "$FICHIER"
        ;;
esac
