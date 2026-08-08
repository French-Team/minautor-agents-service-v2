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

### Session : session-llm-1

| Champ | Valeur |
|---|---|
| **Nom LLM** | llm-1 |
| **Nom Agent** | buffy |
| **Role Agent** | Developpeur principal -- contenu et structures |
| **Derniere mise a jour** | 2026-08-08 |
| **Fiche** | [cerveau-projet/agents/buffy/buffy.md](cerveau-projet/agents/buffy/buffy.md) |
| **Corrections** | [cerveau-projet/agents/buffy/corrections.md](cerveau-projet/agents/buffy/corrections.md) |
| **Active par** | Cerberus (automatique) |
| **Raison** | MISSION (decision utilisateur - 3 infractions a corriger): TON DOMAINE - fichiers du cerveau. LIVRABLE 1 (regle workspace IMMUABLE): creer cerveau-projet/pense-betes/regles-immuables/general/regles-perimetre-workspace.md - ECRITURE = workspace uniquement (Z:/analyste-in-console), HORS WORKSPACE = LECTURE SEULE (jamais creer/modifier/supprimer de fichier hors workspace, meme temporaire), les fichiers temporaires de test/script se creent DANS le workspace (ex: dossier .tmp-test/ local) et se suppriment apres. Inscrire dans index-regles-general.md + regles-general-global.md + index-regles-immuables.md. LIVRABLE 2 (ASCII 2 alternatives): mettre a jour regles-emojis-ascii.md - a la verification ASCII, 2 ALTERNATIVES: [OK] aucun non-ASCII -> continuer / [NON] non-ASCII detecte -> LANCER LE COMBO combo-corriger-ascii (python3 cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.py cerveau-projet/combos/combo-corriger-ascii/definition-combo.json) - JAMAIS corriger soi-meme les accents. LIVRABLE 3 (11 parcours): dans chaque parcours agents/<a>/parcours/parcours-<a>.json, ajouter dans les cases qui ECRIVENT/MODIFIENT un fichier un indice concis: REGLE WORKSPACE (ecriture = workspace seul) + ASCII 2 alternatives (verifier -> OK continuer / NON lancer combo-corriger-ascii). Inspecter chaque parcours pour trouver les cases d ecriture (indices avec ajouter-contenu, ecrire-fichier, editer-fichier, creer). ASCII strict, valider liens, puis reactiver Cerberus. |
## Sessions connues

| Session | Nom LLM | Agent actif | Derniere activite |
|---|---|---|---|
| session-llm-1 | llm-1 | buffy | 2026-08-08 16:58 |
| session-llm-3 | - | Cerberus | 2026-08-07 16:12 |
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
lancer `sidentifier <mon-id>` (id deja lie = retrouvee ; id inconnu llm-N = session-llm-N ;
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
