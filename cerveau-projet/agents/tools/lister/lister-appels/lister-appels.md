# Outil -- Lister les Appels

**Categorie** : Explorer
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Lister tous les appels de fonctions dans un fichier donne.

---

## Utilisation

```
lister-appels(fichier="path/to/file.ts", fonction="nomFonction")
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `fichier` | string | Oui | Chemin du fichier a analyser |
| `fonction` | string | Non | Nom d'une fonction specifique (defaut: toutes) |

---

## Resultat

Retourne une liste d'appels de fonctions.

```markdown
## Resultat

### Appels trouves
- Ligne 15: `autreFonction(param1, param2)`
- Ligne 23: `utilitaire.format(data)`
- Ligne 45: `this.methodePrivee()`
```

---

## Exemples

### Exemple 1 -- Lister tous les appels

```
lister-appels(fichier="src/main.ts")
```

**Resultat** :
- Ligne 10: `init()`
- Ligne 15: `processData(data)`
- Ligne 20: `save()`

### Exemple 2 -- Lister les appels d'une fonction specifique

```
lister-appels(fichier="src/main.ts", fonction="processData")
```

**Resultat** :
- Ligne 15: `processData(data)` -- appel principal
- Ligne 45: `processData(transformedData)` -- appel recursif

---

## Dependances

- Aucune dependance externe
- Utilise l'analyse de syntaxe du langage cible

---

## Implementation

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

- Cet outil est utile pour analyser les dependances
- Permet de tracer l'utilisation d'une fonction
- Utile pour le refactoring et la maintenance

---

