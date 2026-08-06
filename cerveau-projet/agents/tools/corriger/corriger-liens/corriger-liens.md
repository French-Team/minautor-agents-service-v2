# Outil — Corriger les Liens

**Catégorie** : Corriger
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Corriger automatiquement les liens cassés dans les fichiers Markdown.

---

## Utilisation

```
corriger-liens(chemin=".", mode="auto", dry-run=false)
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier à corriger |
| `mode` | string | Non | Mode: "auto" (automatique), "manual" (manuel) (défaut: "auto") |
| `dry-run` | boolean | Non | Si true, simule sans corriger (défaut: false) |

---

## Résultat

Retourne un rapport de correction.

```markdown
## Résultat

### Liens corrigés
- [ancien.md](ancien.md) -> [nouveau.md](nouveau.md)
- dossier/ -> dossier/existant/

### Liens non corrigés
- [perdu.md](perdu.md) -> Aucune correspondance trouvée

### Statistiques
- Liens analysés : 15
- Corrigés : 3
- Non corrigés : 1
```

---

## Exemples

### Exemple 1 — Simuler les corrections

```
corriger-liens(chemin=".", dry-run=true)
```

**Résultat** :
- 3 liens seraient corrigés

### Exemple 2 — Corriger automatiquement

```
corriger-liens(chemin=".", mode="auto")
```

**Résultat** :
- 3 liens corrigés avec succès

---

## Dépendances

- `valider-liens` — Pour identifier les liens cassés
- `lister-fichiers` — Pour trouver les fichiers à corriger
- `lister-dossiers` — Pour trouver les dossiers disponibles

---

## Implémentation

### Dans le contexte du cerveau-projet

1. Utiliser `valider-liens` pour identifier les liens cassés
2. Pour chaque lien cassé :
   - Chercher un fichier avec un nom similaire
   - Vérifier si le fichier existe
   - Si oui, corriger le lien
   - Si non, signaler l'erreur

### Algorithme de correction

```
1. Extraire le chemin cible du lien
2. Si le chemin existe -> OK
3. Sinon :
   a. Chercher dans le dossier parent
   b. Chercher par nom相似
   c. Si trouvé -> corriger
   d. Sinon -> signaler
```

---

## Notes

- Cet outil est essentiel pour la maintenance
- Utiliser `dry-run=true` avant de corriger
- Les corrections sont irréversibles

---

