# Protocole Immuable -- Activation des Agents

> L'activation inclut OBLIGATOIREMENT la lecture du fichier de l'agent.

**Portee :** Tous les agents du cerveau-projet
**Prerequis :** AGENTS.md, fiche de l'agent, corrections de l'agent
**Statut :** prepare (class 02)
**Derniere mise a jour :** 2026-08-05

---

## Principe Fondamental

---

## Le Cycle d'Activation

```
CERBERUS -> IDENTIFIER -> LIRE -> ACTIVER -> TRAVAILLER -> REACTIVER -> [SECOND CONTROLE]
    1          2         3       4          5            6                7
```

| Etape | Action | Responsable |
|---|---|---|
| 1 | Cerberus analyse le besoin | Cerberus |
| 2 | Identifier l'agent adapte | Cerberus |
| 3 | Lire la fiche et les corrections | Cerberus |
| 4 | Activer dans AGENTS.md | Cerberus |
| 5 | Agent execute sa mission | Agent active |
| 6 | Reactiver Cerberus | Agent active |
| 7 | Si la mission figure dans la liste definie : activer Janus | Cerberus |

> **Second controle** : la liste des missions exigeant le second controle est dans la carte de decision de Cerberus. Janus controle, puis reactive Cerberus.

---

## Matrice de decision

| Besoin | Agent | Justification |
|---|---|---|
| Creer/modifier du contenu | Buffy | Developpeur principal |
| Explorer le code | Atlas | Explorateur |
| Valider un travail | Janus | Second controle -- active par Cerberus (liste definie) |
| Coordonner | Cerberus | Gardien de l'entree |

---

## Etape 3 -- Lecture de l'Agent

> **ETAPE OBLIGATOIRE -- Ne pas sauter !**

### Quand lire corrections.md ?

| Situation | Lire ? | Pourquoi |
|---|---|---|
| Premiere activation de l'agent | OUI | Decouvrir les regles |
| Activation normale (agent fonctionne) | NON | L'agent connait deja ses regles |
| Erreur detectee / debug | OUI | Comprendre ce qui a mal tourne |
| Test de l'agent | OUI | Verifier les corrections en cours |

### Regle

> **Ecrire dans corrections.md TOUJOURS, le relire UNIQUEMENT en cas de besoin.**

---

## Etape 4 -- Activation dans AGENTS.md

> **JAMAIS** `str_replace` ou `write_file` pour ce fichier critique.

### Commande d'activation

```bash
cerveau-projet/agents/tools/mettre-a-jour/mettre-a-jour-agents-md/mettre-a-jour-agents-md.sh activer "Agent" "Raison" "Mission"
```

---

## Etape 6 -- Reactivation de Cerberus

> **JAMAIS** `str_replace` ou `write_file` pour AGENTS.md.

### Commande de reactivation

```bash
cerveau-projet/agents/tools/mettre-a-jour/mettre-a-jour-agents-md/mettre-a-jour-agents-md.sh reactiver "Raison" "AgentPrecedent"
```

### Quand ?

```
AVANT de terminer la session.
```

---

## Regles d'Or

| Regle | Description |
|---|---|
| **Activation = Lecture** | Jamais d'activation sans lecture de la fiche |
| **Corrections = Ecriture** | TOUJOURS ecrire, relire UNIQUEMENT en cas d'erreur |
| **Documenter l'activation** | Raison et mission dans AGENTS.md |
| **Reactiver Cerberus** | Toujours revenir a Cerberus |
| **Pas de saut** | Ne jamais sauter une etape |
| **Utiliser mettre-a-jour-agents-md** | Pour toute modification d'AGENTS.md |

---

## Pieges Courants

| Piege | Solution |
|---|---|
| Activer sans lire la fiche | TOUJOURS lire [nom-agent].md |
| Relire corrections.md a tort | Le lire UNIQUEMENT en cas d'erreur |
| Oublier de documenter | Mettre a jour AGENTS.md immediatement |
| Ne pas reactiver Cerberus | C'est la DERNIERE action |
| Lire apres avoir agi | Lire AVANT de commencer |

---

## Liens

- **Protocole parent** : `demarrer.md` -- protocole de demarrage
- **Convention** : `convention-protocoles` -- comment creer des protocoles
- **Regle** : `regles-choisir-agent` -- comment choisir le bon agent
