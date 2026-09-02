---
identite:
  type: racine
  appartient_a: commun
  commun: true
---
# Agents du Cerveau-Projet

> Ce fichier est mis a jour dynamiquement par les agents principaux.
> Chaque session LLM (session-admin, session-freelance...) possede son bloc dedie et son agent principal.
> L'historique complet est dans [AGENTS-historique.md](AGENTS-historique.md) (v1 / session-admin)
> et [AGENTS-historique-v2.md](AGENTS-historique-v2.md) (v2 / session-freelance) - fichiers
> SEPARES par session (decision 2026-08-26 : la v2 est l evolution de la v1, chaque session
> a SES fichiers avec SON format). Vue rapide : [AGENTS-activite-recente.md](AGENTS-activite-recente.md)
> (v1) + [AGENTS-activite-recente-v2.md](AGENTS-activite-recente-v2.md) (v2).

---

## Sessions LLM

### Session : session-admin

| Champ | Valeur |
|---|---|
| **Nom LLM** | glm5 |
| **Nom Agent** | cerberus |
| **Role Agent** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-09-02 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | Cerberus (automatique) |
| **Raison** | Reprise session-admin apres redemarrage des serveurs; Cerberus reprend la communication utilisateur. |
## Sessions connues

| Session | Nom LLM | Agent actif | Derniere activite |
|---|---|---|---|
| session-admin | glm5 | cerberus | 2026-09-02 08:02:25.172 |
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
| 5 | Agent termine : la fin va vers **ORACLE** (modele aero R1, jamais cerberus, jamais un autre agent) via `oracle.py reactiver-fin <agent> --cible oracle` ; le PILOTE decide du suivant. ERREUR HORS-PERIMETRE -> INTER-ROUND (modele aero) : l'agent SIGNALE le besoin a ORACLE (`oracle.py mission-ajouter --agent <habilite>`), MA FIN vers ORACLE, et le **pilote LARGUE l'agent habilite** ; a la fin de l'inter-round, le pilote renvoie l'appelant qui REPREND son round (protocole-fin-mission, modele aero 2026-08-30) |
| 6 | **Cerberus relit SA fiche et SES corrections** puis reprend pour la suite |

> **REGLE DE RELECTURE** : A chaque activation ou reactivation, l'agent relit SA fiche et SES corrections (jamais celles des autres). Activer sans lire = inutile.
<!-- MARBRE:FIN constitution -->

---

## Comment changer d'agent (dans sa session)

Chaque session LLM a son propre cycle. **MODE ID + SESSION (v0.3.0)** : chaque LLM possede SON id
donne par l'utilisateur au demarrage, ET l'utilisateur indique la SESSION voulue
(`session='admin'` = equipe v1 qui gere le cerveau, `session='freelance'` = equipe v2).
Les sessions sont NOMMEES (`session-admin`, `session-freelance`) et non plus numerotees.
Chaque bloc de session dans AGENTS.md contient le champ `| **Nom LLM** | <id> |` : **le LLM se
reconnait en lisant AGENTS.md** -- le bloc qui porte SON id est SON bloc (source double :
AGENTS.md + classeur synchronises). Au demarrage : 1) chercher SON bloc dans AGENTS.md
(champ Nom LLM, dans la session demandee) ; 2) si absent, lancer la SOUS-COMMANDE sidentifier
d'activer-agent-principal :
`python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier <mon-id> <ma-session>`
(la session est creee/retrouvee ; l'id y est lie ; repli heritage : id llm-N -> session-llm-N
si aucun nom de session n'est fourni).

### Depuis Cerberus (dans sa session)

1. Cerberus analyse le besoin
2. Il choisit l'agent approprie
3. Il utilise `python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer <session> <agent> <raison>` pour mettre a jour SON bloc dans AGENTS.md
4. Il documente la raison et la mission
5. L'agent prend le relais
6. **L'agent lit SA fiche et SES corrections** avant de commencer sa mission

### Oracle -- Agent + serveur de coordination v1 (session-admin)

> Oracle est le couple agent + serveur de la session-admin, comme JARVIS en
> v2 (agent JARVIS + serveur jarvis).
> **Agent oracle** : [cerveau-projet/agents/oracle/oracle.md](cerveau-projet/agents/oracle/oracle.md) - coordinateur de l equipe v1, traite les alertes de coordination (processus fantomes, serveurs morts, ecarts harnais) et remonte a Cerberus.
> **Serveur oracle** : `cerveau-projet/agents/tools/oracle/` - route les
> messages (inbox/outbox), historise les actions, gere les agents v1.
> Lancement : `python3 cerveau-projet/agents/tools/oracle/oracle.py demarrage`
> Commandes : envoyer, lire, acquitter, lister, historiser, activer, status, controle-processus
> En session freelance, JARVIS joue ce role.

### Fin de mission (la fin suit SA carte)

1. L'agent termine sa mission
2. LA FIN SUIT SA CARTE (modele aero R1/R3) : la fin de tout agent va vers **ORACLE** (l aeroport) via `oracle.py reactiver-fin <agent> "<bilan>" --cible oracle` - jamais cerberus, jamais un autre agent. C est le **PILOTE** qui decide du suivant (largage d un maillon, retour a Cerberus en fin de round avec le bilan consolide). Les arbres ont des fins `fin-*` vers oracle (audit F4/F5 + reconstruction).
3. ERREUR HORS-PERIMETRE -> INTER-ROUND (modele aero R2/R3, decision utilisateur 2026-08-30) : l'agent N'INTERRUPT PAS le round et ne reactive PAS Cerberus et n'ACTIVE JAMAIS un autre agent : il SIGNALE le besoin a ORACLE (`oracle.py mission-ajouter --file asap --agent <habilite> "<rapport>"`) puis sa fin va vers ORACLE ; le **PILOTE LARGUE l'agent habilite** qui repare ; a la fin de l'inter-round, le pilote renvoie l'appelant qui REPREND son round principal ; cascade autorisee entre habilites (le pilote decide), une erreur n'est JAMAIS seulement detectee : reparation exclusive par l'habilite
4. L'agent documente la fin de mission
4. Le controle revient a Cerberus (directement, ou par le bilan consolide du dernier maillon de la chaine)
5. **Cerberus relit SA fiche et SES corrections** avant de poursuivre

---

## Groupes d'agents (regles-groupes-agents)

> **REGLE IMMUABLE** : [regles-groupes-agents.md](cerveau-projet/agents/regles-immuables/general/regles-groupes-agents.md) -- 3 groupes aux domaines separes :
> **1) Coordination** : Cerberus, Oracle (coordinateur v1). **2) Cerveau-projet** (gerent `cerveau-projet/` lui-meme : outils, parcours, fiches, protocoles, spec des outils, README) : **Buffy** (responsable), Vulcain, Morpheus, Janus, Atlas, Themis, Clio, Hygie, Hermes, Socrate, Redacteur-v2. **3) Trio projets futurs** (ecrivent `pense-betes/`, `specs/`, `todos/` pour le dev des apps futures) : Athena, Promethee, Minerve.
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
| [Socrate](cerveau-projet/agents/socrate/socrate.md) | cerveau-projet/agents/socrate/ | Conversateur de revision strategique | Disponible (en attente) | Discute des revisions, priorise, produit une liste de missions pour Cerberus |
| [Redacteur-v2](cerveau-projet/agents/redacteur-v2/redacteur-v2.md) | cerveau-projet/agents/redacteur-v2/ | Redacteur PRO des docs de la v2 (freelance) | Disponible (en attente) | Agent dedie a la redaction des docs v2 - MODE CONVERSATION (reactive Cerberus sur fin de cycle) |
| [Hades](cerveau-projet/agents/hades/hades.md) | cerveau-projet/agents/hades/ | Gardien des archives git | Disponible (en attente) | SEUL habilite aux commandes git - regle d anciennete : checkout interdit hors fichiers tres recents |
| [Oracle](cerveau-projet/agents/oracle/oracle.md) | cerveau-projet/agents/oracle/ | Coordinateur de l equipe v1 (session-admin) | Disponible (en attente) | Equivalent de JARVIS en v2 - traitement des alertes de coordination (processus fantomes, serveurs morts, roulage messages) + controle processus |

### Agents v2 (freelance)

> **REGLE V2 (PERIMETRE WRITE)** : les agents freelance n'ecrivent QUE dans
> `cerveau-projet/freelance/`. Tout outil - v1 OU v2 - qui ecrirait hors de
> ce perimetre est interdit (ex: `activer-agent-principal` ecrit dans
> AGENTS.md et le classeur v1 ; `guider-parcours` guide vers des parcours
> v1). Demarrage : relire SA fiche puis SES corrections, puis suivre
> SON arbre des decisions `cerveau-projet/freelance/<agent>/parcours/arbre-<agent>.json`.
> Toute communication/activation passe par jarvis.py (envoyer/lire/acquitter/lister/activer).
> **EXCLUSIVITE JARVIS** : Vision est le SEUL agent habilite a modifier JARVIS
> (agent `freelance/jarvis/` + serveur MCP `tools-commun/jarvis/`). Tout autre
> agent qui modifie JARVIS commet une violation de perimetre.

| Agent | Fiche | Role | Statut | Note |
|---|---|---|---|---|
| [Shuri](cerveau-projet/freelance/shuri/shuri.md) | cerveau-projet/freelance/shuri/ | Constructeur des agents de la v2 | Disponible (en attente) | Premier agent MARVEL operationnel - MODE CONVERSATION (reactive Cerberus sur fin de cycle) |
| [Stark](cerveau-projet/freelance/stark/stark.md) | cerveau-projet/freelance/stark/ | Coordinateur de l'equipe freelance, responsable JARVIS | Disponible (en attente) | Iron Man - coordonne Shuri (agents) et Forge (outils) - MODE CONVERSATION |
| [Forge](cerveau-projet/freelance/forge/forge.md) | cerveau-projet/freelance/forge/ | Responsable des outils v2 | Disponible (en attente) | Mutant inventeur - construit les outils freelance (D15) - MODE CONVERSATION |
| [Rogers](cerveau-projet/freelance/rogers/rogers.md) | cerveau-projet/freelance/rogers/ | Gardien des regles, conventions et protocoles | Disponible (en attente) | Captain America - veille au respect des regles - MODE CONVERSATION |
| [Parker](cerveau-projet/freelance/parker/parker.md) | cerveau-projet/freelance/parker/ | Explorateur / diagnostiqueur | Disponible (en attente) | Spider-Man - explore et diagnostique - MODE CONVERSATION |
| [JARVIS](cerveau-projet/freelance/jarvis/jarvis.md) | cerveau-projet/freelance/jarvis/ | Intelligence derriere le serveur, assistant de Stark | Disponible (en attente) | JARVIS - transforme les demandes de Stark en missions precise - MODE CONVERSATION |
| [Vision](cerveau-projet/freelance/vision/vision.md) | cerveau-projet/freelance/vision/ | Gardien exclusif de JARVIS (agent + server MCP) | Disponible (en attente) | Synthezoide ne de JARVIS - SEUL habilite a modifier jarvis.py / jarvis-server.py / l'agent JARVIS - MODE CONVERSATION |
| [Fury](cerveau-projet/freelance/fury/fury.md) | cerveau-projet/freelance/fury/ | Testeur reel HORS-ROUND | Disponible (en attente) | Directeur SHIELD - prend la place de l'utilisateur pour tester des rounds reels - JAMAIS dans un round - MODE CONVERSATION |
| [EDITH](cerveau-projet/freelance/edith/edith.md) | cerveau-projet/freelance/edith/ | Observatrice -- cellule dormante | Dormante (activee par JARVIS sur demande de ses routines vigie/notation ou demande explicite) | Voit tout - analyse les observations de son serveur H24 et rapporte les 4 W - LECTURE SEULE - jamais de sa propre initiative |

---

> **Le cycle** : Chaque session LLM commence et finit avec Cerberus.
> Chaque session utilise SON identifiant (session-admin / session-freelance) pour toutes ses activations.
> **Regle** : La fin de mission suit SA carte (modele aero R1/R3) : toute fin va vers **ORACLE** via `oracle.py reactiver-fin <agent> --cible oracle` - jamais cerberus, jamais un autre agent. C est le pilote qui decide du suivant (la chaine ne retombe JAMAIS sur Cerberus au milieu). ERREUR HORS-PERIMETRE -> INTER-ROUND (2026-08-30) : l'agent signale le besoin a ORACLE (`mission-ajouter --agent <habilite>`), le pilote largue l'habilite, puis renvoie l'appelant qui reprend son round ; une erreur jamais seulement detectee.
