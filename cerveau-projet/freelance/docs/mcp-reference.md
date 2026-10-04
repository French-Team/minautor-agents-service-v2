---
identite:
  nom: mcp-reference
  version: 0.1.0
  cree: 2026-08-22
  type: reference
  appartient_a: rogers
  commun: false
  tags: mcp, reference, documentation, web, freelance, v2
  mot-cles: ["mcp", "reference", "documentation", "web", "protocol", "v2"]
  session: freelance
# Reference MCP -- Informations recuperees depuis modelcontextprotocol.io
# Source : https://modelcontextprotocol.io/introduction
#         https://modelcontextprotocol.io/docs/concepts/architecture

> Document de reference pour l'equipe freelance.
> Rogers en est le gardien.

---

## 1. Definition de MCP

**MCP (Model Context Protocol)** est un standard open-source pour connecter
des applications IA a des systemes externes.

> "Pensez a MCP comme un port USB-C pour les applications IA."
> -- modelcontextprotocol.io

**Ce que MCP permet** :
- Agents accedant a Google Calendar, Notion, etc.
- Claude Code generant une app web depuis un design Figma
- Chatbots d'entreprise connectes a plusieurs bases de donnees
- Modeles IA creant des designs 3D sur Blender

**Pourquoi MCP compte** :
- **Developpeurs** : reduit le temps de developpement et la complexite
- **Applications IA** : acces a un ecosysteme d'outils et de donnees
- **Utilisateurs** : applications IA plus capables

---

## 2. Architecture client-serveur

```
MCP Host (application IA)
    |
    |--- MCP Client 1 -- MCP Server 1
    |--- MCP Client 2 -- MCP Server 2
    +--- MCP Client N -- MCP Server N
```

**Participants** :
| Participant | Role |
|---|---|
| **MCP Host** | Application IA qui coordonne les clients (ex: Claude Desktop, VS Code) |
| **MCP Client** | Composant qui maintient une connexion avec un serveur MCP |
| **MCP Server** | Programme qui fournit le contexte aux clients |

**Exemple** : VS Code = MCP Host. Quand VS Code se connecte au serveur Sentry,
il instancie un MCP Client pour maintenir la connexion.

**Types de serveurs** :
- **Local** : tourne sur la meme machine (transport Stdio)
- **Distants** : tourne sur un serveur (transport Streamable HTTP)

---

## 3. Les 3 primitives MCP

### 3.1 Tools (Outils)
Fonctions executables que les applications IA peuvent appeler.
```json
{
  "name": "envoyer_message",
  "description": "Envoyer un message entre agents",
  "inputSchema": {
    "type": "object",
    "properties": {
      "de": {"type": "string", "description": "Expediteur"},
      "vers": {"type": "string", "description": "Destinataire"},
      "priorite": {"type": "integer", "description": "1-5"}
    },
    "required": ["de", "vers"]
  }
}
```

### 3.2 Resources (Ressources)
Sources de donnees qui fournissent du contexte.
```json
{
  "name": "inbox_agent",
  "description": "Messages recus par un agent",
  "uri": "jarvis://inbox/shuri.jsonl"
}
```

### 3.3 Prompts (Prompts)
Templates reutilisables pour structurer les interactions.
```json
{
  "name": "activer_agent",
  "description": "Template d'activation d'un agent",
  "arguments": [
    {"name": "agent", "description": "Agent a activer"},
    {"name": "mission", "description": "Mission de l'agent"}
  ]
}
```

---

## 4. Transport

### Stdio (Standard Input/Output)
- Communication directe entre processus locaux
- Pas de surcharge reseau
- Performance optimale
- Usage : serveurs locaux

### Streamable HTTP
- HTTP POST pour les messages client -> serveur
- Server-Sent Events pour le streaming
- Authentification standard (Bearer tokens, API keys)
- Usage : serveurs distants

---

## 5. Format JSON-RPC 2.0

Tous les echanges MCP utilisent JSON-RPC 2.0.

### Requete
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": {
        "name": "mon-client",
        "version": "1.0.0"
      }
    }
  }
}
```

### Reponse
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "tools": [
      {
        "name": "envoyer_message",
        "description": "Envoyer un message",
        "inputSchema": {...}
      }
    ]
  }
}
```

### Notification (pas de reponse attendue)
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed",
  "params": {}
}
```

---

## 6. Decouverte (server/discover)

Le client envoie `server/discover` pour connaitre le serveur.

**Requete** :
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "server/discover",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": {
        "name": "jarvis-client",
        "version": "1.0.0"
      },
      "io.modelcontextprotocol/clientCapabilities": {
        "elicitation": {}
      }
    }
  }
}
```

**Reponse** :
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "supportedVersions": ["2026-07-28"],
    "capabilities": {
      "tools": {"listChanged": true},
      "resources": {}
    },
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "jarvis-server",
        "version": "1.0.0"
      }
    },
    "ttlMs": 3600000,
    "cacheScope": "public"
  }
}
```

---

## 7. Creer un serveur MCP Python

### Installation
```bash
pip install mcp
```

### Serveur minimal
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mon-serveur")

@mcp.tool()
def envoyer_message(de: str, vers: str, priorite: int = 3, objet: str = "", corps: str = "") -> str:
    """Envoyer un message entre agents."""
    # Logique ici
    return f"Message envoye de {de} vers {vers}"

@mcp.resource("inbox://{agent}")
def lire_inbox(agent: str) -> str:
    """Lire les messages d'un agent."""
    # Logique ici
    return "Messages..."

if __name__ == "__main__":
    mcp.run()
```

### Lancement
```bash
# Stdio (local)
python mon-serveur.py

# HTTP (distant)
python mon-serveur.py --transport http --port 8080
```

---

## 8. SDK Python

| Package | Description |
|---|---|
| `mcp` | SDK officiel Python |
| `fastmcp` | Helper pour creer rapidement des serveurs |
| `mcp-client` | Client MCP pour Python |

**Installation** :
```bash
pip install mcp
```

**Documentation** : https://modelcontextprotocol.io/docs

---

## 9. Utilisation dans notre projet

### JARVIS comme serveur MCP
```python
from mcp.server.fastmcp import FastMCP

jarvis = FastMCP("jarvis")

@jarvis.tool()
def envoyer_message(de: str, vers: str, priorite: int, objet: str, corps: str) -> str:
    """Envoyer un message via JARVIS."""
    # Ecrire dans inbox/ et outbox/
    return "Message envoye"

@jarvis.tool()
def lire_messages(agent: str) -> str:
    """Lire les messages en attente."""
    # Lire inbox/<agent>.jsonl
    return "Messages..."

@jarvis.tool()
def activer_agent(agent: str, mission: str, session: str = "session-1") -> str:
    """Activer un agent via JARVIS."""
    # Envoyer message P1 bloquant
    return "Agent active"

if __name__ == "__main__":
    jarvis.run()
```

### Agents comme serveurs MCP
Chaque agent peut etre un serveur MCP qui expose ses capacites.
JARVIS route les appels vers le bon agent.
