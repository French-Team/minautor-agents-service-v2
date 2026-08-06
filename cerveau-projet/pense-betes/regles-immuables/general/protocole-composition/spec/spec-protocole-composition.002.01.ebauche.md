# Spec -- Protocole de Composition du Cerveau

**Statut :** ebauche
**ID :** 001
**Class :** 01
**Cree :** 2026-08-06
**Theme :** protocole-composition
**Pense-bete source :** [protocole-composition.001.01.ebauche.md](../protocole-composition.001.01.ebauche.md)

---

## 1. Objectif

Definir la spec technique du protocole de composition du cerveau-projet : comment creer le squelette de base (index, dossiers, templates) de maniere reproductible et validee.

---

## 2. Contexte

### 2.1 Origine

Le protocole composition a ete cree pour standardiser la creation du cerveau-projet afin que chaque nouveau projet demarre avec une structure identique et fiable.

### 2.2 Perimetre

Couvre : creation de l'index, des dossiers, des templates.
Hors perimetre : contenu des pense-betes, specs metier, outils.

### 2.3 Public cible

Buffy (developpeur principal) et tout agent creant un nouveau cerveau-projet.

---

## 3. Exigences Fonctionnelles

### 3.1 Exigence 1 -- Creer index-cerveau.md

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Creer le point d'entree avec titre, version, description et table des matieres |
| **Critere d'acceptation** | Le fichier existe et tous les liens pointent vers des fichiers existants |
| **Dependances** | convention-renommage |

### 3.2 Exigence 2 -- Creer la structure des dossiers

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Creer pense-betes/, conventions/, specs/, regles-immuables/, recherches-web/ |
| **Critere d'acceptation** | Aucun dossier n'est vide (au moins un index) |
| **Dependances** | convention-structures |

### 3.3 Exigence 3 -- Verifier les templates

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Verifier que pense-bete-template, spec-template, todo-template existent |
| **Critere d'acceptation** | Les 3 templates sont presents et suivent le pattern de nommage |
| **Dependances** | convention-renommage |

---

## 4. Exigences Non-Fonctionnelles

| Categorie | Exigence | Critere de mesure |
|---|---|---|
| **Reproductibilite** | Memes etapes = meme structure | Comparaison de deux executions |
| **Maintenabilite** | Structure extensible sans modification profonde | Ajout d'un dossier teste |
| **Coherence** | Respect des conventions de nommage | valider-nommage sans erreur |

---

## 5. Architecture / Structure Technique

### 5.1 Vue d'ensemble

Le protocole suit 3 etapes sequentielles, chacune validee par RVAV :
1. Creer index-cerveau.md
2. Creer la structure des dossiers
3. Verifier les templates

### 5.2 Composants

| Composant | Role | Dependances |
|---|---|---|
| index-cerveau.md | Point d'entree | tous les index |
| Dossiers | Organisation | convention-structures |
| Templates | Gabarits de creation | convention-renommage |

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| Nommage strict | Structure rigide | convention-renommage |
| Dossiers non vides | Temps de creation | Index generes |

### 6.2 Risques

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Liens casses | Moyenne | Eleve | valider-liens a chaque etape |
| Oubli de RVAV | Moyenne | Eleve | Checklist obligatoire |

---

## 7. Livrables attendus

| Livrable | Format | Destination |
|---|---|---|
| Squelette du cerveau | Dossiers + index | cerveau-projet/ |
| Templates | Markdown | pense-betes/ |

---

## 8. Plan de validation

### 8.1 Criteres de succes globaux

- [ ] Les 3 etapes sont executees dans l'ordre
- [ ] Chaque etape passe la boucle RVAV
- [ ] Aucun dossier vide restant

### 8.2 Methode de validation

Revue des fichiers crees + verification des liens.

---

## 9. Liens et References

### 9.1 Pense-bete source

- [protocole-composition.001.01.ebauche.md](../protocole-composition.001.01.ebauche.md)

### 9.2 Conventions applicables

- [convention-renommage.md](../../../conventions/renommage/convention-renommage.md)
- [convention-structures.md](../../../conventions/structures/convention-structures.md)

### 9.3 Regles immuables

- [rvav-workflow.md](../../rvav-workflow.md)

---

## 10. RVAV de la spec

- [rechercher] -- references rassemblees
- [verifier] -- structure complete
- [analyser] -- coherente avec le protocole source
- [valider] -- pret pour le statut suivant
