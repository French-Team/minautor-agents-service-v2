---
identite:
  type: outil
  nom: Oracle
  version: 0.1.0
  cree: 2026-08-26
  appartient_a: commun
  commun: true
  role: Hub de coordination des agents v1
  session: session-admin
---

# Oracle -- Coordination des agents v1

> Equivalent de JARVIS (v2) pour la session-admin (v1).

## Vue d'ensemble

| Champ | Valeur |
|---|---|
| **Nom** | Oracle |
| **Version** | 0.1.0 |
| **Role** | Hub de communication inter-agents v1 |
| **Session** | session-admin |
| **Responsable** | Buffy (creation), Cerberus (usage) |

## Commandes CLI

```bash
# Envoyer un message
python3 oracle.py envoyer <de> <vers> "<objet>" "<corps>"

# Lire les messages non lus
python3 oracle.py lire <agent>

# Acquitter un message
python3 oracle.py acquitter <agent> <id>

# Lister les messages
python3 oracle.py lister <agent>

# Historiser une action
python3 oracle.py historiser <agent> "<raison>" [--type R|IR]

# Activer un agent
python3 oracle.py activer <agent> "<raison>"

# Afficher les sessions
python3 oracle.py sessions

# Etat d'Oracle
python3 oracle.py status
```

## Architecture

```
cerveau-projet/agents/tools/oracle/
├── oracle.py          # CLI (commandes)
├── oracle-server.py   # Serveur MCP (daemon)
├── oracle-data.json   # Config (liste des agents)
├── oracle.md          # Ce fichier
├── inbox/             # Messages recus par agent
│   ├── cerberus.jsonl
│   ├── buffy.jsonl
│   └── ...
├── outbox/            # Messages envoyes par agent
│   ├── cerberus.jsonl
│   ├── buffy.jsonl
│   └── ...
└── files/             # Files de missions
```

## Integration avec les outils existants

Oracle **delegue** a activer-agent-principal.py pour :
- Les activations/reactivations
- L'ecriture dans AGENTS-historique.md (corps)
- L'ecriture dans AGENTS-activite-recente.md (encart)
- L'ecriture dans historique.db (BDD)

Oracle ajoute :
- Le routing des messages (inbox/outbox)
- La consultation rapide de l'etat des agents
- L'historisation centralisee

## Role dans le cycle v1

```
Utilisateur -> Oracle -> Agent -> Oracle -> Utilisateur
```

Oracle est le point d'entree unique pour la communication entre agents v1.
