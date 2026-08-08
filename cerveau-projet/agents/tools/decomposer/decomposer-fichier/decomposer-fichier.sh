#!/bin/bash
# decomposer-fichier.sh
# Outil de decomposition des fichiers markdown
# Permet de voir uniquement ce dont on a besoin
# Proprietaire : Vulcain (outil partage)
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
VERSION="0.2.0"

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
    echo "  --resume              Afficher le resume"
    echo "  --compter             Compter le contenu"
    echo ""
    echo "Options:"
    echo "  --json                Sortie JSON"
    echo "  --verbose             Details supplementaires"
    echo "  --aide                Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 protocole-outils.md --lister"
    echo "  $0 protocole-outils.md --extraire \"Regles\""
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
        # Detecter le debut de la section
        if echo "$ligne" | grep -qi "$section"; then
            dans_section=true
            niveau=$(echo "$ligne" | grep -oE '^#{1,4}' | wc -c)
            niveau=$((niveau - 1))
            echo "$ligne"
            continue
        fi
        
        # Si on est dans la section
        if [ "$dans_section" = true ]; then
            # Detecter la fin de la section (nouveau titre de meme niveau ou superieur)
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
            grep -nE "REGLE|JAMAIS|TOUJOURS|OBLIGATOIRE|INTERDIT" "$fichier"
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

# Fonction pour afficher le resume
afficher_resume() {
    local fichier=$1
    local nom=$(basename "$fichier")
    local lignes=$(wc -l < "$fichier")
    local sections=$(grep -cE "^## [^#]" "$fichier")
    local sous_sections=$(grep -cE "^### [^#]" "$fichier")
    local tableaux=$(grep -cE "^\|.*\|" "$fichier")
    local blocs_code=$(grep -cE '^\`\`\`' "$fichier")
    
    echo "=== Resume de $nom ==="
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
    echo "Caracteres  : $caracteres"
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

# Verifier qu'un fichier a ete specifie
if [ -z "$FICHIER" ]; then
    echo "ERREUR: Fichier non specifie"
    afficher_aide
    exit 1
fi

# Verifier que le fichier existe
if [ ! -f "$FICHIER" ]; then
    echo "ERREUR: Le fichier $FICHIER n'existe pas"
    exit 1
fi

# Executer l'action
case $ACTION in
    lister)
        lister_sections "$FICHIER"
        ;;
    extraire)
        if [ -z "$PARAMETRE" ]; then
            echo "ERREUR: Section non specifiee"
            exit 1
        fi
        extraire_section "$FICHIER" "$PARAMETRE"
        ;;
    filtrer)
        if [ -z "$PARAMETRE" ]; then
            echo "ERREUR: Type non specifie"
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
        # Par defaut : afficher le resume
        afficher_resume "$FICHIER"
        ;;
esac
