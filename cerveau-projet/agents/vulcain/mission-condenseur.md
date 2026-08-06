# Mission — Outil de Condensation Markdown

**Agent** : Vulcain
**Date** : 2026-08-05
**Statut** : En cours

---

## Objectif

Créer un outil `condenseur.sh` qui réduit la taille des fichiers markdown en fusionnant les éléments similaires.

---

## Problème à résoudre

Le purificateur fait un bon travail de nettoyage, mais ne peut pas :
- Fusionner les tables similaires
- Réduire les sections répétitives
- Condenser le frontmatter

---

## Fonctionnalités requises

### 1. Analyser un fichier

```bash
condenseur.sh --analyser [fichier]
```

**Résultat** :
```
Fichier : buffy.md
Lignes : 368
Problèmes détectés :
- Frontmatter : 106 lignes (peut être réduit à ~30)
- Tables similaires : 5 tables de missions (peuvent être fusionnées)
- Sections répétitives : 3 sections avec le même format
```

### 2. Condenser un fichier (dry-run)

```bash
condenseur.sh --dry-run [fichier]
```

**Résultat** :
```
=== Condensation de buffy.md ===

[CONDENSÉ] Frontmatter : 106 → 30 lignes (-76)
[FUSIONNÉ] 5 tables de missions → 1 table (-40)
[RÉDUIT] Sections répétitives : 3 → 1 (-20)

Résumé :
- Avant : 368 lignes
- Après : 232 lignes
- Économie : 136 lignes (37%)
```

### 3. Appliquer la condensation

```bash
condenseur.sh [fichier]
```

---

## Règles de condensation

### Règle 1 — Frontmatter

**Avant** :
```yaml
---
# Fiche d'Agent — Buffy
# Agent principal — Développeur du cerveau-projet

agent:
  nom: "buffy"
  version: "0.2.0"
  cree: "2026-08-04"
  statut: "disponible"  # disponible | en-attente | archivee
  role_principal: true  # agent principal du cerveau-projet

# Profil de l'agent
profil:
  role: "Agent principal — développe et maintient le cerveau-projet avec l'utilisateur"
  specialites:
    - "Développement du cerveau-projet (fichiers principaux)"
    - "Gestion des agents (fichies, corrections, AGENTS.md)"
    - "Création de pense-betes > specs > todos"
    - "Architecture et structures de données"
    - "Conventions et standards"
  ...
```

**Après** :
```yaml
---
agent:
  nom: "buffy"
  version: "0.2.0"
  role: "Agent principal"
  specialites: "Développement, Agents, Contenu"
---
```

### Règle 2 — Tables similaires

**Avant** :
```markdown
### Mission : Créer un fichier
| Étape | Action | Protocole |
|---|---|---|
| 1 | Vérifier le nommage | convention-renommage |
| 2 | Vérifier la structure | convention-structures |
| 3 | Créer le fichier | - |
| 4 | Mettre à jour l'index | - |

### Mission : Modifier un fichier
| Étape | Action | Protocole |
|---|---|---|
| 1 | Lire le fichier | - |
| 2 | Vérifier les dépendances | regles-veracite |
| 3 | Modifier le fichier | - |
```

**Après** :
```markdown
### Missions

| Mission | Étapes | Protocoles |
|---|---|---|
| Créer un fichier | 4 | convention-renommage, convention-structures |
| Modifier un fichier | 3 | regles-veracite |
```

### Règle 3 — Sections répétitives

**Avant** :
```markdown
## Spécialités

### Développement du cerveau-projet
- Créer des fichiers
- Modifier des fichiers
- Valider les conventions

### Gestion des agents
- Créer des agents
- Modifier des agents
- Valider les agents

### Création de contenu
- Créer des pense-betes
- Créer des specs
- Créer des todos
```

**Après** :
```markdown
## Spécialités

Développement du cerveau-projet, Gestion des agents, Création de contenu
```

---

## Critères de validation

- [ ] L'outil détecte correctement les problèmes
- [ ] Le dry-run montre exactement ce qui sera changé
- [ ] La condensation est réversible (backup)
- [ ] Le résultat est lisible
- [ ] L'outil est documenté

---

## Livrables

1. `condenseur.sh` — dans `agents/tools/corriger/condenseur/`
2. `condenseur.md` — documentation
3. Tests avec `buffy.md` et `protocole-versionning-outils.md`
