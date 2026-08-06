# Specification -- Outil mettre-a-jour-modifier-agents-md

**Version** : 0.1.0
**Statut** : Ebauche
**Date creation** : 2026-08-05
**Agent** : Vulcain (creation)

---

## Objectif

Specifier l'outil `mettre-a-jour-modifier-agents-md` qui modifie AGENTS.md de maniere fiable.

---

## Besoins fonctionnels

### Entrees

| Entree | Type | Description |
|---|---|---|
| `action` | string | "activer" ou "reactiver" |
| `agent` | string | Nom de l'agent (si activer) |
| `raison` | string | Raison du changement |
| `mission` | string | Description de la mission (optionnel) |

### Sorties

| Sortie | Type | Description |
|---|---|---|
| `succes` | boolean | true si la modification a reussi |
| `message` | string | Message de confirmation ou d'erreur |
| `fichier_modifie` | string | Chemin du fichier modifie |

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

## Specification des tests

### Test 1 : Activation reussie

**Entree** : `action="activer", agent="Buffy", raison="Test"`
**Resultat attendu** : AGENTS.md mis a jour avec Buffy comme agent principal

### Test 2 : Reactivation reussie

**Entree** : `action="reactiver", raison="Mission terminee"`
**Resultat attendu** : AGENTS.md mis a jour avec Cerberus comme agent principal

### Test 3 : Erreur - agent manquant

**Entree** : `action="activer"` (sans agent)
**Resultat attendu** : Erreur "Agent requis pour l'action activer"

---

## Architecture

```
mettre-a-jour-modifier-agents-md/
|-- mettre-a-jour-modifier-agents-md.md      # Documentation
|-- mettre-a-jour-modifier-agents-md.py      # Script Python
|-- mettre-a-jour-modifier-agents-md.sh      # Script Bash
|-- test-mettre-a-jour-modifier-agents-md.md # Tests
`-- spec/
    `-- spec-mettre-a-jour-modifier-agents-md.md  # Cette specification
```

---

## Contraintes

- Doit fonctionner sur Windows, Linux, Mac
- Doit lire les fichiers de Cerberus lors de la reactivation
- Doit preserver le format markdown
- Doit gerer les erreurs gracieusement

---

## Criteres de succes

| Critere | Mesure |
|---|---|
| **Fiabilite** | 100% des tests passent |
| **Performance** | < 1 seconde |
| **Portabilite** | Fonctionne sur 3 systemes |
| **Documentation** | Complete et claire |

---

