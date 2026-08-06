#!/bin/bash
# generateurs-squelette-spec.sh
# Genere le squelette d'une spec conforme au spec-template et a la convention-renommage
# Version : 0.2.0
# Statut : prepare

# Configuration
VERSION="0.2.0"
STATUT="prepare"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Afficher l'aide
afficher_aide() {
    echo "=== generateurs-squelette-spec v${VERSION} ==="
    echo ""
    echo "Usage: $0 --theme <theme> [--id <id>] [--class <class>] [--statut <statut>] [--dossier <dossier>] [--parent <lien>]"
    echo ""
    echo "Options :"
    echo "  --theme <theme>     Theme de la spec (obligatoire, sans accents ni espaces)"
    echo "  --id <id>           Identifiant numerique (defaut: 001)"
    echo "  --class <class>     Classe numerique (defaut: 01)"
    echo "  --statut <statut>   Statut (defaut: ebauche)"
    echo "  --dossier <dossier> Dossier de destination (defaut: spec/)"
    echo "  --parent <lien>     Lien vers le pense-bete source"
    echo "  --dry-run           Afficher le squelette sans creer le fichier"
    echo "  --help              Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 --theme pipeline"
    echo "  $0 --theme pipeline --id 001 --dossier cerveau-projet/exemples/pense-bete-exemple-01/spec/"
    echo "  $0 --theme pipeline --parent pense-bete-pipeline.001.01.ebauche.md"
    echo ""
}

# Generer le squelette
generer_squelette() {
    local theme="$1"
    local id="$2"
    local class="$3"
    local statut="$4"
    local parent="$5"
    local date=$(date +%Y-%m-%d)
    
    cat << EOF
# Gabarit -- Specification

> **Specification technique de [theme].**

---

## Header

**Statut :** ${statut}
**ID :** ${id}
**Class :** ${class}
**Cree :** ${date}
**Theme :** ${theme}
**Pense-bete source :** ${parent:-[lien vers le pense-bete parent]}

---

## 1. Objectif

[Quel est l'objectif precis de cette spec ? Qu'est-ce qu'elle doit permettre d'atteindre ?]

## 2. Contexte

### 2.1 Origine

[D'ou vient ce besoin ? Quel probleme ou opportunite a declenche cette spec ?]

### 2.2 Perimetre

[Que couvre cette spec ? Qu'est-ce qui est hors perimetre ?]

### 2.3 Public cible

[Qui utilise ou sera impacte par cette spec ?]

---

## 3. Exigences Fonctionnelles

### 3.1 Exigence [ID] -- [Titre]

| Champ | Description |
|---|---|
| **Priorite** | Haute / Moyenne / Basse |
| **Description** | [Description detaillee] |
| **Critere d'acceptation** | [Comment valider que l'exigence est remplie] |
| **Dependances** | [Liens vers d'autres exigences ou specs] |

*(Repeter pour chaque exigence)*

---

## 4. Exigences Non-Fonctionnelles

| Categorie | Exigence | Critere de mesure |
|---|---|---|
| **Performance** | [ex: temps de reponse < 200ms] | [methode de test] |
| **Securite** | [ex: authentification requise] | [critere de validation] |
| **Maintenabilite** | [ex: code testable a 80%] | [couverture de tests] |
| **Accessibilite** | [ex: WCAG 2.1 AA] | [outil de verification] |

---

## 5. Architecture / Structure Technique

### 5.1 Vue d'ensemble

[Description de l'architecture cible]

### 5.2 Composants

| Composant | Role | Dependances |
|---|---|---|
| [Nom] | [Description] | [Liens] |

### 5.3 Modele de donnees

[Si applicable - schema, entites, relations]

### 5.4 Interfaces / API

[Si applicable - points d'entree, contrats, formats]

### 5.5 Flux / Workflows

[Si applicable - sequences d'actions, etats, transitions]

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| [Description] | [Impact] | [Solution] |

### 6.2 Risques

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| [Description] | Elevee / Moyenne / Faible | Eleve / Moyen / Faible | [Solution] |

---

## 7. Livrables attendus

| Livrable | Format | Destination |
|---|---|---|
| [Ex: Code source] | [Repertoire, langage] | [Depot] |
| [Ex: Documentation] | [Markdown, PDF] | [Emplacement] |
| [Ex: Tests] | [Type de tests] | [Repertoire] |

---

## 8. Plan de validation

### 8.1 Criteres de succes globaux

- [ ] [Critere 1]
- [ ] [Critere 2]
- [ ] [Critere 3]

### 8.2 Methode de validation

[Ex: revue par les pairs, tests d'integration, demo fonctionnelle]

### 8.3 Responsables

| Role | Responsable |
|---|---|
| Redaction | [Nom / Role] |
| Validation technique | [Nom / Role] |
| Validation metier | [Nom / Role] |

---

## 9. Liens et References

### 9.1 Pense-bete source

- ${parent:-[lien vers le pense-bete parent]}

### 9.2 Specs connexes

- [Lien vers autres specs liees]

### 9.3 Conventions applicables

- [Lien vers conventions utilisees]

### 9.4 Regles immuables

- [Lien vers regles respectees]

### 9.5 References externes

- [Liens vers documentation, standards, etc.]

---

## 10. RVAV de la spec

- [rechercher] -- toutes les references, dependances externes rassemblees
- [verifier] -- la structure est complete (toutes les sections remplies)
- [analyser] -- la spec est coherente avec le cerveau existant et le pense-bete source
- [valider] -- pret pour le statut suivant (prepare)

---

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| ${date} | v0.1 | [Nom] | [Description du changement] |
EOF
}

# Main
main() {
    local theme=""
    local id="001"
    local class="01"
    local statut="ebauche"
    local dossier="spec"
    local parent=""
    local dry_run="false"
    local help="false"
    
    # Parser les arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --theme)
                theme="$2"
                shift 2
                ;;
            --id)
                id="$2"
                shift 2
                ;;
            --class)
                class="$2"
                shift 2
                ;;
            --statut)
                statut="$2"
                shift 2
                ;;
            --dossier)
                dossier="$2"
                shift 2
                ;;
            --parent)
                parent="$2"
                shift 2
                ;;
            --dry-run)
                dry_run="true"
                shift
                ;;
            --help)
                help="true"
                shift
                ;;
            *)
                echo -e "${RED}[ERREUR] Option inconnue : $1${NC}"
                afficher_aide
                exit 1
                ;;
        esac
    done
    
    # Afficher l'aide
    if [ "$help" = "true" ]; then
        afficher_aide
        exit 0
    fi
    
    # Verifier le theme obligatoire
    if [ -z "$theme" ]; then
        echo -e "${RED}[ERREUR] Le theme est obligatoire (--theme)${NC}"
        afficher_aide
        exit 1
    fi
    
    # Verifier le theme (pas d'accents, pas d'espaces)
    if echo "$theme" | grep -qE '[^a-z0-9-]'; then
        echo -e "${RED}[ERREUR] Le theme doit etre en minuscules sans accents ni espaces : $theme${NC}"
        exit 1
    fi
    
    # Nom du fichier selon convention-renommage : spec-[theme].[id].[class].[statut].md
    local nom_fichier="spec-${theme}.${id}.${class}.${statut}.md"
    local chemin_fichier="${dossier}/${nom_fichier}"
    
    # Generer le squelette
    local squelette=$(generer_squelette "$theme" "$id" "$class" "$statut" "$parent")
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} Squelette de : ${nom_fichier}"
        echo ""
        echo "$squelette"
        exit 0
    fi
    
    # Verifier que le fichier n'existe pas deja
    if [ -f "$chemin_fichier" ]; then
        echo -e "${RED}[ERREUR] Le fichier existe deja : ${chemin_fichier}${NC}"
        exit 1
    fi
    
    # Creer le dossier si necessaire
    mkdir -p "$dossier"
    
    # Creer le fichier
    echo "$squelette" > "$chemin_fichier"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK]${NC} Squelette cree : ${chemin_fichier}"
        exit 0
    else
        echo -e "${RED}[ERREUR] Impossible de creer le fichier${NC}"
        exit 1
    fi
}

# Executer
main "$@"
