# Outil — Lister les Fichiers

**Catégorie** : Explorer
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Lister tous les fichiers d'un chemin donné.

---

## Utilisation

```
lister-fichiers(chemin=".", pattern="*", recursif=false)
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier à explorer |
| `pattern` | string | Non | Pattern de filtrage (défaut: "*") |
| `recursif` | boolean | Non | Si true, explore les sous-dossiers (défaut: false) |

---

## Résultat

Retourne une liste de chemins de fichiers.

```markdown
## Résultat

- fichier1.md
- fichier2.md
- sous-dossier/fichier3.md
```

---

## Exemples

### Exemple 1 — Lister tous les fichiers .md

```
lister-fichiers(chemin=".", pattern="*.md")
```

**Résultat** :
- index-cerveau.md
- demarrer.md
- agents/buffy/buffy.md
- ...

### Exemple 2 — Lister les fichiers recursivement

```
lister-fichiers(chemin=".", pattern="*.md", recursif=true)
```

---

## Dépendances

- Aucune dépendance externe
- Utilise les outils du système de fichiers

---

## Implémentation

### Commande bash equivalent

```bash
# Lister les fichiers .md
find . -name "*.md" -type f

# Lister tous les fichiers
find . -type f
```

### Implementation

1. Parcourir le dossier specifie
2. Appliquer le pattern de filtrage
3. Retourner la liste des fichiers correspondants

---

## Notes

- Cet outil est utilisé pour trouver des fichiers spécifiques
- Le pattern accepte les wildcards (*, ?)
- Utile pour valider la structure du projet

---

