# Spécification — Protocole d'Identification des Agents
---

## Objectif

Garantir que chaque agent se reconnaît et s'identifie avant de travailler.

---

## Architecture

```
cerveau-projet/
|-- AGENTS.md                    <- agent principal actuel
|-- agents/
|   |-- index-agents.md          <- point d'entrée
|   |-- fiche-agent-template.md  <- template de fiche
|   |-- corrections-template.md  <- template de corrections
|   ``-- [nom-agent]/
|       |-- [nom-agent].md       <- fiche de l'agent
|       ``-- corrections.md       <- surcharges/corrections
```

---

## Workflow

```
1. Lire AGENTS.md en premier
2. Se présenter automatiquement
3. Vérifier si la fiche existe
4. Si non -> créer la fiche + corrections
5. Lire corrections.md en priorité
6. Lire la fiche d'agent
7. Mettre à jour AGENTS.md
8. Confirmer l'identification
```

---

## Règles de validation

| Règle | Critère |
|---|---|
| **Lecture AGENTS.md** | Toujours lu en premier |
| **Présentation** | Chaque agent se présente |
| **Fiche** | Chaque agent a une fiche |
| **Corrections** | Les corrections sont lues en priorité |
| **Mise à jour** | AGENTS.md est mis à jour |
| **Confirmation** | L'identification est validée |

---

## Statut

- [rechercher] [OK] Dependances identifiees
- [verifier] [NON] Structure validee
- [analyser] [NON] Coherence verifiee
- [valider] [NON] Approuve
