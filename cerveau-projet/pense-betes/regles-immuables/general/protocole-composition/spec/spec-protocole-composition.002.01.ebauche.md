# Spec — Protocole de Composition du Cerveau

**Statut :** ebauche
**ID :** 001
**Class :** 01
**Créé :** 2026-08-06
**Thème :** protocole-composition
**Pense-bête source :** [protocole-composition.001.01.ebauche.md](../protocole-composition.001.01.ebauche.md)

---

## 1. Objectif

Définir la spec technique du protocole de composition du cerveau-projet : comment créer le squelette de base (index, dossiers, templates) de manière reproductible et validée.

---

## 2. Contexte

### 2.1 Origine

Le protocole composition a été créé pour standardiser la création du cerveau-projet afin que chaque nouveau projet démarre avec une structure identique et fiable.

### 2.2 Périmètre

Couvre : création de l'index, des dossiers, des templates.
Hors périmètre : contenu des pense-betes, specs métier, outils.

### 2.3 Public cible

Buffy (développeur principal) et tout agent créant un nouveau cerveau-projet.

---

## 3. Exigences Fonctionnelles

### 3.1 Exigence 1 — Créer index-cerveau.md

| Champ | Description |
|---|---|
| **Priorité** | Haute |
| **Description** | Créer le point d'entrée avec titre, version, description et table des matières |
| **Critère d'acceptation** | Le fichier existe et tous les liens pointent vers des fichiers existants |
| **Dépendances** | convention-renommage |

### 3.2 Exigence 2 — Créer la structure des dossiers

| Champ | Description |
|---|---|
| **Priorité** | Haute |
| **Description** | Créer pense-betes/, conventions/, specs/, regles-immuables/, recherches-web/ |
| **Critère d'acceptation** | Aucun dossier n'est vide (au moins un index) |
| **Dépendances** | convention-structures |

### 3.3 Exigence 3 — Vérifier les templates

| Champ | Description |
|---|---|
| **Priorité** | Moyenne |
| **Description** | Vérifier que pense-bete-template, spec-template, todo-template existent |
| **Critère d'acceptation** | Les 3 templates sont présents et suivent le pattern de nommage |
| **Dépendances** | convention-renommage |

---

## 4. Exigences Non-Fonctionnelles

| Catégorie | Exigence | Critère de mesure |
|---|---|---|
| **Reproductibilité** | Mêmes étapes = même structure | Comparaison de deux exécutions |
| **Maintenabilité** | Structure extensible sans modification profonde | Ajout d'un dossier testé |
| **Cohérence** | Respect des conventions de nommage | valider-nommage sans erreur |

---

## 5. Architecture / Structure Technique

### 5.1 Vue d'ensemble

Le protocole suit 3 étapes séquentielles, chacune validée par RVAV :
1. Créer index-cerveau.md
2. Créer la structure des dossiers
3. Vérifier les templates

### 5.2 Composants

| Composant | Rôle | Dépendances |
|---|---|---|
| index-cerveau.md | Point d'entrée | tous les index |
| Dossiers | Organisation | convention-structures |
| Templates | Gabarits de création | convention-renommage |

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| Nommage strict | Structure rigide | convention-renommage |
| Dossiers non vides | Temps de création | Index générés |

### 6.2 Risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Liens cassés | Moyenne | Élevé | valider-liens à chaque étape |
| Oubli de RVAV | Moyenne | Élevé | Checklist obligatoire |

---

## 7. Livrables attendus

| Livrable | Format | Destination |
|---|---|---|
| Squelette du cerveau | Dossiers + index | cerveau-projet/ |
| Templates | Markdown | pense-betes/ |

---

## 8. Plan de validation

### 8.1 Critères de succès globaux

- [ ] Les 3 étapes sont exécutées dans l'ordre
- [ ] Chaque étape passe la boucle RVAV
- [ ] Aucun dossier vide restant

### 8.2 Méthode de validation

Revue des fichiers créés + vérification des liens.

---

## 9. Liens et Références

### 9.1 Pense-bête source

- [protocole-composition.001.01.ebauche.md](../protocole-composition.001.01.ebauche.md)

### 9.2 Conventions applicables

- [convention-renommage.md](../../../conventions/renommage/convention-renommage.md)
- [convention-structures.md](../../../conventions/structures/convention-structures.md)

### 9.3 Règles immuables

- [rvav-workflow.md](../../rvav-workflow.md)

---

## 10. RVAV de la spec

- [rechercher] — références rassemblées
- [vérifier] — structure complète
- [analyser] — cohérente avec le protocole source
- [valider] — prêt pour le statut suivant
