---
identite:
  type: outil
  appartient_a: matrice-data-outils
  commun: false
  flux: 2
  version: 1.0.0
---

# Outil DIALOGUER -- Interaction createur (Flux 2 seul)

## Porte unique

Cet outil est la porte unique pour toute interaction avec le createur.
Flux 2 seul : jamais utilise par le cameleon.

Porte PRIVEE (`commun: false`, `flux: 2`) : le lanceur croise le flux de
l appelant depuis cette carte (MO-434) -- un `cameleon` est REFUSE (code 2).
L identite se DECLARE avant le nom de la brique : `--appelant operateur`
(ou variable `MATRICE_APPELANT=operateur`). La regle complete vit dans la
fiche 0 de `manuel-outils.md` -- une seule source, ici ce n est qu un renvoi.

## Verbes

| Verbe | Usage | Codes retour |
|---|---|---|
| `dialoguer` | Pose une question au createur | 0=reponse, 1=timeout, 2=erreur |
| `plan` | Gere les todos | 0=succes, 2=erreur |

## Options dialoguer

| Option | Defaut | Description |
|---|---|---|
| `--question` | (requis) | Question a poser |
| `--choix` | (aucun) | Choix separes par virgule (min 2, max 10) |
| `--timeout` | 0 | Timeout secondes (0 = persistant) |
| `--json` | (non) | Sortie machine JSON |

## Options plan

| Option | Defaut | Description |
|---|---|---|
| `--todos` | (requis) | Liste JSON de todos |
| `--json` | (non) | Sortie machine JSON |

## Architecture

```
dialoguer/
  constants.py     -- Chemins, Flux 2, options
  commun.py        -- Validation, trace, BDD
  dialoguer/
    entry.py       -- Verbe dialoguer (question/choix/timeout)
  plan/
    entry.py       -- Verbe plan (todos)
  main.py          -- Point d'entree (sac a dos + dispatch)
```

## Garanties

- Flux 2 seul (jamais cameleon)
- Trace suivi-optimus (decision)
- Timeout configurable (0 = persistant)
- Compatible stdin interactive
- BDD suivi-optimus tracee
