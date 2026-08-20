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
| **Nom LLM** | opencode |
| **Nom Agent** | morpheus |
| **Role Agent** | Testeur -- validation des outils et des tests |
| **Derniere mise a jour** | 2026-08-19 |
| **Fiche** | [cerveau-projet/agents/morpheus/morpheus.md](cerveau-projet/agents/morpheus/morpheus.md) |
| **Corrections** | [cerveau-projet/agents/morpheus/corrections.md](cerveau-projet/agents/morpheus/corrections.md) |
| **Active par** | Cerberus (automatique) |
| **Raison** | TESTER l outil evaluer-progression cree par Vulcain : ecrire et executer les test-XXX sans que Vulcain touche a aucun fichier de test |

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>').
### Session : session-llm-3

| Champ | Valeur |
|---|---|
| **Nom LLM** | kilo-test2 |
| **Nom Agent** | Cerberus |
| **Role Agent** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-08-18 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | Identification |
| **Raison** | Identification LLM - demarrage de session |


### Session : session-llm-2

| Champ | Valeur |
|---|---|
| **Nom LLM** | kilo-llm |
| **Nom Agent** | themis |
| **Role Agent** | Evaluatrice croisee -- evaluation et audit |
| **Derniere mise a jour** | 2026-08-18 |
| **Fiche** | [cerveau-projet/agents/themis/themis.md](cerveau-projet/agents/themis/themis.md) |
| **Corrections** | [cerveau-projet/agents/themis/corrections.md](cerveau-projet/agents/themis/corrections.md) |
| **Active par** | Cerberus (automatique) |
| **Raison** | Inventaire et audit des outils de performance (tests, fonction, worker, workflow, flux, round, session) : analyser l environnement de travail (OS, ressources, parallelisme) puis lister les outils necessaires et possibles pour ameliorer les performances, afin d etablir des configurations adaptables selon le systeme et les ressources disponibles |

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/themis/parcours/parcours-themis.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>').
### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom LLM** | llm-1 |
| **Nom Agent** | Cerberus |
| **Role Agent** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-08-20 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | janus (retour de mission) |
| **Raison** | Session terminee. Bilan consolide : investigation opencode /tmp/opencode/ + garde-fou v0.5.19 (blocage double activation) + evaluer-processus v0.1.13 (ignore test missions) + bumper v0.1.13 + non-regression 93/96 (3 KO documentes) + nettoyage artefacts. 5 leciones documentees dans cerberus/corrections.md. |
## Sessions connues

| Session | Nom LLM | Agent actif | Derniere activite |
|---|---|---|---|
| session-llm-1 | llm-1 | Cerberus | 2026-08-20 07:03 |
| session-llm-2 | kilo-llm | themis | 2026-08-18 21:05 |
| session-llm-3 | kilo-test2 | Cerberus | 2026-08-18 21:57 |
| session-llm-4 | opencode | morpheus | 2026-08-19 20:51 |
## Configuration Active
<!-- MARBRE:DEBUT constitution -->
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
| 5 | Agent termine : la fin suit SA carte (activation directe -> reactiver Cerberus ; maillon de chaine -> activer le suivant) |
| 6 | **Cerberus relit SA fiche et SES corrections** puis reprend pour la suite |

> **REGLE DE RELECTURE** : A chaque activation ou reactivation, l'agent relit SA fiche et SES corrections (jamais celles des autres). Activer sans lire = inutile.
<!-- MARBRE:FIN constitution -->

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

### Fin de mission (la fin suit SA carte)

1. L'agent termine sa mission
2. LA FIN SUIT SA CARTE (Pattern 8) : activation directe par Cerberus -> l'agent utilise `python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py reactiver <session> <raison> <agent>` pour reactiver Cerberus ; maillon d'une chaine -> l'agent ACTIVE le maillon suivant selon SA carte ; seul le DERNIER maillon reactiver Cerberus avec le bilan consolide
3. L'agent documente la fin de mission
4. Le controle revient a Cerberus (directement, ou par le bilan consolide du dernier maillon de la chaine)
5. **Cerberus relit SA fiche et SES corrections** avant de poursuivre

---

## Groupes d'agents (regles-groupes-agents)

> **REGLE IMMUABLE** : [regles-groupes-agents.md](cerveau-projet/agents/regles-immuables/general/regles-groupes-agents.md) -- 3 groupes aux domaines separes :
> **1) Coordination** : Cerberus. **2) Cerveau-projet** (gerent `cerveau-projet/` lui-meme : outils, parcours, fiches, protocoles, spec des outils, README) : **Buffy** (responsable), Vulcain, Morpheus, Janus, Atlas, Themis, Clio, Hygie, Hermes. **3) Trio projets futurs** (ecrivent `pense-betes/`, `specs/`, `todos/` pour le dev des apps futures) : Athena, Promethee, Minerve.
> **REGLE** : le trio n'est JAMAIS utilise pour developper le cerveau-projet -- c'est Buffy la responsable.

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
| [Hygie](cerveau-projet/agents/hygie/hygie.md) | cerveau-projet/agents/hygie/ | Agent de nettoyage du workspace | Disponible (en attente) | SEUL habilite a TOUT le workspace et a supprimer sans demande prealable |
| [Hermes](cerveau-projet/agents/hermes/hermes.md) | cerveau-projet/agents/hermes/ | Agent de la langue (orthographe, vocabulaire, fautes) | Disponible (en attente) | Agent dedie aux fautes de francais |
| [Gardien](cerveau-projet/agents/gardien/gardien.md) | cerveau-projet/agents/gardien/ | Gardien du marbre (securite du code) | Disponible (en attente) | SEUL a proposer la modification des zones protegees (l utilisateur valide) |
| [Argus](cerveau-projet/agents/argus/argus.md) | cerveau-projet/agents/argus/ | Detecteur de contradictions | Disponible (en attente) | DETECTE et SIGNALE les incoherences (cases, regles, protocoles, git) - ne corrige jamais |
| [Chiron](cerveau-projet/agents/chiron/chiron.md) | cerveau-projet/agents/chiron/ | Educateur des agents -- formation continue | Disponible (en attente) | Re-edue les agents quand les outils/regles/protocoles changent |

---

> **Le cycle** : Chaque session LLM commence et finit avec Cerberus.
> Chaque session utilise SON identifiant (session-llm-N) pour toutes ses activations.
> **Regle** : La fin de mission suit SA carte (Pattern 8) : activation directe par Cerberus -> reactiver Cerberus ; maillon d'une chaine -> activer le suivant selon SA carte ; seul le DERNIER maillon reactiver Cerberus avec le bilan consolide. La chaine ne retombe JAMAIS sur Cerberus au milieu.
