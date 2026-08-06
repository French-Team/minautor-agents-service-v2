# Agents du Cerveau-Projet

> Ce fichier est mis à jour dynamiquement par l'agent principal.
> Il identifie quel agent est actuellement actif et sa configuration.
> L'historique complet est dans [AGENTS-historique.md](AGENTS-historique.md).

---

## Agent Principal Actuel

| Champ | Valeur |
|---|---|
| **Nom** | Cerberus|
| **Rôle** | Gardien de l'entrée — analyse et active les agents|
| **Dernière mise à jour** | 2026-08-06 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Activé par** | Cerberus (retour de mission)|
| **Raison** | Second controle active par Cerberus selon liste definie (branches verdict + anti-boucle Janus/Clio) + bug sed Raison corrige|

---

## Configuration Active

### Règles spécifiques à Cerberus

1. **Écouter avant de décider** — comprendre le besoin avant d'activer un agent
2. **Documenter chaque activation** — raison, mission, agent choisi
3. **Exiger le retour** — chaque agent doit revenir à Cerberus
4. **Ne jamais sauter Cerberus** — point d'entrée unique

### Le cycle fondamental

```
CERBERUS → AGENT → CERBERUS
    1         2         3
```

| Étape | Action |
|---|---|
| 1 | Cerberus accueille l'utilisateur |
| 2 | Cerberus analyse et choisit l'agent |
| 3 | Cerberus active l'agent (mise à jour AGENTS.md) |
| 4 | Agent exécute sa mission |
| 5 | Agent termine et réactive Cerberus |
| 6 | Cerberus reprend pour la suite |

---

## Comment changer d'agent

### Depuis Cerberus

1. Cerberus analyse le besoin
2. Il choisit l'agent approprié
3. Il utilise `modifier-agents-md` pour mettre à jour AGENTS.md
4. Il documente la raison et la mission
5. L'agent prend le relais

### Retour à Cerberus

1. L'agent termine sa mission
2. L'agent utilise `modifier-agents-md reactiver` pour réactiver Cerberus
3. L'agent documente la fin de mission
4. Cerberus reprend le contrôle

---

## Liste des agents

### Agents indispensables

| Agent | Fiche | Rôle | Statut |
|---|---|---|---|
| [Cerberus](cerveau-projet/agents/cerberus/cerberus.md) | cerveau-projet/agents/cerberus/ | Gardien de l'entrée | Disponible (principal) |
| [Buffy](cerveau-projet/agents/buffy/buffy.md) | cerveau-projet/agents/buffy/ | Développeur principal | Disponible (en attente) |

### Agents secondaires

| Agent | Fiche | Rôle | Statut | Note |
|---|---|---|---|---|
| [Atlas](cerveau-projet/agents/atlas/atlas.md) | cerveau-projet/agents/atlas/ | Explorateur | Disponible (en attente) | Carte de décision mise à jour |
| [Janus](cerveau-projet/agents/janus/janus.md) | cerveau-projet/agents/janus/ | Contrôleur des statuts | Disponible (sur demande) | Carte de décision mise à jour |
| [Vulcain](cerveau-projet/agents/vulcain/vulcain.md) | cerveau-projet/agents/vulcain/ | Constructeur d'outils | Disponible (en attente) | 19 outils créés |
| [Morpheus](cerveau-projet/agents/morpheus/morpheus.md) | cerveau-projet/agents/morpheus/ | Testeur dédié | Disponible (en attente) | Agent dédié aux tests |
| [Athena](cerveau-projet/agents/athena/athena.md) | cerveau-projet/agents/athena/ | Rédactrice de pense-bêtes | Disponible (en attente) | Agent dédié aux pense-bêtes |
| [Promethee](cerveau-projet/agents/promethee/promethee.md) | cerveau-projet/agents/promethee/ | Rédacteur de specs | Disponible (en attente) | Agent dédié aux specs |
| [Minerve](cerveau-projet/agents/minerve/minerve.md) | cerveau-projet/agents/minerve/ | Rédactrice de todos | Disponible (en attente) | Agent dédié aux todos |
| [Clio](cerveau-projet/agents/clio/clio.md) | cerveau-projet/agents/clio/ | Muse de l'histoire — README | Disponible (en attente) | Agent dédié au README |

---

> **Le cycle** : Chaque session commence et finit avec Cerberus.
> Il analyse le besoin, active l'agent, et reprend quand l'agent a fini.
> **Règle** : Toujours revenir à Cerberus après chaque mission.
