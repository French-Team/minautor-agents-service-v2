# Sous-Protocole -- Evaluer un Projet
---

## Objectif

Obtenir un etat complet du projet avant de le reprendre.

---

## Prerequis

- L'utilisateur a demande a reprendre un projet existant
- L'agent est identifie et pret

---

## Evaluations a effectuer

### Evaluation 1 -- Structure

| # | Verification | Critere | Action si echec |
|---|---|---|---|
| 1.1 | **Dossier principal existe** | Present et accessible | Creer le dossier |
| 1.2 | **Fichiers de config** | Presents et corrects | Recreer les fichiers |
| 1.3 | **Structure de dossiers** | Conforme aux conventions | Reorganiser |
| 1.4 | **Fichiers d'entree** | Presents et a jour | Mettre a jour |

### Evaluation 2 -- Cerveau-projet

| # | Verification | Critere | Action si echec |
|---|---|---|---|
| 2.1 | **index-cerveau.md** | Present et a jour | Creer/mettre a jour |
| 2.2 | **demarrer.md** | Present et a jour | Creer/mettre a jour |
| 2.3 | **Conventions** | Presentes et a jour | Creer/mettre a jour |
| 2.4 | **Regles** | Presentes et a jour | Creer/mettre a jour |
| 2.5 | **Protocoles** | Presents et a jour | Creer/mettre a jour |

### Evaluation 3 -- Agents

| # | Verification | Critere | Action si echec |
|---|---|---|---|
| 3.1 | **AGENTS.md** | Present et a jour | Creer/mettre a jour |
| 3.2 | **Fiches d'agent** | Presentes et a jour | Creer/mettre a jour |
| 3.3 | **Corrections** | Presentes et a jour | Creer/mettre a jour |

### Evaluation 4 -- Contenu

| # | Verification | Critere | Action si echec |
|---|---|---|---|
| 4.1 | **Pense-betes** | Presents et a jour | Creer/mettre a jour |
| 4.2 | **Specs** | Presentes et a jour | Creer/mettre a jour |
| 4.3 | **Todos** | Presents et a jour | Creer/mettre a jour |

### Evaluation 5 -- Coherence

| # | Verification | Critere | Action si echec |
|---|---|---|---|
| 5.1 | **Liens** | Tous valides | Corriger |
| 5.2 | **References** | Toutes a jour | Mettre a jour |
| 5.3 | **Statuts** | Tous corrects | Corriger |
| 5.4 | **Historique** | Complet et a jour | Completer |

---

## Processus d'evaluation

### Etape 1 -- Explorer la structure

```
1. Lister les fichiers et dossiers
2. Identifier les elements cles
3. Verifier la structure de base
```

### Etape 2 -- Lire les fichiers critiques

```
1. Lire index-cerveau.md
2. Lire demarrer.md
3. Lire AGENTS.md
4. Lire les conventions
```

### Etape 3 -- Verifier la coherence

```
1. Verifier les liens
2. Verifier les references
3. Verifier les statuts
4. Verifier l'historique
```

### Etape 4 -- Classifier le projet

| Cas | Description | Approche |
|---|---|---|
| **Fonctionnel** | Tout marche | Comprendre -> Ajouter |
| **Incomplet** | Contenu manquant | Comprendre -> Completer |
| **Casse** | Erreurs, bugs | Diagnostiquer -> Corriger |
| **A refondre** | Architecture mauvaise | Analyser -> Refondre |
| **Pause** | Reprise apres absence | Evaluer -> Continuer |

### Etape 5 -- Documenter

```
1. Creer un rapport d'evaluation
2. Noter les problemes detectes
3. Proposer des actions correctives
4. Valider avec l'utilisateur
```

---

## Template d'evaluation

```markdown
# Evaluation du projet -- [Nom du projet]

## Structure
- [OK] Dossier principal : [etat]
- [OK] Fichiers de config : [etat]
- [OK] Structure : [etat]
- [OK] Fichiers d'entree : [etat]

## Cerveau-projet
- [OK] index-cerveau.md : [etat]
- [OK] demarrer.md : [etat]
- [OK] Conventions : [etat]
- [OK] Regles : [etat]
- [OK] Protocoles : [etat]

## Agents
- [OK] AGENTS.md : [etat]
- [OK] Fiches : [etat]
- [OK] Corrections : [etat]

## Contenu
- [OK] Pense-betes : [etat]
- [OK] Specs : [etat]
- [OK] Todos : [etat]

## Coherence
- [OK] Liens : [etat]
- [OK] References : [etat]
- [OK] Statuts : [etat]
- [OK] Historique : [etat]

## Classification
**Cas** : [Fonctionnel / Incomplet / Casse / A refondre / Pause]

## Actions proposees
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

---

## Validation

Avant de valider l'evaluation, verifier :

- [ ] Toutes les verifications sont effectuees
- [ ] Le projet est classifie
- [ ] Les actions sont proposees
- [ ] L'utilisateur a valide

---

## Liens

- **Protocole parent** : `protocole-reprendre-projet.md`
- **Convention** : `convention-sous-protocoles.md`
- **Diagnostic** : `sous-protocole-diagnostic.md`

---

*Sous-protocole conforme aux conventions du cerveau-projet*
