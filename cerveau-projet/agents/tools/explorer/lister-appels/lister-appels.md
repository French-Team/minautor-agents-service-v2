# Outil — Lister les Appels

**Catégorie** : Explorer
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Lister tous les appels de fonctions dans un fichier donné.

---

## Utilisation

```
lister-appels(fichier="path/to/file.ts", fonction="nomFonction")
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `fichier` | string | Oui | Chemin du fichier à analyser |
| `fonction` | string | Non | Nom d'une fonction spécifique (défaut: toutes) |

---

## Résultat

Retourne une liste d'appels de fonctions.

```markdown
## Résultat

### Appels trouvés
- Ligne 15: `autreFonction(param1, param2)`
- Ligne 23: `utilitaire.format(data)`
- Ligne 45: `this.methodePrivee()`
```

---

## Exemples

### Exemple 1 — Lister tous les appels

```
lister-appels(fichier="src/main.ts")
```

**Résultat** :
- Ligne 10: `init()`
- Ligne 15: `processData(data)`
- Ligne 20: `save()`

### Exemple 2 — Lister les appels d'une fonction spécifique

```
lister-appels(fichier="src/main.ts", fonction="processData")
```

**Résultat** :
- Ligne 15: `processData(data)` — appel principal
- Ligne 45: `processData(transformedData)` — appel récursif

---

## Dépendances

- Aucune dépendance externe
- Utilise l'analyse de syntaxe du langage cible

---

## Implémentation

### Commande bash equivalent

```bash
# Pour les fichiers TypeScript/JavaScript
grep -n "fonction(" fichier.ts

# Pour les fichiers Python
grep -n "fonction(" fichier.py
```

### Implementation

1. Lire le fichier specifie
2. Analyser la syntaxe du langage
3. Extraire les appels de fonctions
4. Retourner la liste avec les positions

---

## Notes

- Cet outil est utile pour analyser les dépendances
- Permet de tracer l'utilisation d'une fonction
- Utile pour le refactoring et la maintenance

---

