# Agents du Cerveau-Projet

> Ce fichier est mis a jour dynamiquement par les agents principaux.
> Chaque session LLM (session-llm-N) possede son bloc dedie et son agent principal.
> L'historique complet est dans [AGENTS-historique.md](AGENTS-historique.md).

---

## Sessions LLM

### Session : session-llm-5

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus |
| **Role** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-08-07 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | Identification |
| **Raison** | Identification LLM - demarrage de session |


### Session : session-llm-4

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus |
| **Role** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-08-07 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | Identification |
| **Raison** | Identification LLM - demarrage de session |


### Session : session-llm-3

| Champ | Valeur |
|---|---|
| **Nom** | Janus |
| **Role** | Controleur des statuts -- validation et verification |
| **Derniere mise a jour** | 2026-08-07 |
| **Fiche** | [cerveau-projet/agents/janus/janus.md](cerveau-projet/agents/janus/janus.md) |
| **Corrections** | [cerveau-projet/agents/janus/corrections.md](cerveau-projet/agents/janus/corrections.md) |
| **Active par** | Cerberus (automatique) |
| **Raison** | SECOND CONTROLE (Vulcain): controle de l'outil partage generateurs-commande cree (py+sh+json+md+spec). Verdict attendu: VALIDE (ASCII OK, nommage OK, syntaxe OK, parite py/sh OK, index-tools a jour 79 outils, fiche Vulcain assignee). |


### Session : session-llm-2

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus |
| **Role** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-08-07 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | Clio (retour de mission) |
| **Raison** | README mis a jour: 83->85 outils (generateurs-commande, detecter-usage-outils-externes ajoutes). ASCII OK. __pycache__ conserve comme artefact (non liste). Corrections Clio enregistrees. |


### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus |
| **Role** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-08-07 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | Janus (retour de mission) |
| **Raison** | SECOND CONTROLE cycle A+B+C: VERDICT CONFORME. BILAN OUTILS (levier C): outils utilises = activer-agent-principal, valider-nommage, valider-liens (86 valides/0 invalide), verifier-role-fichier (conforme), verifier-separation-preoccupations (OK), combos-valider-cerveau, valider-tableaux (14/14 CONFORME), detecter-surcharge-fichier, detecter-usage-outils-externes (LEVIER B: 0 suspect sur tous les fichiers modifies). CONTROLES: nommage OK, liens OK, roles OK, tableaux CONFORME, traces externes AUCUNE. Points PRE-EXISTANTS hors perimetre de la mission (a traiter par Themis en audit): 2 fichiers non-ASCII dans janus/controles + themis/rapports + dictionnaires (le dossier exemples/ est volontairement pollue pour les tests) + 6 fichiers en surcharge dans agents/. Aucun ne provient de cette mission. Cycle A+B+C complet et operationnel: A (REGLE ABSOLUE 5 dans 12 fiches), B (detecter-usage-outils-externes 41/41), C (REGLE ABSOLUE 6 dans 12 fiches + bilan declenche par Janus). |

---

## Configuration Active

### Regles specifiques a Cerberus

1. **Ecouter avant de decider** -- comprendre le besoin avant d'activer un agent
2. **Documenter chaque activation** -- raison, mission, agent choisi
3. **Exiger le retour** -- chaque agent doit revenir a Cerberus
4. **Ne jamais sauter Cerberus** -- point d'entree unique

### Le cycle fondamental

```
CERBERUS -> AGENT -> CERBERUS
    1         2         3
```

| Etape | Action |
|---|---|
| 1 | Cerberus accueille l'utilisateur |
| 2 | Cerberus analyse et choisit l'agent |
| 3 | Cerberus active l'agent (mise a jour AGENTS.md) |
| 4 | **L'agent active lit SA fiche et SES corrections** puis execute sa mission |
| 5 | Agent termine et reactive Cerberus |
| 6 | **Cerberus relit SA fiche et SES corrections** puis reprend pour la suite |

> **REGLE DE RELECTURE** : A chaque activation ou reactivation, l'agent relit SA fiche et SES corrections (jamais celles des autres). Activer sans lire = inutile.

---

## Comment changer d'agent (dans sa session)

Chaque session LLM a son propre cycle. L'identifiant de session est obtenu au demarrage via `sidentifier <mon-id>` (**MODE ID**) : chaque LLM possede SON id (donne par l'utilisateur), l'outil compare cet id aux sessions enregistrees et rend SA session (id deja lie = retrouvee, id inconnu = creation prochaine libre + liaison). **Un LLM ne deduit jamais sa session d'AGENTS.md** -- la session visible appartient a un AUTRE LLM. Il utilise la session RENDUE par l'outil via SON id.

### Depuis Cerberus (dans sa session)

1. Cerberus analyse le besoin
2. Il choisit l'agent approprie
3. Il utilise `python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer <session> <agent> <raison>` pour mettre a jour SON bloc dans AGENTS.md
4. Il documente la raison et la mission
5. L'agent prend le relais
6. **L'agent lit SA fiche et SES corrections** avant de commencer sa mission

### Retour a Cerberus (dans sa session)

1. L'agent termine sa mission
2. L'agent utilise `python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py reactiver <session> <raison> <agent>` pour reactiver Cerberus
3. L'agent documente la fin de mission
4. Cerberus reprend le controle dans la session
5. **Cerberus relit SA fiche et SES corrections** avant de poursuivre

---

## Liste des agents

### Agents indispensables

| Agent | Fiche | Role | Statut |
|---|---|---|---|
| [Cerberus](cerveau-projet/agents/cerberus/cerberus.md) | cerveau-projet/agents/cerberus/ | Gardien de l'entree | Disponible (principal) |
| [Buffy](cerveau-projet/agents/buffy/buffy.md) | cerveau-projet/agents/buffy/ | Developpeur principal | Disponible (en attente) |

### Agents secondaires

| Agent | Fiche | Role | Statut | Note |
|---|---|---|---|---|
| [Atlas](cerveau-projet/agents/atlas/atlas.md) | cerveau-projet/agents/atlas/ | Explorateur | Disponible (en attente) | Carte de decision mise a jour |
| [Janus](cerveau-projet/agents/janus/janus.md) | cerveau-projet/agents/janus/ | Controleur des statuts | Disponible (sur demande) | Carte de decision mise a jour |
| [Vulcain](cerveau-projet/agents/vulcain/vulcain.md) | cerveau-projet/agents/vulcain/ | Constructeur d'outils | Disponible (en attente) | 19 outils crees |
| [Themis](cerveau-projet/agents/themis/themis.md) | cerveau-projet/agents/themis/ | Evaluatrice croisee | Disponible | 4 evaluateurs + 1 combo |
| [Morpheus](cerveau-projet/agents/morpheus/morpheus.md) | cerveau-projet/agents/morpheus/ | Testeur dedie | Disponible (en attente) | Agent dedie aux tests |
| [Athena](cerveau-projet/agents/athena/athena.md) | cerveau-projet/agents/athena/ | Redactrice de pense-betes | Disponible (en attente) | Agent dedie aux pense-betes |
| [Promethee](cerveau-projet/agents/promethee/promethee.md) | cerveau-projet/agents/promethee/ | Redacteur de specs | Disponible (en attente) | Agent dedie aux specs |
| [Minerve](cerveau-projet/agents/minerve/minerve.md) | cerveau-projet/agents/minerve/ | Redactrice de todos | Disponible (en attente) | Agent dedie aux todos |
| [Clio](cerveau-projet/agents/clio/clio.md) | cerveau-projet/agents/clio/ | Muse de l'histoire -- README | Disponible (en attente) | Agent dedie au README |

---

> **Le cycle** : Chaque session LLM commence et finit avec Cerberus.
> Chaque session utilise SON identifiant (session-llm-N) pour toutes ses activations.
> **Regle** : Toujours revenir a Cerberus apres chaque mission, dans SA session.
