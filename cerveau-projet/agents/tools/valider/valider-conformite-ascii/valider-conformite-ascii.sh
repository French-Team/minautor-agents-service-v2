#!/bin/bash
# valider-conformite-ascii.sh
# Outil pour valider la conformite ASCII de tous les fichiers du projet
# Version : 0.1.2-beta
# Statut : ebauche

# Configuration
VERSION="0.1.2-beta"
STATUT="ebauche"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== valider-conformite-ascii v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] [DOSSIER]"
    echo ""
    echo "Options :"
    echo "  --dry-run       Afficher les erreurs sans corriger"
    echo "  --verbose       Afficher les details"
    echo "  --corriger      Corriger automatiquement les fichiers"
    echo "  --extensions    Filtrer par extensions (ex: md,sh,txt)"
    echo "  --exclure       Exclure des dossiers (ex: .git,node_modules)"
    echo "  --help          Afficher cette aide"
    echo ""
}

# Verifier si un caractere est non-ASCII
est_non_ascii() {
    local fichier="$1"
    if grep -Pq '[^\x00-\x7F]' "$fichier" 2>/dev/null; then
        return 0
    fi
    if LC_ALL=C grep -q '[^[:print:][:space:]]' "$fichier" 2>/dev/null; then
        return 0
    fi
    if sed -n '/[^\x00-\x7F]/p' "$fichier" 2>/dev/null | grep -q .; then
        return 0
    fi
    return 1
}

# Extraire les caracteres non-ASCII
extraire_caracteres_non_ascii() {
    local fichier="$1"
    if grep -Pn '[^\x00-\x7F]' "$fichier" 2>/dev/null; then
        return
    fi
    awk '/[^\x00-\x7F]/ {print NR": "$0}' "$fichier" 2>/dev/null
}

# Construire et appliquer les corrections via perl
corriger_accents() {
    local fichier="$1"
    local dictionnaire="cerveau-projet/agents/tools/corriger/corriger-accents/dictionnaire-accents.txt"
    local temp_file=$(mktemp)
    
    cp "$fichier" "$temp_file"
    
    if [ -f "$dictionnaire" ]; then
        # Utiliser perl pour lire le dictionnaire et appliquer les corrections
        # perl gere correctement les caracteres UTF-8
        perl -CSD -e '
            use strict;
            use warnings;
            
            my $dict_file = shift;
            my $target_file = shift;
            
            # Lire le dictionnaire
            open my $df, "<:encoding(UTF-8)", $dict_file or die "Cannot open $dict_file: $!";
            my @replacements;
            while (<$df>) {
                chomp;
                next if /^\s*#/;
                next if /^\s*$/;
                if (/^(.+?)\|(.*)$/) {
                    my ($old, $new) = ($1, $2);
                    push @replacements, [$old, $new] if length($old) > 0;
                }
            }
            close $df;
            
            # Lire le fichier cible
            open my $tf, "<:encoding(UTF-8)", $target_file or die "Cannot open $target_file: $!";
            my $content = do { local $/; <$tf> };
            close $tf;
            
            # Appliquer les remplacements
            my $changed = 0;
            for my $r (@replacements) {
                my ($old, $new) = @$r;
                my $count = ($content =~ s/\Q$old\E/$new/g);
                $changed += $count if $count > 0;
            }
            
            # Ecrire le resultat si modifie
            if ($changed > 0) {
                open my $out, ">:encoding(UTF-8)", $target_file or die "Cannot write $target_file: $!";
                print $out $content;
                close $out;
                exit 0;
            } else {
                exit 1;
            }
        ' "$dictionnaire" "$temp_file"
        
        local perl_exit=$?
        
        if [ $perl_exit -eq 0 ]; then
            cp "$temp_file" "$fichier"
            rm -f "$temp_file"
            return 0
        fi
    fi
    
    rm -f "$temp_file"
    return 1
}

# Main
main() {
    local dossier="."
    local dry_run="false"
    local verbose="false"
    local corriger="false"
    local extensions=""
    local exclude=".git,node_modules,.agents,.backup,exemples"
    local help="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run="true"
                shift
                ;;
            --verbose)
                verbose="true"
                shift
                ;;
            --corriger)
                corriger="true"
                shift
                ;;
            --extensions)
                extensions="$2"
                shift 2
                ;;
            --exclure)
                exclude="$2"
                shift 2
                ;;
            --help)
                help="true"
                shift
                ;;
            *)
                dossier="$1"
                shift
                ;;
        esac
    done
    
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    echo "=== Valider conformite ASCII ==="
    echo "Version : ${VERSION}"
    echo "Dossier : ${dossier}"
    echo "Fichiers EXCEPTION VOLONTAIRE (dictionnaire-*.txt) exclus automatiquement"
    echo ""
    
    if [ ! -d "$dossier" ]; then
        echo -e "${RED}[ERREUR] Le dossier n'existe pas : $dossier${NC}"
        exit 1
    fi
    
    local total_files=0
    local ascii_files=0
    local non_ascii_files=0
    local error_files=0
    
    local cmd="find \"$dossier\" -type f"
    
    # Exclusions des fichiers EXCEPTION VOLONTAIRE (dictionnaires d'outils)
    # documentees dans regles-emojis-ascii.md
    cmd="$cmd -not -name \"dictionnaire-*.txt\""
    
    if [ -n "$exclude" ]; then
        IFS=',' read -ra EXCLUDE_DIRS <<< "$exclude"
        for dir in "${EXCLUDE_DIRS[@]}"; do
            cmd="$cmd -not -path \"*/$dir/*\""
        done
    fi
    
    if [ -n "$extensions" ]; then
        IFS=',' read -ra EXT_LIST <<< "$extensions"
        local first=true
        for ext in "${EXT_LIST[@]}"; do
            if [ "$first" = "true" ]; then
                cmd="$cmd \\( -name \"*.${ext}\""
                first=false
            else
                cmd="$cmd -o -name \"*.${ext}\""
            fi
        done
        cmd="$cmd \\)"
    fi
    
    while IFS= read -r fichier; do
        if [ ! -f "$fichier" ]; then
            continue
        fi
        
        total_files=$((total_files + 1))
        
        if est_non_ascii "$fichier"; then
            non_ascii_files=$((non_ascii_files + 1))
            
            if [ "$verbose" = "true" ] || [ "$dry_run" = "true" ]; then
                echo ""
                echo "Fichier : $fichier"
                echo "Caracteres non-ASCII detectes :"
                extraire_caracteres_non_ascii "$fichier" | head -5
            fi
            
            if [ "$corriger" = "true" ]; then
                if corriger_accents "$fichier"; then
                    echo -e "  [OK] Corrige : $fichier"
                    ascii_files=$((ascii_files + 1))
                    non_ascii_files=$((non_ascii_files - 1))
                else
                    echo -e "  [ATTENTION] Impossible de corriger : $fichier"
                    error_files=$((error_files + 1))
                fi
            else
                echo -e "  [ERREUR] Non-ASCII : $fichier"
            fi
        else
            ascii_files=$((ascii_files + 1))
            if [ "$verbose" = "true" ]; then
                echo -e "  [OK] ASCII : $fichier"
            fi
        fi
    done < <(eval "$cmd")
    
    echo ""
    echo "=== Resume ==="
    echo "Total fichiers : ${total_files}"
    echo "Fichiers ASCII : ${ascii_files}"
    echo "Fichiers non-ASCII : ${non_ascii_files}"
    
    if [ "$corriger" = "true" ]; then
        echo "Fichiers corriges : $((non_ascii_files - error_files))"
    fi
    
    if [ "$dry_run" = "true" ]; then
        echo ""
        echo "[DRY-RUN] Aucune correction appliquee"
    fi
    
    if [ "$non_ascii_files" -gt 0 ] && [ "$corriger" = "false" ]; then
        echo ""
        echo -e "${YELLOW}[ATTENTION] Des fichiers non-ASCII ont ete detectes${NC}"
        echo "Utilisez --corriger pour les corriger automatiquement"
        exit 1
    fi
    
    exit 0
}

# Executer
main "$@"
