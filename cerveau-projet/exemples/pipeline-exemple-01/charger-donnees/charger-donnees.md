# charger-donnees

> **Fichier** : charger-donnees.md
> **Type** : fonction
> **Role** : Charger les données brutes
> **Convention** : convention-structures

---

## Objectif

Charger des données brutes (fictives pour cet exemple) et les stocker dans le classeur de variables.

## Entrée / Sortie

| Type | Variable | Description |
|---|---|---|
| **Entrée** | *(aucune)* | Pas d'entrée nécessaire |
| **Sortie** | `donnees-brutes` | Tableau de données brutes |

---

## Logique

```
1. Créer des données fictives (tableau d'objets)
2. Vérifier le schéma dans classeur-variables/schema/
3. Écrire la variable "donnees-brutes" dans le classeur
4. Ajouter une entrée dans l'historique
```

---

## Données fictives

```json
[
  {"id": 1, "nom": "Alice", "age": 25, "ville": "Paris"},
  {"id": 2, "nom": "Bob", "age": 30, "ville": "Lyon"},
  {"id": 3, "nom": "Charlie", "age": 35, "ville": "Marseille"},
  {"id": 4, "nom": "Diana", "age": 28, "ville": "Paris"},
  {"id": 5, "nom": "Eve", "age": 32, "ville": "Lyon"}
]
```

---

## Écriture dans le classeur

### Variable `donnees-brutes`

| Champ | Valeur |
|---|---|
| `id` | `"donnees-brutes-001"` |
| `valeur` | *(tableau ci-dessus)* |
| `source` | `"charger-donnees"` |
| `date_creation` | *(date actuelle)* |

### Historique

```markdown
## [DATE] — Écriture

- **Variable** : donnees-brutes
- **Ancienne valeur** : *(aucune)*
- **Nouvelle valeur** : *(tableau de 5 objets)*
- **Source** : charger-donnees
- **Raison** : Initialisation des données brutes
```

---

## Validation

Avant de valider cette fonction, vérifier :

- [ ] Les données sont au format attendu
- [ ] La variable est écrite dans le classeur
- [ ] L'historique est documenté
- [ ] Aucune dépendance directe avec d'autres fonctions

---

## Navigation

- **Parent** : [../index-pipeline.md](../index-pipeline.md)
- **Classeur** : [../../../classeur-variables/index-classeur.md](../../../classeur-variables/index-classeur.md)
- **Fonction suivante** : [../nettoyer-donnees/nettoyer-donnees.md](../nettoyer-donnees/nettoyer-donnees.md)

---

*Fonction conforme aux conventions du cerveau-projet*
