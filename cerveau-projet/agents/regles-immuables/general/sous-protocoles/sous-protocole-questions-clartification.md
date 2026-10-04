---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Sous-Protocole -- Questions de Clarification
---

## Objectif

Obtenir toutes les informations necessaires pour demarrer un projet de maniere claire et complete.

---

## Prerequis

- L'utilisateur a demande a demarrer un nouveau projet
- L'agent est identifie et pret

---

## Questions a poser

### Categorie 1 -- Nom et objectif

| # | Question | Obligatoire | Objectif |
|---|---|---|---|
| 1.1 | **Quel est le nom du projet ?** | [OK] | Identifier le projet |
| 1.2 | **Quel est l'objectif principal ?** | [OK] | Comprendre le but |
| 1.3 | **Quel est le public cible ?** | [OK] | Comprendre les utilisateurs |
| 1.4 | **Quel est le perimetre ?** | [OK] | Delimiter le projet |

### Categorie 2 -- Fonctionnalites

| # | Question | Obligatoire | Objectif |
|---|---|---|---|
| 2.1 | **Quelles sont les fonctionnalites principales ?** | [OK] | Lister les features |
| 2.2 | **Quelles sont les fonctionnalites secondaires ?** | [NON] | Enrichir le projet |
| 2.3 | **Y a-t-il des contraintes techniques ?** | [OK] | Comprendre les limites |
| 2.4 | **Y a-t-il des dependances externes ?** | [NON] | Identifier les integrations |

### Categorie 3 -- Architecture

| # | Question | Obligatoire | Objectif |
|---|---|---|---|
| 3.1 | **Quel stack technique souhaitez-vous ?** | [OK] | Choisir les technologies |
| 3.2 | **Y a-t-il des preferences d'architecture ?** | [NON] | Structurer le projet |
| 3.3 | **Quel est le niveau de complexite attendu ?** | [OK] | Adapter l'approche |
| 3.4 | **Y a-t-il des exemples inspirants ?** | [NON] | S'inspirer |

### Categorie 4 -- Planning

| # | Question | Obligatoire | Objectif |
|---|---|---|---|
| 4.1 | **Quel est le delai souhaite ?** | [OK] | Planifier le travail |
| 4.2 | **Y a-t-il des jalons intermediaires ?** | [NON] | Decomposer le travail |
| 4.3 | **Quelle est la priorite par rapport aux autres projets ?** | [OK] | Ordonner le travail |
| 4.4 | **Y a-t-il des dependances externes ?** | [NON] | Identifier les blocages |

### Categorie 5 -- Livrables

| # | Question | Obligatoire | Objectif |
|---|---|---|---|
| 5.1 | **Quels sont les livrables attendus ?** | [OK] | Definir les outputs |
| 5.2 | **Quel format pour les livrables ?** | [OK] | Standardiser les outputs |
| 5.3 | **Y a-t-il des criteres de validation ?** | [OK] | Definir le succes |
| 5.4 | **Comment validera-t-on la reussite ?** | [OK] | Mesurer le succes |

---

## Processus de collecte

### Etape 1 -- Poser les questions

```
1. Poser les questions une par une
2. Attendre la reponse de l'utilisateur
3. Documenter chaque reponse
4. Poser des questions de suivi si necessaire
```

### Etape 2 -- Synthetiser

```
1. Lister toutes les reponses
2. Identifier les zones d'ombre
3. Poser des questions de clarification
4. Valider la synthese avec l'utilisateur
```

### Etape 3 -- Documenter

```
1. Creer un pense-bete avec les informations collectees
2. Creer une spec si necessaire
3. Creer un todo avec les etapes
4. Valider par RVAV
```

---

## Template de documentation

```markdown
# Informations du projet -- [Nom du projet]

## Nom et objectif
- **Nom** : [reponse]
- **Objectif** : [reponse]
- **Public cible** : [reponse]
- **Perimetre** : [reponse]

## Fonctionnalites
- **Principales** : [reponses]
- **Secondaires** : [reponses]
- **Contraintes techniques** : [reponses]
- **Dependances** : [reponses]

## Architecture
- **Stack technique** : [reponse]
- **Preferences** : [reponses]
- **Complexite** : [reponse]
- **Exemples** : [reponses]

## Planning
- **Delai** : [reponse]
- **Jalons** : [reponses]
- **Priorite** : [reponse]
- **Dependances** : [reponses]

## Livrables
- **Attendus** : [reponses]
- **Format** : [reponse]
- **Criteres** : [reponses]
- **Validation** : [reponse]
```

---

## Validation

Avant de valider les questions, verifier :

- [ ] Toutes les questions obligatoires sont posees
- [ ] Toutes les reponses sont documentees
- [ ] Les zones d'ombre sont identifiees
- [ ] La synthese est validee avec l'utilisateur

---

## Liens

- **Protocole parent** : `protocole-demarrer-projet.md`
- **Convention** : `convention-sous-protocoles.md`
- **Template** : `pense-betes/pense-bete-template.md`

---

*Sous-protocole conforme aux conventions du cerveau-projet*
