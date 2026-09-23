---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# espions-optimus -- Surveillance de la zone Optimus par la Matrice

> La Matrice surveille Optimus comme elle surveille ses BDD : ces espions
> SIGNALENT, ils ne reparent jamais (la reparation passe par Optimus).
> Decide par le createur (M-111) : la zone `_operateur/optimus-prime/`
> est la seule qui n etait couverte par aucun espion.

## Espions

| Espion | Role | Commande |
|---|---|---|
| integrite | Empreintes SHA des fichiers zone Optimus (detection de modification hors BDD) | `python espion-integrite-optimus.py enregistrer` / `verifier` |
| activite | File missions Optimus, frictions actives, verrous BDD non liberes | `python espion-activite-optimus.py` |

## Registre

`registre/registre.json` : empreintes de reference + date de pose.
Mis a jour par `enregistrer` APRES chaque evolution auto-validee.

## Zones surveillees (dans `_operateur/optimus-prime/`)

parcours/, protocoles/, conventions/, regles-immuables/,
super-combos/combos/outils/*.py, optimus-prime.md
(docs internes exclus : .bak, __pycache__)
