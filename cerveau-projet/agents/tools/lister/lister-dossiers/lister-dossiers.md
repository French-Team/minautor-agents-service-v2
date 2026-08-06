# Outil -- Lister les Dossiers

**Categorie** : Explorer
**Version :** 0.2.0
**Statut :** prepare

---

## Objectif

Lister tous les dossiers d'un chemin donne.

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
| `CHEMIN` | Chemin du dossier (defaut: .) |

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier a explorer |
| `recursif` | boolean | Non | Si true, explore les sous-dossiers (defaut: false) |

---

## Resultat

Retourne une liste de chemins de dossiers.

```markdown
## Resultat

- dossier1/
- dossier2/
  - sous-dossier1/
  - sous-dossier2/
- dossier3/
```

---

## Exemples

### Exemple 1 -- Lister les dossiers du repertoire courant

```bash
./lister-dossiers.sh
```

**Resultat** :
- cerveau-projet/
- cerveau-projet/agents/
- cerveau-projet/agents/tools/
- examples/

### Exemple 2 -- Lister les dossiers recursivement

```bash
./lister-dossiers.sh --recursif
```

**Resultat** :
- agents/
- agents/buffy/
- agents/atlas/
- cerveau-projet/
- cerveau-projet/pense-betes/
- ...

---

## Dependances

- Aucune dependance externe
- Utilise les outils du systeme de fichiers

---

## Implementation

### Commande bash equivalent

```bash
# Lister les dossiers (non recursif)
ls -d */

# Lister les dossiers (recursif)
find . -type d
```

### Implementation

1. Parcourir le dossier specifie
2. Identifier les sous-dossiers
3. Si recursif, repeter pour chaque sous-dossier
4. Retourner la liste des dossiers

---

## Notes

- Cet outil est utilise pour explorer la structure du projet
- Utile avant de creer de nouveaux fichiers ou dossiers
- Peut etre combine avec `lister-fichiers` pour une vue complete

---

