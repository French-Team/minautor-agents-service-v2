# nettoyer-donnees

> **Fichier** : nettoyer-donnees.md
> **Type** : fonction
> **Role** : Nettoyer les données brutes
> **Convention** : convention-structures

---

## Objectif

Lire les données brutes du classeur, les nettoyer (supprimer les doublons, formater), et écrire le résultat dans le classeur.

## Entrée / Sortie

| Type | Variable | Description |
|---|---|---|
| **Entrée** | `donnees-brutes` | Données brutes à nettoyer |
| **Sortie** | `donnees-propres` | Données nettoyées |

---

## Logique

```
1. Lire la variable "donnees-brutes" du classeur
2. Vérifier que la variable existe
3. Nettoyer les données :
   - Supprimer les doublons (par id)
   - Formater les noms (première lettre en majuscule)
   - Valider les âges (entiers positifs)
4. Écrire la variable "donnees-propres" dans le classeur
5. Ajouter une entrée dans l'historique
```

---

## Règles de nettoyage

| Règle | Description |
|---|---|
| **Doublons** | Supprimer les entrées avec le même `id` |
| **Noms** | Première lettre en majuscule, le reste en minuscule |
| **Âges** | Doivent être des entiers positifs |
| **Villes** | Première lettre en majuscule |

---

## Exemple de nettoyage

**Avant (donnees-brutes) :**
```json
[
  {"id": 1, "nom": "alice", "age": 25, "ville": "paris"},
  {"id": 1, "nom": "Alice", "age": 25, "ville": "Paris"},
  {"id": 2, "nom": "bob", "age": 30, "ville": "lyon"}
]
```

**Après (donnees-propres) :**
```json
[
  {"id": 1, "nom": "Alice", "age": 25, "ville": "Paris"},
  {"id": 2, "nom": "Bob", "age": 30, "ville": "Lyon"}
]
```

---

## Écriture dans le classeur

### Variable `donnees-propres`

| Champ | Valeur |
|---|---|
| `id` | `"donnees-propres-001"` |
| `valeur` | *(tableau nettoyé)* |
| `source` | `"nettoyer-donnees"` |
| `date_creation` | *(date actuelle)* |

### Historique

```markdown
## [DATE] — Écriture

- **Variable** : donnees-propres
- **Ancienne valeur** : *(aucune)*
- **Nouvelle valeur** : *(tableau nettoyé)*
- **Source** : nettoyer-donnees
- **Raison** : Nettoyage des données brutes
```

---

## Validation

Avant de valider cette fonction, vérifier :

- [ ] La variable `donnees-brutes` existe dans le classeur
- [ ] Les données sont correctement nettoyées
- [ ] La variable `donnees-propres` est écrite dans le classeur
- [ ] L'historique est documenté
- [ ] Aucune dépendance directe avec d'autres fonctions

---

## Navigation

- **Parent** : [../index-pipeline.md](../index-pipeline.md)
- **Classeur** : [../../../classeur-variables/index-classeur.md](../../../classeur-variables/index-classeur.md)
- **Fonction précédente** : [../charger-donnees/charger-donnees.md](../charger-donnees/charger-donnees.md)
- **Fonction suivante** : [../transformer-donnees/transformer-donnees.md](../transformer-donnees/transformer-donnees.md)

---

*Fonction conforme aux conventions du cerveau-projet*
