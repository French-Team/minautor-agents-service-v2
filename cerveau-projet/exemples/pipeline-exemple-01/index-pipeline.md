# Pipeline Exemple 01 — Test du Classeur de Variables

> **Objectif** : Démontrer l'utilisation du classeur de variables pour communiquer entre fonctions.
> **Statut** : ebauche
> **Version** : 001.01

---

## Objectif

Pipeline simple de traitement de données qui illustre :
- La communication via le classeur de variables
- L'indépendance des fonctions entre elles
- La facilité de réorganisation
- La traçabilité des données

---

## Architecture

```
charger-donnees → nettoyer-donnees → transformer-donnees → exporter-donnees
```

### Flux de données

```
1. charger-donnees → écrit "donnees-brutes" dans le classeur
2. nettoyer-donnees → lit "donnees-brutes" → écrit "donnees-propres"
3. transformer-donnees → lit "donnees-propres" → écrit "donnees-transformees"
4. exporter-donnees → lit "donnees-transformees" → écrit "fichier-final"
```

---

## Structure

```
pipeline-exemple-01/
├── index-pipeline.md              ← CE FICHIER (point d'entrée)
├── pipeline.md                    ← orchestrateur
├── charger-donnees/
│   └── charger-donnees.md         ← fonction de chargement
├── nettoyer-donnees/
│   └── nettoyer-donnees.md        ← fonction de nettoyage
├── transformer-donnees/
│   └── transformer-donnees.md     ← fonction de transformation
└── exporter-donnees/
    └── exporter-donnees.md        ← fonction d'export
```

---

## Utilisation

### Exécuter le pipeline

```
1. Lire cet index pour comprendre le pipeline
2. Lire pipeline.md pour voir l'orchestration
3. Lire chaque fonction dans l'ordre
4. Vérifier le classeur de variables pour voir les données
```

### Réorganiser le pipeline

```
1. Ouvrir pipeline.md
2. Modifier l'ordre des appels de fonctions
3. Tester le nouveau flux
4. Valider par RVAV
```

---

## Variables utilisées

| Variable | Type | Source | Description |
|---|---|---|---|
| `donnees-brutes` | array | charger-donnees | Données brutes chargées |
| `donnees-propres` | array | nettoyer-donnees | Données nettoyées |
| `donnees-transformees` | array | transformer-donnees | Données transformées |
| `fichier-final` | string | exporter-donnees | Chemin du fichier exporté |

---

## Documents

| Document | Description |
|---|---|
| [index-pipeline.md](index-pipeline.md) | Ce fichier (point d'entrée) |
| [pipeline.md](pipeline.md) | Orchestrateur du pipeline |
| [simulation-execution.md](simulation-execution.md) | Simulation de l'exécution |

## Navigation

- **Parent** : [../../index-cerveau.md](../../index-cerveau.md)
- **Classeur** : [../../classeur-variables/index-classeur.md](../../classeur-variables/index-classeur.md)
- **Convention** : [../../agents/conventions/structures/convention-classeur-variables.md](../../agents/conventions/structures/convention-classeur-variables.md)

---

*Pipeline conforme aux conventions du cerveau-projet*
