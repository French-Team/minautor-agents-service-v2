---
identite:
  type: regle
  appartient_a: commun
  commun: true
---
# Regle Immuable -- Groupes d'agents et Domaines

---

## Principe Fondamental

Le cerveau-projet est organise en **3 groupes** aux domaines STRICTEMENT
separes. Chaque agent n'opere que dans SON domaine. **Cerberus choisit
toujours l'agent du groupe qui correspond a la tache** ; utiliser un agent
hors de son domaine est une faute d'assignation (lecon 2026-08-10 : Promethee
active pour documenter le Pattern 16 de la spec-guider-parcours, or ce fichier
appartient au cerveau-projet, pas au trio).

---

## Les 3 groupes

### Groupe 1 -- Coordination

| Agent | Role |
|---|---|
| **Cerberus** | Coordonne : analyse les besoins, choisit et active le bon agent, gere les activations (AGENTS.md) |

### Groupe 2 -- Cerveau-projet (gestion du dossier `cerveau-projet/` lui-meme)

Ce groupe developpe, corrige et fait evoluer LE CERVEAU lui-meme : outils,
parcours, cartes de decision, fiches agents, protocoles, regles, conventions,
index, README.

| Agent | Role | Domaine |
|---|---|---|
| **Buffy** | **RESPONSABLE du cerveau-projet** | Modifier les fichiers du cerveau-projet (conventions, regles, protocoles, index, demarrer.md, fiches, parcours, documentation des specs) |
| **Vulcain** | Constructeur d'outils | Creer / modifier / tester / optimiser les OUTILS du cerveau (v2/v3, purification, bugs) |
| **Morpheus** | Testeur dedie | Ecrire et lancer les TESTS (protocole-tests) |
| **Janus** | Controleur des statuts | Second controle, validation, verification croisee |
| **Atlas** | Explorateur | Explorer, chercher, documenter, analyser (information) |
| **Themis** | Evaluatrice croisee | Audit, evaluation, coherence, combos d'audit |
| **Clio** | Muse de l'histoire | Mettre a jour le README quand necessaire |

> **REGLE** : Toute tache de dev/amelioration du cerveau-projet (outils,
> parcours, fiches, protocoles, SPEC DES OUTILS comme spec-guider-parcours)
> est confiee a ce groupe -- en premier lieu **Buffy** (responsable).

### Groupe 3 -- Trio projets futurs (travaille DANS le cerveau, pour Cerberus)

Ce trio cree les fichiers de travail destines au dev des APPLICATIONS FUTURES
pour la future equipe codeur : les pense-betes, les specs et les todos. Ils
ecrivent dans les dossiers `pense-betes/`, `specs/`, `todos/`.

| Agent | Role | Domaine |
|---|---|---|
| **Athena** | Redactrice de pense-betes | Transforme une demande en pense-bete |
| **Promethee** | Redacteur de specs | Transforme un pense-bete en spec |
| **Minerve** | Redactrice de todos | Transforme une spec en todo |

> **REGLE ABSOLUE** : Le trio (Athena, Promethee, Minerve) n'est **JAMAIS**
> utilise pour developper le cerveau-projet lui-meme (modifier outils,
> parcours, fiches, protocoles, ou spec des outils du cerveau). Il est reserve
> a la phase "dev de nouveaux projets". La documentation des outils du cerveau
> (spec-guider-parcours, spec des outils) appartient au groupe 2.

---

## Comment choisir le groupe

1. Identifier la cible de la tache :
   - Fichier de `pense-betes/`, `specs/`, `todos/` (projet futur) -> GROUPE 3 ;
   - Fichier de `cerveau-projet/` (outil, parcours, fiche, protocole, spec
     d'outil, README) -> GROUPE 2 ;
   - Coordination, activation -> GROUPE 1.
2. Dans le groupe 2, prioriser : Buffy (responsable) pour les fichiers du
   cerveau ; Vulcain pour les outils ; Morpheus pour les tests ; Janus pour le
   controle ; Themis pour l'audit ; Atlas pour l'exploration ; Clio pour le
   README.
3. En cas de doute, demander a l'utilisateur (jamais d'assignation par
   habitude).

---

## Consequence pratique (migration des parcours)

La migration des parcours v0.2.0 -> v0.3.x concerne les agents du groupe 2
dont le parcours est en v0.2.0 (atlas, clio, morpheus). Les parcours du trio
(athena, promethee, minerve) ne sont PAS migres dans cette phase : ils seront
prepares lors de la phase "dev de nouveaux projets".
