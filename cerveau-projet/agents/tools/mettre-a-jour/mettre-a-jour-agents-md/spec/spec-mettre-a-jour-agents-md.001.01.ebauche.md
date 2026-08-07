# Specification -- mettre-a-jour-agents-md

**Statut :** prepare
**ID :** 001
**Class :** 01
**Cree :** 2026-08-05
**Theme :** mettre-a-jour-agents-md
**Pense-bete source :** Spec directe (pas de pense-bete parent)

---

## 1. Objectif

Modifier le fichier `AGENTS.md` de maniere fiable et standardisee lors de l'activation ou de la reactivation d'un agent, en mettant a jour la section Agent Principal Actuel et l'historique.

---

## 2. Contexte

### 2.1 Origine

Le cycle du cerveau-projet impose que chaque agent reactive Cerberus a la fin de sa mission (coordinateur > agent > coordinateur). Cette reactivation se fait via la modification de `AGENTS.md`. Sans outil dedie, chaque agent modifiait le fichier manuellement avec des risques d'incoherence (format, historique, erreurs).

### 2.2 Perimetre

**Couvert** : activation (mettre un agent comme principal), reactivation (remettre Cerberus), mise a jour de l'historique, journalisation dans `AGENTS-historique.md`.

**Hors perimetre** : modification d'autres fichiers du cerveau, creation de fiches agents.

### 2.3 Public cible

Tous les agents du cerveau-projet, principalement Cerberus (coordinateur) et les agents actives en mission.

---

## 3. Exigences Fonctionnelles

### 3.1 Exigence 01 -- Activer un agent

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Remplace l'agent principal actuel par l'agent nomme dans la section Agent Principal Actuel |
| **Critere d'acceptation** | Le nom, le role et la fiche de l'agent sont correctement mis a jour |
| **Dependances** | Fichier `AGENTS.md` lisible et ecrivable |

### 3.2 Exigence 02 -- Reactiver Cerberus

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Remet Cerberus comme agent principal (appel a la fin de chaque mission) |
| **Critere d'acceptation** | Cerberus est de nouveau declare principal dans AGENTS.md |
| **Dependances** | Exigence 01 |

### 3.3 Exigence 03 -- Journaliser dans l'historique

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Ajoute une entree datee (AAAA-MM-JJ HH:MM) dans l'historique, limite a 150 interventions, ordre decroissant |
| **Critere d'acceptation** | L'entree est presente en haut, la limite de 150 est respectee |
| **Dependances** | Exigence 01, fichier `AGENTS-historique.md` |

### 3.4 Exigence 04 -- Gerer les erreurs

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Retourne une erreur claire si l'action est invalide ou si un argument obligatoire manque |
| **Critere d'acceptation** | Code de retour non-zero + message explicite |
| **Dependances** | Aucune |

---

## 4. Exigences Non-Fonctionnelles

| Categorie | Exigence | Critere de mesure |
|---|---|---|
| **Performance** | Execution en moins de 1 seconde | Chronometrage |
| **Fiabilite** | Aucune perte de contenu existant | Comparaison avant/apres sur un fichier de test |
| **Maintenabilite** | Script lisible et commente | Revue par l'agent proprietaire |
| **Portabilite** | Compatible Git Bash Windows, Linux, Mac | Aucune commande specifique a un OS |
| **Securite** | Ne pas ecraser les fichiers hors perimetre | Liste de fichiers autorises en constante |

---

## 5. Architecture / Structure Technique

### 5.1 Vue d'ensemble

Le script analyse les arguments (action, agent, raison, mission), verifie leur validite, lit le fichier cible, applique la modification ciblee (section principale et/ou historique), puis ecrit le fichier.

### 5.2 Composants

| Composant | Role | Dependances |
|---|---|---|
| Parseur d'arguments | Lire et valider les entrees | Aucune |
| Lecteur | Lire AGENTS.md et AGENTS-historique.md | Fichiers sources |
| Modificateur | Remplacer la section Agent Principal Actuel | Lecteur |
| Journaliseur | Ajouter l'entree d'historique | Lecteur |
| Ecrivain | Ecrire les fichiers modifies | Modificateur, Journaliseur |

### 5.3 Modele de donnees

Section cible dans AGENTS.md :

```markdown
## Agent Principal Actuel

| Champ | Valeur |
|---|---|
| **Nom** | [agent] |
| **Role** | [role] |
| **Fiche** | [chemin fiche] |
```

### 5.4 Interfaces / API

```bash
mettre-a-jour-agents-md.sh activer <agent> "<raison>" ["<mission>"]
mettre-a-jour-agents-md.sh reactiver "<raison>"
```

### 5.5 Flux / Workflows

```
1. Lire les arguments (action obligatoire)
2. Si activer : agent obligatoire
3. Lire AGENTS.md
4. Remplacer la section Agent Principal Actuel
5. Ajouter l'entree dans l'historique (date + heure, limite 150, decroissant)
6. Ecrire le fichier
7. Retourner un message de confirmation
```

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| Format markdown a preserver | Risque de casser le tableau | Modification ciblee par section, pas d'ecrasement global |

### 6.2 Risques

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Fichier verrouille par un autre processus | Faible | Moyen | Message d'erreur clair |
| Historique trop long | Moyen | Moyen | Troncature a 150 entrees |

---

## 7. Livrables attendus

| Livrable | Format | Destination |
|---|---|---|
| Script | Bash | `agents/tools/mettre-a-jour/mettre-a-jour-agents-md/` |
| Documentation | Markdown | `agents/tools/mettre-a-jour/mettre-a-jour-agents-md/` |
| Specification | Markdown | `agents/tools/mettre-a-jour/mettre-a-jour-agents-md/spec/` |

---

## 8. Plan de validation

### 8.1 Criteres de succes globaux

- [ ] L'activation met bien a jour AGENTS.md
- [ ] La reactivation remet Cerberus principal
- [ ] L'historique est date avec l'heure, limite a 150, ordre decroissant

### 8.2 Methode de validation

Tests manuels sur le dossier `exemples/` avec des fichiers de test.

### 8.3 Responsables

| Role | Responsable |
|---|---|
| Redaction | Promethee |
| Validation technique | Buffy |

---

## 9. Liens et References

### 9.1 Pense-bete source

- Spec directe (pas de pense-bete parent)

### 9.2 Specs connexes

- Aucune

### 9.3 Conventions applicables

- `convention-renommage.md`

### 9.4 Regles immuables

- `regles-emojis-ascii.md`

### 9.5 References externes

- Aucune

---

## 10. RVAV de la spec

- [rechercher] -- references rassemblees (AGENTS.md, AGENTS-historique.md, conventions)
- [verifier] -- structure complete (sections 1-10 presentes)
- [analyser] -- coherent avec l'outil existant (v0.2.0)
- [valider] -- pret pour le statut prepare

---

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| 2026-08-05 | 0.1.0 | Vulcain | Creation initiale |
| 2026-08-07 | 0.2.0 | Promethee | Refonte selon spec-template, version outil 0.2.0 |
