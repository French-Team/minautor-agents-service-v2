---
identite:
  nom: protocoles-mcp
  version: 0.1.0
  cree: 2026-08-22
  type: reference
  appartient_a: rogers
  commun: false
  tags: mcp, jarvis, protocoles, architecture, freelance, v2
  mot-cles: ["mcp", "jarvis", "protocoles", "architecture", "hub", "v2"]
  session: freelance
# Protocoles MCP -- JARVIS et l'equipe Freelance (v2)
# Source : MCP (Model Context Protocol) adapte a notre projet

> Rogers est le gardien de ces protocoles.

---

## 1. Pourquoi MCP ?

**MCP (Model Context Protocol)** est un protocole open-source pour connecter
des composants entre eux. Nous l'utilisons PAS pour connecter des LLMs,
mais pour connecter **nos agents, outils et futurs services**.

| Avant (scripts) | Apres (MCP) |
|---|---|
| Chaque outil = un script isole | Tout connecte via MCP |
| `python3 jarvis.py envoyer ...` | Appel tool MCP `envoyer_message` |
| Communication directe entre scripts | Hub central MCP (JARVIS) |
| Pas de decouverte automatique | Chaque composant expose ses tools |

**Benefices** :
- **Standardise** : un seul protocole pour tout
- **Decouvrable** : chaque composant liste ses tools
- **Evolutif** : ajouter un service = ajouter un tool MCP
- **Interne** : pas d'acces exterieur
- **Traable** : chaque appel est logue

---

## 2. Architecture

```
Agent Shuri  ──┐
Agent Forge  ──┤
Agent Rogers ──┼── MCP ── JARVIS Server ── inbox/outbox/agents/
Agent Stark  ──┤
Outil X      ──┤
Service Y    ──┘
```

**JARVIS** = hub MCP central. Tout le monde passe par lui.
**Chaque agent** = serveur MCP qui expose ses capacites.
**Chaque outil** = peut etre expose via MCP.

---

## 3. Tools MCP de JARVIS

### 3.1 envoyer_message
```
Envoie un message entre agents via JARVIS.
Parametres:
  - de: expediteur (string, requis)
  - vers: destinataire (string, requis)
  - priorite: 1-5 (integer, defaut: 3)
  - objet: sujet du message (string, requis)
  - corps: contenu du message (string, requis)
Retour:
  - id: identifiant du message
  - statut: envoye
```

### 3.2 lire_messages
```
Lit les messages en attente d'un agent.
Parametres:
  - agent: nom de l'agent (string, requis)
  - tous: inclure les messages lus (boolean, defaut: false)
Retour:
  - messages: liste des messages
  - bloquants: nombre de messages P1 non lus
```

### 3.3 acquitter_message
```
Marque un message comme lu et accuse.
Parametres:
  - agent: nom de l'agent (string, requis)
  - id: identifiant du message (string, requis)
Retour:
  - statut: acquitte
  - message_expire: true (le message est purge apres acquittement)
```

### 3.4 activer_agent
```
Active un agent via JARVIS (remplace activer-agent-principal).
Parametres:
  - agent: agent a activer (string, requis)
  - mission: description de la mission (string, requis)
  - session: nom de la session (string, defaut: session-1)
  - de: expediteur (string, defaut: stark)
Retour:
  - id: identifiant du message d'activation
  - statut: active
  - message: "L'agent doit lire son inbox avant de demarrer"
```

### 3.5 status_equipe
```
Tableau de bord de l'equipe.
Parametres: aucun
Retour:
  - agents: liste des agents avec leur grade, etat, dernier message
  - bloques: agents avec messages P1 non lus
  - total_messages: nombre total de messages en attente
```

### 3.6 detecter_alertes
```
Detecte les problemes et alertes.
Parametres: aucun
Retour:
  - alertes: liste des alertes (URGENT/INFO/OK)
  - agents_bloques: agents bloques par P1
  - agents_inactifs: agents sans activite recente
```

### 3.7 historique
```
Historique des actions de la session.
Parametres:
  - agent: filtrer par agent (optionnel)
  - limite: nombre d'entrees (defaut: 20)
Retour:
  - entrees: liste des actions (date, agent, action, details)
```

---

## 4. Resources MCP

### 4.1 inbox/{agent}.jsonl
```
Messages recus par un agent. JSONL, une ligne = un message.
Schema:
  id, de, vers, priorite, date, objet, corps, lu, accuse, type
```

### 4.2 outbox/{agent}.jsonl
```
Messages envoyes par un agent. JSONL, une ligne = un message.
Schema: identique a inbox.
```

### 4.3 status.json
```
Etat actuel de l'equipe.
Schema:
  {
    "agents": {
      "<agent>": {
        "grade": "silver",
        "etat": "actif|inactif|bloque",
        "dernier_message": "2026-08-22T20:00:00",
        "messages_en_attente": 2
      }
    },
    "alertes": [...]
  }
```

### 4.4 config.json
```
Configuration de JARVIS.
Schema:
  {
    "agents_valides": ["stark", "shuri", "forge", "rogers"],
    "priorite_bloquante": 1,
    "expiration_apres_lu": true
  }
```

---

## 5. Comment un agent se connecte a JARVIS

### Etape 1: Decouverte
```python
# L'agent envoie server/discover pour connaitre les tools de JARVIS
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "server/discover",
  "params": {}
}
```

### Etape 2: Liste des tools
```python
# L'agent demande la liste des tools disponibles
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
# Reponse: [envoyer_message, lire_messages, acquitter_message, ...]
```

### Etape 3: Utilisation
```python
# L'agent appelle un tool
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "lire_messages",
    "arguments": {"agent": "shuri"}
  }
}
```

---

## 6. Ajouter un nouvel agent/outil/service

### Nouvel agent
1. Creer la structure `freelance/<agent>/` (template v2)
2. Creer un serveur MCP pour l'agent : `<agent>/<agent>-server.py`
3. Exposer les tools de l'agent via MCP
4. Enregistrer l'agent dans `config.json` de JARVIS
5. JARVIS detecte automatiquement le nouvel agent

### Nouvel outil
1. Creer la structure `tools-commun/<outil>/` (template v2)
2. Si l'outil doit etre accessible via MCP : exposer ses fonctions
3. Ajouter le tool dans la liste des tools de JARVIS
4. Documentation dans le .md de l'outil

### Nouveau service
1. Creer un serveur MCP pour le service
2. Exposer les tools/resources du service
3. Enregistrer dans `config.json` de JARVIS
4. JARVIS route les appels vers le service

---

## 7. Regles et conventions MCP

| Regle | Detail |
|---|---|
| **JARVIS = hub** | Tout passe par JARVIS. Pas de communication directe entre agents. |
| **Decouverte d'abord** | Chaque composant doit repondre a server/discover. |
| **Tools = actions** | Un tool MCP = une action excecutable (pas de lecture seule). |
| **Resources = donnees** | Une resource MCP = une source de donnees (pas d'action). |
| **JSON-RPC 2.0** | Tous les echanges suivent le format JSON-RPC 2.0. |
| **Traabilite** | Chaque appel MCP est logue dans l'historique. |
| **Securite** | Pas d'acces exterieur. Tout est interne a l'ecosysteme. |
| **Evolutif** | Ajouter un tool = ajouter un fichier, pas modifier le code. |

---

## 8. Roadmap

| Phase | Action | Priorite |
|---|---|---|
| 1 | JARVIS serveur MCP (tools + resources) | Critique |
| 2 | Agents comme serveurs MCP | Important |
| 3 | Decouverte automatique des agents | Important |
| 4 | Outils exposes via MCP | Moyen |
| 5 | Futurs services via MCP | Futur |
