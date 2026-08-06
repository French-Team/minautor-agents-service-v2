# Outil — Analyser la Structure

**Catégorie** : Analyser
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Analyser et documenter la structure du projet.

---

## Utilisation

```
analyser-structure(chemin=".", profondeur=3, format="markdown")
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier à analyser |
| `profondeur` | number | Non | Profondeur d'analyse (défaut: 3) |
| `format` | string | Non | Format de sortie: "markdown", "json", "tree" (défaut: "markdown") |

---

## Résultat

Retourne une analyse de la structure.

```markdown
## Résultat

### Structure du projet

```
cerveau-projet/
|-- index-cerveau.md
|-- demarrer.md
|-- agents/
|   |-- buffy/
|   |   |-- buffy.md
|   |   `-- corrections.md
|   `-- atlas/
|       |-- atlas.md
|       `-- corrections.md
|-- conventions/
|   |-- renommage/
|   |-- structures/
|   |-- liens/
|   `-- protocoles/
`-- regles-immuables/
    |-- general/
    `-- hierarchie/
```

### Statistiques
- Dossiers : 25
- Fichiers : 45
- Taille totale : 2.5 MB
```

---

## Exemples

### Exemple 1 — Analyser la structure du projet

```
analyser-structure(chemin=".", profondeur=2)
```

**Résultat** :
- 25 dossiers
- 45 fichiers
- Structure hiérarchique documentée

### Exemple 2 — Analyser en format JSON

```
analyser-structure(chemin=".", format="json")
```

**Résultat** :
```json
{
  "nom": "cerveau-projet",
  "type": "dossier",
  "enfants": [
    {
      "nom": "agents",
      "type": "dossier",
      "enfants": [...]
    }
  ]
}
```

---

## Dépendances

- `lister-dossiers` — Pour explorer les dossiers
- `lister-fichiers` — Pour explorer les fichiers

---

## Implémentation

### Commande bash equivalent

```bash
# Afficher l'arborescence
tree -L 3

# Compter les fichiers et dossiers
find . -type d | wc -l  # Dossiers
find . -type f | wc -l  # Fichiers
```

### Implementation

1. Explorer le dossier specifie
2. Construire l'arborescence recursivement
3. Compter les fichiers et dossiers
4. Formater selon le format demande

---

## Notes

- Cet outil est utile pour documenter le projet
- Peut être utilisé pour générer des README
- Utile pour les revues de code

---

