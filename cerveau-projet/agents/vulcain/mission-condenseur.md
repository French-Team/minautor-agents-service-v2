---
identite:
  type: note
  appartient_a: vulcain
  commun: true
---
# Mission -- Outil de Condensation Markdown

**Agent** : Vulcain
**Date** : 2026-08-05
**Statut** : En cours

---

## Objectif

Creer un outil `condenseur.sh` qui reduit la taille des fichiers markdown en fusionnant les elements similaires.

---

## Probleme a resoudre

Le purificateur fait un bon travail de nettoyage, mais ne peut pas :
- Fusionner les tables similaires
- Reduire les sections repetitives
- Condenser le frontmatter

---

## Fonctionnalites requises

### 1. Analyser un fichier

```bash
condenseur.sh --analyser [fichier]
```

**Resultat** :
```
Fichier : buffy.md
Lignes : 368
Problemes detectes :
- Frontmatter : 106 lignes (peut etre reduit a ~30)
- Tables similaires : 5 tables de missions (peuvent etre fusionnees)
- Sections repetitives : 3 sections avec le meme format
```

### 2. Condenser un fichier (dry-run)

```bash
condenseur.sh --dry-run [fichier]
```

**Resultat** :
```
=== Condensation de buffy.md ===

[CONDENSE] Frontmatter : 106 -> 30 lignes (-76)
[FUSIONNE] 5 tables de missions -> 1 table (-40)
[REDUIT] Sections repetitives : 3 -> 1 (-20)

Resume :
- Avant : 368 lignes
- Apres : 232 lignes
- Economie : 136 lignes (37%)
```

### 3. Appliquer la condensation

```bash
condenseur.sh [fichier]
```

---

## Regles de condensation

### Regle 1 -- Frontmatter

**Avant** :
```yaml
---
# Fiche d'Agent -- Buffy
# Agent principal -- Developpeur du cerveau-projet

agent:
  nom: "buffy"
  version: "0.2.0"
  cree: "2026-08-04"
  statut: "disponible"  # disponible | en-attente | archivee
  role_principal: true  # agent principal du cerveau-projet

# Profil de l'agent
profil:
  role: "Agent principal -- developpe et maintient le cerveau-projet avec l'utilisateur"
  specialites:
    - "Developpement du cerveau-projet (fichiers principaux)"
    - "Gestion des agents (fichies, corrections, AGENTS.md)"
    - "Creation de pense-betes > specs > todos"
    - "Architecture et structures de donnees"
    - "Conventions et standards"
  ...
```

**Apres** :
```yaml
---
agent:
  nom: "buffy"
  version: "0.2.0"
  role: "Agent principal"
  specialites: "Developpement, Agents, Contenu"
---
```

### Regle 2 -- Tables similaires

**Avant** :
```markdown
### Mission : Creer un fichier
| Etape | Action | Protocole |
|---|---|---|
| 1 | Verifier le nommage | convention-renommage |
| 2 | Verifier la structure | convention-structures |
| 3 | Creer le fichier | - |
| 4 | Mettre a jour l'index | - |

### Mission : Modifier un fichier
| Etape | Action | Protocole |
|---|---|---|
| 1 | Lire le fichier | - |
| 2 | Verifier les dependances | regles-veracite |
| 3 | Modifier le fichier | - |
```

**Apres** :
```markdown
### Missions

| Mission | Etapes | Protocoles |
|---|---|---|
| Creer un fichier | 4 | convention-renommage, convention-structures |
| Modifier un fichier | 3 | regles-veracite |
```

### Regle 3 -- Sections repetitives

**Avant** :
```markdown
## Specialites

### Developpement du cerveau-projet
- Creer des fichiers
- Modifier des fichiers
- Valider les conventions

### Gestion des agents
- Creer des agents
- Modifier des agents
- Valider les agents

### Creation de contenu
- Creer des pense-betes
- Creer des specs
- Creer des todos
```

**Apres** :
```markdown
## Specialites

Developpement du cerveau-projet, Gestion des agents, Creation de contenu
```

---

## Criteres de validation

- [ ] L'outil detecte correctement les problemes
- [ ] Le dry-run montre exactement ce qui sera change
- [ ] La condensation est reversible (backup)
- [ ] Le resultat est lisible
- [ ] L'outil est documente

---

## Livrables

1. `condenseur.sh` -- dans `agents/tools/corriger/condenseur/`
2. `condenseur.md` -- documentation
3. Tests avec `buffy.md` et `protocole-versionning-outils.md`
