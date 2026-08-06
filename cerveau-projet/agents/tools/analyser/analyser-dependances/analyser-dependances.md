# Outil -- Analyser les Dependances

**Categorie** : Analyser
**Version** : 0.2.0
**Statut** : prepare

---

## Objectif

Analyser les dependances entre les fichiers du projet.

---

## Utilisation

```
analyser-dependances(chemin=".", fichier="specific.md", direction="both")
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier a analyser |
| `fichier` | string | Non | Fichier specifique a analyser (defaut: tous) |
| `direction` | string | Non | Direction: "imports", "exports", "both" (defaut: "both") |

---

## Resultat

Retourne un graphe de dependances.

```markdown
## Resultat

### Dependances de index-cerveau.md

#### Imports (ce qu'il utilise)
- conventions/renommage/convention-renommage.md
- conventions/structures/convention-structures.md
- regles-immuables/general/regles-emojis-ascii.md

#### Exports (ce qui l'utilise)
- demarrer.md
- agents/buffy/buffy.md

### Statistiques
- Fichiers analyses : 25
- Dependances trouvees : 45
- Fichiers orphelins : 2
```

---

## Exemples

### Exemple 1 -- Analyser toutes les dependances

```
analyser-dependances(chemin=".")
```

**Resultat** :
- 45 dependances trouvees
- 2 fichiers orphelins

### Exemple 2 -- Analyser les dependances d'un fichier

```
analyser-dependances(fichier="index-cerveau.md")
```

**Resultat** :
- 3 imports
- 2 exports

---

## Dependances

- `lister-fichiers` -- Pour trouver les fichiers a analyser

---

## Implementation

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

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels, corrections, promotion |
