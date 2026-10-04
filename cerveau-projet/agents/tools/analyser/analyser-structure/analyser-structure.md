---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# analyser-structure

**Categorie** : Analyser
**Version** : 0.2.0
**Statut** : prepare

---

## Objectif

Analyser et documenter la structure du projet.

---

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 analyser-structure.py [chemin] [options]

Options :
  --profondeur N      Profondeur de l'arborescence (defaut: 3)
  --dry-run           Afficher sans executer
  --verbose           Affichage detaille
  --version           Afficher la version
```

### API (version originale)

```
analyser-structure(chemin=".", profondeur=3, format="markdown")
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier a analyser |
| `profondeur` | number | Non | Profondeur d'analyse (defaut: 3) |
| `format` | string | Non | Format de sortie: "markdown", "json", "tree" (defaut: "markdown") |

---

## Resultat

Retourne une analyse de la structure.

```markdown
## Resultat

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

### Exemple 1 -- Analyser la structure du projet

```
analyser-structure(chemin=".", profondeur=2)
```

**Resultat** :
- 25 dossiers
- 45 fichiers
- Structure hierarchique documentee

### Exemple 2 -- Analyser en format JSON

```
analyser-structure(chemin=".", format="json")
```

**Resultat** :
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

## Dependances

- `lister-dossiers` -- Pour explorer les dossiers
- `lister-fichiers` -- Pour explorer les fichiers

---

## Implementation

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
- Peut etre utilise pour generer des README
- Utile pour les revues de code

---

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py) |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels, corrections, promotion |
