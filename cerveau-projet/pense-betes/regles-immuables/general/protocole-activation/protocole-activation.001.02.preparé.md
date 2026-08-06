# Protocole Immuable — Activation des Agents

> L'activation inclut OBLIGATOIREMENT la lecture du fichier de l'agent.

**Portée :** Tous les agents du cerveau-projet
**Prérequis :** AGENTS.md, fiche de l'agent, corrections de l'agent
**Statut :** préparé (class 02)
**Dernière mise à jour :** 2026-08-05

---

## Principe Fondamental

---

## Le Cycle d'Activation

```
CERBERUS → IDENTIFIER → LIRE → ACTIVER → TRAVAILLER → RÉACTIVER → [SECOND CONTRÔLE]
    1          2         3       4          5            6                7
```

| Étape | Action | Responsable |
|---|---|---|
| 1 | Cerberus analyse le besoin | Cerberus |
| 2 | Identifier l'agent adapté | Cerberus |
| 3 | Lire la fiche et les corrections | Cerberus |
| 4 | Activer dans AGENTS.md | Cerberus |
| 5 | Agent exécute sa mission | Agent activé |
| 6 | Réactiver Cerberus | Agent activé |
| 7 | Si la mission figure dans la liste définie : activer Janus | Cerberus |

> **Second contrôle** : la liste des missions exigeant le second contrôle est dans la carte de décision de Cerberus. Janus contrôle, puis réactive Cerberus.

---

## Matrice de décision

| Besoin | Agent | Justification |
|---|---|---|
| Créer/modifier du contenu | Buffy | Développeur principal |
| Explorer le code | Atlas | Explorateur |
| Valider un travail | Janus | Second contrôle — activé par Cerberus (liste définie) |
| Coordonner | Cerberus | Gardien de l'entrée |

---

## Étape 3 — Lecture de l'Agent

> **ÉTAPE OBLIGATOIRE — Ne pas sauter !**

### Quand lire corrections.md ?

| Situation | Lire ? | Pourquoi |
|---|---|---|
| Première activation de l'agent | OUI | Découvrir les règles |
| Activation normale (agent fonctionne) | NON | L'agent connaît déjà ses règles |
| Erreur détectée / debug | OUI | Comprendre ce qui a mal tourné |
| Test de l'agent | OUI | Vérifier les corrections en cours |

### Règle

> **Écrire dans corrections.md TOUJOURS, le relire UNIQUEMENT en cas de besoin.**

---

## Étape 4 — Activation dans AGENTS.md

> **JAMAIS** `str_replace` ou `write_file` pour ce fichier critique.

### Commande d'activation

```bash
cerveau-projet/agents/tools/corriger/modifier-agents-md/modifier-agents-md.sh activer "Agent" "Raison" "Mission"
```

---

## Étape 6 — Réactivation de Cerberus

> **JAMAIS** `str_replace` ou `write_file` pour AGENTS.md.

### Commande de réactivation

```bash
cerveau-projet/agents/tools/corriger/modifier-agents-md/modifier-agents-md.sh reactiver "Raison" "AgentPrecedent"
```

### Quand ?

```
AVANT de terminer la session.
```

---

## Règles d'Or

| Règle | Description |
|---|---|
| **Activation = Lecture** | Jamais d'activation sans lecture de la fiche |
| **Corrections = Écriture** | TOUJOURS écrire, relire UNIQUEMENT en cas d'erreur |
| **Documenter l'activation** | Raison et mission dans AGENTS.md |
| **Réactiver Cerberus** | Toujours revenir à Cerberus |
| **Pas de saut** | Ne jamais sauter une étape |
| **Utiliser modifier-agents-md** | Pour toute modification d'AGENTS.md |

---

## Pièges Courants

| Piège | Solution |
|---|---|
| Activer sans lire la fiche | TOUJOURS lire [nom-agent].md |
| Relire corrections.md à tort | Le lire UNIQUEMENT en cas d'erreur |
| Oublier de documenter | Mettre à jour AGENTS.md immédiatement |
| Ne pas réactiver Cerberus | C'est la DERNIÈRE action |
| Lire après avoir agi | Lire AVANT de commencer |

---

## Liens

- **Protocole parent** : `demarrer.md` — protocole de démarrage
- **Convention** : `convention-protocoles` — comment créer des protocoles
- **Règle** : `regles-choisir-agent` — comment choisir le bon agent
