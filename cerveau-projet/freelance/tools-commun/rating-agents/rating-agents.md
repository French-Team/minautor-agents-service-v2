# rating-agents

> "Le rating sert a identifier quel agent a des problemes pour qu'il soit repare."

| Champ | Valeur |
|---|---|
| **Version** | 0.1.0 |
| **Type** | outil commun (P1 : entry.py + fonctions/ + P10 os_path) |
| **Proprietaire** | Forge |
| **Cree** | 2026-08-23 |

---

## Paliers

| Sens | Paliers | Signification |
|---|---|---|
| HAUSSE | COPPER -> SILVER -> OR | performance reconnue |
| BAISSE | A_REVOIR -> A_REPARER -> DECLASSE | derapage leve / reparation requise / travail seul interdit |

## Contrat

```
python3 entry.py noter --agent <agent> --palier <palier> --motif "..." [--par <notateur>]
python3 entry.py lister [--agent <agent>]
python3 entry.py problemes
```

- Notateurs habilites : stark, jarvis, fury, rogers (D15: fonctions/paliers.py)
- `problemes` retourne code 1 si au moins un agent est en baisse = du travail existe
- Chaque note trace : date, agent, palier_avant, palier_apres, motif, par

## Donnees (D15)

`notes-agents.jsonl` (append-only) : une ligne JSON par note.

## Philosophie liee

Voir regles/philosophie/ : un agent en baisse n'est pas puni, il est
REPARE (education Chiron, mission de reparation). Le but est la sante
de l'equipe, pas la sanction.
