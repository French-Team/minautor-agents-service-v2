# Outil -- Lister les Fonctions

**Categorie** : Explorer
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Lister toutes les fonctions d'un fichier donne.

---

## Utilisation

```
lister-fonctions(fichier="path/to/file.ts", type="all")
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `fichier` | string | Oui | Chemin du fichier a analyser |
| `type` | string | Non | Type de fonctions: "all", "export", "import" (defaut: "all") |

---

## Resultat

Retourne une liste de fonctions avec leurs signatures.

```markdown
## Resultat

### Fonctions exportees
- `functionA(param1: type, param2: type): returnType`
- `functionB(): void`

### Fonctions privees
- `helperFunction(): string`
```

---

## Exemples

### Exemple 1 -- Lister toutes les fonctions

```
lister-fonctions(fichier="agents/tools/lister/lister-fichiers/lister-fichiers.md")
```

**Resultat** :
- Fonctions trouvees dans le fichier Markdown (sections)

### Exemple 2 -- Lister les fonctions exportees

```
lister-fonctions(fichier="src/utils.ts", type="export")
```

---

## Dependances

- Aucune dependance externe
- Utilise l'analyse de syntaxe du langage cible

---

## Implementation

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
- Fonctionne avec differents langages (TS, JS, Python, etc.)
- Peut etre utilise pour generer de la documentation

---

