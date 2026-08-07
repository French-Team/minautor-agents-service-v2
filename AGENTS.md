# Agents du Cerveau-Projet

> Ce fichier est mis a jour dynamiquement par l'agent principal.
> Il identifie quel agent est actuellement actif et sa configuration.
> L'historique complet est dans [AGENTS-historique.md](AGENTS-historique.md).

---

## Agent Principal Actuel

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus|
| **Role** | Gardien de l'entree -- analyse et active les agents|
| **Derniere mise a jour** | 2026-08-07|
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | Clio (retour de mission)|
| **Raison** | README MAJ: ajout de 2 badges supplementaires en tete (Langages=Bash, Python, Markdown:orange; Version=v0.2.0:blue), fusionnes proprement sur la ligne de badges existante (6 badges au total sur une seule ligne). Valeurs issues des sources de verite (82 .sh Bash, 82 .py Python, 241 .md; version proj v0.2.0 index-cerveau.md). ASCII strict OK, structure preservee, ordre: titre > badges > logo. Note: fusion faite par edition directe ciblee (l'outil --badges creerait une nouvelle ligne par appel) - changement de contenu minime.|prepare) identique remplace par detection Python des noms non-ASCII (faux positif elimine). 2) evaluer-coherence: exclusions convention-*/protocole-*/regles-*/templates/rvav (faux positifs pense-betes/ elimines). 3) combos-audit-general: tableau affiche maintenant les 4 evaluateurs (bug SCORES une ligne). Correction annexe: themis.md -- 4 references combos-combos-audit-general corrigees en combos-audit-general. Tests: syntaxe OK, ASCII OK, statuts OK, outils references OK, combo 4 scores OK.|

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

## Comment changer d'agent

### Depuis Cerberus

1. Cerberus analyse le besoin
2. Il choisit l'agent approprie
3. Il utilise `mettre-a-jour-agents-md` pour mettre a jour AGENTS.md
4. Il documente la raison et la mission
5. L'agent prend le relais
6. **L'agent lit SA fiche et SES corrections** avant de commencer sa mission

### Retour a Cerberus

1. L'agent termine sa mission
2. L'agent utilise `mettre-a-jour-agents-md reactiver` pour reactiver Cerberus
3. L'agent documente la fin de mission
4. Cerberus reprend le controle
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

> **Le cycle** : Chaque session commence et finit avec Cerberus.
> Il analyse le besoin, active l'agent, et reprend quand l'agent a fini.
> **Regle** : Toujours revenir a Cerberus apres chaque mission.
