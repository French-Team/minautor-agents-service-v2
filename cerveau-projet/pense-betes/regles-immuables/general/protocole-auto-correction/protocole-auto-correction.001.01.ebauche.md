# Protocole d'Auto-Correction des Agents

---

## Objectif

Permettre aux agents de :
1. **S'identifier** via une fiche d'agent personnelle
2. **Corriger** leurs propres erreurs de manière automatique
3. **Surcharger** leur configuration sans impacter les autres agents
4. **Devenir l'agent principal** en mettant à jour AGENTS.md

---

## Prérequis

- Le dossier `agents/` existe dans le cerveau-projet
- Les templates `fiche-agent-template.md` et `corrections-template.md` existent
- Le fichier `AGENTS.md` existe à la racine du projet (ou sera créé)

---

## Le Cycle d'Auto-Correction

```
VÉRIFIER → CRÉER/LIRE → APPLIQUER → TRAVAILLER → CORRIGER → RÉACTIVER
    1          2            3           4            5           6
```

| Étape | Action | Responsable |
|---|---|---|
| 1 | Vérifier l'existence de sa fiche | Agent |
| 2 | Créer ou lire sa fiche | Agent |
| 3 | Mettre à jour AGENTS.md | Agent |
| 4 | Exécuter la mission | Agent |
| 5 | Détecter et documenter les erreurs | Agent |
| 6 | Réactiver Cerberus | Agent |

---

## Étape 1 — Vérifier l'existence de sa fiche

```
1. Aller dans agents/
2. Chercher le dossier [nom-agent]/
3. Si le dossier existe → lire la fiche et les corrections
4. Si le dossier n'existe pas → le créer (voir Étape 2)
```

---

## Étape 2 — Créer sa fiche d'agent

```
1. Créer le dossier agents/[nom-agent]/
2. Copier fiche-agent-template.md → agents/[nom-agent]/[nom-agent].md
3. Copier corrections-template.md → agents/[nom-agent]/corrections.md
4. Remplir la fiche avec les informations de l'agent
5. Laisser les corrections vides (seront remplies à la détection d'erreurs)
```

### Structure créée

```
agents/[nom-agent]/
├── [nom-agent].md        ← fiche de l'agent
└── corrections.md         ← surcharges/corrections
```

---

## Étape 3 — Lire sa configuration

### Ordre de lecture

| Priorité | Fichier | Contenu |
|---|---|---|
| 1 | `corrections.md` | Règles spécifiques, surcharges, corrections |
| 2 | `[nom-agent].md` | Fiche principale (après surcharge) |

---

## Étape 4 — Mettre à jour AGENTS.md

```
1. Lire AGENTS.md à la racine du projet
2. Identifier la section de l'agent actuel
3. Mettre à jour la section avec les informations de l'agent
4. Si l'agent n'a pas encore de section, la créer
5. Marquer cet agent comme "agent principal"
```

### Structure de AGENTS.md

```markdown
# Agents du Cerveau-Projet

## Agent Principal Actuel

| Champ | Valeur |
|---|---|
| **Nom** | [nom-agent] |
| **Dernière mise à jour** | [date] |
| **Fiche** | [lien vers la fiche] |

## Historique des Agents

| Date | Agent | Raison du changement |
|---|---|---|
| [date] | [nom-agent] | [raison] |

## Configuration Active

[Configuration de l'agent principal actuel]
```

---

## Étape 5 — Appliquer les corrections (auto-correction)

```
1. Pendant le travail, détecter les erreurs ou patterns problématiques
2. Classifier l'erreur (règle, surcharge, correction, configuration)
3. Ajouter la correction dans agents/[nom-agent]/corrections.md
4. La correction sera appliquée automatiquement lors des prochaines sessions
```

### Types de corrections

| Type | Description | Emplacement |
|---|---|---|
| **Règle** | Nouvelle règle spécifique à l'agent | Section "Règles spécifiques" |
| **Surcharge** | Modification d'une section existante | Section "Surcharges" |
| **Correction** | Correction d'une erreur récurrente | Section "Corrections d'erreurs" |
| **Configuration** | Paramètre de travail spécifique | Section "Configuration spécifique" |

---

## Étape 6 — Passage de témoin (changement d'agent)

```
1. L'agent actuel termine sa session
2. Le nouvel agent visite agents/
3. Le nouvel agent lit sa fiche (ou la crée)
4. Le nouvel agent met à jour AGENTS.md
5. L'agent précédent conserve ses corrections
```

### Règles de passage

| Règle | Description |
|---|---|
| **Pas de suppression** | Les corrections de l'agent précédent restent |
| **Pas de partage** | Chaque agent a ses propres corrections |
| **AGENTS.md dynamique** | Seul l'agent principal y écrit |
| **Traçabilité** | L'historique des agents est conservé |

---

## Pièges courants

| Piège | Solution |
|---|---|
| Oublier de lire les corrections | Toujours lire `corrections.md` en premier |
| Partager les corrections | Chaque agent a son propre dossier |
| Ne pas mettre à jour AGENTS.md | C'est l'étape obligatoire avant de travailler |
| Supprimer les corrections d'un autre | Les corrections sont persistantes |
| Créer une fiche sans corrections | Toujours créer `corrections.md` (même vide) |

---

## Liens

- **Templates** : `agents/fiche-agent-template.md`, `agents/corrections-template.md`
- **Index** : `agents/index-agents.md`
- **Convention** : `pense-betes/conventions/protocoles/convention-protocoles.md`
- **Protocoles** : `protocole-installer-regles` -- installer les regles immuables
- **Protocoles** : `protocole-identification` -- identification des agents
- **Protocoles** : `protocole-recherches-web` -- recherches web
- **AGENTS.md** : `AGENTS.md` (racine du projet)
