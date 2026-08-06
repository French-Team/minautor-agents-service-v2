# Sous-Protocole — Questions de Clarification
---

## Objectif

Obtenir toutes les informations nécessaires pour démarrer un projet de manière claire et complète.

---

## Prérequis

- L'utilisateur a demandé à démarrer un nouveau projet
- L'agent est identifié et prêt

---

## Questions à poser

### Catégorie 1 — Nom et objectif

| # | Question | Obligatoire | Objectif |
|---|---|---|---|
| 1.1 | **Quel est le nom du projet ?** | [OK] | Identifier le projet |
| 1.2 | **Quel est l'objectif principal ?** | [OK] | Comprendre le but |
| 1.3 | **Quel est le public cible ?** | [OK] | Comprendre les utilisateurs |
| 1.4 | **Quel est le périmètre ?** | [OK] | Délimiter le projet |

### Catégorie 2 — Fonctionnalités

| # | Question | Obligatoire | Objectif |
|---|---|---|---|
| 2.1 | **Quelles sont les fonctionnalités principales ?** | [OK] | Lister les features |
| 2.2 | **Quelles sont les fonctionnalités secondaires ?** | [NON] | Enrichir le projet |
| 2.3 | **Y a-t-il des contraintes techniques ?** | [OK] | Comprendre les limites |
| 2.4 | **Y a-t-il des dépendances externes ?** | [NON] | Identifier les intégrations |

### Catégorie 3 — Architecture

| # | Question | Obligatoire | Objectif |
|---|---|---|---|
| 3.1 | **Quel stack technique souhaitez-vous ?** | [OK] | Choisir les technologies |
| 3.2 | **Y a-t-il des préférences d'architecture ?** | [NON] | Structurer le projet |
| 3.3 | **Quel est le niveau de complexité attendu ?** | [OK] | Adapter l'approche |
| 3.4 | **Y a-t-il des exemples inspirants ?** | [NON] | S'inspirer |

### Catégorie 4 — Planning

| # | Question | Obligatoire | Objectif |
|---|---|---|---|
| 4.1 | **Quel est le délai souhaité ?** | [OK] | Planifier le travail |
| 4.2 | **Y a-t-il des jalons intermédiaires ?** | [NON] | Décomposer le travail |
| 4.3 | **Quelle est la priorité par rapport aux autres projets ?** | [OK] | Ordonner le travail |
| 4.4 | **Y a-t-il des dépendances externes ?** | [NON] | Identifier les blocages |

### Catégorie 5 — Livrables

| # | Question | Obligatoire | Objectif |
|---|---|---|---|
| 5.1 | **Quels sont les livrables attendus ?** | [OK] | Définir les outputs |
| 5.2 | **Quel format pour les livrables ?** | [OK] | Standardiser les outputs |
| 5.3 | **Y a-t-il des critères de validation ?** | [OK] | Définir le succès |
| 5.4 | **Comment validera-t-on la réussite ?** | [OK] | Mesurer le succès |

---

## Processus de collecte

### Étape 1 — Poser les questions

```
1. Poser les questions une par une
2. Attendre la réponse de l'utilisateur
3. Documenter chaque réponse
4. Poser des questions de suivi si nécessaire
```

### Étape 2 — Synthétiser

```
1. Lister toutes les réponses
2. Identifier les zones d'ombre
3. Poser des questions de clarification
4. Valider la synthèse avec l'utilisateur
```

### Étape 3 — Documenter

```
1. Créer un pense-bête avec les informations collectées
2. Créer une spec si nécessaire
3. Créer un todo avec les étapes
4. Valider par RVAV
```

---

## Template de documentation

```markdown
# Informations du projet — [Nom du projet]

## Nom et objectif
- **Nom** : [réponse]
- **Objectif** : [réponse]
- **Public cible** : [réponse]
- **Périmètre** : [réponse]

## Fonctionnalités
- **Principales** : [réponses]
- **Secondaires** : [réponses]
- **Contraintes techniques** : [réponses]
- **Dépendances** : [réponses]

## Architecture
- **Stack technique** : [réponse]
- **Préférences** : [réponses]
- **Complexité** : [réponse]
- **Exemples** : [réponses]

## Planning
- **Délai** : [réponse]
- **Jalons** : [réponses]
- **Priorité** : [réponse]
- **Dépendances** : [réponses]

## Livrables
- **Attendus** : [réponses]
- **Format** : [réponse]
- **Critères** : [réponses]
- **Validation** : [réponse]
```

---

## Validation

Avant de valider les questions, vérifier :

- [ ] Toutes les questions obligatoires sont posées
- [ ] Toutes les réponses sont documentées
- [ ] Les zones d'ombre sont identifiées
- [ ] La synthèse est validée avec l'utilisateur

---

## Liens

- **Protocole parent** : `protocole-demarrer-projet.md`
- **Convention** : `convention-sous-protocoles.md`
- **Template** : `pense-betes/pense-bete-template.md`

---

*Sous-protocole conforme aux conventions du cerveau-projet*
