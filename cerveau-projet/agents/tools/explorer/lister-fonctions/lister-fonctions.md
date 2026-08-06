# Outil — Lister les Fonctions

**Catégorie** : Explorer
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Lister toutes les fonctions d'un fichier donné.

---

## Utilisation

```
lister-fonctions(fichier="path/to/file.ts", type="all")
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `fichier` | string | Oui | Chemin du fichier à analyser |
| `type` | string | Non | Type de fonctions: "all", "export", "import" (défaut: "all") |

---

## Résultat

Retourne une liste de fonctions avec leurs signatures.

```markdown
## Résultat

### Fonctions exportées
- `functionA(param1: type, param2: type): returnType`
- `functionB(): void`

### Fonctions privées
- `helperFunction(): string`
```

---

## Exemples

### Exemple 1 — Lister toutes les fonctions

```
lister-fonctions(fichier="agents/tools/explorer/lister-fichiers/lister-fichiers.md")
```

**Résultat** :
- Fonctions trouvées dans le fichier Markdown (sections)

### Exemple 2 — Lister les fonctions exportées

```
lister-fonctions(fichier="src/utils.ts", type="export")
```

---

## Dépendances

- Aucune dépendance externe
- Utilise l'analyse de syntaxe du langage cible

---

## Implémentation

### Commande bash equivalent

```bash
# Pour les fichiers TypeScript/JavaScript
grep -n "function\|const.*=\|export" fichier.ts

# Pour les fichiers Python
grep -n "def \|class " fichier.py
```

### Implementation

1. Lire le fichier specifie
2. Analyser la syntaxe du langage
3. Extraire les declarations de fonctions
4. Retourner la liste avec les signatures

---

## Notes

- Cet outil est utile pour comprendre la structure d'un fichier
- Fonctionne avec différents langages (TS, JS, Python, etc.)
- Peut être utilisé pour générer de la documentation

---

