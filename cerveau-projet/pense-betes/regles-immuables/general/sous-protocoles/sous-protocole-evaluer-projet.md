# Sous-Protocole — Évaluer un Projet
---

## Objectif

Obtenir un état complet du projet avant de le reprendre.

---

## Prérequis

- L'utilisateur a demandé à reprendre un projet existant
- L'agent est identifié et prêt

---

## Évaluations à effectuer

### Évaluation 1 — Structure

| # | Vérification | Critère | Action si échec |
|---|---|---|---|
| 1.1 | **Dossier principal existe** | Présent et accessible | Créer le dossier |
| 1.2 | **Fichiers de config** | Présents et corrects | Recréer les fichiers |
| 1.3 | **Structure de dossiers** | Conforme aux conventions | Réorganiser |
| 1.4 | **Fichiers d'entrée** | Présents et à jour | Mettre à jour |

### Évaluation 2 — Cerveau-projet

| # | Vérification | Critère | Action si échec |
|---|---|---|---|
| 2.1 | **index-cerveau.md** | Présent et à jour | Créer/mettre à jour |
| 2.2 | **demarrer.md** | Présent et à jour | Créer/mettre à jour |
| 2.3 | **Conventions** | Présentes et à jour | Créer/mettre à jour |
| 2.4 | **Règles** | Présentes et à jour | Créer/mettre à jour |
| 2.5 | **Protocoles** | Présents et à jour | Créer/mettre à jour |

### Évaluation 3 — Agents

| # | Vérification | Critère | Action si échec |
|---|---|---|---|
| 3.1 | **AGENTS.md** | Présent et à jour | Créer/mettre à jour |
| 3.2 | **Fiches d'agent** | Présentes et à jour | Créer/mettre à jour |
| 3.3 | **Corrections** | Présentes et à jour | Créer/mettre à jour |

### Évaluation 4 — Contenu

| # | Vérification | Critère | Action si échec |
|---|---|---|---|
| 4.1 | **Pense-bêtes** | Présents et à jour | Créer/mettre à jour |
| 4.2 | **Specs** | Présentes et à jour | Créer/mettre à jour |
| 4.3 | **Todos** | Présents et à jour | Créer/mettre à jour |

### Évaluation 5 — Cohérence

| # | Vérification | Critère | Action si échec |
|---|---|---|---|
| 5.1 | **Liens** | Tous valides | Corriger |
| 5.2 | **Références** | Toutes à jour | Mettre à jour |
| 5.3 | **Statuts** | Tous corrects | Corriger |
| 5.4 | **Historique** | Complet et à jour | Compléter |

---

## Processus d'évaluation

### Étape 1 — Explorer la structure

```
1. Lister les fichiers et dossiers
2. Identifier les éléments clés
3. Vérifier la structure de base
```

### Étape 2 — Lire les fichiers critiques

```
1. Lire index-cerveau.md
2. Lire demarrer.md
3. Lire AGENTS.md
4. Lire les conventions
```

### Étape 3 — Vérifier la cohérence

```
1. Vérifier les liens
2. Vérifier les références
3. Vérifier les statuts
4. Vérifier l'historique
```

### Étape 4 — Classifier le projet

| Cas | Description | Approche |
|---|---|---|
| **Fonctionnel** | Tout marche | Comprendre → Ajouter |
| **Incomplet** | Contenu manquant | Comprendre → Compléter |
| **Cassé** | Erreurs, bugs | Diagnostiquer → Corriger |
| **À refondre** | Architecture mauvaise | Analyser → Refondre |
| **Pause** | Reprise après absence | Évaluer → Continuer |

### Étape 5 — Documenter

```
1. Créer un rapport d'évaluation
2. Noter les problèmes détectés
3. Proposer des actions correctives
4. Valider avec l'utilisateur
```

---

## Template d'évaluation

```markdown
# Évaluation du projet — [Nom du projet]

## Structure
- [OK] Dossier principal : [état]
- [OK] Fichiers de config : [état]
- [OK] Structure : [état]
- [OK] Fichiers d'entrée : [état]

## Cerveau-projet
- [OK] index-cerveau.md : [état]
- [OK] demarrer.md : [état]
- [OK] Conventions : [état]
- [OK] Règles : [état]
- [OK] Protocoles : [état]

## Agents
- [OK] AGENTS.md : [état]
- [OK] Fiches : [état]
- [OK] Corrections : [état]

## Contenu
- [OK] Pense-bêtes : [état]
- [OK] Specs : [état]
- [OK] Todos : [état]

## Cohérence
- [OK] Liens : [état]
- [OK] Références : [état]
- [OK] Statuts : [état]
- [OK] Historique : [état]

## Classification
**Cas** : [Fonctionnel / Incomplet / Cassé / À refondre / Pause]

## Actions proposées
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

---

## Validation

Avant de valider l'évaluation, vérifier :

- [ ] Toutes les vérifications sont effectuées
- [ ] Le projet est classifié
- [ ] Les actions sont proposées
- [ ] L'utilisateur a validé

---

## Liens

- **Protocole parent** : `protocole-reprendre-projet.md`
- **Convention** : `convention-sous-protocoles.md`
- **Diagnostic** : `sous-protocole-diagnostic.md`

---

*Sous-protocole conforme aux conventions du cerveau-projet*
