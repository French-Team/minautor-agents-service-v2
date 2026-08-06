# classeur-variables

<!-- 
  Fichier: classeur-variables.md
  Type: orchestrateur
  Role: Orchestrateur principal du classeur de variables
  Convention: convention-classeur-variables
  Version: 001.01
  Statut: ebauche
-->

## Objectif

Point d'entree unique pour lire et ecrire dans le classeur de variables.

## Utilisation

```
classeur-variables/
├── index-classeur.md           <- point d'entree global
├── classeur-variables.md       <- CE FICHIER (orchestrateur)
├── schema/
│   └── variables-definition.md <- definition des variables
└── [variable]/
    └── [variable].md           <- implementation
```

## Operations

| Operation | Description |
|---|---|
| `lire(nom)` | Lire la valeur d'une variable |
| `ecrire(nom, valeur)` | Ecrire une nouvelle valeur |
| `modifier(nom, transformation)` | Modifier une valeur existante |
| `supprimer(nom)` | Supprimer une variable |
| `lister()` | Lister toutes les variables |

## Regles

| Regle | Principe |
|---|---|
| **R1** | Chaque variable a un nom unique |
| **R2** | Chaque variable a un schema defini |
| **R3** | Lecture et ecriture standardisees |
| **R4** | Pas de modification directe hors classeur |

## Variables courantes

| Variable | Type | Description |
|---|---|---|
| `statut-mission` | string | Statut actuel de la mission |
| `contexte` | object | Contexte de la mission en cours |
| `resultats` | object | Resultats des traitements precedents |
| `erreurs` | array | Liste des erreurs rencontrees |

## Propagation

Apres chaque operation, le classeur met a jour :
- Le schema si necessaire
- Les dependances
- L'historique des modifications

---

*Orchestrateur conforme a convention-classeur-variables*
