---
identite:
  type: outil
  appartient_a: commun
  commun: true
---

# detecter-processus-residuels

**Version :** 0.1.1
**Statut :** ebauche
**Categorie :** Detecter

## Pourquoi cet outil ?

Les scripts temporaires et les tests laissent parfois des **processus
orphelins actifs** (python/node/bash) qui ne meurent pas. Sur Windows,
`ps aux` ne montre que les bash du terminal : les vrais residuels
(python.exe, node.exe) sont visibles via `Get-CimInstance`. Cet outil les
detecte proprement, avec justification, pour permettre ensuite au
nettoyeur (exclusif Hygie) de les terminer.

## Critere de detection

| Type | Definition |
|---|---|
| **PROJET** | Processus python/node/bash dont la commande reference le projet (`analyste-in-console`, `tmp-*`, `.zz-*`, `.tmp-*`, `cerveau-projet/`) |
| **ORPHELIN** | Processus dont le parent est mort (PPID inexistant parmi les processus vivants) |

## Liste blanche protegee

Jamais signales, jamais tuables : `freebuff` (le client), `unsloth` (le
studio python), `codebuff`.

## Usage

```bash
python3 detecter-processus-residuels.py
python3 detecter-processus-residuels.py --detail
python3 detecter-processus-residuels.py --rapport rapport-processus.md
python3 detecter-processus-residuels.py --verbose
```

## Options

| Option | Effet |
|---|---|
| `--detail` | Detail complet des commandes (200 car) |
| `--rapport <f>` | Ecrit le rapport markdown |
| `--verbose` | Affiche les details de detection (liste blanche incluse) |
| `--version` | Affiche la version |
| `--aide` | Affiche l aide complete |

## Sortie

- 0 residuel : `AUCUN RESIDUEL` (etat PROPRE)
- sinon : liste des processus (PID + nom + justification PROJET/ORPHELIN +
  commande) + compteur + verdict avec renvoi vers le nettoyeur

## Compatibilite

- Windows : `Get-CimInstance Win32_Process` via powershell
- Linux/macOS : `ps -eo pid,ppid,comm,args`

## Connexions

- `nettoyer-processus-residuels` : nettoyage (exclusif Hygie)
- `detecter-residus` : detection des residus FICHIERS (Hygie)
