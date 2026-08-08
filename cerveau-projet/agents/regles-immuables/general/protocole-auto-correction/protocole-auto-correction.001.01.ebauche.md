---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole d'Auto-Correction des Agents

---

## Objectif

Permettre aux agents de :
1. **S'identifier** via une fiche d'agent personnelle
2. **Corriger** leurs propres erreurs de maniere automatique
3. **Surcharger** leur configuration sans impacter les autres agents
4. **Devenir l'agent principal** en mettant a jour AGENTS.md

---

## Prerequis

- Le dossier `agents/` existe dans le cerveau-projet
- Les templates `fiche-agent-template.md` et `corrections-template.md` existent
- Le fichier `AGENTS.md` existe a la racine du projet (ou sera cree)

---

## Le Cycle d'Auto-Correction

```
VERIFIER -> CREER/LIRE -> APPLIQUER -> TRAVAILLER -> CORRIGER -> REACTIVER
    1          2            3           4            5           6
```

| Etape | Action | Responsable |
|---|---|---|
| 1 | Verifier l'existence de sa fiche | Agent |
| 2 | Creer ou lire sa fiche | Agent |
| 3 | Mettre a jour AGENTS.md | Agent |
| 4 | Executer la mission | Agent |
| 5 | Detecter et documenter les erreurs | Agent |
| 6 | Reactiver Cerberus | Agent |

---

## Etape 1 -- Verifier l'existence de sa fiche

```
1. Aller dans agents/
2. Chercher le dossier [nom-agent]/
3. Si le dossier existe -> lire la fiche et les corrections
4. Si le dossier n'existe pas -> le creer (voir Etape 2)
```

---

## Etape 2 -- Creer sa fiche d'agent

```
1. Creer le dossier agents/[nom-agent]/
2. Copier fiche-agent-template.md -> agents/[nom-agent]/[nom-agent].md
3. Copier corrections-template.md -> agents/[nom-agent]/corrections.md
4. Remplir la fiche avec les informations de l'agent
5. Laisser les corrections vides (seront remplies a la detection d'erreurs)
```

### Structure creee

```
agents/[nom-agent]/
|-- [nom-agent].md        <- fiche de l'agent
``-- corrections.md         <- surcharges/corrections
```

---

## Etape 3 -- Lire sa configuration

### Ordre de lecture

| Priorite | Fichier | Contenu |
|---|---|---|
| 1 | `corrections.md` | Regles specifiques, surcharges, corrections |
| 2 | `[nom-agent].md` | Fiche principale (apres surcharge) |

---

## Etape 4 -- Mettre a jour AGENTS.md

```
1. Lire AGENTS.md a la racine du projet
2. Identifier la section de l'agent actuel
3. Mettre a jour la section avec les informations de l'agent
4. Si l'agent n'a pas encore de section, la creer
5. Marquer cet agent comme "agent principal"
```

### Structure de AGENTS.md

```markdown
# Agents du Cerveau-Projet

## Agent Principal Actuel

| Champ | Valeur |
|---|---|
| **Nom** | [nom-agent] |
| **Derniere mise a jour** | [date] |
| **Fiche** | [lien vers la fiche] |

## Historique des Agents

| Date | Agent | Raison du changement |
|---|---|---|
| [date] | [nom-agent] | [raison] |

## Configuration Active

[Configuration de l'agent principal actuel]
```

---

## Etape 5 -- Appliquer les corrections (auto-correction)

```
1. Pendant le travail, detecter les erreurs ou patterns problematiques
2. Classifier l'erreur (regle, surcharge, correction, configuration)
3. Ajouter la correction dans agents/[nom-agent]/corrections.md
4. La correction sera appliquee automatiquement lors des prochaines sessions
```

### Types de corrections

| Type | Description | Emplacement |
|---|---|---|
| **Regle** | Nouvelle regle specifique a l'agent | Section "Regles specifiques" |
| **Surcharge** | Modification d'une section existante | Section "Surcharges" |
| **Correction** | Correction d'une erreur recurrente | Section "Corrections d'erreurs" |
| **Configuration** | Parametre de travail specifique | Section "Configuration specifique" |

---

## Etape 6 -- Passage de temoin (changement d'agent)

```
1. L'agent actuel termine sa session
2. Le nouvel agent visite agents/
3. Le nouvel agent lit sa fiche (ou la cree)
4. Le nouvel agent met a jour AGENTS.md
5. L'agent precedent conserve ses corrections
```

### Regles de passage

| Regle | Description |
|---|---|
| **Pas de suppression** | Les corrections de l'agent precedent restent |
| **Pas de partage** | Chaque agent a ses propres corrections |
| **AGENTS.md dynamique** | Seul l'agent principal y ecrit |
| **Tracabilite** | L'historique des agents est conserve |

---

## Pieges courants

| Piege | Solution |
|---|---|
| Oublier de lire les corrections | Toujours lire `corrections.md` en premier |
| Partager les corrections | Chaque agent a son propre dossier |
| Ne pas mettre a jour AGENTS.md | C'est l'etape obligatoire avant de travailler |
| Supprimer les corrections d'un autre | Les corrections sont persistantes |
| Creer une fiche sans corrections | Toujours creer `corrections.md` (meme vide) |

---

## Liens

- **Templates** : `agents/fiche-agent-template.md`, `agents/corrections-template.md`
- **Index** : `agents/index-agents.md`
- **Convention** : `agents/conventions/protocoles/convention-protocoles.md`
- **Protocoles** : `protocole-installer-regles` -- installer les regles immuables
- **Protocoles** : `protocole-identification` -- identification des agents
- **Protocoles** : `protocole-recherches-web` -- recherches web
- **AGENTS.md** : `AGENTS.md` (racine du projet)
