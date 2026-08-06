# Spécification — Outil modifier-agents-md

**Version** : 0.1.0
**Statut** : Ébauche
**Date création** : 2026-08-05
**Agent** : Vulcain (création)

---

## Objectif

Spécifier l'outil `modifier-agents-md` qui modifie AGENTS.md de manière fiable.

---

## Besoins fonctionnels

### Entrées

| Entrée | Type | Description |
|---|---|---|
| `action` | string | "activer" ou "reactiver" |
| `agent` | string | Nom de l'agent (si activer) |
| `raison` | string | Raison du changement |
| `mission` | string | Description de la mission (optionnel) |

### Sorties

| Sortie | Type | Description |
|---|---|---|
| `succes` | boolean | true si la modification a réussi |
| `message` | string | Message de confirmation ou d'erreur |
| `fichier_modifie` | string | Chemin du fichier modifié |

---

## Besoins techniques

### Lecture des fichiers

```python
def lire_fichiers():
    # 1. Lire AGENTS.md
    # 2. Si action == "reactiver":
    #    - Lire agents/cerberus/corrections.md
    #    - Lire agents/cerberus/cerberus.md
    pass
```

### Modification de la section "Agent Principal Actuel"

```python
def modifier_section_principale(fichier, agent, role, raison):
    # Trouver la section "## Agent Principal Actuel"
    # Remplacer les valeurs
    # Garder le format markdown
    pass
```

### Ajout dans l'historique

```python
def ajouter_historique(fichier, agent, raison):
    # Trouver la section "## Historique des Agents"
    # Ajouter une nouvelle ligne
    # Formater avec la date actuelle
    pass
```

---

## Spécification des tests

### Test 1 : Activation réussie

**Entrée** : `action="activer", agent="Buffy", raison="Test"`
**Résultat attendu** : AGENTS.md mis à jour avec Buffy comme agent principal

### Test 2 : Réactivation réussie

**Entrée** : `action="reactiver", raison="Mission terminée"`
**Résultat attendu** : AGENTS.md mis à jour avec Cerberus comme agent principal

### Test 3 : Erreur - agent manquant

**Entrée** : `action="activer"` (sans agent)
**Résultat attendu** : Erreur "Agent requis pour l'action activer"

---

## Architecture

```
modifier-agents-md/
|-- modifier-agents-md.md      # Documentation
|-- modifier-agents-md.py      # Script Python
|-- modifier-agents-md.sh      # Script Bash
|-- test-modifier-agents-md.md # Tests
`-- spec/
    `-- spec-modifier-agents-md.md  # Cette spécification
```

---

## Contraintes

- Doit fonctionner sur Windows, Linux, Mac
- Doit lire les fichiers de Cerberus lors de la réactivation
- Doit préserver le format markdown
- Doit gérer les erreurs gracieusement

---

## Critères de succès

| Critère | Mesure |
|---|---|
| **Fiabilité** | 100% des tests passent |
| **Performance** | < 1 seconde |
| **Portabilité** | Fonctionne sur 3 systèmes |
| **Documentation** | Complète et claire |

---

