---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Specification -- Protocole d'Identification des Agents
---

## Objectif

Garantir que chaque agent se reconnait et s'identifie avant de travailler.

---

## Architecture

```
cerveau-projet/
|-- AGENTS.md                    <- agent principal actuel
|-- agents/
|   |-- index-agents.md          <- point d'entree
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
2. Se presenter automatiquement
3. Verifier si la fiche existe
4. Si non -> creer la fiche + corrections
5. Lire corrections.md en priorite
6. Lire la fiche d'agent
7. Mettre a jour AGENTS.md
8. Confirmer l'identification
```

---

## Regles de validation

| Regle | Critere |
|---|---|
| **Lecture AGENTS.md** | Toujours lu en premier |
| **Presentation** | Chaque agent se presente |
| **Fiche** | Chaque agent a une fiche |
| **Corrections** | Les corrections sont lues en priorite |
| **Mise a jour** | AGENTS.md est mis a jour |
| **Confirmation** | L'identification est validee |

---

## Statut

- [rechercher] [OK] Dependances identifiees
- [verifier] [NON] Structure validee
- [analyser] [NON] Coherence verifiee
- [valider] [NON] Approuve
