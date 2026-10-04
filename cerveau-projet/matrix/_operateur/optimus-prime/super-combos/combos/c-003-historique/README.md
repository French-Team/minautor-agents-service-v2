---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# c-003-historique

> **Combo numerote c-003** -- le numero est OBLIGATOIRE et jamais reutilise
> (contrat de nommage obligatoire CV-008 -- BDD conventions-matrice,
> decision createur 2026-09-13).

Combo dedie a la BDD **Historiques des missions (historiques-missions.jsonl)** (`historique`).

> Historique des missions : trace append-only des missions finies, filtrable par type, tag ou date.
> Genere par `creer-combo.py` (imperatif 46) le 2026-09-13 10:43:41.

## Chaine

1. **lire** : outil `matrice/data/outils/bdd-historique/main.py`, commande `lire` (filtre `--tag <tag>`)
2. **normaliser** : compte les lignes utiles
3. **noter usage** : piste dans `matrice/data/outils/bdd-usages/main.py` (tags `combo,bdd,historique`)

## Usage

```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-003-historique/main.py executer [--tag <tag>] [--mission <id>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-003-historique/main.py lire [--tag <tag>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-003-historique/main.py status
```

## Tags de la BDD

mission,correction
