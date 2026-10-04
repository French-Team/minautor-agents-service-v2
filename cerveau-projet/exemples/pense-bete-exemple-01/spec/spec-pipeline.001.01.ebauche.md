# Spec — Concept de Pipeline

> **Spécification technique du pattern architectural pipeline.**

---

## Objectif technique

Définir comment les pipelines fonctionnent et comment ils sont utilisés dans le cerveau-projet.

---

## Architecture

```
pipeline/
├── index-pipeline.md              ← point d'entrée global
├── pipeline.md                    ← orchestrateur
├── fonction-1/
│   └── fonction-1.md             ← première fonction
├── fonction-2/
│   └── fonction-2.md             ← deuxième fonction
└── fonction-3/
    └── fonction-3.md             ← troisième fonction
```

---

## Données d'entrée

| Donnée | Source | Obligatoire |
|---|---|---|
| Variables à traiter | `classeur-variables/` | [OK] |
| Fonctions à exécuter | Dossiers du pipeline | [OK] |
| Ordre d'exécution | `pipeline.md` | [OK] |

---

## Données de sortie

| Donnée | Destination | Format |
|---|---|---|
| Résultats | `classeur-variables/` | Variables |
| Historique | `classeur-variables/historique/` | Entrées |

---

## Algorithme

```markdown
1. LIRE pipeline.md (orchestrateur)
2. POUR CHAQUE fonction dans l'ordre :
   a. LIRE les variables nécessaires du classeur
   b. EXÉCUTER la fonction
   c. ÉCRIRE les résultats dans le classeur
   d. AJOUTER une entrée dans l'historique
3. VALIDER le résultat final
```

---

## Contraintes

| Contrainte | Description |
|---|---|
| **Dé-couplage** | Les fonctions ne se connaissent pas |
| **Communication** | Uniquement via le classeur de variables |
| **Traçabilité** | Chaque opération est documentée |
| **Réorganisation** | Modifier l'ordre des appels change le flux |

---

## Tests

| Test | Critère |
|---|---|
| **Test de flux** | Le pipeline s'exécute dans l'ordre |
| **Test de communication** | Les variables sont correctement passées |
| **Test de réorganisation** | Changer l'ordre fonctionne |
| **Test de traçabilité** | L'historique est complet |

---

## Navigation

- **Parent** : [pense-bete-pipeline.001.01.ebauche.md](../pense-bete-pipeline.001.01.ebauche.md)
- **Todo** : [todo-pipeline.001.01.ebauche.md](todo-pipeline.001.01.ebauche.md)

---

*Spécification conforme aux conventions du cerveau-projet*
