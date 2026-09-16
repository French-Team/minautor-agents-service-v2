---
identite:
  type: outil-signaler
  appartient_a: matrice-data-outils
  version: 1.0.0
---

# Outil SIGNALER -- Signaler un probleme outil

## Porte unique

Le cameleon utilise cet outil quand un outil est en panne, buggy,
ou qu'une amelioration manquante empeche sa mission.

Le message est depose dans la boite Matrice inbox.
La Matrice le route ensuite vers intercom maintenance (Optimus).

## Verbes

| Verbe | Usage | Codes retour |
|---|---|---|
| `signal` | Signale un probleme outil | 0=depot OK, 2=erreur |

## Options signal

| Option | Obligatoire | Description |
|---|---|---|
| `--outil` | oui | Nom de l'outil en probleme |
| `--niveau` | oui | `critique`, `haute`, `moyenne`, `basse` |
| `--description` | oui | Description du probleme (min 10 car.) |
| `--mission` | non | ID mission interrompue (ex: M-042) |
| `--erreur` | non | Message d'erreur exact |
| `--json` | non | Sortie machine JSON |

## Niveaux d'importance

| Niveau | Signification | Action Optimus |
|---|---|---|
| `critique` | Panne totale, mission impossible | Reparation immediate, resume mission |
| `haute` | Bug bloquent, mission ralentie | Reparation prioritaire |
| `moyenne` | Amelioration manquante | Amelioration planifiee |
| `basse` | Souhait, pas bloquant | File d'attente |

## Flux

```
Cameleon -> signal -> inbox Matrice -> routeur -> maintenance inbox -> Optimus
```

## Garanties

- Message JSONL append-only
- Niveau d'importance oblige
- Depot dans boite Matrice (pas directement dans maintenance)
- La Matrice fait le routing (separation des flux)
