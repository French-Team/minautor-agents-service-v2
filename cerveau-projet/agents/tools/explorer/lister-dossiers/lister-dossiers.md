# Outil — Lister les Dossiers

**Catégorie** : Explorer
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Lister tous les dossiers d'un chemin donné.

---

## Utilisation

### Script bash

```bash
./lister-dossiers.sh [OPTIONS] [CHEMIN]
```

### Options

| Option | Description |
|---|---|
| `--aide, -h` | Afficher l'aide |
| `--recursif, -r` | Explorer les sous-dossiers |
| `--version` | Afficher la version |

### Arguments

| Argument | Description |
|---|---|
| `CHEMIN` | Chemin du dossier (défaut: .) |

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier à explorer |
| `recursif` | boolean | Non | Si true, explore les sous-dossiers (défaut: false) |

---

## Résultat

Retourne une liste de chemins de dossiers.

```markdown
## Résultat

- dossier1/
- dossier2/
  - sous-dossier1/
  - sous-dossier2/
- dossier3/
```

---

## Exemples

### Exemple 1 — Lister les dossiers du répertoire courant

```bash
./lister-dossiers.sh
```

**Résultat** :
- cerveau-projet/
- cerveau-projet/agents/
- cerveau-projet/agents/tools/
- examples/

### Exemple 2 — Lister les dossiers recursivement

```bash
./lister-dossiers.sh --recursif
```

**Résultat** :
- agents/
- agents/buffy/
- agents/atlas/
- cerveau-projet/
- cerveau-projet/pense-betes/
- ...

---

## Dépendances

- Aucune dépendance externe
- Utilise les outils du système de fichiers

---

## Implémentation

### Commande bash equivalent

```bash
# Lister les dossiers (non récursif)
ls -d */

# Lister les dossiers (récursif)
find . -type d
```

### Implementation

1. Parcourir le dossier specifie
2. Identifier les sous-dossiers
3. Si recursif, repeter pour chaque sous-dossier
4. Retourner la liste des dossiers

---

## Notes

- Cet outil est utilisé pour explorer la structure du projet
- Utile avant de créer de nouveaux fichiers ou dossiers
- Peut être combiné avec `lister-fichiers` pour une vue complète

---

