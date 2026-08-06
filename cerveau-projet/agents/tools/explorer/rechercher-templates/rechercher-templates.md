# rechercher-templates

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Explorer
**Chemin :** `agents/tools/explorer/rechercher-templates/`

## Description

Rechercher les fichiers template dans le projet. Un template est un fichier modele qui sert de reference pour creer d'autres fichiers du meme type (fiche d'agent, spec, todo, outil, pense-bete, etc.).

## Utilisation

```bash
# Rechercher par nom (defaut) dans le dossier courant
rechercher-templates.sh

# Rechercher dans un dossier specifique
rechercher-templates.sh cerveau-projet/

# Rechercher dans le contenu des fichiers
rechercher-templates.sh --mode contenu cerveau-projet/

# Combiner tous les modes de detection
rechercher-templates.sh --tous cerveau-projet/

# Avec details
rechercher-templates.sh --verbose cerveau-projet/
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--mode <nom\|frontmatter\|contenu>` | Mode de detection | nom |
| `--tous` | Combiner tous les modes | false |
| `--extensions` | Extensions a chercher | md |
| `--exclure` | Dossiers a exclure | .git,node_modules,.agents |
| `--verbose` | Afficher les details de detection | false |
| `--help` | Afficher l'aide | - |

## Modes de detection

| Mode | Critere | Exemple |
|---|---|---|
| **nom** | Le nom du fichier contient "template" | `spec-template.md`, `fiche-agent-template.md` |
| **frontmatter** | Le fichier a un frontmatter `---` avec des placeholders | Fichiers YAML avec `[nom-agent]` |
| **contenu** | Le contenu mentionne template/modele/placeholder | Fichiers qui referencent un template |

## Ce que l'outil fait

1. **Scan** - Trouve tous les fichiers des extensions specifiees
2. **Detecte** - Applique le mode de detection choisi
3. **Classe** - Separe les templates des autres fichiers
4. **Rapporte** - Liste les templates trouves avec la raison de detection

## Exemples de sortie

```bash
$ rechercher-templates.sh --tous cerveau-projet/

=== Recherche de templates ===
Dossier : cerveau-projet/
Mode : tous
Extensions : md

  [TEMPLATE] cerveau-projet/agents/corrections-template.md
  [TEMPLATE] cerveau-projet/agents/fiche-agent-template.md
  [TEMPLATE] cerveau-projet/agents/tools/tests/template-test.md
  [TEMPLATE] cerveau-projet/pense-betes/pense-bete-template.md
  [TEMPLATE] cerveau-projet/pense-betes/specs/spec-template.md
  [TEMPLATE] cerveau-projet/pense-betes/specs/todo/todo-template.md
  [TEMPLATE] cerveau-projet/recherches-web/templates/recherche-template.md

=== Resume ===
Fichiers trouves : 169
Templates detectes : 7
Fichiers non-templates : 162
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Audit des templates** | Verifier quels templates existent dans le projet |
| **Avant creation** | Verifier si un template existe deja avant d'en creer un |
| **Controle de coherence** | S'assurer que les templates sont a jour avec les evolutions |
| **Revoir un template** | Localiser rapidement tous les templates pour les comparer |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `lister-outils` | Voir les outils, dont le template-test |
| `valider-conformite-ascii` | Verifier la conformite ASCII des templates |
| `rechercher-fichiers-vides` | Verifier qu'aucun template n'est vide |
| `verifier-surcharge-fichier` | Detecter les templates qui grossissent trop |
