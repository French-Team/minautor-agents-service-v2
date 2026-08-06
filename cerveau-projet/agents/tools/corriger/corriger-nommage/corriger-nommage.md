# Outil — Corriger le Nommage

**Catégorie** : Corriger
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Corriger automatiquement le nommage des fichiers et dossiers.

---

## Utilisation

```
corriger-nommage(chemin=".", convention="kebab-case", dry-run=false)
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier à corriger |
| `convention` | string | Non | Convention de nommage (défaut: "kebab-case") |
| `dry-run` | boolean | Non | Si true, simule sans corriger (défaut: false) |

---

## Résultat

Retourne un rapport de correction.

```markdown
## Résultat

### Fichiers renommés
- Buffy.md -> buffy.md
- IndexCerveau.md -> index-cerveau.md

### Fichiers non renommés
- fichier-special.md -> Convention non applicable

### Statistiques
- Fichiers analysés : 20
- Renommés : 2
- Non renommés : 1
```

---

## Exemples

### Exemple 1 — Simuler les corrections

```
corriger-nommage(chemin=".", dry-run=true)
```

**Résultat** :
- 2 fichiers seraient renommés

### Exemple 2 — Corriger automatiquement

```
corriger-nommage(chemin=".", convention="kebab-case")
```

**Résultat** :
- 2 fichiers renommés avec succès

---

## Dépendances

- `valider-nommage` — Pour identifier les fichiers mal nommés
- `lister-fichiers` — Pour trouver les fichiers à corriger
- `lister-dossiers` — Pour trouver les dossiers à corriger
- `convention-renommage.md` — Pour connaître les règles de nommage

---

## Implémentation

### Dans le contexte du cerveau-projet

1. Utiliser `valider-nommage` pour identifier les fichiers mal nommés
2. Pour chaque fichier :
   - Appliquer la convention de nommage
   - Renommer le fichier
   - Mettre à jour les liens qui référencent ce fichier

### Algorithme de correction

```
1. Extraire le nom du fichier
2. Appliquer la convention :
   - kebab-case : minuscules, tirets
   - snake_case : minuscules, underscores
3. Si le nom change -> renommer
4. Mettre à jour les liens
```

---

## Notes

- Cet outil est essentiel pour maintenir la cohérence
- Utiliser `dry-run=true` avant de corriger
- Les renommages peuvent casser les liens

---

