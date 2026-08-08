---
identite:
  type: racine
  appartient_a: commun
  commun: true
---
# Agents du Cerveau-Projet

> Ce fichier est mis a jour dynamiquement par les agents principaux.
> Chaque session LLM (session-llm-N) possede son bloc dedie et son agent principal.
> L'historique complet est dans [AGENTS-historique.md](AGENTS-historique.md).

---

## Sessions LLM

### Session : session-llm-4

| Champ | Valeur |
|---|---|
| **Nom LLM** | llm-2 |
| **Nom Agent** | Cerberus |
| **Role Agent** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-08-08 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | Identification |
| **Raison** | Identification LLM - demarrage de session |


### Session : session-llm-3

| Champ | Valeur |
|---|---|
| **Nom LLM** | kilo-llm |
| **Nom Agent** | Cerberus |
| **Role Agent** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-08-08 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | Identification |
| **Raison** | Identification LLM - demarrage de session |


### Session : session-llm-2

| Champ | Valeur |
|---|---|
| **Nom Agent** | Cerberus |
| **Role Agent** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-08-08 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | Identification |
| **Raison** | Identification LLM - demarrage de session |


### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom LLM** | llm-1 |
| **Nom Agent** | morpheus |
| **Role Agent** | Testeur -- validation des outils et des tests |
| **Derniere mise a jour** | 2026-08-08 |
| **Fiche** | [cerveau-projet/agents/morpheus/morpheus.md](cerveau-projet/agents/morpheus/morpheus.md) |
| **Corrections** | [cerveau-projet/agents/morpheus/corrections.md](cerveau-projet/agents/morpheus/corrections.md) |
| **Active par** | Cerberus (automatique) |
| **Raison** | MISSION TESTS (decision utilisateur, 2 livrables). LIVRABLE 1 - CORRIGER test-003-activer-agent-principal-v033.sh : la fonction nom_session (lignes 40, 114, 134) lit encore **Nom** alors que les blocs session de AGENTS.md utilisent **Nom Agent** (migration v0.5.0 faite avant cette mission - git diff du test vide = probleme preexistant, pas cause par le fix ajouter_historique). CORRECTION : adapter nom_session et tous les autres lectures de champs du test au nouveau format de bloc (Nom LLM / Nom Agent / Role Agent / Statut Agent etc), puis relancer les tests 001 a 007 et confirmer TOUS VALIDES (004-007 deja VALIDE, 001-002 OK). LIVRABLE 2 - CREER LE TEST FORMEL de nettoyer-sessions v0.1.0 : tester-nettoyer-sessions.sh dans cerveau-projet/agents/tools/nettoyer/nettoyer-sessions/tests/ (convention comme les tests activer : nommage test-NNN-...sh, ASCII strict, LF, assertions [OK]/[ERREUR], verdict final). VERIFIER : (a) execution sur COPIES avec les 3 variables AGENTS_FILE + CLASSEUR_STOCKAGE redirigees (lecon: ne jamais toucher les vrais fichiers pendant les tests), (b) blocs ### Session supprimes, (c) section ## Sessions connues supprimee, (d) lignes profil-session-* du classeur supprimees, (e) frontmatter + entete + Configuration Active PRESERVES, (f) AGENTS-historique.md JAMAIS modifie, (g) idempotence (2eme execution = rien de plus), (h) --dry-run ne modifie rien, (i) parite py/sh (memes fichiers resultats), (j) --version. VERDICT attendu : VALIDE. Puis rediger le verdict dans corrections.md de Morpheus et reactiver Cerberus avec bilan et outils utilises declares (REGLE ABSOLUE 6). |
## Sessions connues

| Session | Nom LLM | Agent actif | Derniere activite |
|---|---|---|---|
| session-llm-1 | llm-1 | morpheus | 2026-08-08 19:10 |
| session-llm-2 | - | Cerberus | 2026-08-08 17:55 |
| session-llm-3 | kilo-llm | Cerberus | 2026-08-08 18:17 |
| session-llm-4 | llm-2 | Cerberus | 2026-08-07 16:03 |
| session-llm-5 | llm-3 | Cerberus | 2026-08-07 16:04 |
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

Chaque session LLM a son propre cycle. **MODE ID** : chaque LLM possede SON id (donne par
l'utilisateur au demarrage, ex: `llm-1`). **REGLE ALIGNEMENT (v0.4.0)** : id `llm-N` ->
session `session-llm-N` (le numero de session porte le numero de l'id). Chaque bloc de session
dans AGENTS.md contient le champ `| **Id LLM** | <id> |` : **le LLM se reconnait en lisant
AGENTS.md** -- le bloc qui porte SON id est SON bloc (source double : AGENTS.md + classeur
synchronises). Au demarrage : 1) chercher SON bloc dans AGENTS.md (champ Id LLM) ; 2) si absent,
lancer la SOUS-COMMANDE sidentifier d'activer-agent-principal :
`python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier <mon-id>`
(id deja lie = retrouvee ; id inconnu llm-N = session-llm-N ;
conflit si session-llm-N liee a un autre id = prochaine libre).

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
