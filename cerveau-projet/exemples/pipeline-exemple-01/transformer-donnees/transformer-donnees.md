# transformer-donnees

> **Fichier** : transformer-donnees.md
> **Type** : fonction
> **Role** : Transformer les données nettoyées
> **Convention** : convention-structures

---

## Objectif

Lire les données nettoyées du classeur, les transformer (ajouter des champs calculés), et écrire le résultat dans le classeur.

## Entrée / Sortie

| Type | Variable | Description |
|---|---|---|
| **Entrée** | `donnees-propres` | Données nettoyées à transformer |
| **Sortie** | `donnees-transformees` | Données transformées |

---

## Logique

```
1. Lire la variable "donnees-propres" du classeur
2. Vérifier que la variable existe
3. Transformer les données :
   - Ajouter un champ "tranche_age" (jeune/adulte/senior)
   - Ajouter un champ "initiales" (premières lettres du nom)
   - Formater la date de transformation
4. Écrire la variable "donnees-transformees" dans le classeur
5. Ajouter une entrée dans l'historique
```

---

## Règles de transformation

| Règle | Description |
|---|---|
| **Tranche d'âge** | < 30 : "jeune", 30-50 : "adulte", > 50 : "senior" |
| **Initiales** | Première lettre de chaque mot du nom |
| **Date** | Format ISO 8601 |

---

## Exemple de transformation

**Avant (donnees-propres) :**
```json
[
  {"id": 1, "nom": "Alice", "age": 25, "ville": "Paris"},
  {"id": 2, "nom": "Bob", "age": 30, "ville": "Lyon"}
]
```

**Après (donnees-transformees) :**
```json
[
  {
    "id": 1,
    "nom": "Alice",
    "age": 25,
    "ville": "Paris",
    "tranche_age": "jeune",
    "initiales": "A",
    "date_transformation": "2026-08-04T12:00:00Z"
  },
  {
    "id": 2,
    "nom": "Bob",
    "age": 30,
    "ville": "Lyon",
    "tranche_age": "adulte",
    "initiales": "B",
    "date_transformation": "2026-08-04T12:00:00Z"
  }
]
```

---

## Écriture dans le classeur

### Variable `donnees-transformees`

| Champ | Valeur |
|---|---|
| `id` | `"donnees-transformees-001"` |
| `valeur` | *(tableau transformé)* |
| `source` | `"transformer-donnees"` |
| `date_creation` | *(date actuelle)* |

### Historique

```markdown
## [DATE] — Écriture

- **Variable** : donnees-transformees
- **Ancienne valeur** : *(aucune)*
- **Nouvelle valeur** : *(tableau transformé)*
- **Source** : transformer-donnees
- **Raison** : Transformation des données nettoyées
```

---

## Validation

Avant de valider cette fonction, vérifier :

- [ ] La variable `donnees-propres` existe dans le classeur
- [ ] Les données sont correctement transformées
- [ ] La variable `donnees-transformees` est écrite dans le classeur
- [ ] L'historique est documenté
- [ ] Aucune dépendance directe avec d'autres fonctions

---

## Navigation

- **Parent** : [../index-pipeline.md](../index-pipeline.md)
- **Classeur** : [../../../classeur-variables/index-classeur.md](../../../classeur-variables/index-classeur.md)
- **Fonction précédente** : [../nettoyer-donnees/nettoyer-donnees.md](../nettoyer-donnees/nettoyer-donnees.md)
- **Fonction suivante** : [../exporter-donnees/exporter-donnees.md](../exporter-donnees/exporter-donnees.md)

---

*Fonction conforme aux conventions du cerveau-projet*
