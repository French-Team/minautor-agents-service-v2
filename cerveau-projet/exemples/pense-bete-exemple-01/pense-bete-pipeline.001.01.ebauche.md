# Pense-bête — Concept de Pipeline

**Statut :** ebauche
**ID :** 001
**Class :** 01
**Créé :** 2026-08-04
**Thème :** pipeline

---

## 1. Idée (1-2 phrases)

Le pipeline est un pattern architectural qui permet de composer des fonctions de manière dé-couplée, en utilisant le classeur de variables pour la communication entre fonctions.

---

## 2. Problème / Question

Comment communiquer entre fonctions sans les coupler directement ? Comment réorganiser facilement l'ordre d'exécution sans modifier le code des fonctions ?

---

## 3. Contexte

Ce pense-bête s'inscrit dans le développement du cerveau-projet. Il fait suite à la création du classeur de variables et de la convention-pipelines.

**Liens** :
- `index-cerveau.md` — point d'entrée du cerveau
- `pense-betes/index-pense-bete.md` — index des pense-bêtes
- `classeur-variables/index-classeur.md` — classeur de variables
- `agents/conventions/structures/convention-pipelines.md` — convention pipelines

---

## 4. Liens

- **Pense-bêtes connexes** : Aucun pour le moment
- **Conventions applicables** :
  - `convention-structures.md` — principes d'architecture
  - `convention-classeur-variables.md` — stockage partagé
  - `convention-pipelines.md` — pipelines de traitement
- **Règles immuables** :
  - `regles-hierarchie-par-niveau.md` — hiérarchie des niveaux
  - `rvav-workflow.md` — workflow RVAV

---

## 5. Structure prévue (RVAV par sous-partie)

| Sous-partie | Fichier cible | Statut | RVAV |
|---|---|---|---|
| Idée | `pense-bete-pipeline.001.01.ebauche.md` | ebauche | [X] recherche [OK] |
| Spec | `spec/spec-pipeline.001.01.ebauche.md` | — | à créer |
| Todo | `spec/todo/todo-pipeline.001.01.ebauche.md` | — | à créer |
| Liens | `liens/liens-pipeline.001.01.ebauche.md` | — | à créer |

---

## 6. RVAV du pense-bête

- [X] rechercher -- toutes les références/liens externes sont rassemblés
- [X] vérifier -- la structure (idée + problème + contexte + liens) est complète
- [X] analyser -- l'idée est cohérente avec le cerveau existant (pas de doublon)
- [ ] valider -- prêt pour le statut suivant (`préparé`)

---

## 7. Exemple concret

Un pipeline exemple a été créé dans `examples/pipeline-exemple-01/` pour illustrer le concept.

**Structure** :
```
pipeline-exemple-01/
├── index-pipeline.md
├── pipeline.md
├── simulation-execution.md
├── charger-donnees/
├── nettoyer-donnees/
├── transformer-donnees/
└── exporter-donnees/
```

**Flux** :
```
charger-donnees → nettoyer-donnees → transformer-donnees → exporter-donnees
```

**Communication via le classeur** :
```
1. charger-donnees → écrit "donnees-brutes"
2. nettoyer-donnees → lit "donnees-brutes" → écrit "donnees-propres"
3. transformer-donnees → lit "donnees-propres" → écrit "donnees-transformees"
4. exporter-donnees → lit "donnees-transformees" → écrit "fichier-final"
```

---

## 8. Prochaines étapes

- [ ] Créer la spec technique
- [ ] Créer le todo
- [ ] Créer les liens
- [ ] Valider par RVAV
- [ ] Passer au statut `préparé`

---

*Pense-bête conforme aux conventions du cerveau-projet*
