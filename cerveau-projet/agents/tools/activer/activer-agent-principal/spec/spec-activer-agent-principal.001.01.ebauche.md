# Specification -- activer-agent-principal

**Statut :** prepare
**ID :** 001
**Class :** 01
**Cree :** 2026-08-05
**Theme :** activer-agent-principal
**Pense-bete source :** Spec directe (pas de pense-bete parent)

---

## 1. Objectif

Modifier le fichier `AGENTS.md` de maniere fiable et standardisee lors de l'activation ou de la reactivation d'un agent, en mettant a jour le bloc de session (Agent Principal de la session) et l'historique. Supporte plusieurs sessions LLM en parallele : chaque LLM a son propre bloc et son propre agent principal.

---

## 2. Contexte

### 2.1 Origine

Le cycle du cerveau-projet impose que chaque agent reactive Cerberus a la fin de sa mission (coordinateur > agent > coordinateur). Cette reactivation se fait via la modification de `AGENTS.md`. Sans outil dedie, chaque agent modifiait le fichier manuellement avec des risques d'incoherence (format, historique, erreurs).

### 2.2 Perimetre

**Couvert** : identification de session (`sidentifier`), activation (mettre un agent comme principal de sa session), reactivation (remettre Cerberus dans sa session), liste des sessions (`sessions`), mise a jour de l'historique, journalisation dans `AGENTS-historique.md`, ecriture/mise a jour du profil de session (`profil-session-<session>`) dans le classeur-variables, migration de l'ancienne structure mono-session.

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
| **Description** | Ajoute une entree datee (AAAA-MM-JJ HH:MM) dans l'historique, avec la colonne session, limite a 150 interventions, ordre decroissant |
| **Critere d'acceptation** | L'entree est presente en haut, la limite de 150 est respectee, la session est identifiee |
| **Dependances** | Exigence 01, fichier `AGENTS-historique.md` |

### 3.4 Exigence 04 -- S'identifier (sidentifier)

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Au demarrage d'un LLM : attribue le prochain `session-llm-N` libre (ou utilise le nom fourni), cree le bloc de session, met Cerberus comme agent principal de la session |
| **Critere d'acceptation** | La session est attribuee, son bloc existe, son agent principal est Cerberus |
| **Dependances** | Fichier `AGENTS.md` lisible et ecrivable |

### 3.5 Exigence 05 -- Isoler les sessions

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Chaque action `activer`/`reactiver` ne modifie QUE le bloc `### Session : <session>` vise ; les autres sessions restent intouchees |
| **Critere d'acceptation** | Avec 2 sessions, activer un agent dans la session 1 ne change pas l'agent principal de la session 2 |
| **Dependances** | Exigence 04, Exigence 01 |

### 3.6 Exigence 06 -- Migrer l'ancienne structure

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Si AGENTS.md contient l'ancienne section `## Agent Principal Actuel`, le premier appel convertit en `## Sessions LLM` avec le bloc `### Session : session-llm-1` en conservant les valeurs actuelles |
| **Critere d'acceptation** | Les valeurs (Nom, Role, Fiche, Raison) sont conservees apres migration |
| **Dependances** | Exigence 04 |

### 3.7 Exigence 07 -- Gerer les erreurs

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Retourne une erreur claire si l'action est invalide ou si un argument obligatoire manque |
| **Critere d'acceptation** | Code de retour non-zero + message explicite |
| **Dependances** | Aucune |

### 3.8 Exigence 08 -- Mettre a jour le profil de session dans le classeur

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | A chaque sidentifier/activer/reactiver, ecrit ou met a jour la variable `profil-session-<id>` dans `classeur-variables/stockage/variables-actuelles.md` (ligne existante -> mise a jour agent+date ; absente -> ajoutee a la fin du tableau). REGLE DE DERIVATION : id = profil-session- + partie apres le prefixe `session-` du nom complet (session-llm-1 -> profil-session-llm-1) | REGLE UTILISATEUR : au demarrage la section sessions est VIDE, le 1er LLM devient session-llm-1, tout LLM suivant recoit automatiquement la prochaine libre
| **Critere d'acceptation** | Apres chaque action, la ligne `profil-session-<session>` reflete l'agent principal actuel et la date |
| **Dependances** | Fichier stockage du classeur lisible et ecrivable |

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
## Sessions LLM

### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom** | [agent] |
| **Role** | [role] |
| **Fiche** | [chemin fiche] |
...
```

### 5.4 Interfaces / API

```bash
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier [llm-id]
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer <session> <agent> "<raison>" ["<mission>"]
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py reactiver <session> "<raison>" <agent_precedent>
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sessions
```

### 5.5 Flux / Workflows

```
1. Lire les arguments (action obligatoire)
2. sidentifier : attribuer la session, creer le bloc, Cerberus par defaut
3. activer/reactiver : session obligatoire
4. Migrer l'ancienne structure si necessaire
5. Lire AGENTS.md
6. Modifier UNIQUEMENT le bloc de la session visee
7. Ajouter l'entree dans l'historique (date + heure, session, limite 150, decroissant)
8. Ecrire/mettre a jour le profil de session dans le classeur-variables (profil-session-<session>)
9. Ecrire le fichier
10. Retourner un message de confirmation
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
| Script | Bash | `agents/tools/activer/activer-agent-principal/` |
| Documentation | Markdown | `agents/tools/activer/activer-agent-principal/` |
| Specification | Markdown | `agents/tools/activer/activer-agent-principal/spec/` |

---

## 8. Plan de validation

### 8.1 Criteres de succes globaux

- [ ] sidentifier attribue une session et met Cerberus comme agent principal
- [ ] L'activation met a jour UNIQUEMENT le bloc de la session visee
- [ ] Deux sessions ont deux agents principaux independants
- [ ] La reactivation remet Cerberus principal dans la session
- [ ] La migration conserve les valeurs de l'ancienne structure
- [ ] L'historique est date avec l'heure + session, limite a 150, ordre decroissant
- [ ] Le profil de session est ecrit/mis a jour dans le classeur-variables a chaque action

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
| 2026-08-07 | 0.3.0 | Vulcain | Multi-session LLM : sidentifier, sessions, session obligatoire, blocs isoles, migration, historique 4 colonnes |
| 2026-08-07 | 0.3.1 | Vulcain | Profil de session dans le classeur-variables (profil-session-<session>) ecrit/mis a jour a chaque action |
| 2026-08-07 | 0.3.3 | REGLE UTILISATEUR : session occupee -> attribution automatique de la prochaine libre (1er LLM = llm-1) |
| 2026-08-07 | 0.3.4 | MODE ID : sidentifier <llm-id> (comparaison id -> session, liaison dans le classeur) |
| 0.3.2 | Vulcain | Regle de derivation du nommage (profil-session-<id> sans double prefixe) - correction du verdict A REVOIR de Janus |
