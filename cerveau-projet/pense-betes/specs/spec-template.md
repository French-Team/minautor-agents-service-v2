# Gabarit — Spécification Technique (source de vérité)
---

## Header

```
**Statut :** ebauche | préparé | dev | test | valide
**ID :** 001
**Class :** 01
**Créé :** 2026-08-04
**Thème :** [nom-du-theme]
**Pense-bête source :** [lien vers le pense-bête parent]
```

---

## 1. Objectif

[Quel est l'objectif précis de cette spec ? Qu'est-ce qu'elle doit permettre d'atteindre ?]

[Format : phrase claire, concise, sans ambiguïté]

---

## 2. Contexte

### 2.1 Origine

[D'où vient ce besoin ? Quel problème ou opportunité a déclenché cette spec ?]

### 2.2 Périmètre

[Que couvre cette spec ? Qu'est-ce qui est hors périmètre ?]

### 2.3 Public cible

[Qui utilise ou sera impacté par cette spec ? (utilisateurs, développeurs, système)]

---

## 3. Exigences Fonctionnelles

[Décrire les fonctionnalités concrètes que la spec doit couvrir]

### 3.1 Exigence [ID] — [Titre]

| Champ | Description |
|---|---|
| **Priorité** | Haute / Moyenne / Basse |
| **Description** | [Description détaillée] |
| **Critère d'acceptation** | [Comment valider que l'exigence est remplie] |
| **Dépendances** | [Liens vers d'autres exigences ou specs] |

*(Répéter pour chaque exigence)*

---

## 4. Exigences Non-Fonctionnelles

[Contraintes techniques, performance, sécurité, maintenabilité, etc.]

| Catégorie | Exigence | Critère de mesure |
|---|---|---|
| **Performance** | [ex: temps de réponse < 200ms] | [méthode de test] |
| **Sécurité** | [ex: authentification requise] | [critère de validation] |
| **Maintenabilité** | [ex: code testable à 80%] | [couverture de tests] |
| **Accessibilité** | [ex: WCAG 2.1 AA] | [outil de vérification] |
| **Autre** | [ex: compatible mobile] | [critère] |

---

## 5. Architecture / Structure Technique

### 5.1 Vue d'ensemble

[Description de l'architecture cible — comment les éléments s'assemblent]

### 5.2 Composants

| Composant | Rôle | Dépendances |
|---|---|---|
| [Nom] | [Description] | [Liens] |

### 5.3 Modèle de données

[Si applicable — schéma, entités, relations]

### 5.4 Interfaces / API

[Si applicable — points d'entrée, contrats, formats]

### 5.5 Flux / Workflows

[Si applicable — séquences d'actions, états, transitions]

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| [Description] | [Impact] | [Solution] |

### 6.2 Risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| [Description] | Élevée / Moyenne / Faible | Élevé / Moyen / Faible | [Solution] |

---

## 7. Livrables attendus

[Quels livrables concrets cette spec doit-elle générer ?]

| Livrable | Format | Destination |
|---|---|---|
| [Ex: Code source] | [Répertoire, langage] | [Dépôt] |
| [Ex: Documentation] | [Markdown, PDF] | [Emplacement] |
| [Ex: Tests] | [Type de tests] | [Répertoire] |

---

## 8. Plan de validation

[Comment cette spec sera-t-elle validée ?]

### 8.1 Critères de succès globaux

- [ ] [Critère 1]
- [ ] [Critère 2]
- [ ] [Critère 3]

### 8.2 Méthode de validation

[Ex: revue par les pairs, tests d'intégration, démo fonctionnelle]

### 8.3 Responsables

| Rôle | Responsable |
|---|---|
| Rédaction | [Nom / Rôle] |
| Validation technique | [Nom / Rôle] |
| Validation métier | [Nom / Rôle] |

---

## 9. Liens et Références

### 9.1 Pense-bête source

- [Lien vers le pense-bête parent]

### 9.2 Specs connexes

- [Lien vers autres specs liées]

### 9.3 Conventions applicables

- [Lien vers conventions utilisées]

### 9.4 Règles immuables

- [Lien vers règles respectées]

### 9.5 Références externes

- [Liens vers documentation, standards, etc.]

---

## 10. RVAV de la spec

- [rechercher] — toutes les références, dépendances externes rassemblées
- [vérifier] — la structure est complète (toutes les sections remplies)
- [analyser] — la spec est cohérente avec le cerveau existant et le pense-bête source
- [valider] — prêt pour le statut suivant (`préparé`)
---

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| [Date] | [v0.1] | [Nom] | [Description du changement] |
