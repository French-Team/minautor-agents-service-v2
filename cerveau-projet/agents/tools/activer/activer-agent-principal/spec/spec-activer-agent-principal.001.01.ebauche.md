---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Specification -- activer-agent-principal

**Version :** 0.8.11
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
| **Description** | Remet Cerberus comme agent principal (modele aero R1/R3 : atterrissage terminal du PILOTE en fin de ROUND avec bilan consolide - plus jamais a la fin d une mission, la fin de tout agent va vers ORACLE via reactiver-fin --cible oracle) |
| **Critere d'acceptation** | Cerberus est de nouveau declare principal dans AGENTS.md |
| **Dependances** | Exigence 01 |

### 3.3 Exigence 03 -- Journaliser dans l'historique

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Ajoute une entree datee (AAAA-MM-JJ HH:MM) dans l'historique, avec la colonne session, limite a 150 interventions, ordre decroissant. v0.5.14 : format de bloc lisible (`#>` + ligne `### <date> - <agent>` coloree par agent + ligne de table `| date | session | agent | raison |` INTACTE pour les parseurs + continuations `###>` decalees) |
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
| **Nom LLM** | [id du LLM, ex: llm-1 -- convention v0.5.0 : aucun mot seul, EN TETE] |
| **Nom Agent** | [agent] |
| **Role Agent** | [role] |
| **Fiche** | [chemin fiche] |
...
```

CONVENTION IDENTIFICATION (v0.5.0) : le champ `**Nom**` n'existe plus -- il est remplace par
`**Nom Agent**` et `**Role Agent**`. Les anciens blocs (Nom / Role / Id LLM) sont migres
automatiquement lors de chaque edition (reconstruction complete en ordre canonique,
`**Nom LLM**` en tete).

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
| 2026-09-02 | 0.8.11 | Morpheus | NORMALISATION DE LA SESSION A LA DISPATCH ACTIVATION : la commande `activer <session> <agent>` ecrivait `### Session : <session>` tel quel dans AGENTS.md - un appel `activer admin vulcain` produisait un bloc malforme `### Session : admin` (invisible par nettoyer-sessions, KO test-025). La dispatch normalise desormais le nom de session comme sidentifier (admin -> session-admin, session-* preserve). Version 0.8.11. |
| 2026-09-02 | 0.8.10 | Vulcain | MODELE AERO DANS LES MESSAGES DE GUIDANCE (directive utilisateur) : message post-activation "MA FIN va vers ORACLE (reactiver-fin <agent> --cible oracle), JAMAIS Cerberus ni un autre agent ; le PILOTE decide et atterrit sur Cerberus en fin de round" ; garde-fou auto-reactivation "oublie sa fin (modele aero)" ; docstring activer_cerberus = atterrissage terminal du PILOTE ; exigence 02 specifiee en fin de ROUND (plus de fin de mission). Version 0.8.10. |
| 2026-08-30 | 0.8.9 | Buffy | TRACABILITE R/IR MODELE AERO : detecter_type_round elargi - une raison commencant par SIGNALER, BESOIN INTER-ROUND, ou contenant MISSION-AJOUTER / INTER-ROUND est taggee IR en plus des prefixes INTER-ROUND / FIN D INTER-ROUND. Couvre le signalement a ORACLE du modele aero R2 (le pilote largue l habilite) : l inter-round est desormais trace sans flag manuel sur le vocabulaire aero. Version 0.8.9. |
| 2026-08-29 | 0.8.7 | Vulcain | COLONNE EXECUTEUR ROUTINES (demande utilisateur) : les entrees historisees par les routines v1 (citations, flux, sante, live, encart, vigie-round...) affichaient une colonne Executeur VIDE - elles appellent ajouter_historique sans passeur executeur. Nouveau helper _executeur_routine(agent) qui lit le manifest des routines et retourne RT(<intervalle>s) si l agent est une routine ACTIVE avec intervalle > 0. Version 0.8.7. |
| 2026-08-29 | 0.8.6 | Vulcain | COLONNE DEFCON : l encart v1 passe de 9 a 10 colonnes `| Grade | Agent | Defcon | Executeur | Etat | Secteur | Raison | Heure | id | Type |`. Chaque entree porte le DEFCON courant au moment de l historisation. |
| 2026-08-29 | 0.8.5 | Vulcain | --FORCER LIBRE (support redemarrer-session.py) : main() retire --forcer d argv avant le parsing positionnel. |
| 2026-08-29 | 0.8.4 | Vulcain | ETATS DYNAMIQUES : la liste des etats + leurs regles sortent du code vers etats-actions.json (oracle/, en v ETATS_ACTIONS surchargeable), defaut ABSOLU. |
| 2026-08-29 | 0.8.3 | Vulcain | COLONNE DEBUT/FIN -> ETAT : la colonne Debut/Fin devient Etat avec 5 etats connus, _debut_fin renommee _etat_action. |
| 2026-08-27 | 0.8.2 | Vulcain | COLONNE DEBUT/FIN SUR CERBERUS : activer_cerberus prefxe la raison par 'DEBUT: '. Parite avec _debut_fin. |
| 2026-08-27 | 0.8.1 | Vulcain | TABLEAU V1 GRADE/SECTEUR/DEBUT-FIN : l encart passe a 8 colonnes + _construire_encart_v1 pour la migration. |
| 2026-08-19 | 0.5.17 | Vulcain | TOKENS INTEGRES : activer/reactiver appellent analyser-tokens --snapshot (hybride API/estimation), stockent le snapshot de debut dans le chrono (--tokens), calculent la conso par difference au relais et l affichent au repere : `(9min 11s, tokens: 12.4k env / 8.2k recus)` |
| 2026-08-19 | 0.5.16 | Vulcain | CHRONOMETRE INTEGRE : activer/reactiver appellent chronometrer-duree (arreter le chrono precedent, demarrer le nouveau) et ajoutent la duree au repere `### <date> - <agent> (Xmin Ys)` dans AGENTS-historique |
| 2026-08-19 | 0.5.15 | Vulcain | FORMAT HISTORIQUE RESTRUCTURE : table `agent | heure | date | session | raison`, raison enroulee a 100 caracteres (continuations `###>`), parseurs adaptes |
| 2026-08-05 | 0.1.0 | Vulcain | Creation initiale |
| 2026-08-07 | 0.2.0 | Promethee | Refonte selon spec-template, version outil 0.2.0 |
| 2026-08-07 | 0.3.0 | Vulcain | Multi-session LLM : sidentifier, sessions, session obligatoire, blocs isoles, migration, historique 4 colonnes |
| 2026-08-07 | 0.3.1 | Vulcain | Profil de session dans le classeur-variables (profil-session-<session>) ecrit/mis a jour a chaque action |
| 2026-08-07 | 0.3.3 | REGLE UTILISATEUR : session occupee -> attribution automatique de la prochaine libre (1er LLM = llm-1) |
| 2026-08-07 | 0.3.4 | MODE ID : sidentifier <llm-id> (comparaison id -> session, liaison dans le classeur) |
| 2026-08-07 | 0.3.2 | Vulcain | Regle de derivation du nommage (profil-session-<id> sans double prefixe) - correction du verdict A REVOIR de Janus |
| 2026-08-15 | 0.5.7 | Vulcain | VERROU DU MARBRE : verrouiller_constitution() appelle proteger-verrou-marbre --zone constitution avant toute ecriture (sidentifier/activer/reactiver) et refuse si la Constitution a diverge sans protocole ; desactive en mode test (AGENTS_FILE) ; agent Gardien ajoute au dictionnaire AGENTS ; FIX MARQUEURS : la boucle de retrait de la section Sessions connues s arrete aussi sur les bornes `<!-- MARBRE:` (avant : elle avalait le marqueur DEBUT de la zone constitution) |
| 2026-08-15 | 0.5.6 | Vulcain | ANTI-ACCUMULATION HISTORIQUE : ajouter_historique purge les continuations AVEC l entree depassee (limite 150) - anti-recurrence du parasite de 1183 lignes dans AGENTS-historique. Fichier nettoye + entrees de la matinee reconstruites (incident) |
| 2026-08-14 | 0.5.5 | Vulcain | FIX bug de recollement : reconstruire_bloc recolait les anciennes continuations de la Raison a chaque nouvelle raison -> accumulation (AGENTS.md corrompu). Un champ REMPLACE ignore son ancienne suite (y compris Raison) |
| 2026-08-14 | 0.5.4 | Vulcain | DEMARRAGE OBLIGATOIRE automatique : activer ajoute a la Raison l instruction de lancement du parcours depuis c0 (--reponses OUI), sauf pour Cerberus et reactiver ; fix bug latent : reconstruire_bloc preservait pas la Raison multiligne |
| 2026-08-12 | 0.5.1 | Vulcain | Alignement spec/outil (round 11 coherence documentaire : version de la spec synchronisee avec la version de l outil 0.5.1) |
| 2026-08-08 | 0.5.0 | Vulcain | CONVENTION IDENTIFICATION : blocs de session en Nom LLM (tete) / Nom Agent / Role Agent, migration automatique des anciens champs, table Sessions connues en Nom LLM |
