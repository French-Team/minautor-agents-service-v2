# Outil — Analyser les Dépendances

**Catégorie** : Analyser
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Analyser les dépendances entre les fichiers du projet.

---

## Utilisation

```
analyser-dependances(chemin=".", fichier="specific.md", direction="both")
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier à analyser |
| `fichier` | string | Non | Fichier spécifique à analyser (défaut: tous) |
| `direction` | string | Non | Direction: "imports", "exports", "both" (défaut: "both") |

---

## Résultat

Retourne un graphe de dépendances.

```markdown
## Résultat

### Dépendances de index-cerveau.md

#### Imports (ce qu'il utilise)
- conventions/renommage/convention-renommage.md
- conventions/structures/convention-structures.md
- regles-immuables/general/regles-emojis-ascii.md

#### Exports (ce qui l'utilise)
- demarrer.md
- agents/buffy/buffy.md

### Statistiques
- Fichiers analysés : 25
- Dépendances trouvées : 45
- Fichiers orphelins : 2
```

---

## Exemples

### Exemple 1 — Analyser toutes les dépendances

```
analyser-dependances(chemin=".")
```

**Résultat** :
- 45 dépendances trouvées
- 2 fichiers orphelins

### Exemple 2 — Analyser les dépendances d'un fichier

```
analyser-dependances(fichier="index-cerveau.md")
```

**Résultat** :
- 3 imports
- 2 exports

---

## Dépendances

- `lister-fichiers` — Pour trouver les fichiers a analyser

---

## Implémentation

### Commande bash equivalent

```bash
# Trouver les imports dans les fichiers .md
grep -rn "\[.*\](.*)" *.md

# Analyser les liens
grep -rn "^\[.*\]:.*" *.md
```

### Implementation

1. Utiliser `lister-fichiers` pour trouver tous les .md
2. Extraire les liens Markdown de chaque fichier
3. Construire le graphe de dependances
4. Identifier les fichiers orphelins

---

## Notes

- Cet outil est utile pour comprendre l'architecture
- Permet d'identifier les fichiers critiques
- Utile pour le refactoring et la maintenance

---

