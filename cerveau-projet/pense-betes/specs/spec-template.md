---
identite:
  type: template
  appartient_a: commun
  commun: true
---
# Gabarit -- Specification Technique (source de verite)
---

## Header

```
**Statut :** ebauche | prepare | dev | test | valide
**ID :** 001
**Class :** 01
**Cree :** 2026-08-04
**Theme :** [nom-du-theme]
**Pense-bete source :** [lien vers le pense-bete parent]
```

---

## 1. Objectif

[Quel est l'objectif precis de cette spec ? Qu'est-ce qu'elle doit permettre d'atteindre ?]

[Format : phrase claire, concise, sans ambiguite]

---

## 2. Contexte

### 2.1 Origine

[D'ou vient ce besoin ? Quel probleme ou opportunite a declenche cette spec ?]

### 2.2 Perimetre

[Que couvre cette spec ? Qu'est-ce qui est hors perimetre ?]

### 2.3 Public cible

[Qui utilise ou sera impacte par cette spec ? (utilisateurs, developpeurs, systeme)]

---

## 3. Exigences Fonctionnelles

[Decrire les fonctionnalites concretes que la spec doit couvrir]

### 3.1 Exigence [ID] -- [Titre]

| Champ | Description |
|---|---|
| **Priorite** | Haute / Moyenne / Basse |
| **Description** | [Description detaillee] |
| **Critere d'acceptation** | [Comment valider que l'exigence est remplie] |
| **Dependances** | [Liens vers d'autres exigences ou specs] |

*(Repeter pour chaque exigence)*

---

## 4. Exigences Non-Fonctionnelles

[Contraintes techniques, performance, securite, maintenabilite, etc.]

| Categorie | Exigence | Critere de mesure |
|---|---|---|
| **Performance** | [ex: temps de reponse < 200ms] | [methode de test] |
| **Securite** | [ex: authentification requise] | [critere de validation] |
| **Maintenabilite** | [ex: code testable a 80%] | [couverture de tests] |
| **Accessibilite** | [ex: WCAG 2.1 AA] | [outil de verification] |
| **Autre** | [ex: compatible mobile] | [critere] |

---

## 5. Architecture / Structure Technique

### 5.1 Vue d'ensemble

[Description de l'architecture cible -- comment les elements s'assemblent]

### 5.2 Composants

| Composant | Role | Dependances |
|---|---|---|
| [Nom] | [Description] | [Liens] |

### 5.3 Modele de donnees

[Si applicable -- schema, entites, relations]

### 5.4 Interfaces / API

[Si applicable -- points d'entree, contrats, formats]

### 5.5 Flux / Workflows

[Si applicable -- sequences d'actions, etats, transitions]

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| [Description] | [Impact] | [Solution] |

### 6.2 Risques

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| [Description] | Elevee / Moyenne / Faible | Eleve / Moyen / Faible | [Solution] |

---

## 7. Livrables attendus

[Quels livrables concrets cette spec doit-elle generer ?]

| Livrable | Format | Destination |
|---|---|---|
| [Ex: Code source] | [Repertoire, langage] | [Depot] |
| [Ex: Documentation] | [Markdown, PDF] | [Emplacement] |
| [Ex: Tests] | [Type de tests] | [Repertoire] |

---

## 8. Plan de validation

[Comment cette spec sera-t-elle validee ?]

### 8.1 Criteres de succes globaux

- [ ] [Critere 1]
- [ ] [Critere 2]
- [ ] [Critere 3]

### 8.2 Methode de validation

[Ex: revue par les pairs, tests d'integration, demo fonctionnelle]

### 8.3 Responsables

| Role | Responsable |
|---|---|
| Redaction | [Nom / Role] |
| Validation technique | [Nom / Role] |
| Validation metier | [Nom / Role] |

---

## 9. Liens et References

### 9.1 Pense-bete source

- [Lien vers le pense-bete parent]

### 9.2 Specs connexes

- [Lien vers autres specs liees]

### 9.3 Conventions applicables

- [Lien vers conventions utilisees]

### 9.4 Regles immuables

- [Lien vers regles respectees]

### 9.5 References externes

- [Liens vers documentation, standards, etc.]

---

## 10. RVAV de la spec

- [rechercher] -- toutes les references, dependances externes rassemblees
- [verifier] -- la structure est complete (toutes les sections remplies)
- [analyser] -- la spec est coherente avec le cerveau existant et le pense-bete source
- [valider] -- pret pour le statut suivant (`prepare`)
---

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| [Date] | [v0.1] | [Nom] | [Description du changement] |
