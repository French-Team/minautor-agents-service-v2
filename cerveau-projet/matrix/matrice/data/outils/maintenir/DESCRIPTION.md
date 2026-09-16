---
identite:
  type: outil-maintenir
  appartient_a: matrice-data-outils
  version: 1.0.0
---

# Outil MAINTENIR -- Traiter les signalements maintenance

## Porte unique

Optimus utilise cet outil pour lire et traiter les signalements
du cameleon qui arrivent via intercom maintenance.

## Verbes

| Verbe | Usage | Codes retour |
|---|---|---|
| `maintenir --lister` | Liste les signalements en attente | 0=signaux, 1=vide |
| `maintenir --traiter` | Traite le plus critique | 0=traite, 1=rien |
| `maintenir --etat` | Etat de la maintenance | 0=OK |

## Flux

```
Cameleon -> signal -> inbox Matrice -> routeur -> maintenance inbox -> Optimus (maintenir)
```

## Priorite de traitement

1. `critique` -> reparation immediate, resume mission
2. `haute` -> reparation prioritaire
3. `moyenne` -> amelioration planifiee
4. `basse` -> file d'attente

## Garanties

- Tri par importance (critique en premier)
- Append-only historique
- Marquage traite (pas de double traitement)
- Flux 2 seul (jamais cameleon)
