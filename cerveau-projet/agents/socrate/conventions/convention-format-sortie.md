---
identite:
  type: convention
  appartient_a: socrate
  version: "0.1.0"
  cree: "2026-08-20"
---

# Convention : Format de Sortie

## Fichier de sortie

UN SEUL fichier : `cerveau-projet/agents/socrate/missions-revision.md`

## Template

```markdown
# Missions de Revision -- [DATE]

## Resume
| Niveau | Nombre |
|---|---|
| URGENT | X |
| IMPORTANT | X |
| MOYEN | X |
| BAS | X |

## Missions

### [NIVEAU] Titre de la mission
- **Agent habilite** : [agent]
- **Description** : [ce qu'il faut faire]
- **Raison** : [pourquoi c'est necessaire]
- **Dependances** : [missions a faire avant]
- **Critere de succes** : [comment verifier que c'est fait]

---
```

## Regles

1. UN SEUL fichier, pas de supplements
2. Toute mission a un niveau (URGENT/IMPORTANT/MOYEN/BAS)
3. Toute mission a un agent habilite
4. Toute mission a un critere de succes
5. Les dependances sont tracees
