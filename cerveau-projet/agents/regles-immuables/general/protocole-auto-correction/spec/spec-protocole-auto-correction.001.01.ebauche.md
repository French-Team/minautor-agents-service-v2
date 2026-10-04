---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Specification -- Protocole d'Auto-Correction des Agents
---

## Objectif

Definir un systeme permettant aux agents de :
1. S'identifier de maniere unique
2. Corriger automatiquement leurs erreurs
3. Surcharger leur configuration sans impacter les autres
4. Devenir l'agent principal dynamiquement

---

## Architecture

```
projet-futur/
|-- AGENTS.md                    <- fichier dynamique (agent principal)
|-- cerveau-projet/
|   ``-- agents/
|   |-- index-agents.md          <- point d'entree
|   |-- fiche-agent-template.md  <- template de fiche
|   |-- corrections-template.md  <- template de corrections
|   ``-- [nom-agent]/
|       |-- [nom-agent].md       <- fiche de l'agent
|       ``-- corrections.md       <- surcharges/corrections
```

---

## Format des fichiers

### Fiche d'agent

| Section | Format | Obligatoire |
|---|---|---|
| En-tete YAML | YAML | [OK] |
| Vue d'ensemble | Markdown | [OK] |
| Specialites | Markdown | [OK] |
| Forces | Tableau | [OK] |
| Faiblesses | Tableau | [OK] |
| Style de travail | Markdown | [OK] |
| Limites | Liste | [OK] |
| Connexions | Tableau | [OK] |
| Historique | Tableau | [OK] |

### Corrections

| Section | Format | Obligatoire |
|---|---|---|
| En-tete YAML | YAML | [OK] |
| Regles specifiques | Markdown | [NON] |
| Surcharges | Markdown + YAML | [NON] |
| Corrections d'erreurs | Markdown | [NON] |
| Configuration specifique | YAML | [NON] |
| Statistiques | Tableau | [NON] |
| Notes de session | Markdown | [NON] |

---

## Workflow

```
1. Agent visite agents/
2. Verifie existence de sa fiche
3. Si non -> cree la fiche + corrections
4. Lit sa configuration (corrections en priorite)
5. Met a jour AGENTS.md
6. Travaille
7. Detecte erreurs -> ajoute dans corrections.md
8. Prochaine session -> lit les nouvelles corrections
```

---

## Regles de validation

| Regle | Critere |
|---|---|
| **Unicite** | Chaque agent a un seul dossier |
| **Autonomie** | Pas de partage de corrections |
| **Persistance** | Les corrections restent entre les sessions |
| **Dynamisme** | AGENTS.md est mis a jour a chaque session |
| **Tracabilite** | L'historique est conserve |

---

## Dependances

| Dependance | Type |
|---|---|
| `agents/` | Dossier obligatoire |
| `AGENTS.md` | Fichier obligatoire |
| Templates | Fichiers obligatoires |
| Convention protocoles | Reference |
| `protocole-installer-regles` | Protocole pour installer les regles immuables |
| `protocole-recherches-web` | Protocole pour les recherches web |

---

## Statut

- [rechercher] [OK] Dependances identifiees
- [verifier] [NON] Structure validee
- [analyser] [NON] Coherence verifiee
- [valider] [NON] Approuve
